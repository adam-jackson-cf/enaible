# Plugins

Plugins allow you to extend opencode by hooking into events and customizing behavior. You can create plugins to add features, integrate with external services, or modify opencode’s default behavior.

---

## Create a plugin

A plugin is a JavaScript or TypeScript module that exports one or more plugin functions. Each function receives a context object and returns a hooks object.

---

### Location

Plugins are loaded from:

1. `.opencode/plugin` directory in your project, or
2. Globally from `~/.config/opencode/plugin`

---

### Basic structure

```js
export const MyPlugin = async ({ project, client, $, directory, worktree }) => {
  console.log("Plugin initialized!")

  return {
    // Hook implementations go here
  }
}
```

The plugin function receives:

- `project`: current project information
- `directory`: current working directory
- `worktree`: git worktree path
- `client`: an opencode SDK client for interacting with the AI
- `$`: Bun’s shell API (https://bun.com/docs/runtime/shell) for executing commands

---

### TypeScript support

For TypeScript plugins, import the Plugin type and annotate your export:

```ts
import type { Plugin } from "@opencode-ai/plugin"

export const MyPlugin: Plugin = async ({
  project,
  client,
  $,
  directory,
  worktree,
}) => {
  return {
    // Type-safe hook implementations
  }
}
```

---

## Examples

Below are example plugins demonstrating common use cases.

---

### Send notifications

Send a macOS notification when a session completes:

```js
export const NotificationPlugin = async ({
  project,
  client,
  $,
  directory,
  worktree,
}) => {
  return {
    event: async ({ event }) => {
      if (event.type === "session.idle") {
        await $`osascript -e 'display notification "Session completed!" with title "opencode"'`
      }
    },
  }
}
```

This example uses `osascript` to run AppleScript on macOS.

---

### .env protection

Prevent opencode from reading `.env` files:

```js
export const EnvProtection = async ({
  project,
  client,
  $,
  directory,
  worktree,
}) => {
  return {
    "tool.execute.before": async (input, output) => {
      if (input.tool === "read" && output.args.filePath.includes(".env")) {
        throw new Error("Do not read .env files")
      }
    },
  }
}
```

---

### Custom tools

Plugins can add custom tools that opencode can call:

```ts
import type { Plugin } from "@opencode-ai/plugin"
import { tool } from "@opencode-ai/plugin"

export const CustomToolsPlugin: Plugin = async (ctx) => {
  return {
    tool: {
      mytool: tool({
        description: "This is a custom tool",
        args: {
          foo: tool.schema.string(),
        },
        async execute(args, ctx) {
          return `Hello ${args.foo}!`
        },
      }),
    },
  }
}
```

The `tool` helper creates a custom tool with:

- `description`: what the tool does
- `args`: Zod-like schema for the tool’s arguments
- `execute`: function invoked when the tool is called

Custom tools appear alongside built-in tools in opencode.
