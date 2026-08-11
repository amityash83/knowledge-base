---
title: LLM Wiki Pattern
type: concept
domain: [ai-ml, devops]
status: stable
tags: [llm-wiki, obsidian, knowledge-graph, agentic-ai]
sources: [raw-sources/archive/build-llm-wiki-with-obsidian.md, "https://github.com/wanderloots-tutorials/vibe-coding/blob/main/wanderloots-llm-wiki-core-setup-v1.0.0.md"]
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

### One tutorial's implementation, concretely
Beyond the walkthrough video, the same author publishes a public build spec — a "core setup guide" meant to be handed directly to a coding agent as its build instructions. It's considerably more concrete than the video's narration:

**Folder structure:**
```text
Raw/Sources/       # captured source material only
Raw/Files/          # PDFs and other non-text files
Wiki/Topics/
Wiki/Concepts/
Wiki/Entities/
Wiki/Projects/
Wiki/Logs/
Schema/             # the rules layer
_templates/         # one template per note type
.agents/skills/     # vault-scoped agent skills
scripts/            # wiki_tool.py and friends
```

**What `AGENTS.md` (the schema/contract file) is required to specify:**
- Treat `Raw/Sources/` as source material only — never overwrite it
- Write reusable knowledge only under `Wiki/`
- Keep every compiled note linked back to the Raw source it came from
- Search `Wiki/catalog.jsonl` before opening raw sources or broad context — i.e., check the index before doing expensive work
- Run build, lint, and source checks before every commit
- **Never invent citations**

**Required templates** (`_templates/`): `source-note.md`, `concept-note.md`, `topic-note.md`, `entity-note.md`, `project-note.md`, `log-note.md` — each compiled note is tagged with exactly one of `topic`, `concept`, `entity`, `project`, or `log`.

**`scripts/wiki_tool.py` commands:** `doctor` (health check), `build` (generate `catalog.jsonl` and indexes), `lint` (validate frontmatter and source links), `source-scan` (list raw sources), `source-lint` (validate source coverage), `search-catalog --query "..."` (search compiled notes without opening them), `log --title ... --details ...` (append to the wiki log).

**Build sequence, step by step:** (00) init vault + `.gitignore` → (01) create folder structure → (02) write `AGENTS.md`, schema files, agent skills → (03) create templates with correct frontmatter → (04) build the deterministic tooling (`wiki_tool.py`) → (05) ingest a first source and produce sample wiki notes → (06) run all tools and commit.

**Pre-commit maintenance gate:** run `doctor`, `build`, `lint`, `source-lint`, and an `audit_public.py` check, in that order, before committing.

**Acceptance criteria for "done":** `AGENTS.md` exists with clear rules; the templates directory is complete; `wiki_tool.py` supports every required command; `catalog.jsonl` and `source-manifest.jsonl` exist; at least one raw source is linked to a compiled wiki note; no advanced/bonus folders exist unless explicitly requested.

See [[llm-wiki-pattern-vs-script-free-approach]] for how this vault's own choices compare against this spec, and where it deliberately draws a narrower line (one read-only lint script, no catalog/build layer, no per-vault skill pack).

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
