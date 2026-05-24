# QUICK START GUIDE

## System Status: ✓ READY

All dependencies installed and verified!

## Start the Application

```bash
python app.py
```

Then open: **http://localhost:5000**

## How to Use

1. **Click "Start"** - Begin recording the conversation
2. **Click "Pause"** - Pause/resume recording (optional)
3. **Click "Stop"** - End recording and start transcription
4. **Wait 5-10 seconds** - Transcription processes locally
5. **View Results** - See transcript and medical summary

## Features

✓ **Multilingual** - Handles English + Tamil (code-switching supported)
✓ **Free** - 100% free, runs locally, no cloud costs
✓ **Private** - Data never leaves your machine
✓ **Fast** - 5-10 seconds for 1 minute of audio
✓ **Offline** - Works without internet after setup

## Troubleshooting

### If recording doesn't work:
- Allow microphone permissions in browser
- Use Chrome/Edge (best compatibility)

### If transcription fails:
- Make sure you spoke clearly for at least 2-3 seconds
- Check that FFmpeg is installed: `ffmpeg -version`
- Restart the app: Stop (Ctrl+C) and run `python app.py` again

### If app won't start:
- Check Python is installed: `python --version`
- Reinstall dependencies: `pip install Flask flask-cors faster-whisper`

## Model Options

Edit `app.py` line 17 to change model size:

```python
# Faster, less accurate (75MB)
model = WhisperModel("tiny", device="cpu", compute_type="int8")

# Balanced - DEFAULT (150MB)
model = WhisperModel("base", device="cpu", compute_type="int8")

# More accurate, slower (500MB)
model = WhisperModel("small", device="cpu", compute_type="int8")
```

## File Locations

- **Recordings**: `uploads/` folder
- **App**: `app.py`
- **Frontend**: `index.html`
- **Model Cache**: `C:\Users\Admin\.cache\huggingface\`

## Support

For issues, check:
1. All dependencies installed: `python test_complete.py`
2. FFmpeg working: `ffmpeg -version`
3. Port 5000 not in use
4. Microphone permissions granted

---

**Cost: ₹0 (FREE!)** | **Privacy: 100% Local** | **Languages: English + Tamil**
