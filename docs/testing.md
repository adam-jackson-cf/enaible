# Testing Guide

Enaible ships with several layers of automated tests. This guide explains the different suites, how to run them, and the additional setup required for prompt end-to-end validation.

## CI Quality Gates

Run `scripts/run-ci-quality-gates.sh` to execute the same sequence enforced by `.github/workflows/ci-quality-gates-incremental.yml` (shared unit tests with coverage, Ruff, Mypy, and the Enaible CLI test suite via `uv`). The script is wired into `pre-commit`, so committing without passing the gates will fail locally before CI.

## Unit Tests

Location: `tools/enaible/tests/` and `shared/tests/unit/`

Run both Python unit suites locally:

```bash
uv run --project tools/enaible pytest tools/enaible/tests -v
PYTHONPATH=shared pytest shared/tests/unit -v
```

These suites cover CLI command behaviors, analyzer registry logic, and lower-level utilities.

### Context Utilities

Codex context capture helpers include dedicated tests and lint checks. Run the focused suite alongside the general unit tests:

```bash
PYTHONPATH=shared pytest shared/tests/unit -k context_bundle_capture_codex -v
ruff check shared/context
```

## Integration Tests

Location: `shared/tests/integration/`

Highlights (kept current):

- Analyzer smoke tests (`test_integration_all_analyzers.py`, `test_quality_analyzer.py`)
- Security and root-cause CLI wrappers (`test_integration_security_cli.py`, `test_integration_root_cause_cli.py`)

Run the focused integration suite with:

```bash
uv run --project tools/enaible pytest shared/tests/integration -v \
  -k "integration_all_analyzers or integration_security_cli or integration_root_cause_cli or quality_analyzer"
```

Tests that depended on external CLIs or backlog todos have been removed to reduce flakiness.

## Troubleshooting

- All prompt artifacts are stored under `.enaible/artifacts/prompt-e2e/<prompt-id>/` for manual inspection.

Keeping these suites green ensures shared prompts, analyzers, and installers stay in sync across Codex and Claude Code.
