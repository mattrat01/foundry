#!/usr/bin/env python3
"""
lint_charter.py — form linter for goal charters (foundry/goal-design v2.1)

Usage:  python3 lint_charter.py <charter.md>

Exit codes:
  0 — no errors (warnings may be printed)
  1 — one or more errors found
  2 — usage error (missing argument, unreadable file)

Checks form against two written contracts:
  • foundry/goal-design/BUILD/goal-charter-template.md  (structure)
  • foundry/parked-on-me/BUILD/frontmatter-contract.md  (metadata schema)

Refuses to check substance — see closing line on every report.
"""

import sys
import re

# Anti-Goodhart line — unconditional on every output path (charter constraint 4; finish line d)
ANTI_GOODHART = (
    "Form only. A green charter can still be a hollow goal"
    " — dispatch the skeptic (step 7) for substance."
)

# Status enum — template frontmatter comment: draft→blocked→blessed→dispatched→done|aborted→debriefed
# plus not-loopable (template step 2 falsifiability gate)
VALID_STATUSES = {"draft", "blocked", "blessed", "dispatched", "done", "aborted", "debriefed", "not-loopable"}

# Statuses "past blocked" requiring a non-pending step-7 verdict (check 10)
PAST_BLOCKED = {"blessed", "dispatched", "done", "aborted", "debriefed"}

# Required sections — template v2.1 sections 1–10 + Vision·Goal·Grounding header (check 6)
REQUIRED = [
    (r"^##\s+Vision\s+[·•]\s+Goal\s+[·•]\s+Grounding", "Vision · Goal · Grounding"),
    (r"^##\s+1\.\s+Intent",        "## 1. Intent"),
    (r"^##\s+2\.\s+Finish line",   "## 2. Finish line"),
    (r"^##\s+3\.\s+Grounding",     "## 3. Grounding"),
    (r"^##\s+4\.\s+Scope",         "## 4. Scope"),
    (r"^##\s+5\.\s+Constraints",   "## 5. Constraints"),
    (r"^##\s+6\.\s+Output spec",   "## 6. Output spec"),
    (r"^##\s+7\.\s+Pre-flight",    "## 7. Pre-flight"),
    (r"^##\s+8\.\s+Executor",      "## 8. Executor"),
    (r"^##\s+9\.\s+Abort",         "## 9. Abort"),
    (r"^##\s+10\.\s+Debrief",      "## 10. Debrief"),
]

# Template guidance block marker (check 7)
GUIDANCE_MARKER = "> COPY THIS FILE"

# Placeholder pattern — template uses {{...}} as fill-in markers (check 8)
PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")

# Executor names bolded in step 8 — template step 8 list (check 9)
EXECUTOR_NAMES = {"one-shot", "converge", "workflow", "delegate", "by-hand"}

# Looping executors forbidden when not-loopable (check 12; template step 2 gate)
LOOPING_EXECUTORS = {"converge", "workflow"}

NEXT_H2 = re.compile(r"^##\s")
BOLD_RE  = re.compile(r"\*\*([^*]+)\*\*")


def parse_frontmatter(lines):
    """Return (fm_dict, fm_end_index, error_str).
    Check 1 clause: template frontmatter block; frontmatter-contract.md §Fields.
    """
    if not lines or lines[0].rstrip() != "---":
        return {}, -1, "No opening '---' found at line 1 (frontmatter missing)"
    close = next((i for i, ln in enumerate(lines[1:], 1) if ln.rstrip() == "---"), None)
    if close is None:
        return {}, -1, "Frontmatter '---' block never closed"
    fm = {}
    for raw in "".join(lines[1:close]).splitlines():
        stripped = raw.split("#")[0].rstrip() if "#" in raw else raw.rstrip()
        if ":" in stripped:
            k, _, v = stripped.partition(":")
            k = k.strip()
            if k and not k.startswith(" "):
                fm[k] = v.strip()
    return fm, close, ""


def section_body(lines, pat):
    """Return body lines of the first section matching pat, up to the next ## heading."""
    re_obj = re.compile(pat, re.IGNORECASE)
    start = next((i for i, ln in enumerate(lines) if re_obj.match(ln.rstrip())), None)
    if start is None:
        return []
    body = []
    for ln in lines[start + 1:]:
        if NEXT_H2.match(ln):
            break
        body.append(ln)
    return body


def print_report(path, errors, warnings):
    if errors:
        print(f"ERRORS in {path}:")
        for e in errors:
            print(f"  {e}")
    else:
        print(f"OK: {path} — no form errors found.")
    if warnings:
        print("Warnings (non-blocking):")
        for w in warnings:
            print(f"  {w}")
    print(ANTI_GOODHART)


