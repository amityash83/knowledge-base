---
title: Knowledge Dashboard
tags: [dashboard, knowledge-base, obsidian]
domain: knowledge-management
difficulty: intermediate
created: 2026-04-09
updated: 2026-04-09
---

# Knowledge Dashboard

## Summary
This dashboard is the entry point for the Obsidian vault. It highlights active projects, core learning areas, recent operational notes, and quick links that support a DevOps and AI knowledge workflow.

> **Migration in progress:** the vault is moving to a [[wiki/index|Wiki Index]]-based structure (see [[llm-wiki-design-plan]]). Links below still point at the old folders until their content is carried over.

## Concepts
- A dashboard reduces navigation friction by linking high-value notes first.
- Stable top-level links make the vault easier for humans, RAG chunking, and MCP-driven agents to parse.
- Explicit note names improve search relevance and downstream embedding quality.

## Commands / Code
```bash
# Open the vault root and start from the dashboard
cd /Users/amitmishra/temp/ObsidianVault
```

## Architecture / Flow
1. Capture unstructured ideas in [[inbox-capture-staging]].
2. Promote durable work into [[02-Knowledge/index|Knowledge Index]] and project notes under `01-Projects/`.
3. Convert repeated commands into snippet notes under `03-Snippets/`.
4. Maintain operational history in [[ops-vault-bootstrap-log]].

## Use Cases
- Start daily work from a single navigation page.
- Surface the most important project and knowledge links for fast retrieval.
- Provide a clean anchor note for RAG indexing and agent orchestration.

## Related Topics
- [[wiki/index|Wiki Index]]
- [[02-Knowledge/index|Knowledge Index]]
- [[devops-mcp-control-plane]]
- [[ai-rag-system-blueprint]]
- [[devops-lab-platform-foundation]]
- [[platform-reference-map]]

## Tags
#dashboard #obsidian #knowledge-base #rag #mcp

## Active Projects
- [[devops-mcp-control-plane]]
- [[devops-lab-platform-foundation]]
- [[ai-rag-system-blueprint]]

## Learning Areas
- [[kubernetes-cluster-fundamentals]]
- [[terraform-infrastructure-workflows]]
- [[llm-rag-basic-concepts]]
- [[networking-service-routing-basics]]

## Recent Notes
- [[ops-vault-bootstrap-log]]
- [[platform-reference-map]]
- [[ai-obsidian-bootstrap-prompt]]

## Quick Access
- [[kubernetes-kubectl-common-commands]]
- [[terraform-terraform-cli-workflow]]
- [[ai-rag-pipeline-template]]
- [[platform-reference-map]]
