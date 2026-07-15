# Claude Code adapter

Everything in the kit that is specific to running on **Claude Code** lives in this
directory. The core instruments (charter template, lint, skeptic brief, sample task,
queue) are harness-neutral and never reference this layer's mechanics; this README
is where the neutral rituals get their Claude Code wiring. Running a different
harness? Replace this directory with your own adapter — the core doesn't change.

## Installing

| File here | Where it goes | What it does |
|---|---|---|
| `vault-CLAUDE.md` | `CLAUDE.md` at the root of the folder your sessions work in (adapt the names and paths to your vault first) | Claude Code loads it automatically into every session — the standing operating file that teaches the rituals |
| `agents/goal-skeptic.md` | `.claude/agents/` in your working folder (or `~/.claude/agents/` for all projects) | The skeptic as a dispatchable agent, pinned to a cheap model (`haiku`). Wraps the kit's `instruments/skeptic-brief.md` — that file is the source of truth; keep them in sync |
| `agents/foundry-scout.md` | `.claude/agents/` | Single-pass, hard-capped research scout (pinned to `sonnet`) |
| `commands/think-tank.md` | `.claude/commands/` | `/think-tank` — budget-gated ideation over the workshop |

## The two rituals this adapter implements

- **"Dispatch a fresh independent agent"** (skeptic step): use the Agent/Task tool
  with the `goal-skeptic` agent — or a general agent given the skeptic brief — and
  ONLY the charter. **The dispatch receipt** the core ritual asks you to keep is the
  verbatim subagent tool result: in Claude Code it ends with an `agentId: …` line
  and a `<usage>` block with a `subagent_tokens` count. Save that whole result,
  unedited, as `skeptic-dispatch.log`. A receipt without those markers won't survive
  adjudication.
- **"Load a standing operating file"**: `CLAUDE.md` autoload, per the install table.

## Model routing (the economic rule, wired)

Judgment (charters, synthesis, adversarial review) stays on the session's top model;
mechanical fan-out and single-question research default to a mid-tier model
(`sonnet`); contract-driven checks (skeptics, lint-style passes) to the cheapest
(`haiku`). The agent files above carry these pins in their frontmatter.
