"""
FASTAPI 01: Hello World
=======================

The absolute basics of FastAPI.

Run this file:
    uvicorn 01_hello_world:app --reload

Then visit:
    http://localhost:8000/         <- Root endpoint
    http://localhost:8000/health   <- Health check
    http://localhost:8000/docs     <- Interactive documentation
"""

from fastapi import FastAPI

# =============================================================================
# CREATE THE APP
# =============================================================================

# This is the central object. All routes are attached to it.
app = FastAPI(
    title="AI Engineer Demo API",
    description="Learning FastAPI fundamentals",
    version="1.0.0",
)


# =============================================================================
# BASIC ROUTES
# =============================================================================

@app.get("/")
def root():
    """
    Root endpoint. Just returns a welcome message.
    
    The function return value is automatically converted to JSON.
    """
    return {"message": "Hello, AI Engineer!", "status": "running"}


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    
    Every production API needs this. Used by:
    - Load balancers to check if server is alive
    - Kubernetes liveness/readiness probes
    - Monitoring systems
    """
    return {"status": "healthy"}


# =============================================================================
# PATH PARAMETERS
# =============================================================================

@app.get("/users/{user_id}")
def get_user(user_id: int):
    """
    Path parameter example.
    
    The {user_id} in the path becomes a function argument.
    Type hint (: int) means FastAPI will:
    - Validate it's an integer
    - Return 422 error if not
    - Convert string "123" to int 123
    """
    return {"user_id": user_id, "name": f"User {user_id}"}


@app.get("/items/{item_id}")
def get_item(item_id: str):
    """
    Path parameters can be any type.
    String is the default if you don't specify.
    """
    return {"item_id": item_id}


# =============================================================================
# QUERY PARAMETERS
# =============================================================================

@app.get("/search")
def search(
    q: str,              # Required query param
    limit: int = 10,     # Optional with default
    offset: int = 0,     # Optional with default
):
    """
    Query parameter example.
    
    URL: /search?q=hello&limit=5
    
    Parameters without path placeholder become query params.
    - Required if no default value
    - Optional if has default value
    """
    return {
        "query": q,
        "limit": limit,
        "offset": offset,
        "results": [f"Result {i} for '{q}'" for i in range(offset, offset + limit)],
    }


@app.get("/filter")
def filter_items(
    category: str | None = None,  # Optional (can be None)
    min_price: float = 0,
    max_price: float = 1000,
):
    """
    Optional query params with None.
    
    Using | None (Python 3.10+) means the param can be omitted.
    """
    return {
        "category": category,
        "price_range": [min_price, max_price],
    }


# =============================================================================
# MULTIPLE HTTP METHODS
# =============================================================================

# In-memory "database" for demo
fake_db = {}


@app.post("/items")
def create_item(name: str, price: float):
    """
    POST = Create new resource.
    
    Note: This uses query params for simplicity.
    Real apps use request body (see 02_request_response.py).
    """
    item_id = len(fake_db) + 1
    fake_db[item_id] = {"id": item_id, "name": name, "price": price}
    return fake_db[item_id]


@app.put("/items/{item_id}")
def update_item(item_id: int, name: str, price: float):
    """
    PUT = Update existing resource.
    """
    if item_id not in fake_db:
        return {"error": "Item not found"}
    fake_db[item_id] = {"id": item_id, "name": name, "price": price}
    return fake_db[item_id]


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """
    DELETE = Remove resource.
    """
    if item_id in fake_db:
        del fake_db[item_id]
        return {"deleted": item_id}
    return {"error": "Item not found"}


# =============================================================================
# KEY TAKEAWAYS
# =============================================================================
"""
1. Create app: app = FastAPI()
2. Define routes: @app.get("/path")
3. Return dict: Automatically becomes JSON
4. Path params: /users/{id} -> def func(id: int)
5. Query params: Parameters not in path -> ?key=value
6. Type hints: Enable validation and conversion

NEXT: 02_request_response.py - Pydantic models for request/response validation
"""


# =============================================================================
# RUN INSTRUCTIONS
# =============================================================================
"""
To run this file:

1. Navigate to this directory
2. Run: uvicorn 01_hello_world:app --reload
3. Open: http://localhost:8000/docs

The --reload flag enables hot reloading during development.

Try these URLs:
- http://localhost:8000/
- http://localhost:8000/health
- http://localhost:8000/users/42
- http://localhost:8000/search?q=test&limit=5
"""
