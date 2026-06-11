FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for audio and microphone support
RUN apt-get update && apt-get install -y \
    build-essential \
    espeak \
    alsa-utils \
    portaudio19-dev \
    libpulse-dev \
    pulseaudio \
    git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install build tools
RUN pip install --upgrade pip setuptools wheel

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY main.py .
COPY setup.sh .

# Ensure scripts are executable
RUN chmod +x main.py

# Set environment variables for Ollama
ENV OLLAMA_HOST=http://host.docker.internal:11434

# Expose port for potential future web UI
EXPOSE 5000

# Run the application
CMD ["python3", "main.py"]
