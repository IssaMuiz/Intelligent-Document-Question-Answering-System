# Prompt Builder Documentation

## Overview

The Prompt Builder is responsible for creating the prompt that is sent to the Large Language Model (LLM).

It combines the user's question, retrieved document context, and instructions for the LLM.

## Responsibilities

The Prompt Builder:

- Receives the user's question.
- Receives retrieved document context.
- Provides instructions to the LLM.
- Creates the final prompt.

It does not:

- Retrieve documents.
- Generate embeddings.
- Search the vector store.
- Generate the final answer.

## Input

The Prompt Builder receives:

- `question`: User's question.
- `context`: Relevant document chunks retrieved by the Retriever.

## Output

It returns a formatted prompt containing:

- Instructions.
- Retrieved context.
- User question.
- Answer instruction.

## Basic Flow

User Question + Retrieved Context
            ↓
      Prompt Builder
            ↓
       Final Prompt
            ↓
            LLM

## Grounding

The prompt instructs the LLM to answer using only the provided document context.

If the required information is not available in the context, the LLM is instructed to say that it could not find the answer in the provided documents.

## Future Improvements

The Prompt Builder can later support:

- Citations.
- Different response formats.
- Summarisation prompts.
- Structured outputs.
- Different prompts for different query types.