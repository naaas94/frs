"""
FASTAPI 04: Async Patterns
==========================

Async/await for non-blocking operations.

Essential for AI Engineers because:
- LLM API calls take 1-30 seconds
- Blocking = server can only handle one request at a time
- Async = server can handle thousands of concurrent requests

Run: uvicorn 04_async_patterns:app --reload
"""

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import asyncio
import httpx
import time
from typing import Optional

app = FastAPI(title="Async Patterns Demo")


# =============================================================================
# SYNC VS ASYNC
# =============================================================================

@app.get("/sync")
def sync_endpoint():
    """
    Synchronous endpoint.
    
    When this sleeps, the entire worker thread is blocked.
    Other requests must wait.
    
    Use for: CPU-bound work, quick operations
    """
    time.sleep(1)  # Blocks the thread
    return {"type": "sync", "waited": 1}


@app.get("/async")
async def async_endpoint():
    """
    Asynchronous endpoint.
    
    When this awaits, the thread is free to handle other requests.
    
    Use for: I/O-bound work (API calls, database queries, file I/O)
    """
    await asyncio.sleep(1)  # Non-blocking
    return {"type": "async", "waited": 1}


# =============================================================================
# ASYNC HTTP CALLS (httpx)
# =============================================================================

@app.get("/fetch")
async def fetch_external():
    """
    Make async HTTP request.
    
    httpx is the async-friendly alternative to requests.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get("https://httpbin.org/get")
        return {"status": response.status_code, "data": response.json()}


@app.get("/fetch-multiple")
async def fetch_multiple():
    """
    Make multiple HTTP requests concurrently.
    
    This is the power of async: all 3 requests run in parallel.
    Total time ≈ max(request times), not sum.
    """
    async with httpx.AsyncClient() as client:
        # Create tasks for concurrent execution
        tasks = [
            client.get("https://httpbin.org/delay/1"),
            client.get("https://httpbin.org/delay/1"),
            client.get("https://httpbin.org/delay/1"),
        ]
        
        # Wait for all to complete
        start = time.time()
        responses = await asyncio.gather(*tasks)
        elapsed = time.time() - start
        
        return {
            "message": "3 requests, each with 1s delay",
            "total_time": round(elapsed, 2),
            "expected": "~1s (parallel) not 3s (sequential)"
        }


# =============================================================================
# AI ENGINEER PATTERN: LLM API CALL
# =============================================================================

class LLMRequest(BaseModel):
    prompt: str
    model: str = "gpt-4"


class LLMResponse(BaseModel):
    response: str
    model: str
    latency_ms: int


async def call_llm_api(prompt: str, model: str) -> dict:
    """
    Simulated async LLM API call.
    
    In production, replace with actual OpenAI/Anthropic call:
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": model, "messages": [{"role": "user", "content": prompt}]},
            timeout=30.0
        )
        return response.json()
    """
    # Simulate LLM latency (1-3 seconds)
    await asyncio.sleep(2)
    return {
        "response": f"[{model}] Response to: {prompt[:50]}...",
        "model": model,
    }


@app.post("/generate", response_model=LLMResponse)
async def generate(request: LLMRequest):
    """
    Async LLM generation endpoint.
    """
    start = time.time()
    result = await call_llm_api(request.prompt, request.model)
    latency = int((time.time() - start) * 1000)
    
    return LLMResponse(
        response=result["response"],
        model=result["model"],
        latency_ms=latency
    )


# =============================================================================
# PARALLEL LLM CALLS
# =============================================================================

@app.post("/generate-multiple")
async def generate_multiple(prompts: list[str]):
    """
    Generate responses for multiple prompts in parallel.
    
    Common pattern for:
    - Batch processing
    - Calling multiple models for comparison
    - Fallback chains
    """
    start = time.time()
    
    # Create tasks for all prompts
    tasks = [call_llm_api(prompt, "gpt-4") for prompt in prompts]
    
    # Run in parallel
    results = await asyncio.gather(*tasks)
    
    elapsed = time.time() - start
    
    return {
        "results": results,
        "total_prompts": len(prompts),
        "total_time_seconds": round(elapsed, 2),
        "avg_time_per_prompt": round(elapsed / len(prompts), 2),
    }


# =============================================================================
# TIMEOUT HANDLING
# =============================================================================

@app.post("/generate-with-timeout")
async def generate_with_timeout(prompt: str, timeout_seconds: float = 5.0):
    """
    LLM call with timeout.
    
    Essential for production: LLMs can hang or take forever.
    """
    try:
        result = await asyncio.wait_for(
            call_llm_api(prompt, "gpt-4"),
            timeout=timeout_seconds
        )
        return result
    except asyncio.TimeoutError:
        return {"error": "LLM_TIMEOUT", "message": f"Request timed out after {timeout_seconds}s"}


# =============================================================================
# BACKGROUND TASKS
# =============================================================================

async def send_webhook(url: str, data: dict):
    """Background task: send webhook notification."""
    await asyncio.sleep(0.5)  # Simulate network delay
    print(f"Webhook sent to {url}: {data}")


async def log_request(request_id: str, prompt: str):
    """Background task: log request to database/file."""
    await asyncio.sleep(0.1)
    print(f"Logged request {request_id}: {prompt[:50]}")


@app.post("/generate-with-webhook")
async def generate_with_webhook(
    request: LLMRequest,
    webhook_url: Optional[str] = None,
    background_tasks: BackgroundTasks = None
):
    """
    Generate response and send webhook in background.
    
    Background tasks run AFTER the response is sent.
    Use for: logging, webhooks, cleanup, notifications
    """
    request_id = str(int(time.time() * 1000))
    
    # Generate response
    result = await call_llm_api(request.prompt, request.model)
    
    # Schedule background tasks (run after response)
    if background_tasks:
        background_tasks.add_task(log_request, request_id, request.prompt)
        if webhook_url:
            background_tasks.add_task(send_webhook, webhook_url, result)
    
    return {
        "request_id": request_id,
        "response": result["response"],
        "webhook_scheduled": webhook_url is not None
    }


# =============================================================================
# SEMAPHORE: LIMIT CONCURRENT CALLS
# =============================================================================

# Limit concurrent LLM calls to prevent overwhelming the API
llm_semaphore = asyncio.Semaphore(5)


async def call_llm_with_limit(prompt: str) -> dict:
    """
    Call LLM with concurrency limit.
    
    Semaphore ensures at most N concurrent calls.
    Essential for respecting rate limits.
    """
    async with llm_semaphore:
        return await call_llm_api(prompt, "gpt-4")


@app.post("/batch-generate")
async def batch_generate(prompts: list[str]):
    """
    Generate for many prompts with limited concurrency.
    
    Even with 100 prompts, only 5 run at a time.
    """
    start = time.time()
    
    tasks = [call_llm_with_limit(prompt) for prompt in prompts]
    results = await asyncio.gather(*tasks)
    
    return {
        "results": results,
        "count": len(results),
        "elapsed": round(time.time() - start, 2),
        "concurrent_limit": 5,
    }


# =============================================================================
# STREAMING RESPONSES (SSE)
# =============================================================================

from fastapi.responses import StreamingResponse


async def generate_stream(prompt: str):
    """
    Generator that yields tokens one at a time.
    
    Simulates LLM streaming output.
    """
    words = f"Here is a response to your prompt about {prompt}".split()
    for word in words:
        yield f"data: {word}\n\n"
        await asyncio.sleep(0.2)
    yield "data: [DONE]\n\n"


@app.get("/stream")
async def stream_response(prompt: str):
    """
    Server-Sent Events (SSE) for streaming LLM output.
    
    This is how ChatGPT shows tokens as they're generated.
    """
    return StreamingResponse(
        generate_stream(prompt),
        media_type="text/event-stream"
    )


# =============================================================================
# KEY TAKEAWAYS
# =============================================================================
"""
1. async def + await: Non-blocking I/O
2. httpx.AsyncClient: Async HTTP calls
3. asyncio.gather: Run tasks in parallel
4. asyncio.wait_for: Add timeout
5. BackgroundTasks: Run after response
6. Semaphore: Limit concurrency
7. StreamingResponse: SSE for streaming

FOR AI ENGINEERS:
- Always use async for LLM calls
- Use gather for parallel calls
- Always set timeouts
- Use semaphores for rate limiting
- Use streaming for real-time UX

NEXT: 05_common_interview.py - Patterns they ask about in interviews
"""
