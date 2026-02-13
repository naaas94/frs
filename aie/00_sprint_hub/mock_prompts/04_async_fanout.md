# Async Fan-Out Aggregator

Pattern: fastapi_async
Difficulty: medium

Create `GET /aggregate` that calls three async providers concurrently:

- `provider_a()`
- `provider_b()`
- `provider_c()`

Return:

- Combined payload from successful providers
- Per-provider error details for failed providers
- Total latency in milliseconds

Constraints:

- Use `asyncio.gather` with error handling.
- Do not fail the whole request if one provider fails.
- Time out each provider call after 2 seconds.

Interview follow-up:

- When would you switch to background tasks or queues?
- How would you add circuit breakers?
