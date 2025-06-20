#!/usr/bin/env python3
"""
Test Cog script on RunPod to verify Replicate compatibility
"""

import subprocess
import sys
import os
import tempfile
import json
from pathlib import Path

def install_cog():
    """Install Cog on RunPod"""
    print("📦 Installing Cog...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "cog"], check=True)
        print("✅ Cog installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Cog: {e}")
        return False

def test_cog_build():
    """Test Cog build process"""
    print("🔨 Testing Cog build...")
    
    try:
        # Run cog build
        result = subprocess.run(
            ["cog", "build"],
            capture_output=True,
            text=True,
            cwd="/workspace/dockling-cog"
        )
        
        if result.returncode == 0:
            print("✅ Cog build successful!")
            return True
        else:
            print(f"❌ Cog build failed:")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Cog build error: {e}")
        return False

def test_cog_predict():
    """Test Cog predict with sample input"""
    print("🧪 Testing Cog predict...")
    
    # Create a test file
    test_file = "/workspace/dockling-cog/test_files/test.pdf"
    Path(test_file).parent.mkdir(exist_ok=True)
    
    # Download a sample PDF if test file doesn't exist
    if not Path(test_file).exists():
        print("📥 Downloading test PDF...")
        try:
            subprocess.run([
                "curl", "-o", test_file,
                "https://arxiv.org/pdf/2305.03393.pdf"
            ], check=True)
        except:
            print("⚠️ Could not download test file, using URL instead")
            test_file = "https://arxiv.org/pdf/2305.03393.pdf"
    
    # Test with file upload
    if Path(test_file).exists():
        print(f"📁 Testing with file: {test_file}")
        try:
            result = subprocess.run([
                "cog", "predict", "-i", f"file=@{test_file}", "-i", "to_formats=json"
            ], capture_output=True, text=True, cwd="/workspace/dockling-cog")
            
            if result.returncode == 0:
                print("✅ Cog predict with file successful!")
                print(f"Output: {result.stdout[:500]}...")
                return True
            else:
                print(f"❌ Cog predict with file failed:")
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
        except Exception as e:
            print(f"❌ Cog predict with file error: {e}")
    
    # Test with URL
    print("🌐 Testing with URL...")
    try:
        result = subprocess.run([
            "cog", "predict", "-i", "file_url=https://arxiv.org/pdf/2305.03393.pdf", 
            "-i", "to_formats=json"
        ], capture_output=True, text=True, cwd="/workspace/dockling-cog")
        
        if result.returncode == 0:
            print("✅ Cog predict with URL successful!")
            print(f"Output: {result.stdout[:500]}...")
            return True
        else:
            print(f"❌ Cog predict with URL failed:")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Cog predict with URL error: {e}")
        return False

def test_cog_schema():
    """Test Cog schema generation"""
    print("📋 Testing Cog schema...")
    
    try:
        result = subprocess.run(
            ["cog", "predict", "--help"],
            capture_output=True,
            text=True,
            cwd="/workspace/dockling-cog"
        )
        
        if result.returncode == 0:
            print("✅ Cog schema generated successfully!")
            print("📊 Available inputs:")
            print(result.stdout)
            return True
        else:
            print(f"❌ Cog schema failed:")
            print(f"STDERR: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Cog schema error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Cog for Replicate on RunPod")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("/workspace/dockling-cog/cog.yaml").exists():
        print("❌ cog.yaml not found. Please run this from the project directory.")
        print("Expected: /workspace/dockling-cog/cog.yaml")
        return
    
    # Install Cog
    if not install_cog():
        return
    
    # Test Cog build
    if not test_cog_build():
        print("❌ Cog build failed - this will fail on Replicate too")
        return
    
    # Test Cog schema
    if not test_cog_schema():
        print("❌ Cog schema failed - this will cause issues on Replicate")
        return
    
    # Test Cog predict
    if not test_cog_predict():
        print("❌ Cog predict failed - this indicates runtime issues")
        return
    
    print("\n🎉 All Cog tests passed!")
    print("✅ Your Cog script is ready for Replicate!")
    print("\n📝 Next steps:")
    print("1. Push to Replicate: cog push r8.im/dovudo/dockling")
    print("2. Test on Replicate web interface")
    print("3. Monitor for any runtime issues")

if __name__ == "__main__":
    main() 