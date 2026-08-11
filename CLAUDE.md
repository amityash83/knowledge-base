# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **not a software project** — it's an Obsidian vault (personal Markdown knowledge base), version-controlled with git. "Working in this repo" is mostly reading, writing, and cross-linking Markdown notes according to the schema below, not writing or executing code. The one exception is `scripts/wiki_lint.py` — a small, dependency-free, read-only validator for mechanical frontmatter/link mistakes (see Tooling below). Everything that requires judgment — deciding what a source means, which pages it touches, how a page should be worded — stays a Claude Code operation, never scripted.

The vault implements Andrej Karpathy's ["LLM Wiki" pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): instead of a RAG system that re-retrieves from raw documents on every query, Claude maintains a **persistent, evolving wiki** of cross-linked pages that accumulate and improve every time a new source is ingested. Design rationale and migration status live in [99-System/llm-wiki-design-plan.md](99-System/llm-wiki-design-plan.md) — read it before making structural changes.

## Three layers

1. **`raw-sources/`** — immutable inputs (articles, transcripts, PDFs, pasted notes). Claude reads these but **never edits them**.
   - `raw-sources/inbox/` — drop zone for anything not yet ingested
   - `raw-sources/archive/` — sources already ingested, kept for citation/provenance
2. **`wiki/`** — Claude-owned, cross-linked Markdown pages, one entity per page. This is the only tree Claude writes to as the product of normal work.
3. **This file** — the schema layer: structure, frontmatter, and the operations below.

Domain (`devops`, `ai-ml`, `personal`) is a **frontmatter tag, not a folder** — one shared wiki, not per-domain silos. A page can carry multiple domains (e.g. `domain: [ai-ml, devops]`) so a concept used in both contexts isn't duplicated.

## Wiki structure

Every page lives under `wiki/` in exactly one entity folder:

| Folder | Entity type | What goes here |
|---|---|---|
| `wiki/concepts/` | Concept | A durable idea — "RAG", "Kubernetes Service", "Compound interest" |
| `wiki/tools/` | Tool | A named system — Terraform, pgvector, Obsidian itself |
| `wiki/projects/` | Project | Ongoing work with a start state and a goal; has a `status` field |
| `wiki/runbooks/` | Runbook | A repeatable operational procedure with prerequisites and numbered steps |
| `wiki/people/` | Person | Anyone referenced across sources more than once |
| `wiki/decisions/` | Decision | A dated choice worth remembering the reasoning behind — including decisions about wiki content or tooling (e.g. "chose pgvector over FAISS"). Only decisions about the vault's own folder structure/schema go in `99-System/` instead — see below. |
| `wiki/reviews/` | Review | A synthesized answer to a past query, promoted because it's reusable |

Plus two special files:
- `wiki/index.md` — catalog of every page, grouped by entity type. Update it whenever a page is created or removed.
- `wiki/log.md` — append-only, newest-first record of every ingest/ask/lint run. Never delete entries; only append.

`dashboard.md` at the vault root is the human entry point and points into `wiki/index.md`.

## Page schema

Every wiki page uses this frontmatter, regardless of entity type:

```markdown
---
title: <Title>
type: concept | tool | project | runbook | person | decision | review
domain: [devops, ai-ml, personal]   # array; a page can span domains
status: stable | evolving | stub    # content maturity — for every type except project
                                     # projects use their own lifecycle instead:
                                     # status: active | paused | done
tags: [tag1, tag2]
sources: [raw-sources/archive/<file>]  # provenance back to layer 1; [] if none
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# <Title>

## Summary
## Details
## Open questions
## Related
- [[wikilink-to-related-page]]
```

Notes should be:
- Self-contained and explicit — avoid "this"/"that" (RAG chunking loses the context pronouns rely on)
- Broken into clear headings with short paragraphs (chunk-friendly)
- Linked to related pages via `[[wikilink]]`, including across domains
- Filed with a descriptive kebab-case filename, e.g. `kubernetes-cluster-fundamentals.md`

