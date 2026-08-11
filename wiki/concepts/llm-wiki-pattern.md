---
title: LLM Wiki Pattern
type: concept
domain: [ai-ml, devops]
status: stable
tags: [llm-wiki, obsidian, knowledge-graph, agentic-ai]
sources: [raw-sources/archive/build-llm-wiki-with-obsidian.md]
created: 2026-08-11
updated: 2026-08-11
---

# LLM Wiki Pattern

## Summary
A structured system, built once and used forever, where an agentic AI maintains a shared memory layer between itself and a human — instead of information staying scattered across raw sources, or a plain RAG system re-retrieving fragments on every query, the agent compiles sources into a persistent, cross-linked wiki that gets smarter and better-aligned the more material it's given. This is the pattern this vault itself implements (see [[retrieval-augmented-generation]] and [CLAUDE.md](../../CLAUDE.md)); this page captures the pattern as a concept in its own right, and one tutorial's specific implementation of it.

## Details

### The three core layers
1. **Sources (raw layer)** — captured source material: articles, transcripts, PDFs. Never modified once captured; the wiki cites it, doesn't overwrite it.
2. **Wiki layer** — topics, concepts, entities, and projects extracted from sources by the agent. As new sources are ingested, the wiki cites the raw material it was extracted from, so provenance is always traceable back to layer 1.
3. **Schema layer** — the rules, templates, and instructions (an `agents.md`/`CLAUDE.md`-style file, plus schema docs, workflow guidance) that tell the agent how to maintain the wiki consistently. Described as "the contract between you and the agent" — it's what keeps structure aligned over time even as the wiki grows to thousands of notes.

### The operating loop
Three repeatable operations, run in sequence:
1. **Ingest** — check for new raw sources, extract concepts/entities/topics from each into wiki notes, and have each new note cite its source.
2. **Maintain / Lint** — a validation pass that checks whether the ingest was applied correctly: front matter present and consistent, links resolving, no structural drift. One example surfaced in the source video: a "routing gap" where a concept resolved but a related term didn't, because catalog search failed to pull body text — lint caught and fixed it.
3. **Query** — pull an answer from the index/catalog and only open the relevant pages, rather than re-scanning the whole wiki. Framed explicitly as more efficient than plain RAG retrieval once the wiki and its catalog exist.

This loop is meant to run repeatedly — daily, or on some automated cadence — not as a one-time setup step. The source material frames scaling this to "thousands of sources and tens of thousands of concepts" as the actual target state, which is only tractable if the schema and tooling are solid from the start.

### Why git matters here
Every wiki operation is treated as a git-tracked change, specifically because an agent can make mistakes or corrupt the vault. Git commits act as save points — you can always diff or roll back to before a bad ingest. The wiki log (see [[wiki/log|Wiki Log]] in this vault) is the human-readable complement to that: a record of *what* changed and *why*, so the diff isn't the only way to understand a change.

### One tutorial's implementation choices (for comparison)
A specific walkthrough of this pattern (source: Wanderloots, "The LLM Wiki: A Shared Memory Layer For AI & Humans") builds it with meaningfully more tooling than a pure prompt-driven approach:
- A Python script (`wiki_tool.py`) that performs ingest/index/catalog/lint operations deterministically, rather than leaving the agent to reason out each step from scratch every time.
- Custom local Obsidian-aware skills scoped to the specific vault (e.g. an `llm-wiki-query` skill, an `llm-wiki-ingest` skill), on top of a general Obsidian CLI skill pack.
- Per-entity-type templates (source, concept, topic, entity, project, log) that the agent fills in, rather than one shared frontmatter schema across all types.
- An "Obsidian firewall" — a wrapper skill that checks any Obsidian CLI action against an approved-vault allowlist, so an agent operating in one vault can't accidentally write into another.
- Optional local-model support via Ollama, with a review/draft folder so a human approves a local model's output before it's applied — because local models are noted as more error-prone than cloud models, at least until the schema and skills are well-tuned.

See [[llm-wiki-pattern-vs-script-free-approach]] for how this vault's own choices compare and why.

## Open questions
- **Obsidian vault firewall** — this vault only ever operates on one vault, so a multi-vault safety wrapper hasn't been needed; revisit if a second vault is ever added to the same Claude Code setup.
- **Local model support (Ollama)** — not evaluated for this vault. Would let ingestion run fully offline/free, at a noted cost of more ingest errors compared to a cloud model.
- **PDF ingestion** — the tutorial mentions a planned PDF-to-markdown extraction step for raw sources; this vault currently expects sources to already be markdown/text in `raw-sources/inbox/` (see the manual-transcript convention in [raw-sources/inbox/README.md](../../raw-sources/inbox/README.md)). No PDF path exists yet.
- **"Molecular zettelkasting"** — referenced as the tutorial author's own more advanced knowledge-organization system, layered on top of the basic wiki pattern. Not explained in enough detail in this source to evaluate; would need a dedicated source to assess.
- **Heartbeat-style automation** (e.g. checking for new files every N minutes and running the full ingest/maintain/query loop automatically) — matches the "Later — scheduled agent" stage already named in this vault's own automation path (see [[llm-wiki-design-plan]]), not yet built.

## Related
- [[retrieval-augmented-generation]]
- [[devops-mcp-control-plane]]
- [[ai-rag-system-blueprint]]
- [[llm-wiki-pattern-vs-script-free-approach]]
