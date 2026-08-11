---
title: MCP Architecture (Model Control Plane)
type: concept
domain: [devops, ai-ml]
status: stable
tags: [mcp, architecture, agents, devops]
sources: [raw-sources/archive/MCP-Architecture.md]
created: 2026-08-11
updated: 2026-08-11
---

# MCP Architecture (Model Control Plane)

## Summary
MCP (in this vault's usage, "Model Control Plane") is a system for managing AI agents, orchestrating workflows, and integrating DevOps tools under one control layer — the answer to "too many tools, no central intelligence."

## Details

### Why MCP
Problem: too many disconnected tools (GitHub, Jenkins, Kubernetes) with no unifying intelligence layer. MCP provides:
- A unified control layer
- AI-driven automation across tools
- A modular architecture that can grow tool-by-tool

### Core components
1. **Input layer** — user commands, API requests
2. **Orchestrator** — routes tasks, decides which agent handles a request (see [[ai-agents]])
3. **Agents** — DevOps agent, RAG agent, code agent
4. **Tool integrations** — Kubernetes, GitHub, Jenkins
5. **Memory layer** — vector DB, logs, history (see [[embeddings-and-vector-databases]])
6. **Execution layer** — runs tasks, typically in Docker/sandboxes

### Architecture flow
```text
User Request
   ↓
MCP Orchestrator
   ↓
Agent Selection
   ↓
Tool Execution
   ↓
Response + Memory Update
```

### This vault's role in that picture
- **Obsidian** → Knowledge layer
- **RAG** → Reasoning/intelligence layer (see [[retrieval-augmented-generation]])
- **MCP** → Control plane tying the two to execution

The stated ambition in the original source was a personal "Devin-like" system — an agent that reads this knowledge base and executes DevOps tasks against it.

## Open questions
- Multi-agent routing, audit trails, replay, and self-healing workflows were named as future expansion but never designed in detail.

## Related
- [[ai-agents]]
- [[retrieval-augmented-generation]]
- [[devops-mcp-control-plane]]
- [[aiops]]
