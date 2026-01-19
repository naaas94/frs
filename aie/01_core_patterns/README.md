# Core Patterns for AI Engineers

These three patterns appear in almost every AI Engineer interview. Master them until they're automatic.

---

## The Patterns

| Pattern | What It Does | When You'll Use It |
|---------|--------------|-------------------|
| **Ingestion Loop** | Filter and clean a list of records | Processing API responses, cleaning datasets |
| **Schema Validator** | Check if data matches expected structure | Validating LLM JSON output, config files |
| **API Retry** | Call external API with automatic retry | Calling LLMs, external services |

---

## Pattern 1: Ingestion Loop

**The universal data cleaning pattern.**

Every AI system ingests messy data. This pattern handles:
- Filtering out invalid records
- Cleaning/normalizing valid records
- Tracking errors for debugging

```python
def process_records(items: list[dict]) -> tuple[list[dict], list[dict]]:
    valid, errors = [], []
    for i, item in enumerate(items):
        if not is_valid(item):
            errors.append({"index": i, "reason": "validation failed"})
            continue
        valid.append(clean(item))
    return valid, errors
```

**File**: `ingestion_loop.py`

---

## Pattern 2: Schema Validator

**Validate structured data against a schema.**

Critical for AI systems because:
- LLM JSON outputs need validation
- Config files need validation
- API payloads need validation

```python
SCHEMA = {"name": str, "age": int}

def validate(record: dict, schema: dict) -> tuple[bool, list[str]]:
    errors = []
    for field, expected_type in schema.items():
        if field not in record:
            errors.append(f"missing: {field}")
        elif not isinstance(record[field], expected_type):
            errors.append(f"type error: {field}")
    return len(errors) == 0, errors
```

**File**: `schema_validator.py`

---

## Pattern 3: API Retry

**Call external APIs with exponential backoff.**

Essential because:
- LLM APIs have rate limits
- External services fail randomly
- Network issues happen

```python
def retry(fn, max_attempts=3, base_delay=1.0):
    for attempt in range(max_attempts):
        try:
            return fn()
        except Exception:
            if attempt == max_attempts - 1:
                raise
            time.sleep(base_delay * (2 ** attempt))
```

**File**: `api_retry.py`

---

## How to Practice

1. **Read** each file completely
2. **Type** the template from memory (no copy-paste)
3. **Complete** the practice problems at the bottom
4. **Repeat** until you can write each pattern cold in under 3 minutes

---

## Common Interview Variations

| Base Pattern | Variation They Might Ask |
|--------------|-------------------------|
| Ingestion Loop | "Also count records by category" |
| Ingestion Loop | "Handle nested records" |
| Schema Validator | "Support optional fields" |
| Schema Validator | "Validate nested schemas" |
| API Retry | "Add jitter to prevent thundering herd" |
| API Retry | "Only retry on specific exceptions" |

Each file includes variations to practice.
