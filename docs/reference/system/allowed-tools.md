# Allowed Tool Tokens

Shared skills reference tools via adapter-agnostic tokens (for example, `@BASH`). During rendering, the Enaible toolchain swaps each token for the tool name required by the target system template, similar to how `@ASK_USER_CONFIRMATION` is expanded per adapter.

## Canonical tokens

| Token            | Purpose / Native tool name (default)    |
| ---------------- | --------------------------------------- |
| `@BASH`          | Shell / terminal execution (`Bash`)     |
| `@BASH_OUTPUT`   | Capture bash output (`BashOutput`)      |
| `@KILL_SHELL`    | Terminate shell processes (`KillShell`) |
| `@READ`          | Read files or blobs (`Read`)            |
| `@WRITE`         | Write files (`Write`)                   |
| `@EDIT`          | Edit files (`Edit`)                     |
| `@MULTI_EDIT`    | Multi-file edits (`MultiEdit`)          |
| `@NOTEBOOK_READ` | Read notebook cells (`NotebookRead`)    |
| `@NOTEBOOK_EDIT` | Edit notebook cells (`NotebookEdit`)    |
| `@GREP`          | Pattern search (`Grep`)                 |
| `@GLOB`          | File globbing (`Glob`)                  |
| `@WEB_SEARCH`    | Perform web searches (`WebSearch`)      |
| `@WEB_FETCH`     | Fetch URLs (`WebFetch`)                 |
| `@TASK`          | Task tracking (`Task`)                  |
| `@TODO_WRITE`    | Write TODOs (`TodoWrite`)               |

Add more tokens here whenever a new tool must be referenced in shared skills. Keep names uppercase and prefixed with `@`.

## System mappings

The renderer maps every token to the proper tool string for each adapter listed below. When a system does not support `allowed-tools`, the token replacement still runs but the adapter ignores the value downstream.

| Token            | claude-code    | codex          | copilot          | cursor         | gemini         |
| ---------------- | -------------- | -------------- | ---------------- | -------------- | -------------- |
| `@BASH`          | `Bash`         | `Bash`         | `Bash`\*         | `Bash`         | `Bash`         |
| `@BASH_OUTPUT`   | `BashOutput`   | `BashOutput`   | `BashOutput`\*   | `BashOutput`   | `BashOutput`   |
| `@KILL_SHELL`    | `KillShell`    | `KillShell`    | `KillShell`\*    | `KillShell`    | `KillShell`    |
| `@READ`          | `Read`         | `Read`         | `Read`\*         | `Read`         | `Read`         |
| `@WRITE`         | `Write`        | `Write`        | `Write`\*        | `Write`        | `Write`        |
| `@EDIT`          | `Edit`         | `Edit`         | `Edit`\*         | `Edit`         | `Edit`         |
| `@MULTI_EDIT`    | `MultiEdit`    | `MultiEdit`    | `MultiEdit`\*    | `MultiEdit`    | `MultiEdit`    |
| `@NOTEBOOK_READ` | `NotebookRead` | `NotebookRead` | `NotebookRead`\* | `NotebookRead` | `NotebookRead` |
| `@NOTEBOOK_EDIT` | `NotebookEdit` | `NotebookEdit` | `NotebookEdit`\* | `NotebookEdit` | `NotebookEdit` |
| `@GREP`          | `Grep`         | `Grep`         | `Grep`\*         | `Grep`         | `Grep`         |
| `@GLOB`          | `Glob`         | `Glob`         | `Glob`\*         | `Glob`         | `Glob`         |
| `@WEB_SEARCH`    | `WebSearch`    | `WebSearch`    | `WebSearch`\*    | `WebSearch`    | `WebSearch`    |
| `@WEB_FETCH`     | `WebFetch`     | `WebFetch`     | `WebFetch`\*     | `WebFetch`     | `WebFetch`     |
| `@TASK`          | `Task`         | `Task`         | `Task`\*         | `Task`         | `Task`         |
| `@TODO_WRITE`    | `TodoWrite`    | `TodoWrite`    | `TodoWrite`\*    | `TodoWrite`    | `TodoWrite`    |

\*Copilot adapters do not expose Claude-style `allowed-tools` directly. The template ingests these canonical names and maps them to VS Code tool capabilities (for example, `Bash` → `terminal`, `Read` → `read`). Keep using the shared tokens so the renderer can continue to perform this translation automatically.

> **Note:** `allowed-tools` is currently enforced only by Claude Code. Other adapters ignore the field but still receive the resolved tool names. This lets us enable stricter gating per system without touching shared skills.
