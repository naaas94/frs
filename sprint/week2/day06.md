# Day 6: Mixed Problems - Algo Heavy

## Today's Goal
Alternate between patterns. Build the muscle of quickly identifying which pattern applies.

---

## Session 1: Meeting Rooms II (45 min)

### Problem
`problems/sorting/problem_02_meeting_rooms/`

Find minimum number of conference rooms needed.

**Pattern recognition**:
- Intervals + "how many overlap at once" → Event sweep line
- Sort events (start: +1, end: -1), track running count

**Invariant**: At each event, `current_rooms` = number of meetings active.

---

## Session 2: Find Peak Element (45 min)

### Problem
`problems/binary_search/problem_02_find_peak/`

A peak is larger than its neighbors. Find any peak.

**Pattern recognition**:
- "Any peak" suggests O(log n) is possible
- Binary search: if mid < mid+1, peak is on right; else left

**Invariant**: A peak exists in [left, right]. We shrink toward higher values.

---

## End of Day

### Combined Postmortem
For each problem:
1. Pattern used
2. Time to recognize pattern
3. Bug (if any)
4. One thing to drill

---

## Tomorrow Preview
Day 7: Mixed with plumbing focus


