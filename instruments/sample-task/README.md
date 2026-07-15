# Sample task — linkcheck

Your first chartered build. The task is real, small, and mechanically checkable —
do it with the ritual in `START-HERE.md`, end to end: charter → lint → skeptic (with
the dispatch receipt) → build → verify → debrief.

## The task

Build **linkcheck**: a command-line tool that scans a folder of markdown files and
reports broken *relative* links.

**Spec:**

1. Invocation: `python3 linkcheck.py <folder>`.
2. Scans every `*.md` file under `<folder>` (recursive) for inline markdown links
   `[text](target)` — image links `![alt](target)` are checked the same way. Only
   **relative** targets are checked — any target with a URI scheme prefix
   (`http:`, `https:`, `mailto:`, `ftp:`, `tel:`, anything of the form `word:`)
   is skipped, as are `#`-only anchors. A target with an anchor suffix
   (`file.md#section`) is checked for the file part only.
3. A relative target resolves if the file or directory exists relative to the
   linking file's location.
4. Exit `0` when all relative links resolve.
5. Exit `1` when any link is broken; print one line per broken link:
   `<file>:<line>: <target>`, where `<file>` is the linking file's path relative
   to the scanned `<folder>`.
6. Exit `2` on usage error (missing/nonexistent folder argument).
7. Python stdlib only. One file. ≤ 200 lines.

## Acceptance — the checkable finish line for your charter

The `fixtures/` corpus is the spec's teeth (use it as your charter's grounding):

- `python3 linkcheck.py fixtures/clean` MUST exit `0`.
- `python3 linkcheck.py fixtures/broken` MUST exit `1`, reporting **exactly** the
  planted broken links in that corpus — every one of them, and nothing else. The
  corpus contains decoys (external links, mail links, anchored-but-valid links,
  valid relative links) that a sloppy implementation reports and a correct one
  doesn't. Read the fixtures; the corpus is the contract.

A tool that special-cases these fixture folders instead of implementing the spec is
the exact "lazy technically-compliant executor" your skeptic is briefed to catch —
expect it to.

## Deliverables (all beside each other, in your output folder)

- your filled goal charter (lint-clean, skeptic verdict pasted in step 7, debrief
  filled in step 10)
- `skeptic-dispatch.log` — the raw dispatch receipt (see the skeptic brief)
- `linkcheck.py`
