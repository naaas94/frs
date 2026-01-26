# ingestion loop


### core pattenr:



from numpy import isin


def ingest_records(
    records: list[dict],
) -> tuple[list[dict], list[dict]]:

    errors = []
    valid = []



    for i, item in enumerate(records):

       
        if not is_valid(item):
            errors.append({"index":i, "item": item, "error": "invalid"})
        
        cleaned = clean(item)
        valid.append(cleaned)

    return valid, errors


def is_valid(item: dict) -> bool:

    if not isinstance(item, dict):
        return False
    
    if "age" not in item or "name" not in item:
        return False

    if isinstance(record["age"], bool) and not isinstance(record["age"], int):
        return False

    return True




def clean(item:dict) -> dict:

    return {
        "name" : item["name"].strip().lower(),
        "age" : item["age"],
    }

## fm: ok 


### the adult minor example 


def basic_filter(records: list[dict]) -> tuple[list[dict], list[dict]]:

    adults = []
    invalid = []

    for i, item in enumerate(records):

        if not is_valid(item):
            invalid.append({"index":i, "record": item, "error": "invalid"})
            continue

        if item["age"] >= 18:
            cleaned = clean(item)
            adults.append(cleaned)

    return adults, invalid

### fm: yep ok 


### var 1 : with aggs 


def ingest_with_counts(records: list[dict]) -> dict:
    from functools import defaultdict 

    valid = []
    errors = []
    counts = defaultdict(int)


    for i, item in enumerate(records):

        if not is_valid(item):
            errors.append({"index": i, "item": item, "error": "invalid"})
            continue
        
        category = item.get("category", "unknown")
        cleaned = clean(item)
        valid.append(cleaned)
        counts[category]

    return {
        "valid": valid,
        "errors": errors,
        "counts": dict(counts),
    }

### fm: ok 



# var 2 generator for large data


def ingest_large_data(records: list[dict]):

    for i, item in enumerate(records):
        if not is_valid(item):
            yield {"index": i, "record": item, "error": "invalid"}

        else:
            yield {"index": i, "clean_record": clean(item)}

### fm: yep ok 


# var 3 with detailed error types


def ingest_with_detailed_error_types(records: list[dict]) -> tuple[list[dict], list[dict]]:

    valid  = []
    errors = []


    for i, item in enumerate(records):
        error = validate_with_error(item)
        if error:
            errors.append({"index": i, "record": item, "error": error})
            continue
        else:
            cleaned = clean(item)
            valid.append(cleaned)

    return valid, errors

def validate_with_error(item: dict) -> str | None: 

    if not isinstance(item, dict):
        return "item_not_dict"

    if "age" not in item:
        return "missing_age"
    
    if "name" not in item:
        return "missing_name"
    
    if isinstance(item["age"], bool) and not isinstance(item["age"], int):
        return "type_error_age"

    if item["age"] < 0:
        return "negative_age"

    if not isinstance(item["name"], str):
        return "type_error_name"
    return None

## fm: takes 7 mins approx but ok 

## practice problems: 

### 1: basic filter


def basic_filter(records: list[dict]) -> tuple[list[dict], list[dict]]:

    errors = []
    adults = []


    for i, item in enumerate(records):
        if not is_valid(item):
            errors.append({"index":i, "record": item, "error": "invalid"})
            continue

        if item["age"] >= 18:
            cleaned = clean(item)
            adults.append(cleaned)

    return adults, errors


def is_valid(item: dict) -> bool:

    if not isinstance(item, dict):
        return False

    if "age" not in item or "name" not in item:
        return False

    if isinstance(item["age"], bool) and not isinstance(item["age"], int):
        return False

    return True

def clean(item: dict) -> dict:

    return {
        "name": item["name"].strip().lower(),
        "age": item["age"],
    }
### fm: took 4-5 misn V: yeah ok 


# 2: with transformation 


def ingest_with_valid_email(records: list[dict]) -> tuple[list[dict], list[dict]]:

    errors = []
    valid = []

    for i, item in enumerate(records):
        if not is_valid(item):
            errors.append({"index": i, "record": item, "error": "invalid"})
            continue

        cleaned = clena(item)
        valid.append(cleaned)

    return valid, errors


def is_valid(item: dict) -> bool:

    if not isinstance(item, dict):
        return False
    if "email" not in item:
        return False
    if "@" not in item["email"]:
        return False
    return True

def clean(item: dict) -> dict:

    return {
        "email": item["email"].strip().lower(),
    }


# fm: 5 mins approx - V: I think ok 


### 3 with agg


def with_agg(items: list[dict]) -> dict:

    records = []
    total_value = 0 

    for i, item in enumerate(items):

        if is_valid(item):

            records.append(item)
            total_value += item["value"]

    return {
        "records": records,
        "total_value": total_value,
        "count": len(records)
    }

    


### fm: 5-7 mins - V: some bugs 


# reps: 

# 1: 

def with_agg(items: list[dict]) -> dict:


    valid = []
    total_value = 0

    for i, item in enumerate(items):
        if is_valid(item):
       
            valid.append(item)
            total_value += item["value"]

    return {
        "records": valid,
        "total_value": total_value,
        "count": len(valid)
    }

def is_valid(item: dict) -> bool:

    if not isinstance(item, dict):
        return False

    if "status" not in item or "value" not in item:
        return False

    if item["status"] != "active":
        return False
    return True



