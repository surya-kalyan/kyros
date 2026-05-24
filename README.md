# Medical Conversation Recorder (FREE - Offline)

Web app for recording and transcribing multilingual (English + Tamil) doctor-patient conversations with automatic summarization. **100% FREE - runs locally with no cloud costs!**

## Features
- ✅ Record audio with play/pause/stop controls
- ✅ Multilingual speech-to-text (English + Tamil)
- ✅ Real-time transcription (no waiting!)
- ✅ Automatic medical summary generation
- ✅ Completely FREE - no AWS/cloud costs
- ✅ Works offline after setup

## Tech Stack
- **Frontend**: HTML/CSS/JS (MediaRecorder API)
- **Backend**: Flask + Python
- **Speech-to-Text**: Faster Whisper (OpenAI Whisper optimized)
- **Summarization**: Rule-based extractive summary

## Setup

### 1. Install FFmpeg (Required)

**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# OR download from: https://ffmpeg.org/download.html
```

**Linux:**
```bash
sudo apt install ffmpeg
```

**Mac:**
```bash
brew install ffmpeg
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

**Note**: First run will download the Whisper model (~150MB). This happens automatically.

### 3. Run the Application
```bash
python app.py
```

Open browser: `http://localhost:5000`

## Usage
1. Click **Start** to begin recording
2. Use **Pause** to pause/resume
3. Click **Stop** to end recording
4. Transcription happens instantly (5-10 seconds)
5. View transcript and medical summary

## Model Options

You can change the Whisper model size in `app.py`:

```python
# Faster, less accurate (75MB)
model = WhisperModel("tiny", device="cpu", compute_type="int8")

# Balanced (default) (150MB)
model = WhisperModel("base", device="cpu", compute_type="int8")

# More accurate, slower (500MB)
model = WhisperModel("small", device="cpu", compute_type="int8")

# Best accuracy (1.5GB) - requires GPU
model = WhisperModel("medium", device="cuda", compute_type="float16")
```

## Why Faster Whisper?
- ✅ **100% FREE** - no API costs
- ✅ Supports 99+ languages including Tamil
- ✅ Runs locally - no internet needed after setup
- ✅ Privacy - data never leaves your machine
- ✅ 4x faster than original Whisper
- ✅ Handles code-switching (English + Tamil mix)

## Performance
- **Tiny model**: ~2-3 seconds for 1 minute audio
- **Base model**: ~5-10 seconds for 1 minute audio
- **Small model**: ~15-20 seconds for 1 minute audio

## Cost
**Total: ₹0 (FREE!)** 🎉

## Notes
- Audio is recorded in WebM format
- Transcription happens on your local machine
- First run downloads the model automatically
- Files are stored locally in `uploads/` folder
- Works completely offline after initial setup
