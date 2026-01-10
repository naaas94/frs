"""
DATA PLUMBING PIPELINE PATTERN
===============================

The interview-isomorphic pattern:
parse → validate → normalize → aggregate → select top-k/best → report errors

This covers 90% of "real-world" coding questions.

When to use:
- JSONL/CSV/log processing
- API response handling
- ETL-style transformations
- Error aggregation and reporting
"""

import json
import csv
from typing import List, Dict, Any, Optional, Tuple, Callable, Iterator
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
import re


# =============================================================================
# THE PIPELINE PATTERN
# =============================================================================
"""
Every data plumbing problem follows this flow:

1. PARSE: Read raw input (JSONL, CSV, API response)
2. VALIDATE: Check required fields, types, constraints
3. NORMALIZE: Clean, transform, standardize
4. AGGREGATE: Group, count, sum, compute metrics
5. SELECT: Top-k, filter by condition, rank
6. REPORT: Format output, include error summary
"""


# =============================================================================
# TEMPLATE 1: JSONL Processing Pipeline
# =============================================================================
@dataclass
class ProcessingResult:
    """Container for pipeline results."""
    data: List[Dict]
    errors: List[Dict]
    stats: Dict[str, Any]


def process_jsonl_template(lines: Iterator[str]) -> ProcessingResult:
    """
    Complete JSONL processing pipeline.
    
    INVARIANT: Every line is either successfully processed or logged as an error.
    """
    valid_records = []
    errors = []
    stats = {"total": 0, "valid": 0, "invalid": 0}
    
    for line_num, line in enumerate(lines, 1):
        stats["total"] += 1
        
        # PARSE
        try:
            record = json.loads(line.strip())
        except json.JSONDecodeError as e:
            errors.append({
                "line": line_num,
                "error": "parse_error",
                "message": str(e),
                "raw": line[:100]
            })
            stats["invalid"] += 1
            continue
        
        # VALIDATE
        validation_error = validate_record(record)
        if validation_error:
            errors.append({
                "line": line_num,
                "error": "validation_error",
                "message": validation_error,
                "record": record
            })
            stats["invalid"] += 1
            continue
        
        # NORMALIZE
        normalized = normalize_record(record)
        
        valid_records.append(normalized)
        stats["valid"] += 1
    
    return ProcessingResult(data=valid_records, errors=errors, stats=stats)


def validate_record(record: Dict) -> Optional[str]:
    """
    Validate a single record. Returns error message or None if valid.
    
    Customize for your schema.
    """
    required_fields = ["id", "timestamp", "value"]
    
    for field in required_fields:
        if field not in record:
            return f"Missing required field: {field}"
    
    # Type checks
    if not isinstance(record.get("value"), (int, float)):
        return f"Invalid type for 'value': expected number"
    
    return None


def normalize_record(record: Dict) -> Dict:
    """
    Normalize a validated record.
    
    Common transformations:
    - Parse dates
    - Lowercase strings
    - Convert types
    - Add computed fields
    """
    return {
        "id": str(record["id"]),
        "timestamp": parse_timestamp(record["timestamp"]),
        "value": float(record["value"]),
        # Add computed fields
        "value_bucket": record["value"] // 10 * 10
    }


def parse_timestamp(ts: Any) -> datetime:
    """Parse various timestamp formats."""
    if isinstance(ts, datetime):
        return ts
    if isinstance(ts, (int, float)):
        return datetime.fromtimestamp(ts)
    if isinstance(ts, str):
        # Try common formats
        for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
            try:
                return datetime.strptime(ts, fmt)
            except ValueError:
                continue
    raise ValueError(f"Cannot parse timestamp: {ts}")


