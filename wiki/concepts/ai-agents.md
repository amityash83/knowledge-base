---
title: AI Agents
type: concept
domain: [ai-ml, devops]
status: stable
tags: [agents, automation, mcp]
sources: [raw-sources/archive/AI-Agents.md]
created: 2026-08-11
updated: 2026-08-11
---

# AI Agents

## Summary
An AI agent perceives input, decides, and takes action: LLM + tools + memory + execution = agent. Agents extend a plain LLM by giving it the ability to call tools and retain state across steps, rather than just answering a single prompt.

## Details

### Core capabilities
- Understand user intent
- Plan steps
- Execute actions
- Learn from feedback

### Architecture
```text
User Input
   ↓
LLM (Reasoning)
   ↓
Tool Selection
   ↓
Execution
   ↓
Memory Update
```

### Types of agents
- **Reactive agents** — no memory, single-step actions
- **Tool-using agents** — call APIs, execute scripts
- **Multi-step agents** — plan and execute multi-step workflows
- **Multi-agent systems** — multiple agents collaborating

### Key components
- **LLM** — the reasoning "brain" of the agent
- **Tools** — APIs, CLI commands, scripts the agent can invoke
- **Memory** — short-term (context window) and long-term (vector DB — see [[embeddings-and-vector-databases]])
- **Orchestrator** — controls the flow between reasoning, tool selection, and execution; see [[mcp-architecture]]

### This vault's intended agent roles
- **DevOps agent** — deploys apps
- **RAG agent** — answers queries grounded in [[retrieval-augmented-generation]]
- **Code agent** — generates code

## Open questions
- No concrete agent framework (LangGraph, AutoGPT-style loop) or memory system has been chosen yet — flagged as future expansion in the source note.

## Related
- [[mcp-architecture]]
- [[retrieval-augmented-generation]]
- [[artificial-intelligence]]
- [[devops-mcp-control-plane]]
