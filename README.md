# AudioToText API

🎵 AI-powered audio transcription service using AssemblyAI. Convert audio files or URLs to text with high accuracy.

## 🚀 Live Demo

**API is live at**: https://audiototext-z5j7.onrender.com

- 🌐 **API Root**: https://audiototext-z5j7.onrender.com/
- 📖 **Interactive Docs**: https://audiototext-z5j7.onrender.com/docs
- ❤️ **Health Check**: https://audiototext-z5j7.onrender.com/health

## ✨ Features

- 🌍 **Multi-Language Support** - Automatic language detection and transcription
- 🇮🇳 **Indian Languages** - Hindi, Tamil, Telugu, Bengali, Gujarati, Kannada, Malayalam, Marathi, Punjabi, Urdu, and more
- 🎵 **Audio URL Transcription** - Submit public audio URLs for transcription
- 📁 **File Upload** - Upload audio files directly (MP3, WAV, M4A, MP4, WebM, FLAC)
- 🔍 **Language Detection** - Automatic detection or manual specification
- 🚀 **Fast Processing** - Powered by AssemblyAI's advanced speech recognition
- 📊 **Detailed Metadata** - Get word count, confidence scores, language info, and more
- 🌐 **REST API** - Easy integration with any application
- 📖 **Interactive Docs** - Built-in Swagger UI documentation

## 🎯 Quick Test

Try the live API right now:

```bash
# Test health check
curl https://audiototext-z5j7.onrender.com/health

# Get supported languages
curl https://audiototext-z5j7.onrender.com/languages

# Auto-detect language and transcribe
curl -X POST "https://audiototext-z5j7.onrender.com/transcribe-url" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "audio_url=https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"

# Transcribe Hindi audio (specify language)
curl -X POST "https://audiototext-z5j7.onrender.com/transcribe-url" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "audio_url=YOUR_HINDI_AUDIO_URL&language_code=hi"
```

## 📡 API Endpoints

### Health Check
```bash
GET /health
```

### Get Supported Languages
```bash
GET /languages
```

### Transcribe Audio URL (Multi-Language)
```bash
POST /transcribe-url
Content-Type: application/x-www-form-urlencoded

# Auto-detect language
audio_url=https://example.com/audio.mp3

# Or specify language
audio_url=https://example.com/audio.mp3&language_code=hi
```

### Upload Audio File (Multi-Language)
```bash
POST /transcribe-file
Content-Type: multipart/form-data

file: <audio_file>
language_code: hi  # Optional: specify language or leave empty for auto-detection
```

### Supported Language Codes
- **Auto-detection**: Leave `language_code` empty
- **Hindi**: `hi` - हिन्दी
- **Tamil**: `ta` - தமிழ்
- **Telugu**: `te` - తెలుగు
- **Bengali**: `bn` - বাংলা
- **Gujarati**: `gu` - ગુજરાતી
- **Kannada**: `kn` - ಕನ್ನಡ
- **Malayalam**: `ml` - മലയാളം
- **Marathi**: `mr` - मराठी
- **Punjabi**: `pa` - ਪੰਜਾਬੀ
- **Urdu**: `ur` - اردو
- **English**: `en` - English
- And many more... (see `/languages` endpoint)

## 💻 Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/shinjini14/audiototext.git
   cd audiototext
   ```

2. **Set up environment**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key**
   Set environment variable:
   ```bash
   export ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here
   ```

4. **Run the API**
   ```bash
   uvicorn app:app --reload
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs

## 🔧 Example Usage

### Using curl
```bash
# Transcribe from URL
curl -X POST "https://audiototext-z5j7.onrender.com/transcribe-url" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "audio_url=https://example.com/audio.mp3"

# Upload file
curl -X POST "https://audiototext-z5j7.onrender.com/transcribe-file" \
  -F "file=@audio.mp3"
```

### Using Python
```python
import requests

# Transcribe URL
response = requests.post(
    "https://audiototext-z5j7.onrender.com/transcribe-url",
    data={"audio_url": "https://example.com/audio.mp3"}
)

result = response.json()
print(f"Transcript: {result['transcript']}")
print(f"Word count: {result['metadata']['word_count']}")
```

### Using JavaScript
```javascript
// Transcribe URL
const response = await fetch('https://audiototext-z5j7.onrender.com/transcribe-url', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: 'audio_url=https://example.com/audio.mp3'
});

const result = await response.json();
console.log('Transcript:', result.transcript);
```

## 📋 Response Format

```json
{
  "transcript": "The transcribed text will appear here...",
  "metadata": {
    "transcription_id": "abc123",
    "audio_url": "https://example.com/audio.mp3",
    "status": "completed",
    "word_count": 42,
    "confidence": 0.95,
    "language_code": "en",
    "audio_duration": 30.5
  }
}
```

## 🚀 Deployment

This API is deployed on **Render** using the `render.yaml` configuration.

### Deploy Your Own

1. **Fork this repository**
2. **Sign up at**: https://render.com
3. **Connect your GitHub repository**
4. **Set environment variable**: `ASSEMBLYAI_API_KEY`
5. **Deploy automatically**

### Docker Support

Build and run with Docker:
```bash
docker build -t audiototext .
docker run -p 8000:8000 -e ASSEMBLYAI_API_KEY=your_key audiototext
```

## 🎵 Supported Audio Formats

- MP3
- WAV
- M4A
- MP4
- WebM
- FLAC

## 🛠️ Tech Stack

- **Backend**: FastAPI + Python
- **AI**: AssemblyAI Speech Recognition
- **Hosting**: Render
- **Documentation**: Swagger UI (built-in)

## 📄 License

MIT License

---

**🌟 Star this repo if you find it useful!**
