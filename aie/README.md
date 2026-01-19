# AI Engineer Interview Prep Track

A focused, practical preparation track for AI Engineer, Forward Deployed Engineer, and AI Solutions Architect roles.

---

## What This Track Covers

This track focuses on the **practical coding patterns** that appear in AI Engineer interviews - not LeetCode-style algorithms, but the real-world patterns you'll use daily:

| Module | Focus | Time to Master |
|--------|-------|----------------|
| **01_core_patterns/** | The 3 essential patterns (ingestion, validation, retry) | 2-3 days |
| **02_fastapi_fundamentals/** | Building AI APIs from scratch | 2-3 days |
| **03_drills/** | Timed practice combining everything | Ongoing |

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

### Week 1: Learn the Patterns (5-6 hours total)

1. **Day 1-2**: Work through `01_core_patterns/`
   - Read each file top to bottom
   - Type out each template from memory (don't copy-paste)
   - Complete the practice problems at the bottom

2. **Day 3-4**: Work through `02_fastapi_fundamentals/`
   - Run each example locally (`uvicorn filename:app --reload`)
   - Modify and experiment
   - Build small variations

3. **Day 5+**: Daily drills from `03_drills/`
   - Time yourself
   - No looking at references
   - Track your times

### The "Cold Rep" Method

For each pattern, practice until you can write it **cold** (no references) in under 3 minutes:

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
