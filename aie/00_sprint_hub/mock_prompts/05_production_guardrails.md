# Production Guardrails API

Pattern: production_api
Difficulty: medium

Given a FastAPI app, add these guardrails:

- Request logging middleware with latency
- Basic per-IP rate limiting
- Health endpoint (`/health`)
- API key auth dependency for protected routes

Constraints:

- Keep public health endpoint unauthenticated.
- Return `429` on rate limits and `401` on auth failures.
- Add one test scenario per guardrail.

Interview follow-up:

- What should move from in-memory to Redis?
- What logs/metrics are must-have in production?
