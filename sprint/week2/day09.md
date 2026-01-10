# Day 9: Patch Weakest Pattern

## Today's Goal
Targeted remediation. You identified your weakest pattern yesterday. Today we fix it.

---

## Review Your Postmortems

Run: `python -m cli.progress`

Look at:
- Pattern with lowest confidence
- Most frequent bug class
- Patterns that took longest to recognize

**Pick ONE pattern to focus on today.**

---

## Remediation Protocol

### Step 1: Re-read the Notebook (15 min)
Go back to `notebooks/tier_a/0X_[pattern].ipynb`

- Read the template out loud
- State the invariant out loud
- Trace through the example manually

### Step 2: Drill 2 Problems (60 min)

Pick 2 problems from your weak pattern:
- First: Easy/familiar (rebuild confidence)
- Second: Medium/new (stress test)

**Slower is fine today**. Focus on:
- Saying the invariant before coding
- Writing tests first
- Clean, correct code

### Step 3: Create Your Fix Rule (15 min)

Write one sentence that prevents your most common bug:

Examples:
- "Always check `left < right` vs `left <= right` based on search space definition"
- "Add to visited WHEN ENQUEUEING, not when popping"
- "Handle empty input before the main loop"

---

## End of Day

### Confidence Check
On a scale of 1-5, how automatic does this pattern feel now?

- 1-2: Need more drilling tomorrow
- 3: Getting there, one more day
- 4-5: Ready to move on

---

## Tomorrow Preview
Day 10: Continue remediation OR move to second weak pattern

