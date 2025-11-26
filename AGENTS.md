# AI-Assisted Workflows Developer Guide

This document is for maintainers of the Enaible toolchain inside the `ai-assisted-workflows` repository. It explains how to extend prompts, analyzers, and installers, as well as the checks required before shipping changes. End-user installation and usage live in `README.md`.

## Audience & Expectations

- You are updating prompt source files, analyzer implementations, or system installers.
- You run all quality gates (`ruff`, `mypy`, `pytest`, `enaible prompts diff`) before merging.
- You keep managed assets in `.codex/`, `.claude/`, `.github/` synchronized via `enaible install`.

## Toolchain Requirements

- Python 3.12 (local and CI use the same floor; `tools/enaible/pyproject.toml` enforces `<3.13`).
- `uv` 0.4 or newer for syncing and running Enaible commands.
- Bun ≥1.2 with the Ultracite preset when you edit JavaScript/Tailwind resources referenced by managed prompts.

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
