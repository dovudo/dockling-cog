# RunPod Setup Instructions (No Docker)

## Quick Start

### 1. Choose RunPod Template
- **Template:** `Better PyTorch CUDA12.4`
- **GPU:** RTX 4090 or RTX 3090 (24GB VRAM recommended)
- **RAM:** 32GB+ recommended

### 2. After Pod Starts

```bash
# Connect to RunPod
ssh l1m1ybn41rdld2-6441116e@ssh.runpod.io -i ~/.ssh/id_ed25519

# Go to workspace
cd /workspace

# Clone your repository
git clone https://github.com/dovudo/dockling-cog.git
cd dockling-cog

# Run direct Python script (no Docker needed)
python runpod_direct.py
```

### 3. Alternative Manual Setup

If you prefer manual setup:

```bash
# Install dependencies
pip install docling-serve requests python-multipart

# Set environment variables
export DOCLING_SERVE_PORT=5001
export DOCLING_SERVE_MAX_SYNC_WAIT=600
export DOCLING_SERVE_ENG_KIND=local
export DOCLING_SERVE_ENG_LOC_NUM_WORKERS=2
export CUDA_VISIBLE_DEVICES=0

# Start docling-serve
docling-serve run
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
├── runpod_direct.py       # Direct Python runner (no Docker)
├── test_runpod.py         # Test script
├── predict.py             # Main application
└── test_files/            # Test files directory
```

## Troubleshooting

### If service doesn't start:
```bash
# Check if docling-serve is installed
which docling-serve

# Check Python packages
pip list | grep docling

# Check port availability
netstat -tlnp | grep 5001

# Check logs in the terminal where you ran the script
```

### If CUDA issues:
```bash
# Check CUDA
nvidia-smi

# Check PyTorch CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Check CUDA version
nvcc --version
```

### If dependencies fail:
```bash
# Update pip
pip install --upgrade pip

# Install with specific version
pip install docling-serve==latest

# Check Python version
python --version
```

## Performance Tips

- Use `DOCLING_SERVE_ENG_LOC_NUM_WORKERS=1` for single GPU
- Set `CUDA_VISIBLE_DEVICES=0` for first GPU
- Monitor GPU usage with `nvidia-smi`
- Use `htop` to monitor CPU and memory usage

## Running in Background

To run the service in the background:

```bash
# Start in background
nohup python runpod_direct.py > docling.log 2>&1 &

# Check if running
ps aux | grep docling

# View logs
tail -f docling.log

# Stop background process
pkill -f "python runpod_direct.py"
``` 