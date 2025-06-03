# 🚀 AudioToText API Deployment Guide

Deploy your FastAPI backend to get a shareable public URL that others can access.

## 🎯 Quick Start Options

### Option 1: Ngrok (Instant - Recommended for Testing)

**Fastest way to get a public URL in 2 minutes!**

1. **Download Ngrok**: https://ngrok.com/download
2. **Extract and run**:
   ```bash
   # Terminal 1: Start your FastAPI server
   cd backend
   python -m uvicorn app:app --host 0.0.0.0 --port 8000
   
   # Terminal 2: Create public tunnel
   ngrok http 8000
   ```
3. **Get your URL**: Ngrok shows something like `https://abc123.ngrok.io`
4. **Share**: Send this URL to others - they can access your API!

**Test your deployed API:**
- API Docs: `https://your-ngrok-url.ngrok.io/docs`
- Health Check: `https://your-ngrok-url.ngrok.io/health`

---

### Option 2: Railway (Free Hosting - Permanent)

**Free hosting with permanent URL**

1. **Create account**: https://railway.app
2. **Connect GitHub**: Link your repository
3. **Deploy**: Railway auto-detects the `railway.json` file
4. **Set environment variable**: Add `ASSEMBLYAI_API_KEY` in Railway dashboard
5. **Get URL**: Railway provides a permanent URL like `https://your-app.railway.app`

---

### Option 3: Render (Free Hosting)

**Another free hosting option**

1. **Create account**: https://render.com
2. **Connect repository**: Link your GitHub repo
3. **Deploy**: Render uses the `render.yaml` file
4. **Set environment**: Add `ASSEMBLYAI_API_KEY` in Render dashboard
5. **Get URL**: Render provides URL like `https://your-app.onrender.com`

---

### Option 4: Heroku (Free Tier Available)

1. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli
2. **Deploy**:
   ```bash
   heroku create your-app-name
   heroku config:set ASSEMBLYAI_API_KEY=your_api_key_here
   git push heroku main
   ```
3. **Get URL**: `https://your-app-name.herokuapp.com`

---

## 🧪 Testing Your Deployed API

Once deployed, test with these commands (replace `YOUR_URL` with your actual URL):

### Test Health Check
```bash
curl https://YOUR_URL/health
```

### Test Transcription (URL)
```bash
curl -X POST "https://YOUR_URL/transcribe-url" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "audio_url=https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"
```

### Test with PowerShell
```powershell
Invoke-WebRequest -Uri "https://YOUR_URL/transcribe-url" -Method POST -ContentType "application/x-www-form-urlencoded" -Body "audio_url=https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"
```

---

## 📱 Share Your API

Once deployed, you can share:

1. **API Documentation**: `https://YOUR_URL/docs`
2. **Direct API endpoint**: `https://YOUR_URL/transcribe-url`
3. **Health check**: `https://YOUR_URL/health`

---

## 🔧 Environment Variables

All deployment platforms need this environment variable:

```
ASSEMBLYAI_API_KEY=your_actual_api_key_here
```

---

## 🚨 Important Notes

### Security
- The current CORS settings allow all origins (`"*"`) for demo purposes
- For production, remove the `"*"` and specify exact domains

### Rate Limits
- AssemblyAI has rate limits on their API
- Consider implementing rate limiting for production use

### File Size
- Current limit: 100MB per file
- Adjust based on your hosting platform's limits

---

## 🐛 Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Ensure `requirements.txt` includes all dependencies
   - Check Python version compatibility

2. **CORS errors**
   - Verify CORS settings in `app.py`
   - Check if your frontend domain is allowed

3. **Environment variable not found**
   - Ensure `ASSEMBLYAI_API_KEY` is set in your hosting platform
   - Check the variable name spelling

4. **Timeout errors**
   - Increase timeout settings in your hosting platform
   - AssemblyAI transcription can take time for long audio files

### Logs
Check your hosting platform's logs for detailed error messages:
- Railway: Dashboard → Deployments → Logs
- Render: Dashboard → Service → Logs
- Heroku: `heroku logs --tail`

---

## 🎉 Success!

Once deployed, your API will be accessible worldwide! Share the URL with others and they can:

- Upload audio files for transcription
- Provide audio URLs for transcription
- View the interactive API documentation
- Get JSON responses with transcripts and metadata

**Example deployed API**: `https://your-app.railway.app/docs`
