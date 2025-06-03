from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        html = """<!DOCTYPE html>
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

    <footer style="text-align: center; margin-top: 50px; color: #666;">
        <p>AudioToText API - Powered by AssemblyAI</p>
        <p><a href="/api/health">Test Health Check</a></p>
    </footer>
</body>
</html>"""

        self.wfile.write(html.encode())
