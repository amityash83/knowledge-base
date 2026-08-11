---
title: Knowledge Dashboard
tags: [dashboard, knowledge-base, obsidian, wiki]
domain: knowledge-management
difficulty: intermediate
created: 2026-04-09
updated: 2026-08-11
---

# Knowledge Dashboard

## Summary
This dashboard is the entry point for the Obsidian vault. It highlights active projects, core concepts, and recent operations, and points into the [[wiki/index|Wiki Index]] — the actual catalog of every page — for full navigation.

## Concepts
- A dashboard reduces navigation friction by linking high-value pages first.
- Stable top-level links make the vault easier for humans and Claude Code to parse.
- The full page catalog lives in [[wiki/index|Wiki Index]], grouped by entity type; this page is just the fast path to what matters most right now.

## Commands / Code
```bash
# Open the vault root and start from the dashboard
cd /Users/amitmishra/temp/ObsidianVault
```

## Architecture / Flow
1. Drop new material into `raw-sources/inbox/`.
2. Run `/ingest` to read it and update `wiki/` pages (see [CLAUDE.md](CLAUDE.md) for the operation definitions).
3. Ask questions with `/ask`, which searches `wiki/` and cites the pages it used.
4. Run `/lint` periodically to catch contradictions, stale pages, and orphaned links.
5. Every operation is recorded in [[wiki/log|Wiki Log]].

## Use Cases
- Start daily work from a single navigation page.
- Surface the most important project and concept links for fast retrieval.
- Provide a clean anchor note for Claude Code's `/ask` and `/ingest` operations.

## Related Topics
- [[wiki/index|Wiki Index]]
- [[wiki/log|Wiki Log]]
- [[llm-wiki-design-plan]]
- [[devops-mcp-control-plane]]
- [[ai-rag-system-blueprint]]
- [[devops-lab-platform-foundation]]

## Tags
#dashboard #obsidian #knowledge-base #wiki

## Active Projects
- [[devops-mcp-control-plane]]
- [[devops-lab-platform-foundation]]
- [[ai-rag-system-blueprint]]

## Core Concepts
- [[artificial-intelligence]]
- [[retrieval-augmented-generation]]
- [[kubernetes-cluster-fundamentals]]
- [[terraform-workflow]]
- [[mcp-architecture]]

## Runbooks
- [[postgresql-rds-db-setup-for-applications]]
- [[aws-alb-opensearch-log-pipeline]]

## Quick Access
- [[kubectl]]
- [[terraform]]
- [[ai-learning-free-courses]]
