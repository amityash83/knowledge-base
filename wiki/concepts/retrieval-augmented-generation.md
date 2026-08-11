---
title: Retrieval-Augmented Generation
type: concept
domain: [ai-ml, devops]
status: stable
tags: [rag, llm, retrieval, embeddings]
sources: [raw-sources/archive/RAG-Basics.md, "raw-sources/archive/AI-RAG(Advance).md", raw-sources/archive/AI-Concepts.md, raw-sources/archive/llm-rag-basic-concepts.md, raw-sources/archive/ai-rag-pipeline-template.md]
created: 2026-08-11
updated: 2026-08-11
---

# Retrieval-Augmented Generation

## Summary
RAG combines a **retriever** (finds relevant data) with a **generator** (an LLM that produces the answer). Instead of relying only on what a model learned during training, RAG grounds generation in your own data, retrieved at query time.

## Details

### Why RAG
LLMs on their own have three problems: hallucination, limited/frozen knowledge, and no access to private data. RAG addresses this by injecting real-time, relevant knowledge from your own documents at query time.

### How it works, end to end
1. Normalize source documents with consistent metadata and headings.
2. Chunk documents into retrieval units, aligned to headings/semantic boundaries (not arbitrary fixed windows) — this is what keeps context efficient without losing meaning.
3. Convert chunks into embeddings (vectors) and store them with metadata.
4. On a query, retrieve the most relevant chunks by semantic similarity, then rerank.
5. Send only the retrieved context to the LLM and ask it to answer from that context — this is what makes answers grounded rather than speculative.

Conceptual pipeline:
```text
parse_markdown -> chunk_sections -> embed_chunks -> retrieve -> rerank -> answer
```

Minimal template:
```python
documents = load_markdown()
chunks = split_by_headings(documents)
vectors = embed(chunks)
results = retrieve(query, vectors, filters={"domain": "ai-ml"})
answer = generate(query, context=results)
```

### Key components
- **Data source** — Obsidian notes, PDFs, logs (see [[artificial-intelligence]] for what counts as a data source)
- **Embeddings** — text converted to vectors; see [[embeddings-and-vector-databases]]
- **Vector database** — stores embeddings for fast similarity search; see [[embeddings-and-vector-databases]]
- **Retriever** — finds the relevant chunks for a query
- **Reranker** — determines whether generation ends up grounded or speculative
- **LLM** — generates the final, cited answer

### RAG as a layered architecture
1. **Data layer** — notes, docs, logs
2. **Processing layer** — chunking, cleaning
3. **Embedding layer** — text → vectors
4. **Storage layer** — vector DB
5. **Retrieval layer** — search relevant data
6. **Generation layer** — LLM produces the response

### Advanced considerations
- **Chunking strategies** — fixed-size, semantic, or sliding-window; semantic chunking (by heading/section) generally preserves meaning best for note-style content.
- **Retrieval types** — dense (embedding similarity) vs. hybrid (dense + keyword/BM25).
- **Context optimization** — trimming retrieved context to reduce token usage while preserving accuracy.
- **Metadata filtering** — filtering retrieval by domain, difficulty, project, or recency improves precision beyond similarity alone.

### This vault's own RAG use case
This vault *is* a RAG-style system in practice: Obsidian notes are the knowledge base, an embedding step would index them, a vector DB would store them, and an LLM (Claude Code) generates grounded answers — orchestrated through the `/ask` operation defined in [CLAUDE.md](../../CLAUDE.md). See [[ai-rag-system-blueprint]] for the project that formalizes this.

## Open questions
- No chunking strategy, embedding model, or vector DB has actually been chosen/implemented yet for this vault — these were listed as future expansion in the original sources (LangChain, LlamaIndex, hybrid search) but nothing was decided.

## Related
- [[embeddings-and-vector-databases]]
- [[ai-agents]]
- [[mcp-architecture]]
- [[ai-rag-system-blueprint]]
- [[devops-mcp-control-plane]]
