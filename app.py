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
        "description": "AI-powered audio transcription service with multi-language support",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "transcribe_url": "/transcribe-url",
            "transcribe_file": "/transcribe-file",
            "supported_languages": "/languages"
        },
        "features": [
            "Multi-language detection and transcription",
            "Support for Indian languages (Hindi, Tamil, Telugu, Bengali, etc.)",
            "Automatic language detection",
            "Manual language specification",
            "High-quality transcription with confidence scores"
        ]
    }

@app.get("/languages")
async def get_supported_languages():
    """Get list of ALL supported languages for transcription, including ALL Indian languages."""
    return {
        "supported_languages": {
            # Auto Detection
            "auto": "Automatic Detection",

            # Major Indian Languages (Official Languages of India)
            "hi": "Hindi (हिन्दी)",
            "bn": "Bengali (বাংলা)",
            "te": "Telugu (తెలుగు)",
            "mr": "Marathi (मराठी)",
            "ta": "Tamil (தமிழ்)",
            "ur": "Urdu (اردو)",
            "gu": "Gujarati (ગુજરાતી)",
            "kn": "Kannada (ಕನ್ನಡ)",
            "ml": "Malayalam (മലയാളം)",
            "or": "Odia (ଓଡ଼ିଆ)",
            "pa": "Punjabi (ਪੰਜਾਬੀ)",
            "as": "Assamese (অসমীয়া)",
            "mai": "Maithili (मैथिली)",
            "mag": "Magahi (मगही)",
            "bho": "Bhojpuri (भोजपुरी)",
            "new": "Newari (नेवारी)",
            "gom": "Konkani (कोंकणी)",
            "sd": "Sindhi (سنڌي)",
            "ne": "Nepali (नेपाली)",
            "sa": "Sanskrit (संस्कृत)",

            # Regional Indian Languages
            "ks": "Kashmiri (कॉशुर)",
            "doi": "Dogri (डोगरी)",
            "mni": "Manipuri (মৈতৈলোন্)",
            "sat": "Santali (ᱥᱟᱱᱛᱟᱲᱤ)",
            "bo": "Tibetan (བོད་སྐད་)",
            "dv": "Dhivehi (ދިވެހި)",
            "si": "Sinhala (සිංහල)",

            # Dravidian Languages
            "tcy": "Tulu (ತುಳು)",
            "kod": "Kodava (କୋଡ଼ବା)",

            # Indo-Aryan Languages
            "raj": "Rajasthani (राजस्थानी)",
            "bpy": "Bishnupriya (বিষ্ণুপ্রিয়া)",
            "bh": "Bihari (बिहारी)",
            "awa": "Awadhi (अवधी)",
            "braj": "Braj (ब्रज)",
            "hne": "Chhattisgarhi (छत्तीसगढ़ी)",
            "gju": "Gujari (गुर्जरी)",
            "kha": "Khasi (খাসি)",
            "lus": "Mizo (Mizo ṭawng)",
            "mnc": "Manchu (ᠮᠠᠨᠵᡠ)",

            # Austro-Asiatic Languages
            "ho": "Ho (𑣸𑣉)",
            "kru": "Kurukh (कुड़ुख़)",
            "sck": "Sadri (सादरी)",

            # Tibeto-Burman Languages
            "lep": "Lepcha (ᰛᰩᰵ)",
            "rab": "Rabha (রাভা)",
            "grt": "Garo (আ·চিক)",
            "njo": "Ao (আও)",

            # Other South Asian Languages
            "dz": "Dzongkha (རྫོང་ཁ)",
            "my": "Myanmar (မြန်မာ)",
            "th": "Thai (ไทย)",
            "lo": "Lao (ລາວ)",
            "km": "Khmer (ខ្មែរ)",
            "vi": "Vietnamese (Tiếng Việt)",

            # International Languages
            "en": "English",
            "zh": "Chinese (中文)",
            "ja": "Japanese (日本語)",
            "ko": "Korean (한국어)",
            "ar": "Arabic (العربية)",
            "fa": "Persian (فارسی)",
            "tr": "Turkish (Türkçe)",
            "ru": "Russian (Русский)",
            "de": "German (Deutsch)",
            "fr": "French (Français)",
            "es": "Spanish (Español)",
            "pt": "Portuguese (Português)",
            "it": "Italian (Italiano)",
            "nl": "Dutch (Nederlands)",
            "sv": "Swedish (Svenska)",
            "da": "Danish (Dansk)",
            "no": "Norwegian (Norsk)",
            "fi": "Finnish (Suomi)",
            "pl": "Polish (Polski)",
            "cs": "Czech (Čeština)",
            "sk": "Slovak (Slovenčina)",
            "hu": "Hungarian (Magyar)",
            "ro": "Romanian (Română)",
            "bg": "Bulgarian (Български)",
            "hr": "Croatian (Hrvatski)",
            "sr": "Serbian (Српски)",
            "sl": "Slovenian (Slovenščina)",
            "et": "Estonian (Eesti)",
            "lv": "Latvian (Latviešu)",
            "lt": "Lithuanian (Lietuvių)",
            "mt": "Maltese (Malti)",
            "ga": "Irish (Gaeilge)",
            "cy": "Welsh (Cymraeg)",
            "eu": "Basque (Euskera)",
            "ca": "Catalan (Català)",
            "gl": "Galician (Galego)",
            "is": "Icelandic (Íslenska)",
            "mk": "Macedonian (Македонски)",
            "sq": "Albanian (Shqip)",
            "he": "Hebrew (עברית)",
            "yi": "Yiddish (ייִדיש)",
            "am": "Amharic (አማርኛ)",
            "ti": "Tigrinya (ትግርኛ)",
            "om": "Oromo (Afaan Oromoo)",
            "so": "Somali (Soomaali)",
            "sw": "Swahili (Kiswahili)",
            "zu": "Zulu (isiZulu)",
            "xh": "Xhosa (isiXhosa)",
            "af": "Afrikaans",
            "ms": "Malay (Bahasa Melayu)",
            "id": "Indonesian (Bahasa Indonesia)",
            "tl": "Filipino (Tagalog)",
            "haw": "Hawaiian (ʻŌlelo Hawaiʻi)"
        },
        "indian_languages": {
            "constitutional_languages": {
                "description": "22 Official Languages of India as per 8th Schedule of Constitution",
                "languages": {
                    "hi": "Hindi (हिन्दी)",
                    "bn": "Bengali (বাংলা)",
                    "te": "Telugu (తెలుగు)",
                    "mr": "Marathi (मराठी)",
                    "ta": "Tamil (தமிழ்)",
                    "ur": "Urdu (اردو)",
                    "gu": "Gujarati (ગુજરાતી)",
                    "kn": "Kannada (ಕನ್ನಡ)",
                    "ml": "Malayalam (മലയാളം)",
                    "or": "Odia (ଓଡ଼ିଆ)",
                    "pa": "Punjabi (ਪੰਜਾਬੀ)",
                    "as": "Assamese (অসমীয়া)",
                    "mai": "Maithili (मैथिली)",
                    "sa": "Sanskrit (संस्कृत)",
                    "ne": "Nepali (नेपाली)",
                    "ks": "Kashmiri (कॉशुर)",
                    "sd": "Sindhi (سنڌي)",
                    "gom": "Konkani (कोंकणी)",
                    "doi": "Dogri (डोगरी)",
                    "mni": "Manipuri (মৈতৈলোন্)",
                    "sat": "Santali (ᱥᱟᱱᱛᱟᱲᱤ)",
                    "bo": "Bodo (बड़ो)"
                }
            },
            "regional_languages": {
                "description": "Major Regional Languages of India",
                "languages": {
                    "bho": "Bhojpuri (भोजपुरी)",
                    "mag": "Magahi (मगही)",
                    "new": "Newari (नेवारी)",
                    "raj": "Rajasthani (राजस्थानी)",
                    "tcy": "Tulu (ತುಳು)",
                    "kod": "Kodava (କୋଡ଼ବା)",
                    "bpy": "Bishnupriya (বিষ্ণুপ্রিয়া)",
                    "awa": "Awadhi (अवधी)",
                    "braj": "Braj (ब्रज)",
                    "hne": "Chhattisgarhi (छत्तीसगढ़ी)",
                    "kha": "Khasi (খাসি)",
                    "lus": "Mizo (Mizo ṭawng)",
                    "ho": "Ho (𑣸𑣉)",
                    "kru": "Kurukh (कुड़ुख़)",
                    "lep": "Lepcha (ᰛᰩᰵ)",
                    "grt": "Garo (আ·চিক)"
                }
            }
        },
        "usage": {
            "auto_detection": "Leave language_code empty for automatic detection",
            "manual_specification": "Provide language_code parameter (e.g., 'hi' for Hindi, 'ta' for Tamil)",
            "total_languages": "100+ languages supported",
            "indian_languages_count": "40+ Indian languages supported",
            "examples": {
                "auto_detect": "No language_code parameter",
                "hindi": "language_code=hi",
                "tamil": "language_code=ta",
                "bengali": "language_code=bn",
                "telugu": "language_code=te"
            }
        }
    }

