# charter-lint

Deterministic form linter for foundry goal charters (v2.1 template). stdlib only, read-only.

**Checks (12):** frontmatter parses · `type: goal-charter` · status enum · ISO `created` · `blockers` is a list · all 10 sections present · guidance block deleted · no `{{placeholders}}` · exactly one executor in step 8 · past-blocked status needs non-pending verdict · `debriefed` needs non-empty section 10 · `not-loopable` forbids looping executors.

**Refuses to check:** substance of any kind. The skeptic checks substance. Every report ends with a line saying so.

**Run:** `python3 lint_charter.py <charter.md>`

**Exit codes:** `0` = clean · `1` = errors · `2` = usage error

**Fixtures:** `fixtures/good.md` (exits 0) + one `bad-<defect>.md` per check (exits 1). `fixtures/README.md` maps each to its contract clause.

**Note for parked.py users:** fixtures carry deliberately live-looking frontmatter (planted defects). Add this folder to `parked.ignore` beside parked.py or they will pollute your queue — observed in the wild the day both instruments first met.
