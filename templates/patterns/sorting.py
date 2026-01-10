"""
SORTING WITH KEY FUNCTIONS PATTERN
===================================

When to use:
- Custom ordering requirements
- Tie-breaker logic (sort by X, then by Y)
- Interval problems (merge, overlap)
- Greedy algorithms that need sorted input

Time: O(n log n) for the sort
Space: O(n) for Timsort's merge operations
"""

from typing import List, Tuple, Callable, Any
from functools import cmp_to_key


# =============================================================================
# TEMPLATE 1: Single Key Sort
# =============================================================================
def single_key_sort_template(items: List[Any], key_func: Callable) -> List[Any]:
    """
    Sort by a single computed key.
    
    Examples:
    - Sort strings by length: key=len
    - Sort by absolute value: key=abs
    - Sort by second element: key=lambda x: x[1]
    """
    return sorted(items, key=key_func)


# =============================================================================
# TEMPLATE 2: Multi-Key Sort with Tie-Breakers
# =============================================================================
def multi_key_sort_template(items: List[Tuple]) -> List[Tuple]:
    """
    Sort by multiple keys with different directions.
    
    TRICK: Use tuple of keys. Negate numeric values for descending.
    
    Example: Sort by score descending, then by name ascending
    """
    # items = [(name, score), ...]
    
    # Sort by score DESC (-x[1]), then name ASC (x[0])
    return sorted(items, key=lambda x: (-x[1], x[0]))


# Example with strings (can't negate)
def sort_with_string_tiebreaker(items: List[Tuple[str, int, str]]) -> List:
    """
    When you can't negate (strings), use cmp_to_key.
    
    items = [(name, priority, category), ...]
    Sort by: priority ASC, category DESC, name ASC
    """
    def compare(a, b):
        # Compare priority ascending
        if a[1] != b[1]:
            return a[1] - b[1]
        # Compare category descending (reverse the comparison)
        if a[2] != b[2]:
            return -1 if a[2] > b[2] else 1
        # Compare name ascending
        if a[0] != b[0]:
            return -1 if a[0] < b[0] else 1
        return 0
    
    return sorted(items, key=cmp_to_key(compare))


# =============================================================================
# TEMPLATE 3: Merge Intervals
# =============================================================================
def merge_intervals_template(intervals: List[List[int]]) -> List[List[int]]:
    """
    Merge overlapping intervals.
    
    INVARIANT: After sorting by start time, we only need to check
    if current interval overlaps with the last merged interval.
    """
    if not intervals:
        return []
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        last_end = merged[-1][1]
        
        if start <= last_end:  # Overlapping
            merged[-1][1] = max(last_end, end)
        else:  # Non-overlapping
            merged.append([start, end])
    
    return merged


# =============================================================================
# TEMPLATE 4: Meeting Rooms II (Min Rooms Needed)
# =============================================================================
def min_meeting_rooms_template(intervals: List[List[int]]) -> int:
    """
    Find minimum number of rooms needed for all meetings.
    
    TRICK: Treat starts and ends as separate events.
    Sort all events, +1 for start, -1 for end.
    Track maximum concurrent meetings.
    """
    events = []
    
    for start, end in intervals:
        events.append((start, 1))   # +1 room needed
        events.append((end, -1))    # -1 room freed
    
    # Sort by time; if tie, process ends before starts (free room first)
    events.sort(key=lambda x: (x[0], x[1]))
    
    max_rooms = 0
    current_rooms = 0
    
    for time, delta in events:
        current_rooms += delta
        max_rooms = max(max_rooms, current_rooms)
    
    return max_rooms


# =============================================================================
# TEMPLATE 5: Custom Object Sorting
# =============================================================================
class Task:
    def __init__(self, name: str, priority: int, deadline: int):
        self.name = name
        self.priority = priority
        self.deadline = deadline
    
    def __repr__(self):
        return f"Task({self.name}, p={self.priority}, d={self.deadline})"


def sort_tasks_template(tasks: List[Task]) -> List[Task]:
    """
    Sort custom objects by multiple attributes.
    """
    # Sort by deadline ASC, then priority DESC, then name ASC
    return sorted(tasks, key=lambda t: (t.deadline, -t.priority, t.name))


# =============================================================================
# TEMPLATE 6: Lexicographic Sort Edge Cases
# =============================================================================
def largest_number_template(nums: List[int]) -> str:
    """
    Arrange numbers to form the largest number.
    
    TRICK: Compare a+b vs b+a as strings.
    Example: "9" + "34" = "934" vs "34" + "9" = "349" → "9" comes first
    """
    str_nums = [str(n) for n in nums]
    
    def compare(a, b):
        if a + b > b + a:
            return -1  # a should come first
        elif a + b < b + a:
            return 1   # b should come first
        return 0
    
    str_nums.sort(key=cmp_to_key(compare))
    
    # Handle edge case: all zeros
    if str_nums[0] == "0":
        return "0"
    
    return "".join(str_nums)


# =============================================================================
# EDGE CASES TO CHECK
# =============================================================================
"""
□ Empty list
□ Single element
□ All elements equal
□ Already sorted
□ Reverse sorted
□ Intervals that touch (end == start of next)
□ Nested intervals
□ Negative numbers in keys
□ String comparison vs numeric comparison
"""


# =============================================================================
# COMMON BUGS
# =============================================================================
"""
1. Modifying list while sorting -> use sorted() for new list
2. Wrong direction for negation (descending = negate)
3. String comparison is lexicographic, not numeric ("9" > "10")
4. Interval overlap: using < instead of <= (off-by-one)
5. Tie-breaker order matters: (a, b) != (b, a)
6. cmp_to_key return values: -1 (a first), 1 (b first), 0 (equal)
"""

