"""
API RETRY PATTERN
=================

Call external APIs with automatic retry and exponential backoff.

Pattern: try → catch → sleep → retry (with limit)

When to use:
- Calling LLM APIs (OpenAI, Anthropic, etc.) - they fail often
- Any external HTTP API call
- Database connections
- Any operation that can fail transiently

Time target: Write from memory in < 3 minutes
"""

import time
from typing import Callable, TypeVar, Any
from functools import wraps

T = TypeVar("T")


# =============================================================================
# THE CORE PATTERN
# =============================================================================

def call_with_retry(
    fn: Callable[[], T],
    max_attempts: int = 3,
    base_delay: float = 1.0,
) -> T:
    """
    Call a function with retry on exception.
    
    Uses exponential backoff: delay doubles each attempt.
    - Attempt 1: immediate
    - Attempt 2: wait 1s
    - Attempt 3: wait 2s
    
    Args:
        fn: Zero-argument function to call
        max_attempts: Maximum number of tries
        base_delay: Initial delay in seconds
    
    Returns:
        Result of fn() if successful
    
    Raises:
        Last exception if all attempts fail
    """
    last_exception = None
    
    for attempt in range(max_attempts):
        try:
            return fn()
        except Exception as e:
            last_exception = e
            
            # If this was the last attempt, don't sleep
            if attempt == max_attempts - 1:
                raise
            
            # Exponential backoff: 1s, 2s, 4s, ...
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)
    
    # Should never reach here, but satisfy type checker
    raise last_exception  # type: ignore


# =============================================================================
# VARIATION 1: Decorator Version
# =============================================================================

def retry(max_attempts: int = 3, base_delay: float = 1.0):
    """
    Decorator version of retry pattern.
    
    Usage:
        @retry(max_attempts=3)
        def call_api():
            return requests.get(url)
    """
    def decorator(fn: Callable[..., T]) -> Callable[..., T]:
        @wraps(fn)
        def wrapper(*args, **kwargs) -> T:
            return call_with_retry(
                lambda: fn(*args, **kwargs),
                max_attempts=max_attempts,
                base_delay=base_delay,
            )
        return wrapper
    return decorator


# =============================================================================
# VARIATION 2: With Specific Exceptions
# =============================================================================

def retry_on(
    fn: Callable[[], T],
    exceptions: tuple[type[Exception], ...],
    max_attempts: int = 3,
    base_delay: float = 1.0,
) -> T:
    """
    Only retry on specific exception types.
    Other exceptions propagate immediately.
    
    Example:
        retry_on(call_api, (TimeoutError, ConnectionError))
    """
    for attempt in range(max_attempts):
        try:
            return fn()
        except exceptions as e:
            if attempt == max_attempts - 1:
                raise
            time.sleep(base_delay * (2 ** attempt))
        # Non-matching exceptions propagate immediately
    
    raise RuntimeError("Unreachable")


# =============================================================================
# VARIATION 3: With Jitter (Prevent Thundering Herd)
# =============================================================================

import random

def retry_with_jitter(
    fn: Callable[[], T],
    max_attempts: int = 3,
    base_delay: float = 1.0,
    jitter: float = 0.5,
) -> T:
    """
    Add random jitter to prevent thundering herd.
    
    When many clients retry at the same time, they can overwhelm the server.
    Jitter spreads out the retries.
    
    jitter=0.5 means delay varies by ±50%
    """
    for attempt in range(max_attempts):
        try:
            return fn()
        except Exception:
            if attempt == max_attempts - 1:
                raise
            
            delay = base_delay * (2 ** attempt)
            # Add jitter: delay * (1 ± jitter)
            jittered_delay = delay * (1 + random.uniform(-jitter, jitter))
            time.sleep(jittered_delay)
    
    raise RuntimeError("Unreachable")


# =============================================================================
# VARIATION 4: With Callback/Logging
# =============================================================================

def retry_with_callback(
    fn: Callable[[], T],
    max_attempts: int = 3,
    base_delay: float = 1.0,
    on_retry: Callable[[int, Exception], None] | None = None,
) -> T:
    """
    Call a callback on each retry (for logging/monitoring).
    
    Example:
        def log_retry(attempt, error):
            print(f"Attempt {attempt} failed: {error}")
        
        retry_with_callback(call_api, on_retry=log_retry)
    """
    for attempt in range(max_attempts):
        try:
            return fn()
        except Exception as e:
            if on_retry:
                on_retry(attempt + 1, e)
            
            if attempt == max_attempts - 1:
                raise
            
            time.sleep(base_delay * (2 ** attempt))
    
    raise RuntimeError("Unreachable")


