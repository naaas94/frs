# Day 2: Sorting by Key + Tie-breakers

## Today's Goal
Master custom sorting with lambda keys and handle multi-field tie-breaking.

---

## Warm-Up (5 min)

**Micro-drill from yesterday**: [Insert from postmortem]

Review sorting template:
```python
# Multi-key sort: primary ASC, secondary DESC
sorted(items, key=lambda x: (x.start, -x.end))

# When you can't negate (strings):
from functools import cmp_to_key
def compare(a, b):
    if a != b:
        return a - b  # or string comparison
    return secondary_comparison
sorted(items, key=cmp_to_key(compare))
```

---

## Timed Problem (45 min)

### Problem: Merge Intervals
`problems/sorting/problem_01_merge_intervals/`

**Invariant to state**: After sorting by start, overlapping intervals are adjacent. Merge if `current.start <= last.end`.

**Execution Protocol**:
- [ ] 0-2 min: Restate, pattern = "sort + linear scan"
- [ ] 2-4 min: Test cases: empty, single, no overlap, all overlap, unsorted
- [ ] 4-19 min: Implement (sort → iterate → merge)
- [ ] 19-24 min: Edge cases

---

## Plumbing Rep (45 min)

### Exercise: CSV Validation
`problems/plumbing/problem_02_csv_validation/`

The pipeline for structured data:
1. Parse CSV rows
2. Validate: email format, numeric age, required fields
3. Collect valid rows + errors with line numbers
4. Return structured result

---

## End of Day

### Postmortem Template
1. **Pattern used**: _______________
2. **Bug class**: _______________
3. **Fix rule**: _______________
4. **Micro-drill for tomorrow**: _______________
5. **Test case**: _______________

---

## Tomorrow Preview
Day 3: Binary Search Boundaries

