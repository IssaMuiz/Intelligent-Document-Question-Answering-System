# Retriever Documentation

## Overview

The **Retriever** is responsible for retrieving the most relevant document chunks for a user's query. It acts as the orchestration layer between the Embedding Generator and the Vector Store.

Unlike the Vector Store, which focuses only on storing and searching vectors, the Retriever manages the complete retrieval workflow by converting a user's natural language question into an embedding, performing semantic search, and formatting the retrieved results for downstream Large Language Models (LLMs).

The Retriever represents the online query pipeline of the Intelligent Document Question Answering System.

---

## Objectives

The Retriever is designed to:

- Convert user queries into embedding vectors.
- Search the Vector Store for semantically similar document chunks.
- Return the most relevant chunks.
- Format retrieved chunks into context suitable for LLM prompts.
- Provide a clean interface for the application's retrieval pipeline.

---

## Why Do We Need a Retriever?

Without a Retriever, every application component would need to manually execute the following steps:

1. Generate a query embedding.
2. Search the Vector Store.
3. Retrieve the top-k results.
4. Format the retrieved chunks.

This would duplicate logic across the codebase.

The Retriever encapsulates this workflow into a single reusable component.

Instead of writing:

```python
query_embedding = embedder.embed_text(query)
results = vector_store.search(query_embedding)
context = format_context(results)
```

the application simply calls:

```python
results = retriever.retrieve(query)
context = retriever.format_context(results)
```

This improves readability, maintainability, and extensibility.

---

## Responsibilities

The Retriever is responsible for:

- Embedding user queries.
- Retrieving relevant document chunks.
- Formatting retrieved chunks.
- Coordinating retrieval components.

The Retriever is **not** responsible for:

- Parsing PDF documents.
- Cleaning text.
- Chunking documents.
- Generating document embeddings.
- Storing vectors.
- Answer generation.

---

## Query Pipeline

```text
User Question
      │
      ▼
Embed Query
      │
      ▼
Embedding Generator
      │
      ▼
Query Embedding
      │
      ▼
Vector Store Search
      │
      ▼
Top-k Results
      │
      ▼
Format Context
      │
      ▼
LLM Ready Context
```

---

## Class Structure

```text
Retriever
│
├── __init__()
├── embed_query()
├── retrieve()
└── format_context()
```

---

## Method Descriptions

### `__init__()`

Initializes the Retriever.

Dependencies:

- EmbeddingGenerator
- VectorStore

The Retriever receives these dependencies through dependency injection rather than creating them internally.

Benefits include:

- Loose coupling.
- Easier testing.
- Easier replacement of components.
- Better software architecture.

---

### `embed_query()`

Converts a user's natural language query into an embedding vector.

Input:

```python
"What is habit stacking?"
```

Output:

```python
[
    0.057,
    -0.072,
    ...
]
```

The returned embedding is later used for semantic similarity search.

---

### `retrieve()`

Coordinates the semantic retrieval workflow.

Processing Steps:

1. Receive a user question.
2. Generate a query embedding.
3. Search the Vector Store.
4. Return the top-k ranked document chunks.

Output:

```python
[
    {
        "page_number": 12,
        "text": "...",
        "similarity": 0.96
    },
    ...
]
```

---

### `format_context()`

Converts retrieved document chunks into a single formatted context string suitable for prompting an LLM.

Input:

```python
[
    {...},
    {...},
    {...}
]
```

Output:

```text
Page 12
...

--------------------------------------------------------------------------------

Page 15
...

--------------------------------------------------------------------------------

Page 18
...
```

This formatted context becomes part of the final LLM prompt.

---

## Dependencies

The Retriever depends on:

### Embedding Generator

Responsible for converting text into dense vector embeddings.

Used by:

```python
embed_query()
```

### Vector Store

Responsible for semantic similarity search.

Used by:

```python
retrieve()
```

The Retriever does not implement embedding generation or vector search itself. Instead, it coordinates these components.

---

## Engineering Decisions

### Dependency Injection

Instead of creating dependencies internally, the Retriever receives them during initialization.

Example:

```python
retriever = Retriever(
    embedder=embedder,
    vector_store=vector_store
)
```

This improves modularity and allows components to be replaced independently.

---

### Separation of Responsibilities

Each component in the retrieval pipeline performs a single responsibility.

```text
Embedding Generator
        │
        ▼
Creates embeddings

Vector Store
        │
        ▼
Searches embeddings

Retriever
        │
        ▼
Coordinates the workflow
```

This design follows the **Single Responsibility Principle (SRP)**.

---

### Reusability

The Retriever provides a simple interface for any application layer.

Examples include:

- Streamlit applications.
- FastAPI services.
- REST APIs.
- Evaluation scripts.
- Command-line interfaces.

Regardless of the application, retrieval is always performed through:

```python
retriever.retrieve(query)
```

---

## Advantages

The Retriever provides:

- Clean abstraction.
- Reduced code duplication.
- Improved maintainability.
- Better modularity.
- Easier testing.
- Future extensibility.

Future improvements such as query expansion, hybrid search, reranking, or metadata filtering can be added inside the Retriever without changing the application's public interface.

---

## Current Limitations

The Retriever currently:

- Performs semantic retrieval only.
- Does not rerank retrieved documents.
- Does not support hybrid keyword + semantic search.
- Does not filter results using metadata.
- Does not perform query rewriting or expansion.

These features can be added in future versions without changing the external API.

---

## Summary

The Retriever is the orchestration layer of the Intelligent Document Question Answering System.

It bridges the gap between user questions and semantic retrieval by coordinating query embedding, vector search, and context preparation.

Rather than implementing retrieval algorithms itself, the Retriever delegates responsibilities to specialized components while exposing a clean and reusable interface to the rest of the application.

This modular design closely follows modern Retrieval-Augmented Generation (RAG) architectures used in production AI systems.