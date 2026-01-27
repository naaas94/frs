"""
AI ENGINEER DRILLS
==================

Timed practice problems combining core patterns.

Usage:
    python drill_problems.py           # Run self-tests
    pytest drill_problems.py -v        # Run all tests
    pytest drill_problems.py::TestDrill01 -v  # Run specific drill

Instructions:
1. Read the problem docstring
2. Set a timer
3. Implement the solution
4. Run tests to verify
"""

from typing import Any
import time


# =============================================================================
# DRILL 01: Adult Filter (Ingestion Loop)
# Target time: 3 minutes
# =============================================================================

def filter_adults(people: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    DRILL 01: Adult Filter
    
    Filter a list of people to only include adults (age >= 18).
    
    Args:
        people: List of dicts, each may have "name" and "age" keys
    
    Returns:
        (adults, errors) where:
        - adults: List of valid records with age >= 18
        - errors: List of {"index": i, "reason": str} for invalid records
    
    Invalid records:
        - Missing "age" key
        - "age" is not an integer
    
    Example:
        Input: [{"name": "Alice", "age": 25}, {"name": "Bob"}, {"name": "Eve", "age": 16}]
        Output: ([{"name": "Alice", "age": 25}], [{"index": 1, "reason": "missing or invalid age"}])
    
    Note: Bob is invalid (no age), Eve is valid but not an adult (not an error)
    """
    adults = []
    errors = []
    
    for i, person in enumerate(people):
        # Check if age exists and is int
        if not isinstance(person.get("age"), int):
            errors.append({"index": i, "reason": "missing or invalid age"})
            continue
        
        # Filter to adults only
        if person["age"] >= 18:
            adults.append(person)
    
    return adults, errors


# =============================================================================
# DRILL 02: Email Validator (Schema Validator)
# Target time: 3 minutes
# =============================================================================

def validate_user(user: dict) -> tuple[bool, list[str]]:
    """
    DRILL 02: Email Validator
    
    Validate a user record against this schema:
        - "name": str (required)
        - "email": str (required, must contain "@")
        - "age": int (required, must be >= 0)
    
    Args:
        user: Dict to validate
    
    Returns:
        (is_valid, errors) where:
        - is_valid: True if all validations pass
        - errors: List of error messages
    
    Example:
        Input: {"name": "Alice", "email": "alice@test.com", "age": 25}
        Output: (True, [])
        
        Input: {"name": "Bob", "email": "invalid", "age": -5}
        Output: (False, ["email must contain @", "age must be >= 0"])
    """
    errors = []
    
    # Check name
    if "name" not in user:
        errors.append("missing: name")
    elif not isinstance(user["name"], str):
        errors.append("name must be string")
    
    # Check email
    if "email" not in user:
        errors.append("missing: email")
    elif not isinstance(user["email"], str):
        errors.append("email must be string")
    elif "@" not in user["email"]:
        errors.append("email must contain @")
    
    # Check age
    if "age" not in user:
        errors.append("missing: age")
    elif not isinstance(user["age"], int):
        errors.append("age must be integer")
    elif user["age"] < 0:
        errors.append("age must be >= 0")
    
    return len(errors) == 0, errors


# =============================================================================
# DRILL 03: Flaky Function (API Retry)
# Target time: 3 minutes
# =============================================================================

def call_with_retry(
    fn: callable,
    max_attempts: int = 3,
    base_delay: float = 0.1,  # Small delay for testing
) -> Any:
    """
    DRILL 03: Flaky Function Retry
    
    Call a function with retry on exception.
    Uses exponential backoff: delay doubles each attempt.
    
    Args:
        fn: Zero-argument function to call
        max_attempts: Maximum number of tries
        base_delay: Initial delay in seconds
    
    Returns:
        Result of fn() if successful
    
    Raises:
        Last exception if all attempts fail
    
    Example:
        count = 0
        def flaky():
            nonlocal count
            count += 1
            if count < 3:
                raise ValueError("Not yet")
            return "success"
        
        result = call_with_retry(flaky, max_attempts=3)
        # result == "success", count == 3
    """
    for attempt in range(max_attempts):
        try:
            return fn()
        except Exception:
            if attempt == max_attempts - 1:
                raise
            time.sleep(base_delay * (2 ** attempt))
    
    raise RuntimeError("Unreachable")


# =============================================================================
# DRILL 04: Nested Schema Validator
# Target time: 5 minutes
# =============================================================================

def validate_nested(record: dict, schema: dict) -> tuple[bool, list[str]]:
    """
    DRILL 04: Nested Schema Validator
    
    Validate a record against a schema that may have nested structures.
    Schema values can be:
        - A type (str, int, bool, etc.) - check isinstance
        - A dict - recurse into nested structure
    
    Args:
        record: Dict to validate
        schema: Dict mapping field names to types or nested schemas
    
    Returns:
        (is_valid, errors) with dot-notation for nested fields
    
    Example:
        schema = {"name": str, "address": {"city": str, "zip": int}}
        record = {"name": "Alice", "address": {"city": "NYC"}}
        Output: (False, ["address.zip: missing"])
    """
    errors = []
    
    for field, expected in schema.items():
        if field not in record:
            errors.append(f"{field}: missing")
            continue
        
        value = record[field]
        
        if isinstance(expected, dict):
            # Nested schema - recurse
            if not isinstance(value, dict):
                errors.append(f"{field}: expected object")
            else:
                _, nested_errors = validate_nested(value, expected)
                errors.extend(f"{field}.{e}" for e in nested_errors)
        else:
            # Type check
            if not isinstance(value, expected):
                errors.append(f"{field}: wrong type")
    
    return len(errors) == 0, errors


# =============================================================================
# DRILL 05: JSONL Cleaner (Ingestion + Schema)
    # lets do 5 more ok ### 
# Target time: 10 minutes
# =============================================================================

import json

def process_jsonl(lines: list[str]) -> dict[str, Any]:
    """
    DRILL 05: JSONL Cleaner
    
    Process JSONL lines with:
    1. Parse JSON (skip malformed)
    2. Validate schema: {"id": int, "value": float}
    3. Filter: only keep records where value > 0
    4. Aggregate: sum of values, count
    
    Args:
        lines: List of JSON strings (one per line)
    
    Returns:
        {
            "records": [valid filtered records],
            "total_value": sum of values,
            "count": number of valid records,
            "errors": [{"line": 1-indexed line num, "type": "parse"|"validation"|"filter"}]
        }
    
    Example:
        Input: ['{"id": 1, "value": 10.5}', 'invalid', '{"id": 2, "value": -5}']
        Output: {
            "records": [{"id": 1, "value": 10.5}],
            "total_value": 10.5,
            "count": 1,
            "errors": [
                {"line": 2, "type": "parse"},
                {"line": 3, "type": "filter"}  # valid but value <= 0
            ]
        }
    """
    records = []
    errors = []
    total = 0.0
    
    for line_num, line in enumerate(lines, 1):
        # Parse
        try:
            data = json.loads(line.strip())
        except json.JSONDecodeError:
            errors.append({"line": line_num, "type": "parse"})
            continue
        
        # Validate schema
        if not isinstance(data.get("id"), int):
            errors.append({"line": line_num, "type": "validation"})
            continue
        if not isinstance(data.get("value"), (int, float)):
            errors.append({"line": line_num, "type": "validation"})
            continue
        
        # Filter
        if data["value"] <= 0:
            errors.append({"line": line_num, "type": "filter"})
            continue
        
        # Collect
        records.append(data)
        total += data["value"]
    
    return {
        "records": records,
        "total_value": total,
        "count": len(records),
        "errors": errors,
    }


# =============================================================================
# DRILL 06: Resilient API Call (Schema + Retry)
    #    LETS DO 10 MORE OF THIS ####################
# Target time: 10 minutes
# =============================================================================

def fetch_and_validate(
    fetch_fn: callable,
    schema: dict[str, type],
    max_retries: int = 3,
) -> dict[str, Any]:
    """
    DRILL 06: Resilient API Call
    
    1. Call fetch_fn with retry (exponential backoff)
    2. Validate response against schema
    3. Return result or error info
    
    Args:
        fetch_fn: Function that returns a dict (may raise exceptions)
        schema: Expected schema {field: type}
        max_retries: Number of retry attempts
    
    Returns:
        On success: {"success": True, "data": validated_response}
        On fetch failure: {"success": False, "error": "fetch_failed", "message": str}
        On validation failure: {"success": False, "error": "validation_failed", "errors": [...]}
    """
    # Step 1: Fetch with retry
    response = None
    last_error = None
    
    for attempt in range(max_retries):
        try:
            response = fetch_fn()
            break
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                time.sleep(0.1 * (2 ** attempt))
    
    if response is None:
        return {
            "success": False,
            "error": "fetch_failed",
            "message": str(last_error),
        }
    
    # Step 2: Validate
    errors = []
    for field, expected_type in schema.items():
        if field not in response:
            errors.append(f"missing: {field}")
        elif not isinstance(response[field], expected_type):
            errors.append(f"wrong type: {field}")
    
    if errors:
        return {
            "success": False,
            "error": "validation_failed",
            "errors": errors,
        }
    
    return {"success": True, "data": response}


# =============================================================================
# DRILL 07: Batch Processor (Full Pipeline)

          # LETS DO 10 MORE BABYYYY ######################

# Target time: 15 minutes
# =============================================================================

def process_batch(
    items: list[dict],
    required_fields: list[str],
    transform_fn: callable,
    filter_fn: callable,
) -> dict[str, Any]:
    """
    DRILL 07: Batch Processor
    
    Full data pipeline:
    1. Validate: each item has all required_fields
    2. Transform: apply transform_fn to valid items
    3. Filter: keep only items where filter_fn returns True
    
    Args:
        items: List of dicts to process
        required_fields: List of field names that must exist
        transform_fn: Function to transform valid items
        filter_fn: Function to filter transformed items
    
    Returns:
        {
            "results": [final filtered results],
            "stats": {
                "total": total input count,
                "valid": passed validation,
                "transformed": passed transform (no exception),
                "filtered": passed filter,
            },
            "errors": [{"index": i, "stage": "validation"|"transform"|"filter", "reason": str}]
        }
    """
    results = []
    errors = []
    stats = {"total": len(items), "valid": 0, "transformed": 0, "filtered": 0}
    
    for i, item in enumerate(items):
        # Validate
        missing = [f for f in required_fields if f not in item]
        if missing:
            errors.append({
                "index": i,
                "stage": "validation",
                "reason": f"missing fields: {missing}"
            })
            continue
        stats["valid"] += 1
        
        # Transform
        try:
            transformed = transform_fn(item)
        except Exception as e:
            errors.append({
                "index": i,
                "stage": "transform",
                "reason": str(e)
            })
            continue
        stats["transformed"] += 1
        
        # Filter
        if not filter_fn(transformed):
            errors.append({
                "index": i,
                "stage": "filter",
                "reason": "filtered out"
            })
            continue
        stats["filtered"] += 1
        
        results.append(transformed)
    
    return {
        "results": results,
        "stats": stats,
        "errors": errors,
    }


# =============================================================================
# DRILL 08: Config Validator with Defaults

    ### COOL SHIT BRAH LETS DO 10 MORE ######

    # YOU AND ME BABY. ME, YOU, YOU, ME, ME, YOU, YOU, ME, YOU, ME, etc ### 
# Target time: 10 minutes
# =============================================================================

def validate_config(
    config: dict,
    schema: dict[str, dict],
) -> tuple[dict, list[str]]:
    """
    DRILL 08: Config Validator with Defaults
    
    Validate config with optional fields and defaults.
    
    Schema format:
        {
            "field_name": {
                "type": type,  # Required type
                "required": bool,  # Default False
                "default": value,  # Used if field missing and not required
            }
        }
    
    Args:
        config: Config dict to validate
        schema: Schema with type, required, default info
    
    Returns:
        (validated_config, errors) where validated_config has defaults applied
    
    Example:
        schema = {
            "host": {"type": str, "required": True},
            "port": {"type": int, "required": False, "default": 8080},
        }
        config = {"host": "localhost"}
        Output: ({"host": "localhost", "port": 8080}, [])
    """
    errors = []
    result = {}
    
    for field, spec in schema.items():
        field_type = spec["type"]
        required = spec.get("required", False)
        default = spec.get("default")
        
        if field in config:
            # Check type
            if not isinstance(config[field], field_type):
                errors.append(f"{field}: wrong type")
            else:
                result[field] = config[field]
        elif required:
            errors.append(f"{field}: required")
        elif default is not None:
            result[field] = default
    
    return result, errors


# =============================================================================
# TESTS
# =============================================================================

class TestDrill01:
    """Tests for Adult Filter drill."""
    
    def test_basic(self):
        people = [
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 17},
            {"name": "Charlie", "age": 18},
        ]
        adults, errors = filter_adults(people)
        assert len(adults) == 2
        assert len(errors) == 0
    
    def test_invalid_age(self):
        people = [
            {"name": "Alice", "age": "twenty"},
            {"name": "Bob"},
        ]
        adults, errors = filter_adults(people)
        assert len(adults) == 0
        assert len(errors) == 2
    
    def test_empty(self):
        adults, errors = filter_adults([])
        assert adults == []
        assert errors == []


class TestDrill02:
    """Tests for Email Validator drill."""
    
    def test_valid(self):
        user = {"name": "Alice", "email": "alice@test.com", "age": 25}
        is_valid, errors = validate_user(user)
        assert is_valid
        assert errors == []
    
    def test_invalid_email(self):
        user = {"name": "Bob", "email": "invalid", "age": 25}
        is_valid, errors = validate_user(user)
        assert not is_valid
        assert "email must contain @" in errors
    
    def test_missing_fields(self):
        user = {}
        is_valid, errors = validate_user(user)
        assert not is_valid
        assert len(errors) == 3


class TestDrill03:
    """Tests for Retry drill."""
    
    def test_success_first_try(self):
        result = call_with_retry(lambda: "success")
        assert result == "success"
    
    def test_success_after_retry(self):
        count = 0
        def flaky():
            nonlocal count
            count += 1
            if count < 3:
                raise ValueError("fail")
            return "success"
        
        result = call_with_retry(flaky, max_attempts=3, base_delay=0.01)
        assert result == "success"
        assert count == 3
    
    def test_all_fail(self):
        import pytest
        def always_fail():
            raise ValueError("always")
        
        with pytest.raises(ValueError):
            call_with_retry(always_fail, max_attempts=2, base_delay=0.01)


class TestDrill04:
    """Tests for Nested Schema Validator drill."""
    
    def test_flat_valid(self):
        schema = {"name": str, "age": int}
        record = {"name": "Alice", "age": 25}
        is_valid, errors = validate_nested(record, schema)
        assert is_valid
    
    def test_nested_valid(self):
        schema = {"user": {"name": str}, "active": bool}
        record = {"user": {"name": "Alice"}, "active": True}
        is_valid, errors = validate_nested(record, schema)
        assert is_valid
    
    def test_nested_missing(self):
        schema = {"user": {"name": str, "age": int}}
        record = {"user": {"name": "Alice"}}
        is_valid, errors = validate_nested(record, schema)
        assert not is_valid
        assert "user.age: missing" in errors


class TestDrill05:
    """Tests for JSONL Cleaner drill."""
    
    def test_basic(self):
        lines = [
            '{"id": 1, "value": 10.5}',
            '{"id": 2, "value": 20.0}',
        ]
        result = process_jsonl(lines)
        assert result["count"] == 2
        assert result["total_value"] == 30.5
    
    def test_parse_error(self):
        lines = ['invalid json']
        result = process_jsonl(lines)
        assert result["count"] == 0
        assert len(result["errors"]) == 1
        assert result["errors"][0]["type"] == "parse"
    
    def test_filter(self):
        lines = ['{"id": 1, "value": -5}']
        result = process_jsonl(lines)
        assert result["count"] == 0
        assert result["errors"][0]["type"] == "filter"


class TestDrill06:
    """Tests for Resilient API Call drill."""
    
    def test_success(self):
        result = fetch_and_validate(
            lambda: {"id": 1, "name": "test"},
            {"id": int, "name": str}
        )
        assert result["success"]
        assert result["data"]["id"] == 1
    
    def test_fetch_failure(self):
        def fail():
            raise ConnectionError("network error")
        
        result = fetch_and_validate(fail, {}, max_retries=2)
        assert not result["success"]
        assert result["error"] == "fetch_failed"
    
    def test_validation_failure(self):
        result = fetch_and_validate(
            lambda: {"id": "not-an-int"},
            {"id": int}
        )
        assert not result["success"]
        assert result["error"] == "validation_failed"


class TestDrill07:
    """Tests for Batch Processor drill."""
    
    def test_full_pipeline(self):
        items = [
            {"name": "a", "value": 10},
            {"name": "b", "value": 5},
            {"value": 20},  # missing name
        ]
        
        result = process_batch(
            items,
            required_fields=["name", "value"],
            transform_fn=lambda x: {**x, "value": x["value"] * 2},
            filter_fn=lambda x: x["value"] > 10,
        )
        
        assert result["stats"]["total"] == 3
        assert result["stats"]["valid"] == 2
        assert result["stats"]["filtered"] == 1
        assert len(result["results"]) == 1
        assert result["results"][0]["value"] == 20  # 10 * 2


class TestDrill08:
    """Tests for Config Validator drill."""
    
    def test_with_defaults(self):
        schema = {
            "host": {"type": str, "required": True},
            "port": {"type": int, "required": False, "default": 8080},
        }
        config, errors = validate_config({"host": "localhost"}, schema)
        assert config == {"host": "localhost", "port": 8080}
        assert errors == []
    
    def test_missing_required(self):
        schema = {"host": {"type": str, "required": True}}
        config, errors = validate_config({}, schema)
        assert "host: required" in errors


# =============================================================================
# SELF-TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("AI ENGINEER DRILLS - Self Test")
    print("=" * 60)
    
    # Drill 01
    print("\n[Drill 01] Adult Filter")
    people = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 17},
        {"name": "Charlie"},
    ]
    adults, errors = filter_adults(people)
    print(f"  Adults: {len(adults)}, Errors: {len(errors)}")
    assert len(adults) == 1
    assert len(errors) == 1
    print("  ✓ Passed")
    
    # Drill 02
    print("\n[Drill 02] Email Validator")
    valid, errs = validate_user({"name": "Test", "email": "test@x.com", "age": 20})
    assert valid
    valid, errs = validate_user({"name": "Test", "email": "bad", "age": 20})
    assert not valid
    print("  ✓ Passed")
    
    # Drill 03
    print("\n[Drill 03] Retry")
    counter = [0]  # Use list to avoid nonlocal issues
    def flaky():
        counter[0] += 1
        if counter[0] < 2:
            raise ValueError("fail")
        return "ok"
    result = call_with_retry(flaky, max_attempts=3, base_delay=0.01)
    assert result == "ok"
    print("  ✓ Passed")
    
    # Drill 04
    print("\n[Drill 04] Nested Schema")
    valid, errs = validate_nested(
        {"user": {"name": "Alice"}},
        {"user": {"name": str, "age": int}}
    )
    assert not valid
    assert "user.age: missing" in errs
    print("  ✓ Passed")
    
    # Drill 05
    print("\n[Drill 05] JSONL Cleaner")
    result = process_jsonl(['{"id": 1, "value": 10}', 'bad', '{"id": 2, "value": -5}'])
    assert result["count"] == 1
    assert len(result["errors"]) == 2
    print("  ✓ Passed")
    
    # Drill 06
    print("\n[Drill 06] Resilient API")
    result = fetch_and_validate(lambda: {"id": 1}, {"id": int})
    assert result["success"]
    print("  ✓ Passed")
    
    # Drill 07
    print("\n[Drill 07] Batch Processor")
    result = process_batch(
        [{"x": 1}, {"x": 2}],
        ["x"],
        lambda i: {**i, "y": i["x"] * 2},
        lambda i: i["y"] > 2
    )
    assert len(result["results"]) == 1
    print("  ✓ Passed")
    
    # Drill 08
    print("\n[Drill 08] Config Validator")
    config, errs = validate_config(
        {"host": "localhost"},
        {"host": {"type": str, "required": True}, "port": {"type": int, "default": 80}}
    )
    assert config["port"] == 80
    print("  ✓ Passed")
    
    print("\n" + "=" * 60)
    print("All drills passed! Run with pytest for full test suite.")
    print("=" * 60)
