---
description: Install dependency monitoring with Dependabot and audit triggers
agent: agent
tools: ["githubRepo", "search/codebase"]
---

# Purpose

Install multi-ecosystem dependency monitoring with Dependabot and path-triggered CI audits configured for minimal noise.

## Variables

### Optional (derived from $ARGUMENTS)

- @AUDIT_LEVEL = ${input:audit-level} — severity threshold (default critical)
- @AUTO = ${input:auto} — skip STOP confirmations (auto-approve checkpoints)
- @BRANCH_PROTECTION = ${input:branch-protection} — enable branch-protection scaffolding when true
- @EXCLUDE = ${input:exclude} [repeatable] — paths to exclude from monitoring
- @PACKAGE_FILE = ${input:package-file} — restrict monitoring to a specific manifest

### Derived (internal)

- @DETECTED_ECOSYSTEMS — ecosystems identified during setup (npm, pip, cargo, etc.)

## Instructions

- Detect all package ecosystems unless `--package-file` explicitly narrows scope.
- Use the registry-driven setup script; do not replicate its logic manually.
- Document detection heuristics, excluded paths, and resulting configurations.
- Generate Dependabot and GitHub Actions workflows with path-based triggers.
- Update security policy documentation to reflect the monitoring approach.
- Respect STOP confirmations unless @AUTO is provided; when auto is active, treat checkpoints as approved without altering other behavior.

## Workflow

1. Environment preparation
   - Run `git rev-parse --is-inside-work-tree`; exit immediately if not in a git repository because generated workflows rely on repository structure.
2. Parse arguments
   - Capture `--audit-level`, `--package-file`, all `--exclude` values, and the optional `--branch-protection` flag.
   - Store results in `AUDIT_LEVEL`, `PACKAGE_FILE`, `EXCLUDE_PATHS[]`, and `SETUP_BRANCH_PROTECTION` (default `AUDIT_LEVEL=critical`).
3. Execute setup script
   - Build exclusion flags only when values are provided:
     ```bash
     EXCLUDE_ARGS=""
     for path in "${EXCLUDE_PATHS[@]}"; do
       EXCLUDE_ARGS+=" --exclude \"$path\""
     done
     ```
   - Run the shared setup module via the Enaible environment:
     ```bash
     PYTHONPATH=shared \
       uv run --project tools/enaible python shared/setup/security/setup_package_monitoring.py \
         --audit-level "${AUDIT_LEVEL:-critical}" \
         --branch-protection "${SETUP_BRANCH_PROTECTION:-false}" \
         ${PACKAGE_FILE:+--package-file "$PACKAGE_FILE"} \
         ${EXCLUDE_ARGS}
     ```
   - Capture stdout to extract detected ecosystems and generated files.
4. Review generated artifacts
   - `.github/dependabot.yml`
   - `.github/workflows/package-audit.yml`
   - `SECURITY.md` (new or updated)
   - Optional branch protection configuration summary (if requested).
5. Validate configuration
   - Confirm workflow triggers monitor only package files.
   - Ensure Dependabot entries cover each detected ecosystem with appropriate schedule.
   - Verify audit workflow executes critical-level checks aligned with Dependabot PRs.
6. Summarize outcome
   - Report ecosystems, audit level, exclusions, and branch protection status.
   - Provide next steps for enabling workflows (commit/push, review Actions tab).

## Output

```md
# RESULT

- Summary: Package monitoring configured (audit level: <AUDIT_LEVEL>).

## ECOSYSTEMS

- <ecosystem 1>
- <ecosystem 2>

## GENERATED FILES

- .github/workflows/package-audit.yml
- .github/dependabot.yml
- SECURITY.md (<created|updated>)

## SETTINGS

- Branch Protection: <enabled|disabled>
- Exclusions: <paths or none>
- Package File Override: <value or none>

## NEXT STEPS

1. Commit and push generated files.
2. Review Actions tab for package-audit workflow.
3. Monitor Dependabot PRs for security updates.
```

<!-- generated: enaible -->
