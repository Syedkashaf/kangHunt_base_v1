from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
import os
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# In-memory dictionary to track requests (Format: {"api_key": [timestamp1, timestamp2]})
request_tracker = {}

# RATE LIMIT SETTINGS: 5 requests per 60 seconds
RATE_LIMIT_REQUESTS = 5
RATE_LIMIT_WINDOW_SEC = 60

async def verify_api_key(api_key: str = Security(api_key_header)):
    # 1. AUTHENTICATION CHECK
    expected_key = os.getenv("CORE_API_KEY")
    if api_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied: Invalid API Key"
        )
        
    # 2. RATE LIMITING LOGIC (Traffic Control)
    current_time = time.time()
    
    if api_key not in request_tracker:
        request_tracker[api_key] = []
        
    # Remove timestamps older than the window (60 seconds ago)
    request_tracker[api_key] = [
        timestamp for timestamp in request_tracker[api_key] 
        if current_time - timestamp < RATE_LIMIT_WINDOW_SEC
    ]
    
    # Check if the user exceeded the limit
    if len(request_tracker[api_key]) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate Limit Exceeded: Maximum {RATE_LIMIT_REQUESTS} requests per minute allowed."
        )
        
    # Add current request timestamp and allow access
    request_tracker[api_key].append(current_time)
    
    return api_key
