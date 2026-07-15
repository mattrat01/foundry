<p align="center">
  <img src="assets/logo.svg" width="120" alt="The Foundry logo — a crucible pouring a molten drop onto a cast bar">
</p>

<h1 align="center">The Foundry</h1>
<p align="center"><em>Thinking, poured into tools.</em></p>

<p align="center">
  <a href="https://the-foundry-nu.vercel.app"><strong>Visit the site →</strong></a>
</p>

---

The Foundry is a way of working with AI that fixes the three problems everyone hits
once the honeymoon ends:

1. **Great thinking evaporates.** A session sharpens ideas, makes decisions, designs
   solutions — then the chat ends and it's all gone. The next session starts from
   zero, and you pay again to rebuild what you already had.
2. **Vague goals burn budget.** Hand an AI an open-ended wish ("research some
   ideas?") and it will cheerfully consume your entire usage allowance being
   thorough about nothing.
3. **The expensive model does the grunt work.** Using a frontier model for
   mechanical legwork is paying an architect to carry bricks.

The Foundry's answer is old-fashioned: **a workshop with moulds.** In a real foundry
you don't carve every object by hand — you make the mould once, carefully, and pour
into it forever. Here, the mould is *durable written thinking*, and the pour is an
AI agent building from it.

## The shape

```
THINK ──────────▶ BUILD ──────────▶ GRADUATE
capture reasoning   an agent builds     proven tools promoted
as append-only      from the writing;   into everyday use —
files — the source  the written brief   skills, standing rules,
of truth            IS the instruction  live tools
```

Around that spine, five disciplines do the safeguarding:

| Discipline | What it prevents |
|---|---|
| **Goal charters** — every buildable goal gets a one-page contract with a finish line that *can fail* | Vague goals; work nobody can check |
| **Independent skeptics** — a fresh AI, given only the contract, attacks it before anything is built | Loopholes; goals a lazy builder could satisfy by cheating (a skeptic caught a real one on this repo's first build) |
| **The queue** — everything deferred to the human lands on one regenerated page with its unblock action | Decisions silently rotting while you're away |
| **Gate pricing** — human sign-off *before* the irreversible and the expensive; everything reversible proceeds and can be vetoed after | Both failure modes at once: bottlenecked-on-approvals *and* unsupervised recklessness |
| **Dogfooding with receipts** — every run records what the tools revealed about themselves; tools change only when a real run produced real evidence | Tool-fiddling; a workshop that never learns |

And one economic rule ties it together: **expensive model time converts to durable
text, or it's wasted.** Answers are opex; instruments, charters, and rulebooks are
capex. Judgment goes to the frontier model, legwork to mid-tier models, mechanical
checks to the cheapest — and everything the frontier model figures out lands in a
file that every future session (on any model) inherits automatically.

## New here? One door in.

**Read [`START-HERE.md`](START-HERE.md).** It teaches the one week-one ritual (the
chartered build: charter → lint → skeptic → build → verify → debrief), hands you a
sample task to prove it on today, and lists every other instrument with the trigger
that says when to adopt it. Everything below is the map, not the path.

## What's in this repo

```
START-HERE.md                       the entry door — week-one ritual, sample task,
                                    later-wave triggers. Read this first.
site/index.html                     the public site — the pitch, safeguards, worked
                                    example, and adoption path (live at
                                    the-foundry-nu.vercel.app)
instruments/                        the harness-neutral core
  goal-charter-template.md          the goal contract: vision/goal/grounding split,
                                    falsifiability gate, dispatched pre-flight,
                                    abort clauses, post-run debrief
  skeptic-brief.md                  the context-free skeptic's instructions +
                                    the dispatch-receipt rule (source of truth;
                                    the Claude Code agent wraps it)
  sample-task/                      your first chartered build: a small real task
                                    (linkcheck) with a planted-defect fixture
                                    corpus as its mechanically checkable bar
  charter-lint/                     deterministic form linter for goal charters —
                                    12 checks, each citing the template clause it
                                    implements, with a planted-defect fixture
                                    corpus; checks form only and says so on every
                                    report (the skeptic checks substance)
  parked.py                         the queue renderer — scans file frontmatter,
                                    writes the "waiting on you" page as markdown
                                    + a matching HTML view; "World (since date) —"
                                    blockers render as a separate "waiting on the
                                    world" queue; a parked.roots file beside the
                                    script opts extra directories into the scan
  frontmatter-contract.md           the written schema parked.py consumes —
                                    status enum, blockers list, and the full
                                    blocker-prefix taxonomy (NOD / SIGN / TEST /
                                    WAIT / DECIDE)
  adapters/                         everything harness-specific, one dir per
                                    harness — the swappable part
    claude-code/                    vault-CLAUDE.md operating file, agent
                                    definitions (goal-skeptic, foundry-scout),
                                    /think-tank command, install README
assets/logo.svg                     the mark: crucible, pour, cast bar
```

## Adopting it

You don't install the Foundry; you transplant its organs into your own vault.
`START-HERE.md` is the guided version of this; the shape of it:

1. **Week one is one ritual:** the chartered build, proven on the kit's sample
   task. Charter from the template, lint it
   (`python3 instruments/charter-lint/lint_charter.py <your-charter.md>` — form
   defects are free to catch), then dispatch a fresh agent with **only the
   charter** and `instruments/skeptic-brief.md` — and keep the dispatch receipt.
   The ten minutes it takes has paid for itself on every real run so far.
2. Wire your harness: copy `instruments/adapters/<your-harness>/` into place per
   its README (for Claude Code: the operating file at your working root, agents
   and commands under `.claude/`). Another harness? Write the equivalent adapter;
   the core never changes.
3. Later waves, on their triggers (see START-HERE): the `parked.py` queue when
   deferred decisions start rotting; append-only `THINK.md` topic folders when
   good reasoning starts evaporating; the scout and think-tank when research and
   ideation need caps.
4. Let your own usage feed amendments — but only with receipts: a change to any
   instrument must name the logged observation it responds to.

## Provenance

Designed and built by Matt Ratcliffe in his working vault, directing AI agents
end-to-end — with the system used on itself throughout its own construction: the
charter template chartered the queue tool; a skeptic attacked that charter and
found a real exploit before a line of code existed; and the queue's first
amendment came from its first real reader's complaint.

## License

MIT — see [LICENSE](LICENSE).
