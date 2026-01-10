"""JSONL Log Aggregation - Solution Template"""

import json
from typing import List, Dict, Any
from collections import defaultdict


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
    # TODO: Implement your solution here
    # Steps:
    # 1. PARSE: Try json.loads(), catch JSONDecodeError
    # 2. VALIDATE: Check required fields exist
    # 3. AGGREGATE: Update endpoint stats
    # 4. SELECT: Sort by count descending
    # 5. REPORT: Return metrics + errors
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