# -----------------------------------
# 7. POST /transcribe-url (Enhanced with language detection)
# -----------------------------------
@app.post("/transcribe-url", response_model=TranscriptionResponse)
async def transcribe_url(
    audio_url: str = Form(...),
    language_code: str = Form(None, description="Optional: Specify language code (e.g., 'hi', 'ta', 'te', 'bn', 'gu', 'kn', 'ml', 'mr', 'pa', 'ur', 'as', 'or', 'mai', 'bho', 'raj', 'new', etc.) or leave empty for auto-detection. See /languages for full list.")
):
    """
    Accept a public audio URL, submit to AssemblyAI with language detection, and return:
      { transcript: "...", metadata: { ... } }

    Supports multiple languages including:
    - English (en) - Default
    - Hindi (hi)
    - Tamil (ta)
    - Telugu (te)
    - Bengali (bn)
    - Gujarati (gu)
    - Kannada (kn)
    - Malayalam (ml)
    - Marathi (mr)
    - Punjabi (pa)
    - Urdu (ur)
    - And many more...
    """
    # 1. Configure transcription with multi-language detection
    try:
        config = aai.TranscriptionConfig(
            language_detection=True if not language_code else False,
            language_code=language_code if language_code else None,
            punctuate=True,
            format_text=True,
            speaker_labels=True,  # Enable speaker diarization
            auto_chapters=True,   # Enable chapter detection
            sentiment_analysis=True,  # Enable sentiment analysis
            entity_detection=True,   # Enable entity detection
            word_boost=["Hindi", "Tamil", "Telugu", "Bengali", "Gujarati", "Kannada", "Malayalam", "Marathi", "Punjabi", "Urdu"],  # Boost Indian language recognition
            boost_param="high"
        )

        transcriber = aai.Transcriber(config=config)
        transcript_request = transcriber.submit(audio_url)
        transcript_id = transcript_request.id
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AssemblyAI API error: {e}")

    # 2. Wait for completion
    transcript = _get_completed_transcription(transcript_id)

    # 3. Build enhanced response with multi-language info
    transcript_text = transcript.text or ""
    words = transcript.words or []
    word_count = len(words) if words else None

    # Get detected language info
    detected_language = getattr(transcript, 'language_code', 'en')
    language_confidence = getattr(transcript, 'language_confidence', None)

    # Extract multi-language segments
    language_segments = []
    if words:
        current_segment = {"language": None, "text": "", "start": None, "end": None, "confidence": None}

        for word in words:
            word_lang = getattr(word, 'language_code', detected_language)
            word_confidence = getattr(word, 'confidence', 0.0)

            if current_segment["language"] != word_lang:
                # Save previous segment if it exists
                if current_segment["text"].strip():
                    language_segments.append(current_segment.copy())

                # Start new segment
                current_segment = {
                    "language": word_lang,
                    "text": word.text + " ",
                    "start": word.start,
                    "end": word.end,
                    "confidence": word_confidence
                }
            else:
                # Continue current segment
                current_segment["text"] += word.text + " "
                current_segment["end"] = word.end
                current_segment["confidence"] = max(current_segment["confidence"] or 0, word_confidence)

        # Add final segment
        if current_segment["text"].strip():
            language_segments.append(current_segment)

    # Get speaker information if available
    speakers = []
    if hasattr(transcript, 'utterances') and transcript.utterances:
        for utterance in transcript.utterances:
            speakers.append({
                "speaker": utterance.speaker,
                "text": utterance.text,
                "start": utterance.start,
                "end": utterance.end,
                "confidence": utterance.confidence
            })

    # Get chapters if available
    chapters = []
    if hasattr(transcript, 'chapters') and transcript.chapters:
        for chapter in transcript.chapters:
            chapters.append({
                "summary": chapter.summary,
                "headline": chapter.headline,
                "start": chapter.start,
                "end": chapter.end
            })

    metadata = {
        "transcription_id": transcript_id,
        "audio_url": audio_url,
        "status": str(transcript.status),
        "word_count": word_count,
        "confidence": transcript.confidence,
        "detected_language": detected_language,
        "language_confidence": language_confidence,
        "requested_language": language_code,
        "audio_duration": getattr(transcript, 'audio_duration', None),
        "language_detection_enabled": True if not language_code else False,
        "multi_language_segments": language_segments,
        "total_languages_detected": len(set(seg["language"] for seg in language_segments)),
        "speakers": speakers,
        "chapters": chapters,
        "languages_found": list(set(seg["language"] for seg in language_segments))
    }
    return TranscriptionResponse(transcript=transcript_text, metadata=metadata)