# 2: 


def with_aggs(items: list[dict]) -> dict:

    records = []
    total_value = 0

    for item in items: 
        if is_valid(item):
            records.append(item)

            total_value += item["value"]

    return {
        "records" : records,
        "total_value": total_value,
        "count": len(records),
    }


def is_valid(item: dict) -> bool:

    if not isinstance(item, dict):
        return False

    if "status" not in item or "value" not in item:
        return False

    if item["status"] != "active":
        return False

    if isinstance(item["value"], bool) and not isinstance(item["value"], int):
        return False

    return True


# --- fm: 5-10 mins - V: critical but at comparing status instead of item["status"]


# 3: 


def with_aggs(items: list[dict]) -> dict:

    valid = []
    total_value = 0


    for item in items:
        if is_valid(item):
            valid.append(item)

            total_value += item["value"]

        
    return {
        "records": valid,
        "total_value": total_value,
        "count": len(valid),
    }


def is_valid(item: dict) -> bool:


    if not isinstance(item, dict):
        return False

    if "status" not in item or "value" not in item:
        return False

    if item["status"] != "active":
        return False

    if not isinstance(item["value"], (int, float)):
        return False

    
    return True


# 4: 


# 8:12


def with_aggs(items: list[dict]) -> dict:


    valid = []
    total_value = 0


    for item in items:
        if is_valid(item):
            valid.append(item)

            total_value += item["value"]


    return {
        "valid": valid,
        "total_value": total_value,
        "count": len(valid),
    }


def is_valid(item: dict) -> bool:


    if not isinstance(item, dict):
        return False

    if "status" not in item or "value" not in item:
        return False

    if item["status"] != "active": 
        return False
    
    if not isinstance(item["value"], (int, float)):
        return False

    return True

### fm: 3 mins - V: fine 


# 5 


def with_aggs(items: list[dict]) -> dict:


    records = []
    total_value = 0

    for item in items:
        if is_valid(item):
            records.append(item)

            total_value += item["value"]

    return {
        "records" : records,
        "total_value": total_value,
        "count": len(records),
    }


def is_valid(item: dict) -> bool:


    if not isinstance(item, dict):
        return False

    if "status" not in item or "value" not in item:
        return False

    if item["status"] != "active": 
        return False

    if not isinstance(item["value"], (int, float)):
        return False
    
    return True

# fm: 3-5 mins V: 


# 4 nested records


def nested_records(items: list[dict]) -> tuple[list[dict], list[dict]]:

    valid = []
    invalid = []

    for i, item in enumerate(items):

        u = item.get("user")

        if isinstance(u, dict):
            if is_valid(u):
                valid.append(item)

            else:
                invalid.append({"index": i, "item": item, "error": "invalid"})
                continue

        else:
            invalid.append({"index": i, "item": item, "error": f"type error: {u} (expected an object)"})
            continue

    return valid, invalid 


def is_valid(item: dict) -> bool:

    if not isinstance(item, dict):
        return False

    if "name" not in item or "age" not in item:
        return False

    if not isinstance(item["age"], (int, float)):
        return False


    return True

### fm: some reps would be nice - logic was fine just the specs were off from the original example 



# 1: 


def nested_records_ingestion(items: list[dict]) -> tuple[list[dict], list[dict]]:

    valid = []
    errors = []


    for i, item in enumerate(items):
        u = item.get("user")
        if not isinstance(u, dict):
            errors.append({"index": i, "item": item, "error": f"type error: {u}"})
            continue
        
        name = u.get("name")
        age = u.get("age")


        if not isinstance(name, str):
            errors.append({"index": i, "item": item, "error": "invalid name"})
            continue

        if not isinstance(age, (int, float)):
            errors.append({"index": i, "item": item, "error": "invalid age"})
            continue

        valid.append({"name": name, "age": age})

    return valid, errors

## fm: we could use u user instead of full item for the errors - other than that ok 

# 2: 


def nested_records_ingestion(items: list[dict]) -> tuple[list[dict], list[dict]]:

    errors = []
    valid = []

    for i, item in enumerate(items):

        u = item.get("user")
        if not isinstance(u, dict):
            errors.append({"index":i, "user": u, "error": "user not a dict"})
            continue

        
        name = u.get("name")
        age = u.get("age")

        if not isinstance(name, str):
            errors.append({"index": i, "user": u, "error": "invalid name"})
            continue

        if isinstance(age, bool) and not isinstance(age, int):
            errors.append({"index": i, "user": u, "error": "invalid age"})
            continue

        valid.append({"name":name,"age":age})

    return valid, errors

# fm: bug: getting the values from the item and not the user, the nested dict - seems the age type verification is not better


# 3:


def nested_records_ingestion(items: list[dict]) -> tuple[list[dict], list[dict]]:

    errors = []
    valid = []

    for i, item in enumerate(items):

        u = item.get("user")
        if not isinstance(u, dict):
            errors.append({"index": i, "user": u, "error": "user not a dict"})
            continue

        name = u.get("name")
        age = u.get("age")

        if not isinstance(name, str):
            errors.append({"index": i, "user": u, "error": "invalid name"})
            continue

        if not isinstance(age, (int, float)):
            errors.append({"index": i, "user": u, "error": "invalid age"})
            continue

        valid.append({"name": name, "age": age})

    return valid, errors

# fm: 4-5 mins - V: solid 




