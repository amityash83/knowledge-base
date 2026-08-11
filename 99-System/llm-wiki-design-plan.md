---
title: LLM Wiki Design & Migration Plan
tags: [system, wiki, obsidian, rag, plan]
domain: knowledge-management
difficulty: intermediate
created: 2026-08-11
updated: 2026-08-11
status: planning
---

# LLM Wiki — Design & Migration Plan

> Plan only — nothing described here has been created yet. This is the reference doc to execute against when migration starts.

## Source pattern

Based on Andrej Karpathy's ["LLM Wiki" gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): instead of a RAG system that re-retrieves from raw documents on every query, an LLM maintains a **persistent, evolving wiki** — structured, cross-linked Markdown pages that accumulate and improve every time a new source is added.

Three layers:

1. **Raw sources** — immutable documents (articles, papers, transcripts). The LLM reads but never modifies these.
2. **The wiki** — LLM-owned, cross-linked Markdown pages organized by entity: concepts, tools, projects, people, decisions.
3. **The schema** — a config document (`CLAUDE.md`) defining wiki structure, conventions, and operations.

Core operations: **ingest** (process a new source, touch 10-15 pages), **query** (answer a question from the wiki, cite pages, promote good answers to new pages), **lint** (periodic pass for contradictions, stale claims, orphaned pages).

## Decisions made

- **One shared wiki, not three.** DevOps/Infra, AI/ML learning, and Personal all live in the same `wiki/` tree with shared entity types. Domain is a frontmatter tag (`domain: [ai-ml]`), not a folder boundary — so a concept page can be tagged across domains and cross-link into a project note without duplicating content.
- **On-demand trigger to start.** You drop sources into `raw-sources/inbox/` and explicitly run `/ingest` (or ask a question, or run `/lint`) in a Claude Code session. No background process yet — this proves the ingest logic before trusting it unattended.
- **Fresh wiki, fold in the few real notes.** Most of the current numbered-folder notes (`02-Knowledge/`, `06-Resources/`, etc.) are thin ~45-50 line templated scaffolding from an earlier bootstrap pass, not real content debt. The two runbooks (`04-Runbooks/`) and the six `AI-*` folder notes carry the real content and migrate over largely as-is.
- **Obsidian is view-only.** It never needs to write back to the vault for this to work — it just needs to point at the same folder Claude edits, so wikilinks and graph view work for free.

## Folder structure

Replaces the current `00`–`99` numbered scheme and the flat `AI-*` folders with entity-typed folders under `wiki/`. Numbers encoded a linear "capture → promote" pipeline; entity types encode what a page *is*, which is what makes pages easy for Claude to find and link at ingest time.

```
ObsidianVault/
├── raw-sources/              # layer 1 — never edited by Claude
│   ├── inbox/                # drop zone: articles, PDFs, pasted transcripts, voice notes
│   └── archive/               # sources already ingested, kept for citation/audit
│
├── wiki/                     # layer 2 — Claude-owned, cross-linked pages
│   ├── index.md              # catalog of every page, by entity type
│   ├── log.md                # append-only: every ingest / query / lint run
│   ├── concepts/              # durable ideas — "RAG", "Kubernetes Services", "Compounding"
│   ├── tools/                 # named systems — "Terraform", "Obsidian", "pgvector"
│   ├── projects/              # active/ongoing work with a start state and a goal
│   ├── runbooks/               # procedures — carried over from 04-Runbooks/ as-is
│   ├── people/                 # collaborators, authors, mentors referenced across notes
│   ├── decisions/              # dated calls worth remembering *why* you made
│   └── reviews/                # synthesized answers to past queries, promoted to pages
│
├── 00-Inbox/                 # → folds into raw-sources/inbox/ (see Migration)
├── 99-System/                 # kept: bootstrap + master-prompt notes, historical record
├── CLAUDE.md                  # layer 3 — the schema (this plan becomes its source)
└── dashboard.md               # Obsidian home note → now points at wiki/index.md
```

## Entity types

Seven page kinds, shared across all three domains. Every wiki page is exactly one of these.

