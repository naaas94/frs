"""
HASHMAP GROUPING / COUNTING PATTERN
====================================

When to use:
- Count frequencies of elements
- Group elements by some key/property
- Find pairs/complements (two-sum style)
- Check for duplicates or anagrams

Time: O(n) typically
Space: O(n) for the hashmap
"""

from collections import Counter, defaultdict
from typing import List, Dict, Any, Tuple


# =============================================================================
# TEMPLATE 1: Frequency Counting
# =============================================================================
def frequency_count_template(arr: List[Any]) -> Dict[Any, int]:
    """
    Count occurrences of each element.
    
    Example: [1, 2, 2, 3, 3, 3] -> {1: 1, 2: 2, 3: 3}
    """
    # Method 1: Counter (preferred)
    counts = Counter(arr)
    
    # Method 2: Manual (if you need custom logic)
    # counts = {}
    # for x in arr:
    #     counts[x] = counts.get(x, 0) + 1
    
    return counts


# =============================================================================
# TEMPLATE 2: Grouping by Key
# =============================================================================
def grouping_template(items: List[Any], key_func) -> Dict[Any, List[Any]]:
    """
    Group items by a computed key.
    
    Example: Group words by sorted letters (anagram grouping)
    """
    groups = defaultdict(list)
    
    for item in items:
        key = key_func(item)
        groups[key].append(item)
    
    return dict(groups)


# Example: Group anagrams
def group_anagrams(strs: List[str]) -> List[List[str]]:
    """
    Group strings that are anagrams of each other.
    
    INVARIANT: After processing each string, all anagrams seen so far
    are in the same group (keyed by sorted characters).
    """
    groups = defaultdict(list)
    
    for s in strs:
        # Key = tuple of sorted characters (immutable, hashable)
        key = tuple(sorted(s))
        groups[key].append(s)
    
    return list(groups.values())


# =============================================================================
# TEMPLATE 3: Two-Sum / Complement Search
# =============================================================================
def two_sum_template(nums: List[int], target: int) -> Tuple[int, int]:
    """
    Find two indices whose values sum to target.
    
    INVARIANT: seen[x] stores the index where we saw value x.
    For each num, we check if (target - num) was seen before.
    """
    seen = {}  # value -> index
    
    for i, num in enumerate(nums):
        complement = target - num
        
        if complement in seen:
            return (seen[complement], i)
        
        seen[num] = i
    
    return (-1, -1)  # Not found


# =============================================================================
# TEMPLATE 4: Top-K by Frequency (with Counter)
# =============================================================================
def top_k_frequent_template(nums: List[int], k: int) -> List[int]:
    """
    Return the k most frequent elements.
    
    Uses Counter.most_common() - O(n log n) but simple.
    For O(n), use bucket sort (see heap template for heap approach).
    """
    counts = Counter(nums)
    
    # most_common returns [(element, count), ...] sorted by count desc
    return [elem for elem, count in counts.most_common(k)]


# =============================================================================
# EDGE CASES TO CHECK
# =============================================================================
"""
□ Empty array
□ Single element
□ All elements the same
□ All elements different
□ Negative numbers (if applicable)
□ Zero as a key/value
□ Case sensitivity for strings
□ Unicode/special characters
"""


# =============================================================================
# COMMON BUGS
# =============================================================================
"""
1. Using list as dict key (unhashable) -> use tuple(sorted(list))
2. Modifying dict while iterating -> iterate over list(dict.keys())
3. defaultdict vs regular dict -> defaultdict won't raise KeyError
4. Counter subtraction can have zero/negative counts -> use +counter to filter
"""

