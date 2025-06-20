#!/usr/bin/env python3
"""
Direct docling-serve runner for RunPod (without Docker)
"""

import subprocess
import time
import requests
import sys
import os
from pathlib import Path

def install_dependencies():
    """Install required packages"""
    print("📦 Installing dependencies...")
    
    packages = [
        "docling-serve",
        "requests", 
        "python-multipart"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    
    return True

def check_cuda():
    """Check CUDA availability"""
    print("🔍 Checking CUDA availability...")
    
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        print(f"PyTorch CUDA available: {cuda_available}")
        
        if cuda_available:
            print(f"CUDA device count: {torch.cuda.device_count()}")
            print(f"Current device: {torch.cuda.current_device()}")
            print(f"Device name: {torch.cuda.get_device_name()}")
        
        return cuda_available
    except ImportError:
        print("❌ PyTorch not available")
        return False

def start_docling_serve():
    """Start docling-serve directly"""
    print("🚀 Starting docling-serve...")
    
    # Set environment variables
    env = os.environ.copy()
    env.update({
        "DOCLING_SERVE_PORT": "5001",
        "DOCLING_SERVE_MAX_SYNC_WAIT": "600",
        "DOCLING_SERVE_ENG_KIND": "local",
        "DOCLING_SERVE_ENG_LOC_NUM_WORKERS": "2",
        "CUDA_VISIBLE_DEVICES": "0",
        "PYTHONUNBUFFERED": "1"
    })
    
    try:
        # Start docling-serve
        process = subprocess.Popen(
            ["docling-serve", "run"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print(f"✅ docling-serve started with PID: {process.pid}")
        return process
        
    except FileNotFoundError:
        print("❌ docling-serve command not found")
        return None
    except Exception as e:
        print(f"❌ Failed to start docling-serve: {e}")
        return None

def wait_for_service(process, timeout=60):
    """Wait for service to be ready"""
    print("⏳ Waiting for service to start...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get("http://localhost:5001/docs", timeout=5)
            if response.status_code == 200:
                print("✅ Service is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        # Check if process is still running
        if process.poll() is not None:
            print("❌ Service process died")
            stdout, stderr = process.communicate()
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
        
        time.sleep(2)
    
    print("❌ Service failed to start within timeout")
    return False

def test_service():
    """Test the service with a sample request"""
    print("🧪 Testing service...")
    
    test_url = "https://arxiv.org/pdf/2305.03393.pdf"
    
    payload = {
        "files": [test_url],
        "from_formats": ["pdf"],
        "to_formats": ["json"],
        "do_ocr": True,
        "ocr_engine": "easyocr",
        "image_export_mode": "embedded"
    }
    
    try:
        response = requests.post(
            "http://localhost:5001/v1alpha/convert/source",
            json=payload,
            headers={"accept": "application/json"},
            timeout=300
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Test successful!")
            print(f"📊 Result size: {len(str(result))} characters")
            return True
        else:
            print(f"❌ Test failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Starting Docling on RunPod (Direct Mode)")
    print("=" * 50)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return
    
    # Check CUDA
    if not check_cuda():
        print("⚠️ CUDA not available, but continuing...")
    
    # Start service
    process = start_docling_serve()
    if not process:
        print("❌ Failed to start service")
        return
    
    try:
        # Wait for service
        if not wait_for_service(process):
            print("❌ Service failed to start")
            return
        
        # Test service
        if test_service():
            print("\n🎉 Docling is ready to use!")
            print("📊 Service URL: http://localhost:5001")
            print("📚 API docs: http://localhost:5001/docs")
            print("\n📝 Keep this terminal open to keep the service running.")
            print("Press Ctrl+C to stop the service.")
            
            # Keep the process running
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Stopping service...")
                process.terminate()
                process.wait()
                print("✅ Service stopped")
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping service...")
        process.terminate()
        process.wait()
        print("✅ Service stopped")

if __name__ == "__main__":
    main() 