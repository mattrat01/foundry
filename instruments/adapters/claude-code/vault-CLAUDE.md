# How to work this vault

> Adapt this file to your own vault, then install it as `CLAUDE.md` at the root of
> the folder your AI sessions work in — Claude Code loads it into every session
> automatically. Replace `<kit>` with wherever you placed the kit's `instruments/`,
> and the queue paths with wherever you run `parked.py`. This file is the standing
> memory that makes the rituals automatic instead of remembered.

Layer order on conflict: project file > this file > any global operating file.

## Spend models like capital

- **Expensive model time converts to durable text, or it's wasted.** Session answers
  are opex; charters, templates, and operating files are capex. On a top-tier model,
  bias hard toward capex.
- **Route by role when dispatching agents:** judgment (charters, theses, adversarial
  synthesis, instrument design) stays on the session's top model; mechanical
  execution, single-question research, and fan-out workers default to a mid-tier
  model; contract-driven checks (skeptics, format/lint passes) to the cheapest. If
  an entire requested task is mechanical, say so and recommend a cheaper model.
- **Close the capture loop before closing the work:** if the session produced
  reasoning or a decision that is not yet in a durable file a future session will
  load, write it to that file before moving on.

## Starting a session here

1. Read `PARKED.md` — what's waiting on the human. Regenerate with
   `python3 <kit>/parked.py`; if the script can't run, read the file as-is and note
   its `Generated:` date.
2. Working in a project subfolder? Read its README / operating file / charter first.
3. New kind of work → check the kit for an existing instrument before inventing one.

## The working method (the kit's instruments)

Nothing gets built until the layer above exists. In order:

| Move | Instrument |
|---|---|
| Frame a buildable goal | `<kit>/goal-charter-template.md` — falsifiable finish line + apparatus, grounding with provenance, executor picked last |
| Catch form defects free | `python3 <kit>/charter-lint/lint_charter.py <charter>` before dispatching anything |
| Falsify the goal before spending | dispatch a context-free skeptic with ONLY the charter (`<kit>/skeptic-brief.md`; the `goal-skeptic` agent in this adapter) — keep the dispatch receipt |
| After any run | debrief inside the artifact it governs, answering the instruments-used question |

## Hard lines (vault-wide)

- Fan-out is capped and declared before it runs; hitting a cap = halt and report —
  that is success, not failure.
- Irreversible, outward-facing, or budget-spending moves get a live human signature
  BEFORE they run. Reversible work proceeds on **debrief-veto**: do it, record it
  in the governing artifact's debrief, and file the pending veto as a `blockers:`
  frontmatter entry so it surfaces in PARKED.md — the human strikes it later, and a
  struck item gets reverted. A deferred gate that isn't in PARKED.md doesn't exist.
- Instrument amendments are evidence-gated: a change to any template, agent, or
  rule names the logged observation it responds to. "Felt slow" is an anecdote,
  not a finding.
