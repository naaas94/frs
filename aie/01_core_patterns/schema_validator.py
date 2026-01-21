"""
SCHEMA VALIDATOR PATTERN
========================

Validate data against a dictionary-defined schema.

Pattern: define schema → check fields → check types → return (valid, errors)

When to use:
- Validating LLM JSON outputs (critical for structured generation)
- Validating API request/response payloads
- Validating configuration files
- Any "does this match expected structure?" task

Time target: Write from memory in < 3 minutes
"""

from typing import Any


# =============================================================================
# THE CORE PATTERN
# =============================================================================

# Schema: field_name -> expected_type
SCHEMA = {
    "name": str,
    "age": int,
    "email": str,
}


def validate_schema(record: dict, schema: dict) -> tuple[bool, list[str]]:
    """
    Validate a record against a schema.
    
    Args:
        record: The data to validate
        schema: Dict mapping field names to expected types
    
    Returns:
        (is_valid, list_of_errors)
    
    INVARIANT: is_valid == (len(errors) == 0)
    """
    errors = []
    
    for field, expected_type in schema.items():
        # Check field exists
        if field not in record:
            errors.append(f"missing: {field}")
            continue
        
        # Check type
        if not isinstance(record[field], expected_type):
            actual_type = type(record[field]).__name__
            errors.append(f"type error: {field} (expected {expected_type.__name__}, got {actual_type})")
    
    return len(errors) == 0, errors


# =============================================================================
# EXAMPLE: LLM Output Validation
# =============================================================================

LLM_OUTPUT_SCHEMA = {
    "answer": str,
    "confidence": float,
    "sources": list,
}


def validate_llm_response(response: dict) -> tuple[bool, list[str]]:
    """
    Validate that LLM JSON output matches expected schema.
    
    This is critical when using LLMs with JSON mode / structured output.
    You MUST validate before using the response.
    """
    return validate_schema(response, LLM_OUTPUT_SCHEMA)


# =============================================================================
# VARIATION 1: Optional Fields
# =============================================================================

def validate_with_optional(
    record: dict, 
    required: dict[str, type],
    optional: dict[str, type] | None = None
) -> tuple[bool, list[str]]:
    """
    Validate with required and optional fields.
    Optional fields are only type-checked if present.
    """
    errors = []
    optional = optional or {}
    
    # Check required fields
    for field, expected_type in required.items():
        if field not in record:
            errors.append(f"missing required: {field}")
        elif not isinstance(record[field], expected_type):
            errors.append(f"type error: {field}")
    
    # Check optional fields (only if present)
    for field, expected_type in optional.items():
        if field in record and not isinstance(record[field], expected_type):
            errors.append(f"type error (optional): {field}")
    
    return len(errors) == 0, errors


# =============================================================================
# VARIATION 2: Nested Schema Validation
# =============================================================================

def validate_nested(record: dict, schema: dict) -> tuple[bool, list[str]]:
    """
    Validate nested structures.
    Schema values can be types OR nested dicts.
    
    Example schema:
    {
        "user": {
            "name": str,
            "age": int,
        },
        "active": bool,
    }
    """
    errors = []
    
    for field, expected in schema.items():
        if field not in record:
            errors.append(f"missing: {field}")
            continue
        
        value = record[field]
        
        # If expected is a dict, recurse
        if isinstance(expected, dict):
            if not isinstance(value, dict):
                errors.append(f"type error: {field} (expected object)")
            else:
                is_valid, nested_errors = validate_nested(value, expected)
                errors.extend(f"{field}.{e}" for e in nested_errors)
        else:
            # expected is a type
            if not isinstance(value, expected):
                errors.append(f"type error: {field}")
    
    return len(errors) == 0, errors


# =============================================================================
# VARIATION 3: With Custom Validators
# =============================================================================

def validate_with_custom(
    record: dict, 
    schema: dict[str, type],
    validators: dict[str, callable] | None = None
) -> tuple[bool, list[str]]:
    """
    Add custom validation functions for specific fields.
    
    Example validators:
    {
        "email": lambda x: "@" in x,
        "age": lambda x: 0 <= x <= 150,
    }
    """
    errors = []
    validators = validators or {}
    
    for field, expected_type in schema.items():
        if field not in record:
            errors.append(f"missing: {field}")
            continue
        
        value = record[field]
        
        # Type check
        if not isinstance(value, expected_type):
            errors.append(f"type error: {field}")
            continue
        
        # Custom validation
        if field in validators:
            if not validators[field](value):
                errors.append(f"validation failed: {field}")
    
    return len(errors) == 0, errors


# =============================================================================
# VARIATION 4: Batch Validation
# =============================================================================

def validate_batch(
    records: list[dict], 
    schema: dict
) -> tuple[list[dict], list[dict]]:
    """
    Validate multiple records, return valid and invalid separately.
    Combines Schema Validator with Ingestion Loop pattern.
    """
    valid = []
    invalid = []
    
    for i, record in enumerate(records):
        is_valid, errors = validate_schema(record, schema)
        if is_valid:
            valid.append(record)
        else:
            invalid.append({"index": i, "record": record, "errors": errors})
    
    return valid, invalid


