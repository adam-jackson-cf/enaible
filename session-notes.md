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

---

## 2025-10-16T14:45:00Z

### Overview

- Hardened analyzer exclusions after the CLI migration smoke test flagged missing results (see `todos/cli-migration/code-quality-run-1.txt`).
- Unified system-specific prompts to call the shared Enaible tooling for context capture and analysis.
- Completed variable-table rollout work that began in the 12:03 UTC session, ensuring all shared prompts follow the new schema.

### Actions

- Removed dependency-name vendor detection heuristics and added a quality analyzer integration test to cover the Juice Shop sample.
- Added a high-volume findings hint to the Enaible analyzer CLI so users can re-run with `--exclude` when third-party code surfaces.
- Re-rendered Claude Code, Codex, and OpenCode context prompts to use `uv run --project tools/enaible` invocations.
- Standardized `## Variables` sections across the shared prompt catalog, including empty tables for commands without arguments.

### Files

- `shared/core/base/vendor_detector.py`, `shared/analyzers/quality/jscpd_analyzer.py`
- `shared/tests/integration/test_quality_analyzer.py`
- `systems/*/(commands|prompts)/get-recent-context.md`, `codify-*-history.md`
- `tools/enaible/src/enaible/commands/analyzers.py`
- `todos/cli-migration/code-quality-report.txt`

### Decisions

- Rely on path-based exclusions plus `.gitignore`/user-specified globs for vendor filtering; dependency name matching is no longer used.
- Treat the shared prompt variable table as the single source of truth for downstream renders (system-specific files should not diverge).
- Surface analyzer volume hints instead of auto-pruning so users remain in control of exclusions.

### Next Steps

- Monitor `enaible analyzers run` feedback to gauge whether additional default exclusions are needed.
- Re-run the CLI migration suite after integrating future prompt updates to ensure the integration test continues to pass.
- Backfill documentation in `docs/system/*` to note the new Enaible-managed context capture pattern.

### Context

- Findings originated from the CLI migration artifacts in `todos/cli-migration/code-quality-run-1.txt` and follow-up discussions on prompt duplication.

## 2025-10-16T15:44:21Z

### Overview

- Standardized workflow formatting across Codex, Claude, and OpenCode prompts to mirror the analyze-security pattern while retaining existing steps.

### Actions

- Replaced legacy behavior/process sections with unified workflow blocks highlighting commands, semantic search handling, and summary guidance.
- Removed Step 1 environment checks in favor of prerequisites/instructions and aligned optional dashboard guidance.
- Synced variable-specific instructions (report generation, exec plan emission) to the new format without altering command semantics.

### Files

- systems/claude-code/commands/\*.md
- systems/opencode/command/\*.md
- systems/codex/prompts/\*.md

### Decisions

- Treat analyze-security workflow as the canonical template for prompt verbosity/structure going forward.
- Keep dependency sync and auth preflights outside numbered steps to avoid Step 1 environment checks.

### Next Steps

- Monitor upcoming prompt additions to ensure they follow the standardized workflow layout before rendering system outputs.
- resume 0199ed9f-3721-7f81-a61b-68ed6f54dada

### Context

- Aligns with user directive to equalize verbosity and command placement across all CLI prompt files.