| Type | Folder | What it is |
|---|---|---|
| Concept | `wiki/concepts/` | A durable idea that doesn't change once understood — "RAG", "Kubernetes Service", "Compound interest". The bulk of AI/ML learning content lands here. |
| Tool | `wiki/tools/` | A named system you use — Terraform, pgvector, Obsidian itself. Tracks version notes, gotchas, links to concepts it implements. |
| Project | `wiki/projects/` | Has a start state and a goal — e.g. `devops-mcp-control-plane`. Status field (active/paused/done) instead of a separate active-projects folder. |
| Runbook | `wiki/runbooks/` | A repeatable procedure with prerequisites, numbered steps, common failures — the shape the two existing runbooks already use. |
| Person | `wiki/people/` | Anyone referenced across sources more than once — author, mentor, collaborator. Thin pages that mostly exist to be linked from elsewhere. |
| Decision | `wiki/decisions/` | A personal or technical choice worth remembering the reasoning behind, dated — e.g. "chose pgvector over Pinecone, 2026-08". Where the Personal domain mostly lives. |
| Review | `wiki/reviews/` | A synthesized answer to a past query that turned out reusable. Not written directly; only promoted from a query. |

## Page schema

One frontmatter shape for every entity type. Keeps what already works in the current standard (tags, domain, created/updated) and adds what the wiki pattern needs: entity type, source provenance, status.

```markdown
---
title: Retrieval-Augmented Generation
type: concept                 # concept | tool | project | runbook | person | decision | review
domain: [ai-ml]                # ai-ml | devops | personal — an array, notes can span domains
status: stable                 # stable | evolving | stub — signals lint targets
tags: [rag, retrieval, llm]
sources: [raw-sources/archive/2026-08-rag-survey.pdf]
created: 2026-08-11
updated: 2026-08-11
---

# Retrieval-Augmented Generation

## Summary
## Details
## Open questions          ← new: what this page doesn't yet answer
## Related
- [[kubernetes-cluster-fundamentals]]  ← cross-domain link, made cheap by one shared wiki
```

The `Summary / Concepts / Related Topics / Tags` shape from the current standard survives almost unchanged — it was already RAG-friendly. New additions:
- `type` — so Claude can filter by entity kind
- `sources` — provenance back to layer 1, for citations
- `status` — what lint checks
- `Open questions` section — turns a note from a dead-end into something ingest revisits later

## Operations

Three verbs, same as the gist. Each becomes a slash-command-style skill invoked explicitly — nothing runs unattended yet (see Automation path).

| Operation | You do | Claude does |
|---|---|---|
| `/ingest` | Drop a file/link/paste into `raw-sources/inbox/`, run the command | Reads the source, decides which existing pages it touches (typically several), creates new pages where none fit, updates `wiki/log.md`, moves the source to `archive/` |
| `/ask` | Ask a question in plain language | Searches `wiki/` (not raw sources) for relevant pages, answers with citations to specific pages, offers to promote the answer to `wiki/reviews/` if reusable |
| `/lint` | Run periodically, e.g. weekly | Flags contradictions between pages, stale `status: stub` pages, orphaned pages with no inbound links, domains with thin coverage |

## Obsidian as the viewer

Obsidian's job is purely to view and browse what Claude writes — it never needs to write back for this to work.

- **Wikilinks & graph view (already true)** — notes already use `[[wikilinks]]`. Point Obsidian's vault root at the same folder Claude edits and the graph view becomes a live map of the entity network for free.
- **Dataview plugin (worth adding)** — query pages by frontmatter, e.g. "all `type: decision` tagged `personal` from the last 30 days" — without Claude having to hand-maintain more index pages.
- **Web Clipper (optional)** — clip an article straight into `raw-sources/inbox/` from the browser, the fastest way to keep the inbox fed between Claude Code sessions.

## Migration plan — status: complete (2026-08-11)

