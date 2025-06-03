#!/usr/bin/env python3
"""
Test Railway deployment
Replace YOUR_RAILWAY_URL with your actual Railway URL
"""

import requests
import json

# Replace this with your actual Railway URL
RAILWAY_URL = "https://your-app-name.railway.app"

def test_railway_deployment():
    print(f"🧪 Testing Railway deployment at: {RAILWAY_URL}")
    print("=" * 60)
    
    # Test health check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{RAILWAY_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed!")
            data = response.json()
            print(f"   Response: {data}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test root endpoint
    print("\n2️⃣ Testing Root Endpoint...")
    try:
        response = requests.get(f"{RAILWAY_URL}/", timeout=10)
        if response.status_code == 200:
            print("✅ Root endpoint working!")
            data = response.json()
            print(f"   API: {data.get('message', 'N/A')}")
            print(f"   Description: {data.get('description', 'N/A')}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test API documentation
    print("\n3️⃣ Testing API Documentation...")
    try:
        response = requests.get(f"{RAILWAY_URL}/docs", timeout=10)
        if response.status_code == 200:
            print("✅ API documentation accessible!")
            print(f"   📖 View docs at: {RAILWAY_URL}/docs")
        else:
            print(f"❌ API docs failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API docs error: {e}")
    
    # Test transcription (optional)
    print("\n4️⃣ Transcription Test (Optional)")
    test_transcription = input("Test transcription with sample audio? (y/N): ").lower().strip()
    
    if test_transcription in ['y', 'yes']:
        print("🎵 Testing transcription...")
        
        audio_url = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"
        
        try:
            print("📤 Sending transcription request...")
            response = requests.post(
                f"{RAILWAY_URL}/transcribe-url",
                data={"audio_url": audio_url},
                timeout=300  # 5 minutes
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
            print("⏰ Transcription timed out (normal for long audio)")
        except Exception as e:
            print(f"❌ Transcription error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Railway Deployment Test Complete!")
    print(f"🌐 Your API is live at: {RAILWAY_URL}")
    print(f"📖 Interactive docs: {RAILWAY_URL}/docs")
    print(f"🔗 Share this URL with anyone!")
    
    print("\n📋 Quick Commands:")
    print(f"curl {RAILWAY_URL}/health")
    print(f'curl -X POST "{RAILWAY_URL}/transcribe-url" -d "audio_url=https://example.com/audio.mp3"')

if __name__ == "__main__":
    print("📝 Instructions:")
    print("1. Replace RAILWAY_URL in this script with your actual Railway URL")
    print("2. Run: python test_railway.py")
    print()
    test_railway_deployment()
