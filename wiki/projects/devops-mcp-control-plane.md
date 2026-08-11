---
title: DevOps MCP Control Plane
type: project
domain: [devops, ai-ml]
status: active
tags: [mcp, devops, automation, agents, platform-engineering]
sources: [raw-sources/archive/devops-mcp-control-plane.md]
created: 2026-08-11
updated: 2026-08-11
---

# DevOps MCP Control Plane

## Summary
A modular control plane for running operational workflows through agents, tools, and shared knowledge — making routine platform work observable, reusable, and safe to automate. Implements the [[mcp-architecture]] concept as an actual project.

## Details

### Design intent
- MCP exposes tools, data sources, and actions to agents in a structured way.
- The control plane separates policy, execution, observability, and knowledge retrieval — these shouldn't be tangled together.
- Shared knowledge notes (this wiki) reduce repeated prompting and improve agent consistency across runs.

### Intended flow
1. Register MCP-capable tools and data sources.
2. Define guardrails for operational actions such as deployments or diagnostics.
3. Route requests through intent classification and policy checks.
4. Attach retrieval from wiki pages before execution (see [[retrieval-augmented-generation]]).
5. Log results for audit and iterative improvement.

```bash
# Example MCP-oriented development workflow
git checkout -b codex/mcp-control-plane
```

## Open questions
- No policy engine, guardrail implementation, or audit logging has actually been built yet — this remains a design intent captured from the original source note, not a running system.

## Related
- [[mcp-architecture]]
- [[ai-agents]]
- [[retrieval-augmented-generation]]
- [[ai-rag-system-blueprint]]
