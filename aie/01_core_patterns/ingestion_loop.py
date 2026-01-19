"""
INGESTION LOOP PATTERN
======================

The universal data cleaning pattern for AI systems.

Pattern: iterate → validate → transform → collect

When to use:
- Processing API responses (especially from LLMs)
- Cleaning datasets before training/inference
- Parsing JSONL/CSV files
- Any "filter and transform" task

Time target: Write from memory in < 3 minutes
"""

from typing import Any


# =============================================================================
# THE CORE PATTERN
# =============================================================================

def process_records(items: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    Process a list of records, separating valid from invalid.
    
    Returns:
        (valid_records, errors)
    
    INVARIANT: len(valid) + len(errors) == len(items)
    Every input is either in valid or has an error logged.
    """
    valid = []
    errors = []
    
    for i, item in enumerate(items):
        # VALIDATE
        if not is_valid(item):
            errors.append({"index": i, "reason": "validation failed", "item": item})
            continue
        
        # TRANSFORM
        cleaned = clean(item)
        valid.append(cleaned)
    
    return valid, errors


def is_valid(item: dict) -> bool:
    """Check if record meets requirements. Customize per use case."""
    # Example: require 'name' and 'age' fields
    if not isinstance(item, dict):
        return False
    if "name" not in item or "age" not in item:
        return False
    if not isinstance(item.get("age"), int):
        return False
    return True


def clean(item: dict) -> dict:
    """Normalize/transform a valid record. Customize per use case."""
    return {
        "name": item["name"].strip().lower(),
        "age": item["age"],
    }


# =============================================================================
# EXAMPLE: The "Adult/Minor" Drill
# =============================================================================

def filter_adults(people: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    Classic interview drill: filter to adults only (age >= 18).
    Return (adults, errors) where errors includes invalid records.
    
    This is the pattern Gemini calls "The Ingestion Loop".
    """
    adults = []
    errors = []
    
    for i, person in enumerate(people):
        # Validate: must have 'age' as int
        if not isinstance(person.get("age"), int):
            errors.append({"index": i, "reason": "missing or invalid age"})
            continue
        
        # Filter: only adults
        if person["age"] >= 18:
            adults.append(person)
    
    return adults, errors


# =============================================================================
# VARIATION 1: With Aggregation
# =============================================================================

def process_with_counts(items: list[dict]) -> dict:
    """
    Process records AND count by category.
    Common interview extension: "also aggregate by X".
    """
    from collections import defaultdict
    
    valid = []
    errors = []
    counts = defaultdict(int)
    
    for i, item in enumerate(items):
        if not is_valid(item):
            errors.append({"index": i, "reason": "invalid"})
            continue
        
        cleaned = clean(item)
        valid.append(cleaned)
        
        # Aggregate by some field
        category = item.get("category", "unknown")
        counts[category] += 1
    
    return {
        "valid": valid,
        "errors": errors,
        "counts": dict(counts),
    }


# =============================================================================
# VARIATION 2: Generator for Large Data
# =============================================================================

def process_stream(items):
    """
    Generator version for memory efficiency.
    Use when data is too large to hold in memory.
    """
    for i, item in enumerate(items):
        if not is_valid(item):
            yield {"type": "error", "index": i, "item": item}
        else:
            yield {"type": "valid", "data": clean(item)}


# =============================================================================
# VARIATION 3: With Detailed Error Types
# =============================================================================

def process_with_error_types(items: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    Categorize errors for better debugging.
    Interviewers love asking "how would you debug this?"
    """
    valid = []
    errors = []
    
    for i, item in enumerate(items):
        error = validate_with_reason(item)
        if error:
            errors.append({"index": i, "error_type": error, "item": item})
            continue
        valid.append(clean(item))
    
    return valid, errors


def validate_with_reason(item: dict) -> str | None:
    """Return error type or None if valid."""
    if not isinstance(item, dict):
        return "not_a_dict"
    if "name" not in item:
        return "missing_name"
    if "age" not in item:
        return "missing_age"
    if not isinstance(item["age"], int):
        return "invalid_age_type"
    if item["age"] < 0:
        return "negative_age"
    return None


# =============================================================================
# PRACTICE PROBLEMS
# =============================================================================
"""
Practice these until you can solve each in under 5 minutes.

PROBLEM 1: Basic Filter
------------------------
Input: [{"name": "Alice", "age": 25}, {"name": "Bob"}, {"age": 30}, {"name": "Charlie", "age": 15}]
Task: Return only records with both name AND age, where age >= 18
Expected: ([{"name": "Alice", "age": 25}], [errors for invalid records])

PROBLEM 2: With Transformation
------------------------------
Input: [{"email": "ALICE@TEST.COM"}, {"email": "bob"}, {"email": "charlie@example.org"}]
Task: Filter to valid emails (contain "@"), normalize to lowercase
Expected: ([{"email": "alice@test.com"}, {"email": "charlie@example.org"}], [error for "bob"])

PROBLEM 3: With Aggregation
---------------------------
Input: [{"status": "active", "value": 10}, {"status": "inactive", "value": 5}, {"status": "active", "value": 20}]
Task: Filter to "active" only, return sum of values and count
Expected: {"records": [...], "total_value": 30, "count": 2}

PROBLEM 4: Nested Records
-------------------------
Input: [{"user": {"name": "Alice", "age": 25}}, {"user": {"name": "Bob"}}, {"user": null}]
Task: Extract user objects, filter to valid ones with age
Expected: ([{"name": "Alice", "age": 25}], [errors for others])
"""


# =============================================================================
# SELF-TEST
# =============================================================================

if __name__ == "__main__":
    # Test the adult filter
    test_data = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 17},
        {"name": "Charlie"},  # missing age
        {"name": "Diana", "age": "thirty"},  # wrong type
        {"name": "Eve", "age": 21},
    ]
    
    adults, errors = filter_adults(test_data)
    
    print("Adults:", adults)
    print("Errors:", errors)
    print()
    print(f"✓ Found {len(adults)} adults")
    print(f"✓ Logged {len(errors)} errors")
    
    # Verify invariant
    assert len(adults) + len(errors) + 1 == len(test_data)  # +1 for Bob (valid but minor)
    print("✓ All tests passed!")
