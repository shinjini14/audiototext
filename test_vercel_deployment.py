#!/usr/bin/env python3
"""
Test your Vercel deployment
Replace YOUR_VERCEL_URL with your actual Vercel URL
"""

import requests
import json

# Replace this with your actual Vercel URL
VERCEL_URL = "https://your-app.vercel.app"

def test_vercel_api():
    print(f"🧪 Testing Vercel deployment at: {VERCEL_URL}")
    print("=" * 60)
    
    # Test health check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{VERCEL_URL}/health", timeout=15)
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return
    
    # Test API docs
    print("\n2️⃣ Testing API Documentation...")
    try:
        response = requests.get(f"{VERCEL_URL}/docs", timeout=15)
        if response.status_code == 200:
            print("✅ API documentation accessible!")
            print(f"📖 View docs at: {VERCEL_URL}/docs")
        else:
            print(f"❌ API docs failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API docs error: {e}")
    
    # Test root endpoint
    print("\n3️⃣ Testing Root Endpoint...")
    try:
        response = requests.get(f"{VERCEL_URL}/", timeout=15)
        if response.status_code == 200:
            print("✅ Root endpoint working!")
            data = response.json()
            print(f"   API: {data.get('message', 'N/A')}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Optional transcription test
    print("\n4️⃣ Transcription Test (Optional)")
    test_transcription = input("Test transcription with sample audio? (y/N): ").lower().strip()
    
    if test_transcription in ['y', 'yes']:
        print("🎵 Testing transcription...")
        
        audio_url = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"
        
        try:
            print("📤 Sending transcription request...")
            response = requests.post(
                f"{VERCEL_URL}/transcribe-url",
                data={"audio_url": audio_url},
                timeout=300  # 5 minutes
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Transcription successful!")
                print(f"📝 Transcript preview: {result['transcript'][:100]}...")
                print(f"📊 Word count: {result['metadata']['word_count']}")
                print(f"🎯 Confidence: {result['metadata']['confidence']}")
            else:
                print(f"❌ Transcription failed: {response.status_code}")
                print(f"   Error: {response.text}")
        
        except requests.exceptions.Timeout:
            print("⏰ Transcription timed out (normal for long audio)")
        except Exception as e:
            print(f"❌ Transcription error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Vercel Deployment Test Complete!")
    print(f"🌐 Your API is live at: {VERCEL_URL}")
    print(f"📖 Interactive docs: {VERCEL_URL}/docs")
    print(f"🔗 Share this URL with anyone!")

if __name__ == "__main__":
    print("📝 Instructions:")
    print("1. Replace VERCEL_URL in this script with your actual Vercel URL")
    print("2. Run: python test_vercel_deployment.py")
    print()
    test_vercel_api()
