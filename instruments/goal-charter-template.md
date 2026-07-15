---
type: goal-charter
status: draft   # draft → blocked → blessed → dispatched → done | aborted → debriefed
created: {{YYYY-MM-DD}}
working_title: {{short handle for this goal}}
blockers: []    # hoist every open Gate-A question / missing apparatus here — this is the "waiting on a human" surface
tags:
  - type/goal-charter
  - domain/goal-design
---

# Goal charter — {{working_title}}

> COPY THIS FILE, fill the sections top-to-bottom, delete this guidance block, then
> hand the finished charter to an executor (converge / subagent / workflow / by-hand).
> The charter is **provider-agnostic**: the goal object doesn't change when the executor
> does. Fill in order — each step constrains the next; the executor is picked LAST,
> after the goal survives the pre-flight. A malformed goal is free to fix here and
> ruinously expensive to discover after a run has burned through it.
>
> **Counter-signature principle (governs every gate below):** no gate is self-certified.
> Every gate names who — other than the drafter — checks it, and where their verdict is
> recorded. Every recursion bottoms out at a human signature.

## Vision · Goal · Grounding

Keep these three distinct. **Vision inspires · goal falsifies · grounding bridges.**
Vision points at *what grounding to gather*; grounding gives the goal *its teeth*; the
goal is the *falsifiable projection* of the vision.

- **Vision** — direction. Needn't be falsifiable. Sets the search space.
  > e.g. "Make coaching feel effortless for the athlete."
- **Goal** — the falsifiable *slice* of the vision you're building now (see step 2).
  > e.g. "A one-page weekly plan an athlete reads in under 60s and follows without asking."
- **Grounding** — the external truth that decides whether the goal is met (see step 3).
  > e.g. "Blessed corpus: the coach's 3 gold-standard plans + the readability rubric."

---

## 1. Intent — one sentence

Why this matters and what changes when it's done. No sentence → it's a mood, not a goal.
> e.g. "So the athlete acts on the plan same-day instead of DMing three clarifying questions."

## 2. Finish line — falsifiable, and runnable NOW

The checkable bar. Can a skeptic verify "done" **without trusting the builder**?

⚠ **FALSIFIABILITY GATE.** Name a bar a skeptic can *check* against something external —
a file, a test, a measurement, a tool output, a rubric. If you cannot, either
(a) narrow the goal until you can, or (b) mark the frontmatter `status: not-loopable`:
the goal may still be worth doing, but **converge and workflow are now invalid
executors** (step 8 is restricted to one-shot / by-hand) — a goal with no checkable bar
will spin or quietly get worse if looped. A confession without this consequence is a
warning label, not a gate.

⚠ **APPARATUS.** Falsifiable-in-principle ≠ falsifiable-now. Name **who runs the check,
with what, and whether that apparatus exists today** (test data, a test recipient, a
rubric file, a live environment). A check you can't run yet is a promissory note —
missing apparatus is either explicitly in scope to build, or a `blockers:` entry. It is
never fine print.

> e.g. "Handed the plan + the readability rubric, an independent reader confirms: fits
> one page, every session names its target, no undefined jargon — zero blocking gaps.
> Apparatus: rubric at <path> (exists); any fresh reader can run it in <10 min.
> *Note the accepted proxy gap: the vision is behavioral (reads in 60s, follows without
> asking); this bar checks textual proxies for it. The gap is named, not hidden.*"

## 3. Grounding — build it, don't just name it (sub-loop)

Grounding is not a one-liner you assert; it's a small refine loop you run FIRST.

⚠ **A wrong grounding is worse than none** — it launders bad correctness criteria with
false authority, and the builder rationalises against a reference that points the wrong
way. The verification gates below are what stop confident-but-wrong.

**Sub-loop:**
1. **Research** — from vision + seed references, gather the standards / prior art / data /
   references that define "correct" for this goal. The goal (step 2) bounds this search —
   only gather what bears on the finish line, or you research forever.
   > e.g. "Pulled: the coach's 3 exemplar plans, a plain-language rubric, 2 athlete quotes."
