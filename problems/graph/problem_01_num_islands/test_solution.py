"""Tests for Number of Islands"""

import pytest
from solution_template import num_islands


class TestNumIslands:
    """Test cases for num_islands function."""
    
    def test_single_island(self):
        """One large island."""
        grid = [
            ["1", "1", "1", "1", "0"],
            ["1", "1", "0", "1", "0"],
            ["1", "1", "0", "0", "0"],
            ["0", "0", "0", "0", "0"]
        ]
        assert num_islands(grid) == 1
    
    def test_multiple_islands(self):
        """Three separate islands."""
        grid = [
            ["1", "1", "0", "0", "0"],
            ["1", "1", "0", "0", "0"],
            ["0", "0", "1", "0", "0"],
            ["0", "0", "0", "1", "1"]
        ]
        assert num_islands(grid) == 3
    
    def test_no_islands(self):
        """All water."""
        grid = [["0", "0"], ["0", "0"]]
        assert num_islands(grid) == 0
    
    def test_all_land(self):
        """Entire grid is one island."""
        grid = [["1", "1"], ["1", "1"]]
        assert num_islands(grid) == 1
    
    def test_single_cell_land(self):
        """Single cell of land."""
        grid = [["1"]]
        assert num_islands(grid) == 1
    
    def test_diagonal_not_connected(self):
        """Diagonal cells are not connected."""
        grid = [
            ["1", "0"],
            ["0", "1"]
        ]
        assert num_islands(grid) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

