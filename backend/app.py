# backend/app.py

import os
import tempfile
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import assemblyai as aai

# -----------------------------------
# 1. Load ASSEMBLYAI_API_KEY from environment
# -----------------------------------
# Try to load from .env file (for local development)
load_dotenv()

# Get API key from environment variables (works for both local .env and Railway)
api_key = os.getenv("ASSEMBLYAI_API_KEY")
if not api_key:
    raise RuntimeError(
        "ERROR: Please set ASSEMBLYAI_API_KEY environment variable."
    )

# ------------------------------
# 2. Set AssemblyAI API key
# ------------------------------
aai.settings.api_key = api_key

# ------------------------------
# 3. Create FastAPI app & configure CORS
# ------------------------------
app = FastAPI(
    title="AudioToText API",
    description="AI-powered audio transcription service using AssemblyAI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

origins = [
    "http://localhost:3000",   # frontend
    "http://127.0.0.1:3000",
    "http://localhost:8000",   # for curl/testing
    "http://127.0.0.1:8000",
    "https://*.ngrok.io",      # ngrok tunnels
    "https://*.railway.app",   # railway hosting
    "https://*.render.com",    # render hosting
    "https://*.herokuapp.com", # heroku hosting
    "*",                       # Allow all origins for demo (remove in production)
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# 4. Pydantic model for JSON response
# -----------------------------------
class TranscriptionResponse(BaseModel):
    transcript: str
    metadata: dict


# -----------------------------------
# 5. Helper: Get completed transcription
# -----------------------------------
def _get_completed_transcription(transcript_id: str) -> aai.Transcript:
    """
    Get the completed transcription from AssemblyAI.
    This will wait until the transcription is complete.
    Returns the transcript object. Raises HTTPException on failure.
    """
    try:
        # This will automatically wait for completion
        transcript = aai.Transcript.get_by_id(transcript_id)

        # Check if transcription failed
        if transcript.status == aai.TranscriptStatus.error:
            error_msg = getattr(transcript, 'error', 'Unknown transcription error')
            raise HTTPException(
                status_code=500,
                detail=f"Transcription failed: {error_msg}"
            )

        return transcript
    except HTTPException:
        # Re-raise HTTPException as-is
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AssemblyAI API error: {e}")


# -----------------------------------
# 6. Health check endpoint
# -----------------------------------
@app.get("/health")
async def health_check():
    """Health check endpoint for deployment platforms."""
    return {"status": "healthy", "message": "AudioToText API is running"}

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "AudioToText API",
        "description": "AI-powered audio transcription service",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "transcribe_url": "/transcribe-url",
            "transcribe_file": "/transcribe-file"
        }
    }

# -----------------------------------
# 7. POST /transcribe-url
# -----------------------------------
@app.post("/transcribe-url", response_model=TranscriptionResponse)
async def transcribe_url(audio_url: str = Form(...)):
    """
    Accept a public audio URL, submit to AssemblyAI, poll until done, and return:
      { transcript: "...", metadata: { ... } }
    """
    # 1. Submit transcription job
    try:
        transcriber = aai.Transcriber()
        transcript_request = transcriber.submit(audio_url)
        transcript_id = transcript_request.id
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AssemblyAI API error: {e}")

    # 2. Wait for completion
    transcript = _get_completed_transcription(transcript_id)

    # 3. Build response
    transcript_text = transcript.text or ""
    words = transcript.words or []
    word_count = len(words) if words else None

    metadata = {
        "transcription_id": transcript_id,
        "audio_url": audio_url,
        "status": str(transcript.status),
        "word_count": word_count,
        "confidence": transcript.confidence,
        "language_code": getattr(transcript, 'language_code', None),
        "audio_duration": getattr(transcript, 'audio_duration', None),
    }
    return TranscriptionResponse(transcript=transcript_text, metadata=metadata)


# -----------------------------------
# 7. POST /transcribe-file
# -----------------------------------
@app.post("/transcribe-file", response_model=TranscriptionResponse)
async def transcribe_file(file: UploadFile = File(...)):
    """
    Accept an uploaded audio file, save temporarily, upload to AssemblyAI,
    poll until done, and return { transcript, metadata }.
    """
    # 1. Validate file extension
    filename = file.filename or ""
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    allowed_exts = [".mp3", ".wav", ".m4a", ".mp4", ".webm", ".flac"]
    if ext not in allowed_exts:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}. Allowed: {allowed_exts}",
        )

    # 2. Save to temp file
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save temp file: {e}")

    # 3. Submit transcription job directly with file path
    try:
        transcriber = aai.Transcriber()
        transcript_request = transcriber.submit(tmp_path)
        transcript_id = transcript_request.id
    except Exception as e:
        try:
            os.remove(tmp_path)
        except OSError:
            pass
        raise HTTPException(status_code=500, detail=f"AssemblyAI transcript error: {e}")

    # 5. Delete local temp file
    try:
        os.remove(tmp_path)
    except OSError:
        pass

    # 6. Wait for completion
    transcript = _get_completed_transcription(transcript_id)

    # 7. Build response
    transcript_text = transcript.text or ""
    words = transcript.words or []
    word_count = len(words) if words else None

    metadata = {
        "transcription_id": transcript_id,
        "filename": filename,
        "status": str(transcript.status),
        "word_count": word_count,
        "confidence": transcript.confidence,
        "language_code": getattr(transcript, 'language_code', None),
        "audio_duration": getattr(transcript, 'audio_duration', None),
    }
    return TranscriptionResponse(transcript=transcript_text, metadata=metadata)