2. **Verify — TWO gates, both required:**
   - **Gate A · Blessed, with provenance** — the user reviews and approves the corpus
     (propose-and-wait). For EACH item record: *what makes it authoritative* (whose
     authority is being borrowed — an expert, a spec, measured data?) and *what was
     actually checked, how* — not just "approved." Where the user isn't competent to
     judge an item and no external authority is named, mark it **unverified**: the
     adversary may not treat it as ground truth.
     > e.g. "Coach (the domain authority) read all 3 exemplars against last season's
     > outcomes; dropped one stale plan. Rubric: borrowed from <source>, unreviewed —
     > marked unverified."
   - **Gate B · Checked against the goal** — does each item *bear on the finish line*, or
     is it decorative? Cut anything that doesn't discipline "done."
     > e.g. "Rubric + exemplars bear directly; the athlete quotes are colour — moved to vision."
3. **Blessed corpus** — what survives both gates. This is what the adversary tests against.
   > e.g. "Blessed grounding = 3 exemplar plans + readability rubric, at <path>."

## 4. Scope — what's OUT (deferrals by name)

Name what you are NOT building. Scope rot is the default failure of any capable executor;
an unnamed exclusion is an invitation to wander.
> e.g. "OUT: multi-week periodisation · nutrition · a UI · anything beyond the single page."

## 5. Constraints — non-negotiables

Invariants the executor must not violate regardless of how it reaches the finish line.
**Each constraint here must be covered by the pre-flight verdict (step 7) — name how each
is checked.** An unverified invariant is decoration: a run can hit the bar while silently
violating every one.
> e.g. "Markdown only · no external deps · keep the athlete's name/HR data untouched · one file."

## 6. Output spec — the artifact shape

The container. Underspecify and you get right content in the wrong form.
> e.g. "One `.md` file, <300 lines, frontmatter + these sections in this order, at <path>."

## 7. Pre-flight — falsify the GOAL ITSELF (before spending a token)

**Dispatch this — do not self-answer.** Hand the charter to a FRESH, context-free skeptic
(one subagent call, minutes) with ONLY this file — no drafting context. Require a
PASS/FAIL verdict per question with a named exploit, and **paste the verdict verbatim
below, attributed**. The drafter's job is to *obtain* the verdict, not author it — a
drafter grading its own goal is "rationalised done" one level up. (Self-answering is
legal only for throwaway goals; mark it prominently if so. Pointing a full converge pass
at the goal is the high-stakes graduation.)

The skeptic answers:

- **Can this be satisfied vacuously?**
- **Is the finish line actually checkable — and runnable now?** Who runs the check, with
  what, in how long? If the apparatus doesn't exist, FAIL.
- **Is the grounding real or decorative?** Does anything marked *unverified* carry weight
  it hasn't earned?
- **What's the laziest technically-compliant way to "meet" this?**
- **Are the constraints (step 5) checkable, and checked by whom?**
- **Is this ONE goal?** If the finish line has an "and" joining unlike checks, or step 8
  wants two executors, it's two charters — split.

> Verdict (verbatim, attributed): "..."

## 8. Executor — pick LAST

Only now, with the goal falsified, match mechanism to the goal's shape. Circle one and
say why.
- **one-shot** — a single agent pass nails it; no adversary needed.
- **converge** — needs generate→critique→converge against grounding to a checkable bar.
  *(Invalid if `not-loopable`.)*
- **workflow** — parallel fan-out / repeated structure across many items. *(Invalid if
  `not-loopable`.)*
- **delegate** — hand to a subagent with scope + context + output spec.
- **by-hand** — you build it; the charter is just the discipline.

⚠ **If you can't circle one, that's a finding, not a formality.** Needing two executors
means either phases of one arc (say so explicitly) or the goal is really two goals —
go back to step 2 and split the charter. Executor-refusal is a goal-fission detector.
> e.g. "converge — the finish line is checkable against a rubric and one pass won't get there."

