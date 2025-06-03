#!/usr/bin/env python3
"""
Quick test to check the transcribe-url endpoint
"""

import requests
import json

def test_transcribe_url():
    """Test the transcribe-url endpoint with a sample audio URL."""
    print("🧪 Testing /transcribe-url endpoint...")
    
    # Sample audio URL (AssemblyAI's working demo file)
    test_url = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"
    
    try:
        print(f"📤 Sending request to transcribe: {test_url}")
        response = requests.post(
            "http://localhost:8000/transcribe-url",
            data={"audio_url": test_url},
            timeout=180  # 3 minutes timeout for transcription
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Transcription successful!")
            print(f"📝 Transcript: {result['transcript'][:200]}...")
            print(f"📊 Status: {result['metadata']['status']}")
            print(f"🔢 Word count: {result['metadata']['word_count']}")
            print(f"🎯 Confidence: {result['metadata']['confidence']}")
            print(f"🌐 Language: {result['metadata']['language_code']}")
            print(f"⏱️ Duration: {result['metadata']['audio_duration']}")
            print(f"🔍 Full metadata: {json.dumps(result['metadata'], indent=2)}")
            return True
        else:
            print(f"❌ Transcription failed with status code: {response.status_code}")
            print(f"Error response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Transcription might take longer than expected.")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on port 8000.")
        return False
    except Exception as e:
        print(f"❌ Error during transcription: {e}")
        return False

if __name__ == "__main__":
    test_transcribe_url()
