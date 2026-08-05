# Vector Store Documentation

## Overview

The **Vector Store** is responsible for storing, searching, saving, and loading document embeddings. It acts as the retrieval engine of the Intelligent Document Question Answering System by enabling semantic similarity search over embedded document chunks.

Unlike a traditional database that searches using exact values or keywords, the Vector Store searches using embedding vectors, allowing it to retrieve text based on meaning rather than exact word matches.

This implementation is intentionally built from scratch to demonstrate the core concepts behind semantic retrieval before introducing production-grade vector databases such as FAISS or ChromaDB.

---

## Objectives

The Vector Store is designed to:

- Store embedding records in memory.
- Add individual or multiple embedding records.
- Compute cosine similarity between embeddings.
- Retrieve the most relevant document chunks.
- Persist indexed embeddings to disk.
- Reload saved indexes without reprocessing documents.

---

## Why Do We Need a Vector Store?

After document chunking and embedding generation, every chunk is represented as a numerical vector.

Example:

```python
{
    "chunk_id": "atomic_habits_chunk_001",
    "page_number": 5,
    "text": "...",
    "embedding": [...]
}
```

Without a Vector Store, there would be no efficient way to search through these embeddings when answering user questions.

The Vector Store bridges the gap between document indexing and information retrieval.

---

## Responsibilities

The Vector Store is responsible for:

- Storing embedding records.
- Performing semantic similarity search.
- Ranking retrieved results.
- Saving indexed data.
- Loading indexed data.

The Vector Store is **not** responsible for:

- Parsing PDF documents.
- Cleaning text.
- Chunking text.
- Generating embeddings.
- Generating answers with an LLM.

---

## Class Structure

```text
VectorStore
│
├── __init__()
├── add()
├── add_many()
├── cosine_similarity()
├── search()
├── save()
└── load()
```

---

## Method Descriptions

### `__init__()`

Initializes an empty Vector Store.

Responsibilities:

- Create internal storage for embedding records.

Output:

```python
self.records = []
```

---

### `add()`

Adds a single embedding record to the Vector Store.

Input:

```python
record
```

Output:

The record is appended to the internal storage.

---

### `add_many()`

Adds multiple embedding records.

Rather than duplicating logic, this method internally calls `add()` for every record.

This design improves maintainability and follows object-oriented best practices.

---

### `cosine_similarity()`

Computes the cosine similarity between two embedding vectors.

Input:

- Query embedding
- Stored embedding

Output:

```python
float
```

Similarity scores range approximately from:

```text
-1.0  ← Opposite meanings

 0.0  ← Unrelated

 1.0  ← Identical semantic meaning
```

Since embeddings are normalized during generation, cosine similarity is computed using the dot product.

---

### `search()`

Retrieves the most semantically similar document chunks.

Processing Steps:

1. Compare the query embedding with every stored embedding.
2. Compute cosine similarity.
3. Attach similarity scores.
4. Sort by descending similarity.
5. Return the top-k results.

Output:

```python
[
    {
        "chunk_id": "...",
        "text": "...",
        "similarity": 0.94
    },
    ...
]
```

---

### `save()`

Serializes the Vector Store to disk using Python's `pickle` module.

Purpose:

Avoid rebuilding embeddings every time the application starts.

Output:

```text
vector_store.pkl
```

---

### `load()`

Loads a previously saved Vector Store from disk.

Responsibilities:

- Restore embedding records.
- Enable immediate retrieval without reprocessing documents.

---

## Internal Data Structure

The Vector Store maintains embedding records as a list of dictionaries.

```python
[
    {
        "chunk_id": "...",
        "page_number": 3,
        "text": "...",
        "embedding": [...]
    },

    {
        ...
    }
]
```

Each record preserves both semantic vectors and document metadata.

---

## Retrieval Workflow

```text
User Question
      │
      ▼
Embedding Generator
      │
      ▼
Query Embedding
      │
      ▼
Vector Store
      │
      ▼
Cosine Similarity
      │
      ▼
Rank Results
      │
      ▼
Top-k Chunks
```

---

## Input

Example embedding record:

```python
{
    "chunk_id": "atomic_habits_chunk_001",
    "page_number": 5,
    "text": "...",
    "embedding": [...]
}
```

---

## Output

Example search results:

```python
[
    {
        "chunk_id": "page12_chunk_1",
        "page_number": 12,
        "text": "...",
        "similarity": 0.956
    },

    {
        "chunk_id": "atomic_habits_chunk_031",
        "page_number": 18,
        "text": "...",
        "similarity": 0.943
    }
]
```

---

## Engineering Decisions

### In-Memory Storage

Embedding records are stored in a Python list to simplify understanding before introducing specialized vector indexes.

### Encapsulation

`add_many()` reuses `add()` instead of duplicating insertion logic, making future enhancements easier.

### Brute-Force Search

The current implementation compares the query embedding against every stored embedding.

This approach has a time complexity of **O(n)** and is suitable for learning and small datasets.

Production systems replace this with Approximate Nearest Neighbor (ANN) indexing using tools such as FAISS.

### Persistence

The Vector Store uses Python's `pickle` module for serialization, allowing indexed embeddings to be reused across application sessions.

---

## Limitations

Current implementation:

- Linear search complexity (O(n)).
- Entire index stored in RAM.
- Uses Pickle for persistence.

Future improvements:

- FAISS indexing.
- ChromaDB integration.
- Persistent vector databases.
- Approximate Nearest Neighbor search.
- Cloud-hosted vector storage.

---

## Summary

The Vector Store is the semantic retrieval engine of the Intelligent Document Question Answering System.

It stores document embeddings, performs cosine similarity search, ranks document chunks by semantic relevance, and supports persistence through save and load operations.

Although intentionally implemented with a simple in-memory structure for educational purposes, the overall architecture mirrors production Retrieval-Augmented Generation (RAG) systems and provides the conceptual foundation for integrating high-performance vector databases such as FAISS, ChromaDB, Pinecone, or Milvus.