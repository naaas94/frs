# AIE Prep Roadmap

**Target role:** API- and product-focused AI Engineer — calling OpenAI/Anthropic (or similar), building RAG/agents, owning APIs and reliability.

This repo is your technical prep path. Follow the phases in order; use the sprint hub for daily focus.

---

## Phase 1: Foundations (Week 1)

**Goal:** Core patterns and FastAPI are automatic so you can build a small endpoint cold.

| Step | What | Where | Time |
|------|------|--------|------|
| 1.1 | Learn the 3 patterns (ingestion, schema validation, retry) | `01_core_patterns/` — read each file, type from memory | 2–3 days |
| 1.2 | Run every FastAPI example, modify and re-run | `02_fastapi_fundamentals/` (01 → 05, `uvicorn <file>:app --reload`) | 2–3 days |
| 1.3 | Cold rep: write each pattern from memory in &lt;3 min; build a validated POST endpoint in &lt;5 min | Same modules, timed, no references | Before Phase 2 |

**Check:** You pass **Gate 1** and **Gate 2** in `00_sprint_hub/GATES.md`.

---

## Phase 2: Drills and Mocks (Week 2)

**Goal:** Timed reps under interview conditions; find gaps via postmortems.

| Step | What | Where | Time |
|------|------|--------|------|
| 2.1 | Timed drills 05 → 08 (no refs), then 09–10 as full interview sim | `03_drills/drill_problems.py`, `pytest aie/03_drills/drill_problems.py -v` | ~10–15 min per drill |
| 2.2 | Core mocks (algo/plumbing) | `python -m cli.mock` | 35–45 min each |
| 2.3 | AIE mocks (API/design prompts) | `python -m cli.mock --mode aie` | 35–45 min each |
| 2.4 | After every mock: postmortem + next micro-drill | `python -m cli.postmortem` | 5–10 min |

**Check:** You pass **Gate 3** and **Gate 4** in `00_sprint_hub/GATES.md`.

---

## Phase 3: Sprint Hub — Ongoing

**Goal:** One place to decide “what to do today” and close remaining gates.

**Entry point:** `00_sprint_hub/README.md`

| Asset | Use |
|--------|-----|
| **GATES.md** | Readiness checklist; pick your weakest gate and drill it. |
| **mock_prompts/** | AIE mock prompts. List: `python -m cli.mock --mode aie --list-problems` |
| **agents_tools/** | ReAct/tool loop. Run: `python aie/00_sprint_hub/agents_tools/react_loop.py`. Add a tool, add a cost cap. |
| **devops_cloud.md** | Recognition-level deployment/observability. Read and answer the practice prompts out loud. |

**Check:** You pass **Gate 5** (agents/tools) and **Gate 6** (devops/cloud) in `00_sprint_hub/GATES.md`.

---

## Daily Loop (60–90 min)

Once in Phase 2–3, a typical day:

1. **20–30 min** — One mock: `python -m cli.mock` or `python -m cli.mock --mode aie`
2. **10 min** — Postmortem: `python -m cli.postmortem`
3. **20–30 min** — Focused rep: one gate (e.g. drills 05–08, or FastAPI variation)
4. **10–20 min** — Verbal review: one section of `00_sprint_hub/devops_cloud.md` or Tier C architecture

---

## Commands

```bash
# Mocks
python -m cli.mock                    # Core (algo/plumbing)
python -m cli.mock --mode aie         # AIE (API/design)
python -m cli.mock --mode aie --list-problems
python -m cli.mock --mode aie -p fastapi_async

# Postmortem
python -m cli.postmortem

# Drills
pytest aie/03_drills/drill_problems.py -v
pytest aie/03_drills/drill_problems.py::TestDrill05 -v

# Agents lab
python aie/00_sprint_hub/agents_tools/react_loop.py

# FastAPI (from repo root)
uvicorn aie.02_fastapi_fundamentals.01_hello_world:app --reload
```

---

## You’re Ready When

- All 6 gates in `00_sprint_hub/GATES.md` feel passable.
- You can do 3+ AIE mocks and 3+ core mocks with postmortems and fewer repeated mistakes.
- You can explain in &lt;60 sec: ReAct loop, health vs readiness, and one deployment tradeoff (e.g. Cloud Run vs Lambda).

Use **ROADMAP.md** (this file) as the sequence; use **00_sprint_hub/** as the daily map and checklist.
