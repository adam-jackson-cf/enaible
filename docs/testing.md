# Testing Guide

Enaible ships with several layers of automated tests. This guide explains the different suites, how to run them, and the additional setup required for prompt end-to-end validation.

## Unit Tests

Location: `tools/enaible/tests/` and `shared/tests/unit/`

Run both Python unit suites locally:

```bash
uv run --project tools/enaible pytest tools/enaible/tests -v
PYTHONPATH=shared pytest shared/tests/unit -v
```

These suites cover CLI command behaviors, analyzer registry logic, and lower-level utilities.

## Integration Tests

Location: `shared/tests/integration/`

Highlights:

- Analyzer smoke tests (`test_integration_all_analyzers.py`, `test_quality_analyzer.py`)
- Context capture fixtures and CLI installer scripts
- Background workflow smoke test (`test_todo_background_script.py`)

Run the full integration suite with:

```bash
PYTHONPATH=shared pytest shared/tests/integration -v
```

Some tests require optional CLIs (Codex, Claude, Qwen, Gemini). They automatically skip when dependencies are missing.

## Troubleshooting

- All prompt artifacts are stored under `.enaible/artifacts/prompt-e2e/<prompt-id>/` for manual inspection.

Keeping these suites green ensures shared prompts, analyzers, and installers stay in sync across Codex and Claude Code.
