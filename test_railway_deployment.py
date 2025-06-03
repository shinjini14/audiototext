#!/usr/bin/env python3
"""
Quick test for Railway deployment
Replace YOUR_RAILWAY_URL with your actual Railway URL
"""

import requests

# Replace this with your actual Railway URL
RAILWAY_URL = "https://your-app-name.railway.app"

def test_railway_api():
    print(f"🧪 Testing Railway deployment at: {RAILWAY_URL}")
    print("=" * 60)
    
    # Test health check
    try:
        response = requests.get(f"{RAILWAY_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return
    
    # Test API docs
    try:
        response = requests.get(f"{RAILWAY_URL}/docs", timeout=10)
        if response.status_code == 200:
            print("✅ API documentation accessible!")
            print(f"📖 View docs at: {RAILWAY_URL}/docs")
        else:
            print(f"❌ API docs failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API docs error: {e}")
    
    print("\n🎉 Your API is live on Railway!")
    print(f"🌐 Share this URL: {RAILWAY_URL}")
    print(f"📖 Interactive docs: {RAILWAY_URL}/docs")
    print(f"🔗 Health check: {RAILWAY_URL}/health")

if __name__ == "__main__":
    test_railway_api()
