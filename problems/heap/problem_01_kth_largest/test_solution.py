"""Tests for Kth Largest Element"""

import pytest
from solution_template import find_kth_largest


class TestFindKthLargest:
    """Test cases for find_kth_largest function."""
    
    def test_basic_case(self):
        """Standard example."""
        assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    
    def test_with_duplicates(self):
        """Array with duplicate values."""
        assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    
    def test_k_equals_1(self):
        """Find the largest element."""
        assert find_kth_largest([3, 2, 1, 5, 6, 4], 1) == 6
    
    def test_k_equals_n(self):
        """Find the smallest element."""
        assert find_kth_largest([3, 2, 1, 5, 6, 4], 6) == 1
    
    def test_single_element(self):
        """Single element array."""
        assert find_kth_largest([1], 1) == 1
    
    def test_all_same(self):
        """All elements are the same."""
        assert find_kth_largest([5, 5, 5, 5], 2) == 5
    
    def test_negative_numbers(self):
        """Array with negative numbers."""
        assert find_kth_largest([-1, -2, -3, -4], 2) == -2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

