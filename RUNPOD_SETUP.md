# RunPod Setup Instructions (No Docker)

## Quick Start

### 1. Choose RunPod Template
- **Template:** `Better PyTorch CUDA12.4`
- **GPU:** RTX 4090 or RTX 3090 (24GB VRAM recommended)
- **RAM:** 32GB+ recommended

### 2. Test Cog for Replicate

```bash
# Connect to RunPod
ssh l1m1ybn41rdld2-6441116e@ssh.runpod.io -i ~/.ssh/id_ed25519

# Go to workspace
cd /workspace

# Clone your repository
git clone https://github.com/dovudo/dockling-cog.git
cd dockling-cog

# Test Cog (this is what you need!)
python test_cog_on_runpod.py
```

### 3. Manual Cog Testing

If you want to test Cog manually:

```bash
# Install Cog
pip install cog

# Test build
cog build

# Test predict with URL
cog predict -i file_url="https://arxiv.org/pdf/2305.03393.pdf" -i to_formats=json

# Test predict with file
curl -o test.pdf https://arxiv.org/pdf/2305.03393.pdf
cog predict -i file=@test.pdf -i to_formats=json
```

### 4. Alternative: Direct docling-serve

If you want to test just docling-serve (not Cog):

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

### 5. Test the Service

```bash
# Check if service is running
curl http://localhost:5001/docs

# Run test script
python test_runpod.py
```

### 6. API Usage

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
├── test_cog_on_runpod.py   # Test Cog for Replicate compatibility
├── runpod_direct.py        # Direct Python runner (no Docker)
├── test_runpod.py          # Test script for docling-serve
├── predict.py              # Main Cog application
└── test_files/             # Test files directory
```

## What Each Test Does

### `test_cog_on_runpod.py` - Tests Cog for Replicate
1. **Installs Cog** - same as on your local machine
2. **Tests Cog build** - verifies Docker image builds correctly
3. **Tests Cog schema** - checks input/output definitions
4. **Tests Cog predict** - runs actual predictions with file/URL
5. **Reports results** - tells you if it's ready for Replicate

### `runpod_direct.py` - Tests docling-serve directly
1. **Installs docling-serve** - without Cog wrapper
2. **Starts service** - runs docling-serve directly
3. **Tests API** - verifies the underlying service works

## Troubleshooting

### If Cog tests fail:
```bash
# Check Cog installation
which cog
cog --version

# Check Docker (if needed)
docker --version

# Check Python packages
pip list | grep cog
```

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