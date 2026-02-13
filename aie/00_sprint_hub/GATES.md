# AIE Readiness Gates

Use this checklist to decide what to drill next and whether you are interview-ready for AI Engineer loops.

## Gate 1: Core Patterns (Cold)

- Write ingestion loop from memory in under 3 minutes.
- Write schema validator from memory in under 3 minutes.
- Write retry with exponential backoff from memory in under 3 minutes.
- Pass corresponding reps in `aie/01_core_patterns/`.

## Gate 2: FastAPI Execution

- Build a validated `POST` endpoint in under 5 minutes.
- Implement one custom error path with `HTTPException`.
- Explain path/query/body model flow clearly.
- Execute all modules in `aie/02_fastapi_fundamentals/`.

## Gate 3: AIE Drills

- Complete drills 05 to 08 in timed no-reference mode.
- Complete drills 09 and 10 as interview simulations.
- Keep a time/error log and show trend improvement.
- Pass tests in `aie/03_drills/drill_problems.py`.

## Gate 4: Mock Interview Performance

- Complete at least 3 core mocks (`python -m cli.mock`).
- Complete at least 3 AIE mocks (`python -m cli.mock --mode aie`).
- For each mock, record a postmortem and next-day micro-drill.
- Demonstrate faster pattern recognition and fewer repeated bug classes.

## Gate 5: Agents and Tools Literacy

- Explain ReAct loop (think -> act -> observe -> repeat) in 60 seconds.
- Implement or extend a minimal tool router.
- Describe safety controls: max iterations, tool allowlist, schema checks.
- Complete practice in `aie/00_sprint_hub/agents_tools/`.

## Gate 6: DevOps and Cloud Fundamentals

- Explain health checks, readiness, and liveness use cases.
- Describe baseline FastAPI containerization flow.
- Explain one deployment target (Cloud Run, ECS, or Lambda) with tradeoffs.
- Complete notes and prompts in `aie/00_sprint_hub/devops_cloud.md`.

## Weekly Review Cadence

- Monday: run one timed core mock + one AIE mock.
- Midweek: patch weakest gate with focused drills.
- Friday: rerun same gate under tighter time constraints.
- Weekend: one full mock and one architecture verbal review.
