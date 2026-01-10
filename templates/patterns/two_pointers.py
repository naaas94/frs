"""
TWO POINTERS / SLIDING WINDOW PATTERN
======================================

When to use:
- Subarray/substring problems with constraints
- Finding pairs in sorted arrays
- Shrink/expand window to optimize
- In-place array modifications

Time: O(n) typically (each pointer moves at most n times)
Space: O(1) for pointers, O(k) if storing window contents
"""

from typing import List, Set
from collections import defaultdict


# =============================================================================
# TEMPLATE 1: Fixed-Size Sliding Window
# =============================================================================
def fixed_window_template(arr: List[int], k: int) -> int:
    """
    Process all windows of size k.
    
    INVARIANT: window always contains exactly k elements [i-k+1, i].
    """
    if len(arr) < k:
        return 0
    
    # Initialize first window
    window_sum = sum(arr[:k])
    result = window_sum
    
    # Slide window: remove left element, add right element
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        result = max(result, window_sum)  # or min, or other operation
    
    return result


# =============================================================================
# TEMPLATE 2: Variable-Size Sliding Window (Shrink/Expand)
# =============================================================================
def variable_window_template(s: str) -> int:
    """
    Find longest/shortest substring satisfying some condition.
    
    INVARIANT: window [left, right] always satisfies the constraint.
    When constraint breaks, shrink from left until valid again.
    """
    left = 0
    result = 0
    window_state = {}  # Track what's in the window (e.g., char counts)
    
    for right in range(len(s)):
        # EXPAND: Add s[right] to window
        char = s[right]
        window_state[char] = window_state.get(char, 0) + 1
        
        # SHRINK: While window is invalid, remove from left
        while not is_valid(window_state):  # Define your validity check
            left_char = s[left]
            window_state[left_char] -= 1
            if window_state[left_char] == 0:
                del window_state[left_char]
            left += 1
        
        # UPDATE: Window [left, right] is now valid
        result = max(result, right - left + 1)
    
    return result


def is_valid(state: dict) -> bool:
    """Define your window validity condition here."""
    # Example: all characters appear at most once
    return all(count <= 1 for count in state.values())


# =============================================================================
# TEMPLATE 3: Longest Substring Without Repeating Characters
# =============================================================================
def longest_unique_substring(s: str) -> int:
    """
    Classic sliding window problem.
    
    INVARIANT: window [left, right] contains no duplicate characters.
    """
    char_index = {}  # char -> last seen index
    left = 0
    max_length = 0
    
    for right, char in enumerate(s):
        # If char was seen and is in current window, shrink
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1
        
        char_index[char] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length


# =============================================================================
# TEMPLATE 4: Two Pointers - Opposite Ends (Sorted Array)
# =============================================================================
def two_sum_sorted_template(nums: List[int], target: int) -> List[int]:
    """
    Find two numbers in SORTED array that sum to target.
    
    INVARIANT: If sum < target, we need larger sum (move left pointer right).
               If sum > target, we need smaller sum (move right pointer left).
    """
    left, right = 0, len(nums) - 1
    
    while left < right:
        current_sum = nums[left] + nums[right]
        
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return []  # Not found


# =============================================================================
# TEMPLATE 5: Container With Most Water
# =============================================================================
def container_water_template(heights: List[int]) -> int:
    """
    Find max area between two lines.
    
    INVARIANT: We can only improve by moving the shorter line inward,
    because moving the taller line can only decrease the area.
    """
    left, right = 0, len(heights) - 1
    max_area = 0
    
    while left < right:
        width = right - left
        height = min(heights[left], heights[right])
        max_area = max(max_area, width * height)
        
        # Move the shorter side
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1
    
    return max_area


# =============================================================================
# TEMPLATE 6: Fast/Slow Pointers (Same Direction)
# =============================================================================
def remove_duplicates_template(nums: List[int]) -> int:
    """
    Remove duplicates in-place from SORTED array.
    
    INVARIANT: nums[0:slow+1] contains unique elements.
    fast scans ahead, slow marks where to place next unique.
    """
    if not nums:
        return 0
    
    slow = 0
    
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    
    return slow + 1  # Length of unique portion


# =============================================================================
# EDGE CASES TO CHECK
# =============================================================================
"""
□ Empty array/string
□ Single element
□ Window size > array length
□ All elements the same
□ All elements different
□ Target not achievable
□ Negative numbers
"""


# =============================================================================
# COMMON BUGS
# =============================================================================
"""
1. Off-by-one in window boundaries -> window is [left, right] inclusive
2. Forgetting to update left when constraint breaks
3. Not handling empty string/array upfront
4. Wrong shrink condition (< vs <=)
5. Accessing index -1 when left = 0
"""

