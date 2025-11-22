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
│   └── claude-code/        # Managed outputs (prompts/rules) consumed by respective CLIs
├── tools/enaible/          # uv-packaged Typer CLI providing render/install/run commands
├── docs/                   # Maintainer guidance (installation, analysis, monitoring, agents, roadmap)
└── todos/                  # Planning notes and exec plans
```

## Prompt Catalog & Drift Control

1. **Author** prompt sources under `shared/prompts/*.md` using the shared tokens/variables patterns.
2. **Render** every edited prompt for all systems:
   ```bash
   uv run --project tools/enaible enaible prompts render --prompt all --system all
   ```
3. **Detect drift** before committing:
   ```bash
   uv run --project tools/enaible enaible prompts diff
   uv run --project tools/enaible enaible prompts validate
   ```

````
Both commands must exit `0`. Managed files include `<!-- generated: enaible -->`; do not hand-edit generated blocks.
4. **Install** regenerated prompts into local scopes when you need to verify in a CLI:
 ```bash
 uv run --project tools/enaible enaible install codex --mode sync --scope project --target .
 uv run --project tools/enaible enaible install claude-code --mode sync --scope project --target .
````

The installer treats everything under `commands/`, `agents/`, and `rules/` as managed assets even when a sentinel is absent so subsequent installs will overwrite manual edits—apply custom changes to upstream sources instead. 5. **Lint** prompt sources and unmanaged Markdown using:

```bash
uv run --project tools/enaible enaible prompts lint
```

## Prompt Token Conventions

- Use `@TOKEN` placeholders for all non-argument variables inside prompts, including inside code fences. Avoid `$VAR`, `${...}`, and `$(...)` in prompt bodies to prevent accidental argument parsing.
- Reserve `$`-prefixed tokens only in the `## Variables` section to denote positional/user arguments (e.g., `$1`, `$2`, `$ARGUMENTS`). `$` must not appear elsewhere in a prompt.
- Examples:
  - ✅ `- @ARTIFACT_ROOT = .enaible/artifacts/analyze-code-quality/@TIMESTAMP`
  - ✅ `uv run ... --out "@ARTIFACT_ROOT/quality-lizard.json"`
  - ❌ `ARTIFACT_ROOT=".enaible/.../$(date -u +%Y%m%dT%H%M%SZ)"`
  - ❌ `--out "$ARTIFACT_ROOT/quality-lizard.json"`

## Analyzer Development Workflow

- Import analyzers through the `analyzers.*` namespace only. The registry bootstrap lives in `shared/core/base/registry_bootstrap.py`.
- When adding a new analyzer:
  1. Implement it under the appropriate category in `shared/analyzers/<category>/`.
  2. Register it via `registry_bootstrap.py`.
  3. Add coverage in `tools/enaible/tests/` or `shared/tests/` to exercise creation and normalization.
  4. Expose guidance in the relevant prompt if the workflow relies on it.
- Preferred execution for local testing:
  ```bash
  uv run --project tools/enaible enaible analyzers list
  uv run --project tools/enaible enaible analyzers run quality:lizard --target . --out .enaible/artifacts/dev/$(date -u +%Y%m%dT%H%M%SZ)/lizard.json
  ```
- Manual fallback when debugging outside Enaible:
  ```bash
  PYTHONPATH=shared python -m analyzers.quality.complexity_lizard . --output-format json
  ```
- Avoid mutating `sys.path` inside analyzers; rely on `load_workspace()` to supply `shared/` when running through Enaible.

## Quality Gates Before Merging

```bash
uv sync --project tools/enaible
uv run --project tools/enaible ruff check tools/enaible/src
uv run --project tools/enaible mypy tools/enaible/src
uv run --project tools/enaible pytest tools/enaible/tests -v
uv run --project tools/enaible enaible prompts diff
```

Run additional `PYTHONPATH=shared pytest shared/tests` when analyzer behavior changes.

## Context Capture & Artifact Hygiene

- Capture session history with:
  ```bash
  uv run --project tools/enaible enaible context_capture --platform codex --days 3 --output-format json
  ```
- Respect `.enaible/artifacts/<task>/<timestamp>/` for evidence storage. Managed prompts assume this layout.
- Keep diagnostic records by exporting `enaible doctor` results:
  ```bash
  uv run --project tools/enaible enaible doctor --json > .enaible/doctor.json
  ```

## Provenance Governance

For provenance-aware PR analysis using the sibling repo `../provenance`:

1. `make docker-start` inside `../provenance` (requires GitHub authentication).
2. Ensure secrets `PROVENANCE_API_URL=http://provenance:8000` and `PROVENANCE_API_TOKEN=<token>` exist on the target repo.
3. Label PRs with `provenance` to trigger `.github/workflows/provenance-selfhosted.yml`.
4. `make docker-stop` when finished to tear down the stack and deregister the runner.

## Reference Material

- [docs/installation.md](docs/installation.md) — provisioning Enaible and syncing managed assets
- [docs/analysis-scripts.md](docs/analysis-scripts.md) — analyzer catalog and usage patterns
- [docs/subagents.md](docs/subagents.md) — managed prompt catalog and render/install workflow
- [docs/monitoring.md](docs/monitoring.md) — artifact conventions and diagnostics
- [docs/roadmap.md](docs/roadmap.md) — current milestone tracking
