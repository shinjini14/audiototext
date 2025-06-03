import json

# Simple health check for Vercel
def handler(request):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "status": "healthy",
            "message": "AudioToText API is running",
            "timestamp": "2025-01-04"
        })
    }
