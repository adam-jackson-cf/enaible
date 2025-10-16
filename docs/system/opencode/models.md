# OpenCode Models Documentation

## Overview

OpenCode uses the [AI SDK](https://ai-sdk.dev/) and [Models.dev](https://models.dev) to support **75+ LLM providers** and local model running.

## Providers

Most popular providers are preloaded by default. Providers can be added through `opencode auth login`.

## Selecting a Model

To select a model, type:

```
/models
```

## Recommended Models

Top recommended models for code generation and tool calling:

- Claude Sonnet 4
- Claude Opus 4
- Kimi K2
- Qwen3 Coder
- GPT 4.1
- Gemini 2.5 Pro

## Setting a Default Model

Configure in `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "lmstudio/google/gemma-3n-e4b"
}
```

## Model Configuration

Global model configuration example:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "openai": {
      "models": {
        "gpt-5": {
          "options": {
            "reasoningEffort": "high",
            "textVerbosity": "low"
          }
        }
      }
    }
  }
}
```

## Model Loading Priority

1. Command line flag (`--model` or `-m`)
2. OpenCode config model list
3. Last used model
4. Internal priority model

**Source**: Mock documentation from WebFetch
**Date Extracted**: 2025-09-10
