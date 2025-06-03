#!/usr/bin/env python3
"""
Simple startup script for Railway deployment
"""

import os
import sys
import uvicorn

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Change working directory to backend
os.chdir(backend_path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Python path: {sys.path[:3]}")

    # Import the app from the current directory (backend)
    from app import app

    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
