# Purpose

Create a GitHub Actions workflow that runs repository security analyzers (Semgrep + Detect-Secrets) on pull requests with path-based triggers, uploads machine-readable JSON artifacts, and enforces a configurable fail gate (default: high). Supports Semgrep ruleset overrides at generation time and at dispatch time.

## Variables

### Optional (derived from $ARGUMENTS)

- @FAIL_ON = --fail-on — severity threshold to fail the job (default high)
- @MIN_SEVERITY = --min-severity — analyzer output filtering (critical|high|medium|low|info) passed to the runner (default low)
- @SEMGREP_CONFIG = --semgrep-config — comma/newline separated list of Semgrep configs (e.g., `auto`, `p/owasp-top-ten,r/secrets`, `security/semgrep/custom.yml`)
- @PATHS_INCLUDE = --paths-include [repeatable] — additional glob paths to include in triggers
- @EXCLUDE = --exclude [repeatable] — glob paths to exclude from triggers
- @COMMENT_ON_PR = --comment-on-pr — add a summary PR comment when true (default true)

### Derived (internal)

- @WORKFLOW = .github/workflows/security-analysis.yml — generated workflow path

## Instructions

- Use the generator script; do not hand author the workflow.
- The workflow runs `security:semgrep` and `security:detect_secrets` via uv + Enaible CLI (`enaible analyzers run`) and publishes JSON artifacts.
- Path triggers ensure the job runs only when code files change; additional includes/excludes are honored.
- The gating step fails the job when any analyzer reports findings at or above @FAIL_ON.
- Semgrep ruleset override precedence: workflow dispatch input > workflow default from generator > analyzer fallback (`auto`).

## Workflow

1. Environment preparation
   - Verify a git repository is present with `git rev-parse --is-inside-work-tree`.
2. Parse arguments
   - Capture `--fail-on`, `--min-severity`, `--semgrep-config`, all `--paths-include`, all `--exclude`, and `--comment-on-pr`.
3. Generate workflow
   - Create directory `.github/workflows` if missing.
   - Write `codex-security-analysis.yml` (backup existing to `codex-security-analysis.yml.bak`).
   - Include:
     - `actions/checkout@v4` (pinned SHA), `astral-sh/setup-uv@v2`
     - Install tools in uv/Enaible env: `semgrep` and `detect-secrets` (pip)
     - Env defaults: `SEMGREP_DEFAULT_CONFIGS` from `--semgrep-config` (fallback `auto`)
     - Run analyzers via uv + Enaible CLI:
       - `uv run --project tools/enaible enaible analyzers run security:semgrep --out artifacts/security_semgrep.json`
       - `uv run --project tools/enaible enaible analyzers run security:detect_secrets --out artifacts/security_secrets.json`
     - Render prioritized Markdown using Enaible CLI:
       - `uv run --project tools/enaible enaible ci security-markdown artifacts --out security_priority.md`
     - Upload artifacts (JSON per analyzer + Markdown)
     - Gate on `FAIL_ON` (critical|high|medium|low)
     - Optional PR comment summarizing counts
4. Summarize outcome
   - Echo generated path, thresholds, semgrep configs, comment setting, and trigger filters.

## Output

```md
# RESULT

- Summary: Security Analysis CI configured (fail-on: <@FAIL_ON>, min-severity: <@MIN_SEVERITY>).

## GENERATED FILES

- .github/workflows/codex-security-analysis.yml

## SETTINGS

- Semgrep Configs (default): <value>
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
/setup-security-analysis-ci

# Override Semgrep configs (registry packs + local rules)
/setup-security-analysis-ci --semgrep-config="p/owasp-top-ten,r/secrets,security/semgrep" --fail-on=high

# Adjust analyzer min-severity and disable PR comments
/setup-security-analysis-ci --min-severity=medium --comment-on-pr=false
```
