# AIE Sprint Hub

This is the centralized workspace for your current AIE sprint.

Use this folder as your single map for what to tackle next, in order.

## Start Here

1. Read `GATES.md` and pick your weakest gate.
2. Run one AIE mock from `mock_prompts/`.
3. Capture postmortem (`python -m cli.postmortem`).
4. Do one focused rep from `../03_drills/` or `../02_fastapi_fundamentals/`.
5. Repeat daily.

## Folder Map

- `GATES.md` - readiness checklist and weekly cadence
- `mock_prompts/` - AIE-focused mock interview prompts
- `agents_tools/` - hands-on ReAct/tool-router reps
- `devops_cloud.md` - cloud/deployment interview prep notes

## Daily Loop (60-90 min)

- 20-30 min: `python -m cli.mock --mode aie`
- 10 min: postmortem and next micro-drill
- 20-30 min: targeted coding rep in FastAPI or drills
- 10-20 min: verbal architecture/devops review

## Command Cheatsheet

```bash
# list AIE prompts
python -m cli.mock --mode aie --list-problems

# run one AIE mock
python -m cli.mock --mode aie --pattern fastapi_async

# run full drill suite
pytest aie/03_drills/drill_problems.py -v

# run agents lab
python aie/00_sprint_hub/agents_tools/react_loop.py
```
