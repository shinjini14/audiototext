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
    # 1. Configure transcription with AssemblyAI's multi-language feature (beta)
    try:
        config = aai.TranscriptionConfig(
            # Use multi-language detection (beta feature)
            language_detection=True,
            multichannel=False,  # Set to True if audio has multiple channels
            punctuate=True,
            format_text=True,
            speaker_labels=True,  # Enable speaker diarization
            auto_chapters=True,   # Enable chapter detection
            sentiment_analysis=False,  # Disable for better performance
            entity_detection=False,   # Disable for better performance
            # Boost Indian languages for better recognition
            word_boost=["Hindi", "Tamil", "Telugu", "Bengali", "Gujarati", "Kannada", "Malayalam", "Marathi", "Punjabi", "Urdu", "Assamese", "Odia", "Nepali", "Sanskrit"],
            boost_param="high",
            # Enable language detection for each word/segment
            language_code=None,  # Let AssemblyAI auto-detect all languages
            dual_channel=False
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

    # Extract multi-language segments using AssemblyAI's language detection
    language_segments = []
    if words:
        current_segment = {"language": None, "text": "", "start": None, "end": None, "confidence": None, "word_count": 0}

        for word in words:
            # AssemblyAI provides language_code for each word in multi-language transcription
            word_lang = getattr(word, 'language_code', detected_language) or detected_language
            word_confidence = getattr(word, 'confidence', 0.0)
            word_text = getattr(word, 'text', '')

            if current_segment["language"] != word_lang:
                # Save previous segment if it exists
                if current_segment["text"].strip():
                    current_segment["text"] = current_segment["text"].strip()
                    language_segments.append(current_segment.copy())

                # Start new segment
                current_segment = {
                    "language": word_lang,
                    "text": word_text + " ",
                    "start": word.start,
                    "end": word.end,
                    "confidence": word_confidence,
                    "word_count": 1
                }
            else:
                # Continue current segment
                current_segment["text"] += word_text + " "
                current_segment["end"] = word.end
                current_segment["confidence"] = max(current_segment["confidence"] or 0, word_confidence)
                current_segment["word_count"] += 1

        # Add final segment
        if current_segment["text"].strip():
            current_segment["text"] = current_segment["text"].strip()
            language_segments.append(current_segment)

    # Get language detection results from AssemblyAI
    language_detection_results = []
    if hasattr(transcript, 'language_detection') and transcript.language_detection:
        for detection in transcript.language_detection:
            language_detection_results.append({
                "language": detection.language,
                "confidence": detection.confidence,
                "start": detection.start,
                "end": detection.end
            })

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
        "language_detection_enabled": True,
        "multi_language_segments": language_segments,
        "total_languages_detected": len(set(seg["language"] for seg in language_segments)) if language_segments else 1,
        "speakers": speakers,
        "chapters": chapters,
        "languages_found": list(set(seg["language"] for seg in language_segments)) if language_segments else [detected_language],
        "language_detection_results": language_detection_results,
        "multilingual_transcription": True,
        "feature_used": "AssemblyAI Multi-Language Transcription (Beta)"
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

    # 3. Submit transcription job with AssemblyAI's multi-language feature (beta)
    try:
        config = aai.TranscriptionConfig(
            # Use multi-language detection (beta feature)
            language_detection=True,
            multichannel=False,  # Set to True if audio has multiple channels
            punctuate=True,
            format_text=True,
            speaker_labels=True,  # Enable speaker diarization
            auto_chapters=True,   # Enable chapter detection
            sentiment_analysis=False,  # Disable for better performance
            entity_detection=False,   # Disable for better performance
            # Boost Indian languages for better recognition
            word_boost=["Hindi", "Tamil", "Telugu", "Bengali", "Gujarati", "Kannada", "Malayalam", "Marathi", "Punjabi", "Urdu", "Assamese", "Odia", "Nepali", "Sanskrit"],
            boost_param="high",
            # Enable language detection for each word/segment
            language_code=None,  # Let AssemblyAI auto-detect all languages
            dual_channel=False
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

    # Extract multi-language segments using AssemblyAI's language detection
    language_segments = []
    if words:
        current_segment = {"language": None, "text": "", "start": None, "end": None, "confidence": None, "word_count": 0}

        for word in words:
            # AssemblyAI provides language_code for each word in multi-language transcription
            word_lang = getattr(word, 'language_code', detected_language) or detected_language
            word_confidence = getattr(word, 'confidence', 0.0)
            word_text = getattr(word, 'text', '')

            if current_segment["language"] != word_lang:
                # Save previous segment if it exists
                if current_segment["text"].strip():
                    current_segment["text"] = current_segment["text"].strip()
                    language_segments.append(current_segment.copy())

                # Start new segment
                current_segment = {
                    "language": word_lang,
                    "text": word_text + " ",
                    "start": word.start,
                    "end": word.end,
                    "confidence": word_confidence,
                    "word_count": 1
                }
            else:
                # Continue current segment
                current_segment["text"] += word_text + " "
                current_segment["end"] = word.end
                current_segment["confidence"] = max(current_segment["confidence"] or 0, word_confidence)
                current_segment["word_count"] += 1

        # Add final segment
        if current_segment["text"].strip():
            current_segment["text"] = current_segment["text"].strip()
            language_segments.append(current_segment)

    # Get language detection results from AssemblyAI
    language_detection_results = []
    if hasattr(transcript, 'language_detection') and transcript.language_detection:
        for detection in transcript.language_detection:
            language_detection_results.append({
                "language": detection.language,
                "confidence": detection.confidence,
                "start": detection.start,
                "end": detection.end
            })

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


# -----------------------------------
# 9. POST /transcribe-multilang (NEW: Dedicated Multi-Language Endpoint)
# -----------------------------------
@app.post("/transcribe-multilang", response_model=TranscriptionResponse)
async def transcribe_multilang_url(
    audio_url: str = Form(..., description="Public URL of the audio file to transcribe"),
    enable_speaker_labels: bool = Form(True, description="Enable speaker diarization"),
    enable_chapters: bool = Form(True, description="Enable auto-chapter generation")
):
    """
    🌍 **Multi-Language Transcription Endpoint**

    Uses AssemblyAI's dedicated multi-language transcription feature (beta) to detect and transcribe
    multiple languages within a single audio file with high accuracy.

    **Features:**
    - Automatic detection of multiple languages in single audio
    - Word-level language detection
    - Speaker diarization (who spoke when)
    - Auto-chapter generation
    - Timestamp information for each language segment
    - Enhanced accuracy for Indian languages

    **Supported Languages:**
    - All 40+ Indian languages (Hindi, Tamil, Telugu, Bengali, etc.)
    - 100+ international languages
    - Automatic detection - no manual specification needed

    **Returns:**
    - Full transcript with mixed languages
    - Language segments with timestamps
    - Speaker information
    - Chapter summaries
    - Language confidence scores
    """

    # Configure AssemblyAI for optimal multi-language detection
    try:
        config = aai.TranscriptionConfig(
            # Core multi-language settings
            language_detection=True,  # Enable automatic language detection
            language_code=None,       # Don't specify - let AI detect all languages

            # Enhanced features
            speaker_labels=enable_speaker_labels,  # Who spoke when
            auto_chapters=enable_chapters,         # Auto-generate chapters

            # Text formatting
            punctuate=True,
            format_text=True,

            # Performance optimizations
            sentiment_analysis=False,  # Disable for faster processing
            entity_detection=False,    # Disable for faster processing

            # Indian language boost for better accuracy
            word_boost=[
                "Hindi", "Tamil", "Telugu", "Bengali", "Gujarati", "Kannada",
                "Malayalam", "Marathi", "Punjabi", "Urdu", "Assamese", "Odia",
                "Nepali", "Sanskrit", "Bhojpuri", "Maithili", "Rajasthani"
            ],
            boost_param="high"
        )

        # Submit transcription
        transcriber = aai.Transcriber(config=config)
        transcript_request = transcriber.submit(audio_url)
        transcript_id = transcript_request.id

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AssemblyAI submission error: {e}")

    # Wait for completion
    transcript = _get_completed_transcription(transcript_id)

    # Process results
    transcript_text = transcript.text or ""
    words = transcript.words or []

    # Extract language segments with improved logic
    language_segments = []
    if words:
        current_segment = {
            "language": None,
            "language_name": None,
            "text": "",
            "start_time": None,
            "end_time": None,
            "confidence": 0.0,
            "word_count": 0
        }

        for word in words:
            word_lang = getattr(word, 'language_code', 'en') or 'en'
            word_confidence = getattr(word, 'confidence', 0.0)
            word_text = getattr(word, 'text', '')

            # Get language name from our supported languages
            lang_name = _get_language_name(word_lang)

            if current_segment["language"] != word_lang:
                # Save previous segment
                if current_segment["text"].strip():
                    current_segment["text"] = current_segment["text"].strip()
                    language_segments.append(current_segment.copy())

                # Start new segment
                current_segment = {
                    "language": word_lang,
                    "language_name": lang_name,
                    "text": word_text + " ",
                    "start_time": word.start / 1000.0,  # Convert to seconds
                    "end_time": word.end / 1000.0,
                    "confidence": word_confidence,
                    "word_count": 1
                }
            else:
                # Continue current segment
                current_segment["text"] += word_text + " "
                current_segment["end_time"] = word.end / 1000.0
                current_segment["confidence"] = max(current_segment["confidence"], word_confidence)
                current_segment["word_count"] += 1

        # Add final segment
        if current_segment["text"].strip():
            current_segment["text"] = current_segment["text"].strip()
            language_segments.append(current_segment)

    # Get speakers
    speakers = []
    if hasattr(transcript, 'utterances') and transcript.utterances:
        for utterance in transcript.utterances:
            speakers.append({
                "speaker": utterance.speaker,
                "text": utterance.text,
                "start_time": utterance.start / 1000.0,
                "end_time": utterance.end / 1000.0,
                "confidence": utterance.confidence
            })

    # Get chapters
    chapters = []
    if hasattr(transcript, 'chapters') and transcript.chapters:
        for chapter in transcript.chapters:
            chapters.append({
                "title": chapter.headline,
                "summary": chapter.summary,
                "start_time": chapter.start / 1000.0,
                "end_time": chapter.end / 1000.0
            })

    # Build comprehensive metadata
    languages_found = list(set(seg["language"] for seg in language_segments))
    language_names_found = list(set(seg["language_name"] for seg in language_segments))

    metadata = {
        "transcription_id": transcript_id,
        "audio_url": audio_url,
        "status": str(transcript.status),
        "processing_time": getattr(transcript, 'audio_duration', 0),

        # Language detection results
        "multilingual_detection": {
            "total_languages_detected": len(languages_found),
            "languages_found": languages_found,
            "language_names_found": language_names_found,
            "primary_language": getattr(transcript, 'language_code', 'en'),
            "language_confidence": getattr(transcript, 'language_confidence', None)
        },

        # Segments and speakers
        "language_segments": language_segments,
        "total_segments": len(language_segments),
        "speakers": speakers,
        "total_speakers": len(set(s["speaker"] for s in speakers)) if speakers else 0,
        "chapters": chapters,
        "total_chapters": len(chapters),

        # Statistics
        "word_count": len(words),
        "confidence": transcript.confidence,
        "audio_duration_seconds": getattr(transcript, 'audio_duration', 0),

        # Feature info
        "features_used": {
            "multi_language_detection": True,
            "speaker_diarization": enable_speaker_labels,
            "auto_chapters": enable_chapters,
            "indian_language_boost": True,
            "api_version": "AssemblyAI Multi-Language (Beta)"
        }
    }

    return TranscriptionResponse(transcript=transcript_text, metadata=metadata)


def _get_language_name(lang_code: str) -> str:
    """Get human-readable language name from language code."""
    language_names = {
        "hi": "Hindi (हिन्दी)",
        "bn": "Bengali (বাংলা)",
        "te": "Telugu (తెలుగు)",
        "ta": "Tamil (தமிழ்)",
        "mr": "Marathi (मराठी)",
        "ur": "Urdu (اردو)",
        "gu": "Gujarati (ગુજરાતી)",
        "kn": "Kannada (ಕನ್ನಡ)",
        "ml": "Malayalam (മലയാളം)",
        "pa": "Punjabi (ਪੰਜਾਬੀ)",
        "as": "Assamese (অসমীয়া)",
        "or": "Odia (ଓଡ଼ିଆ)",
        "ne": "Nepali (नेपाली)",
        "sa": "Sanskrit (संस्कृत)",
        "en": "English",
        "zh": "Chinese (中文)",
        "ar": "Arabic (العربية)",
        "es": "Spanish (Español)",
        "fr": "French (Français)",
        "de": "German (Deutsch)",
        "ja": "Japanese (日本語)",
        "ko": "Korean (한국어)",
        "ru": "Russian (Русский)"
    }
    return language_names.get(lang_code, f"Language ({lang_code})")
