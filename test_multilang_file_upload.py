#!/usr/bin/env python3
"""
Test script for the new AssemblyAI Multi-Language File Upload endpoint
"""

import requests
import json
import os

def test_multilang_file_endpoint():
    """Test the new multi-language file upload endpoint"""
    
    url = "http://localhost:8000/transcribe-multilang-file"
    
    print("🎤 Testing AssemblyAI Enhanced Multi-Language File Upload...")
    print(f"URL: {url}")
    print("-" * 70)
    
    # Check if we have a test audio file
    test_files = [
        "test_audio.mp3",
        "test_audio.wav", 
        "audio.mp3",
        "audio.wav",
        "sample.mp3",
        "sample.wav"
    ]
    
    test_file = None
    for file_name in test_files:
        if os.path.exists(file_name):
            test_file = file_name
            break
    
    if not test_file:
        print("⚠️  No test audio file found!")
        print("💡 To test file upload, place an audio file in the current directory with one of these names:")
        for file_name in test_files:
            print(f"   • {file_name}")
        print("\n🔄 Testing endpoint without file (to check validation)...")
        test_without_file()
        return
    
    print(f"📁 Using test file: {test_file}")
    print(f"📊 File size: {os.path.getsize(test_file) / (1024*1024):.2f} MB")
    
    # Test with all features enabled
    data = {
        "enable_speaker_labels": "true",
        "enable_chapters": "true", 
        "enable_sentiment": "false",  # Disable for faster processing
        "enable_entities": "false"    # Disable for faster processing
    }
    
    try:
        with open(test_file, 'rb') as audio_file:
            files = {'file': (test_file, audio_file, 'audio/mpeg')}
            
            print("🚀 Uploading file and starting transcription...")
            print("⏳ This may take a few minutes for multi-language processing...")
            
            response = requests.post(url, data=data, files=files, timeout=300)
            
            print(f"\n📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ SUCCESS! Multi-Language File Upload Working!")
                
                # Display transcript
                transcript = result.get('transcript', '')
                print(f"\n📝 Transcript ({len(transcript)} characters):")
                print(f"   {transcript[:200]}{'...' if len(transcript) > 200 else ''}")
                
                # Display metadata highlights
                metadata = result.get('metadata', {})
                multilingual = metadata.get('multilingual_detection', {})
                
                print(f"\n🌍 Multi-Language Analysis:")
                print(f"   • Languages detected: {multilingual.get('total_languages_detected', 0)}")
                print(f"   • Languages found: {multilingual.get('languages_found', [])}")
                print(f"   • Language names: {multilingual.get('language_names_found', [])}")
                print(f"   • Language switching: {'Yes' if multilingual.get('language_switching_detected') else 'No'}")
                
                print(f"\n📊 Content Analysis:")
                print(f"   • Total segments: {metadata.get('total_segments', 0)}")
                print(f"   • Total speakers: {metadata.get('total_speakers', 0)}")
                print(f"   • Total chapters: {metadata.get('total_chapters', 0)}")
                print(f"   • Word count: {metadata.get('audio_analysis', {}).get('word_count', 0)}")
                print(f"   • Duration: {metadata.get('audio_analysis', {}).get('duration_seconds', 0):.1f} seconds")
                
                print(f"\n🎯 Features Used:")
                features = metadata.get('features_used', {})
                for feature, enabled in features.items():
                    if isinstance(enabled, bool):
                        status = "✅" if enabled else "❌"
                        print(f"   • {feature.replace('_', ' ').title()}: {status}")
                
                # Show language segments if available
                segments = metadata.get('language_segments', [])
                if segments:
                    print(f"\n🗣️ Language Segments ({len(segments)}):")
                    for i, segment in enumerate(segments[:3]):  # Show first 3
                        lang_name = segment.get('language_name', 'Unknown')
                        text = segment.get('text', '')[:50]
                        duration = segment.get('end_time', 0) - segment.get('start_time', 0)
                        print(f"   {i+1}. {lang_name}: \"{text}...\" ({duration:.1f}s)")
                    if len(segments) > 3:
                        print(f"   ... and {len(segments) - 3} more segments")
                
            else:
                print("❌ ERROR!")
                print(f"Response: {response.text}")
                
    except requests.exceptions.Timeout:
        print("⏰ Request timed out - this is normal for longer audio files")
        print("💡 The transcription is still processing in the background")
    except FileNotFoundError:
        print(f"❌ File not found: {test_file}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_without_file():
    """Test endpoint validation without a file"""
    
    url = "http://localhost:8000/transcribe-multilang-file"
    
    try:
        response = requests.post(url, data={
            "enable_speaker_labels": "true",
            "enable_chapters": "true"
        })
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 422:
            print("✅ Validation working correctly - file is required")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def show_endpoint_info():
    """Show information about available endpoints"""
    
    url = "http://localhost:8000/"
    
    print("\n🏠 Checking Available Endpoints...")
    print("-" * 70)
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            endpoints = result.get('endpoints', {})
            
            print("✅ Available Transcription Endpoints:")
            for name, path in endpoints.items():
                if 'transcribe' in name:
                    if 'multilang-file' in name:
                        status = "🆕 NEW!"
                    elif 'openai' in name:
                        status = "🔴 Quota Issue"
                    else:
                        status = "🟢 Ready"
                    print(f"   • {name}: {path} - {status}")
                    
        else:
            print(f"❌ Error getting endpoints: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def show_usage_examples():
    """Show usage examples"""
    
    print("\n" + "="*70)
    print("💡 USAGE EXAMPLES")
    print("="*70)
    
    print("\n🎯 Basic Multi-Language File Upload:")
    print("curl -X POST 'http://localhost:8000/transcribe-multilang-file' \\")
    print("  -F 'file=@your-audio.mp3' \\")
    print("  -F 'enable_speaker_labels=true' \\")
    print("  -F 'enable_chapters=true'")
    
    print("\n🎯 Full Feature Upload:")
    print("curl -X POST 'http://localhost:8000/transcribe-multilang-file' \\")
    print("  -F 'file=@multilingual-meeting.wav' \\")
    print("  -F 'enable_speaker_labels=true' \\")
    print("  -F 'enable_chapters=true' \\")
    print("  -F 'enable_sentiment=true' \\")
    print("  -F 'enable_entities=true'")
    
    print("\n🌟 Perfect For:")
    print("   • Multi-language meetings (Hindi + English)")
    print("   • Indian language podcasts")
    print("   • Customer service calls")
    print("   • Educational content")
    print("   • Conference recordings")
    
    print("\n📁 Supported Formats:")
    print("   • MP3, WAV, M4A, MP4, WEBM, FLAC")
    print("   • Max size: 100MB")
    print("   • Multi-language detection: Automatic")

if __name__ == "__main__":
    show_endpoint_info()
    test_multilang_file_endpoint()
    show_usage_examples()
