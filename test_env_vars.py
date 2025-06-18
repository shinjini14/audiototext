#!/usr/bin/env python3
"""
Test script to check environment variables
"""

import os
from dotenv import load_dotenv

def test_env_vars():
    """Test if environment variables are loaded correctly"""
    
    print("🔍 Testing Environment Variables...")
    print("-" * 50)
    
    # Load .env file
    load_dotenv()
    
    # Check AssemblyAI key
    assemblyai_key = os.getenv("ASSEMBLYAI_API_KEY")
    print(f"ASSEMBLYAI_API_KEY: {'✅ Set' if assemblyai_key else '❌ Not set'}")
    if assemblyai_key:
        print(f"  Length: {len(assemblyai_key)} characters")
        print(f"  Starts with: {assemblyai_key[:10]}...")
    
    # Check OpenAI key
    openai_key = os.getenv("OPENAI_API_KEY")
    print(f"OPENAI_API_KEY: {'✅ Set' if openai_key else '❌ Not set'}")
    if openai_key:
        print(f"  Length: {len(openai_key)} characters")
        print(f"  Starts with: {openai_key[:10]}...")
        
        # Validate OpenAI key format
        if openai_key.startswith('sk-'):
            print("  Format: ✅ Valid OpenAI key format")
        else:
            print("  Format: ❌ Invalid OpenAI key format (should start with 'sk-')")
    
    print("-" * 50)
    
    # Test OpenAI client initialization
    try:
        from openai import OpenAI
        
        if openai_key:
            print("🧪 Testing OpenAI Client Initialization...")
            client = OpenAI(api_key=openai_key)
            print("✅ OpenAI client created successfully")
            
            # Test a simple API call (this will fail if key is invalid)
            print("🔑 Testing API key validity...")
            try:
                # This is a minimal API call to test the key
                models = client.models.list()
                print("✅ OpenAI API key is valid!")
                print(f"Available models: {len(models.data)} found")
            except Exception as e:
                print(f"❌ OpenAI API key validation failed: {e}")
        else:
            print("❌ Cannot test OpenAI client - no API key found")
            
    except ImportError:
        print("❌ OpenAI library not installed")
    except Exception as e:
        print(f"❌ Error testing OpenAI client: {e}")

if __name__ == "__main__":
    test_env_vars()
