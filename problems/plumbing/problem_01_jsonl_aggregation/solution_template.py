"""JSONL Log Aggregation - Solution Template"""

import json
from typing import List, Dict, Any
from collections import defaultdict

from templates.patterns.plumbing import validate_record


def aggregate_logs(logs: List[str]) -> Dict[str, Any]:
    """
    Aggregate API logs by endpoint with error handling.
    
    Args:
        logs: List of JSONL strings (one JSON object per line)
        
    Returns:
        Dict with "metrics" (list of endpoint stats) and "errors" (list of issues)
    
    INVARIANT: After processing line i, stats contains complete
    aggregation for all valid records [1, i], and errors contains
    all parse/validation failures.
    """
    ## parse -> validate -> normalize -> aggregate -> select -> report
    #
    data = [logs]
    errors = []
    results = {}

    #parse
    try parsed = json.loads(raw)
    except Exception as e:
        errors.append(e, "stage:parsing", "error type", json.JSONDecodeError,loc, snippet/raw)
        
        continue 

    #validate 

    try msg = validate_record(parsed)
        if msg: 
            parsed if isinstance(parsed, str) else None 
    except Exception as e: 
        errors.append(e, "stage:validation", "error type", json.JSONDecodeError,loc, snippet/raw)

    #nomralize

    try clean = normalize(parsed)
        parsed if isinstance(parsed, str) else None
    except Exception as e: 
        errors.append(e, "stage:normalization", "error type", json.JSONDecodeError,loc, snippet/raw)

       





    pass


if __name__ == "__main__":
    sample_logs = [
        '{"endpoint": "/api/users", "latency_ms": 100, "status": 200}',
        '{"endpoint": "/api/users", "latency_ms": 150, "status": 500}',
        'malformed json',
        '{"endpoint": "/api/orders", "latency_ms": 50, "status": 200}',
        '{"missing": "fields"}'
    ]
    result = aggregate_logs(sample_logs)
    print(f"Metrics: {result.get('metrics')}")
    print(f"Errors: {result.get('errors')}")

