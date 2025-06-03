from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def root():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AudioToText API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            .header { text-align: center; color: #333; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { color: #007acc; font-weight: bold; }
            .url { color: #d73a49; }
            .description { color: #666; margin-top: 5px; }
            .test-btn { background: #28a745; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎵 AudioToText API</h1>
            <p>AI-powered audio transcription service using AssemblyAI</p>
        </div>
        
        <h2>📡 Available Endpoints</h2>
        
        <div class="endpoint">
            <div><span class="method">GET</span> <span class="url">/api/health</span></div>
            <div class="description">Health check endpoint</div>
            <a href="/api/health" class="test-btn">Test</a>
        </div>
        
        <div class="endpoint">
            <div><span class="method">POST</span> <span class="url">/api/transcribe-url</span></div>
            <div class="description">Transcribe audio from a public URL</div>
            <div class="description"><strong>Form data:</strong> audio_url</div>
        </div>
        
        <div class="endpoint">
            <div><span class="method">GET</span> <span class="url">/api/app/docs</span></div>
            <div class="description">Interactive API documentation (Swagger UI)</div>
            <a href="/api/app/docs" class="test-btn">Open Docs</a>
        </div>
        
        <h2>🧪 Quick Test</h2>
        <p>Test the transcription API with a sample audio file:</p>
        
        <form action="/api/transcribe-url" method="post" style="background: #f8f9fa; padding: 20px; border-radius: 5px;">
            <label for="audio_url">Audio URL:</label><br>
            <input type="url" id="audio_url" name="audio_url" 
                   value="https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"
                   style="width: 100%; padding: 8px; margin: 8px 0;">
            <br>
            <input type="submit" value="Transcribe Audio" class="test-btn" style="border: none; cursor: pointer;">
        </form>
        
        <h2>📖 Usage Examples</h2>
        
        <h3>Using curl:</h3>
        <pre style="background: #f6f8fa; padding: 15px; border-radius: 5px; overflow-x: auto;">
curl -X POST "https://audiototext-two.vercel.app/api/transcribe-url" \\
  -H "Content-Type: application/x-www-form-urlencoded" \\
  -d "audio_url=https://example.com/audio.mp3"</pre>
        
        <h3>Using Python:</h3>
        <pre style="background: #f6f8fa; padding: 15px; border-radius: 5px; overflow-x: auto;">
import requests

response = requests.post(
    "https://audiototext-two.vercel.app/api/transcribe-url",
    data={"audio_url": "https://example.com/audio.mp3"}
)

result = response.json()
print(result["transcript"])</pre>
        
        <footer style="text-align: center; margin-top: 50px; color: #666;">
            <p>AudioToText API - Powered by AssemblyAI</p>
        </footer>
    </body>
    </html>
    """)

# Vercel handler
def handler(request):
    return root()
