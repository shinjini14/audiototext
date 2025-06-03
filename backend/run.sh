# backend/run.sh
#!/usr/bin/env bash

# Activate the virtualenv
source ./venv/bin/activate

# Make sure we’re in the backend/ directory
cd "$(dirname "$0")"

# Run Uvicorn on port 8000, with auto‐reload
uvicorn app:app --reload --host 0.0.0.0 --port 8000
