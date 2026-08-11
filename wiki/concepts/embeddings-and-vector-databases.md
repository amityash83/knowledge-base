---
title: Embeddings and Vector Databases
type: concept
domain: [ai-ml]
status: stable
tags: [embeddings, vector-database, rag]
sources: [raw-sources/archive/AI-Concepts.md, raw-sources/archive/RAG-Basics.md, "raw-sources/archive/AI-RAG(Advance).md"]
created: 2026-08-11
updated: 2026-08-11
---

# Embeddings and Vector Databases

## Summary
Embeddings convert text into numeric vectors that capture semantic similarity, letting a system compare meaning rather than exact words. Vector databases store those embeddings and enable fast similarity search over them — the storage/retrieval backbone of any RAG system.

## Details

### Embeddings
- Convert text (or other content) into vectors of numbers.
- Similar meanings end up close together in vector space, which is what makes semantic search possible.
- Used in search, RAG retrieval, and recommendation systems.

### Vector databases
- Store embeddings and support fast nearest-neighbor / similarity search.
- Examples referenced across this vault's sources: Pinecone, Weaviate, FAISS.

## Open questions
- No vector DB has been selected or deployed for this vault's own use — remains a future decision, tracked under [[ai-rag-system-blueprint]].

## Related
- [[retrieval-augmented-generation]]
- [[artificial-intelligence]]
