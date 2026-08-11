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

## Migration plan

Most existing numbered-folder notes are thin (~45-50 line) templated scaffolding from an earlier bootstrap pass — there isn't much content debt. Two runbooks and the six `AI-*` notes carry the real content and migrate as-is.

### Phase 1 — Scaffold the schema
- Create `raw-sources/{inbox,archive}/` and `wiki/{concepts,tools,projects,runbooks,people,decisions,reviews}/`
- Write `wiki/index.md` and `wiki/log.md` (empty, structure only)
- Rewrite `CLAUDE.md` to describe this structure as the schema layer, replacing today's folder-convention section

### Phase 2 — Carry over real content
- `04-Runbooks/*` → `wiki/runbooks/` unchanged in substance, frontmatter upgraded to the new schema
- `AI-AIOps/`, `AI-Agents/`, `AI-MCP/`, `AI-Models/`, `AI-RAG/`, `AI-Experiments/`, `01-Foundation/AI/*` → split into `wiki/concepts/` pages (one concept per page, not one page per old folder) tagged `domain: [ai-ml]`
- `03-Projects/*` → `wiki/projects/`, each gets a `status` field

### Phase 3 — Retire or archive the thin scaffolding
- `02-Knowledge/*`, `06-Resources/*` — templated stubs with little unique content; either fold their few real facts into the new concept pages or move the raw files into `raw-sources/archive/` as historical input, not live wiki pages
- `00-Inbox/inbox-capture-staging.md` → becomes `raw-sources/inbox/` itself; the note explaining the inbox becomes redundant once the folder name says it
- `99-System/*` — keep as historical record of the original design brief, referenced from the new `CLAUDE.md` rather than acted on

### Phase 4 — First real ingest
- Drop one new real source into `raw-sources/inbox/` and run `/ingest` to prove the schema before trusting it with a backlog
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
