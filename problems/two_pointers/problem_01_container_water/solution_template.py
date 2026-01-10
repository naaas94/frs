"""Container With Most Water - Solution Template"""

from typing import List


def max_area(height: List[int]) -> int:
    """
    Find two lines that form a container holding the most water.
    
    Args:
        height: List of line heights
        
    Returns:
        Maximum area of water that can be contained
    
    INVARIANT: The optimal solution is either in [left, right] or
    we've already computed it. We shrink from the shorter side
    because keeping it can't improve the answer.
    """
    # TODO: Implement your solution here
    pass


if __name__ == "__main__":
    result = max_area([1, 8, 6, 2, 5, 4, 8, 3, 7])
    print(f"Result: {result}")  # Expected: 49

