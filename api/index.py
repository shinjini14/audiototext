# Simple index page for Vercel
def handler(request):
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>AudioToText API</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .header { text-align: center; color: #333; }
        .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .method { color: #007acc; font-weight: bold; }
        .url { color: #d73a49; }
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
        <div>Health check endpoint</div>
        <a href="/api/health" class="test-btn">Test Health</a>
    </div>

    <div class="endpoint">
        <div><span class="method">POST</span> <span class="url">/api/transcribe-url</span></div>
        <div>Transcribe audio from a public URL</div>
        <div><strong>Form data:</strong> audio_url</div>
    </div>

    <h2>🧪 Quick Test</h2>
    <form action="/api/transcribe-url" method="post" style="background: #f8f9fa; padding: 20px; border-radius: 5px;">
        <label for="audio_url">Audio URL:</label><br>
        <input type="url" id="audio_url" name="audio_url"
               value="https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"
               style="width: 100%; padding: 8px; margin: 8px 0;">
        <br>
        <input type="submit" value="Transcribe Audio" class="test-btn" style="border: none; cursor: pointer;">
    </form>

    <footer style="text-align: center; margin-top: 50px; color: #666;">
        <p>AudioToText API - Powered by AssemblyAI</p>
    </footer>
</body>
</html>"""

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html",
            "Access-Control-Allow-Origin": "*"
        },
        "body": html_content
    }
