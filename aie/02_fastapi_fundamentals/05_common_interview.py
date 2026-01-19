"""
FASTAPI 05: Common Interview Patterns
=====================================

Patterns that come up in AI Engineer interviews.

These are the "how would you..." questions:
- How would you add rate limiting?
- How would you add logging?
- How would you handle authentication?
- How would you do health checks?

Run: uvicorn 05_common_interview:app --reload
"""

from fastapi import FastAPI, Request, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import time
from typing import Optional
from collections import defaultdict
import asyncio

app = FastAPI(title="Interview Patterns Demo")


# =============================================================================
# PATTERN 1: REQUEST LOGGING MIDDLEWARE
# =============================================================================

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log every request with timing.
    
    Middleware runs for EVERY request.
    Good for: logging, timing, adding headers
    """
    start = time.time()
    
    # Get request info
    method = request.method
    path = request.url.path
    
    # Call the actual endpoint
    response = await call_next(request)
    
    # Log after response
    duration_ms = (time.time() - start) * 1000
    print(f"{method} {path} - {response.status_code} - {duration_ms:.1f}ms")
    
    # Add timing header
    response.headers["X-Response-Time-MS"] = str(int(duration_ms))
    
    return response


# =============================================================================
# PATTERN 2: SIMPLE RATE LIMITING
# =============================================================================

# In-memory rate limit store (use Redis in production)
rate_limit_store: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT = 10  # requests
RATE_WINDOW = 60  # seconds


def check_rate_limit(client_ip: str) -> bool:
    """
    Check if client has exceeded rate limit.
    
    Simple sliding window implementation.
    """
    now = time.time()
    window_start = now - RATE_WINDOW
    
    # Remove old entries
    rate_limit_store[client_ip] = [
        t for t in rate_limit_store[client_ip] if t > window_start
    ]
    
    # Check limit
    if len(rate_limit_store[client_ip]) >= RATE_LIMIT:
        return False
    
    # Add current request
    rate_limit_store[client_ip].append(now)
    return True


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """
    Rate limiting middleware.
    
    Returns 429 if rate limit exceeded.
    """
    client_ip = request.client.host if request.client else "unknown"
    
    # Skip rate limiting for health checks
    if request.url.path == "/health":
        return await call_next(request)
    
    if not check_rate_limit(client_ip):
        return JSONResponse(
            status_code=429,
            content={"error": "RATE_LIMIT_EXCEEDED", "retry_after": 60}
        )
    
    return await call_next(request)


# =============================================================================
# PATTERN 3: API KEY AUTHENTICATION
# =============================================================================

# Fake API keys (use database in production)
VALID_API_KEYS = {"sk-test-key-123", "sk-prod-key-456"}


async def verify_api_key(x_api_key: str = Header(...)):
    """
    Dependency that verifies API key.
    
    Add to endpoints that need auth:
        @app.get("/protected", dependencies=[Depends(verify_api_key)])
    """
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return x_api_key


@app.get("/protected")
async def protected_endpoint(api_key: str = Depends(verify_api_key)):
    """
    Endpoint that requires API key.
    
    Call with header: X-API-Key: sk-test-key-123
    """
    return {"message": "You have access!", "key_used": api_key[:10] + "..."}


@app.get("/public")
async def public_endpoint():
    """
    Public endpoint - no auth required.
    """
    return {"message": "Anyone can access this"}


# =============================================================================
# PATTERN 4: HEALTH CHECKS
# =============================================================================

# Service states
services = {
    "database": True,
    "cache": True,
    "llm_api": True,
}


class HealthResponse(BaseModel):
    status: str
    services: dict[str, str]
    version: str


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Comprehensive health check.
    
    Returns status of all dependencies.
    Used by: load balancers, Kubernetes, monitoring
    """
    service_status = {}
    all_healthy = True
    
    for service, is_up in services.items():
        if is_up:
            service_status[service] = "healthy"
        else:
            service_status[service] = "unhealthy"
            all_healthy = False
    
    return HealthResponse(
        status="healthy" if all_healthy else "degraded",
        services=service_status,
        version="1.0.0"
    )


@app.get("/ready")
async def readiness_check():
    """
    Readiness check - is the service ready to accept traffic?
    
    Different from health:
    - Health: is the process alive?
    - Ready: is it ready to serve requests?
    """
    # Check critical dependencies
    if not services["database"]:
        raise HTTPException(status_code=503, detail="Database not ready")
    
    return {"ready": True}


# =============================================================================
# PATTERN 5: CORS (Cross-Origin Resource Sharing)
# =============================================================================

