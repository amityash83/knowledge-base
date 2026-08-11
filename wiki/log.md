---
title: Wiki Log
type: review
domain: [devops, ai-ml, personal]
status: stable
tags: [log, wiki]
sources: []
created: 2026-08-11
updated: 2026-08-11
---

# Wiki Log

Append-only record of every `/ingest`, `/ask`, and `/lint` run. Newest entries at the top.

## Related
- [[wiki/index|Wiki Index]]
- [[llm-wiki-design-plan]]

---

### 2026-08-11 — first real ingest (Phase 4 complete)
**Operation:** ingest
**Source:** `raw-sources/inbox/build-llm-wiki-with-obsidian.md` — full transcript of "The LLM Wiki: A Shared Memory Layer For AI & Humans" (Wanderloots, YouTube), manually captured by the user since automated transcript fetching isn't reliable from this environment (YouTube captions are JS-rendered / signed URLs expire immediately — confirmed via WebFetch and curl before falling back to manual capture).
**Pages created:**
- Concept: [[llm-wiki-pattern]] — the 3-layer sources/wiki/schema pattern, its ingest/maintain/query loop, and why git matters for it
- Decision: [[llm-wiki-pattern-vs-script-free-approach]] — recorded why this vault stays script-free vs. the source's more heavily tooled (Python script, custom Obsidian skills, vault firewall) implementation of the same pattern
**Pages updated (cross-linked):** [[retrieval-augmented-generation]], [[devops-mcp-control-plane]], [[ai-rag-system-blueprint]], [[llm-wiki-design-plan]]
**Not created:** No stub pages for the source's advanced features not yet relevant to this vault (Obsidian multi-vault firewall, local model via Ollama, PDF ingestion, "molecular zettelkasting") — captured instead as Open questions on [[llm-wiki-pattern]] so they're findable later without speculative empty pages.
**Summary:** First ingest run against genuinely new material (not part of the bulk migration), closing out Phase 4 of [[llm-wiki-design-plan]]. Source moved to `raw-sources/archive/build-llm-wiki-with-obsidian.md`.

### 2026-08-11 — Phase 4 deferred
**Operation:** none (deferred)
**Summary:** Attempted to start Phase 4 (first `/ingest` against genuinely new material). No script or tooling was needed — confirmed `/ingest` is purely a prompt-driven operation, nothing to build. No real source was available yet, and a synthetic test note was deliberately skipped since it would validate less than waiting for real content. `raw-sources/inbox/` remains empty. Phase 4 stays open — pick it up the next time real material (an article, a note, anything not already in the wiki) is dropped into the inbox.

### 2026-08-11 — scope clarification: 99-System/ vs wiki/decisions/
**Operation:** schema clarification
**Summary:** Checked Karpathy's gist directly — it defines only three layers (raw-sources, wiki, schema file) and relies on git history for structural change, with no dedicated "system notes" concept. `99-System/` predates this migration and isn't part of the original pattern; kept but scoped narrowly in `CLAUDE.md`: it holds only documents about the vault's own folder structure/schema. Every other kind of decision — including tooling choices like vector DB selection — goes in `wiki/decisions/` so `/ask` and `/lint` can find it. No files moved.

### 2026-08-11 — migration ingest
**Operation:** ingest (bulk, Phase 2/3 of [[llm-wiki-design-plan]])
**Sources:** all 26 real-content files from the old `00-Inbox/`, `01-Foundation/AI/`, `02-Knowledge/`, `03-Projects/`, `04-Runbooks/`, `04-Snippets/`, `05-Logs/`, `06-Resources/`, and `AI-*/` folders, moved unchanged into `raw-sources/archive/` before ingest.
**Pages created:**
- Concepts (10): [[artificial-intelligence]], [[machine-learning-vs-deep-learning]], [[retrieval-augmented-generation]], [[embeddings-and-vector-databases]], [[ai-agents]], [[aiops]], [[mcp-architecture]], [[kubernetes-cluster-fundamentals]], [[kubernetes-service-networking]], [[terraform-workflow]]
- Tools (2): [[kubectl]], [[terraform]]
- Projects (3): [[devops-lab-platform-foundation]], [[devops-mcp-control-plane]], [[ai-rag-system-blueprint]]
- Runbooks (2): [[postgresql-rds-db-setup-for-applications]], [[aws-alb-opensearch-log-pipeline]]
- Reviews (1): [[ai-learning-free-courses]]
**Merges:** RAG content from `RAG-Basics.md`, `AI-RAG(Advance).md`, `AI-Concepts.md`'s RAG section, and `llm-rag-basic-concepts.md` consolidated into the single [[retrieval-augmented-generation]] page instead of four overlapping pages. `AI-Basics.md` split across [[artificial-intelligence]] and [[aiops]] by topic rather than kept as one multi-topic page.
**Not carried forward as pages:** `platform-reference-map.md` and the old `02-Knowledge/index.md` / `03-Projects/index.md` — their job (a curated map of top pages) is superseded by this index; archived as sources only. `ops-vault-bootstrap-log.md` and `inbox-capture-staging.md` archived as historical record, not turned into wiki pages (no durable entity to extract).
**Summary:** First real ingest pass, run as one single pass across all sources per plan. Old folders (`00-Inbox/`, `01-Foundation/`, `02-Knowledge/`, `03-Projects/`, `04-Runbooks/`, `04-Snippets/`, `05-Logs/`, `06-Resources/`, `AI-AIOps/`, `AI-Agents/`, `AI-Experiments/`, `AI-MCP/`, `AI-Models/`, `AI-RAG/`) removed after migration — see [[llm-wiki-design-plan]] Phase 3.
**Note:** `AI-Experiments.md` and `AI-Models.md` were read during ingest but contained no durable, vault-specific content beyond generic definitions already covered by [[artificial-intelligence]], [[ai-agents]], and [[machine-learning-vs-deep-learning]] — archived as sources, no dedicated page created. Revisit if either accumulates real experiment logs or model-selection decisions later.

### 2026-08-11 — scaffold
**Operation:** setup
**Summary:** Created `raw-sources/{inbox,archive}/` and `wiki/{concepts,tools,projects,runbooks,people,decisions,reviews}/`. Initialized `wiki/index.md` and this log. Rewrote `CLAUDE.md` to describe the three-layer schema and the ingest/ask/lint operations. Linked `dashboard.md` to `wiki/index.md`. No content migrated yet — Phase 1 of [[llm-wiki-design-plan]] complete; Phase 2 (carry over runbooks, AI-* concepts, projects) not started.