def lint(path):
    errors, warnings = [], []
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError as e:
        print(f"ERROR: Cannot read file: {e}", file=sys.stderr)
        print(ANTI_GOODHART, file=sys.stderr)
        return 2

    text = "".join(lines)

    # C1 — frontmatter parses (clause: template frontmatter block; frontmatter-contract.md §Fields)
    fm, fm_end, fm_err = parse_frontmatter(lines)
    if fm_err:
        errors.append(f"[C1] Frontmatter parse error: {fm_err}")
        print_report(path, errors, warnings)
        return 1

    # C2 — type: goal-charter (clause: template frontmatter field `type: goal-charter`)
    if fm.get("type") != "goal-charter":
        errors.append(f"[C2] `type: goal-charter` missing or wrong (got: {fm.get('type')!r})")

    # C3 — status in valid enum (clause: template frontmatter comment draft→…→debriefed; step 2 not-loopable)
    status = fm.get("status", "")
    if status not in VALID_STATUSES:
        errors.append(f"[C3] `status:` must be one of {sorted(VALID_STATUSES)}, got {status!r}")

    # C4 — created is ISO YYYY-MM-DD (clause: frontmatter-contract.md §Fields `created:`)
    created = fm.get("created", "")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", created):
        errors.append(f"[C4] `created:` must be an ISO YYYY-MM-DD date, got {created!r}")

    # C5 — blockers is a list not a scalar (clause: frontmatter-contract.md §Fields `blockers:` list)
    for ln in lines[1:fm_end]:
        s = ln.strip()
        if s.startswith("blockers:"):
            after = s[len("blockers:"):].split("#")[0].strip()
            if after and after not in ("[]",):
                errors.append("[C5] `blockers:` must be a list (use `[]` or `- item` lines), not a scalar")
            break

    # C6 — all ten numbered sections + Vision header present (clause: template v2.1 sections 1–10)
    for pat, label in REQUIRED:
        if not any(re.compile(pat, re.IGNORECASE).match(ln.rstrip()) for ln in lines):
            errors.append(f"[C6] Required section missing: '{label}'")

    # C7 — template guidance block deleted (clause: template header "> COPY THIS FILE … delete this guidance block")
    if GUIDANCE_MARKER in text:
        errors.append("[C7] Template guidance block not deleted (found '> COPY THIS FILE' blockquote)")

    # C8 — no {{placeholder}} survives (clause: template uses {{...}} as fill-in markers)
    placeholders = PLACEHOLDER_RE.findall(text)
    if placeholders:
        errors.append(f"[C8] Unfilled placeholder(s) found: {sorted(set(placeholders))}")

    # C9 — section 8 has exactly ONE executor circled (clause: template step 8 "Circle one")
    s8 = "".join(section_body(lines, r"^##\s+8\.\s+Executor"))
    picked = [b.strip().lower() for b in BOLD_RE.findall(s8) if b.strip().lower() in EXECUTOR_NAMES]
    if len(picked) == 0:
        errors.append(f"[C9] Section 8 (Executor) has no bolded executor name (expected one of: {sorted(EXECUTOR_NAMES)})")
    elif len(picked) >= 2:
        errors.append(f"[C9] Section 8 (Executor) has {len(picked)} bolded executor names ({picked}); exactly one required")

    # C10 — past-blocked status requires non-pending step-7 verdict
    # Clause: template step 7 "paste the verdict verbatim below, attributed"; goal-charter finish line (b)
    if status in PAST_BLOCKED:
        s7_lines = section_body(lines, r"^##\s+7\.\s+Pre-flight")
        verdict_lines = [ln for ln in s7_lines if "verdict" in ln.lower() and "verbatim" in ln.lower()]
        if not verdict_lines:
            errors.append(f"[C10] Status is '{status}' (past blocked) but no 'Verdict (verbatim, attributed' line in section 7")
        elif not any("pending" not in ln.lower() for ln in verdict_lines):
            errors.append(f"[C10] Status is '{status}' (past blocked) but all step-7 verdict lines still contain 'pending'")

    # C11 — debriefed requires non-empty section 10 (clause: template step 10 "append-only; do not fill at draft time")
    if status == "debriefed":
        body = section_body(lines, r"^##\s+10\.\s+Debrief")
        meaningful = [ln for ln in body if ln.strip() and ln.strip() != "---"]
        if not meaningful:
            errors.append("[C11] Status is 'debriefed' but section 10 (Debrief) is empty")

    # C12 — not-loopable forbids converge/workflow in step 8 (clause: template step 2 falsifiability gate)
    is_not_loopable = (status == "not-loopable") or bool(fm.get("not-loopable", ""))
    if is_not_loopable and picked:
        bad = [p for p in picked if p in LOOPING_EXECUTORS]
        if bad:
            errors.append(f"[C12] Charter is marked not-loopable but section 8 circles a looping executor: {bad}")

    # Optional warning: very short scope section (substance-adjacent; does not affect exit code)
    s4 = "".join(section_body(lines, r"^##\s+4\.\s+Scope")).strip()
    if s4 and len(s4) < 40:
        warnings.append("[W] Section 4 (Scope OUT) is very short — consider naming deferrals explicitly")

    print_report(path, errors, warnings)
    return 1 if errors else 0


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 lint_charter.py <charter.md>", file=sys.stderr)
        print(ANTI_GOODHART, file=sys.stderr)
        sys.exit(2)
    sys.exit(lint(sys.argv[1]))


if __name__ == "__main__":
    main()
