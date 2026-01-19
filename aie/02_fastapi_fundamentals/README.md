# FastAPI Fundamentals for AI Engineers

A crash course on building APIs with FastAPI - the skills you need for AI Engineer interviews.

---

## Why FastAPI?

FastAPI is the de facto standard for building AI/ML APIs because:

1. **Native async** - Essential for LLM calls that take seconds
2. **Pydantic validation** - Automatic request/response validation
3. **Auto-generated docs** - Interactive API documentation
4. **Type hints** - Modern Python, great developer experience

---

## What AI Engineers Need to Know

| Topic | Why It Matters | File |
|-------|----------------|------|
| Basic routing | Expose models as endpoints | `01_hello_world.py` |
| Pydantic models | Validate I/O (critical for LLM output!) | `02_request_response.py` |
| Error handling | Graceful failures, proper status codes | `03_error_handling.py` |
| Async patterns | Non-blocking LLM calls | `04_async_patterns.py` |
| Interview patterns | Common questions they ask | `05_common_interview.py` |

---

## Quick Start

```bash
# Install dependencies
pip install fastapi uvicorn httpx pydantic

# Run any file
uvicorn 01_hello_world:app --reload

# Open browser
# http://localhost:8000/docs  <- Interactive docs
# http://localhost:8000/health <- Your endpoint
```

---

## The Mental Model

FastAPI is just **decorated functions**:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/path")       # HTTP method + path
def my_function():      # Your logic
    return {"data": x}  # Return dict/Pydantic model -> JSON
```

That's it. Everything else builds on this.

---

## Key Concepts

### 1. Route Decorators

```python
@app.get("/items")      # Read data
@app.post("/items")     # Create data
@app.put("/items/{id}") # Update data
@app.delete("/items/{id}") # Delete data
```

### 2. Path Parameters

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):  # Automatically parsed from URL
    return {"id": user_id}
```

### 3. Query Parameters

```python
@app.get("/search")
def search(q: str, limit: int = 10):  # ?q=hello&limit=5
    return {"query": q, "limit": limit}
```

### 4. Request Body (Pydantic)

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
def create_item(item: Item):  # Auto-validated JSON body
    return item
```

### 5. Response Models

```python
@app.get("/items/{id}", response_model=Item)
def get_item(id: int):
    return {"name": "Widget", "price": 9.99}  # Validated on output
```

---

## Common Interview Questions

1. **"Design an endpoint that calls an LLM and returns structured output"**
   - See: `02_request_response.py`, `04_async_patterns.py`

2. **"How do you handle errors in an API?"**
   - See: `03_error_handling.py`

3. **"How would you handle long-running model inference?"**
   - See: `04_async_patterns.py` (background tasks)

4. **"How do you validate LLM outputs?"**
   - See: `02_request_response.py` (response models)

5. **"How would you add rate limiting?"**
   - See: `05_common_interview.py`

---

## Files in This Folder

| File | What You'll Learn |
|------|-------------------|
| `01_hello_world.py` | Basic app structure, routes, running the server |
| `02_request_response.py` | Pydantic models, request validation, response models |
| `03_error_handling.py` | HTTPException, custom error handlers |
| `04_async_patterns.py` | async/await, background tasks, concurrent calls |
| `05_common_interview.py` | Rate limiting, logging, streaming, auth |

---

## How to Practice

1. **Run each file** and play with the `/docs` interface
2. **Modify** the examples - add fields, change logic
3. **Build variations** - combine patterns
4. **Time yourself** - can you build a basic endpoint in 5 minutes?

---

## Cheat Sheet

```python
# Minimal app
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello"}

# With validation
from pydantic import BaseModel

class Request(BaseModel):
    text: str

@app.post("/process")
def process(req: Request):
    return {"result": req.text.upper()}

# With error handling
from fastapi import HTTPException

@app.get("/items/{id}")
def get_item(id: int):
    if id not in db:
        raise HTTPException(404, "Not found")
    return db[id]

# Async
@app.get("/async")
async def async_endpoint():
    result = await some_async_call()
    return result
```
