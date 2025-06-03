"""
Vercel entry point for AudioToText API
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import the FastAPI app
from app import app

# This is the entry point for Vercel
handler = app
