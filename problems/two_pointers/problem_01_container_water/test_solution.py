"""Tests for Container With Most Water"""

import pytest
from solution_template import max_area


class TestMaxArea:
    """Test cases for max_area function."""
    
    def test_basic_case(self):
        """Standard example."""
        assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    
    def test_two_elements(self):
        """Minimum array size."""
        assert max_area([1, 1]) == 1
    
    def test_increasing(self):
        """Heights strictly increasing."""
        assert max_area([1, 2, 3, 4, 5]) == 6  # 1 and 5 with height 1, or 2 and 4 with height 2*2=4... actually (0,4) gives 4*1=4, (1,4) gives 3*2=6
    
    def test_decreasing(self):
        """Heights strictly decreasing."""
        assert max_area([5, 4, 3, 2, 1]) == 6
    
    def test_same_height(self):
        """All same height."""
        assert max_area([5, 5, 5, 5, 5]) == 20  # width 4, height 5
    
    def test_valley(self):
        """Valley shape."""
        assert max_area([10, 1, 1, 1, 10]) == 40  # width 4, height 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


