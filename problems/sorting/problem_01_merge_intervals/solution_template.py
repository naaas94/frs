"""Merge Intervals - Solution Template"""

from typing import List


def merge(intervals: List[List[int]]) -> List[List[int]]:
    """
    Merge overlapping intervals.
    
    Args:
        intervals: List of [start, end] intervals
        
    Returns:
        List of merged non-overlapping intervals
    
    INVARIANT: After sorting by start, overlapping intervals are
    adjacent. We merge if current.start <= last.end.
    """
    # TODO: Implement your solution here
    pass


if __name__ == "__main__":
    result = merge([[1, 3], [2, 6], [8, 10], [15, 18]])
    print(f"Result: {result}")  # Expected: [[1,6],[8,10],[15,18]]


