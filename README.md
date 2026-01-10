# FRS - Interview Sprint Platform

A 14-day interview preparation sprint platform for Data Scientists transitioning to MLE/AI Engineer roles.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start today's timed session
python -m cli.timer --day 1

# Run a full mock interview
python -m cli.mock

# Record your postmortem
python -m cli.postmortem

# View progress dashboard
python -m cli.progress
```

## Structure

```
frs/
├── cli/                    # CLI tools (timer, mocks, dashboard)
├── notebooks/
│   ├── tier_a/            # 7 pattern notebooks (6 algo + plumbing)
│   ├── tier_b/            # ML quickfire cards
│   └── tier_c/            # Architecture vocab
├── problems/              # Problem bank by pattern
├── solutions/             # Your work (gitignored)
├── logs/                  # Postmortems + session logs
├── templates/             # Code templates for each pattern
└── sprint/                # 14-day schedule with daily guides
```

## The 3-Tier Framework

### Tier A: Pass/Fail Gating (Must Automate)
- **Execution Protocol**: 2 min restate → 2 min tests → 15 min baseline → 5 min edges
- **6 Algorithm Patterns**: Hashmap, Two Pointers, Sorting, Heap, Binary Search, BFS/DFS
- **Data Plumbing**: parse → validate → normalize → aggregate → select → report

### Tier B: Role Credibility (60-second answers)
- Leakage vs overfitting
- ROC-AUC vs PR-AUC
- Calibration
- Class imbalance levers
- Slice-based error analysis

### Tier C: Narrative Breadth (Recognition-level)
- RAG/Agents architecture
- Observability
- Deployment patterns

## Daily Structure (90 minutes)

- **45 min**: Timed live-coding (one medium problem, no notes, talk aloud, tests first)
- **45 min**: Plumbing rep (one function from the 8-set)

## Stop Condition

You're ready when you can solve a medium in 30-35 minutes with:
- Correct code
- Tests passing
- Clear verbal walkthrough

## Two Stress Interrupts

1. **Freeze → Baseline**: "I will implement the simplest correct baseline first."
2. **Re-anchor Invariant**: "What must be true after each step? I'll state it, then code."

