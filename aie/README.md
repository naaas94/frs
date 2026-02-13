# AI Engineer Interview Prep Track

A focused, practical preparation track for **API- and product-focused AI Engineer** roles: calling OpenAI/Anthropic (or similar), building RAG/agents, and owning APIs and reliability.

---

## Start Here

**[ROADMAP.md](ROADMAP.md)** — Your step-by-step path: Phase 1 (foundations) → Phase 2 (drills + mocks) → Phase 3 (sprint hub). Use it as the sequence; use **00_sprint_hub/** for daily focus and the gates checklist.

---

## What This Track Covers

Practical coding patterns that show up in AIE interviews (not LeetCode-style algorithms):

| Module | Focus | Time to Master |
|--------|-------|----------------|
| **01_core_patterns/** | Ingestion, schema validation, retry with backoff | 2-3 days |
| **02_fastapi_fundamentals/** | Building AI APIs (routing, Pydantic, async, guardrails) | 2-3 days |
| **03_drills/** | Timed practice combining patterns; pytest-backed | Ongoing |
| **00_sprint_hub/** | Gates checklist, AIE mock prompts, agents lab, devops notes | Ongoing |

---

## The Interview Landscape

### What AI Engineers Actually Get Asked

Based on common interview patterns for AI Engineer / Forward Deployed Engineer roles:

1. **Data Processing**: "Parse this JSONL, filter invalid records, aggregate by category"
2. **API Design**: "Design an endpoint that takes a prompt and returns LLM response"
3. **Error Handling**: "How do you handle when the LLM API fails?"
4. **Validation**: "How do you ensure LLM output matches expected schema?"
5. **Async**: "How would you call multiple LLMs in parallel?"

### Why These Patterns Matter

Unlike traditional SWE roles that focus on algorithms, AI Engineer interviews test:

- **Can you wrangle messy data?** → Ingestion Loop
- **Can you validate structured outputs?** → Schema Validator (critical for LLM JSON mode)
- **Can you handle flaky external APIs?** → API Retry (LLMs fail often)
- **Can you build production APIs?** → FastAPI fundamentals

---

## How to Use This Track

Follow **[ROADMAP.md](ROADMAP.md)** for the full sequence (Phase 1 → 2 → 3). In short:

- **Phase 1:** Core patterns + FastAPI (run every file, then cold reps).
- **Phase 2:** Drills 05–10 + core and AIE mocks + postmortems.
- **Phase 3:** Sprint hub daily — gates, mock prompts, agents lab, devops review.

### Cold Rep Method (per pattern)

Until you can write each pattern **cold** in under 3 minutes:

```
Rep 1: Read and understand (5 min)
Rep 2: Type while looking at reference (3 min)
Rep 3: Type from memory, check after (5 min)
Rep 4: Type from memory, timed (3 min target)
Rep 5+: Daily cold rep until automatic
```

---

## Quick Reference: The 3 Core Patterns

### 1. Ingestion Loop
```python
def process(items):
    valid, errors = [], []
    for i, item in enumerate(items):
        if not is_valid(item):
            errors.append({"index": i, "error": "..."})
            continue
        valid.append(clean(item))
    return valid, errors
```

### 2. Schema Validator
```python
def validate(record, schema):
    errors = []
    for field, expected_type in schema.items():
        if field not in record:
            errors.append(f"missing: {field}")
        elif not isinstance(record[field], expected_type):
            errors.append(f"type error: {field}")
    return len(errors) == 0, errors
```

### 3. API Retry
```python
def retry(fn, max_attempts=3, delay=1.0):
    for attempt in range(max_attempts):
        try:
            return fn()
        except Exception:
            if attempt == max_attempts - 1:
                raise
            time.sleep(delay * (2 ** attempt))
```

---

## Prerequisites

- Python 3.10+
- Basic familiarity with:
  - `dict`, `list`, type hints
  - `try/except`
  - `json` module

For FastAPI section:
```bash
pip install fastapi uvicorn httpx pydantic
```

---

## Folder Structure

```
aie/
├── README.md                      # You are here
├── ROADMAP.md                     # Step-by-step prep path (start here)
├── 00_sprint_hub/
│   ├── README.md                  # Sprint map + daily guide
│   ├── GATES.md                   # AIE readiness gates checklist
│   ├── mock_prompts/              # AIE mock interview prompts
│   ├── agents_tools/              # ReAct + tool use lab
│   └── devops_cloud.md            # DevOps/cloud interview prep
├── 01_core_patterns/
│   ├── README.md                  # Pattern explanations
│   ├── ingestion_loop.py          # Filter/clean pattern
│   ├── schema_validator.py        # Dict-based validation
│   └── api_retry.py               # Retry with backoff
├── 02_fastapi_fundamentals/
│   ├── README.md                  # FastAPI crash course
│   ├── 01_hello_world.py          # Basic routing
│   ├── 02_request_response.py     # Pydantic models
│   ├── 03_error_handling.py       # HTTPException
│   ├── 04_async_patterns.py       # async/await
│   └── 05_common_interview.py     # Interview patterns
└── 03_drills/
    ├── README.md                  # Practice guide
    └── drill_problems.py          # Timed drills
```