Most existing numbered-folder notes were thin (~45-50 line) templated scaffolding from an earlier bootstrap pass — there wasn't much content debt. Execution deviated from the original plan below in one deliberate way: rather than hand-migrating old notes into `wiki/` folder-by-folder, **every real-content file was moved into `raw-sources/archive/` unchanged and then run through one real `/ingest` pass** — treating the old vault as source material to ingest, not as pages to reshuffle. This produced a properly deduplicated, split, cross-linked wiki instead of a 1:1 file-for-file copy. Full detail of what was merged/split/dropped is in the "2026-08-11 — migration ingest" entry of `wiki/log.md`.

### Phase 1 — Scaffold the schema ✅
- Created `raw-sources/{inbox,archive}/` and `wiki/{concepts,tools,projects,runbooks,people,decisions,reviews}/`
- Wrote `wiki/index.md` and `wiki/log.md`
- Rewrote `CLAUDE.md` to describe this structure as the schema layer

### Phase 2 — Move everything real into raw-sources, then ingest ✅
- All 26 real-content files (2 runbooks, 6 `AI-*` notes, 4 `01-Foundation/AI` notes, 4 `02-Knowledge` notes + its index, 3 `03-Projects` notes + its index, 3 `04-Snippets` notes, 2 `06-Resources` notes, 1 `05-Logs` note, 1 `00-Inbox` note) moved via `git mv` into `raw-sources/archive/`, preserving git history
- One ingest pass read all of them together and produced: 10 concept pages, 2 tool pages, 3 project pages, 2 runbook pages, 1 review page — deduplicating four overlapping RAG notes into a single [[retrieval-augmented-generation]] page, and splitting the multi-topic `AI-Basics.md` across [[artificial-intelligence]] and [[aiops]]
- `AI-Experiments.md` and `AI-Models.md` were read but had no durable content beyond what the other concept pages already cover — archived as sources with no dedicated page

### Phase 3 — Remove the old folders ✅
- `platform-reference-map.md` and the old `02-Knowledge/index.md` / `03-Projects/index.md` were archived as sources, not turned into pages — their job is superseded by `wiki/index.md`
- All now-empty old folders (`00-Inbox/`, `01-Foundation/`, `02-Knowledge/`, `03-Projects/`, `04-Runbooks/`, `04-Snippets/`, `05-Logs/`, `06-Resources/`, `AI-AIOps/`, `AI-Agents/`, `AI-Experiments/`, `AI-MCP/`, `AI-Models/`, `AI-RAG/`) were deleted
- `99-System/*` kept in place as historical design record, untouched

### Phase 4 — First real ingest against new material — open, waiting on a real source
- No script or tooling is needed for this step — `/ingest` is just a prompt: give Claude a source, it reads it and updates `wiki/` pages directly. There's nothing to build.
- Deliberately not tested with synthetic/placeholder content — the point of this phase is to validate the operation against something real, so a fake test note would prove less than waiting for actual material.
- Next real source you drop into `raw-sources/inbox/` (an article, a meeting note, anything not already in the wiki) — ask for `/ingest` and this phase closes out.
- Check the result: does it link into the migrated pages correctly, does `log.md` read clearly, does Obsidian's graph view look sane

## Automation path

You want scheduled ingestion eventually. Starting on-demand isn't a lesser version of that — it's the only way to validate the ingest logic before letting it run unattended against real notes.

1. **Now — on-demand.** You drop sources, you say "ingest inbox." Every write is something you watched happen.
2. **Next — packaged skill.** Turn ingest/ask/lint into repeatable skills so the steps don't drift between sessions.
3. **Later — scheduled agent.** A cron-triggered cloud agent checks the inbox on a schedule and commits — once you trust unattended writes to it.

## Open decisions for execution time

Deliberately left open — worth answering when actually building, not now.

| Question | Why it can wait |
|---|---|
| Exact `/ingest` skill prompt wording | Easier to tune against real sources than to guess in the abstract |
| How aggressively lint auto-fixes vs. flags for review | Depends on how much you trust the first few ingests |
| Whether personal/decisions pages need extra privacy handling before Obsidian sync | Depends on whether this vault ever syncs to a shared device |

## Related
- [[ai-obsidian-bootstrap-prompt]]
- [[obsidian-rag-mcp-master-prompt]]
- [[dashboard]]
