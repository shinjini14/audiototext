#!/usr/bin/env python3
"""
Test OpenAI API quota and limits
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

def test_openai_quota():
    """Test OpenAI API quota and available models"""
    
    load_dotenv()
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_key:
        print("❌ No OpenAI API key found")
        return
    
    print("🔍 Testing OpenAI API Status...")
    print("-" * 50)
    
    try:
        client = OpenAI(api_key=openai_key)
        
        # Test 1: List available models
        print("📋 Checking available models...")
        models = client.models.list()
        
        whisper_models = [m for m in models.data if 'whisper' in m.id.lower()]
        gpt_models = [m for m in models.data if 'gpt-4o' in m.id.lower()]
        
        print(f"✅ Total models available: {len(models.data)}")
        print(f"🎤 Whisper models: {[m.id for m in whisper_models]}")
        print(f"🧠 GPT-4o models: {[m.id for m in gpt_models]}")
        
        # Test 2: Check if whisper-1 is available
        whisper_1_available = any(m.id == 'whisper-1' for m in models.data)
        print(f"🎯 whisper-1 available: {'✅ Yes' if whisper_1_available else '❌ No'}")
        
        # Test 3: Try a simple API call to check quota
        print("\n💰 Testing API quota...")
        
        # Create a very small test audio file (silence)
        import tempfile
        import wave
        import struct
        
        # Create 1 second of silence
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            with wave.open(temp_file.name, 'w') as wav_file:
                wav_file.setnchannels(1)  # mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(16000)  # 16kHz
                
                # 1 second of silence
                silence = struct.pack('<h', 0) * 16000
                wav_file.writeframes(silence)
            
            # Test transcription
            try:
                with open(temp_file.name, 'rb') as audio_file:
                    transcription = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        response_format="text"
                    )
                print("✅ API quota test successful!")
                print(f"📝 Test transcription result: '{transcription}'")
                
            except Exception as e:
                error_msg = str(e).lower()
                if 'quota' in error_msg or 'limit' in error_msg:
                    print("❌ QUOTA EXCEEDED!")
                    print(f"Error: {e}")
                    print("\n💡 Solutions:")
                    print("1. Check your OpenAI billing: https://platform.openai.com/account/billing")
                    print("2. Add payment method if you haven't")
                    print("3. Wait for quota reset (monthly)")
                    print("4. Upgrade your plan if needed")
                elif 'rate' in error_msg:
                    print("⏰ RATE LIMIT HIT!")
                    print(f"Error: {e}")
                    print("💡 Solution: Wait a few minutes and try again")
                else:
                    print(f"❌ Other API error: {e}")
            
            # Clean up
            os.unlink(temp_file.name)
        
    except Exception as e:
        print(f"❌ Failed to connect to OpenAI API: {e}")
        
        error_msg = str(e).lower()
        if 'api_key' in error_msg or 'authentication' in error_msg:
            print("💡 Solution: Check your API key")
        elif 'quota' in error_msg or 'billing' in error_msg:
            print("💡 Solution: Check your OpenAI billing and quota")

def check_account_info():
    """Display account information"""
    print("\n" + "="*60)
    print("📊 ACCOUNT INFORMATION")
    print("="*60)
    print("🔗 Check your OpenAI account:")
    print("   • Usage: https://platform.openai.com/usage")
    print("   • Billing: https://platform.openai.com/account/billing")
    print("   • API Keys: https://platform.openai.com/api-keys")
    print("\n💡 Common Issues:")
    print("   • Free tier has limited quota")
    print("   • Need to add payment method for higher limits")
    print("   • Monthly usage resets on billing date")
    print("   • Rate limits: 3 requests/minute for free tier")

if __name__ == "__main__":
    test_openai_quota()
    check_account_info()
