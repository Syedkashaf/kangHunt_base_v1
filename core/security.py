from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
import os
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Dictionary to track API request timestamps for rate limiting
request_tracker = {}

# Rate limiting configuration
RATE_LIMIT_REQUESTS = 5
RATE_LIMIT_WINDOW_SEC = 60

async def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Validates incoming API key and enforces rate limiting.
    
    Step 1: Check if the provided API key matches the configured key.
    Step 2: Track request timestamps and ensure rate limit isn't exceeded.
    """
    # Check if the API key is valid
    expected_key = os.getenv("CORE_API_KEY")
    if api_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied: Invalid API Key"
        )
        
    # Rate limiting implementation
    current_time = time.time()
    
    # Initialize request list for this API key if not exists
    if api_key not in request_tracker:
        request_tracker[api_key] = []
        
    # Remove timestamps outside the rate limit window
    request_tracker[api_key] = [
        timestamp for timestamp in request_tracker[api_key] 
        if current_time - timestamp < RATE_LIMIT_WINDOW_SEC
    ]
    
    # Check if rate limit has been exceeded
    if len(request_tracker[api_key]) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate Limit Exceeded: Maximum {RATE_LIMIT_REQUESTS} requests per minute allowed."
        )
        
    # Record this request and allow access
    request_tracker[api_key].append(current_time)
    
    return api_key
