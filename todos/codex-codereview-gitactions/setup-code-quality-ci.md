# Purpose

Create a GitHub Actions workflow that runs repository code-quality analyzers on pull requests with path-based triggers, uploads machine-readable JSON artifacts, and enforces a configurable fail gate (default: high). Designed to mirror the established setup pattern and generator flow.

## Variables

### Optional (derived from $ARGUMENTS)

- @FAIL_ON = --fail-on — severity threshold to fail the job (default high)
- @PATHS_INCLUDE = --paths-include [repeatable] — additional glob paths to include in triggers
- @EXCLUDE = --exclude [repeatable] — glob paths to exclude from triggers
- @COMMENT_ON_PR = --comment-on-pr — add a summary PR comment when true (default true)

### Derived (internal)

- @WORKFLOW = .github/workflows/code-quality.yml — generated workflow path

## Instructions

- Use the generator script; do not hand author the workflow.
- The workflow runs quality analyzers via uv + Enaible CLI (`enaible analyzers run`) and publishes JSON artifacts.
- Path triggers ensure the job runs only when code files change; additional includes/excludes are honored.
- The gating step fails the job when any analyzer reports findings at or above @FAIL_ON.

## Workflow

1. Environment preparation
   - Verify a git repository is present with `git rev-parse --is-inside-work-tree`.
2. Parse arguments
   - Capture `--fail-on`, all `--paths-include`, all `--exclude`, and `--comment-on-pr`.
3. Generate workflow
   - Create directory `.github/workflows` if missing.
   - Write `codex-code-quality.yml` (backup existing to `codex-code-quality.yml.bak`).
   - Include:
     - `actions/checkout@v4` (pinned SHA), `actions/setup-node@v4` (pinned SHA), `astral-sh/setup-uv@v2`
     - Install tools in uv/Enaible env: `lizard` (pip via uv); `jscpd` (npm -g)
     - Run analyzers via uv + Enaible CLI:
       - `uv run --project tools/enaible enaible analyzers run quality:lizard --out artifacts/quality_lizard.json`
       - `uv run --project tools/enaible enaible analyzers run quality:jscpd --out artifacts/quality_jscpd.json`
       - `uv run --project tools/enaible enaible analyzers run quality:pattern_classifier --out artifacts/quality_patterns.json`
     - Convert to CodeClimate JSON using Enaible CLI:
       - `uv run --project tools/enaible enaible ci convert-codeclimate artifacts --out gl-code-quality-report.json`
     - Upload artifacts (JSON per analyzer + CodeClimate JSON)
     - Gate on `FAIL_ON` (critical|high|medium|low)
     - Optional PR comment summarizing counts
4. Summarize outcome
   - Echo generated path, fail threshold, comment setting, and trigger filters.

## Output

```md
# RESULT

- Summary: Code Quality CI configured (fail-on: <@FAIL_ON>).

## GENERATED FILES

- .github/workflows/codex-code-quality.yml

## SETTINGS

- Comment on PR: <true|false>
- Extra Includes: <globs or none>
- Exclusions: <globs or none>

## NEXT STEPS

1. Commit and push generated files.
2. Open/refresh a PR touching code paths to see the workflow run.
3. Inspect the uploaded artifacts for detailed findings.
```

## Examples

```bash
# Default fail on high severity
/setup-code-quality-ci

# Fail on medium and add extra includes
/setup-code-quality-ci --fail-on=medium --paths-include='apps/**' --paths-include='packages/**'

# Disable PR comments
/setup-code-quality-ci --comment-on-pr=false
```
