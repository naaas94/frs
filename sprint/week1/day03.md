# Day 3: Binary Search Boundaries

## Today's Goal
Binary search finds WHERE a condition CHANGES, not exact matches. Drill the boundary-finding template.

---

## Warm-Up (5 min)

**Micro-drill from yesterday**: [Insert from postmortem]

Binary search template:
```python
def lower_bound(arr, target):
    """First position where arr[i] >= target."""
    left, right = 0, len(arr)
    while left < right:
        mid = left + (right - left) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left

# Key insight: We're finding the boundary where condition changes
# left of answer: condition is False
# right of answer: condition is True
```

---

## Timed Problem (45 min)

### Problem: Search in Rotated Sorted Array
`problems/binary_search/problem_01_search_rotated/`

**Invariant**: One half is ALWAYS sorted. Check if target is in sorted half, else search other half.

**Common bugs**:
- Infinite loop (left or right must move each iteration)
- Wrong comparison (`<` vs `<=`)
- Integer overflow (use `left + (right - left) // 2`)

---

## Plumbing Rep (45 min)

### Exercise: JSONL Aggregation (again)
Repeat yesterday's plumbing exercise but:
1. Time yourself
2. Try to do it faster than yesterday
3. Add a new feature: top-K slowest endpoints

---

## End of Day Postmortem
1. **Pattern used**: _______________
2. **Bug class**: _______________
3. **Fix rule**: _______________
4. **Micro-drill for tomorrow**: _______________
5. **Test case**: _______________

---

## Tomorrow Preview
Day 4: BFS/DFS Visited Template