# =============================================================================
# VARIATION 5: Async Version
# =============================================================================

import asyncio

async def retry_async(
    fn: Callable[[], Any],  # Can be sync or async
    max_attempts: int = 3,
    base_delay: float = 1.0,
) -> Any:
    """
    Async version of retry pattern.
    
    Works with both sync and async functions.
    """
    for attempt in range(max_attempts):
        try:
            result = fn()
            # Handle both sync and async functions
            if asyncio.iscoroutine(result):
                return await result
            return result
        except Exception:
            if attempt == max_attempts - 1:
                raise
            await asyncio.sleep(base_delay * (2 ** attempt))
    
    raise RuntimeError("Unreachable")


# =============================================================================
# REAL-WORLD EXAMPLE: LLM API Call
# =============================================================================

def call_llm_with_retry(prompt: str, model: str = "gpt-4") -> dict:
    """
    Example of how you'd call an LLM API with retry.
    
    In a real implementation, you'd use openai or httpx.
    """
    def make_request():
        # Simulate API call (replace with actual implementation)
        import random
        if random.random() < 0.3:  # 30% failure rate
            raise ConnectionError("API temporarily unavailable")
        return {"response": f"Answer to: {prompt}", "model": model}
    
    return call_with_retry(make_request, max_attempts=3, base_delay=1.0)


# =============================================================================
# PRACTICE PROBLEMS
# =============================================================================
"""
Practice these until you can solve each in under 5 minutes.

PROBLEM 1: Basic Retry
----------------------
Task: Write a function that calls an API, retrying up to 3 times with 1s delay.
Test: Mock function that fails first 2 times, succeeds on 3rd.
Expected: Returns result after 3rd attempt.

PROBLEM 2: Retry Decorator
--------------------------
Task: Write a @retry decorator that wraps any function.
Usage: @retry(max_attempts=3, delay=1.0)
Test: Decorate a flaky function, verify it retries.

PROBLEM 3: Specific Exceptions
------------------------------
Task: Only retry on TimeoutError and ConnectionError, not ValueError.
Test: Function that raises ValueError should fail immediately.

PROBLEM 4: With Jitter
----------------------
Task: Add ±25% jitter to delay.
Test: Run multiple retries, verify delays are randomized.

PROBLEM 5: Async Retry
----------------------
Task: Write async version using asyncio.sleep.
Test: Async function that fails twice, verify await works.

PROBLEM 6: Full LLM Pattern
---------------------------
Task: Combine retry with:
  - Parse JSON response
  - Validate against schema
  - Return structured result or error
This combines all 3 core patterns!
"""


# =============================================================================
# SELF-TEST
# =============================================================================

if __name__ == "__main__":
    # Test basic retry
    print("Test 1: Retry succeeds on 3rd attempt")
    
    call_counter = [0]  # Use list to avoid nonlocal issues at module level
    def flaky_function():
        call_counter[0] += 1
        if call_counter[0] < 3:
            raise ConnectionError(f"Failed attempt {call_counter[0]}")
        return "success"
    
    result = call_with_retry(flaky_function, max_attempts=3, base_delay=0.1)
    print(f"  Result: {result}")
    print(f"  Attempts: {call_counter[0]}")
    assert result == "success"
    assert call_counter[0] == 3
    
    # Test that it raises after max attempts
    print("\nTest 2: Raises after max attempts")
    
    def always_fails():
        raise ValueError("Always fails")
    
    try:
        call_with_retry(always_fails, max_attempts=2, base_delay=0.1)
        assert False, "Should have raised"
    except ValueError as e:
        print(f"  Caught expected error: {e}")
    
    # Test decorator
    print("\nTest 3: Decorator version")
    
    dec_counter = [0]  # Use list to avoid nonlocal issues at module level
    
    @retry(max_attempts=3, base_delay=0.1)
    def decorated_flaky():
        dec_counter[0] += 1
        if dec_counter[0] < 2:
            raise RuntimeError("Fail")
        return "decorated success"
    
    result = decorated_flaky()
    print(f"  Result: {result}")
    assert result == "decorated success"
    
    print("\n✓ All tests passed!")