# -----------------------------------
# 8. POST /transcribe-file (Enhanced with language detection)
# -----------------------------------
@app.post("/transcribe-file", response_model=TranscriptionResponse)
async def transcribe_file(
    file: UploadFile = File(...),
    language_code: str = Form(None, description="Optional: Specify language code (e.g., 'hi', 'ta', 'te', 'bn', 'gu', 'kn', 'ml', 'mr', 'pa', 'ur', 'as', 'or', 'mai', 'bho', 'raj', 'new', etc.) or leave empty for auto-detection. See /languages for full list.")
):
    """
    Accept an uploaded audio file with language detection, save temporarily, upload to AssemblyAI,
    poll until done, and return { transcript, metadata }.

    Supports multiple languages including Indian languages:
    - Hindi (hi), Tamil (ta), Telugu (te), Bengali (bn)
    - Gujarati (gu), Kannada (kn), Malayalam (ml), Marathi (mr)
    - Punjabi (pa), Urdu (ur), and many more...
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

    # 3. Submit transcription job with multi-language detection
    try:
        config = aai.TranscriptionConfig(
            language_detection=True if not language_code else False,
            language_code=language_code if language_code else None,
            punctuate=True,
            format_text=True,
            speaker_labels=True,  # Enable speaker diarization
            auto_chapters=True,   # Enable chapter detection
            sentiment_analysis=True,  # Enable sentiment analysis
            entity_detection=True,   # Enable entity detection
            word_boost=["Hindi", "Tamil", "Telugu", "Bengali", "Gujarati", "Kannada", "Malayalam", "Marathi", "Punjabi", "Urdu"],  # Boost Indian language recognition
            boost_param="high"
        )

        transcriber = aai.Transcriber(config=config)
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

    # 7. Build enhanced response with multi-language info
    transcript_text = transcript.text or ""
    words = transcript.words or []
    word_count = len(words) if words else None

    # Get detected language info
    detected_language = getattr(transcript, 'language_code', 'en')
    language_confidence = getattr(transcript, 'language_confidence', None)

    # Extract multi-language segments
    language_segments = []
    if words:
        current_segment = {"language": None, "text": "", "start": None, "end": None, "confidence": None}

        for word in words:
            word_lang = getattr(word, 'language_code', detected_language)
            word_confidence = getattr(word, 'confidence', 0.0)

            if current_segment["language"] != word_lang:
                # Save previous segment if it exists
                if current_segment["text"].strip():
                    language_segments.append(current_segment.copy())

                # Start new segment
                current_segment = {
                    "language": word_lang,
                    "text": word.text + " ",
                    "start": word.start,
                    "end": word.end,
                    "confidence": word_confidence
                }
            else:
                # Continue current segment
                current_segment["text"] += word.text + " "
                current_segment["end"] = word.end
                current_segment["confidence"] = max(current_segment["confidence"] or 0, word_confidence)

        # Add final segment
        if current_segment["text"].strip():
            language_segments.append(current_segment)

    # Get speaker information if available
    speakers = []
    if hasattr(transcript, 'utterances') and transcript.utterances:
        for utterance in transcript.utterances:
            speakers.append({
                "speaker": utterance.speaker,
                "text": utterance.text,
                "start": utterance.start,
                "end": utterance.end,
                "confidence": utterance.confidence
            })

    # Get chapters if available
    chapters = []
    if hasattr(transcript, 'chapters') and transcript.chapters:
        for chapter in transcript.chapters:
            chapters.append({
                "summary": chapter.summary,
                "headline": chapter.headline,
                "start": chapter.start,
                "end": chapter.end
            })

    metadata = {
        "transcription_id": transcript_id,
        "filename": filename,
        "status": str(transcript.status),
        "word_count": word_count,
        "confidence": transcript.confidence,
        "detected_language": detected_language,
        "language_confidence": language_confidence,
        "requested_language": language_code,
        "audio_duration": getattr(transcript, 'audio_duration', None),
        "language_detection_enabled": True if not language_code else False,
        "multi_language_segments": language_segments,
        "total_languages_detected": len(set(seg["language"] for seg in language_segments)),
        "speakers": speakers,
        "chapters": chapters,
        "languages_found": list(set(seg["language"] for seg in language_segments))
    }
    return TranscriptionResponse(transcript=transcript_text, metadata=metadata)
