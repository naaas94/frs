"""Tests for Merge Intervals"""

import pytest
from solution_template import merge


class TestMergeIntervals:
    """Test cases for merge function."""
    
    def test_basic_merge(self):
        """Standard overlapping intervals."""
        assert merge([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    
    def test_touching_intervals(self):
        """Intervals that touch at endpoints."""
        assert merge([[1, 4], [4, 5]]) == [[1, 5]]
    
    def test_single_interval(self):
        """Only one interval."""
        assert merge([[1, 5]]) == [[1, 5]]
    
    def test_no_overlap(self):
        """No intervals overlap."""
        assert merge([[1, 2], [4, 5], [7, 8]]) == [[1, 2], [4, 5], [7, 8]]
    
    def test_all_overlap(self):
        """All intervals merge into one."""
        assert merge([[1, 10], [2, 5], [3, 7]]) == [[1, 10]]
    
    def test_unsorted_input(self):
        """Input not sorted by start."""
        assert merge([[8, 10], [1, 3], [2, 6], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    
    def test_contained_interval(self):
        """One interval fully contains another."""
        assert merge([[1, 10], [3, 5]]) == [[1, 10]]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


