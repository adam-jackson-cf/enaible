# AI-Assisted Workflows Developer Guide

This document is for maintainers of the Enaible toolchain inside the `enaible` repository. It explains how to extend prompts, analyzers, and installers, as well as the checks required before shipping changes. End-user installation and usage live in `README.md`.

## Audience & Expectations

- You are updating prompt source files, analyzer implementations, or system installers.
- You run all quality gates (`enaible prompts lint`, `enaible prompts validate`, `ruff`, `mypy`, `pytest`) before merging.
- You keep managed assets in `.codex/`, `.claude/`, `.github/` synchronized via `enaible install`.

## Toolchain Requirements

- Python 3.12 (local and CI use the same floor; `tools/enaible/pyproject.toml` enforces `<3.13`).
- `uv` 0.4 or newer for syncing and running Enaible commands.
- Bun ≥1.2 with the Ultracite preset when you edit JavaScript/Tailwind resources referenced by managed prompts.

## Quality Gates

Run the consolidated gate harness before every commit (triggered automatically by pre commit hook, see below):

```bash
bash scripts/run-ci-quality-gates.sh --fix --stage
```

That single entry point executes everything listed:

— prompt lint + validate

- template rendering,
- Ruff format/check,
- Prettier,
- shared analyzer unit tests with coverage,
- repo-wide mypy,
- Enaible CLI pytest suite

This is so the same evidence drives both local commits and `.github/workflows/ci-quality-gates-incremental.yml`.

Only fall back to the individual commands when you need to debug a specific failure.

### Pre-commit Hooks

Install the hook runner once via `pre-commit install`. The lone hook defined in `.pre-commit-config.yaml` shells out to `scripts/run-ci-quality-gates.sh --fix --stage`, which is the same entry point used by `.github/workflows/ci-quality-gates-incremental.yml`. That script executes every gate above—prompt lint/validate, Ruff format/check (respecting `.gitignore` plus `shared/tests/fixture/`), Prettier, shared analyzer unit tests with coverage, mypy via `mypy.ini`, and the Enaible CLI pytest suite—so local commits and CI stay perfectly aligned. Do **not** add bespoke git hooks; route all future pre-commit behavior through this central `pre-commit` config so we keep a single source of truth.

### Prompt Validation

**Lint prompt token usage** (invoked automatically by the gate script):

```bash
ENAIBLE_REPO_ROOT=$(pwd) uv run --directory tools/enaible enaible prompts lint
```

Validates:

- No forbidden `$VAR` tokens outside code blocks (use `@TOKEN` in Variables section instead)
- All `@TOKEN` references in body are declared in Variables section
- Variable shape: tokens start with `@`, positional map to `$N`, flags map to `--flag-name`

Checks:

- Managed prompts: `shared/prompts/*.md`
- Unmanaged prompts: `systems/*/commands/*.md`, `systems/*/prompts/*.md`
- Skips files with `<!-- generated: enaible -->` comment

**Validate rendered prompts match sources**:

```bash
ENAIBLE_REPO_ROOT=$(pwd) uv run --directory tools/enaible enaible prompts validate
```

Ensures rendered files in `systems/*/` match catalog output. Run `ENAIBLE_REPO_ROOT=$(pwd) uv run --directory tools/enaible enaible prompts render` to sync if drift detected.

### Python Quality Checks (for debugging individual steps)

- **Ruff format/check** (gate script runs `uv run --directory tools/enaible ruff check .` plus `PYTHONPATH=shared uv run ruff check shared/` using `shared/config/formatters/ruff.toml`).
- **Mypy** (gate script runs `uv run --with mypy mypy --config-file mypy.ini` which covers both shared analyzers and `tools/enaible/src`).
- **Tests**
  - Shared analyzers: `PYTHONPATH=shared pytest shared/tests/unit -v`
  - Enaible CLI: `uv run --directory tools/enaible pytest tests/`

## Repository Structure (maintainer view)

```
ai-assisted-workflows/
├── shared/
│   ├── analyzers/          # Security, quality, architecture, performance, root_cause implementations
│   ├── core/base/          # Analyzer registry + abstractions
│   ├── context/            # Context capture scripts invoked by enaible
│   └── prompts/            # Source prompt catalog rendered into CLI commands
├── systems/
│   ├── antigravity/        # Managed workflows for the Antigravity runtime
│   ├── claude-code/        # Managed outputs (prompts/rules) consumed by Claude Code
│   ├── codex/              # Managed prompts/rules consumed by the Codex CLI
│   ├── copilot/            # Copilot adapter prompts/rules (rendered from shared sources)
│   ├── cursor/             # Cursor-specific agent/rule overlays
│   └── gemini/             # Gemini adapter commands/templates
├── tools/enaible/          # uv-packaged Typer CLI providing render/install/run commands
├── docs/                   # Maintainer guidance (installation, analysis, monitoring)
└── todos/                  # Planning notes and exec plans
```

### For detailed development workflows for this codebase, see:

- `shared/prompts/AGENTS.md` — when you want to add a new shared prompt
- `systems/AGENTS.md` — when you want to add a new system adapter
- `docs/testing.md` — active test suites and how to run them

### When you need to track tasks across sessions

If `--tasks` is included in the users request or a request requires persistent task tracking beyond the current session, you **must** use Beads (bd).

**Available Commands:**

- `bd ready` — List active tasks at session start
- `bd create "<title>"` — Create a new tracked task (returns ID)
- `bd show <id>` — View task details
- `bd close <id>` — Mark task complete
- `bd list --label <name>` — Filter tasks by label

## Copilot Documentation Review Automation

- `.github/workflows/copilot-doc-review.yml` runs on PR updates, pushes to `main`, and manual dispatch to keep README/AGENTS files aligned with committed code.
- `.github/workflows/helpers/copilot_doc_review_prompt.py` enumerates those documentation files (skipping fixtures, caches, and `node_modules`), builds a targeted diff, and records run metadata.
- Pull requests receive a persistent comment mentioning `@copilot` via `peter-evans/create-or-update-comment`, so the Copilot coding agent can edit docs directly in-branch before merge.
- Pushes to `main` open or refresh a `copilot-doc-review` issue assigned to `copilot-swe-agent[bot]`, ensuring the agent runs even when changes land outside PR review.
- GitHub’s current coding-agent settings only expose Claude Sonnet 4.5, Claude Opus 4.5, GPT-5.1-Codex-Max, or Auto. Haiku 4.5 cannot be selected yet; revisit the Copilot settings UI once GitHub adds more model options.
- The push workflow fails fast unless `COPILOT_ASSIGNMENT_TOKEN` (a repo-scoped PAT stored as an Actions _repository_ secret) exists, because GitHub only accepts `agent_assignment` payloads from user tokens.
- Push jobs only run from `refs/heads/main`; all other pushes rely on the PR leg of the workflow.
- To avoid recursive Copilot PRs triggering new Copilot sweeps, the workflow bails out whenever `github.actor == app/copilot-swe-agent` or when the PR branch starts with `copilot/` (only manual/human PRs run the doc review).
