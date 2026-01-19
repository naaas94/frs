"""
FASTAPI 03: Error Handling
==========================

Proper error responses for production APIs.

Key concepts:
- HTTPException for expected errors
- Exception handlers for unexpected errors
- Consistent error response format

Run: uvicorn 03_error_handling:app --reload
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Error Handling Demo")


# =============================================================================
# BASIC HTTP EXCEPTIONS
# =============================================================================

# Fake database
users_db = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    """
    Get user by ID with proper error handling.
    
    HTTPException is the standard way to return error responses:
    - status_code: HTTP status (404, 400, 500, etc.)
    - detail: Error message (string or dict)
    """
    if user_id not in users_db:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} not found"
        )
    return users_db[user_id]


@app.delete("/users/{user_id}")
def delete_user(user_id: int, confirm: bool = False):
    """
    Delete user with confirmation check.
    
    400 Bad Request = client error (missing/invalid input)
    """
    if not confirm:
        raise HTTPException(
            status_code=400,
            detail="Must confirm deletion with ?confirm=true"
        )
    
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    del users_db[user_id]
    return {"deleted": user_id}


# =============================================================================
# STRUCTURED ERROR RESPONSES
# =============================================================================

class ErrorDetail(BaseModel):
    """Structured error response."""
    code: str
    message: str
    field: Optional[str] = None


@app.post("/register")
def register_user(username: str, email: str):
    """
    Registration with structured errors.
    
    Return error details as dict for more info.
    """
    errors = []
    
    if len(username) < 3:
        errors.append(ErrorDetail(
            code="USERNAME_TOO_SHORT",
            message="Username must be at least 3 characters",
            field="username"
        ))
    
    if "@" not in email:
        errors.append(ErrorDetail(
            code="INVALID_EMAIL",
            message="Email must contain @",
            field="email"
        ))
    
    if errors:
        raise HTTPException(
            status_code=422,
            detail=[e.model_dump() for e in errors]
        )
    
    return {"username": username, "email": email}


# =============================================================================
# CUSTOM EXCEPTION CLASSES
# =============================================================================

class ModelNotLoadedError(Exception):
    """Raised when ML model is not loaded."""
    def __init__(self, model_name: str):
        self.model_name = model_name


class RateLimitExceeded(Exception):
    """Raised when rate limit is exceeded."""
    def __init__(self, retry_after: int):
        self.retry_after = retry_after


# Register custom exception handlers
@app.exception_handler(ModelNotLoadedError)
async def model_not_loaded_handler(request: Request, exc: ModelNotLoadedError):
    """
    Custom handler for ModelNotLoadedError.
    
    Returns 503 Service Unavailable - appropriate when service is temporarily down.
    """
    return JSONResponse(
        status_code=503,
        content={
            "error": "MODEL_NOT_LOADED",
            "message": f"Model '{exc.model_name}' is not loaded",
            "retry_after": 30,
        }
    )


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """
    Custom handler for rate limiting.
    
    Returns 429 Too Many Requests with Retry-After header.
    """
    return JSONResponse(
        status_code=429,
        content={
            "error": "RATE_LIMIT_EXCEEDED",
            "message": "Too many requests",
            "retry_after": exc.retry_after,
        },
        headers={"Retry-After": str(exc.retry_after)}
    )


# Example endpoints using custom exceptions
model_loaded = False


@app.post("/predict")
def predict(text: str):
    """
    Prediction endpoint that requires loaded model.
    """
    if not model_loaded:
        raise ModelNotLoadedError("sentiment-classifier")
    
    return {"prediction": "positive", "confidence": 0.95}


@app.post("/generate")
def generate(prompt: str):
    """
    Example with rate limiting.
    
    In production, you'd track request counts per user/IP.
    """
    # Simulated rate limit check
    import random
    if random.random() < 0.3:  # 30% chance of rate limit
        raise RateLimitExceeded(retry_after=60)
    
    return {"response": f"Generated for: {prompt}"}


# =============================================================================
# GLOBAL EXCEPTION HANDLER
# =============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Catch-all for unexpected errors.
    
    IMPORTANT: In production, you should:
    - Log the full traceback
    - Send to error tracking (Sentry, etc.)
    - Return generic message (don't leak internal details)
    """
    # In production: log exc with traceback
    print(f"Unexpected error: {exc}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred",
        }
    )


