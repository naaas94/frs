# DevOps + Cloud Deployment Patterns

Goal: recognition-level readiness for common AIE deployment interview prompts.

---

## 1) Health Checks and Service Readiness

For FastAPI services, separate:

- Liveness: process is running (`/health/live`)
- Readiness: dependencies are available (`/health/ready`)

Why interviewers care:

- Prevent routing traffic to an unready pod
- Improve rollback behavior during deploys

Quick talking point:

> Liveness answers "should container restart?" and readiness answers "should this instance receive traffic?".

---

## 2) Config and Secrets

Baseline production pattern:

- Load config from environment variables
- Keep secrets in secret manager (not in code or images)
- Validate config at startup and fail fast

Interview prompt:

> How do you manage API keys for model providers across dev/stage/prod?

Strong answer:

- Per-environment secret stores
- Rotation policy
- Least privilege IAM

---

## 3) Containerizing a FastAPI App

Minimal flow:

1. Build image with pinned dependencies
2. Expose app on expected port
3. Run with Uvicorn (or Gunicorn+Uvicorn workers)
4. Add health endpoints for orchestrator checks

Example Dockerfile (conceptual):

```Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "aie.02_fastapi_fundamentals.01_hello_world:app", "--host", "0.0.0.0", "--port", "8080"]
```

---

## 4) Cloud Targets: What to Say

### Cloud Run

- Great for HTTP APIs, easy autoscaling to zero
- Fast to ship, less infrastructure overhead
- Watch cold starts and per-request timeout settings

### ECS/Fargate

- Good when you need VPC-heavy integration and custom networking
- More control, more operational surface area

### Lambda + API Gateway

- Good for bursty, event-driven APIs
- Constraint-heavy for long-running inference unless async pattern used

---

## 5) Observability Baseline

Minimum signals:

- Request count, p95/p99 latency, error rate
- Upstream provider latency/error split (LLM/provider-specific)
- Structured logs with request id and user/session id (when allowed)

Interview prompt:

> A model endpoint gets slower after deploy. What do you check first?

Suggested answer:

1. Compare p95 latency by endpoint and dependency
2. Inspect recent config/model/version changes
3. Check retries/timeouts and upstream saturation

---

## 6) Practice Prompts

1. "How would you deploy this FastAPI app safely with zero downtime?"
2. "How would you roll back if error rate doubles after release?"
3. "What metrics decide scale-out for an LLM-backed endpoint?"
4. "Where would you put rate limits and why?"
