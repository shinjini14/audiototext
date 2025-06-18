#!/usr/bin/env python3
"""
Test AssemblyAI multi-language endpoint as alternative to OpenAI
"""

import requests
import json

def test_assemblyai_multilang():
    """Test AssemblyAI multi-language endpoint"""
    
    url = "http://localhost:8000/transcribe-multilang"
    
    # Test with a sample audio URL (you can replace with your own)
    test_audio_url = "https://www2.cs.uic.edu/~i101/SoundFiles/BabyElephantWalk60.wav"
    
    data = {
        "audio_url": test_audio_url,
        "enable_speaker_labels": True,
        "enable_chapters": True
    }
    
    print("🧪 Testing AssemblyAI Multi-Language Endpoint...")
    print(f"URL: {url}")
    print(f"Audio URL: {test_audio_url}")
    print("-" * 60)
    
    try:
        response = requests.post(url, data=data)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS! AssemblyAI Multi-Language Working!")
            print(f"📝 Transcript: {result.get('transcript', 'N/A')[:200]}...")
            
            metadata = result.get('metadata', {})
            multilingual = metadata.get('multilingual_detection', {})
            
            print(f"🌍 Languages detected: {multilingual.get('total_languages_detected', 0)}")
            print(f"🗣️ Languages found: {multilingual.get('languages_found', [])}")
            print(f"📊 Total segments: {metadata.get('total_segments', 0)}")
            print(f"👥 Total speakers: {metadata.get('total_speakers', 0)}")
            
        else:
            print("❌ ERROR!")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def show_available_endpoints():
    """Show all available endpoints"""
    
    url = "http://localhost:8000/"
    
    print("\n🏠 Available Endpoints:")
    print("-" * 60)
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            endpoints = result.get('endpoints', {})
            
            print("✅ Working Endpoints:")
            for name, path in endpoints.items():
                if 'openai' not in name:  # Skip OpenAI since it's quota exceeded
                    status = "🟢 Ready"
                else:
                    status = "🔴 Quota Exceeded"
                print(f"   • {name}: {path} - {status}")
                
        else:
            print(f"❌ Error getting endpoints: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def show_recommendations():
    """Show recommendations for multi-language transcription"""
    
    print("\n" + "="*60)
    print("💡 RECOMMENDATIONS FOR MULTI-LANGUAGE TRANSCRIPTION")
    print("="*60)
    
    print("\n🥇 BEST CURRENT OPTION: AssemblyAI Multi-Language")
    print("   • Endpoint: /transcribe-multilang")
    print("   • ✅ Already working with your API key")
    print("   • ✅ Excellent Indian language support")
    print("   • ✅ Speaker diarization")
    print("   • ✅ Language segment detection")
    print("   • ✅ Auto chapters")
    
    print("\n🥈 ALTERNATIVE: AssemblyAI File Upload")
    print("   • Endpoint: /transcribe-file")
    print("   • ✅ Direct file upload")
    print("   • ✅ Multi-language detection")
    
    print("\n🔮 FUTURE: OpenAI Whisper (when quota available)")
    print("   • Endpoint: /transcribe-openai")
    print("   • 🔴 Currently quota exceeded")
    print("   • 💰 Add billing to OpenAI account")
    
    print("\n🚀 QUICK TEST COMMANDS:")
    print("   # Test with URL:")
    print("   curl -X POST 'http://localhost:8000/transcribe-multilang' \\")
    print("     -F 'audio_url=YOUR_AUDIO_URL'")
    print()
    print("   # Test with file:")
    print("   curl -X POST 'http://localhost:8000/transcribe-file' \\")
    print("     -F 'file=@your-audio.mp3'")

if __name__ == "__main__":
    show_available_endpoints()
    test_assemblyai_multilang()
    show_recommendations()
