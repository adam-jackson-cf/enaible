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

Before merging changes, run all quality gates to ensure code quality and prompt validity:

### Prompt Validation

**Lint prompt token usage** (from repository root):

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

**Validate rendered prompts match sources** (from repository root):

```bash
ENAIBLE_REPO_ROOT=$(pwd) uv run --directory tools/enaible enaible prompts validate
```

Ensures rendered files in `systems/*/` match catalog output. Run `ENAIBLE_REPO_ROOT=$(pwd) uv run --directory tools/enaible enaible prompts render` to sync if drift detected.

### Python Quality Checks

**Linting and formatting** (from repository root):

```bash
# Enaible package
uv run --directory tools/enaible ruff check .

# Shared analyzers
PYTHONPATH=shared uv run ruff check shared/
```

**Type checking** (from repository root):

```bash
uv run --with mypy mypy --config-file mypy.ini
```

**Unit tests** (from repository root):

```bash
# Enaible tests
uv run --directory tools/enaible pytest tests/

# Shared analyzer tests
PYTHONPATH=shared pytest shared/tests/unit -v
```

### Pre-commit Hooks

Install the hook runner once via `pre-commit install`. The lone hook defined in `.pre-commit-config.yaml` shells out to `scripts/run-ci-quality-gates.sh --fix --stage`, which is the same entry point used by `.github/workflows/ci-quality-gates-incremental.yml`. That script executes every gate above—prompt lint/validate, Ruff format/check (respecting `.gitignore` plus `shared/tests/fixture/`), Prettier, shared analyzer unit tests with coverage, mypy via `mypy.ini`, and the Enaible CLI pytest suite—so local commits and CI stay perfectly aligned.

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

## Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**

- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
