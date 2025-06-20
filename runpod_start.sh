#!/bin/bash

# RunPod startup script for Better PyTorch CUDA12.4
# This script builds and runs the docling-serve container

set -e

echo "🚀 Starting Docling on RunPod..."

# Check if we're in the right directory
if [ ! -f "Dockerfile.runpod" ]; then
    echo "❌ Dockerfile.runpod not found. Please run this script from the project directory."
    exit 1
fi

# Check CUDA availability
echo "🔍 Checking CUDA availability..."
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi
else
    echo "⚠️  nvidia-smi not found. CUDA might not be available."
fi

# Check PyTorch CUDA
echo "🔍 Checking PyTorch CUDA..."
python -c "import torch; print(f'PyTorch CUDA available: {torch.cuda.is_available()}')"

# Build the Docker image
echo "🔨 Building Docker image..."
docker build -f Dockerfile.runpod -t dockling-runpod .

# Stop any existing container
echo "🛑 Stopping existing containers..."
docker stop dockling-container 2>/dev/null || true
docker rm dockling-container 2>/dev/null || true

# Run the container
echo "🚀 Starting docling-serve container..."
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

# Wait for service to start
echo "⏳ Waiting for service to start..."
sleep 10

# Check if service is running
echo "🔍 Checking service status..."
if curl -f http://localhost:5001/docs > /dev/null 2>&1; then
    echo "✅ Service is running successfully!"
    echo "📊 Service URL: http://localhost:5001"
    echo "📚 API docs: http://localhost:5001/docs"
else
    echo "❌ Service failed to start. Checking logs..."
    docker logs dockling-container
    exit 1
fi

echo "🎉 Docling is ready to use!"
echo ""
echo "📝 Test commands:"
echo "  curl http://localhost:5001/docs"
echo "  python test_runpod.py"
echo ""
echo "📊 Monitor logs:"
echo "  docker logs -f dockling-container" 