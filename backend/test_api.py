#!/usr/bin/env python3
"""
Simple test script to verify the FastAPI backend is working.
"""

import requests
import json

def test_server_health():
    """Test if the server is running and responding."""
    try:
        response = requests.get("http://localhost:8000/docs")
        if response.status_code == 200:
            print("✅ Server is running and responding!")
            print("📖 API documentation available at: http://localhost:8000/docs")
            return True
        else:
            print(f"❌ Server responded with status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on port 8000.")
        return False
    except Exception as e:
        print(f"❌ Error testing server: {e}")
        return False

def test_transcribe_url():
    """Test the transcribe-url endpoint with a sample audio URL."""
    print("\n🧪 Testing /transcribe-url endpoint...")
    
    # Sample audio URL (AssemblyAI's demo file)
    test_url = "https://storage.googleapis.com/aai-docs-samples/nbc.wav"
    
    try:
        response = requests.post(
            "http://localhost:8000/transcribe-url",
            data={"audio_url": test_url},
            timeout=120  # 2 minutes timeout for transcription
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Transcription successful!")
            print(f"📝 Transcript: {result['transcript'][:100]}...")
            print(f"📊 Metadata: {json.dumps(result['metadata'], indent=2)}")
            return True
        else:
            print(f"❌ Transcription failed with status code: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Transcription might take longer than expected.")
        return False
    except Exception as e:
        print(f"❌ Error during transcription: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Audio-to-Text Backend API")
    print("=" * 50)
    
    # Test 1: Server health
    if not test_server_health():
        print("\n❌ Server health check failed. Please start the server first.")
        exit(1)
    
    # Test 2: Transcription endpoint (optional, requires API key)
    print("\n⚠️  Note: The transcription test requires a valid AssemblyAI API key.")
    user_input = input("Do you want to test the transcription endpoint? (y/N): ")
    
    if user_input.lower() in ['y', 'yes']:
        test_transcribe_url()
    else:
        print("⏭️  Skipping transcription test.")
    
    print("\n✅ Testing complete!")
    print("🌐 You can also test the API manually at: http://localhost:8000/docs")
