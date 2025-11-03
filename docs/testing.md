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

Some tests require optional CLIs (Codex, Claude, OpenCode, Qwen, Gemini). They automatically skip when dependencies are missing.

## Prompt End-to-End Tests (OpenCode)

Location: `shared/tests/integration/test_opencode_prompts.py`

Purpose: render and install the latest OpenCode prompts, launch each command inside a tmux session, and verify the model produces the expected sections against a small fixture repository. Prompts run with the new `--auto` flag so the scripted workflow can respond automatically at every STOP gate while interactive users keep the default confirmation flow. This ensures prompt updates remain executable after changes to shared templates or analyzers.

### Environment prerequisites

- `tmux` installed on the host.
- OpenCode CLI (`opencode`) upgraded to v1.0.11 or later (`opencode upgrade`).
- GitHub Copilot authentication (`opencode auth list` should list "GitHub Copilot") or a valid `GITHUB_TOKEN`.
- Optional: set `PROMPT_E2E_FORCE=1` to re-run all prompts even if hashes are unchanged.

### Running the suite

The tests are opt-in to avoid consuming tokens during regular CI runs. Prompts are executed with the new `--auto` flag so STOP confirmations are auto-approved. Enable the suite explicitly:

```bash
ENABLE_OPENCODE_E2E=1 PYTHONPATH=shared pytest shared/tests/integration/test_opencode_prompts.py -v
```

Artifacts and caches are written to `.enaible/prompt-e2e/`.

### Result caching

`systems/opencode/prompt-manifest.json` tracks every managed prompt, its semantic version, and the files that influence rendering. The test computes a SHA256 hash from those source files plus the OpenCode command template. Successful runs record the hash and timestamp in `.enaible/prompt-e2e/opencode.json`. Unchanged prompts are skipped automatically unless `PROMPT_E2E_FORCE=1` is set.

## Troubleshooting

- Use `shared/tests/integration/fixtures/check-ai-cli-auth.sh opencode --report <file>` to confirm OpenCode credentials before running the E2E suite.
- tmux sessions are named `enaible-opencode-<prompt-id>-<timestamp>`. Inspect logs with `tmux capture-pane -p -t <session>` if a run fails.
- All prompt artifacts are stored under `.enaible/artifacts/prompt-e2e/<prompt-id>/` for manual inspection.

## Adding new prompts or tests

1. Update the prompt manifest (`systems/opencode/prompt-manifest.json`) with the new entry, success markers, and version bump.
2. Extend fixtures under `shared/tests/integration/fixtures/prompt-e2e/` if the prompt needs dedicated input files.
3. Run the E2E suite with `PROMPT_E2E_FORCE=1` to refresh the cache.
4. Commit the updated cache (`.enaible/prompt-e2e/opencode.json`) alongside source changes.

Keeping these suites green ensures shared prompts, analyzers, and installers stay in sync across Codex, Claude Code, and OpenCode.