@app.get("/crash")
def intentional_crash():
    """
    Test endpoint that crashes.
    
    The global exception handler catches this.
    """
    raise RuntimeError("Something went wrong!")


# =============================================================================
# VALIDATION ERROR HANDLER
# =============================================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom handler for Pydantic validation errors.
    
    Default FastAPI response is detailed but verbose.
    This simplifies it.
    """
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Request validation failed",
            "details": errors,
        }
    )


# =============================================================================
# AI ENGINEER PATTERN: LLM Error Handling
# =============================================================================

class LLMError(Exception):
    """Base class for LLM errors."""
    pass


class LLMTimeoutError(LLMError):
    """LLM API timed out."""
    pass


class LLMRateLimitError(LLMError):
    """LLM API rate limited."""
    def __init__(self, retry_after: int = 60):
        self.retry_after = retry_after


class LLMInvalidResponseError(LLMError):
    """LLM returned invalid/unparseable response."""
    def __init__(self, raw_response: str):
        self.raw_response = raw_response


@app.exception_handler(LLMTimeoutError)
async def llm_timeout_handler(request: Request, exc: LLMTimeoutError):
    return JSONResponse(
        status_code=504,  # Gateway Timeout
        content={"error": "LLM_TIMEOUT", "message": "LLM request timed out"}
    )


@app.exception_handler(LLMRateLimitError)
async def llm_rate_limit_handler(request: Request, exc: LLMRateLimitError):
    return JSONResponse(
        status_code=429,
        content={"error": "LLM_RATE_LIMITED", "retry_after": exc.retry_after}
    )


@app.exception_handler(LLMInvalidResponseError)
async def llm_invalid_response_handler(request: Request, exc: LLMInvalidResponseError):
    return JSONResponse(
        status_code=502,  # Bad Gateway
        content={
            "error": "LLM_INVALID_RESPONSE",
            "message": "LLM returned unparseable response",
            # In production, don't expose raw_response to users
        }
    )


# =============================================================================
# HTTP STATUS CODE CHEAT SHEET
# =============================================================================
"""
Common status codes for AI/ML APIs:

SUCCESS:
- 200 OK: Request succeeded
- 201 Created: Resource created
- 202 Accepted: Request accepted for async processing

CLIENT ERRORS (4xx):
- 400 Bad Request: Invalid input
- 401 Unauthorized: Not authenticated
- 403 Forbidden: Not authorized
- 404 Not Found: Resource doesn't exist
- 422 Unprocessable Entity: Validation failed
- 429 Too Many Requests: Rate limited

SERVER ERRORS (5xx):
- 500 Internal Server Error: Unexpected error
- 502 Bad Gateway: Upstream service error (LLM returned bad response)
- 503 Service Unavailable: Service temporarily down (model not loaded)
- 504 Gateway Timeout: Upstream timeout (LLM took too long)
"""


# =============================================================================
# KEY TAKEAWAYS
# =============================================================================
"""
1. HTTPException: Standard way to return errors
2. Custom exceptions: Define domain-specific errors
3. Exception handlers: @app.exception_handler(MyError)
4. Global handler: Catch-all for unexpected errors
5. Structured errors: Return consistent error format

FOR AI ENGINEERS:
- Use 503 when model not loaded
- Use 504 when LLM times out
- Use 502 when LLM returns bad response
- Use 429 for rate limiting
- Always log unexpected errors

NEXT: 04_async_patterns.py - Async operations for LLM calls
"""