`Open questions` is what makes a page revisitable: something a future `/ingest` should try to answer, not a rhetorical gap.

## Operations

Three verbs, invoked on demand — nothing runs unattended yet (see the design plan's Automation path for the intended progression to scheduled ingestion).

- **Ingest** — given a source in `raw-sources/inbox/`: read it, decide which existing `wiki/` pages it touches (often several), create new pages only where none fit, append an entry to `wiki/log.md`, update `wiki/index.md` if pages were added/removed, then move the source to `raw-sources/archive/`.
- **Ask** — given a question: search `wiki/` (not raw sources) for relevant pages, answer with citations to specific pages by filename, and if the answer is reusable, offer to promote it to `wiki/reviews/`.
- **Lint** — periodic pass over `wiki/`: flag contradictions between pages, `status: stub` pages that have gone stale, pages with no inbound `[[links]]`, and domains with thin coverage. Report findings; don't silently rewrite pages. Run `scripts/wiki_lint.py` first (see Tooling) to clear mechanical issues before doing this semantic pass — no point reasoning about contradictions on a page with a typo'd `type:` field.

## Tooling

`scripts/wiki_lint.py` — a read-only, dependency-free (stdlib-only) script that checks every `wiki/*.md` page for mechanical mistakes: invalid `type`/`domain`/`status` values, missing required frontmatter fields, malformed dates, `sources` paths that don't exist on disk, and `[[wikilinks]]` that don't resolve to any page. Run it with `python3 scripts/wiki_lint.py` (add `--json` for machine-readable output). It never edits a file — only reports. This is deliberately the *only* script in the vault: it replaces token spent on Claude eyeballing frontmatter by hand, but the actual judgment calls (what a source means, which pages it touches, how to word a page) stay Claude Code operations. See [[llm-wiki-pattern-vs-script-free-approach]] for the fuller reasoning on where that line is drawn, and revisit it if the wiki grows enough that more automation (e.g. auto-generating `wiki/index.md`) starts paying for itself.

Run it after any `/ingest` and before any `/lint` pass.

## Migration status

Migration from the old `00`–`99` numbered-folder scheme (plus flat `AI-*` topic folders) into the `wiki/` structure is **complete**. Those folders no longer exist — everything real they held was moved into `raw-sources/archive/` and ingested into `wiki/` in one pass; see the "2026-08-11 — migration ingest" entry in `wiki/log.md` for exactly what was merged, split, or dropped.

- **All content lives in `wiki/`** now, following the schema above.
- `raw-sources/archive/` holds the original pre-migration files for provenance/citation — treat them as read-only history, not as pages to edit.
- `99-System/` is kept permanently as historical design record (the original bootstrap prompts plus [llm-wiki-design-plan.md](99-System/llm-wiki-design-plan.md)) — it documents the vault's own design, not domain content, so it stays outside `wiki/`.

Note: Karpathy's original gist defines only three layers — `raw-sources/`, `wiki/`, and the schema file — and relies on git history for tracking structural change, with no dedicated "system notes" area. `99-System/` is this vault's own addition on top of that pattern, kept because it predates this migration. Scope it narrowly: it holds **only** documents about the vault's own folder structure/schema (this file's design rationale). Every other kind of decision — tooling choices, domain content, personal calls — belongs in `wiki/decisions/`, not here, so `/ask` and `/lint` can actually find it.

## Editorial conventions

- **Runbooks** carry a Prerequisites section, numbered steps with runnable commands, a Common Errors & Fixes section, and often a reusable templated version of the commands (e.g. `{{DB_NAME}}` placeholders). Preserve this shape.
- Do not delete existing information when restructuring — prefer merging, re-linking, or moving into `raw-sources/archive/` over deleting.
- Runbook SQL/shell examples sometimes contain example credentials (e.g. `StrongPassword123`) — these are placeholder/template values, not live secrets, but don't add real secrets when editing these files.
