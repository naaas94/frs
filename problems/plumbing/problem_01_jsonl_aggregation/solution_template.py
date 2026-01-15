"""JSONL Log Aggregation - Solution Template"""

import json
from re import T
from typing import List, Dict, Any
from collections import defaultdict

import sys
from pathlib import Path

# Add project root to sys.path to enable imports
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

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
    errors: list[dict[str, any]] = []
    stats = {"total":0,"valid":0,"invalid":0}

    def _new_acc() -> dict[str,any]:
        return {
            "count":0,
            "sum_latency_ms": 0.00,
            "min_latency": None,
            "max_latency": None,
            "error_count": 0,
            "success_count": 0
        } 

    acc: dict[str, dict[str, any]] = defaultdict(_new_acc)
    
    def normalize_record(record: Dict) -> Dict:
        return {
            "endpoint": str(record["endpoint"]),
            "latency_ms": int(record["latency_ms"]),
            "status": int(record["status"])
        }



        #### parse 
    for i, line in enumerate(logs):
        stats["total"] +=1 
        try: 
            parsed = json.loads(line.strip())
        except json.JSONDecodeError as e: 
            errors.append(
                {
                    "line": i,
                    "type":"parse",
                    "message": str(e),
                    "raw": line
                }
            )   
            stats["invalid"] =+1
            continue
        
        ### validate 

        validated = validate_record(parsed)
        if validated: 
            stats["valid"] +=1
        else:
            errors.append(
                {
                    "line": i,
                    "type":"validation",
                    "message": validated,
                    "raw": parsed
                }
            )
            stats["invalid"] +=1
            continue

        ### normalize

        try:
            clean = normalize_record(parsed)
        except Exception as e:
        
            errors.append(
                {
                    "line_num": i,
                    "error":"normalize_error",
                    "message": str(e),
                    "line": parsed
                }
            )
            stats["invalid"] =+1
            continue

        ### agg
        endpoint = clean.get("endpoint", "unknown")
        latency = clean.get("latency_ms", None)
        status = clean.get("status", None)

        # check types if normalize didnt + add to statistics


        #select?

        a = acc[endpoint]
        a["count"] +=1 
        a["sum_latency_ms"] += float(latency)
        
        if status >= 400: 
            a["error_count"] +=1
        else:
            a["success_count"] +=1         
        
        

    ### final reporting
    metrics: list[dict[str,any]] = []

    for endpoint, a in acc.items(): 
        count = a["count"]
        avg_latency = (a["sum_latency_ms"] / count) if count else 0.00
        error_rate = (a["error_count"] / count) if count else 0.00
        metrics.append(
            {
                "endpoint": endpoint,
                "count": count,
                "avg_latency":avg_latency,
                "error_rate": error_rate
            }
        )
    metrics.sort(key=lambda m: (-m["count"], m["endpoint"]))

    return{"metrics":metrics,"errors":errors,"stats":stats}



















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

