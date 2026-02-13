# Resilient LLM Call Service

Pattern: schema_retry
Difficulty: medium

Implement a function used by `POST /generate` that:

1. Calls `fetch_llm()` with retry and exponential backoff
2. Validates returned JSON against schema:
   - `answer: str`
   - `confidence: float`
3. Returns structured error details if retries or validation fail

Constraints:

- Retry up to 3 attempts.
- Only retry network/runtime failures, not schema failures.
- Surface which attempt succeeded in the response.

Interview follow-up:

- How would you add jitter?
- What telemetry would you capture per attempt?
