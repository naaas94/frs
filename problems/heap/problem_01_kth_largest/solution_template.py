"""Kth Largest Element - Solution Template"""

from typing import List
import heapq


def find_kth_largest(nums: List[int], k: int) -> int:
    """
    Find the kth largest element in the array.
    
    Args:
        nums: List of integers
        k: Which largest element to find (1-indexed)
        
    Returns:
        The kth largest element
    
    INVARIANT: Maintain a min-heap of size k containing the k largest
    elements seen so far. The root is the kth largest.
    """
    # TODO: Implement your solution here
    pass


if __name__ == "__main__":
    result = find_kth_largest([3, 2, 1, 5, 6, 4], 2)
    print(f"Result: {result}")  # Expected: 5


