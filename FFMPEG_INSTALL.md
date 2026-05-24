# FFmpeg Installation Guide

FFmpeg is required for Faster Whisper to process audio files.

## Windows

### Option 1: Using Chocolatey (Recommended)
```bash
choco install ffmpeg
```

### Option 2: Manual Installation
1. Download from: https://www.gyan.dev/ffmpeg/builds/
2. Extract to `C:\ffmpeg`
3. Add to PATH:
   - Search "Environment Variables" in Windows
   - Edit "Path" variable
   - Add `C:\ffmpeg\bin`
4. Restart terminal

### Option 3: Using Scoop
```bash
scoop install ffmpeg
```

## Verify Installation
```bash
ffmpeg -version
```

You should see FFmpeg version information.

## Troubleshooting

If you get "ffmpeg not found" error:
1. Make sure FFmpeg is in your PATH
2. Restart your terminal/IDE
3. Try running: `where ffmpeg` (Windows) to verify installation
