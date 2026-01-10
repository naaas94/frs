"""Two Sum - Solution Template"""

from typing import List, Tuple


def two_sum(nums: List[int], target: int) -> Tuple[int, int]:
    """
    Find two indices whose values sum to target.
    
    Args:
        nums: List of integers
        target: Target sum
        
    Returns:
        Tuple of two indices (i, j) where nums[i] + nums[j] == target
    
    INVARIANT: After processing index i, `seen` contains all values
    from indices [0, i] mapped to their indices.
    """
    # TODO: Implement your solution here
    pass


if __name__ == "__main__":
    # Quick manual test
    result = two_sum([2, 7, 11, 15], 9)
    print(f"Result: {result}")

