# Purpose

Install multi-ecosystem dependency monitoring with Dependabot and path-triggered CI audits configured for minimal noise.

## Variables

- `AUDIT_LEVEL` ← value from `--audit-level` (default `critical`).
- `PACKAGE_FILE` ← path from `--package-file` (optional).
- `EXCLUDE_PATHS[]` ← paths supplied via `--exclude`.
- `SETUP_BRANCH_PROTECTION` ← boolean when `--branch-protection=true`.
- `SCRIPT_PATH` ← resolved path to `setup_package_monitoring.py`.
- `SCRIPTS_ROOT` ← computed base directory.
- `DETECTED_ECOSYSTEMS[]` ← languages/package managers discovered.
- `$ARGUMENTS` ← raw argument string.

## Instructions

- Detect all package ecosystems unless `--package-file` explicitly narrows scope.
- Use the registry-driven setup script; do not replicate its logic manually.
- Document detection heuristics, excluded paths, and resulting configurations.
- Generate Dependabot and GitHub Actions workflows with path-based triggers.
- Update security policy documentation to reflect the monitoring approach.

## Workflow

1. Verify prerequisites
   - Run `python3 --version`; exit immediately if Python 3 is unavailable because the setup script requires it.
   - Run `ls .claude/scripts/setup/security/*.py || ls "$HOME/.claude/scripts/setup/security/"`; if both fail, prompt for a directory containing `setup_package_monitoring.py` and exit if unavailable.
   - Run `git rev-parse --is-inside-work-tree`; exit immediately if not in a git repository because generated workflows rely on repository structure.
2. Parse arguments
   - Capture `AUDIT_LEVEL`, `PACKAGE_FILE`, multiple `--exclude` values, and `SETUP_BRANCH_PROTECTION`.
3. Resolve script location
   - Search project-level `.claude/scripts/setup/security/`, then user-level equivalent.
   - Prompt for path when unresolved; ensure `setup_package_monitoring.py` exists.
4. Prepare environment
   - Compute `SCRIPTS_ROOT` and run `PYTHONPATH="$SCRIPTS_ROOT" python -c "import core.base; print('env OK')"`; abort on failure.
5. Execute setup script
   - Run:
     ```bash
     PYTHONPATH="$SCRIPTS_ROOT" python -m setup.security.setup_package_monitoring \
       --audit-level "$AUDIT_LEVEL" \
       --branch-protection "${SETUP_BRANCH_PROTECTION:-false}" \
       ${PACKAGE_FILE:+--package-file "$PACKAGE_FILE"} \
       $(printf ' --exclude %q' "${EXCLUDE_PATHS[@]}")
     ```
   - Capture stdout to extract detected ecosystems and generated files.
6. Review generated artifacts
   - `.github/dependabot.yml`
   - `.github/workflows/package-audit.yml`
   - `SECURITY.md` (new or updated)
   - Optional branch protection configuration summary (if requested).
7. Validate configuration
   - Confirm workflow triggers monitor only package files.
   - Ensure Dependabot entries cover each detected ecosystem with appropriate schedule.
   - Verify audit workflow executes critical-level checks aligned with Dependabot PRs.
8. Summarize outcome
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
