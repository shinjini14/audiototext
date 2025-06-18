#!/usr/bin/env python3
"""
Test script for OpenAI Whisper endpoint
"""

import requests
import json

def test_openai_endpoint_without_file():
    """Test the OpenAI endpoint without a file to see the error handling"""
    
    url = "http://localhost:8000/transcribe-openai"
    
    print("🧪 Testing OpenAI Whisper endpoint (without file)...")
    print(f"URL: {url}")
    print("-" * 50)
    
    try:
        # Test without file
        response = requests.post(url, data={
            "language": "en",
            "model": "gpt-4o-transcribe"
        })
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def test_root_endpoint():
    """Test the root endpoint to see if OpenAI endpoint is listed"""
    
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
            
            # Check if OpenAI endpoint is listed
            endpoints = result.get('endpoints', {})
            if 'transcribe_openai' in endpoints:
                print("✅ OpenAI endpoint is properly registered!")
            else:
                print("❌ OpenAI endpoint not found in endpoints list")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_openai_docs():
    """Test if the OpenAI endpoint appears in the API docs"""
    
    url = "http://localhost:8000/docs"
    
    print(f"\n📚 API Documentation available at: {url}")
    print("You can test the OpenAI endpoint directly from the docs!")

if __name__ == "__main__":
    # Test root endpoint first
    test_root_endpoint()
    
    # Test OpenAI endpoint without file
    test_openai_endpoint_without_file()
    
    # Show docs URL
    test_openai_docs()
    
    print("\n" + "="*60)
    print("📝 NEXT STEPS TO USE OPENAI ENDPOINT:")
    print("1. Get your OpenAI API key from https://platform.openai.com/api-keys")
    print("2. Update .env file: OPENAI_API_KEY=your-actual-api-key")
    print("3. Test with an audio file:")
    print("   curl -X POST 'http://localhost:8000/transcribe-openai' \\")
    print("     -F 'file=@your-audio.mp3' \\")
    print("     -F 'language=hi' \\")
    print("     -F 'model=gpt-4o-transcribe'")
    print("4. Or use the interactive docs at http://localhost:8000/docs")
    print("="*60)
