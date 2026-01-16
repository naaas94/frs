# JSONL Log Aggregation

## Difficulty: Medium
## Pattern: Data Plumbing (parse → validate → aggregate → report)

## Problem Statement

You are given a list of JSONL (JSON Lines) strings representing API request logs. Each valid log entry has the following structure:

```json
{"endpoint": "/api/users", "latency_ms": 120, "status": 200, "timestamp": "2024-01-15T10:30:00Z"}
```

Write a function that:
1. Parses each line as JSON (skip malformed lines)
2. Validates required fields exist (endpoint, latency_ms, status)
3. Aggregates metrics per endpoint: request count, average latency, error rate (status >= 400)
4. Returns results sorted by request count descending, plus a list of parse/validation errors

## Examples

```
Input: [
    '{"endpoint": "/api/users", "latency_ms": 100, "status": 200}',
    '{"endpoint": "/api/users", "latency_ms": 150, "status": 500}',
    'malformed json',
    '{"endpoint": "/api/orders", "latency_ms": 50, "status": 200}',
    '{"missing": "fields"}'
]

Output: {
    "metrics": [
        {"endpoint": "/api/users", "count": 2, "avg_latency": 125.0, "error_rate": 0.5},
        {"endpoint": "/api/orders", "count": 1, "avg_latency": 50.0, "error_rate": 0.0}
    ],
    "errors": [
        {"line": 3, "type": "parse"},
        {"line": 5, "type": "validation"}
    ]
}
```

## Constraints

- 0 <= len(logs) <= 10^5
- Each line is a string (may be malformed JSON)
- Latency values are positive integers
- Status codes are integers

## Time/Space Targets

- Time: O(n) single pass
- Space: O(e) where e = unique endpoints


