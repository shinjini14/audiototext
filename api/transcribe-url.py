import os
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import JSONResponse
import assemblyai as aai

# Setup
api_key = os.getenv("ASSEMBLYAI_API_KEY")
if not api_key:
    raise RuntimeError("ASSEMBLYAI_API_KEY not set")

aai.settings.api_key = api_key

app = FastAPI()

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

@app.post("/")
def transcribe_url(audio_url: str = Form(...)):
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
    
    return {
        "transcript": transcript.text or "",
        "metadata": metadata
    }

# Vercel handler
def handler(request):
    if request.method == "POST":
        # Extract form data from request
        audio_url = request.form.get("audio_url")
        if not audio_url:
            return JSONResponse({"error": "audio_url is required"}, status_code=400)
        return transcribe_url(audio_url)
    else:
        return JSONResponse({"error": "Method not allowed"}, status_code=405)
