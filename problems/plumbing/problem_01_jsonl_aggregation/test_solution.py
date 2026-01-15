"""Tests for JSONL Log Aggregation"""

import pytest
from solution_template import aggregate_logs


class TestAggregateLogs:
    """Test cases for aggregate_logs function."""
    
    def test_basic_aggregation(self):
        """Basic case with valid logs."""
        logs = [
            '{"endpoint": "/api/users", "latency_ms": 100, "status": 200}',
            '{"endpoint": "/api/users", "latency_ms": 200, "status": 200}',
        ]
        result = aggregate_logs(logs)
        assert len(result["metrics"]) == 1
        assert result["metrics"][0]["count"] == 2
        assert result["metrics"][0]["avg_latency"] == 150.0
        assert result["metrics"][0]["error_rate"] == 0.0
        assert len(result["errors"]) == 0
    
    def test_parse_error(self):
        """Malformed JSON is captured as error."""
        logs = [
            '{"endpoint": "/api/users", "latency_ms": 100, "status": 200}',
            'not valid json',
        ]
        result = aggregate_logs(logs)
        assert len(result["metrics"]) == 1
        assert len(result["errors"]) == 1
        assert result["errors"][0]["type"] == "parse"
        assert result["errors"][0]["line"] == 1
    
    def test_validation_error(self):
        """Missing required fields captured as validation error."""
        logs = [
            '{"endpoint": "/api/users", "latency_ms": 100, "status": 200}',
            '{"endpoint": "/api/orders"}',  # missing latency_ms and status
        ]
        result = aggregate_logs(logs)
        assert len(result["metrics"]) == 1
        assert len(result["errors"]) == 1
        assert result["errors"][0]["type"] == "validation"
    
    def test_error_rate_calculation(self):
        """Error rate calculated correctly for status >= 400."""
        logs = [
            '{"endpoint": "/api/users", "latency_ms": 100, "status": 200}',
            '{"endpoint": "/api/users", "latency_ms": 100, "status": 404}',
            '{"endpoint": "/api/users", "latency_ms": 100, "status": 500}',
        ]
        result = aggregate_logs(logs)
        # 2 out of 3 are errors (404, 500)
        assert abs(result["metrics"][0]["error_rate"] - 2/3) < 0.01
    
    def test_sorted_by_count(self):
        """Results sorted by count descending."""
        logs = [
            '{"endpoint": "/api/orders", "latency_ms": 50, "status": 200}',
            '{"endpoint": "/api/users", "latency_ms": 100, "status": 200}',
            '{"endpoint": "/api/users", "latency_ms": 100, "status": 200}',
            '{"endpoint": "/api/users", "latency_ms": 100, "status": 200}',
        ]
        result = aggregate_logs(logs)
        assert result["metrics"][0]["endpoint"] == "/api/users"
        assert result["metrics"][0]["count"] == 3
    
    def test_empty_input(self):
        """Empty log list."""
        result = aggregate_logs([])
        assert result["metrics"] == []
        assert result["errors"] == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

