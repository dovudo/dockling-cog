# RunPod Setup Instructions

## Quick Start

### 1. Choose RunPod Template
- **Template:** `PyTorch 2.3.1 (CUDA 12.1)`
- **GPU:** RTX 4090 or RTX 3090 (24GB VRAM recommended)
- **RAM:** 32GB+ recommended

### 2. After Pod Starts

```bash
# Clone your repository
git clone https://github.com/your-username/dockling-replica.git
cd dockling-replica

# Build and run
docker-compose up --build
```

### 3. Test the Service

```bash
# Check if service is running
curl http://localhost:5001/docs

# Run test script
python test_runpod.py
```

### 4. API Usage

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
dockling-replica/
├── Dockerfile.runpod      # RunPod optimized Dockerfile
├── docker-compose.yml     # Local/RunPod deployment
├── test_runpod.py         # Test script
├── predict.py             # Main application
└── test_files/            # Test files directory
```

## Troubleshooting

### If service doesn't start:
```bash
# Check logs
docker-compose logs

# Check if port is available
netstat -tlnp | grep 5001
```

### If CUDA issues:
```bash
# Check CUDA
nvidia-smi

# Check PyTorch CUDA
python -c "import torch; print(torch.cuda.is_available())"
```

## Performance Tips

- Use `DOCLING_SERVE_ENG_LOC_NUM_WORKERS=1` for single GPU
- Set `CUDA_VISIBLE_DEVICES=0` for first GPU
- Monitor GPU usage with `nvidia-smi` 