"""
HEAP / PRIORITY QUEUE / TOP-K PATTERN
======================================

When to use:
- Find k largest/smallest elements
- Streaming data with running min/max
- Merge k sorted lists
- Task scheduling with priorities

Time: O(n log k) for top-k, O(log n) per push/pop
Space: O(k) for top-k heap
"""

import heapq
from typing import List, Tuple, Any, Optional
from collections import Counter


# =============================================================================
# CRITICAL: Python heapq is a MIN-HEAP
# =============================================================================
"""
heapq functions:
- heapq.heappush(heap, item)     # Add item, O(log n)
- heapq.heappop(heap)            # Remove and return smallest, O(log n)
- heapq.heapify(list)            # Transform list into heap in-place, O(n)
- heapq.nlargest(k, iterable)    # Return k largest, O(n log k)
- heapq.nsmallest(k, iterable)   # Return k smallest, O(n log k)
- heapq.heappushpop(heap, item)  # Push then pop, O(log n)

For MAX-HEAP: negate values when pushing, negate again when popping
"""


# =============================================================================
# TEMPLATE 1: Top-K Largest Elements
# =============================================================================
def top_k_largest_template(nums: List[int], k: int) -> List[int]:
    """
    Find k largest elements.
    
    Method 1: Use nlargest (simple, recommended for interviews)
    """
    return heapq.nlargest(k, nums)


def top_k_largest_heap(nums: List[int], k: int) -> List[int]:
    """
    Method 2: Maintain a MIN-heap of size k.
    
    INVARIANT: Heap contains the k largest elements seen so far.
    The smallest of those k is at the top (min-heap root).
    """
    if k <= 0:
        return []
    
    # Initialize with first k elements
    heap = nums[:k]
    heapq.heapify(heap)
    
    # For remaining elements, push if larger than smallest in heap
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)  # More efficient than pop + push
    
    return heap  # Note: not sorted


# =============================================================================
# TEMPLATE 2: Top-K Frequent Elements
# =============================================================================
def top_k_frequent_template(nums: List[int], k: int) -> List[int]:
    """
    Return k most frequent elements.
    
    Method 1: Counter.most_common (simple)
    """
    counts = Counter(nums)
    return [elem for elem, count in counts.most_common(k)]


def top_k_frequent_heap(nums: List[int], k: int) -> List[int]:
    """
    Method 2: Heap approach (useful when k << n)
    
    Use min-heap of size k, keyed by frequency.
    """
    counts = Counter(nums)
    
    # Heap of (count, element) - keeps k most frequent
    heap = []
    
    for elem, count in counts.items():
        if len(heap) < k:
            heapq.heappush(heap, (count, elem))
        elif count > heap[0][0]:
            heapq.heapreplace(heap, (count, elem))
    
    return [elem for count, elem in heap]


# =============================================================================
# TEMPLATE 3: Kth Largest Element
# =============================================================================
def kth_largest_template(nums: List[int], k: int) -> int:
    """
    Find the kth largest element (1-indexed: k=1 is the max).
    
    INVARIANT: Min-heap of size k. Root is the kth largest.
    """
    heap = []
    
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    
    return heap[0]


# =============================================================================
# TEMPLATE 4: Max-Heap (Negate Values)
# =============================================================================
def max_heap_template(nums: List[int]) -> int:
    """
    Get maximum element using min-heap.
    
    TRICK: Negate values to simulate max-heap.
    """
    # Convert to max-heap by negating
    max_heap = [-x for x in nums]
    heapq.heapify(max_heap)
    
    # Pop max (negate again to get original value)
    max_val = -heapq.heappop(max_heap)
    
    return max_val


# =============================================================================
# TEMPLATE 5: Merge K Sorted Lists
# =============================================================================
def merge_k_sorted_template(lists: List[List[int]]) -> List[int]:
    """
    Merge k sorted arrays into one sorted array.
    
    INVARIANT: Heap contains one element from each non-empty list.
    Always pop the smallest and add the next element from that list.
    """
    result = []
    
    # Heap of (value, list_index, element_index)
    heap = []
    
    # Initialize with first element of each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))
    
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        
        # If there's a next element in this list, add it
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
    
    return result


# =============================================================================
# TEMPLATE 6: Task Scheduler
# =============================================================================
def task_scheduler_template(tasks: List[str], n: int) -> int:
    """
    Schedule tasks with cooldown n between same tasks.
    Return minimum time to complete all tasks.
    
    GREEDY: Always schedule the most frequent remaining task.
    """
    counts = Counter(tasks)
    
    # Max-heap of remaining counts (negate for max-heap)
    max_heap = [-count for count in counts.values()]
    heapq.heapify(max_heap)
    
    time = 0
    
    while max_heap:
        cycle = []
        
        # Try to fill n+1 slots in this cycle
        for _ in range(n + 1):
            if max_heap:
                cycle.append(heapq.heappop(max_heap))
        
        # Decrement counts and re-add non-zero
        for count in cycle:
            if count + 1 < 0:  # Still has remaining tasks (remember: negated)
                heapq.heappush(max_heap, count + 1)
        
        # Time for this cycle: n+1 if more tasks remain, else actual tasks done
        if max_heap:
            time += n + 1
        else:
            time += len(cycle)
    
    return time


# =============================================================================
# TEMPLATE 7: Heap with Custom Objects
# =============================================================================
class Item:
    def __init__(self, priority: int, value: str):
        self.priority = priority
        self.value = value
    
    def __lt__(self, other):
        # Define comparison for heap ordering
        return self.priority < other.priority
    
    def __repr__(self):
        return f"Item({self.priority}, {self.value})"


def custom_object_heap_template():
    """
    Use custom objects in heap by implementing __lt__.
    """
    heap = []
    heapq.heappush(heap, Item(3, "low"))
    heapq.heappush(heap, Item(1, "high"))
    heapq.heappush(heap, Item(2, "medium"))
    
    while heap:
        item = heapq.heappop(heap)
        print(item)  # Pops in priority order: 1, 2, 3


# =============================================================================
# EDGE CASES TO CHECK
# =============================================================================
"""
□ Empty array
□ k = 0
□ k > len(array)
□ k = len(array)
□ All elements the same
□ Negative numbers
□ Duplicate elements with same frequency
"""


# =============================================================================
# COMMON BUGS
# =============================================================================
"""
1. Forgetting heapq is MIN-heap (not max)
2. Not negating for max-heap
3. Using heap[0] to peek without checking if empty
4. Off-by-one: kth largest (k=1 is max, not k=0)
5. heappush vs heapreplace semantics
6. Tuple comparison: compares element-by-element, ensure first element is sortable
"""

