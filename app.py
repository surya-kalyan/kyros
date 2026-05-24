import os
import time
import re
import json
import tempfile
import requests as http_requests
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from faster_whisper import WhisperModel

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

INITIAL_PROMPT = (
    "This is a doctor-patient conversation in Tamil and English. "
    "நோயாளி மருத்துவரிடம் பேசுகிறார். "
    "வலி, காய்ச்சல், மருந்து, மாத்திரை, tablet, medicine, fever, pain."
)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "<your_groq_api_key_here>")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

print("Loading Whisper model...")
model = WhisperModel("medium", device="cpu", compute_type="int8")
print("Model loaded!")


def transcribe_audio(filepath, prev_text=""):
    prompt = (INITIAL_PROMPT + " " + prev_text[-200:]).strip() if prev_text else INITIAL_PROMPT
    segments, info = model.transcribe(
        filepath,
        language=None,
        task="transcribe",
        vad_filter=True,
        vad_parameters={
            "min_silence_duration_ms": 500,
            "speech_pad_ms": 400,
            "min_speech_duration_ms": 100,
            "threshold": 0.3,
        },
        beam_size=5,
        best_of=5,
        patience=2,
        condition_on_previous_text=True,
        initial_prompt=prompt,
        temperature=[0.0, 0.2, 0.4],
        no_speech_threshold=0.6,
        compression_ratio_threshold=2.8,
        word_timestamps=False,
        repetition_penalty=1.1,
    )
    parts = [s.text.strip() for s in segments if s.text.strip()]
    return " ".join(parts), info.language


def generate_summary_groq(transcript):
    try:
        resp = http_requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": GROQ_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a medical assistant. Extract structured information from a doctor-patient "
                            "conversation transcript which may be in Tamil, English, or mixed language. "
                            "Return ONLY a JSON object with these keys: overview (string), symptoms (list), "
                            "medications (list), diagnosis (list), followup (list). Be concise and clinical."
                        )
                    },
                    {"role": "user", "content": f"Transcript:\n{transcript}"}
                ],
                "temperature": 0.3,
                "max_tokens": 1024,
                "response_format": {"type": "json_object"}
            },
            timeout=15
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        return json.loads(content)
    except Exception as e:
        print(f"Groq summary error: {e}")
        return None


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/transcribe_chunk', methods=['POST'])
def transcribe_chunk():
    """Receives a small audio chunk (~3s), returns transcript immediately."""
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio'}), 400

    prev_text = request.form.get('prev_text', '')
    chunk = request.files['audio']

    # Save to temp file
    suffix = '.webm'
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=UPLOAD_FOLDER) as f:
        chunk.save(f)
        tmp_path = f.name

    wav_path = tmp_path.replace('.webm', '.wav')
    try:
        file_size = os.path.getsize(tmp_path)
        print(f"[chunk] file_size={file_size}")
        if file_size < 200:
            return jsonify({'text': '', 'language': ''})

        ret = os.system(f'ffmpeg -y -i "{tmp_path}" -ar 16000 -ac 1 -f wav "{wav_path}" -loglevel error')
        print(f"[chunk] ffmpeg ret={ret}, wav_exists={os.path.exists(wav_path)}")
        if ret != 0 or not os.path.exists(wav_path):
            return jsonify({'text': '', 'language': ''})

        text, lang = transcribe_audio(wav_path, prev_text)
        print(f"[chunk] lang={lang} | {text}")
        return jsonify({'text': text, 'language': lang})
    except Exception as e:
        print(f"Chunk transcription error: {e}")
        return jsonify({'text': '', 'language': '', 'error': str(e)})
    finally:
        for p in [tmp_path, wav_path]:
            try:
                os.unlink(p)
            except Exception:
                pass


@app.route('/upload', methods=['POST'])
def upload_audio():
    """Full recording upload — returns transcript + medical summary."""
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file'}), 400

    file = request.files['audio']
    filename = secure_filename(f"{int(time.time())}.webm")
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    if os.path.getsize(filepath) < 1000:
        return jsonify({'status': 'FAILED', 'transcript': 'Audio too small.', 'summary': 'N/A'})

    wav_path = filepath.replace('.webm', '.wav')
    try:
        os.system(f'ffmpeg -y -i "{filepath}" -ar 16000 -ac 1 -f wav "{wav_path}" -loglevel quiet')
        transcribe_path = wav_path if os.path.exists(wav_path) else filepath
        transcript, lang = transcribe_audio(transcribe_path)
        if not transcript:
            transcript = "No speech detected."
        medical_info = generate_summary_groq(transcript) or extract_medical_info(transcript)
        return jsonify({
            'status': 'COMPLETED',
            'transcript': transcript,
            'medical_info': medical_info,
            'language': lang
        })
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({'status': 'FAILED', 'error': str(e)}), 500


def extract_medical_info(transcript):
    sentences = [s.strip() for s in re.split(r'[.!?\n]+', transcript) if len(s.strip()) > 5]

    def find_sentences(keywords):
        return list(dict.fromkeys(
            s for s in sentences if any(k in s.lower() for k in keywords)
        ))

    symptoms = find_sentences([
        'pain','ache','fever','cough','cold','headache','nausea','vomit','dizzy',
        'fatigue','tired','weak','swelling','rash','bleeding','breathless','chest',
        'stomach','throat','itching','burning','numbness',
        'வலி','காய்ச்சல்','இருமல்','தலைவலி','வாந்தி','மயக்கம்','சோர்வு'
    ])
    medications = find_sentences([
        'tablet','capsule','syrup','medicine','drug','dose','mg','ml','paracetamol',
        'antibiotic','prescribed','take','twice','thrice','daily','morning','night',
        'மாத்திரை','மருந்து','டோஸ்'
    ])
    diagnosis = find_sentences([
        'diagnosed','diagnosis','infection','disease','disorder','positive','negative',
        'test','result','scan','x-ray','blood','urine','sugar','pressure','diabetes',
        'நோய்','பரிசோதனை','ரிசல்ட்'
    ])
    followup = find_sentences([
        'follow','revisit','come back','next visit','appointment','rest','avoid',
        'diet','drink water','exercise','advice',
        'மீண்டும் வாருங்கள்','ஓய்வு','தண்ணீர்'
    ])

    used = set(symptoms[:2] + medications[:2] + diagnosis[:2] + followup[:1])
    overview_pool = [s for s in sentences if s not in used]
    overview = ' '.join(overview_pool[:3]) or ' '.join(sentences[:3])

    return {
        'overview':    overview,
        'symptoms':    symptoms[:5],
        'medications': medications[:5],
        'diagnosis':   diagnosis[:4],
        'followup':    followup[:4],
    }


@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    text = data.get('text', '').strip()
    target_lang = data.get('target_lang', 'English')
    if not text:
        return jsonify({'error': 'No text'}), 400
    try:
        resp = http_requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": GROQ_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": f"Translate the following medical conversation transcript to {target_lang}. Preserve medical terms accurately. Return only the translated text, nothing else."
                    },
                    {"role": "user", "content": text}
                ],
                "temperature": 0.2,
                "max_tokens": 2048,
            },
            timeout=15
        )
        resp.raise_for_status()
        translated = resp.json()["choices"][0]["message"]["content"]
        return jsonify({'translated': translated})
    except Exception as e:
        print(f"Translation error: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 7860)), threaded=True)
