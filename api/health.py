from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def health():
    return {"status": "healthy", "message": "AudioToText API is running"}

# Vercel handler
def handler(request):
    return health()
