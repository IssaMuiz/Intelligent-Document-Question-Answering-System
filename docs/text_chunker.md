# 05. Text Chunker

## Overview

The Text Chunker is the third core component of the Intelligent Document Question Answering System. Its responsibility is to divide cleaned document text into smaller, semantically meaningful segments that can be embedded, indexed, and retrieved efficiently.

Large Language Models and embedding models cannot effectively represent entire books or long documents as a single vector. Instead, documents are divided into smaller chunks that preserve sufficient context while remaining specific to a particular topic.

The chunker converts a cleaned document into a collection of structured chunks, each containing both text and metadata required for retrieval and source attribution.

---

# Objectives

The objectives of the Text Chunker are to:

- Split cleaned document text into manageable pieces.
- Preserve semantic context using overlapping chunks.
- Maintain traceability back to the original document.
- Produce retrieval-ready chunks for embedding generation.
- Preserve useful metadata for downstream components.

---

# Why Chunking Matters

Embedding an entire document into a single vector is rarely effective.

A long document often discusses multiple topics, making a single embedding too general to accurately represent any specific section.

For example, a book may discuss:

- Habit formation
- Motivation
- Productivity
- Decision making
- Personal growth

Representing all these topics with a single embedding reduces retrieval precision.

Chunking solves this problem by dividing the document into smaller, focused units that can be independently embedded and retrieved.

---

# Design Philosophy

The Text Chunker follows several software engineering principles.

## 1. Single Responsibility Principle (SRP)

The chunker is responsible only for dividing cleaned text into retrieval-ready chunks.

It does **not**:

- Parse PDF documents.
- Clean extracted text.
- Generate embeddings.
- Store vectors.
- Retrieve information.
- Generate answers.

Each component performs one clearly defined responsibility.

---

## 2. Metadata Preservation

Every chunk retains metadata linking it back to its source page.

This enables future components to provide accurate citations such as:

> Source: Atomic Habits, Page 42

Maintaining traceability is essential for trustworthy Question Answering systems.

---

## 3. Retrieval-Oriented Design

The chunking strategy is designed to optimize semantic retrieval rather than human readability.

The goal is to maximize retrieval accuracy while preserving enough context for downstream language models.

---

# Chunking Strategy

Version 1 uses **fixed-size overlapping word-based chunking**.

Configuration:

- Chunk Size: **300 words**
- Chunk Overlap: **50 words**

This means each chunk contains approximately 300 words, while the final 50 words of one chunk become the first 50 words of the next chunk.

Example:

```
Chunk 1

Words 1 – 300

Chunk 2

Words 251 – 550

Chunk 3

Words 501 – 800
```

The overlapping region preserves context across chunk boundaries.

---

# Why Overlap?

Without overlap:

```
Chunk 1

...machine learning is transforming

Chunk 2

healthcare through better diagnosis...
```

The sentence is split across two chunks, reducing semantic coherence.

With overlap:

```
Chunk 1

...machine learning is transforming healthcare...

Chunk 2

...transforming healthcare through better diagnosis...
```

The shared context improves embedding quality and retrieval performance.

---

# Why Word-Based Chunking?

Version 1 performs chunking based on words rather than characters.

Advantages:

- Avoids splitting words.
- Produces more natural chunks.
- Easier to reason about.
- Suitable for books and research papers.

Future versions may implement token-based chunking for closer alignment with transformer models.

---

# Architecture

```
Clean Document
       │
       ▼
TextChunker.chunk()
       │
       ├──────────────┐
       ▼              ▼
chunk_page()      create_chunk()
       │
       ▼
Structured Chunks
```

---

# Workflow

The chunking pipeline follows these steps:

1. Receive a cleaned document.
2. Process one page at a time.
3. Split page text into overlapping chunks.
4. Generate metadata for every chunk.
5. Return a list of structured chunks.

---

# Methods

## chunk()

Coordinates the chunking process for the entire document.

Responsibilities:

- Iterate through every page.
- Call `chunk_page()` for each page.
- Combine all generated chunks.
- Return the complete list of chunks.

---

## chunk_page()

Splits a single page into overlapping chunks.

Responsibilities:

- Split text into words.
- Apply the configured chunk size.
- Apply chunk overlap.
- Generate chunk text.
- Create structured chunk objects.

---

## create_chunk()

Constructs the final chunk dictionary.

Each chunk contains:

- Unique chunk identifier
- Chunk index
- Source page number
- Chunk text
- Word count

This standardized structure is used throughout the remainder of the RAG pipeline.

---

# Input Structure

The chunker accepts the cleaned document produced by the Text Preprocessor.

```python
{
    "filename": "...",
    "metadata": {...},
    "pages": [...]
}
```

---

# Output Structure

The chunker returns a list of structured chunks.

```python
[
    {
        "chunk_id": "page_3_chunk_0",
        "chunk_index": 0,
        "page_number": 3,
        "text": "...",
        "word_count": 287
    },
    {
        "chunk_id": "page_3_chunk_1",
        "chunk_index": 1,
        "page_number": 3,
        "text": "...",
        "word_count": 300
    }
]
```

Each chunk serves as an independent retrieval unit.

---

# Design Decisions

## Why use fixed-size chunks?

Fixed-size chunking is simple, deterministic, and easy to evaluate.

It provides a solid baseline before introducing more advanced chunking strategies.

---

## Why use overlapping chunks?

Overlap reduces information loss at chunk boundaries.

Important ideas that span two chunks remain partially visible in both embeddings, improving retrieval quality.

---

## Why preserve page numbers?

Maintaining page numbers enables accurate source attribution during Question Answering.

Even after chunking, every chunk can be traced back to its location in the original document.

---

## Why return a list instead of another document dictionary?

The next stage of the pipeline—embedding generation—operates on individual chunks rather than entire documents.

Returning a list simplifies downstream processing.

---

# Current Capabilities

Version 1 of the Text Chunker can:

- Generate fixed-size chunks.
- Produce overlapping chunks.
- Preserve source page numbers.
- Assign unique chunk identifiers.
- Calculate chunk word counts.
- Produce retrieval-ready structured chunks.

---

# Current Limitations

The current implementation has several limitations.

It does not yet support:

- Cross-page chunking
- Sentence-aware chunking
- Paragraph-aware chunking
- Recursive chunking
- Semantic chunking
- Token-based chunking
- Table-aware chunking
- Multi-document chunk linking

These enhancements will be considered in future iterations.

---

# Lessons Learned

Developing the Text Chunker reinforced several important engineering concepts:

- Chunk quality has a direct impact on retrieval quality.
- Overlapping chunks preserve context across boundaries.
- Metadata is as important as the chunk text itself.
- Chunk size represents a balance between context and specificity.
- Modular design makes it easier to experiment with different chunking strategies.

---

# Future Improvements

Future versions of the chunker may include:

- Recursive chunking
- Sentence-aware chunking
- Semantic chunking
- Token-based chunking
- Cross-page chunking
- Adaptive chunk sizes
- Layout-aware chunking
- Multi-format document support

These improvements aim to increase retrieval accuracy while maintaining scalability.

---

# Next Step

With parsing, preprocessing, and chunking complete, the next stage of the pipeline is **Embedding Generation**.

The embedding component will transform each text chunk into a dense vector representation, enabling semantic search within the vector database.