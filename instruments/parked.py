#!/usr/bin/env python3
# parked.py — scan foundry frontmatter and render a "parked on the owner" view
# Usage: python3 parked.py [foundry-root]   (defaults to two levels above this file)
# Output: foundry-root/PARKED.md + PARKED.html — regenerable; do not edit by hand
# Both render from one scan in one human-triggered run; the HTML cannot drift from the MD.
#
# Extra scan roots: place BUILD/parked.roots beside this script — one path per line
# (absolute or relative to the vault root, the parent of the foundry root).
# Lines beginning with # and blank lines are ignored.
# A path that does not exist renders as a visible warning in both outputs.

import html as html_mod
import re
import sys
from datetime import date
from pathlib import Path

TODAY = date.today()
FOUNDRY_ROOT = (
    Path(sys.argv[1]).resolve() if len(sys.argv) > 1
    else Path(__file__).resolve().parents[2]
)
VAULT_ROOT = FOUNDRY_ROOT.parent   # parent of the foundry root
RENDER_PATH = FOUNDRY_ROOT / "PARKED.md"
HTML_PATH = FOUNDRY_ROOT / "PARKED.html"
ROOTS_FILE = Path(__file__).resolve().parent / "parked.roots"
IGNORE_FILE = Path(__file__).resolve().parent / "parked.ignore"
EXPLAINER_MAX = 220
OWNER = "the owner"                     # adopters: change to your name
EDITOR_SCHEME = "vscode://file/"   # click-through target; path text stays visible regardless

# Blocker taxonomy — parsed from the prefix convention already in use in frontmatter.
# NOD = one-nod debrief-veto · SIGN = gate needing a live signature ·
# TEST = acceptance / real-world test · WAIT = waiting on the world (no action from the owner) ·
# DECIDE = anything unclassified.
BLOCKER_KINDS = [
    (re.compile(r"^debrief-veto\b", re.I), "nod", "NOD", "one-nod veto — strike it or it stands"),
    (re.compile(r"^gate\b", re.I), "sign", "SIGN", "needs your live signature before it runs"),
    (re.compile(r"^step\s*\d+\b|^accept", re.I), "test", "TEST", "acceptance or real-world test"),
    (re.compile(r"^world\b", re.I), "wait", "WAIT", "waiting on the world — no action from the owner"),
]
PREFIX_STRIP = re.compile(r"^(debrief-veto|gate|step\s*\d+|world(\s*\([^)]*\))?)\s*[—–:-]+\s*", re.I)

# Regex to extract the optional `since` date from a World blocker:
#   "World (since 2026-06-26) — …"  →  "2026-06-26"
WORLD_SINCE_RE = re.compile(r"^world\s*\(\s*since\s+(\d{4}-\d{2}-\d{2})\s*\)", re.I)


def blocker_kind(text):
    for rx, key, label, tip in BLOCKER_KINDS:
        if rx.match(text):
            return key, label, tip
    return "decide", "DECIDE", "needs a decision from you"


def is_world_blocker(text):
    """True iff this blocker is a world-wait (World — or World (since …) —)."""
    return bool(re.match(r"^world\b", text, re.I))


def world_since_date(text):
    """Extract the `since` date from a World blocker, or None."""
    m = WORLD_SINCE_RE.match(text)
    return m.group(1) if m else None


