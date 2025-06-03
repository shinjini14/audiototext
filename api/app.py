import os
import tempfile
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import assemblyai as aai

# Load API key from environment
api_key = os.getenv("ASSEMBLYAI_API_KEY")
if not api_key:
    raise RuntimeError("ASSEMBLYAI_API_KEY environment variable not set")

aai.settings.api_key = api_key

# Create FastAPI app
app = FastAPI(
    title="AudioToText API",
    description="AI-powered audio transcription service",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranscriptionResponse(BaseModel):
    transcript: str
    metadata: dict

def _get_completed_transcription(transcript_id: str):
    try:
        transcript = aai.Transcript.get_by_id(transcript_id)
        if transcript.status == aai.TranscriptStatus.error:
            error_msg = getattr(transcript, 'error', 'Unknown error')
            raise HTTPException(status_code=500, detail=f"Transcription failed: {error_msg}")
        return transcript
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API error: {e}")

@app.get("/")
async def root():
    return {
        "message": "AudioToText API",
        "description": "AI-powered audio transcription service",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "API is running"}

@app.post("/transcribe-url", response_model=TranscriptionResponse)
async def transcribe_url(audio_url: str = Form(...)):
    try:
        transcriber = aai.Transcriber()
        transcript_request = transcriber.submit(audio_url)
        transcript_id = transcript_request.id
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Submission error: {e}")

    transcript = _get_completed_transcription(transcript_id)
    
    words = transcript.words or []
    metadata = {
        "transcription_id": transcript_id,
        "audio_url": audio_url,
        "status": str(transcript.status),
        "word_count": len(words),
        "confidence": transcript.confidence,
        "language_code": getattr(transcript, 'language_code', None),
        "audio_duration": getattr(transcript, 'audio_duration', None),
    }
    
    return TranscriptionResponse(transcript=transcript.text or "", metadata=metadata)

@app.post("/transcribe-file", response_model=TranscriptionResponse)
async def transcribe_file(file: UploadFile = File(...)):
    filename = file.filename or ""
    _, ext = os.path.splitext(filename)
    allowed_exts = [".mp3", ".wav", ".m4a", ".mp4", ".webm", ".flac"]
    
    if ext.lower() not in allowed_exts:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File save error: {e}")

    try:
        transcriber = aai.Transcriber()
        transcript_request = transcriber.submit(tmp_path)
        transcript_id = transcript_request.id
    except Exception as e:
        try:
            os.remove(tmp_path)
        except:
            pass
        raise HTTPException(status_code=500, detail=f"Submission error: {e}")

    try:
        os.remove(tmp_path)
    except:
        pass

    transcript = _get_completed_transcription(transcript_id)
    
    words = transcript.words or []
    metadata = {
        "transcription_id": transcript_id,
        "filename": filename,
        "status": str(transcript.status),
        "word_count": len(words),
        "confidence": transcript.confidence,
        "language_code": getattr(transcript, 'language_code', None),
        "audio_duration": getattr(transcript, 'audio_duration', None),
    }
    
    return TranscriptionResponse(transcript=transcript.text or "", metadata=metadata)
