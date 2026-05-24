"""
Test script to verify all dependencies are working
"""
import sys
import os

print("=" * 60)
print("KYROS MEDICAL RECORDER - SYSTEM CHECK")
print("=" * 60)

# Test 1: Check Python version
print("\n1. Checking Python version...")
print(f"   [OK] Python {sys.version.split()[0]}")

# Test 2: Check Flask
print("\n2. Checking Flask...")
try:
    import flask
    print(f"   [OK] Flask {flask.__version__}")
except ImportError as e:
    print(f"   [FAIL] Flask not found: {e}")
    sys.exit(1)

# Test 3: Check Flask-CORS
print("\n3. Checking Flask-CORS...")
try:
    import flask_cors
    print(f"   [OK] Flask-CORS installed")
except ImportError as e:
    print(f"   [FAIL] Flask-CORS not found: {e}")
    sys.exit(1)

# Test 4: Check Faster Whisper
print("\n4. Checking Faster Whisper...")
try:
    from faster_whisper import WhisperModel
    print(f"   [OK] Faster Whisper installed")
except ImportError as e:
    print(f"   [FAIL] Faster Whisper not found: {e}")
    sys.exit(1)

# Test 5: Check FFmpeg
print("\n5. Checking FFmpeg...")
import subprocess
try:
    result = subprocess.run(['ffmpeg', '-version'], 
                          capture_output=True, 
                          text=True, 
                          timeout=5)
    if result.returncode == 0:
        version_line = result.stdout.split('\n')[0]
        print(f"   [OK] {version_line}")
    else:
        print(f"   [FAIL] FFmpeg error")
        sys.exit(1)
except FileNotFoundError:
    print(f"   [FAIL] FFmpeg not found in PATH")
    print(f"   Install: choco install ffmpeg")
    sys.exit(1)
except Exception as e:
    print(f"   [FAIL] FFmpeg check failed: {e}")
    sys.exit(1)

# Test 6: Check uploads folder
print("\n6. Checking uploads folder...")
if not os.path.exists('uploads'):
    os.makedirs('uploads')
    print(f"   [OK] Created uploads folder")
else:
    print(f"   [OK] Uploads folder exists")

# Test 7: Load Whisper model (this will download if needed)
print("\n7. Loading Whisper model (first time will download ~150MB)...")
try:
    model = WhisperModel("base", device="cpu", compute_type="int8")
    print(f"   [OK] Whisper model loaded successfully")
except Exception as e:
    print(f"   [FAIL] Failed to load model: {e}")
    sys.exit(1)

# Test 8: Check index.html
print("\n8. Checking index.html...")
if os.path.exists('index.html'):
    print(f"   [OK] index.html found")
else:
    print(f"   [FAIL] index.html not found")
    sys.exit(1)

print("\n" + "=" * 60)
print("[SUCCESS] ALL CHECKS PASSED!")
print("=" * 60)
print("\nYou can now run the app:")
print("  python app.py")
print("\nThen open: http://localhost:5000")
print("=" * 60)
