"""Number of Islands - Solution Template"""

from typing import List
from collections import deque


def num_islands(grid: List[List[str]]) -> int:
    """
    Count the number of islands in the grid.
    
    Args:
        grid: 2D grid where '1' is land, '0' is water
        
    Returns:
        Number of distinct islands
    
    INVARIANT: After BFS/DFS from cell (r, c), all connected land
    cells are marked visited. Each traversal = one island.
    """
    # TODO: Implement your solution here
    pass


if __name__ == "__main__":
    grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"]
    ]
    result = num_islands(grid)
    print(f"Result: {result}")  # Expected: 3

