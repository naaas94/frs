# core pattern


from math import e
from operator import itemgetter
from typing import Callable
from unittest import expectedFailure


SCHEMA = {
    "name": str,
    "age": int,
    "email": str,
}

def validate_record(
    item: dict,
    schema: dict,
) -> tuple[bool, list[str]]:


    errors = []

    for field, expected_type in schema.items():
        if field not in item:
            errors.append(f"Missing: {field}")
            continue
        if not isinstance(item[field], expected_type):
            errors.append(f"Type_error: {field}")

    return len(errors) == 0, errors


# fm: 5-7 misn - V: ok - I always forget that I can get the actual type name with dunder method but ok


# Var 1 w optional field:



def validate_with_optional(
    item: dict,
    required: dict[str, type],
    optional: dict[str, type] | None = None,
) -> tuple[bool, list]:


    errors = []
    optional = optional or {}

    for field, expected_type in required.items():
        if field not in item:
            errors.append(f"Missing: {field}")
            continue

        if not isinstance(item[field], expected_type):
            errors.append(f"Type_error (required): {field}")

    for field, expected_type in optional.items():
        if field in item and not isinstance(item[field], expected_type):
            errors.append(f"Type_error (optional): {field}")
    return len(errors) == 0, errors

# --- fm: 5-7 mins - V: good but have to remember to optional = optional or {}


#  var 2: nested schema validation


def nested_validation(
    item: dict,
    schema: dict,
) -> tuple[bool, list[str]]:


    errors = []
    for field, expected_type in schema.items():
        if field not in item:
            errors.append(f"Missing: {field}")
            continue

        value = item[field]
        if isinstance(expected_type, dict):
            if not isinstance(value, dict):
                errors.append(f"Type error: {field} (not object)")
          
            else:
                is_valid, nested_errors = nested_validation(value, expected_type)
                errors.extend(f"{field}.{e}" for e in nested_errors)
                continue
        
        else:
            if not isinstance(value, expected_type):
                errors.append(f"type error: {field}")
    
    return len(errors) == 0, errors

### --- fm: 8 mins approx - V: fine 


# var 3: with custom validators 



def validate_with_custom(
    item: dict,
    schema: dict,
    validators: dict[str, Callable],
) -> tuple[bool, list[str]]:


    errors = []
    validators = validators or {}

    for field, expected_type in schema.items():
        if field not in item:
            errors.append(f"Missing: {field}")
            continue

        value = item[field]
        if not isinstance(value, expected_type):
            errors.append(f"type error: {field}")
            continue

        if field in validators:
            if not validators[field](value):
                errors.append(f"validation error: {field}")
                continue

    return len(errors) == 0, errors

# fm: 7-8 mins - V: Callable and also | None = None for the validators - if FIELD in validators - The rest fine 


# var 4 batch validation


def batch_validation(
    items: list[dict],
    schema: dict,
) -> tuple[list[dict], list[dict]]:


    errors = []
    valid = []

    for i, item in enumerate(items):
        is_valid, batch_errors = validate_record(item, schema)
        if is_valid:
            valid.append(item)
        else:
            errors.append({"index": i, "item": item, "error": batch_errors})
            continue

    return valid, errors

# fm- 4 mins - V:  it was fine- I overcomplicated and got mixed up so I'll do some 3 reps

# 1 

def validate_batch(
    items: list[dict],
    schema: dict,
) -> tuple[list[dict], list[dict]]:

    valid = []
    invalid = []

    for i, item in enumerate(items):
        is_valid, errors = validate_record(item, schema)
        if is_valid:
            valid.append(item)

        else:
            invalid.append({"index":i, "item": item, "errors": errors})

    return valid, invalid 


# 2 

def validate_batch(
    items: list[dict],
    schema: dict,
) -> tuple[list[dict], list[dict]]:

    valid = []
    invalid = []

    for i, item in enumerate(items):
        is_valid, errors = validate_record(item, schema)
        if is_valid:
            valid.append(item)

        else:
            invalid.append({"index": i, "item": item, "errors": errors})
            continue

    return valid, invalid

# fm: 3 mins - V: yep fine 


# 3 


def validate_batch(
    items: list[dict],
    schema: dict,
) -> tuple[list[dict], list[dict]]:

    valid = []
    invalid = []

    for i, item in enumerate(items):
        is_valid, errors = validate_record(item, schema)
        if is_valid:
            valid.append(item)

        else: 
            invalid.append({"index": i, "item": item, "errors": errors})
            continue

    return valid, invalid

#--- fm: 3-4 mins - V: i think ok 


# var 