# CORS must be added AFTER other middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourfrontend.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# PATTERN 6: REQUEST ID TRACKING
# =============================================================================

import uuid


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """
    Add unique request ID to every request.
    
    Essential for debugging and log correlation.
    """
    request_id = str(uuid.uuid4())[:8]
    
    # Store in request state for use in endpoint
    request.state.request_id = request_id
    
    response = await call_next(request)
    
    # Add to response headers
    response.headers["X-Request-ID"] = request_id
    
    return response


@app.get("/request-info")
async def request_info(request: Request):
    """
    Show request ID.
    """
    return {"request_id": request.state.request_id}


# =============================================================================
# PATTERN 7: DEPENDENCY INJECTION
# =============================================================================

class DatabaseConnection:
    """Fake database connection."""
    def __init__(self):
        self.connected = True
    
    async def query(self, sql: str):
        await asyncio.sleep(0.1)
        return [{"id": 1, "data": "result"}]


# Dependency that provides database connection
async def get_db():
    """
    Dependency that provides database connection.
    
    FastAPI calls this for each request that needs it.
    """
    db = DatabaseConnection()
    try:
        yield db
    finally:
        # Cleanup (close connection, etc.)
        pass


@app.get("/users-from-db")
async def get_users(db: DatabaseConnection = Depends(get_db)):
    """
    Endpoint using dependency injection.
    
    The 'db' parameter is automatically provided by FastAPI.
    """
    results = await db.query("SELECT * FROM users")
    return {"users": results}


# =============================================================================
# PATTERN 8: CACHING
# =============================================================================

# Simple in-memory cache (use Redis in production)
cache: dict[str, tuple[float, any]] = {}
CACHE_TTL = 60  # seconds


def get_cached(key: str):
    """Get from cache if not expired."""
    if key in cache:
        timestamp, value = cache[key]
        if time.time() - timestamp < CACHE_TTL:
            return value
    return None


def set_cached(key: str, value: any):
    """Set cache with timestamp."""
    cache[key] = (time.time(), value)


@app.get("/expensive-operation")
async def expensive_operation(param: str):
    """
    Endpoint with caching.
    
    First call: slow (simulated expensive operation)
    Subsequent calls: fast (from cache)
    """
    cache_key = f"expensive:{param}"
    
    # Check cache
    cached = get_cached(cache_key)
    if cached:
        return {"result": cached, "source": "cache"}
    
    # Expensive operation
    await asyncio.sleep(2)
    result = f"Computed result for {param}"
    
    # Cache result
    set_cached(cache_key, result)
    
    return {"result": result, "source": "computed"}


# =============================================================================
# INTERVIEW QUESTIONS CHEAT SHEET
# =============================================================================
"""
Q: "How would you add rate limiting?"
A: Middleware that tracks requests per IP in Redis/memory, returns 429 if exceeded.

Q: "How would you add authentication?"
A: Dependency that validates API key/JWT from header, raises 401 if invalid.

Q: "How would you add logging?"
A: Middleware that logs request method, path, status, and duration for each request.

Q: "How would you add caching?"
A: Check cache before expensive operations, store results with TTL, use Redis for distributed cache.

Q: "How would you do health checks?"
A: Separate /health (is process alive) and /ready (are dependencies up) endpoints.

Q: "How would you handle CORS?"
A: CORSMiddleware with explicit allowed origins, methods, and headers.

Q: "How would you track requests for debugging?"
A: Add unique request ID to each request, include in logs and response headers.

Q: "How would you structure a large FastAPI app?"
A: Split into routers (app.include_router), separate concerns into files.
"""


# =============================================================================
# BONUS: SIMPLE ROUTER EXAMPLE
# =============================================================================

from fastapi import APIRouter

# Create a router for a group of related endpoints
users_router = APIRouter(prefix="/v1/users", tags=["users"])


@users_router.get("/")
async def list_users():
    return {"users": []}


@users_router.get("/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}


# Include router in main app
app.include_router(users_router)


# =============================================================================
# KEY TAKEAWAYS
# =============================================================================
"""
1. Middleware: Runs for every request (logging, rate limiting)
2. Dependencies: Inject shared resources (db, auth)
3. Health checks: /health and /ready for different purposes
4. Rate limiting: Track requests per client, return 429
5. Authentication: Validate headers, return 401/403
6. Caching: Check cache first, store with TTL
7. Request tracking: Unique ID for debugging
8. Routers: Organize large apps into modules

These patterns appear in almost every AI Engineer interview.
Practice explaining each in 60 seconds.
"""
