# Day 1: Hashmap Grouping + Top-K

## Today's Goal
Internalize the hashmap pattern so deeply that you recognize it instantly and write it without thinking.

---

## Warm-Up (5 min)
Review the hashmap template from `notebooks/tier_a/01_hashmap_grouping.ipynb`:
```python
from collections import Counter, defaultdict

# Frequency counting
counts = Counter(arr)

# Grouping by key
groups = defaultdict(list)
for item in items:
    key = compute_key(item)
    groups[key].append(item)

# Two-sum pattern
seen = {}
for i, num in enumerate(nums):
    complement = target - num
    if complement in seen:
        return (seen[complement], i)
    seen[num] = i
```

---

## Timed Problem (45 min)

### Problem: Two Sum
`problems/hashmap/problem_01_two_sum/`

**Execution Protocol**:
- [ ] 0-2 min: Restate problem, pick pattern (hashmap - complement lookup)
- [ ] 2-4 min: Write 2-3 test cases first
- [ ] 4 min: **BASELINE PROMPT** - "Simplest correct solution first"
- [ ] 4-19 min: Implement baseline
- [ ] 10 min: **INVARIANT PROMPT** - "What's true after each step?"
- [ ] 19-24 min: Edge cases + cleanup

**Run tests**: `python -m pytest test_solution.py -v`

---

## Plumbing Rep (45 min)

### Exercise: JSONL Aggregation
`problems/plumbing/problem_01_jsonl_aggregation/`

Practice the universal pipeline:
```
parse → validate → normalize → aggregate → select → report
```

Focus on:
- [ ] Handling malformed JSON gracefully
- [ ] Collecting errors with line numbers
- [ ] Single-pass aggregation

---

## End of Day

### Postmortem (5 min)
Fill out after your timed session:

1. **Pattern used**: _______________
2. **Bug class**: _______________
3. **Fix rule**: _______________
4. **Micro-drill for tomorrow**: _______________
5. **Test case that would have caught it**: _______________

Run: `python -m cli.postmortem`

---

## Tomorrow Preview
Day 2: Sorting by Key + Tie-breakers (Merge Intervals)

