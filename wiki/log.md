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
