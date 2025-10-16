# Enaible CLI Migration Guide

## Overview

This playbook explains how to onboard teams to the Enaible CLI, replacing legacy prompt path probing with standardized commands and managed artifacts.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) 0.7+ available on PATH (via `pip install uv` or system package)
- Existing AI-Assisted Workflows checkout (repo root assumed)

## Local Developer Workflow

1. **Sync the Enaible workspace**
   ```bash
   uv sync --project tools/enaible
   ```
2. **Run CLI unit tests**
   ```bash
   uv run --project tools/enaible pytest tools/enaible/tests -v
   ```
3. **Verify prompt drift**
   ```bash
   uv run --project tools/enaible enaible prompts diff
   ```
4. **(Optional) Capture environment diagnostics**
   ```bash
   uv run --project tools/enaible enaible doctor --json
   ```

## Shared Prompt Variables

All shared prompts define their inputs via a standardized markdown table:

```md
## Variables

| Token          | Type                      | Description                                       |
| -------------- | ------------------------- | ------------------------------------------------- |
| `$TARGET_PATH` | positional #1 (REQUIRED)  | Path to analyze; defaults to the current project. |
| `$VERBOSE`     | flag --verbose (OPTIONAL) | Enable verbose logging.                           |
```

- **Token** – Always `$UPPER_SNAKE_CASE`, matching the placeholder used inside the prompt body.
- **Type** – One of `positional #<n>`, `flag --name`, `named --name`, or `config`, optionally suffixed with `(REQUIRED)` / `(OPTIONAL)`.
- **Description** – Human-readable guidance that may restate required/optional semantics.

The Enaible renderer parses this table, removes it from the shared body, and re-renders a system-specific `## Variables` section while wiring positional arguments into Claude frontmatter (`argument-hint`) and Codex/OpenCode bindings. Always update the table when adding or changing prompt inputs.

## Installation Modes

Use `enaible install <system>` to materialize system assets (`claude-code`, `opencode`, or `codex`). Available modes:

| Mode              | Behavior                                                                                 |
| ----------------- | ---------------------------------------------------------------------------------------- |
| `merge` (default) | Adds new files and updates managed ones, preserving unmanaged files.                     |
| `update`          | Overwrites managed files only when they already exist at the destination.                |
| `sync`            | Ensures managed files match the source; skips unmanaged files but rewrites managed ones. |
| `fresh`           | Recreates the destination from scratch before installing assets.                         |

Example (project scope):

```bash
uv run --project tools/enaible enaible install claude-code --target /path/to/project --mode merge
```

## Rollout Phases

1. **Pilot** – Regenerate `analyze-security` and `get-codebase-primer` prompts, validate in each system.
2. **Adoption** – Update repos to call `enaible analyzers run` and render prompts during CI.
3. **Enforcement** – Enable the Enaible CI job (`ci-quality-gates-incremental.yml`) across branches.
4. **Enablement** – Walk teams through the installation modes and doctor diagnostics.

## CI Integration

- CI job `enaible-cli` runs on PRs: syncs the workspace, executes tests, and fails on prompt drift.
- Keep `.enaible/schema.json` tracked; artifacts produced at runtime should be gitignored (`.enaible/*`).

## Contact Points

- Migration Owner: CLI Platform Team (`#enaible-cli` on internal chat)
- Incident Response: File an issue in `docs/enaible/migration-guide.md` if anomalies are observed.
