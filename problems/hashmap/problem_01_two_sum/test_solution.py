"""Tests for Two Sum"""

import pytest
from solution_template import two_sum


class TestTwoSum:
    """Test cases for two_sum function."""
    
    def test_basic_case(self):
        """Basic example from problem statement."""
        result = two_sum([2, 7, 11, 15], 9)
        assert result == (0, 1) or result == (1, 0)
    
    def test_middle_elements(self):
        """Target sum is in middle of array."""
        result = two_sum([3, 2, 4], 6)
        assert sorted(result) == [1, 2]
    
    def test_duplicate_values(self):
        """Same value appears twice."""
        result = two_sum([3, 3], 6)
        assert sorted(result) == [0, 1]
    
    def test_negative_numbers(self):
        """Array contains negative numbers."""
        result = two_sum([-1, -2, -3, -4, -5], -8)
        assert sorted(result) == [2, 4]
    
    def test_zero_target(self):
        """Target is zero with positive and negative."""
        result = two_sum([1, -1, 2, -2], 0)
        i, j = sorted(result)
        nums = [1, -1, 2, -2]
        assert nums[i] + nums[j] == 0
    
    def test_large_numbers(self):
        """Large values near int limits."""
        result = two_sum([1000000000, 2, 1000000000], 2000000000)
        assert sorted(result) == [0, 2]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


