---
type: goal-charter
status: in-progress
created: 2026-06-01
working_title: test-fixture-bad-invalid-status
blockers: []
tags:
  - type/goal-charter
  - domain/tooling
---

# Goal charter — test-fixture-bad-invalid-status

Defect: `status` is `in-progress`, which is not in the valid enum.

## Vision · Goal · Grounding

- **Vision** — every push to the repo has a green badge.
- **Goal** — a CI script that runs the test suite and exits non-zero on failure.
- **Grounding** — the existing Makefile test target and the team's definition of done.

## 1. Intent — one sentence

So broken commits are caught before they reach main.

## 2. Finish line — falsifiable, and runnable NOW

Running `make test` exits 0 on green and 1 on failure. Apparatus: Makefile exists.

## 3. Grounding — blessed corpus

1. `Makefile` — checked: read this session.
Gate A: reviewed. Gate B: disciplines finish line.

## 4. Scope — what's OUT (deferrals by name)

- Integration tests beyond the unit suite

## 5. Constraints — non-negotiables

1. No new dependencies.

## 6. Output spec — the artifact shape

One `ci.sh` script at `scripts/ci.sh`.

## 7. Pre-flight — dispatched skeptic verdict

> Verdict (verbatim, attributed — goal-skeptic, 2026-06-01): "**SOUND.**"

## 8. Executor — pick LAST

**delegate** — one subagent pass.

## 9. Abort & escalate — read by the executor

- Kill conditions: if Makefile absent, halt.
- Budget: one pass.
- Renegotiation: halt with evidence.

## 10. Debrief — after execution (append-only; do not fill at draft time)

---

## Revision history (append-only)

- **v1 — 2026-06-01.** Fixture.
