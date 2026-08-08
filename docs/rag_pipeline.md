# RAG Pipeline Documentation

## Overview

The RAG Pipeline connects the retrieval and generation components of the system.

It receives a user's question, retrieves relevant document chunks, builds a prompt, and generates an answer using the LLM.

## Responsibilities

The RAG Pipeline:

1. Receives the user's question.
2. Retrieves relevant document chunks.
3. Formats the retrieved context.
4. Builds the LLM prompt.
5. Sends the prompt to the Generator.
6. Returns the generated answer.

## Components

The RAG Pipeline uses:

- Retriever
- Prompt Builder
- Generator

## Basic Flow

User Question
      ↓
Retriever
      ↓
Relevant Chunks
      ↓
Format Context
      ↓
Prompt Builder
      ↓
Generator
      ↓
LLM
      ↓
Final Answer

## Example

answer = rag_pipeline.ask(
    "What does the book say about identity-based habits?",
    top_k=5
)

The pipeline handles the complete process internally.

## Current Limitations

The current pipeline is primarily designed for question answering using the top-k relevant chunks.

It does not yet handle:

- Whole-book summarisation.
- Global document insights.
- Chapter-level summarisation.
- Multi-document analysis.
- Query routing.
- Reranking.
- Source citations.

## Future Improvements

The RAG Pipeline can later be extended with:

- Query routing for different types of user requests.
- Whole-document summarisation.
- Chapter-level summarisation.
- Multi-document reasoning.
- Reranking of retrieved chunks.
- Source citations.
- RAG evaluation.
- Improved context management.

## Summary

The RAG Pipeline provides the complete workflow from a user's question to a generated answer.

It connects the Retriever, Prompt Builder, and Generator while keeping each component responsible for its own task.