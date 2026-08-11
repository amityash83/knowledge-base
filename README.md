---
title: Obsidian Vault README
tags: [readme, knowledge-base, obsidian, wiki]
domain: knowledge-management
difficulty: beginner
created: 2026-04-10
updated: 2026-08-11
---

# Obsidian Vault README

## Purpose
This vault is a personal LLM-maintained wiki, following Andrej Karpathy's ["LLM Wiki" pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): instead of a RAG system that re-retrieves from raw documents on every query, Claude Code maintains a persistent, evolving wiki of cross-linked Markdown pages that accumulate and improve every time a new source is ingested. Obsidian is used purely as the viewer — graph view, wikilinks, and (optionally) Dataview over the same files Claude writes.

Full schema and conventions live in [CLAUDE.md](CLAUDE.md); the design rationale and migration history live in [99-System/llm-wiki-design-plan.md](99-System/llm-wiki-design-plan.md).

## Three Layers

### `raw-sources/`
Immutable inputs — articles, transcripts, PDFs, pasted notes. Claude reads these but never edits them.
- `raw-sources/inbox/` — drop zone for anything not yet ingested
- `raw-sources/archive/` — sources already ingested, kept for citation/provenance

### `wiki/`
Claude-owned, cross-linked Markdown pages, one entity per page:
- `wiki/concepts/` — durable ideas (Kubernetes, RAG, MCP, ...)
- `wiki/tools/` — named systems (Terraform, kubectl, ...)
- `wiki/projects/` — ongoing work with a status field
- `wiki/runbooks/` — repeatable operational procedures
- `wiki/people/` — collaborators, authors, mentors
- `wiki/decisions/` — dated choices worth remembering the reasoning behind
- `wiki/reviews/` — synthesized answers to past queries, promoted because they're reusable
- `wiki/index.md` — catalog of every page, by entity type
- `wiki/log.md` — append-only record of every ingest/ask/lint run

### `CLAUDE.md`
The schema layer — folder structure, page frontmatter, and the ingest/ask/lint operation definitions.

## How To Use This Vault
1. Start from [dashboard.md](dashboard.md) or [wiki/index.md](wiki/index.md).
2. Drop new material into `raw-sources/inbox/`.
3. Ask Claude Code to `/ingest` it — it reads the source, updates or creates the relevant `wiki/` pages, logs the operation, and archives the source.
4. Ask questions directly — Claude Code searches `wiki/` and answers with citations.
5. Run a `/lint` pass periodically to catch contradictions, stale pages, and orphaned links.

## Note Design Standard
Every wiki page uses one frontmatter shape (`type`, `domain`, `status`, `tags`, `sources`, `created`/`updated`) and the same section order:
- `Summary`
- `Details`
- `Open questions`
- `Related`

See [CLAUDE.md](CLAUDE.md) for the full schema and entity-type table.

## Naming Convention
Descriptive kebab-case file names with domain context, e.g. `kubernetes-cluster-fundamentals.md`, `aws-alb-opensearch-log-pipeline.md`.

## Key Entry Points
- [dashboard.md](dashboard.md)
- [wiki/index.md](wiki/index.md)
- [wiki/log.md](wiki/log.md)
- [CLAUDE.md](CLAUDE.md)
- [99-System/llm-wiki-design-plan.md](99-System/llm-wiki-design-plan.md)
