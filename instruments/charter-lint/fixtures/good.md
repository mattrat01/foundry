---
type: goal-charter
status: dispatched
created: 2026-06-01
working_title: test-fixture-good
blockers: []
tags:
  - type/goal-charter
  - domain/tooling
---

# Goal charter — test-fixture-good

## Vision · Goal · Grounding

- **Vision** — every push to the repo has a green badge.
- **Goal** — a CI script that runs the test suite and exits non-zero on failure.
- **Grounding** — the existing Makefile test target and the team's definition of done.

## 1. Intent — one sentence

So broken commits are caught before they reach main and the team stops debugging in production.

## 2. Finish line — falsifiable, and runnable NOW

Running `make test` in CI exits 0 on a green suite and 1 on any failure, verified by
injecting a known-failing test and observing exit 1.

Apparatus: the Makefile target exists today. A skeptic runs `make test` in under 5 minutes.

## 3. Grounding — blessed corpus

1. `Makefile` — the authoritative test target. Checked: read this session.
2. Team definition of done — reviewed and approved by the lead last sprint.

Gate A (blessed): items 1–2 reviewed by the tech lead; no unverified items.
Gate B (checked against goal): both items discipline the finish line directly.

## 4. Scope — what's OUT (deferrals by name)

- Integration tests beyond the unit suite
- Deployment pipeline changes
- Coverage thresholds

## 5. Constraints — non-negotiables

1. No new dependencies — stdlib tooling only.
2. Idempotent: running twice in a row produces the same result.

## 6. Output spec — the artifact shape

One `ci.sh` script, under 50 lines, at `scripts/ci.sh`.

## 7. Pre-flight — dispatched skeptic verdict

Dispatched to a context-free skeptic (cheap model, skeptic-brief contract).

> Verdict (verbatim, attributed — goal-skeptic, 2026-06-01): "**SOUND.** Finish line is
> falsifiable and runnable now. Apparatus exists. Grounding is real. No vacuous exploit
> found. Constraints are checkable. One goal."

## 8. Executor — pick LAST

**delegate** — one subagent pass with this charter as brief; the artifact is a small
shell script with a mechanically checkable bar.

## 9. Abort & escalate — read by the executor

- Kill conditions: if the Makefile target is absent or broken, halt and report.
- Budget: one builder pass.
- Renegotiation: if the bar proves wrong, halt with evidence; never amend unilaterally.

## 10. Debrief — after execution (append-only; do not fill at draft time)

---

## Revision history (append-only)

- **v1 — 2026-06-01.** Initial draft for fixture purposes.
