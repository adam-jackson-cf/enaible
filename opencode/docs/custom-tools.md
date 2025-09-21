# OpenCode Custom Tools Documentation

_Source: https://opencode.ai/docs/custom-tools/ - Scraped on 2025-09-21_

## Overview

Custom tools extend OpenCode capabilities. They are functions the LLM can call during conversations.

## Tool Definition

Tools are defined as `.ts/.js` files in `.opencode/tool/` or globally in `~/.config/opencode/tool/`.

Use the `tool()` helper for type safety and validation. Define argument types with `tool.schema`, which is just Zod.

## Basic Tool Example

`.opencode/tool/database.ts`

```typescript
import { tool } from "@opencode-ai/plugin"
export default tool({
  description: "Query the project database",
  args: {
    query: tool.schema.string().describe("SQL query to execute"),
  },
  async execute(args) {
    // Your database logic here
    return `Executed query: ${args.query}`
  },
})
```

The filename becomes the tool name. This creates a `database` tool.

You can also import Zod directly and return a plain object.

## Multiple Tools in One File

You can export multiple tools from a single file. Each export becomes a separate tool with the name `<filename>_<exportname>`.

`.opencode/tool/math.ts`

```typescript
import { tool } from "@opencode-ai/plugin"
export const add = tool({
  description: "Add two numbers",
  args: {
    a: tool.schema.number().describe("First number"),
    b: tool.schema.number().describe("Second number"),
  },
  async execute(args) {
    return args.a + args.b
  },
})
export const multiply = tool({
  description: "Multiply two numbers",
  args: {
    a: tool.schema.number().describe("First number"),
    b: tool.schema.number().describe("Second number"),
  },
  async execute(args) {
    return args.a * args.b
  },
})
```

This creates two tools: `math_add` and `math_multiply`.

## Schema Validation

Use `tool.schema` to define tool arguments with validation and descriptions.

`.opencode/tool/calculator.ts`

```typescript
import { tool } from "@opencode-ai/plugin"
export default tool({
  description: "Perform mathematical calculations",
  args: {
    expression: tool.schema
      .string()
      .describe("Mathematical expression to evaluate"),
    precision: tool.schema.number().optional().describe("Decimal precision"),
  },
  async execute(args) {
    // Your calculation logic here
    return `Result: ${eval(args.expression).toFixed(args.precision || 2)}`
  },
})
```

## Session Context

Tools receive context about the current session.

`.opencode/tool/project.ts`

```typescript
import {
```
