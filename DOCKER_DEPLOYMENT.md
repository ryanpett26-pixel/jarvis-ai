# Docker Deployment Guide

## Overview
JARVIS AI can be deployed using Docker and Docker Compose for isolated, containerized execution with integrated Ollama LLM backend.

## Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- 2GB+ available disk space
- Microphone and speaker (for audio passthrough)

## Quick Start

### Using docker-compose (Recommended)
```bash
# Clone the repository
git clone https://github.com/ryanpett26-pixel/jarvis-ai.git
cd jarvis-ai

# Start containers (builds image automatically)
docker-compose up -d

# View logs
docker-compose logs -f jarvis-ai

# Stop containers
docker-compose down
```

## Architecture

### Services
1. **jarvis-ai**: Main application container
   - Python 3.12 runtime
   - All dependencies pre-installed
   - Audio device passthrough for microphone/speaker
   - Connects to Ollama API

2. **ollama**: LLM backend (optional but recommended)
   - Ollama container running on port 11434
   - Access via `http://ollama:11434` from jarvis-ai service
   - Provides `llama3` and other models

### Networks
- Containers communicate via `jarvis-network` bridge network
- Ollama listens on `0.0.0.0:11434` within container
- Exposed to host on port `11434`

## Configuration

### Environment Variables
Edit `docker-compose.yml` to customize:

```yaml
environment:
  OLLAMA_HOST: "http://ollama:11434"  # Ollama API endpoint
  PYTHONUNBUFFERED: "1"                # Real-time logging
```

### Audio Passthrough
Audio device `/dev/snd` is mounted for microphone/speaker access:
```yaml
devices:
  - /dev/snd

volumes:
  - /dev/snd:/dev/snd
```

For macOS with Docker Desktop, audio passthrough may require additional setup.

## Building the Image Manually

```bash
docker build -t jarvis-ai:1.0.0 .
```

### Build Arguments (optional)
```bash
docker build -t jarvis-ai:custom \
  --build-arg PYTHON_VERSION=3.11 .
```

## Running Individual Container

```bash
# Without Ollama (connect to external API)
docker run -it \
  -e OLLAMA_HOST=http://external-host:11434 \
  -v /dev/snd:/dev/snd \
  --device /dev/snd \
  jarvis-ai:1.0.0

# With local Ollama
docker run -it \
  -e OLLAMA_HOST=http://ollama-container:11434 \
  --network jarvis-network \
  -v /dev/snd:/dev/snd \
  --device /dev/snd \
  jarvis-ai:1.0.0
```

## Troubleshooting

### "No space left on device"
Clean up unused Docker resources:
```bash
docker system prune -a --volumes
```

### Audio not working
1. Verify `/dev/snd` exists on host: `ls -l /dev/snd/`
2. Check device permissions: `stat /dev/snd/`
3. Ensure Docker has device access

### Ollama not responding
```bash
# Check Ollama container
docker-compose logs ollama

# Test connection from jarvis-ai
docker-compose exec jarvis-ai \
  curl -s http://ollama:11434/api/tags
```

### Container exits immediately
```bash
# Check logs
docker-compose logs jarvis-ai

# Run with interactive terminal
docker-compose run --rm jarvis-ai /bin/bash
```

## Performance Tips

1. **Use volume mounts** for development:
   ```yaml
   volumes:
     - .:/app  # Development mode
   ```

2. **Resource limits** (add to docker-compose.yml):
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '2'
         memory: 2G
   ```

3. **Enable BuildKit** for faster builds:
   ```bash
   DOCKER_BUILDKIT=1 docker build .
   ```

## Production Deployment

For production, consider:
- Use specific image tags instead of `latest`
- Configure resource limits
- Use separate networks for security
- Mount volumes for data persistence
- Use environment files for secrets
- Enable restart policies
- Set up health checks

Example health check:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## Pushing to Registry

```bash
# Tag image
docker tag jarvis-ai:1.0.0 your-registry/jarvis-ai:1.0.0

# Push to Docker Hub or custom registry
docker push your-registry/jarvis-ai:1.0.0
```

## References
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Ollama Documentation](https://ollama.ai/)

---
For issues or questions, open an issue on [GitHub](https://github.com/ryanpett26-pixel/jarvis-ai/issues).
