# AI Engineer Drills

Timed practice problems combining all core patterns.

---

## How to Practice

### The Cold Rep Method

1. **Set a timer** - strict time limit
2. **No references** - close all docs
3. **Type from scratch** - no copy-paste
4. **Run and verify** - tests must pass
5. **Review** - what was slow? what did you forget?

### Time Targets

| Drill Level | Time | Goal |
|-------------|------|------|
| Basic | 3-5 min | Single pattern |
| Intermediate | 10-15 min | Two patterns |
| Interview | 20-30 min | Full problem |

### Daily Practice Schedule

```
Day 1-3: Basic drills (5 min each)
Day 4-6: Intermediate drills (15 min each)  
Day 7+: Full interview problems (30 min)
```

---

## Drill Categories

### Level 1: Basic (3-5 minutes each)

| # | Drill | Pattern | Target Time |
|---|-------|---------|-------------|
| 1 | Adult Filter | Ingestion Loop | 3 min |
| 2 | Email Validator | Schema Validator | 3 min |
| 3 | Flaky Function | API Retry | 3 min |
| 4 | Hello FastAPI | FastAPI Basics | 5 min |

### Level 2: Intermediate (10-15 minutes each)

| # | Drill | Patterns | Target Time |
|---|-------|----------|-------------|
| 5 | JSONL Cleaner | Ingestion + Schema | 10 min |
| 6 | Resilient API | Schema + Retry | 10 min |
| 7 | FastAPI CRUD | FastAPI + Validation | 15 min |

### Level 3: Interview Simulation (20-30 minutes)

| # | Drill | Patterns | Target Time |
|---|-------|----------|-------------|
| 8 | Full Pipeline | All Core Patterns | 20 min |
| 9 | LLM Endpoint | FastAPI + All Patterns | 25 min |
| 10 | Production API | Everything | 30 min |

---

## Drill Checklist

Before starting each drill:
- [ ] Timer set
- [ ] No references open
- [ ] Editor ready (empty file)
- [ ] Understand the problem (read once, then start)

After each drill:
- [ ] Tests pass
- [ ] Code is clean
- [ ] Record your time
- [ ] Note what was slow

---

## Running the Drills

```bash
# Navigate to drills folder
cd aie/03_drills

# Run all drill tests
python -m pytest drill_problems.py -v

# Run specific drill
python -m pytest drill_problems.py::TestDrill01 -v

# Run just the drill file (shows self-test output)
python drill_problems.py
```

---

## Progress Tracking

Keep a log of your times:

```
Date       | Drill        | Time   | Notes
-----------|--------------|--------|------------------
2024-01-15 | Adult Filter | 4:30   | Forgot enumerate
2024-01-15 | Adult Filter | 3:10   | Clean
2024-01-16 | Email Valid  | 5:00   | Type checks slow
```

**Goal**: Each drill should get faster with practice. When you can do basic drills in under 3 minutes cold, you're ready.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forgetting `enumerate` | Always use for index tracking |
| Wrong error format | Match expected output exactly |
| Not handling empty input | Check at start of function |
| Returning wrong type | Read return type annotation |
| Off-by-one errors | Lines are 1-indexed, arrays are 0-indexed |
