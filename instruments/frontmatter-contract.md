# Frontmatter contract — parked.py

Authoritative schema for YAML frontmatter parked.py consumes. All consumers must
reference this doc, not convention-by-example.

## Fields

**`status:`** (string) — `open` (active think-work, no action needed) · `blocked`
(treated as blocked even if `blockers:` is empty) · `dispatched` / `done` / `aborted`
/ `active` (counted in "everything else"). Missing `status` and `type` → untracked.

**`blockers:`** (list of strings) — Each entry is one blocker. Non-empty list OR
`status: blocked` → item is blocked. Example:
```yaml
blockers:
  - "Debrief-veto — the owner: approve the dual-render approach"
  - "World (since 2026-06-26) — CGM screenshot covering a training day"
```

**`summary:`** (string, optional) — One-line explainer shown in renders. Wins over
the first-paragraph body fallback.

**`created:`** (ISO 8601 date, optional) — `YYYY-MM-DD`. Used to compute wait-age.

## Blocker-prefix taxonomy

Matched case-insensitively against the start of each blocker string. Priority order:

| Prefix | Kind | Label | Meaning |
|---|---|---|---|
| `Debrief-veto —` | nod | NOD | One-nod veto — strike it or it stands |
| `Gate —` | sign | SIGN | Needs a live signature before it runs |
| `Step N —` or `Accept` | test | TEST | Acceptance or real-world test |
| `World —` or `World (since YYYY-MM-DD) —` | wait | WAIT | Waiting on the world — no action from the owner |
| anything else | decide | DECIDE | Needs a decision from the owner |

**World blockers:** the optional `(since YYYY-MM-DD)` form gives the wait its own
age, computed from `since`; falls back to the file's `created:` date. An item whose
blockers are ALL WAIT renders in "Waiting on the world" (excluded from the
waiting-on-you count). An item with ≥1 non-WAIT blocker renders in "Waiting on you";
any WAIT blockers appear inline, tagged `[WAIT]`.

*Extend: add a row to the taxonomy table when a new prefix is adopted; bump this
doc in the same commit.*
