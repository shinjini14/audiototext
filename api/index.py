"""
Vercel entry point for AudioToText API
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import the FastAPI app from backend
try:
    from app import app
except ImportError as e:
    # Fallback: create a simple error app
    from fastapi import FastAPI
    app = FastAPI()

    @app.get("/")
    async def error():
        return {"error": f"Could not import backend app: {e}"}

# This is the entry point for Vercel
handler = app
