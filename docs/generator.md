# Generator Documentation

## Overview

The Generator is responsible for sending prompts to the Large Language Model (LLM) and returning the generated response.

The current implementation uses Ollama with the Qwen 2.5 3B model.

## Responsibilities

The Generator:

- Receives a complete prompt.
- Sends the prompt to Ollama.
- Specifies the model to use.
- Receives the generated response.
- Returns the response.

It does not:

- Parse documents.
- Process text.
- Generate embeddings.
- Search the vector store.
- Build prompts.

## Model

Current model:

Qwen 2.5 3B

The model runs locally through Ollama.

## Configuration

The Generator accepts:

- `model`: Name of the Ollama model.
- `base_url`: URL of the Ollama server.

Default Ollama URL:

`http://localhost:11434`

## Basic Flow

Prompt
  ↓
Generator
  ↓
Ollama
  ↓
Qwen 2.5 3B
  ↓
Generated Answer

## Future Improvements

The Generator can later support:

- OpenAI API.
- Other hosted LLM APIs.
- Different local models.
- Streaming responses.
- Temperature control.
- Token limits.
- Retry mechanisms.