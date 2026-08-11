#!/usr/bin/env python3
"""
wiki_lint.py — read-only frontmatter and link validator for wiki/*.md.

Purpose: catch mechanical mistakes (bad `type`, missing fields, dangling
`sources` paths, unresolved [[wikilinks]]) without spending Claude's tokens
on eyeballing frontmatter by hand. This script never writes anything —
it only reports. Deciding *what* a page should say, which pages an ingest
touches, and how pages should be worded remains Claude's job; see
CLAUDE.md and 99-System/llm-wiki-design-plan.md for why the split is drawn
here (wiki/decisions/llm-wiki-pattern-vs-script-free-approach.md has the
fuller reasoning).

Usage:
    python3 scripts/wiki_lint.py            # human-readable report
    python3 scripts/wiki_lint.py --json      # machine-readable report
    python3 scripts/wiki_lint.py --quiet     # exit code only, no output

Exit code: 0 if no problems found, 1 otherwise. No external dependencies —
stdlib only, so nothing to install.
"""

import json
import re
import sys
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = VAULT_ROOT / "wiki"

VALID_TYPES = {"concept", "tool", "project", "runbook", "person", "decision", "review"}
VALID_DOMAINS = {"devops", "ai-ml", "personal"}
VALID_STATUSES = {"stable", "evolving", "stub"}  # content maturity — every type except project
VALID_PROJECT_STATUSES = {"active", "paused", "done"}  # project lifecycle — see CLAUDE.md Page schema
REQUIRED_FIELDS = ["title", "type", "domain", "status", "tags", "sources", "created", "updated"]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)")


def parse_frontmatter(text):
    """Minimal YAML-subset parser for this vault's flat frontmatter schema.
    Handles: strings, dates, and single-line lists (`[a, b]` or `[]`).
    Returns (frontmatter_dict, body_text) or (None, text) if no frontmatter block."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    fm_block = text[4:end]
    body = text[end + 5:]
    fm = {}
    for line in fm_block.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            if not inner:
                fm[key] = []
            else:
                fm[key] = [v.strip().strip('"').strip("'") for v in inner.split(",")]
        else:
            fm[key] = value.strip('"').strip("'")
    return fm, body


def find_wiki_pages():
    return sorted(p for p in WIKI_DIR.rglob("*.md") if p.name not in {"index.md", "log.md"})


def all_page_stems():
    """Every valid wikilink target this vault can resolve. Obsidian resolves
    [[wikilinks]] vault-wide, not just within wiki/ — so this includes wiki/
    pages, the two special wiki/ files, and non-wiki pages (dashboard.md,
    README.md, and everything under 99-System/) that wiki pages legitimately
    link out to (e.g. [[llm-wiki-design-plan]])."""
    stems = {p.stem for p in find_wiki_pages()}
    stems |= {"index", "log"}
    stems |= {p.stem for p in VAULT_ROOT.glob("*.md")}
    stems |= {p.stem for p in (VAULT_ROOT / "99-System").glob("*.md")}
    return stems


def check_page(path, fm, body, known_stems):
    problems = []
    rel = path.relative_to(VAULT_ROOT)

    if fm is None:
        return [f"{rel}: no frontmatter block found"]

    for field in REQUIRED_FIELDS:
        if field not in fm or fm[field] in (None, "", []):
            problems.append(f"{rel}: missing or empty required field '{field}'")

    if "type" in fm and fm["type"] not in VALID_TYPES:
        problems.append(f"{rel}: invalid type '{fm['type']}' (expected one of {sorted(VALID_TYPES)})")

    if "domain" in fm:
        domains = fm["domain"] if isinstance(fm["domain"], list) else [fm["domain"]]
        bad = [d for d in domains if d not in VALID_DOMAINS]
        if bad:
            problems.append(f"{rel}: invalid domain(s) {bad} (expected subset of {sorted(VALID_DOMAINS)})")

    if "status" in fm:
        allowed = VALID_PROJECT_STATUSES if fm.get("type") == "project" else VALID_STATUSES
        if fm["status"] not in allowed:
            problems.append(f"{rel}: invalid status '{fm['status']}' (expected one of {sorted(allowed)})")

    for date_field in ("created", "updated"):
        if date_field in fm and fm[date_field] and not DATE_RE.match(fm[date_field]):
            problems.append(f"{rel}: {date_field} '{fm[date_field]}' is not YYYY-MM-DD")

    if "sources" in fm and isinstance(fm["sources"], list):
        for src in fm["sources"]:
            if not src or src.startswith(("http://", "https://")):
                continue  # external citation, not a local path — nothing to check on disk
            src_path = VAULT_ROOT / src
            if not src_path.exists():
                problems.append(f"{rel}: sources entry '{src}' does not exist on disk")

    body_no_code = re.sub(r"`[^`]*`", "", body)  # strip inline code spans so example
    body_no_code = re.sub(r"```.*?```", "", body_no_code, flags=re.DOTALL)  # and fenced blocks
    for link in WIKILINK_RE.findall(body_no_code):  # aren't mistaken for real [[links]]
        target = link.split("|")[0].strip()
        target_stem = target.rsplit("/", 1)[-1]
        if target_stem not in known_stems:
            problems.append(f"{rel}: [[{target}]] does not resolve to any known page")

    return problems


def main():
    args = sys.argv[1:]
    as_json = "--json" in args
    quiet = "--quiet" in args

    if not WIKI_DIR.is_dir():
        print(f"error: {WIKI_DIR} not found", file=sys.stderr)
        return 1

    pages = find_wiki_pages()
    known_stems = all_page_stems()
    all_problems = []

    for path in pages:
        text = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        all_problems.extend(check_page(path, fm, body, known_stems))

    if as_json:
        print(json.dumps({"pages_checked": len(pages), "problems": all_problems}, indent=2))
    elif not quiet:
        print(f"Checked {len(pages)} wiki pages.")
        if all_problems:
            print(f"\n{len(all_problems)} problem(s) found:\n")
            for p in all_problems:
                print(f"  - {p}")
        else:
            print("No problems found.")

    return 1 if all_problems else 0


if __name__ == "__main__":
    sys.exit(main())
