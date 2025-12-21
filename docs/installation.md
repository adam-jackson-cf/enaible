# Manual Installation Guide

This guide walks through provisioning the Enaible toolchain and installing agent assets for Codex, Claude Code, and Copilot. All commands are intended to run from the repository root (`enaible/`).

## Prerequisites

- Python 3.12 (Enaible declares `<3.13`)
- [`uv`](https://docs.astral.sh/uv/latest/) 0.4 or newer on your `PATH`
- Git for cloning repositories referenced by workflows
- Optional: Bun ≥1.2 with the Ultracite preset when you extend JavaScript/Tailwind surfaces defined in the system rulebooks

Verify your environment:

```bash
python --version            # Expect 3.12.x
uv --version                 # Confirm uv is installed
```

### Step 1 - clone repo and cd into target folder

```bash
git clone https://github.com/adam-jackson-cf/enaible.git
```

### Step 2 — Install system assets

Use `enaible install` to copy prompts, command docs, and rulebooks into the correct directories for each CLI surface. The table shows common install targets; replace `<project>` with your workspace path when installing into a different repository.

| System      | Project-scope install                                                                               | User-scope install                                                                    | Notes                                                                               |
| ----------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Codex       | `uv run --project tools/enaible enaible install codex --mode sync --scope project --target .`       | `uv run --project tools/enaible enaible install codex --mode sync --scope user`       | Copies `prompts/`, `rules/`, helper docs, and merges global rules into `AGENTS.md`. |
| Claude Code | `uv run --project tools/enaible enaible install claude-code --mode sync --scope project --target .` | `uv run --project tools/enaible enaible install claude-code --mode sync --scope user` | Copies `commands/`, `agents/`, `rules/`, settings, and regenerates managed prompts. |
| Copilot     | `uv run --project tools/enaible enaible install copilot --mode sync --scope project --target .`     | `uv run --project tools/enaible enaible install copilot --mode sync --scope user`     | Copies `prompts/` and `rules/` for GitHub Copilot surfaces.                         |

Key flags:

- `--mode sync` updates only managed files (sentinel-bearing or assets under `commands/`, `agents/`, and `rules/`). Use `--mode fresh` to rebuild a scope from scratch or `--mode merge` when seeding a new repository.
- `--target` defaults to the current working directory. Point it at a different checkout when installing from a tooling monorepo into downstream projects.
- Set `ENAIBLE_INSTALL_SKIP_SYNC=1` to bypass the automatic `uv sync` inside the installer when you already ran it manually.

## Rendering prompts after edits

Whenever you change items inside `shared/prompts/` or the templates under `docs/system/**`, re-render managed prompts and re-install the relevant system:

```bash
uv run --project tools/enaible enaible prompts render --prompt all --system all
uv run --project tools/enaible enaible install codex --mode sync --scope project
```

Repeat the `enaible install` step for `claude-code` when that surface is affected.

## Validate before publishing

Quality gates mirror the CI workflow defined in `.github/workflows/ci-quality-gates-incremental.yml`. When you install via the script, the session log (`~/.enaible/install-sessions/session-<timestamp>.md`) records each command and exit code so you can attach it to tickets or incident reports.

```bash
uv run --project tools/enaible ruff check tools/enaible/src
uv run --project tools/enaible mypy tools/enaible/src
uv run --project tools/enaible pytest tools/enaible/tests -v
uv run --project tools/enaible enaible prompts diff
```

Resolved prompts should show no diff; regenerate and reinstall when drift is detected.
