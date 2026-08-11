# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **not a software project** — it's an Obsidian vault (personal Markdown knowledge base) for DevOps and AI notes, version-controlled with git. There is no build, lint, or test tooling. "Working in this repo" means reading, writing, and reorganizing Markdown notes according to the conventions below, not writing or executing code.

The vault is designed to serve three purposes simultaneously:
- Human-readable technical documentation
- RAG-ready retrieval (chunkable, keyword-explicit notes)
- MCP-style agent workflows (notes that describe automatable steps)

## Vault structure

Two organizational schemes coexist in this repo — know both when navigating or filing new notes:

**Numbered folders (current standard, use this for new notes):**
- `00-Inbox/` — raw, unclassified capture (see `inbox-capture-staging.md`)
- `01-Foundation/` — foundational subject-matter notes, organized in subfolders by domain (e.g. `01-Foundation/AI/`)
- `02-Knowledge/` — durable, stable domain knowledge (Kubernetes, Terraform, RAG/LLM concepts, networking). Has an `index.md`.
- `03-Projects/` — active project notes and project-level context. Has an `index.md`.
- `04-Runbooks/` — step-by-step operational procedures (e.g. RDS setup, log pipelines)
- `04-Snippets/` — reusable commands/templates (kubectl, Terraform CLI, RAG pipeline templates)
- `05-Logs/` — historical/operational timelines (vault bootstrap log, migration records)
- `06-Resources/` — canonical reference maps and curated link collections
- `99-System/` — system/bootstrap prompts and vault design-rule notes (read these to understand *why* the vault is shaped this way)

Note: `README.md` describes an older numbering (`01-Projects`, `03-Snippets`, `04-Logs`, `05-Resources`) that doesn't match the folders actually on disk today. Trust the folder names on disk (as listed above), not the README's numbers, when filing new notes.

**Flat `AI-*` folders (older/parallel scheme, still populated):** `AI-AIOps/`, `AI-Agents/`, `AI-Experiments/`, `AI-MCP/`, `AI-Models/`, `AI-RAG/` — one topic file per folder. These predate the numbered-folder standard and use a lighter emoji-heading style (see Note formats below). Don't invent more folders in this scheme; new AI content should go into `01-Foundation/AI/` or `02-Knowledge/` instead.

`dashboard.md` at the vault root is the entry point/navigation hub — it links out to active projects, learning areas, and recent notes via `[[wikilink]]` references. When adding a significant new project or knowledge note, consider linking it from `dashboard.md`.

## Note formats

Two note styles are both in active use. Match the style already used in the folder you're editing; use the frontmatter style for anything new in the numbered folders.

**Frontmatter style** (current standard — `02-Knowledge/`, `03-Projects/`, `99-System/`, etc.):
```markdown
---
title: <Title>
tags: [tag1, tag2, tag3]
domain: <domain>
difficulty: beginner|intermediate|advanced
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# <Title>

## Summary
## Concepts
## Commands / Code
## Architecture / Flow
## Use Cases
## Related Topics
- [[wikilink-to-related-note]]
## Tags
#hashtag #style #tags
```

**Emoji-heading style** (older — `AI-*/` folders): no frontmatter; `#` heading with an emoji, `tags: #a #b #c` as a plain line, sections with emoji bullets (📌, 🔹, 👉), a `Related Notes` section of `[[wikilinks]]`, no closing `## Tags` block.

Regardless of style, notes are expected to be:
- Self-contained and explicit (avoid "this"/"that" — RAG chunking loses context that pronouns rely on)
- Broken into clear headings with short paragraphs (chunk-friendly)
- Linked to related notes via `[[wikilink]]`
- Tagged for retrieval, using structured tags like `#infra/kubernetes`, `#tool/terraform`, `#project/mcp`, `#learning`

File names are descriptive kebab-case with domain context, e.g. `kubernetes-cluster-fundamentals.md`, `aws-alb-opensearch-log-pipeline-runbook.md`.

## Editorial conventions

- **Runbooks** (`04-Runbooks/`) document real operational procedures (e.g. AWS RDS/PostgreSQL setup, ALB logs → OpenSearch pipeline). They include a Prerequisites section, numbered steps with runnable commands, a Common Errors & Fixes section, and often end with a reusable templated version of the commands (e.g. `{{DB_NAME}}` placeholders). Preserve this shape when adding or editing runbooks.
- Treat `99-System/ai-obsidian-bootstrap-prompt.md` and `99-System/obsidian-rag-mcp-master-prompt.md` as the design brief for the vault — they record the original intent (RAG/MCP-ready structure) and the exact note template originally specified. If asked to "organize the vault" or restructure notes, consult these first.
- Do not delete existing information when restructuring notes — prefer merging, re-linking, or moving over deleting (this is an explicit constraint from the bootstrap brief).
- When promoting an inbox item, follow the flow: rough capture in `00-Inbox/` → durable note in `02-Knowledge/` or `03-Projects/` → reusable commands extracted to `04-Snippets/` → milestone recorded in `05-Logs/`.
- Runbook SQL/shell examples in this vault sometimes contain example credentials (e.g. `StrongPassword123`) — these are placeholder/template values for local reference notes, not live secrets, but don't add real secrets when editing these files.
