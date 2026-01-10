"""Tests for Search in Rotated Sorted Array"""

import pytest
from solution_template import search


class TestSearchRotated:
    """Test cases for search function."""
    
    def test_target_in_right_half(self):
        """Target is in the smaller (right) half."""
        assert search([4, 5, 6, 7, 0, 1, 2], 0) == 4
    
    def test_target_not_found(self):
        """Target doesn't exist."""
        assert search([4, 5, 6, 7, 0, 1, 2], 3) == -1
    
    def test_single_element_not_found(self):
        """Single element, target not present."""
        assert search([1], 0) == -1
    
    def test_single_element_found(self):
        """Single element, target present."""
        assert search([1], 1) == 0
    
    def test_target_in_left_half(self):
        """Target is in the larger (left) half."""
        assert search([4, 5, 6, 7, 0, 1, 2], 5) == 1
    
    def test_target_at_pivot(self):
        """Target is at the rotation point."""
        assert search([4, 5, 6, 7, 0, 1, 2], 7) == 3
    
    def test_no_rotation(self):
        """Array is not rotated (rotated by 0)."""
        assert search([1, 2, 3, 4, 5], 3) == 2
    
    def test_rotated_by_one(self):
        """Array rotated by one position."""
        assert search([2, 1], 1) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

