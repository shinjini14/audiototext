#!/usr/bin/env python3
"""
Test script for Google Cloud Speech-to-Text endpoint
"""

import requests
import json

def test_google_cloud_endpoint():
    """Test the Google Cloud Speech-to-Text endpoint"""
    
    # API endpoint
    url = "http://localhost:8000/transcribe-google-cloud"
    
    # Test data
    data = {
        "audio_uri": "gs://test-bucket/test-audio.flac",
        "first_language": "en-US",
        "alternate_languages": "hi-IN,ta-IN,te-IN,bn-IN"
    }
    
    print("🧪 Testing Google Cloud Speech-to-Text endpoint...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    print("-" * 50)
    
    try:
        # Make the request
        response = requests.post(url, data=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print("-" * 50)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"Transcript: {result.get('transcript', 'N/A')}")
            print(f"Metadata keys: {list(result.get('metadata', {}).keys())}")
        else:
            print("❌ ERROR!")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR!")
        print("Make sure the FastAPI server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")

def test_root_endpoint():
    """Test the root endpoint to see available endpoints"""
    
    url = "http://localhost:8000/"
    
    print("\n🏠 Testing root endpoint...")
    print(f"URL: {url}")
    print("-" * 50)
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Root endpoint working!")
            print(f"Available endpoints: {result.get('endpoints', {})}")
            print(f"Features: {result.get('features', [])}")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Test root endpoint first
    test_root_endpoint()
    
    # Test Google Cloud endpoint
    test_google_cloud_endpoint()
    
    print("\n" + "="*60)
    print("📝 NEXT STEPS:")
    print("1. Set up Google Cloud Project")
    print("2. Enable Speech-to-Text API")
    print("3. Create Service Account credentials")
    print("4. Set GOOGLE_APPLICATION_CREDENTIALS environment variable")
    print("5. Upload audio files to Google Cloud Storage")
    print("6. Test with real gs:// URIs")
    print("="*60)
