# Day 8: Full Mock Interview #1

## Today's Goal
Simulate real interview conditions. This is a test, not practice.

---

## Pre-Mock Checklist
- [ ] Clear desk, phone away
- [ ] Timer ready (35-45 minutes)
- [ ] No notes, no looking things up
- [ ] Talk aloud as you solve

---

## Mock Session (45 min)

Run: `python -m cli.mock`

The CLI will:
1. Select a random medium problem
2. Start the timer
3. Prompt you at key intervals
4. Run tests when you submit

**Follow the execution protocol**:
- 0-2 min: Restate + pattern
- 2-4 min: Test cases
- 4 min: "Baseline first" prompt
- 10 min: "State your invariant" prompt
- 35-45 min: Time's up

---

## Post-Mock Review (30 min)

This is where learning happens.

### Immediate Debrief
1. Did you finish? With correct code?
2. What was your pattern recognition time?
3. Where did you get stuck?

### Detailed Postmortem
Run: `python -m cli.postmortem`

Fill out all 5 fields:
1. **Pattern used**: 
2. **Bug class**: 
3. **Fix rule**: 
4. **Micro-drill**: 
5. **Test case that would catch it**: 

### Identify Weak Spots
Look at your postmortem history:
- Most common bug class?
- Slowest pattern recognition?
- Missing edge cases?

**Tomorrow focuses on your weakest pattern.**

---

## Tomorrow Preview
Day 9-10: Remediation (patch your weakest pattern)


