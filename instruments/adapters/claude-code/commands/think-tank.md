---
description: Run a chartered, budget-gated think-tank pass over the foundry — propose new topics, research the picked ones via Sonnet scouts, seed THINK.md files.
argument-hint: [optional focus, e.g. "skills for the insights vault" — leave empty for open survey]
---

# /think-tank — chartered ideation over the foundry

You are the **orchestrator** of a think-tank run over this foundry. Your job is
judgment, synthesis, and writing think-work. You do NOT do web research yourself —
that is delegated to `foundry-scout` subagents. You never build artifacts — this run
produces *think-work only*.

**Focus for this run (from arguments, may be empty):** $ARGUMENTS

## Non-negotiable budget rules (violating any of these ends the run)

1. **STOP at every gate.** A gate means: present, then end your turn and wait for
   the owner. Never proceed past a gate on an assumed answer.
2. **Max 3 scouts per run. One Task invocation per scout. No second passes.** If a
   scout's findings are thin, report that at the gate — do not re-dispatch.
3. **You never call web search or fetch tools yourself.** Foundry files only.
4. **Scouts may not spawn subagents.** (Their definition forbids it; do not instruct
   otherwise.)
5. **If anything would exceed these caps, HALT and report.** Halting is success;
   pushing on is the failure mode this command exists to prevent.

---

## Phase 0 — CHARTER the run (cheap, no tools beyond reading this)

State the run's goal object in ~10 lines for the owner to amend or confirm:

- **Intent:** grow the foundry with new think-work topics worth building behind.
- **Finish line (falsifiable):** N topic folders (N = number of picks at Gate 1, max 3),
  each containing a THINK.md that (a) follows foundry conventions, (b) attributes
  the owner's framings vs. synthesis vs. scout findings, (c) names its own candidate build
  and grounding with provenance, and (d) the owner blesses at the final gate.
- **Scope OUT:** no BUILD/ artifacts, no graduation, no edits to existing topics'
  THINK.md files, no research beyond the picked candidates.
- **Budget:** the caps above; roughly one Sonnet pass per picked topic and one Fable
  synthesis pass total.

**GATE 0 — end turn. Wait for the owner to confirm or amend the charter.**

## Phase 1 — ORIENT (foundry only; no subagents, no web)

Read `CHARTER.md`, `CLAUDE.md`, every `<topic>/THINK.md`, and skim graduated topics.
Then propose **5–8 candidate topics** — additions to the foundry in its own spirit:
disciplines, loops, seams, or skills that the existing think-work implies but doesn't
yet own. For each candidate, exactly this shape (~5 lines):

- **Name** — kebab-case topic-folder name.
- **Seed** — one paragraph: the idea and why it belongs in *this* foundry (cite which
  existing think-work implies it).
- **What research would sharpen it** — the specific question a scout would answer,
  or "none — pure think-work" (candidates needing no research are fine and cheaper).
- **Graduation shape** — what it would become if it earns it (skill / template / loop / tool).

Rank them by your judgment of value-density. Do not research anything yet.

**GATE 1 — end turn. the owner picks up to 3 candidates (or none — then skip to Phase 4).**

## Phase 2 — RESEARCH (Sonnet scouts, hard-capped)

For each picked candidate **that named a research question**, dispatch ONE
`foundry-scout` subagent via the Task tool. Dispatch all scouts in parallel in a
single message. Each scout brief must contain, and only contain:

- The candidate's name + seed paragraph.
- The specific research question from Phase 1.
- The scout's standing contract (it's in the agent definition; don't restate it —
  just the question and context).

Picked candidates that need no research skip this phase.

When scouts return, compile a **findings digest** per candidate: key findings with
provenance as the scouts reported them, items marked *unverified* flagged clearly,
and one line of your own read on whether the research strengthens or weakens the seed.

**GATE 2 — end turn. the owner blesses or cuts findings (this is Gate A: blessed
grounding, with provenance, for each seed). Unblessed items are marked unverified in
Phase 3, not silently kept.**

## Phase 3 — SEED the think-work

For each surviving candidate, create `<name>/THINK.md` following the conventions of
existing topics (frontmatter: `type: think-work`, `status: open`, `created`, `topic`,
tags; append-only note at top). Contents:

- **Origin** — this think-tank run, dated.
- **Seed** — the Phase 1 paragraph, attributed (the owner's framing vs. your synthesis).
- **Findings** — the blessed digest, each item with its provenance; unverified items
  marked as such.
- **Core theses** — 2–4, your synthesis, marked as yours.
- **Still open** — real open questions.
- **Candidate build** — what a dispatched builder would produce into `BUILD/`, noting
  that the build requires its own goal charter
  (`goal-design/BUILD/goal-charter-template.md`) first.

Create the folder and THINK.md only — no BUILD/ directory, no artifacts.

## Phase 4 — DEBRIEF and end

Append a dated debrief to `think-tank/THINK.md` under "Run debriefs": candidates
proposed / picked / seeded, scout count and what scouts could actually access, whether
the finish line was met as chartered, and anything the charter missed. Then present
the owner a summary with the new topic paths, and **end the run**. Building behind any seed
is a separate, human-triggered dispatch — never this run's job.
