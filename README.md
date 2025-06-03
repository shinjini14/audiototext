# 🎵 AudioToText API

A powerful FastAPI-based backend service for transcribing audio files using AssemblyAI.
**Now with deployment support for sharing with others!**

## 🚀 Quick Deploy & Share

**Want to share your API with others? Deploy it in minutes:**

1. **Instant Public URL (Ngrok)**:
   ```bash
   # Start your API
   cd backend && python -m uvicorn app:app --host 0.0.0.0 --port 8000

   # In another terminal, create public tunnel
   ngrok http 8000
   ```
   Get instant URL like `https://abc123.ngrok.io` - share this with anyone!

2. **Permanent Free Hosting**: See [DEPLOYMENT.md](DEPLOYMENT.md) for Railway, Render, Heroku options.

## 🌐 Live API Features

## Features

- 🎵 **Audio URL Transcription**: Submit a public audio URL for transcription
- 📁 **File Upload Transcription**: Upload audio files directly for transcription
- 🔄 **Real-time Polling**: Automatically polls AssemblyAI until transcription is complete
- 🌐 **CORS Support**: Configured for frontend integration
- 📖 **Interactive API Docs**: Built-in Swagger/OpenAPI documentation

## Quick Start

### Prerequisites

- Python 3.8 or higher
- AssemblyAI API key ([Get one here](https://www.assemblyai.com/dashboard/))

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key:**
   - The `.env` file already exists with a placeholder
   - Replace `your_assemblyai_api_key_here` with your actual API key:
   ```bash
   # Edit backend/.env
   ASSEMBLYAI_API_KEY=your_actual_api_key_here
   ```

### Running the Server

#### Option 1: Using the batch script (Windows)
```bash
./run.bat
```

#### Option 2: Using Python directly
```bash
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

#### Option 3: Using the bash script (Linux/Mac)
```bash
./run.sh
```

### Testing the API

1. **Open the interactive API documentation:**
   - Visit: http://localhost:8000/docs
   - This provides a web interface to test all endpoints

2. **Run the test script:**
   ```bash
   python test_api.py
   ```

3. **Manual testing with curl:**
   ```bash
   # Test with a public audio URL
   curl -X POST "http://localhost:8000/transcribe-url" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "audio_url=https://storage.googleapis.com/aai-docs-samples/nbc.wav"
   ```

## API Endpoints

### POST `/transcribe-url`
Transcribe audio from a public URL.

**Request:**
- `audio_url` (form data): Public URL to an audio file

**Response:**
```json
{
  "transcript": "The transcribed text...",
  "metadata": {
    "transcription_id": "abc123",
    "audio_url": "https://example.com/audio.mp3",
    "status": "completed",
    "word_count": 150,
    "confidence": 0.95,
    "language": "en",
    "audio_duration": 30.5
  }
}
```

### POST `/transcribe-file`
Transcribe an uploaded audio file.

**Request:**
- `file` (multipart/form-data): Audio file upload

**Response:**
```json
{
  "transcript": "The transcribed text...",
  "metadata": {
    "transcription_id": "abc123",
    "filename": "audio.mp3",
    "status": "completed",
    "word_count": 150,
    "confidence": 0.95,
    "language": "en",
    "audio_duration": 30.5
  }
}
```

## Supported Audio Formats

- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- MP4 (.mp4)
- WebM (.webm)
- FLAC (.flac)

## Configuration

The application can be configured via environment variables in the `.env` file:

- `ASSEMBLYAI_API_KEY`: Your AssemblyAI API key (required)

## Troubleshooting

### Common Issues

1. **"Import assemblyai could not be resolved"**
   - Make sure you've installed the dependencies: `pip install -r requirements.txt`

2. **"Please set ASSEMBLYAI_API_KEY in backend/.env"**
   - Edit the `.env` file and add your actual AssemblyAI API key

3. **"Form data requires python-multipart to be installed"**
   - Install the missing dependency: `pip install python-multipart`

4. **Server won't start**
   - Check if port 8000 is already in use
   - Try a different port: `uvicorn app:app --port 8001`

### Getting Help

- Check the interactive API docs at http://localhost:8000/docs
- Review the server logs in the terminal
- Test with the provided `test_api.py` script

## Development

The server runs with auto-reload enabled, so changes to the code will automatically restart the server during development.

For production deployment, remove the `--reload` flag and consider using a production WSGI server like Gunicorn.
