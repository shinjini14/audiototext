# 🚀 Quick Deploy Guide - Get Your API Online in 5 Minutes!

## ⚡ Option 1: Ngrok (Fastest - 2 minutes)

**Perfect for instant sharing and testing**

### Step 1: Download Ngrok
- Go to: https://ngrok.com/download
- Download for Windows
- Extract the zip file

### Step 2: Start Your API
```bash
cd backend
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```
✅ Keep this terminal running!

### Step 3: Create Public Tunnel
Open a new terminal:
```bash
# Navigate to where you extracted ngrok
cd path/to/ngrok
./ngrok http 8000
```

### Step 4: Get Your Public URL
Ngrok will show something like:
```
Forwarding    https://abc123.ngrok.io -> http://localhost:8000
```

🎉 **Your API is now live!** Share `https://abc123.ngrok.io` with anyone!

### Test Your Deployed API:
- **API Docs**: https://abc123.ngrok.io/docs
- **Health Check**: https://abc123.ngrok.io/health
- **Test Transcription**:
  ```bash
  curl -X POST "https://abc123.ngrok.io/transcribe-url" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "audio_url=https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"
  ```

---

## 🏗️ Option 2: Railway (Permanent Free Hosting)

**For a permanent URL that doesn't require your computer to be on**

### Step 1: Create Railway Account
- Go to: https://railway.app
- Sign up with GitHub

### Step 2: Deploy
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Connect your repository
4. Railway will auto-detect the `railway.json` file and deploy!

### Step 3: Set Environment Variable
1. Go to your project dashboard
2. Click "Variables"
3. Add: `ASSEMBLYAI_API_KEY` = `your_actual_api_key`
4. Click "Deploy"

### Step 4: Get Your URL
Railway will provide a URL like: `https://your-app.railway.app`

---

## 🧪 Test Your Deployed API

Use this script to test any deployed API:

```bash
python test_deployed_api.py https://your-deployed-url.com
```

---

## 📱 Share Your API

Once deployed, share these links:

1. **📖 Interactive API Docs**: `https://your-url/docs`
   - Beautiful web interface to test the API
   - Shows all endpoints and parameters
   - Try it directly in the browser!

2. **🔗 Direct API Endpoint**: `https://your-url/transcribe-url`
   - For developers to integrate
   - Accepts POST requests with audio URLs

3. **❤️ Health Check**: `https://your-url/health`
   - Shows if the API is running
   - Good for monitoring

---

## 💡 Usage Examples for Others

Share these examples with people who want to use your API:

### Using curl:
```bash
curl -X POST "https://YOUR_URL/transcribe-url" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "audio_url=https://example.com/audio.mp3"
```

### Using Python:
```python
import requests

response = requests.post(
    "https://YOUR_URL/transcribe-url",
    data={"audio_url": "https://example.com/audio.mp3"}
)

result = response.json()
print(result["transcript"])
```

### Using JavaScript:
```javascript
const formData = new FormData();
formData.append('audio_url', 'https://example.com/audio.mp3');

fetch('https://YOUR_URL/transcribe-url', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data.transcript));
```

---

## 🎯 What Others Can Do With Your API

✅ **Upload audio files** (MP3, WAV, M4A, etc.)  
✅ **Provide audio URLs** from the internet  
✅ **Get accurate transcriptions** with confidence scores  
✅ **View metadata** (word count, duration, language)  
✅ **Use the interactive docs** at `/docs`  
✅ **Integrate into their own apps** with simple HTTP requests  

---

## 🔧 Troubleshooting

### Ngrok Issues:
- **"command not found"**: Make sure ngrok is in your PATH or run from the ngrok directory
- **"tunnel not found"**: Restart ngrok and get a new URL
- **"connection refused"**: Make sure your FastAPI server is running on port 8000

### Railway Issues:
- **Build failed**: Check that all files are committed to GitHub
- **Environment variable**: Make sure `ASSEMBLYAI_API_KEY` is set correctly
- **Timeout**: Railway has a 10-minute build timeout

### API Issues:
- **CORS errors**: The API allows all origins for demo purposes
- **Transcription fails**: Check that the audio URL is publicly accessible
- **Slow responses**: Large audio files take longer to process

---

## 🎉 Success!

Your AudioToText API is now live and shareable! 🚀

**Next Steps:**
1. Share your API URL with friends/colleagues
2. Test it with different audio files
3. Check the interactive docs at `/docs`
4. Monitor usage and performance

**Need help?** Check the full [DEPLOYMENT.md](DEPLOYMENT.md) guide for more options and details.
