"""
FASTAPI 02: Request & Response Models
=====================================

Using Pydantic for input validation and output schemas.

THIS IS THE MOST IMPORTANT FILE FOR AI ENGINEERS.

Why? Because:
- LLMs return JSON that needs validation
- API requests need validation
- Response schemas document your API

Run: uvicorn 02_request_response:app --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

app = FastAPI(title="Request/Response Demo")


# =============================================================================
# BASIC PYDANTIC MODELS
# =============================================================================

class ItemCreate(BaseModel):
    """
    Request model for creating an item.
    
    Pydantic automatically:
    - Validates types
    - Converts compatible types (str -> int if possible)
    - Returns 422 error with details if validation fails
    """
    name: str
    price: float
    quantity: int = 1  # Optional with default
    description: Optional[str] = None  # Optional, can be None


class ItemResponse(BaseModel):
    """
    Response model.
    
    Separating request/response models is best practice:
    - Request: what client sends
    - Response: what server returns (may include computed fields)
    """
    id: int
    name: str
    price: float
    quantity: int
    description: Optional[str]
    created_at: datetime


# In-memory storage
items_db: dict[int, ItemResponse] = {}
item_counter = 0


@app.post("/items", response_model=ItemResponse)
def create_item(item: ItemCreate):
    """
    Create an item with validated input.
    
    The 'item: ItemCreate' parameter means:
    - FastAPI expects JSON body matching ItemCreate schema
    - Automatic validation
    - 422 error if invalid
    
    The 'response_model=ItemResponse' means:
    - Output is validated against ItemResponse
    - Extra fields are stripped
    - Documentation shows expected response
    """
    global item_counter
    item_counter += 1
    
    new_item = ItemResponse(
        id=item_counter,
        name=item.name,
        price=item.price,
        quantity=item.quantity,
        description=item.description,
        created_at=datetime.now(),
    )
    items_db[item_counter] = new_item
    return new_item


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    """
    Get item by ID.
    """
    if item_id not in items_db:
        return {"error": "Not found"}  # Will fail response validation!
    return items_db[item_id]


# =============================================================================
# FIELD VALIDATION
# =============================================================================

class UserCreate(BaseModel):
    """
    Model with field constraints.
    """
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = Field(..., ge=0, le=150)  # ge=greater or equal, le=less or equal
    
    # Custom validator
    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v.lower()  # Normalize to lowercase


@app.post("/users")
def create_user(user: UserCreate):
    """
    Create user with validated fields.
    
    Try these in /docs:
    - username: "ab" -> Error (too short)
    - email: "invalid" -> Error (pattern mismatch)
    - age: -5 -> Error (must be >= 0)
    - username: "hello world" -> Error (not alphanumeric)
    """
    return {"message": f"Created user {user.username}", "user": user}


# =============================================================================
# AI ENGINEER PATTERN: LLM Response Validation
# =============================================================================

class LLMRequest(BaseModel):
    """Request to LLM endpoint."""
    prompt: str = Field(..., min_length=1, max_length=10000)
    model: str = "gpt-4"
    temperature: float = Field(0.7, ge=0, le=2)
    max_tokens: int = Field(1000, ge=1, le=4000)


class LLMResponse(BaseModel):
    """
    Expected LLM response structure.
    
    THIS IS CRITICAL: When using LLM JSON mode, you MUST validate
    the response matches your expected schema.
    """
    answer: str
    confidence: float = Field(..., ge=0, le=1)
    sources: list[str] = []
    reasoning: Optional[str] = None


@app.post("/generate", response_model=LLMResponse)
def generate(request: LLMRequest):
    """
    Example LLM endpoint with validated I/O.
    
    In production:
    1. Validate input (automatic via Pydantic)
    2. Call LLM API
    3. Parse JSON response
    4. Validate output matches LLMResponse schema
    5. Return validated response
    """
    # Simulated LLM response
    return LLMResponse(
        answer=f"Response to: {request.prompt[:50]}...",
        confidence=0.85,
        sources=["source1.pdf", "source2.pdf"],
        reasoning="Based on retrieved documents...",
    )


# =============================================================================
# NESTED MODELS
# =============================================================================

class Address(BaseModel):
    street: str
    city: str
    country: str = "USA"


class Company(BaseModel):
    name: str
    address: Address  # Nested model
    employees: list[str] = []


@app.post("/companies")
def create_company(company: Company):
    """
    Nested model example.
    
    Request body:
    {
        "name": "Acme Inc",
        "address": {
            "street": "123 Main St",
            "city": "San Francisco"
        },
        "employees": ["Alice", "Bob"]
    }
    """
    return company


# =============================================================================
# LIST OF MODELS
# =============================================================================

class BatchItem(BaseModel):
    name: str
    value: float


class BatchRequest(BaseModel):
    items: list[BatchItem]


class BatchResponse(BaseModel):
    processed: int
    total_value: float
    items: list[BatchItem]


@app.post("/batch", response_model=BatchResponse)
def process_batch(request: BatchRequest):
    """
    Process a batch of items.
    
    Common pattern for bulk operations.
    """
    total = sum(item.value for item in request.items)
    return BatchResponse(
        processed=len(request.items),
        total_value=total,
        items=request.items,
    )


# =============================================================================
# KEY TAKEAWAYS
# =============================================================================
"""
1. Define models: class MyModel(BaseModel)
2. Request body: def func(data: MyModel)
3. Response model: @app.post(..., response_model=MyResponse)
4. Field validation: Field(..., min_length=3, ge=0)
5. Custom validators: @field_validator

FOR AI ENGINEERS:
- Always validate LLM responses with response_model
- Use Field() constraints for input validation
- Nested models for complex structures
- Separate request/response models

NEXT: 03_error_handling.py - Proper error responses
"""