def parse_frontmatter(path):
    """Parse top YAML block only. Returns dict or None if absent/unclosed."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return None
    if not lines or lines[0].strip() != "---":
        return None
    close = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None)
    if close is None:
        return None
    fm, i, block = {}, 0, lines[1:close]
    while i < len(block):
        line = block[i]
        if ":" in line and not line[0] in (" ", "\t"):
            key, _, val = line.partition(":")
            key, val = key.strip(), val.strip().strip('"').strip("'")
            if " #" in val:
                val = val[:val.index(" #")].strip()
            j, items = i + 1, []
            while j < len(block) and block[j].startswith("  ") and block[j].lstrip().startswith("- "):
                items.append(block[j].strip()[2:].strip().strip('"').strip("'")); j += 1
            if items:
                fm[key] = items; i = j; continue
            if val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                fm[key] = [] if not inner else [x.strip().strip('"').strip("'") for x in inner.split(",")]
            else:
                fm[key] = val
        i += 1
    return fm


def explainer(path, fm):
    """One-line 'what is this' per item. `summary:` frontmatter wins;
    fallback is the first prose paragraph of the body, truncated."""
    s = fm.get("summary")
    if isinstance(s, str) and s.strip():
        return s.strip()
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return ""
    # skip past frontmatter
    start = 0
    if lines and lines[0].strip() == "---":
        close = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), None)
        if close is not None:
            start = close + 1
    para, in_comment, prev_blank = [], False, True
    for line in lines[start:]:
        t = line.strip()
        if in_comment:
            if "-->" in t:
                in_comment = False
            prev_blank = False
            continue
        if t.startswith("<!--"):
            if "-->" not in t:
                in_comment = True
            prev_blank = False
            continue
        if not t:
            if para:
                break
            prev_blank = True
            continue
        # not prose: headings, quotes, tables, rules, lists, code fences,
        # indented lines (wrapped list/quote continuations)
        if (t.startswith(("#", ">", "|", "---", "- ", "* ", "```"))
                or line[:1] in (" ", "\t")):
            if para:
                break
            prev_blank = False
            continue
        if not para and not prev_blank:
            # mid-block line following a skipped construct — a continuation, not a paragraph
            continue
        para.append(t)
        prev_blank = False
    text = " ".join(para).strip()
    if len(text) > EXPLAINER_MAX:
        cut = text[:EXPLAINER_MAX].rsplit(" ", 1)[0]
        text = cut + "…"
    return text


def age_days(created):
    try:
        return (TODAY - date.fromisoformat(created)).days
    except Exception:
        return None


def age(created):
    d = age_days(created)
    if d is None:
        return "age unknown"
    return "since today" if d == 0 else ("1 day" if d == 1 else f"{d} days")


def blockers_list(bl):
    if isinstance(bl, list):
        return [b for b in bl if b]
    return [bl] if isinstance(bl, str) and bl else []


def is_blocked(fm):
    return fm.get("status") == "blocked" or bool(blockers_list(fm.get("blockers", [])))


def load_extra_roots():
    """Read BUILD/parked.roots and return (roots, warnings).
    roots = list of resolved Path objects that exist.
    warnings = list of 'root not found: <path>' strings for missing paths.
    Returns ([], []) if the file is absent or empty — foundry-only behaviour."""
    if not ROOTS_FILE.exists():
        return [], []
    roots, warnings = [], []
    for raw in ROOTS_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        p = Path(line)
        if not p.is_absolute():
            p = VAULT_ROOT / p
        p = p.resolve()
        if p.exists():
            roots.append(p)
        else:
            warnings.append(f"root not found: {line}")
    return roots, warnings


def load_ignores():
    """Read BUILD/parked.ignore: vault-relative path prefixes or fnmatch globs,
    one per line, # comments. Files under a matching path are excluded from the
    scan entirely. Exists because test corpora (e.g. charter-lint fixtures) carry
    deliberately live-looking frontmatter that must never enter the queue —
    observed 2026-07-04 when a planted-defect fixture rendered as a 33-day wait."""
    if not IGNORE_FILE.exists():
        return []
    entries = []
    for raw in IGNORE_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.strip().rstrip("/")
        if line and not line.startswith("#"):
            entries.append(line)
    return entries


def is_ignored(md, ignores):
    from fnmatch import fnmatch
    try:
        vrel = str(md.resolve().relative_to(VAULT_ROOT))
    except ValueError:
        vrel = str(md)
    return any(vrel == pat or vrel.startswith(pat + "/") or fnmatch(vrel, pat)
               for pat in ignores)


def make_item(md, rel_label, fm):
    """Build the dict shared by blocked and world items."""
    return {
        "path": rel_label,
        "title": fm.get("working_title") or fm.get("topic") or rel_label,
        "created": fm.get("created", ""),
        "explainer": explainer(md, fm),
        "blockers": blockers_list(fm.get("blockers", [])),
    }


def scan_root(root, label_base, blocked_h, world_only, open_t, other, bad, skip_paths,
              ignores=()):
    """Scan one directory root and classify its .md files.
    blocked_h  — items with ≥1 human blocker (world blockers shown inline).
    world_only — items whose blockers are ALL world-waits.
    skip_paths — set of resolved paths already written (PARKED.md / PARKED.html).
    ignores    — parked.ignore entries; matching files never enter any bucket."""
    for md in sorted(root.rglob("*.md")):
        if md.resolve() in skip_paths:
            continue
        if ignores and is_ignored(md, ignores):
            continue
        # Relative label: try relative to FOUNDRY_ROOT first; fall back to vault-relative
        try:
            rel = str(md.relative_to(FOUNDRY_ROOT))
        except ValueError:
            try:
                rel = str(md.relative_to(VAULT_ROOT))
            except ValueError:
                rel = str(md)
        fm = parse_frontmatter(md)
        if fm is None:
            other["no-frontmatter"] = other.get("no-frontmatter", 0) + 1
            continue
        st = fm.get("status", "")
        if not isinstance(st, str):
            bad.append(rel); continue
        if not st and "type" not in fm:
            other["untracked"] = other.get("untracked", 0) + 1; continue
        if is_blocked(fm):
            item = make_item(md, rel, fm)
            bls = item["blockers"]
            human_blockers = [b for b in bls if not is_world_blocker(b)]
            if human_blockers:
                # ≥1 human blocker → "Waiting on you"; world blockers stay inline
                blocked_h.append(item)
            else:
                # ALL blockers are world-waits (or status:blocked with no blocker text)
                world_only.append(item)
        elif st == "open":
            open_t.append({"path": rel,
                           "topic": fm.get("topic") or fm.get("working_title") or rel,
                           "created": fm.get("created", ""),
                           "explainer": explainer(md, fm)})
        else:
            k = st or "unknown"
            other[k] = other.get(k, 0) + 1


def collect():
    """Scan foundry root + any extra roots declared in parked.roots.
    Returns (blocked_h, world_only, open_t, other, bad, warnings)."""
    blocked_h, world_only, open_t, other, bad = [], [], [], {}, []
    extra_roots, warnings = load_extra_roots()
    ignores = load_ignores()

    skip_paths = {RENDER_PATH.resolve(), HTML_PATH.resolve()}

    # Always scan the foundry root first
    scan_root(FOUNDRY_ROOT, None, blocked_h, world_only, open_t, other, bad, skip_paths,
              ignores)

    # Then scan each extra root (skipping anything already in the foundry tree)
    for root in extra_roots:
        scan_root(root, None, blocked_h, world_only, open_t, other, bad, skip_paths,
                  ignores)

    def sort_key(x):
        return date.fromisoformat(x["created"]) if x["created"] else date.max

    blocked_h.sort(key=sort_key)
    world_only.sort(key=sort_key)
    return blocked_h, world_only, open_t, other, bad, warnings


def world_wait_age(item):
    """Age string for a world-only item. Uses the earliest `since` date across
    all World blockers; falls back to the file's `created` date."""
    since_dates = []
    for b in item["blockers"]:
        sd = world_since_date(b)
        if sd:
            try:
                since_dates.append(date.fromisoformat(sd))
            except ValueError:
                pass
    if since_dates:
        return age(min(since_dates).isoformat())
    return age(item["created"])


