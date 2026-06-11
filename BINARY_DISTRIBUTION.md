# Standalone Binary Distribution Guide

## Overview
JARVIS AI v1.0.0 is available as standalone executables for Linux/Mac and Windows, eliminating the need for Python installation.

## Download
Download the appropriate binary for your system from [GitHub Releases](https://github.com/ryanpett26-pixel/jarvis-ai/releases/tag/v1.0.0):

- **Linux/Mac**: `main` (executable binary)
- **Windows**: `main.bat` (batch launcher)

## System Requirements

### All Platforms
- Microphone and speakers
- 500MB free disk space
- Stable internet connection (for Ollama API)

### Linux/Mac
- Ubuntu 20.04+, Debian 11+, or macOS 10.14+
- Audio libraries: `espeak`, `alsa-utils` (usually pre-installed)

### Windows
- Windows 10/11 (64-bit)
- Python 3.10+ must be installed and in PATH
- VC++ Redistributable (usually already installed)

## Installation & Usage

### Linux/Mac

1. **Download the binary**:
   ```bash
   wget https://github.com/ryanpett26-pixel/jarvis-ai/releases/download/v1.0.0/main
   # or use curl:
   curl -L -O https://github.com/ryanpett26-pixel/jarvis-ai/releases/download/v1.0.0/main
   ```

2. **Make it executable**:
   ```bash
   chmod +x main
   ```

3. **Run it**:
   ```bash
   ./main
   ```

### Windows

1. **Download the batch launcher**:
   - Download `main.bat` from the release page
   - Save it to your preferred location

2. **Run it**:
   - Double-click `main.bat`, or
   - Open Command Prompt and run:
     ```cmd
     main.bat
     ```

## Initial Setup

### 1. Ollama Installation (Required for Voice Interaction)

**Linux/Mac**:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve  # Start Ollama in background or separate terminal
```

**Windows**:
- Download from [ollama.ai](https://ollama.ai)
- Run installer
- Ollama will start automatically

### 2. Pull a Model

```bash
ollama pull llama3
# or for smaller model:
ollama pull neural-chat
```

### 3. Verify Setup

Test that everything works:
```bash
# Test speech recognition
python3 -c "import speech_recognition as sr; print('✓ Speech Recognition ready')"

# Test text-to-speech
python3 -c "import pyttsx3; print('✓ Text-to-Speech ready')"

# Test system diagnostics
python3 -c "import psutil; print(f'✓ System Monitoring ready (CPU: {psutil.cpu_percent()}%)')"

# Test Ollama connection
curl http://localhost:11434/api/tags
```

## Usage

Once running, JARVIS AI will:
1. **Greet you**: "Jarvis online. How can I assist you today?"
2. **Listen for voice input**: Say commands or questions
3. **Process requests**: Responds with voice and text
4. **Display diagnostics**: Shows system info via animated particle orb

### Voice Commands

- **"Jarvis, run diagnostics"** - Display system CPU and memory usage
- **"Jarvis, what time is it?"** - Get current time
- **"Jarvis, [any question]"** - Get response from LLM model
- **"You up?"** - Check if JARVIS is responsive

## Troubleshooting

### "No module named 'speech_recognition'"
**Solution**: Install Python dependencies
```bash
pip install -r requirements.txt
```

### "Ollama connection failed"
**Solutions**:
1. Verify Ollama is running: `ollama serve`
2. Check endpoint: `curl http://localhost:11434/api/tags`
3. Verify model is pulled: `ollama list`

### "Microphone not detected"
**Linux/Mac**:
```bash
# Install audio libraries
sudo apt-get install -y espeak alsa-utils portaudio19-dev python3-pyaudio
```

**Windows**:
- Check Sound Settings > Privacy & Security > Microphone
- Ensure app has microphone permission
- Test with: `python -m speech_recognition`

### "Text-to-speech not working"
```bash
# Test TTS engine
python3 -c "import pyttsx3; engine = pyttsx3.init(); engine.say('test'); engine.runAndWait()"

# If not working, try:
# Linux: sudo apt-get install espeak
# Mac: brew install espeak
# Windows: Already built-in
```

### Application crashes on startup
1. Check Python version: `python3 --version` (must be 3.10+)
2. Verify all dependencies: `pip list`
3. Check system audio: `speaker-test -t sine -c 2`

## Performance Optimization

### Reduce Latency
- Use a lighter model: `ollama pull neural-chat` instead of `llama3`
- Close unnecessary applications
- Ensure stable internet connection

### Lower Memory Usage
- Quantized models: `ollama pull neural-chat:q2_K`
- Reduce particle count in `main.py`
- Close other resource-heavy apps

## Advanced Configuration

### Custom Ollama Endpoint
Edit connection in code or set environment variable:
```bash
export OLLAMA_HOST=http://remote-server:11434
./main
```

### Custom Port for Web UI (Future)
```bash
export JARVIS_PORT=5001
./main
```

## System Compatibility

| OS | Version | Status | Notes |
|---|---------|--------|-------|
| Linux | Ubuntu 20.04+ | ✓ Tested | Works best with PulseAudio |
| Linux | Debian 11+ | ✓ Tested | - |
| macOS | 10.14+ | ✓ Tested | Audio passthrough may need setup |
| Windows | 10/11 (64-bit) | ✓ Tested | Requires Python in PATH |

## Uninstallation

Simply delete the binary:
```bash
rm ./main        # Linux/Mac
del main.bat     # Windows
```

To fully uninstall Ollama:
```bash
# Linux
sudo systemctl stop ollama
sudo systemctl disable ollama
sudo rm -rf /usr/local/bin/ollama

# macOS
brew uninstall ollama

# Windows
Control Panel > Programs > Uninstall
```

## Getting Help

- Check [GitHub Issues](https://github.com/ryanpett26-pixel/jarvis-ai/issues)
- Review [OLLAMA_SETUP.md](OLLAMA_SETUP.md) for detailed Ollama setup
- See [DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md) for containerized setup

---
For feedback or bug reports, [create an issue](https://github.com/ryanpett26-pixel/jarvis-ai/issues/new) on GitHub.
