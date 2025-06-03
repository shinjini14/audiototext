@echo off
REM backend/run.bat
REM Windows batch script to run the FastAPI application

echo Starting FastAPI Audio-to-Text Backend...

REM Change to the backend directory
cd /d "%~dp0"

REM Run Uvicorn on port 8000 with auto-reload
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000

pause
