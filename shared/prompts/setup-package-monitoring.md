# Purpose

Install multi-ecosystem dependency monitoring with Dependabot and path-triggered CI audits configured for minimal noise.

## Variables

### Required

- (none)

### Optional (derived from $ARGUMENTS)

- @AUDIT_LEVEL = --audit-level — severity threshold (default critical)
- @PACKAGE_FILE = --package-file — restrict monitoring to a specific manifest
- @EXCLUDE = --exclude [repeatable] — paths to exclude from monitoring
- @BRANCH_PROTECTION = --branch-protection — enable branch-protection scaffolding when true

### Derived (internal)

- @DETECTED_ECOSYSTEMS = <derived> — ecosystems identified during setup (npm, pip, cargo, etc.)

## Instructions

- Detect all package ecosystems unless `--package-file` explicitly narrows scope.
- Use the registry-driven setup script; do not replicate its logic manually.
- Document detection heuristics, excluded paths, and resulting configurations.
- Generate Dependabot and GitHub Actions workflows with path-based triggers.
- Update security policy documentation to reflect the monitoring approach.

## Workflow

1. Environment preparation
   - Run `git rev-parse --is-inside-work-tree`; exit immediately if not in a git repository because generated workflows rely on repository structure.
   - !`uv sync --project tools/enaible`
2. Parse arguments
   - Capture `--audit-level`, `--package-file`, all `--exclude` values, and the optional `--branch-protection` flag.
   - Store results in `AUDIT_LEVEL`, `PACKAGE_FILE`, `EXCLUDE_PATHS[]`, and `SETUP_BRANCH_PROTECTION` (default `AUDIT_LEVEL=critical`).
3. Execute setup script
   - Run the shared setup module via the Enaible environment:
     ```bash
     PYTHONPATH=shared \
       uv run --project tools/enaible python shared/setup/security/setup_package_monitoring.py \
         --audit-level "${AUDIT_LEVEL:-critical}" \
         --branch-protection "${SETUP_BRANCH_PROTECTION:-false}" \
         ${PACKAGE_FILE:+--package-file "$PACKAGE_FILE"} \
         $(printf ' --exclude %q' "${EXCLUDE_PATHS[@]}")
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

## Examples

```bash
# Default critical-only auditing across detected ecosystems
/setup-package-monitoring

# Specify a package file and enable branch protection
/setup-package-monitoring --package-file=requirements.txt --branch-protection=true
```
