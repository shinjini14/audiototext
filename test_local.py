#!/usr/bin/env python3
"""
Test the app locally before deploying
"""

import os
import sys

def test_local_app():
    print("🧪 Testing local app setup...")
    
    # Set environment variable for testing
    os.environ["ASSEMBLYAI_API_KEY"] = "c050c9bad17d4de885b6e8a23d2445ff"
    
    # Add backend to path
    backend_path = os.path.join(os.getcwd(), 'backend')
    sys.path.insert(0, backend_path)
    
    try:
        print("📦 Testing imports...")
        
        # Test FastAPI import
        from fastapi import FastAPI
        print("✅ FastAPI imported")
        
        # Test uvicorn import
        import uvicorn
        print("✅ uvicorn imported")
        
        # Test AssemblyAI import
        import assemblyai as aai
        print("✅ assemblyai imported")
        
        # Test app import
        from backend.app import app
        print("✅ App imported successfully")
        
        # Test app creation
        print(f"✅ App type: {type(app)}")
        print(f"✅ App title: {app.title}")
        
        print("\n🎉 All imports successful!")
        print("✅ The app should work on Railway")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_local_app()
    if success:
        print("\n🚀 Ready for Railway deployment!")
    else:
        print("\n❌ Fix the errors before deploying to Railway")
