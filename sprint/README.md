# 14-Day Interview Sprint

A structured, job-fast optimized sprint to prepare for MLE/AI Engineer technical interviews.

## Quick Start

```bash
# Start Day 1
python -m cli.timer --day 1

# View progress
python -m cli.progress

# Run a mock interview
python -m cli.mock
```

## Sprint Structure

### Week 1: Automate the Templates
| Day | Focus | Pattern |
|-----|-------|---------|
| 1 | [Hashmap Grouping](week1/day01.md) | Counter, defaultdict, two-sum |
| 2 | [Sorting by Key](week1/day02.md) | Custom keys, tie-breakers |
| 3 | [Binary Search](week1/day03.md) | Boundary finding |
| 4 | [BFS/DFS](week1/day04.md) | Visited template |
| 5 | [Mixed Problem](week1/day05.md) | Two pointers |
| 6 | Rest day | - |
| 7 | Weekend practice | 2 problems + plumbing |

### Week 2: Integrate + Mock
| Day | Focus | Type |
|-----|-------|------|
| 8 | [Mixed Algo](week2/day06.md) | 2 problems |
| 9 | [Mixed + Plumbing](week2/day07.md) | Algo + pipeline |
| 10 | [Full Mock #1](week2/day08.md) | 45 min timed |
| 11 | [Remediation](week2/day09.md) | Patch weak patterns |
| 12 | [Remediation](week2/day10.md) | Continue patching |
| 13 | [Full Mock #2](week2/day11.md) | 45 min timed |
| 14 | [Stabilization](week2/day12_14.md) | Repeat until automatic |

## Daily Time Commitment

- **Weekdays**: 90 minutes
  - 45 min timed coding
  - 45 min plumbing practice
- **Weekends**: 
  - 1 rest day
  - 1 practice day (90 min)

## Execution Protocol

Every timed session follows this structure:
1. **0-2 min**: Restate problem, identify pattern
2. **2-4 min**: Write test cases FIRST
3. **4 min**: Baseline prompt ("Simplest correct solution")
4. **4-19 min**: Implement baseline
5. **10 min**: Invariant prompt ("What must be true?")
6. **19-24 min**: Edge cases + cleanup

## Stress Interrupts

When stuck, use these two prompts:
1. **Freeze**: "I will implement the simplest correct baseline first."
2. **Confused**: "What must be true after each step? I'll state it, then code."

## Stop Condition

You're ready when:
- ✅ Medium solved in 30-35 minutes
- ✅ Correct code with passing tests
- ✅ Pattern recognition < 30 seconds
- ✅ Clean, readable implementation

## Files

- `schedule.yaml` - Machine-readable schedule
- `week1/` - Daily guides for Week 1
- `week2/` - Daily guides for Week 2

