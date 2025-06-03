#!/usr/bin/env python3
"""
Test the current Vercel deployment at audiototext-two.vercel.app
"""

import requests

BASE_URL = "https://audiototext-two.vercel.app"

def test_endpoints():
    print("🧪 Testing AudioToText API Deployment")
    print(f"🌐 Base URL: {BASE_URL}")
    print("=" * 60)
    
    endpoints_to_test = [
        ("Root", "/"),
        ("Health", "/api/health"),
        ("API App", "/api/app"),
        ("API Docs", "/api/app/docs"),
        ("Transcribe URL", "/api/transcribe-url"),
    ]
    
    for name, endpoint in endpoints_to_test:
        url = f"{BASE_URL}{endpoint}"
        print(f"\n🔍 Testing {name}: {endpoint}")
        
        try:
            if endpoint == "/api/transcribe-url":
                # POST request for transcription
                response = requests.post(
                    url,
                    data={"audio_url": "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"},
                    timeout=30
                )
            else:
                # GET request for others
                response = requests.get(url, timeout=10)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ SUCCESS")
                if endpoint == "/":
                    print("   📄 Root page loaded")
                elif endpoint == "/api/health":
                    try:
                        data = response.json()
                        print(f"   💚 Health: {data.get('status', 'unknown')}")
                    except:
                        print("   📄 Health page loaded (HTML)")
                elif endpoint == "/api/transcribe-url":
                    try:
                        data = response.json()
                        print(f"   🎵 Transcript preview: {data.get('transcript', 'N/A')[:50]}...")
                    except:
                        print("   📄 Transcription response received")
            elif response.status_code == 404:
                print("   ❌ NOT FOUND")
            elif response.status_code == 405:
                print("   ⚠️  METHOD NOT ALLOWED (expected for some endpoints)")
            else:
                print(f"   ⚠️  Status {response.status_code}: {response.text[:100]}")
                
        except requests.exceptions.Timeout:
            print("   ⏰ TIMEOUT (normal for transcription)")
        except requests.exceptions.ConnectionError:
            print("   🔌 CONNECTION ERROR")
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Working Endpoints Summary:")
    print(f"🌐 Main page: {BASE_URL}/")
    print(f"❤️  Health check: {BASE_URL}/api/health")
    print(f"📖 API docs: {BASE_URL}/api/app/docs")
    print(f"🎵 Transcribe: {BASE_URL}/api/transcribe-url")
    
    print("\n💡 If any endpoint shows 404, try:")
    print("1. Wait a few minutes for deployment to complete")
    print("2. Check Vercel deployment logs")
    print("3. Verify environment variables are set")

if __name__ == "__main__":
    test_endpoints()
