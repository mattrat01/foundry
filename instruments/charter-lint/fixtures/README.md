# Fixtures — defect ⇄ clause table

Each `bad-*.md` file is identical to `good.md` except for exactly one planted defect.
Running `python3 ../lint_charter.py <fixture>` should exit 1 for every bad-* file and
exit 0 for `good.md`.

| Fixture | Check | Planted defect | Template section / contract line |
|---|---|---|---|
| `good.md` | — | (none — clean charter) | — |
| `bad-no-frontmatter.md` | C1 | No opening `---` YAML block | Template frontmatter block; frontmatter-contract.md §Fields |
| `bad-wrong-type.md` | C2 | `type: think-work` instead of `goal-charter` | Template frontmatter field `type: goal-charter` |
| `bad-invalid-status.md` | C3 | `status: in-progress` (not in enum) | Template frontmatter comment `draft→…→debriefed`; template step 2 `not-loopable` |
| `bad-created-not-iso.md` | C4 | `created: 1 June 2026` (not YYYY-MM-DD) | frontmatter-contract.md §Fields `created:` (ISO 8601 date) |
| `bad-blockers-scalar.md` | C5 | `blockers: "waiting on the owner"` (scalar, not list) | frontmatter-contract.md §Fields `blockers:` (list of strings) |
| `bad-missing-section.md` | C6 | `## 5. Constraints` section absent | Template v2.1 sections 1–10 + Vision·Goal·Grounding header |
| `bad-guidance-block.md` | C7 | `> COPY THIS FILE` blockquote not deleted | Template header blockquote "delete this guidance block" |
| `bad-placeholder.md` | C8 | `{{some-unfilled-placeholder}}` left in body | Template uses `{{...}}` as fill-in markers |
| `bad-two-executors.md` | C9 | Two bolded executors (**delegate** + **converge**) in section 8 | Template step 8 "Circle one" |
| `bad-pending-verdict.md` | C10 | Status `dispatched` but verdict line says "pending" | Template step 7 paste-verbatim; goal-charter finish line (b) |
| `bad-debriefed-empty-s10.md` | C11 | Status `debriefed` but section 10 body is empty | Template step 10 "append-only; do not fill at draft time" |
| `bad-not-loopable-converge.md` | C12 | Status `not-loopable` but section 8 circles **converge** | Template step 2 falsifiability gate / `not-loopable` consequence |