def render(blocked_h, world_only, open_t, other, bad, warnings):
    # Summary line: include world count only when there are world items or warnings
    # (keeps output byte-identical to v1 when roots is absent and no World blockers exist)
    world_clause = (f" · {len(world_only)} waiting on the world" if (world_only or warnings) else "")
    L = ["<!-- generated by parked-on-me/BUILD — do not edit — re-run parked.py to refresh -->",
         f"<!-- Generated: {TODAY.isoformat()} -->", "",
         f"# Parked on {OWNER}", "",
         f"_{len(blocked_h)} waiting on you{world_clause} · {len(open_t)} open topics · generated {TODAY.isoformat()}_", ""]

    # ── Warnings ──────────────────────────────────────────────────────────────
    if warnings:
        L += ["## Warnings", ""]
        for w in warnings:
            L.append(f"- {w}")
        L.append("")

    # ── Waiting on you ────────────────────────────────────────────────────────
    L.append("## Waiting on you")
    L.append("")
    if blocked_h:
        for x in blocked_h:
            L.append(f"### {x['title']}  ·  waiting {age(x['created'])}")
            L.append("")
            if x["explainer"]:
                L.append(f"_{x['explainer']}_")
                L.append("")
            for b in (x["blockers"] or ["(marked blocked, but no blocker text — open the file)"]):
                kind_label = "[WAIT] " if is_world_blocker(b) else ""
                L.append(f"- [ ] {kind_label}{b}")
            L.append("")
            L.append(f"  <sub>`{x['path']}`</sub>")
            L.append("")
    else:
        L += ["Nothing — the queue is clear.", ""]

    # ── Waiting on the world (omitted entirely when empty — preserves v1 byte-identity) ──
    if world_only or warnings:
        L.append("## Waiting on the world")
        L.append("")
        if world_only:
            L.append(f"_{len(world_only)} item{'s' if len(world_only) != 1 else ''} stalled on an external event — "
                     f"no action from you until the world moves_")
            L.append("")
            for x in world_only:
                L.append(f"### {x['title']}  ·  waiting {world_wait_age(x)}")
                L.append("")
                if x["explainer"]:
                    L.append(f"_{x['explainer']}_")
                    L.append("")
                for b in (x["blockers"] or ["(marked blocked, but no blocker text — open the file)"]):
                    L.append(f"- [WAIT] {b}")
                L.append("")
                L.append(f"  <sub>`{x['path']}`</sub>")
                L.append("")
        else:
            L += ["_None — nothing stalled on the world right now._", ""]

    # ── Open think-work ───────────────────────────────────────────────────────
    L += ["## Open think-work (no action needed)", ""]
    if open_t:
        for x in open_t:
            tail = f" — {x['explainer']}" if x["explainer"] else ""
            L.append(f"- **{x['topic']}** — open {age(x['created'])}{tail}")
    else:
        L.append("_None._")
    L += ["", "## Everything else", ""]
    if other:
        parts = ", ".join(f"{v} {k}" for k, v in sorted(other.items()))
        L.append(f"{sum(other.values())} files, none needing you: {parts}")
    else:
        L.append("_None._")
    L.append("")
    if bad:
        L += ["## Unparseable frontmatter", ""] + [f"- `{p}`" for p in bad] + [""]
    return "\n".join(L) + "\n"


