---
title: AI RAG System Blueprint
type: project
domain: [ai-ml]
status: active
tags: [rag, ai, retrieval, embeddings, knowledge-base]
sources: [raw-sources/archive/ai-rag-system-blueprint.md]
created: 2026-08-11
updated: 2026-08-11
---

# AI RAG System Blueprint

## Summary
A retrieval-augmented generation system built on this vault's own structured content, using embeddings and metadata-aware search. Focused on retrieval quality, document chunking, and operational maintainability rather than research novelty. This is the project umbrella for actually implementing the [[retrieval-augmented-generation]] concept against this wiki.

## Details

### Design intent
- High-quality note structure improves chunk boundaries, metadata filters, and recall — which is exactly what the `wiki/` page schema in [CLAUDE.md](../../CLAUDE.md) is designed for.
- Retrieval quality depends on explicit language, linked context, and consistent tagging (see the "self-contained, explicit" note convention).

### Intended flow
1. Ingest markdown notes and parse frontmatter.
2. Split notes into chunks aligned to headings and semantic sections.
3. Generate embeddings and store vectors with metadata filters.
4. Retrieve by semantic similarity with domain-aware reranking.
5. Provide the selected chunks to an LLM with citation-friendly context.

### Use cases
- Building an internal assistant over this vault's DevOps and AI content
- Answering operational questions with grounded, cited knowledge
- Powering MCP agents with retrieval-backed context (see [[devops-mcp-control-plane]])

## Open questions
- No embedding model, vector store, or actual indexing pipeline has been implemented yet. The current `/ask` operation (see [CLAUDE.md](../../CLAUDE.md)) is a manual, Claude-driven approximation of this blueprint rather than the automated pipeline described here.

## Related
- [[retrieval-augmented-generation]]
- [[embeddings-and-vector-databases]]
- [[devops-mcp-control-plane]]
- [[llm-wiki-pattern]]