# =============================================================================
# TEMPLATE 2: CSV Processing with Error Handling
# =============================================================================
def process_csv_template(filepath: str) -> ProcessingResult:
    """
    Process CSV file with robust error handling.
    """
    valid_records = []
    errors = []
    
    with open(filepath, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row_num, row in enumerate(reader, 2):  # 2 because header is row 1
            try:
                # VALIDATE
                if not row.get("id"):
                    raise ValueError("Missing id")
                
                # NORMALIZE
                record = {
                    "id": row["id"].strip(),
                    "name": row.get("name", "").strip().lower(),
                    "amount": float(row.get("amount", 0))
                }
                
                valid_records.append(record)
                
            except (ValueError, KeyError) as e:
                errors.append({
                    "row": row_num,
                    "error": str(e),
                    "raw": dict(row)
                })
    
    return ProcessingResult(
        data=valid_records,
        errors=errors,
        stats={"valid": len(valid_records), "errors": len(errors)}
    )


# =============================================================================
# TEMPLATE 3: Aggregation Patterns
# =============================================================================
def aggregate_template(records: List[Dict]) -> Dict[str, Any]:
    """
    Common aggregation operations.
    """
    if not records:
        return {"count": 0}
    
    # Group by key
    by_category = defaultdict(list)
    for r in records:
        by_category[r.get("category", "unknown")].append(r)
    
    # Compute stats per group
    stats = {}
    for category, items in by_category.items():
        values = [item["value"] for item in items]
        stats[category] = {
            "count": len(items),
            "sum": sum(values),
            "avg": sum(values) / len(values),
            "min": min(values),
            "max": max(values)
        }
    
    return stats


def top_k_by_field(records: List[Dict], field: str, k: int, reverse: bool = True) -> List[Dict]:
    """
    Get top-k records by a field value.
    
    reverse=True: largest first (default)
    reverse=False: smallest first
    """
    return sorted(records, key=lambda r: r.get(field, 0), reverse=reverse)[:k]


# =============================================================================
# TEMPLATE 4: API Response Processing
# =============================================================================
def process_api_response_template(response: Dict) -> ProcessingResult:
    """
    Process paginated or nested API responses.
    """
    errors = []
    
    # Check for API-level errors
    if response.get("error"):
        return ProcessingResult(
            data=[],
            errors=[{"error": "api_error", "message": response["error"]}],
            stats={"success": False}
        )
    
    # Extract data (handle different response shapes)
    data = response.get("data") or response.get("results") or response.get("items") or []
    
    if not isinstance(data, list):
        data = [data]
    
    # Process each item
    valid_items = []
    for i, item in enumerate(data):
        try:
            processed = {
                "id": item["id"],
                "value": item.get("value", 0),
                "metadata": item.get("meta", {})
            }
            valid_items.append(processed)
        except (KeyError, TypeError) as e:
            errors.append({"index": i, "error": str(e)})
    
    return ProcessingResult(
        data=valid_items,
        errors=errors,
        stats={
            "total": len(data),
            "valid": len(valid_items),
            "has_next": response.get("has_next", False),
            "cursor": response.get("cursor")
        }
    )


# =============================================================================
# TEMPLATE 5: Error Aggregation and Reporting
# =============================================================================
def aggregate_errors(errors: List[Dict]) -> Dict[str, Any]:
    """
    Summarize errors by type/category.
    """
    if not errors:
        return {"total": 0, "by_type": {}}
    
    error_types = Counter(e.get("error", "unknown") for e in errors)
    
    return {
        "total": len(errors),
        "by_type": dict(error_types),
        "sample_errors": errors[:5],  # First 5 for debugging
        "most_common": error_types.most_common(3)
    }


def format_report(result: ProcessingResult) -> str:
    """
    Format processing result as human-readable report.
    """
    lines = [
        "=" * 50,
        "PROCESSING REPORT",
        "=" * 50,
        f"Total records: {result.stats.get('total', len(result.data) + len(result.errors))}",
        f"Valid: {result.stats.get('valid', len(result.data))}",
        f"Errors: {result.stats.get('invalid', len(result.errors))}",
    ]
    
    if result.errors:
        lines.append("")
        lines.append("ERROR SUMMARY:")
        error_summary = aggregate_errors(result.errors)
        for error_type, count in error_summary["by_type"].items():
            lines.append(f"  - {error_type}: {count}")
    
    lines.append("=" * 50)
    return "\n".join(lines)


# =============================================================================
# TEMPLATE 6: Log Parsing (Regex + Aggregation)
# =============================================================================
def parse_logs_template(log_lines: List[str]) -> ProcessingResult:
    """
    Parse structured log files.
    
    Example log format: "2024-01-15 10:30:45 [ERROR] Service failed: timeout"
    """
    log_pattern = re.compile(
        r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (.+)'
    )
    
    records = []
    errors = []
    
    for i, line in enumerate(log_lines):
        match = log_pattern.match(line.strip())
        
        if match:
            timestamp_str, level, message = match.groups()
            records.append({
                "line": i + 1,
                "timestamp": datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S"),
                "level": level.upper(),
                "message": message
            })
        else:
            errors.append({"line": i + 1, "error": "parse_failed", "raw": line[:100]})
    
    # Aggregate by level
    level_counts = Counter(r["level"] for r in records)
    
    return ProcessingResult(
        data=records,
        errors=errors,
        stats={"by_level": dict(level_counts)}
    )


# =============================================================================
# EDGE CASES TO CHECK
# =============================================================================
"""
□ Empty input
□ Malformed JSON/CSV
□ Missing required fields
□ Wrong types (string where number expected)
□ Unicode/encoding issues
□ Very large files (memory)
□ Nested/complex structures
□ Null/None values
□ Empty strings vs missing fields
□ Timezone handling
"""


# =============================================================================
# COMMON BUGS
# =============================================================================
"""
1. Not handling empty input upfront
2. Using dict[key] instead of dict.get(key) for optional fields
3. Not stripping whitespace from CSV fields
4. Assuming JSON is valid without try/except
5. Integer division when float expected
6. Not preserving error context (line number, raw data)
7. Modifying data while iterating
8. Timezone-naive datetime comparisons
"""

