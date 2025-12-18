# AI-Assisted Workflows Developer Guide

This document is for maintainers of the Enaible toolchain inside the `ai-assisted-workflows` repository. It explains how to extend prompts, analyzers, and installers, as well as the checks required before shipping changes. End-user installation and usage live in `README.md`.

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
# Enaible package
uv run --directory tools/enaible mypy src

# Shared analyzers
PYTHONPATH=shared uv run mypy shared/
```

**Unit tests** (from repository root):

```bash
# Enaible tests
uv run --directory tools/enaible pytest tests/

# Shared analyzer tests
PYTHONPATH=shared pytest shared/tests/unit -v
```

### Pre-commit Hooks

The repository includes pre-commit hooks (`.pre-commit-config.yaml`) that run automatically on commit:

- Trailing whitespace removal
- End-of-file fixer
- JSON/YAML validation
- Python: pyupgrade, black, ruff, mypy
- Prettier for other files

Install hooks: `pre-commit install`

> **Codex git pushes:** The Codex shell does not inherit Cursor's GUI askpass bridge. Run `unset GIT_ASKPASS` (and `unset SSH_ASKPASS` if set) before pushing so git reuses your stored credentials without Cursor's modal failing in the background.

## Repository Structure (maintainer view)

```
ai-assisted-workflows/
├── shared/
│   ├── analyzers/          # Security, quality, architecture, performance, root_cause implementations
│   ├── core/base/          # Analyzer registry + abstractions
│   ├── context/            # Context capture scripts invoked by enaible
│   └── prompts/            # Source prompt catalog rendered into CLI commands
├── systems/
│   ├── codex/
│   ├── claude-code/        # Managed outputs (prompts/rules) consumed by respective CLIs
│   ├── copilot/            # Copilot adapter prompts/rules (rendered from shared sources)
│   └── cursor/             # Cursor-specific agent/rule overlays
├── tools/enaible/          # uv-packaged Typer CLI providing render/install/run commands
├── docs/                   # Maintainer guidance (installation, analysis, monitoring)
└── todos/                  # Planning notes and exec plans
```

For detailed workflows, see:

- `shared/prompts/AGENTS.md` — adding and validating shared prompts
- `shared/analyzers/AGENTS.md` — analyzer registry rules and tests
- `shared/context/AGENTS.md` — context capture commands and artifacts
- `systems/AGENTS.md` — system adapter playbook and managed-file rules
- `docs/testing.md` — active test suites and how to run them
