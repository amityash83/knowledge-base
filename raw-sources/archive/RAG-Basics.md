# 📚 RAG Basics (Retrieval-Augmented Generation)

tags: #AI #RAG #LLM #KnowledgeSystem

---

## 📌 What is RAG?

RAG = Retrieval + Generation

It combines:

1. **Retriever** → Finds relevant data
2. **Generator (LLM)** → Generates answer

👉 Instead of relying only on model training, RAG uses **your own data**

---

## 🔹 Why RAG?

Problems with LLMs:

* Hallucination
* Limited knowledge
* No access to private data

👉 RAG solves this by:

* Injecting real-time knowledge
* Using your documents

---

## 🔹 How RAG Works

1. Store documents (Obsidian notes)
2. Convert into embeddings
3. Store in vector DB
4. Query → retrieve relevant chunks
5. Send to LLM → generate answer

---

## 🔹 Key Components

### 1. Data Source

* Obsidian notes
* PDFs
* Logs

### 2. Embeddings

* Convert text → vectors

👉 Related: [[AI Concepts]]

---

### 3. Vector Database

* Stores embeddings

Examples:

* FAISS
* Weaviate

---

### 4. Retriever

* Finds relevant chunks

---

### 5. LLM

* Generates final answer

---

## 🔹 RAG Architecture (Simple)

```text
User Query
   ↓
Retriever (Vector DB)
   ↓
Relevant Context
   ↓
LLM (GPT / Local Model)
   ↓
Answer
```

---

## 🔹 Your Use Case (Important 🚀)

* Obsidian → Knowledge Base
* Docker → Run vector DB
* MCP → Orchestrate queries

👉 This becomes:

> Your personal AI assistant

---

## 🔗 Related Notes

* [[AI Basics]]
* [[AI Concepts]]
* [[ML vs DL]]
* [[MCP Architecture]]

---

## 🚀 Future Expansion

* LangChain
* LlamaIndex
* Chunking strategies
* Embedding models
* Hybrid search

---
