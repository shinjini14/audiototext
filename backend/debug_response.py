#!/usr/bin/env python3
"""
Debug script to check the actual response structure from AssemblyAI
"""

import assemblyai as aai
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("ASSEMBLYAI_API_KEY")
aai.settings.api_key = api_key

def debug_transcript_structure():
    """Debug the actual structure of a transcript response."""
    print("🔍 Debugging AssemblyAI transcript structure...")
    
    # Sample audio URL
    test_url = "https://storage.googleapis.com/aai-docs-samples/nbc.wav"
    
    try:
        # Submit transcription
        transcriber = aai.Transcriber()
        transcript_request = transcriber.submit(test_url)
        transcript_id = transcript_request.id
        
        print(f"📤 Submitted transcript with ID: {transcript_id}")
        
        # Get completed transcript
        transcript = aai.Transcript.get_by_id(transcript_id)
        
        print("✅ Transcript completed!")
        print(f"📝 Text: {transcript.text[:100]}...")
        
        # Debug the structure
        print("\n🔍 Transcript object attributes:")
        for attr in dir(transcript):
            if not attr.startswith('_'):
                try:
                    value = getattr(transcript, attr)
                    if not callable(value):
                        print(f"  {attr}: {type(value)} = {value}")
                except:
                    print(f"  {attr}: <could not access>")
        
        print("\n🔍 Transcript.__dict__:")
        print(json.dumps(transcript.__dict__, indent=2, default=str))
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_transcript_structure()