# =============================================================================
# PRACTICE PROBLEMS
# =============================================================================
"""
Practice these until you can solve each in under 5 minutes.

PROBLEM 1: Basic Schema
-----------------------
Schema: {"name": str, "age": int, "active": bool}
Input: {"name": "Alice", "age": "25", "active": True}
Task: Validate and return errors
Expected: (False, ["type error: age (expected int, got str)"])

"""

def validate_input(record:dict, schema:dict) -> tuple[bool, list]:

    errors = []

    if isinstance(record, dict):

        for field, expected_type in schema.items():
                        
                if field not in record:
                    errors.append(f"missing: {field}")
                    

                if not isinstance(record[field], expected_type):
                    errors.append(f"type error: {field} (expected {expected_type.__name__}, got {type(record[field]).__name__})")
                    
    else:
        errors.append(f"record not a dict {record}")

                    
    return len(errors) == 0, errors






"""

PROBLEM 2: With Optional Fields
-------------------------------
Required: {"id": int, "name": str}
Optional: {"email": str, "phone": str}
Input: {"id": 1, "name": "Alice", "phone": 12345}
Task: Validate - id and name ok, phone has wrong type
Expected: (False, ["type error (optional): phone"])

"""

def validate_with_optional_fields(
    record: dict, 
    required: dict[str, type],
    optional: dict[str, type] | None = None,
    ) -> tuple[bool, list]:

    errors = []

    for field, expected_type in required.items():
        if field not in record:
            errors.append(f"missing {field}")
            continue

        if not isinstance(record[field], expected_type):
            errors.append(f"type error: {field}")
            continue


    if optional:
        for field, expected_type in optional.items():
            if field in record:
                if not isinstance(record[field], expected_type):
                    errors.append(f"type error (optional): {field}")

    return len(errors) == 0, errors

        
    






"""

PROBLEM 3: Nested Validation
----------------------------
Schema: {
    "user": {"name": str, "age": int},
    "metadata": {"created": str}
}
Input: {"user": {"name": "Alice"}, "metadata": {"created": "2024-01-01"}}
Task: Validate nested structure
Expected: (False, ["user.missing: age"])
"""

def nested_validation(record: dict, schema:dict) -> tuple[bool, list]:

    errors = []

    for field, expected_type in schema.items():
        if field not in record:
            errors.append(f"missing: {field}")
            continue

        value = record[field]

        if isinstance(expected_type, dict):
            if not isinstance(value, dict):
                errors.append(f"type error: {field}")

            else:
                is_valid, nested_errors = nested_validation(value, expected_type)
                errors.extend(f"{field}.{e}" for e in nested_errors)

        else: 

            if not isinstance(value, expected_type):
                errors.append(f"type error: {field}")

    return len(errors) == 0, errors



### this took a while a some lookups - also self recursion and not just call a diff funct













"""


PROBLEM 4: Custom Validators
----------------------------
Schema: {"email": str, "age": int}
Validators: {"email": lambda x: "@" in x, "age": lambda x: x >= 0}
Input: {"email": "invalid-email", "age": -5}
Task: Both custom validations should fail
Expected: (False, ["validation failed: email", "validation failed: age"])
"""















""" 



PROBLEM 5: Batch Validation
---------------------------
Schema: {"id": int, "value": float}
Input: [
    {"id": 1, "value": 10.5},
    {"id": "two", "value": 20.0},
    {"id": 3, "value": "thirty"},
]
Task: Return valid records and errors
Expected: valid=[first], invalid=[second and third with error details]
"""


# =============================================================================
# SELF-TEST
# =============================================================================

if __name__ == "__main__":
    # Test basic validation
    test_schema = {"name": str, "age": int, "active": bool}
    
    valid_record = {"name": "Alice", "age": 25, "active": True}
    invalid_record = {"name": "Bob", "age": "thirty", "active": True}
    missing_field = {"name": "Charlie", "age": 30}
    
    print("Test 1: Valid record")
    is_valid, errors = validate_schema(valid_record, test_schema)
    print(f"  Valid: {is_valid}, Errors: {errors}")
    assert is_valid and len(errors) == 0
    
    print("\nTest 2: Invalid type")
    is_valid, errors = validate_schema(invalid_record, test_schema)
    print(f"  Valid: {is_valid}, Errors: {errors}")
    assert not is_valid and "age" in errors[0]
    
    print("\nTest 3: Missing field")
    is_valid, errors = validate_schema(missing_field, test_schema)
    print(f"  Valid: {is_valid}, Errors: {errors}")
    assert not is_valid and "active" in errors[0]
    
    print("\nTest 4: Nested validation")
    nested_schema = {"user": {"name": str, "age": int}}
    nested_record = {"user": {"name": "Alice"}}  # missing age
    is_valid, errors = validate_nested(nested_record, nested_schema)
    print(f"  Valid: {is_valid}, Errors: {errors}")
    assert not is_valid and "user.missing: age" in errors
    
    print("\n✓ All tests passed!")
