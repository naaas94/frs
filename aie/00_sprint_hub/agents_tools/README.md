# Agents and Tools Lab

Hands-on practice for tool-calling agent fundamentals used in AIE interviews.

## What You Will Practice

- Parsing model actions safely
- Routing tool calls through an allowlist
- Feeding observations back to the model loop
- Enforcing max-iteration guardrails

## Run

```bash
python aie/00_sprint_hub/agents_tools/react_loop.py
```

## Suggested Reps

1. Add a new tool (`search_faq`) and update the parser tests.
2. Add a cost counter (`tokens` or `calls`) and stop early at budget.
3. Add retry for transient tool failures only.
4. Add structured trace output for each loop step.
