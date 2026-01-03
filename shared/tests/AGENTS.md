## Testing

Frameworks: `pytest` (unit + integration) plus the Enaible CLI (`uv run --project tools/enaible ...`). Prefer the CLI wrappers—they bootstrap the analyzer registry, honor gitignore patterns, and normalize JSON output automatically.

Always run suites under the pyenv-managed Python 3.12 toolchain:

```bash
export UV_PYTHON="$(pyenv which python3.12 || pyenv which python)"
```

Prefix every command with `uv run --python "$UV_PYTHON"` so tests never fall back to the system Python 3.9.

### Integration Suites

- **All analyzers smoke** (`shared/tests/integration/test_integration_all_analyzers.py:1-21`)

  ```bash
  NO_EXTERNAL=true uv run --python "$UV_PYTHON" --project tools/enaible \
    pytest shared/tests/integration/test_integration_all_analyzers.py -q
  ```

  Clears external dependencies by default; unset `NO_EXTERNAL` to include tools like Semgrep or Detect-Secrets.

- **Security CLI adapters** (`shared/tests/integration/test_integration_security_cli.py:1-64`)

  ```bash
  uv run --python "$UV_PYTHON" --project tools/enaible pytest shared/tests/integration/test_integration_security_cli.py -k semgrep
  uv run --python "$UV_PYTHON" --project tools/enaible pytest shared/tests/integration/test_integration_security_cli.py -k detect_secrets
  ```

  Each test spins up `integration.cli.evaluate_security` for a small subset; make sure the corresponding binaries (`semgrep`, `detect-secrets`) exist on PATH or the test skips.

- **Root-cause CLI** (`shared/tests/integration/test_integration_root_cause_cli.py:1-14`)

  ```bash
  uv run --python "$UV_PYTHON" --project tools/enaible pytest shared/tests/integration/test_integration_root_cause_cli.py -q
  ```

  Validates `integration.cli.evaluate_root_cause` end-to-end.

- **Docs-scraper skill** (`shared/tests/integration/test_docs_scraper_skill.py:1-110`)

  ```bash
  uv run --python "$UV_PYTHON" pytest shared/tests/integration/test_docs_scraper_skill.py -rA
  ```

  Requires Crawl4AI + Playwright Chromium (`playwright install chromium`); the test skips politely if browsers are absent.

### Targeted Analyzer Runs

Use the Typer command instead of invoking modules manually:

```bash
uv run --python "$UV_PYTHON" --project tools/enaible enaible analyzers list
uv run --python "$UV_PYTHON" --project tools/enaible enaible analyzers run quality:lizard --target shared/tests/fixture/test_codebase --summary
uv run --python "$UV_PYTHON" --project tools/enaible enaible analyzers run security:semgrep --target shared/tests/fixture/test_codebase/test-python --max-files 10 --min-severity medium
```

- `--no-external` sets `ENAIBLE_DISABLE_EXTERNAL=1` for the run.
- `--exclude` can be repeated to add repo-specific ignore globs.
- Use `--out .enaible/artifacts/<task>/<timestamp>/result.json` to persist normalized payloads for CI evidence.
