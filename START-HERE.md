# Start here

You've been handed a working method, not a philosophy. This page is the whole
week-one curriculum: **one ritual, practiced once on a provided task.** Everything
else in the kit is a later wave — adopt it when its trigger fires, not before.

## The week-one ritual: the chartered build

Every non-trivial piece of work gets a one-page contract *before* anything is built,
and an independent attack on that contract *before* any effort is spent. That's the
kernel. It works like this, end to end:

1. **Charter it.** Copy `instruments/goal-charter-template.md` next to your work and
   fill it top-to-bottom. The template is the teacher — each section says what it
   wants and why. The two teeth: a **finish line that can fail** (a check someone
   can run) and **grounding** (the external truth the check runs against).
2. **Lint it.** `python3 instruments/charter-lint/lint_charter.py <your-charter.md>`
   until it exits clean. This catches form defects for free; it checks no substance
   and says so on every report.
3. **Skeptic it.** Dispatch a fresh, independent agent — one with none of your
   drafting context — giving it ONLY two things: `instruments/skeptic-brief.md` (its
   instructions) and your charter (its target). **Keep the receipt:** save the raw,
   unedited dispatch record your tooling returns — identity and usage metadata
   intact — as `skeptic-dispatch.log` beside the charter, and paste the verdict
   verbatim into the charter's step 7. A verdict you wrote yourself is worthless; a
   paraphrased one is a rewrite. MALFORMED → amend the charter and re-dispatch a
   fresh skeptic. This ten-minute step has paid for itself on every real run so far.
4. **Build to the charter.** The charter is the brief; scope not licensed by it
   doesn't get built.
5. **Verify against the finish line** — run the actual check the charter names,
   don't assert it.
6. **Debrief in the charter** (its step 10): did the bar hold, what did the charter
   miss, which kit instruments you used and what the use revealed. The debrief is
   what makes the next charter better.

## Prove it now — the sample task

`instruments/sample-task/` contains a small, real task with a mechanically checkable
spec. Your first chartered build is that task, today, with the ritual above. If any
step of this kit is unclear enough to stall you, **the kit is at fault** — note where
it lost you; that's a defect report, not a confession.

## Later waves — adopt when the trigger fires

| Instrument | Adopt when… |
|---|---|
| `instruments/parked.py` + `instruments/frontmatter-contract.md` — the "waiting on me" queue | decisions you deferred start silently rotting; run it over your working folder and wire it to session start once you trust it |
| Think-work folders (append-only `THINK.md` per topic; see README) | good session reasoning starts evaporating instead of compounding |
| `adapters/claude-code/agents/foundry-scout.md` — capped research scout | research questions start fanning out mid-build and eating your budget |
| `adapters/claude-code/commands/think-tank.md` — budget-gated ideation | you want structured ideation over the workshop itself |
| `adapters/claude-code/vault-CLAUDE.md` — the standing operating file | the rituals are habits and you want every session to inherit them automatically |

## The swappable part

Everything specific to a particular AI harness lives in `instruments/adapters/` —
one directory per harness (currently `claude-code/`, with its own README for
installation). Running something other than Claude Code? Replace that directory.
The rituals on this page don't change; only the wiring that implements "dispatch a
fresh independent agent" and "load a standing operating file" does.
