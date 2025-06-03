#!/usr/bin/env python3
"""
Simple startup script for Railway deployment
"""

import os
import sys

def main():
    print("🚀 Starting AudioToText API...")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Files in current directory: {os.listdir('.')}")

    # Check if backend directory exists
    if os.path.exists('backend'):
        print("✅ Backend directory found")
        print(f"Files in backend: {os.listdir('backend')}")
    else:
        print("❌ Backend directory not found!")
        return

    # Check environment variables
    port = os.environ.get("PORT", "8000")
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")

    print(f"🌐 Port: {port}")
    print(f"🔑 API Key: {'✅ Set' if api_key else '❌ Missing'}")

    # Add backend to Python path
    backend_path = os.path.join(os.getcwd(), 'backend')
    sys.path.insert(0, backend_path)

    try:
        print("📦 Testing imports...")
        import uvicorn
        print("✅ uvicorn imported")

        # Import the app
        from backend.app import app
        print("✅ FastAPI app imported")

        print(f"🚀 Starting uvicorn on 0.0.0.0:{port}")
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=int(port),
            log_level="info"
        )

    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()
        return

if __name__ == "__main__":
    main()
