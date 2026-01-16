"""Search in Rotated Sorted Array - Solution Template"""

from typing import List


def search(nums: List[int], target: int) -> int:
    """
    Search for target in rotated sorted array.
    
    Args:
        nums: Rotated sorted array with unique elements
        target: Value to find
        
    Returns:
        Index of target, or -1 if not found
    
    INVARIANT: One half is always sorted. Check if target is in 
    the sorted half, otherwise search the other half.
    """
    # TODO: Implement your solution here
    pass


if __name__ == "__main__":
    result = search([4, 5, 6, 7, 0, 1, 2], 0)
    print(f"Result: {result}")  # Expected: 4


