"""
BINARY SEARCH BOUNDARIES PATTERN
=================================

When to use:
- Find boundary in sorted/monotonic data
- Search in rotated sorted array
- Find peak/valley
- Minimize/maximize with monotonic condition

Time: O(log n)
Space: O(1)
"""

from typing import List, Optional, Callable
import bisect


# =============================================================================
# CRITICAL: Binary Search is for BOUNDARIES, not exact matches
# =============================================================================
"""
The key insight: Binary search finds where a condition CHANGES.

Instead of "find x", think "find the first position where f(x) is true"

Two main patterns:
1. bisect_left:  first position where arr[i] >= target
2. bisect_right: first position where arr[i] > target
"""


# =============================================================================
# TEMPLATE 1: Find First Position >= Target (Lower Bound)
# =============================================================================
def lower_bound_template(arr: List[int], target: int) -> int:
    """
    Find the first index where arr[i] >= target.
    If all elements < target, returns len(arr).
    
    This is what bisect_left does.
    
    INVARIANT: 
    - Everything in arr[0:left] is < target
    - Everything in arr[right:] is >= target
    """
    left, right = 0, len(arr)
    
    while left < right:
        mid = left + (right - left) // 2  # Avoid overflow
        
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    
    return left


# =============================================================================
# TEMPLATE 2: Find Last Position <= Target (Upper Bound - 1)
# =============================================================================
def upper_bound_template(arr: List[int], target: int) -> int:
    """
    Find the last index where arr[i] <= target.
    If all elements > target, returns -1.
    
    TRICK: bisect_right gives first index > target, so subtract 1.
    """
    left, right = 0, len(arr)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if arr[mid] <= target:
            left = mid + 1
        else:
            right = mid
    
    return left - 1


# =============================================================================
# TEMPLATE 3: Using Python's bisect module
# =============================================================================
def bisect_examples(arr: List[int], target: int):
    """
    Python's bisect module - use it in interviews!
    
    bisect_left:  first position where arr[i] >= target
    bisect_right: first position where arr[i] > target
    """
    # Find insertion point for target (maintains sorted order)
    idx_left = bisect.bisect_left(arr, target)
    idx_right = bisect.bisect_right(arr, target)
    
    # Check if target exists
    exists = idx_left < len(arr) and arr[idx_left] == target
    
    # Count occurrences of target
    count = idx_right - idx_left
    
    return idx_left, idx_right, exists, count


# =============================================================================
# TEMPLATE 4: Search in Rotated Sorted Array
# =============================================================================
def search_rotated_template(nums: List[int], target: int) -> int:
    """
    Search in a rotated sorted array (no duplicates).
    
    INVARIANT: One half is always sorted. Check which half,
    then check if target is in that sorted half.
    """
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        
        # Left half is sorted
        if nums[left] <= nums[mid]:
            # Target is in left half
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is sorted
        else:
            # Target is in right half
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1


# =============================================================================
# TEMPLATE 5: Find Peak Element
# =============================================================================
def find_peak_template(nums: List[int]) -> int:
    """
    Find any peak (element greater than neighbors).
    
    INVARIANT: If nums[mid] < nums[mid+1], peak is on the right.
               If nums[mid] > nums[mid+1], peak is on the left (or mid itself).
    """
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] < nums[mid + 1]:
            # Ascending, peak is to the right
            left = mid + 1
        else:
            # Descending or at peak, search left (including mid)
            right = mid
    
    return left


# =============================================================================
# TEMPLATE 6: Find Minimum in Rotated Sorted Array
# =============================================================================
def find_min_rotated_template(nums: List[int]) -> int:
    """
    Find minimum element in rotated sorted array.
    
    INVARIANT: If nums[mid] > nums[right], min is in right half.
               Otherwise, min is in left half (including mid).
    """
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] > nums[right]:
            # Rotation point is in right half
            left = mid + 1
        else:
            # Min is in left half (including mid)
            right = mid
    
    return nums[left]


# =============================================================================
# TEMPLATE 7: Binary Search on Answer (Minimize/Maximize)
# =============================================================================
def binary_search_on_answer_template(low: int, high: int, is_feasible: Callable[[int], bool]) -> int:
    """
    Find minimum value where condition becomes True.
    
    Used for: "What's the minimum X such that we can achieve Y?"
    
    INVARIANT: 
    - All values in [low, left) make is_feasible return False
    - All values in [left, high] make is_feasible return True
    """
    while low < high:
        mid = low + (high - low) // 2
        
        if is_feasible(mid):
            high = mid  # mid might be answer, but try smaller
        else:
            low = mid + 1  # mid doesn't work, try larger
    
    return low


# Example: Koko eating bananas
def min_eating_speed(piles: List[int], h: int) -> int:
    """
    Find minimum eating speed to finish all piles in h hours.
    """
    def can_finish(speed: int) -> bool:
        hours = sum((pile + speed - 1) // speed for pile in piles)  # Ceiling division
        return hours <= h
    
    left, right = 1, max(piles)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if can_finish(mid):
            right = mid
        else:
            left = mid + 1
    
    return left


# =============================================================================
# EDGE CASES TO CHECK
# =============================================================================
"""
□ Empty array
□ Single element
□ Target not in array
□ Target at first/last position
□ All elements same
□ Two elements
□ Duplicates (affects rotated search!)
□ Integer overflow in mid calculation (use left + (right-left)//2)
"""


# =============================================================================
# COMMON BUGS
# =============================================================================
"""
1. Off-by-one: left < right vs left <= right (depends on inclusive/exclusive)
2. Infinite loop: not moving left or right correctly
3. mid calculation: (left + right) // 2 can overflow -> use left + (right - left) // 2
4. Wrong boundary: searching for >= vs > vs == 
5. Return value: index vs value vs -1
6. Rotated array with duplicates: worst case O(n)
"""

