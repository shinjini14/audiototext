#!/usr/bin/env python3
"""
Simple startup script for Railway deployment
"""

import os
import subprocess

if __name__ == "__main__":
    port = os.environ.get("PORT", "8000")
    print(f"Starting server on port {port}")
    print(f"Current directory: {os.getcwd()}")

    # Use subprocess to run uvicorn with proper port handling
    cmd = [
        "python", "-m", "uvicorn",
        "backend.app:app",
        "--host", "0.0.0.0",
        "--port", str(port)
    ]

    print(f"Running command: {' '.join(cmd)}")
    subprocess.run(cmd)