## 9. Abort & escalate — read by the executor

The charter is a contract; this is its remedies clause. Mid-run discoveries that the
goal is wrong must have a channel — otherwise the executor's only options are to spin
or to silently rewrite the bar (Goodhart).

- **Kill conditions** — named assumptions that, if false, HALT the run and return to the
  principal. Start from the Gate-A answers and the apparatus.
  > e.g. "If the exemplar plans turn out mutually contradictory, stop — the grounding is wrong."
- **Budget** — hard cap (rounds / time / tokens). Hitting it = halt + report, not push on.
  > e.g. "Max 5 converge rounds."
- **Renegotiation clause** — if the finish line itself proves wrong or unreachable under
  the constraints, the executor halts and returns to the principal with evidence. **The
  executor never amends the bar unilaterally.**

## 10. Debrief — after execution (append-only; do not fill at draft time)

What makes the charter a learning instrument rather than paperwork — and what makes
"the template earned its keep" measurable. After the run, append:

- **Did the bar hold as written**, or did it need renegotiation mid-run? Verdict by whom?
- **Which charter-flagged risks/blockers materialized** — and did any catch here avert a
  mid-build failure? (Name the counterfactual cost.)
- **What did the charter miss** that the run surfaced?
- **Instruments used** — which foundry instruments (skills, templates, subagents,
  disciplines) the run used, and what the use revealed about each ("used, no findings"
  is a valid answer). Feeds evidence-gated amendments — see `dogfood-loop/THINK.md`.
- **Human counter-signature** — who accepted the artifact, and where it landed (step 6 path).

---

## Failure modes targeted (coverage unproven)

| Failure mode | What it looks like | Targeted by |
|---|---|---|
| **Vacuous satisfaction** | Met on a technicality; intent missed. | Step 1 intent + step 7 |
| **Goodhart** | The proxy gets optimised; the actual aim doesn't. | Step 2 gate + steps 7, 9 |
| **Rationalised done** | No external grounding, so the builder grades itself passing. | Step 3 sub-loop + counter-signature |
| **Scope creep** | No "what's out," so it wanders. | Step 4 deferrals |
| **Wrong artifact** | Right work, wrong form. | Step 6 output spec |
| **Spin-in-flight** | Goal proves wrong mid-run; executor pushes on or rewrites the bar. | Step 9 abort/renegotiate |
| **Compound goal** | Several goals stapled together; slices need different executors. | Step 7 one-goal check + step 8 fission detector |
| **Promissory bar** | Checkable in principle, no apparatus to check it now. | Step 2 apparatus + step 7 |

---

## Revision history (append-only)

- **v1 — 2026-07-01.** Initial build from THINK.md's 8-step process: vision·goal·grounding
  header, falsifiability gate, grounding sub-loop (two gates), self-answered pre-flight
  as step 8, executor as step 7, five-failure-mode table.
- **v2 — 2026-07-02.** After the three-stream audit (see THINK.md, "Audit + philosophy
  pass"): counter-signature principle added to the header; executor and pre-flight
  swapped so the executor is literally last; falsifiability-gate escape hatch given a
  structural consequence (`not-loopable` restricts executors); apparatus requirement on
  the finish line (falsifiable-now, not in-principle); Gate A records per-item provenance
  and what-was-checked, with an *unverified* downgrade; constraints wired into the
  pre-flight verdict; pre-flight is dispatched to a context-free skeptic by default, two
  questions added (constraints coverage, one-goal check); new step 9 Abort & escalate
  (kill conditions, budget, renegotiation clause); new step 10 Debrief (post-execution,
  append-only); status enum + `blockers:` hoisted into frontmatter; failure-mode table
  retitled and extended (spin-in-flight, compound goal, promissory bar).
- **v2.1 — 2026-07-03.** Step 10 gains the **instruments-used** question (the
  dogfooding standing rule: every run records what the instruments revealed about
  themselves). First real debrief to carry it was written hours before the rule
  was formalised.
