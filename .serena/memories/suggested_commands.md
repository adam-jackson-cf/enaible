# Suggested Commands

- TypeScript/Bun: `bun install`, `bun run dev`, `bun run test`, `bun run typecheck`, `bun run build`.
- Lint/format: `bunx ultracite check src`, `bunx ultracite fix src`, `bunx tsc --noEmit`.
- Python tooling: `uv sync`, `uv run ruff check .`, `uv run black --check .`, `uv run mypy src`.
- Testing suites: `PYTHONPATH=shared pytest shared/tests/unit -v`, `PYTHONPATH=shared pytest shared/tests/integration -v`, coverage with `PYTHONPATH=shared pytest shared/tests/unit --cov=shared --cov-report=html`.
- Analyzer execution: `PYTHONPATH="$SCRIPTS_ROOT" python -m core.cli.run_analyzer --analyzer category:tool --target . --output-format json` (script path discovered via CLI hierarchy).
- CI workflow: `.github/workflows/ci-quality-gates.yml` for quality gates.
