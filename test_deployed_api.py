#!/usr/bin/env python3
"""
Test script for deployed AudioToText API
Usage: python test_deployed_api.py https://your-deployed-url.com
"""

import sys
import requests
import json
import time

def test_api(base_url):
    """Test the deployed API endpoints."""
    
    if not base_url.startswith('http'):
        base_url = f"https://{base_url}"
    
    print(f"🧪 Testing AudioToText API at: {base_url}")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Root Endpoint
    print("\n2️⃣ Testing Root Endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Root endpoint working!")
            data = response.json()
            print(f"   API: {data.get('message')}")
            print(f"   Description: {data.get('description')}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test 3: API Documentation
    print("\n3️⃣ Testing API Documentation...")
    try:
        response = requests.get(f"{base_url}/docs", timeout=10)
        if response.status_code == 200:
            print("✅ API documentation accessible!")
            print(f"   📖 View docs at: {base_url}/docs")
        else:
            print(f"❌ API docs failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API docs error: {e}")
    
    # Test 4: Transcription (if user wants to test)
    print("\n4️⃣ Transcription Test (Optional)")
    test_transcription = input("Do you want to test transcription? (y/N): ").lower().strip()
    
    if test_transcription in ['y', 'yes']:
        print("🎵 Testing transcription with sample audio...")
        
        # Sample audio URL
        audio_url = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"
        
        try:
            print(f"📤 Sending transcription request...")
            response = requests.post(
                f"{base_url}/transcribe-url",
                data={"audio_url": audio_url},
                timeout=300  # 5 minutes for transcription
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Transcription successful!")
                print(f"📝 Transcript preview: {result['transcript'][:100]}...")
                print(f"📊 Word count: {result['metadata']['word_count']}")
                print(f"🎯 Confidence: {result['metadata']['confidence']}")
                print(f"⏱️ Duration: {result['metadata']['audio_duration']} seconds")
            else:
                print(f"❌ Transcription failed: {response.status_code}")
                print(f"   Error: {response.text}")
        
        except requests.exceptions.Timeout:
            print("⏰ Transcription timed out (this is normal for long audio files)")
        except Exception as e:
            print(f"❌ Transcription error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 API Testing Complete!")
    print(f"🌐 Your API is live at: {base_url}")
    print(f"📖 Documentation: {base_url}/docs")
    print(f"🔗 Share this URL with others to let them use your API!")
    
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python test_deployed_api.py <your-api-url>")
        print("Example: python test_deployed_api.py https://my-app.railway.app")
        print("Example: python test_deployed_api.py abc123.ngrok.io")
        sys.exit(1)
    
    api_url = sys.argv[1]
    test_api(api_url)

if __name__ == "__main__":
    main()
