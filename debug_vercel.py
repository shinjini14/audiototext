#!/usr/bin/env python3
"""
Debug script to test what's happening with Vercel deployment
"""

import os
import sys

def debug_environment():
    """Debug the current environment and imports."""
    print("🔍 Vercel Deployment Debug")
    print("=" * 50)
    
    print(f"Python version: {sys.version}")
    print(f"Python path: {sys.path}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Files in current directory: {os.listdir('.')}")
    
    print("\n📦 Environment Variables:")
    for key, value in os.environ.items():
        if 'ASSEMBLYAI' in key or 'VERCEL' in key or 'PYTHON' in key:
            print(f"  {key}: {value}")
    
    print("\n🧪 Testing Imports:")
    
    # Test FastAPI import
    try:
        import fastapi
        print(f"✅ FastAPI: {fastapi.__version__}")
    except ImportError as e:
        print(f"❌ FastAPI: {e}")
    
    # Test AssemblyAI import
    try:
        import assemblyai
        print(f"✅ AssemblyAI: {assemblyai.__version__}")
    except ImportError as e:
        print(f"❌ AssemblyAI: {e}")
    
    # Test other dependencies
    for module in ['uvicorn', 'pydantic', 'python_multipart']:
        try:
            __import__(module)
            print(f"✅ {module}: imported successfully")
        except ImportError as e:
            print(f"❌ {module}: {e}")
    
    print("\n🔑 API Key Check:")
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if api_key:
        print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
    else:
        print("❌ API Key not found")
    
    print("\n📁 File Structure:")
    for root, dirs, files in os.walk('.'):
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")

if __name__ == "__main__":
    debug_environment()
