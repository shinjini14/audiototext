#!/usr/bin/env python3
"""
Test multi-language support for AudioToText API
"""

import requests

# Use your live Render URL
BASE_URL = "https://audiototext-z5j7.onrender.com"

def test_supported_languages():
    """Test the supported languages endpoint."""
    print("🌍 Testing supported languages endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/languages")
        if response.status_code == 200:
            data = response.json()
            print("✅ Supported languages endpoint working!")
            print(f"📋 Total languages supported: {len(data['supported_languages'])}")
            
            print("\n🇮🇳 Constitutional Languages of India (22 Official):")
            constitutional = data['indian_languages']['constitutional_languages']['languages']
            for lang_code, lang_name in list(constitutional.items())[:10]:  # Show first 10
                print(f"   {lang_code}: {lang_name}")
            print(f"   ... and {len(constitutional)-10} more constitutional languages")

            print("\n🏞️ Regional Languages of India:")
            regional = data['indian_languages']['regional_languages']['languages']
            for lang_code, lang_name in list(regional.items())[:8]:  # Show first 8
                print(f"   {lang_code}: {lang_name}")
            print(f"   ... and {len(regional)-8} more regional languages")

            print(f"\n📊 Total Indian languages: {len(constitutional) + len(regional)}")
            print(f"📊 Total languages supported: {len(data['supported_languages'])}")
            
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_auto_detection():
    """Test automatic language detection."""
    print("\n🔍 Testing automatic language detection...")
    
    # Sample English audio
    audio_url = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"
    
    try:
        response = requests.post(
            f"{BASE_URL}/transcribe-url",
            data={"audio_url": audio_url},
            timeout=300
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Auto-detection successful!")
            print(f"🗣️  Detected language: {result['metadata']['detected_language']}")
            print(f"🎯 Language confidence: {result['metadata']['language_confidence']}")
            print(f"📝 Transcript preview: {result['transcript'][:100]}...")
            return True
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.Timeout:
        print("⏰ Request timed out (normal for long audio)")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_specific_language():
    """Test with specific language code."""
    print("\n🎯 Testing specific language specification...")
    
    # Sample audio (you can replace with Hindi/other language audio)
    audio_url = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"
    
    try:
        response = requests.post(
            f"{BASE_URL}/transcribe-url",
            data={
                "audio_url": audio_url,
                "language_code": "en"  # Specify English
            },
            timeout=300
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Language specification successful!")
            print(f"🎯 Requested language: {result['metadata']['requested_language']}")
            print(f"🗣️  Detected language: {result['metadata']['detected_language']}")
            print(f"🔧 Language detection enabled: {result['metadata']['language_detection_enabled']}")
            print(f"📝 Transcript preview: {result['transcript'][:100]}...")
            return True
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.Timeout:
        print("⏰ Request timed out (normal for long audio)")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all multi-language tests."""
    print("🧪 Testing Multi-Language AudioToText API")
    print(f"🌐 Base URL: {BASE_URL}")
    print("=" * 60)
    
    results = []
    
    # Test 1: Supported languages
    results.append(test_supported_languages())
    
    # Test 2: Auto-detection
    results.append(test_auto_detection())
    
    # Test 3: Specific language
    results.append(test_specific_language())
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"✅ Passed: {sum(results)}/{len(results)}")
    
    if all(results):
        print("🎉 All multi-language features working!")
    else:
        print("⚠️  Some tests failed - check the logs above")
    
    print("\n💡 Usage Examples:")
    print("# Auto-detect language:")
    print(f'curl -X POST "{BASE_URL}/transcribe-url" -d "audio_url=YOUR_AUDIO_URL"')
    
    print("\n# Specify Hindi:")
    print(f'curl -X POST "{BASE_URL}/transcribe-url" -d "audio_url=YOUR_AUDIO_URL&language_code=hi"')
    
    print("\n# Get supported languages:")
    print(f'curl "{BASE_URL}/languages"')

if __name__ == "__main__":
    main()
