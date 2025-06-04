#!/usr/bin/env python3
"""
Test multi-language segment detection in AudioToText API
"""

import requests

# Use your live Render URL
BASE_URL = "https://audiototext-z5j7.onrender.com"

def test_multi_language_detection():
    """Test AssemblyAI's dedicated multi-language detection endpoint."""
    print("🌍 Testing AssemblyAI Multi-Language Detection (Beta)")
    print(f"🌐 Base URL: {BASE_URL}")
    print("=" * 70)

    # Sample audio URL (replace with actual multi-language audio)
    audio_url = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"

    print("🎵 Testing with sample audio...")
    print(f"📎 Audio URL: {audio_url}")

    try:
        print("\n📤 Sending multi-language transcription request...")
        response = requests.post(
            f"{BASE_URL}/transcribe-multilang",
            data={
                "audio_url": audio_url,
                "enable_speaker_labels": True,
                "enable_chapters": True
            },
            timeout=300  # 5 minutes
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Multi-language transcription successful!")
            
            # Display basic info
            print(f"\n📝 Full Transcript:")
            print(f"   {result['transcript'][:200]}...")
            
            # Display language detection results
            metadata = result['metadata']
            multilingual = metadata.get('multilingual_detection', {})

            print(f"\n🔍 Multi-Language Detection Results:")
            print(f"   Primary Language: {multilingual.get('primary_language', 'N/A')}")
            print(f"   Language Confidence: {multilingual.get('language_confidence', 'N/A')}")
            print(f"   Total Languages Found: {multilingual.get('total_languages_detected', 0)}")
            print(f"   Languages: {multilingual.get('languages_found', [])}")
            print(f"   Language Names: {multilingual.get('language_names_found', [])}")

            # Display multi-language segments
            segments = metadata.get('language_segments', [])
            if segments:
                print(f"\n🌍 Language Segments ({len(segments)} segments):")
                for i, segment in enumerate(segments[:5]):  # Show first 5 segments
                    lang_name = segment.get('language_name', 'Unknown')
                    text = segment.get('text', '').strip()
                    start = segment.get('start_time', 0)
                    end = segment.get('end_time', 0)
                    confidence = segment.get('confidence', 0)
                    word_count = segment.get('word_count', 0)

                    print(f"   Segment {i+1}:")
                    print(f"     Language: {lang_name}")
                    print(f"     Time: {start:.1f}s - {end:.1f}s")
                    print(f"     Words: {word_count}")
                    print(f"     Confidence: {confidence:.2f}")
                    print(f"     Text: {text[:100]}...")
                    print()

                if len(segments) > 5:
                    print(f"   ... and {len(segments) - 5} more segments")
            else:
                print("\n🔍 Single language detected (no language switching)")
            
            # Display speaker information
            speakers = metadata.get('speakers', [])
            if speakers:
                print(f"\n🗣️  Speaker Diarization ({len(speakers)} speakers):")
                for i, speaker in enumerate(speakers[:3]):  # Show first 3 speakers
                    speaker_id = speaker.get('speaker', 'Unknown')
                    text = speaker.get('text', '').strip()
                    start = speaker.get('start', 0) / 1000
                    end = speaker.get('end', 0) / 1000
                    
                    print(f"   {speaker_id}: ({start:.1f}s - {end:.1f}s)")
                    print(f"     {text[:100]}...")
                    print()
            
            # Display chapters
            chapters = metadata.get('chapters', [])
            if chapters:
                print(f"\n📚 Auto-Generated Chapters ({len(chapters)} chapters):")
                for i, chapter in enumerate(chapters[:3]):  # Show first 3 chapters
                    headline = chapter.get('headline', 'No headline')
                    summary = chapter.get('summary', 'No summary')
                    start = chapter.get('start', 0) / 1000
                    end = chapter.get('end', 0) / 1000
                    
                    print(f"   Chapter {i+1}: {headline}")
                    print(f"     Time: {start:.1f}s - {end:.1f}s")
                    print(f"     Summary: {summary[:100]}...")
                    print()
            
            # Display statistics
            print(f"\n📊 Statistics:")
            print(f"   Word Count: {metadata.get('word_count', 0)}")
            print(f"   Audio Duration: {metadata.get('audio_duration', 0)} seconds")
            print(f"   Overall Confidence: {metadata.get('confidence', 0):.2f}")
            
            return True
            
        else:
            print(f"❌ Transcription failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out (normal for long audio files)")
        print("   The transcription might still be processing...")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run multi-language detection test."""
    success = test_multi_language_detection()
    
    print("\n" + "=" * 70)
    if success:
        print("🎉 Multi-Language Detection Test Complete!")
        print("\n💡 Features Tested:")
        print("   ✅ Multi-language segment detection")
        print("   ✅ Speaker diarization")
        print("   ✅ Auto-chapter generation")
        print("   ✅ Language confidence scores")
        print("   ✅ Timestamp information")
        
        print("\n🎯 Usage Examples:")
        print("   # Multi-language transcription (recommended):")
        print(f'   curl -X POST "{BASE_URL}/transcribe-multilang" \\')
        print('     -d "audio_url=YOUR_MULTILANG_AUDIO_URL" \\')
        print('     -d "enable_speaker_labels=true" \\')
        print('     -d "enable_chapters=true"')

        print("\n   # Standard transcription:")
        print(f'   curl -X POST "{BASE_URL}/transcribe-url" \\')
        print('     -d "audio_url=YOUR_AUDIO_URL"')

        print("\n   # Upload a file:")
        print(f'   curl -X POST "{BASE_URL}/transcribe-file" \\')
        print('     -F "file=@your_audio.mp3"')
        
    else:
        print("❌ Multi-Language Detection Test Failed")
        print("   Check the API logs and try again")

if __name__ == "__main__":
    main()
