# Session Notes

## 2025-10-15

- Completed Enaible CLI Phases 1–4 (scaffold, analyzers, prompt templating, pilot renders).
- Upgraded Typer to 0.18.0 to restore compatibility with Click 8.3 and verified analyzer/prompt commands.
- Added CI job `enaible-cli` plus documentation for local guardrails and installation workflows.
- Implemented `enaible install` modes (`merge`, `update`, `sync`, `fresh`) with backing tests and rollout guide.

---

## 2025-10-16T12:03:59Z

### Overview

- Standardized prompt variable definitions with a structured table and automated argument hints across Claude Code, OpenCode, and Codex outputs.
- Added Enaible prompt parsing utilities, refreshed templates, and regenerated managed prompts after fixing `uv run --project tools/enaible` invocation gaps highlighted during install testing.
- Consolidated system documentation under `docs/system/<system>/` for cleaner layout.

### Actions

- Implemented `VariableSpec` parsing in `tools/enaible/src/enaible/prompts/utils.py` and wired it into the renderer/templates.
- Updated shared prompts and regenerated system outputs; ensured CLI tests and `enaible prompts diff` pass.
- Migrated documentation folders from `docs/systems/*` to `docs/system/*`.
- Replaced analyzer command snippets to include `uv run --project tools/enaible` so installations provision dependencies correctly.

### Files

- `shared/prompts/` (analyze-_, plan-_)
- `tools/enaible/src/enaible/prompts/{renderer.py,utils.py}` and associated tests
- `docs/system/claude-code|codex|opencode/**`
- `systems/<system>/(commands|prompts)` generated outputs

### Outstanding

- Monitor real-world installs to confirm the synced prompts resolve the dependency spawning issue in Claude workflows.

### Decisions

- Adopted `$UPPER_SNAKE_CASE` token convention with standardized variables tables across all shared prompts.
- Enaible installer now defaults to running `uv sync --project tools/enaible` while skipping legacy installer assets.
- System documentation now lives exclusively under `docs/system/<system>/`.

### Next Steps

- Validate upcoming prompts adhere to the variables-table format and leverage the automated rendering path before merging future changes.

### Context

- User reported `uv run enaible …` failures inside Claude after install; resolved by updating prompt commands to reference the project-scoped Enaible CLI.