HTML_CSS = """
  :root{
    --iron:#211F1C; --soot:#2B2823; --paper:#EFEAE1; --paper2:#E6E0D3;
    --ink:#2A241B; --ink-soft:#5A5142; --ember:#D96A28; --ember-hot:#F0913F;
    --brass:#8A6D3B; --line:#CDC4B0; --line-dark:#453F36; --paper-on-dark:#EDE7DA;
    --cold:#8B8D91; --sky:#3B6E8A; --sky-soft:#C8DDE8;
  }
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:var(--paper);color:var(--ink);
       font-family:"Source Sans 3",system-ui,sans-serif;font-size:1rem;line-height:1.55}
  ::selection{background:var(--ember);color:#fff}
  a{color:inherit;text-decoration:none}
  a:hover,a:focus-visible{color:var(--ember)}
  :focus-visible{outline:2px solid var(--ember);outline-offset:2px}
  .mono{font-family:"IBM Plex Mono",monospace}
  header{background:var(--iron);color:var(--paper-on-dark);padding:2.4rem 0 1.6rem}
  .wrap{max-width:46rem;margin:0 auto;padding:0 1.3rem}
  .eyebrow{font-family:"IBM Plex Mono",monospace;font-size:.7rem;letter-spacing:.18em;
           text-transform:uppercase;color:var(--ember-hot)}
  h1{font-family:"Zilla Slab",serif;font-weight:700;font-size:clamp(1.9rem,5vw,2.6rem);
     letter-spacing:-.01em;margin:.35rem 0 .3rem}
  .counts{color:#CFC8B9;font-size:.98rem}
  .counts strong{color:var(--paper-on-dark)}
  .chips{display:flex;gap:.55rem;flex-wrap:wrap;margin-top:1.3rem}
  .chip{font-family:"IBM Plex Mono",monospace;font-size:.72rem;letter-spacing:.08em;
        text-transform:uppercase;padding:.42rem .8rem;border:1px solid var(--line-dark);
        background:var(--soot);color:#C9C2B3;cursor:pointer}
  .chip .n{color:var(--ember-hot);margin-left:.35rem}
  .chip:hover{border-color:var(--ember)}
  .chip[aria-pressed="true"]{background:var(--ember);border-color:var(--ember);color:#fff}
  .chip[aria-pressed="true"] .n{color:#fff}
  main{padding:2rem 0 3.5rem}
  h2{font-family:"IBM Plex Mono",monospace;font-size:.72rem;letter-spacing:.16em;
     text-transform:uppercase;font-weight:500;color:var(--brass);margin:2.4rem 0 1rem}
  h2:first-child{margin-top:0}
  .card{background:var(--paper2);border:1px solid var(--line);border-left:3px solid var(--line);
        padding:1.1rem 1.25rem 1rem;margin-bottom:1rem}
  .card.hot{border-left-color:var(--ember-hot)}
  .card.cooling{border-left-color:var(--brass)}
  .card.cold{border-left-color:var(--cold)}
  .card.world-card{border-left-color:var(--sky)}
  .card h3{font-family:"Zilla Slab",serif;font-weight:600;font-size:1.2rem;line-height:1.25}
  .card h3 a:hover{color:var(--ember)}
  .heat{font-family:"IBM Plex Mono",monospace;font-size:.7rem;letter-spacing:.06em;
        white-space:nowrap;margin-left:.6rem;vertical-align:2px}
  .heat::before{content:"●";margin-right:.35rem}
  .hot .heat{color:var(--ember)}
  .cooling .heat{color:var(--brass)}
  .cold .heat{color:var(--cold)}
  .world-card .heat{color:var(--sky)}
  .explainer{color:var(--ink-soft);font-size:.93rem;margin:.35rem 0 .7rem;max-width:38rem}
  ul.blockers{list-style:none;margin:.2rem 0 .65rem}
  ul.blockers li{display:flex;gap:.7rem;align-items:baseline;padding:.4rem 0;
                 border-top:1px solid var(--line);font-size:.94rem}
  ul.blockers li:first-child{border-top:none}
  .k{font-family:"IBM Plex Mono",monospace;font-size:.62rem;letter-spacing:.1em;
     padding:.14rem .45rem;flex:none;cursor:default}
  .k-nod{background:var(--ember);color:#fff}
  .k-sign{background:var(--iron);color:var(--ember-hot)}
  .k-test{background:transparent;color:var(--brass);box-shadow:inset 0 0 0 1px var(--brass)}
  .k-decide{background:transparent;color:var(--ink-soft);box-shadow:inset 0 0 0 1px var(--line)}
  .k-wait{background:var(--sky);color:#fff}
  .path{font-family:"IBM Plex Mono",monospace;font-size:.75rem;color:var(--ink-soft);
        word-break:break-all}
  .path a:hover{color:var(--ember)}
  .clear{font-family:"Zilla Slab",serif;font-size:1.3rem;color:var(--ink-soft)}
  .world-intro{color:var(--ink-soft);font-size:.93rem;margin:.5rem 0 1rem;font-style:italic}
  details{border:1px solid var(--line);background:var(--paper2)}
  summary{cursor:pointer;padding:.85rem 1.25rem;font-family:"IBM Plex Mono",monospace;
          font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--brass);
          list-style:none}
  summary::-webkit-details-marker{display:none}
  summary::before{content:"▸";margin-right:.6rem;display:inline-block;transition:transform .15s}
  details[open] summary::before{transform:rotate(90deg)}
  @media (prefers-reduced-motion:reduce){summary::before{transition:none}}
  ul.open{list-style:none;padding:0 1.25rem 1rem}
  ul.open li{padding:.55rem 0;border-top:1px solid var(--line);font-size:.94rem}
  ul.open .topic{font-family:"Zilla Slab",serif;font-weight:600;font-size:1.02rem}
  ul.open .age{font-family:"IBM Plex Mono",monospace;font-size:.72rem;color:var(--ink-soft);
               margin-left:.5rem}
  ul.open .explainer{margin:.15rem 0 0}
  .rest{color:var(--ink-soft);font-size:.9rem}
  .warnings{background:#FFF8E7;border:1px solid var(--brass);padding:.75rem 1rem;
            margin-bottom:1.5rem;font-size:.88rem;color:var(--ink-soft)}
  .warnings p{font-family:"IBM Plex Mono",monospace;font-size:.78rem;margin:.3rem 0 0}
  footer{border-top:1px solid var(--line);margin-top:2.6rem;padding-top:1rem;
         color:var(--ink-soft);font-size:.82rem}
  footer .mono{font-size:.75rem}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Zilla+Slab:wght@600;700'
         '&family=Source+Sans+3:ital,wght@0,400;0,600;1,400'
         '&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">')

FILTER_JS = """
document.querySelectorAll('.chip').forEach(function(chip){
  chip.addEventListener('click', function(){
    var kind = chip.dataset.kind;
    document.querySelectorAll('.chip').forEach(function(c){
      c.setAttribute('aria-pressed', c === chip ? 'true' : 'false');
    });
    document.querySelectorAll('ul.blockers li').forEach(function(li){
      li.hidden = kind !== 'all' && li.dataset.kind !== kind;
    });
    document.querySelectorAll('.card:not(.world-card)').forEach(function(card){
      card.hidden = kind !== 'all' &&
        !card.querySelector('ul.blockers li[data-kind="' + kind + '"]');
    });
  });
});
"""


def heat_class(created):
    d = age_days(created)
    if d is None or d <= 1:
        return "hot"
    return "cooling" if d <= 3 else "cold"

HEAT_WORD = {"hot": "still hot", "cooling": "cooling", "cold": "gone cold"}


def editor_href(rel_path):
    # rel_path may be relative to foundry or to vault root — resolve via FOUNDRY_ROOT first,
    # fall back to VAULT_ROOT if the foundry-relative path doesn't exist.
    p = FOUNDRY_ROOT / rel_path
    if not p.exists():
        p = VAULT_ROOT / rel_path
    return EDITOR_SCHEME + str(p)


def render_html(blocked_h, world_only, open_t, other, bad, warnings):
    e = html_mod.escape

    # Count kinds only from human-blocked items (WAIT chips only if inline in "Waiting on you")
    kind_counts = {}
    for x in blocked_h:
        for b in x["blockers"]:
            k = blocker_kind(b)[0]
            kind_counts[k] = kind_counts.get(k, 0) + 1
    total_blockers = sum(kind_counts.values())
    oldest = max((d for x in blocked_h if (d := age_days(x["created"])) is not None), default=None)

    P = ["<!doctype html>", '<html lang="en"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1">',
         "<!-- generated by parked-on-me/BUILD — do not edit — re-run parked.py to refresh -->",
         f"<title>Parked on {e(OWNER)}</title>", FONTS,
         f"<style>{HTML_CSS}</style></head><body>",
         '<header><div class="wrap">',
         '<p class="eyebrow">The Foundry &middot; queue</p>',
         f"<h1>Parked on {e(OWNER)}</h1>"]
    if blocked_h:
        oldest_txt = "" if oldest is None else (
            " · oldest still hot" if oldest <= 1 else f" · oldest waiting {oldest} days")
        P.append(f'<p class="counts"><strong>{len(blocked_h)}</strong> item{"s" if len(blocked_h) != 1 else ""} '
                 f'waiting on you — <strong>{total_blockers}</strong> unblocks{e(oldest_txt)}</p>')
        chips = [("all", "All", total_blockers)]
        for key, label, _tip in [("nod", "Nods", None), ("sign", "Signatures", None),
                                 ("test", "Tests", None), ("decide", "Decisions", None),
                                 ("wait", "World waits", None)]:
            if kind_counts.get(key):
                chips.append((key, label, kind_counts[key]))
        P.append('<div class="chips" role="group" aria-label="Filter by unblock type">')
        for key, label, n in chips:
            pressed = "true" if key == "all" else "false"
            P.append(f'<button class="chip" data-kind="{key}" aria-pressed="{pressed}">'
                     f'{label}<span class="n">{n}</span></button>')
        P.append("</div>")
    else:
        world_count_txt = (f" · <strong>{len(world_only)}</strong> waiting on the world"
                           if world_only else "")
        P.append(f'<p class="counts">Nothing waiting on you.{world_count_txt}</p>')
    P.append("</div></header>")

    P.append('<main><div class="wrap">')

    # ── Warnings ──────────────────────────────────────────────────────────────
    if warnings:
        P.append('<div class="warnings"><strong>Warnings</strong>')
        for w in warnings:
            P.append(f'<p>{e(w)}</p>')
        P.append("</div>")

    # ── Waiting on you ────────────────────────────────────────────────────────
    P.append("<h2>Waiting on you</h2>")
    if blocked_h:
        for x in blocked_h:
            heat = heat_class(x["created"])
            P.append(f'<section class="card {heat}">')
            P.append(f'<h3><a href="{e(editor_href(x["path"]))}">{e(x["title"])}</a>'
                     f'<span class="heat">{e(age(x["created"]))} · {HEAT_WORD[heat]}</span></h3>')
            if x["explainer"]:
                P.append(f'<p class="explainer">{e(x["explainer"])}</p>')
            P.append('<ul class="blockers">')
            for b in (x["blockers"] or ["(marked blocked, but no blocker text — open the file)"]):
                key, label, tip = blocker_kind(b)
                shown = PREFIX_STRIP.sub("", b) or b
                P.append(f'<li data-kind="{key}"><span class="k k-{key}" title="{e(tip)}">{label}</span>'
                         f"<span>{e(shown)}</span></li>")
            P.append("</ul>")
            P.append(f'<p class="path"><a href="{e(editor_href(x["path"]))}">{e(x["path"])}</a></p>')
            P.append("</section>")
    else:
        P.append('<p class="clear">The queue is clear. Nothing cooling, nothing cold.</p>')

    # ── Waiting on the world (omitted entirely when empty — preserves v1 byte-identity) ──
    if world_only or warnings:
        P.append("<h2>Waiting on the world</h2>")
        if world_only:
            P.append(f'<p class="world-intro">{len(world_only)} item{"s" if len(world_only) != 1 else ""} '
                     f'stalled on an external event — no action from you until the world moves.</p>')
            for x in world_only:
                wait_age = world_wait_age(x)
                P.append('<section class="card world-card">')
                P.append(f'<h3><a href="{e(editor_href(x["path"]))}">{e(x["title"])}</a>'
                         f'<span class="heat">{e(wait_age)}</span></h3>')
                if x["explainer"]:
                    P.append(f'<p class="explainer">{e(x["explainer"])}</p>')
                P.append('<ul class="blockers">')
                for b in (x["blockers"] or ["(marked blocked, but no blocker text — open the file)"]):
                    key, label, tip = blocker_kind(b)
                    shown = PREFIX_STRIP.sub("", b) or b
                    P.append(f'<li data-kind="{key}"><span class="k k-{key}" title="{e(tip)}">{label}</span>'
                             f"<span>{e(shown)}</span></li>")
                P.append("</ul>")
                P.append(f'<p class="path"><a href="{e(editor_href(x["path"]))}">{e(x["path"])}</a></p>')
                P.append("</section>")
        else:
            P.append('<p class="rest">Nothing stalled on the world right now.</p>')

    # ── Also in the shop ──────────────────────────────────────────────────────
    P.append("<h2>Also in the shop</h2>")
    if open_t:
        P.append(f"<details><summary>Open think-work — {len(open_t)} topic"
                 f'{"s" if len(open_t) != 1 else ""}, no action needed</summary>')
        P.append('<ul class="open">')
        for x in open_t:
            P.append(f'<li><a href="{e(editor_href(x["path"]))}"><span class="topic">{e(x["topic"])}</span></a>'
                     f'<span class="age">open {e(age(x["created"]))}</span>')
            if x["explainer"]:
                P.append(f'<p class="explainer">{e(x["explainer"])}</p>')
            P.append("</li>")
        P.append("</ul></details>")
    else:
        P.append('<p class="rest">No open think-work.</p>')

    if bad:
        P.append("<h2>Unparseable frontmatter</h2><ul class='open'>")
        P += [f'<li class="path">{e(p)}</li>' for p in bad]
        P.append("</ul>")

    P.append("<footer>")
    if other:
        parts = ", ".join(f"{v} {k}" for k, v in sorted(other.items()))
        P.append(f"<p>{sum(other.values())} more files, none needing you: {e(parts)}.</p>")
    P.append(f'<p>Generated {TODAY.isoformat()} · re-run <span class="mono">parked.py</span> to refresh '
             "&middot; this page is a render — the files are the truth.</p>")
    P.append("</footer>")
    P.append(f"</div></main><script>{FILTER_JS}</script></body></html>")
    return "\n".join(P) + "\n"


def main():
    blocked_h, world_only, open_t, other, bad, warnings = collect()
    RENDER_PATH.write_text(render(blocked_h, world_only, open_t, other, bad, warnings), encoding="utf-8")
    HTML_PATH.write_text(render_html(blocked_h, world_only, open_t, other, bad, warnings), encoding="utf-8")
    print(f"Written: {RENDER_PATH}")
    print(f"Written: {HTML_PATH}")
    print(f"  Waiting on you: {len(blocked_h)}, Waiting on world: {len(world_only)}, "
          f"Open topics: {len(open_t)}, Everything else: {sum(other.values())}, "
          f"Unparseable: {len(bad)}, Warnings: {len(warnings)}")


if __name__ == "__main__":
    main()
