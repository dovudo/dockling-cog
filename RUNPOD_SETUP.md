# RunPod Setup Instructions

## Quick Start

### 1. Choose RunPod Template
- **Template:** `Better PyTorch CUDA12.4`
- **GPU:** RTX 4090 or RTX 3090 (24GB VRAM recommended)
- **RAM:** 32GB+ recommended

### 2. After Pod Starts

```bash
# Clone your repository
git clone https://github.com/dovudo/dockling-cog.git
cd dockling-cog

# Make script executable and run
chmod +x runpod_start.sh
./runpod_start.sh
```

### 3. Alternative Manual Setup

If you prefer manual setup:

```bash
# Clone repository
git clone https://github.com/dovudo/dockling-cog.git
cd dockling-cog

# Build Docker image
docker build -f Dockerfile.runpod -t dockling-runpod .

# Run container
docker run -d \
    --name dockling-container \
    --gpus all \
    -p 5001:5001 \
    -e DOCLING_SERVE_PORT=5001 \
    -e DOCLING_SERVE_MAX_SYNC_WAIT=600 \
    -e DOCLING_SERVE_ENG_KIND=local \
    -e DOCLING_SERVE_ENG_LOC_NUM_WORKERS=2 \
    -e CUDA_VISIBLE_DEVICES=0 \
    dockling-runpod
```

### 4. Test the Service

```bash
# Check if service is running
curl http://localhost:5001/docs

# Run test script
python test_runpod.py
```

### 5. API Usage

```bash
# Test with URL
curl -X POST http://localhost:5001/v1alpha/convert/source \
  -H "Content-Type: application/json" \
  -d '{
    "files": ["https://arxiv.org/pdf/2305.03393.pdf"],
    "to_formats": ["json"],
    "do_ocr": true
  }'
```

## Files Structure
```
dockling-cog/
├── Dockerfile.runpod      # RunPod optimized Dockerfile
├── runpod_start.sh        # Startup script for RunPod
├── test_runpod.py         # Test script
├── predict.py             # Main application
└── test_files/            # Test files directory
```

## Troubleshooting

### If service doesn't start:
```bash
# Check logs
docker logs dockling-container

# Check if port is available
netstat -tlnp | grep 5001

# Restart container
docker restart dockling-container
```

### If CUDA issues:
```bash
# Check CUDA
nvidia-smi

# Check PyTorch CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Check container GPU access
docker exec dockling-container nvidia-smi
```

### Container management:
```bash
# Stop container
docker stop dockling-container

# Start container
docker start dockling-container

# Remove container
docker rm dockling-container

# View logs
docker logs -f dockling-container
```

## Performance Tips

- Use `DOCLING_SERVE_ENG_LOC_NUM_WORKERS=1` for single GPU
- Set `CUDA_VISIBLE_DEVICES=0` for first GPU
- Monitor GPU usage with `nvidia-smi`
- Use `docker stats dockling-container` to monitor resource usage 