#!/usr/bin/env python3
"""
Test script for docling-serve on RunPod
"""

import requests
import json
import time
from pathlib import Path

def test_docling_serve():
    """Test docling-serve API"""
    
    base_url = "http://localhost:5001"
    
    print("🧪 Testing docling-serve on RunPod...")
    
    # Test 1: Check if service is running
    try:
        response = requests.get(f"{base_url}/docs", timeout=10)
        if response.status_code == 200:
            print("✅ Service is running")
        else:
            print(f"❌ Service returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to service: {e}")
        return False
    
    # Test 2: Test with a sample URL
    test_url = "https://arxiv.org/pdf/2305.03393.pdf"
    
    payload = {
        "files": [test_url],
        "from_formats": ["pdf"],
        "to_formats": ["json"],
        "do_ocr": True,
        "ocr_engine": "easyocr",
        "image_export_mode": "embedded"
    }
    
    print(f"📄 Testing with URL: {test_url}")
    
    try:
        response = requests.post(
            f"{base_url}/v1alpha/convert/source",
            json=payload,
            headers={"accept": "application/json"},
            timeout=300  # 5 minutes timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Conversion successful!")
            print(f"📊 Result size: {len(str(result))} characters")
            return True
        else:
            print(f"❌ Conversion failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        return False

def test_local_file():
    """Test with a local file if available"""
    
    test_file = "test_files/sample.pdf"
    if not Path(test_file).exists():
        print(f"⚠️ Test file not found: {test_file}")
        return False
    
    base_url = "http://localhost:5001"
    
    payload = {
        "files": [test_file],
        "from_formats": ["pdf"],
        "to_formats": ["json"],
        "do_ocr": True,
        "ocr_engine": "easyocr"
    }
    
    print(f"📁 Testing with local file: {test_file}")
    
    try:
        response = requests.post(
            f"{base_url}/v1alpha/convert/source",
            json=payload,
            headers={"accept": "application/json"},
            timeout=300
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Local file conversion successful!")
            return True
        else:
            print(f"❌ Local file conversion failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error with local file: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting docling-serve tests...")
    
    # Wait for service to start
    print("⏳ Waiting for service to start...")
    time.sleep(10)
    
    # Run tests
    success = test_docling_serve()
    
    if success:
        print("\n🎉 All tests passed! Ready for RunPod deployment.")
    else:
        print("\n❌ Tests failed. Check the configuration.")
    
    # Test local file if available
    test_local_file() 