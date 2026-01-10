# Day 5: Mixed Problem - Two Pointers

## Today's Goal
Practice pattern recognition under pressure. The problem won't tell you which pattern to use.

---

## Warm-Up (5 min)

**Micro-drill from yesterday**: [Insert from postmortem]

Two pointers template:
```python
# Opposite ends (sorted array or shrinking search space)
left, right = 0, len(arr) - 1
while left < right:
    if condition_met:
        return result
    elif need_larger:
        left += 1
    else:
        right -= 1

# Sliding window
left = 0
for right in range(len(s)):
    # Expand: add s[right] to window
    while not valid:
        # Shrink: remove s[left]
        left += 1
    # Update result
```

---

## Timed Problem (45 min)

### Problem: Container With Most Water
`problems/two_pointers/problem_01_container_water/`

**Pattern recognition hints**:
- "Two indices" → often two pointers
- "Maximize/minimize" with array → could be DP, greedy, or two pointers
- Here: move the shorter line because keeping it can't improve

**Invariant**: Optimal solution is either in [left, right] or already computed.

---

## Plumbing Rep (45 min)

### Exercise: CSV Validation (timed)
`problems/plumbing/problem_02_csv_validation/`

Set a 25-minute timer. Can you finish with clean code?

---

## Week 1 Reflection

Before the weekend:
1. Which pattern felt most automatic?
2. Which pattern still requires conscious thought?
3. What's your most common bug class?

**Focus next week on your weakest patterns.**

---

## End of Day Postmortem
1. **Pattern used**: _______________
2. **Bug class**: _______________
3. **Fix rule**: _______________
4. **Micro-drill for tomorrow**: _______________
5. **Test case**: _______________

---

## Weekend
- One day OFF (rest)
- One day: 2 timed problems + 1 plumbing rep

