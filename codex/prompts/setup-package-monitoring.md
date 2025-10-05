# setup-package-monitoring v3.0

**Mindset**: "Smart dependency monitoring with Dependabot + minimal CI auditing"

## Behavior

Sets up comprehensive package monitoring through:

1. **Dependabot** for automated dependency updates across all detected languages
2. **Minimal CI auditing** that ONLY runs when package files change
3. **Critical-only vulnerability blocking** to avoid duplication with Dependabot

## Workflow Process

### Phase 1: Multi-Language Ecosystem Detection

Automatically detects ALL package ecosystems in the project:

- **Python**: requirements.txt, pyproject.toml, Pipfile, setup.py, setup.cfg
- **JavaScript/TypeScript**: package.json with lock files (npm, yarn, pnpm, bun)
- **Go**: go.mod, go.sum
- **Rust**: Cargo.toml, Cargo.lock
- **.NET**: _.csproj, _.sln, packages.config

**Efficiency Arguments (Optional):**

- **--package-file=<path>**: Skip ecosystem detection by specifying package file directly (e.g., `--package-file=requirements.txt`)
- **--exclude=<path>**: Exclude directories/files from package search (e.g., `--exclude=node_modules`, `--exclude=vendor`)

When `--package-file` is provided, the command bypasses automatic detection and uses the specified file directly.
Multiple `--exclude` arguments can be provided to exclude multiple paths.

### Phase 2: Script Integration

**FIRST - Resolve SCRIPT_PATH:**

1. **Try project-level .codex folder**:

   ```bash
   Glob: ".codex/scripts/setup/security/*.py"
   ```

2. **Try user-level .codex folder**:

   ```bash
   Bash: ls "$HOME/.codex/scripts/setup/security/"
   ```

3. **Interactive fallback if not found**:
   - List searched locations: `.codex/scripts/setup/security/` and `$HOME/.codex/scripts/setup/security/`
   - Ask user: "Could not locate package monitoring setup scripts. Please provide full path to the scripts directory:"
   - Validate provided path contains expected scripts (setup_package_monitoring.py)
   - Set SCRIPT_PATH to user-provided location

**Pre-flight environment check (fail fast if imports not resolved):**

```bash
SCRIPTS_ROOT="$(cd "$(dirname \"$SCRIPT_PATH\")/../.." && pwd)"
PYTHONPATH="$SCRIPTS_ROOT" python -c "import core.base; print('env OK')"
```

**THEN - Execute Package Monitoring Setup Script:**

```bash
PYTHONPATH="$SCRIPTS_ROOT" python -m setup.security.setup_package_monitoring \
  --audit-level "${AUDIT_LEVEL:-critical}" \
  --branch-protection "${SETUP_BRANCH_PROTECTION:-false}" \
  ${PACKAGE_FILE:+--package-file "$PACKAGE_FILE"} \
  ${EXCLUDE_PATH:+--exclude "$EXCLUDE_PATH"}
```

## Example Usage

```bash
# Setup with default critical-only auditing
/setup-package-monitoring

# Setup with different audit level
/setup-package-monitoring --audit-level=moderate

# Setup with branch protection
/setup-package-monitoring --branch-protection=true

# Skip search by specifying package file directly
/setup-package-monitoring --package-file=requirements.txt

# Exclude large directories from search
/setup-package-monitoring --exclude=node_modules --exclude=vendor

# Combine for maximum efficiency
/setup-package-monitoring --package-file=package.json --exclude=dist --audit-level=moderate
```

## Expected Output

```
🔧 Setting up package monitoring for python, javascript, go with audit level: critical
✅ Created .github/workflows/package-audit.yml (path-triggered audit for package changes)
✅ Created .github/dependabot.yml (multi-ecosystem dependency updates)
✅ Created SECURITY.md (security policy documentation)

🔧 Configuration:
  - Ecosystems: python, javascript, go
  - Audit Level: critical
  - Branch Protection: false

🚀 Next Steps:
  1. Commit and push these files to activate the workflows
  2. Check the 'Actions' tab in GitHub to see workflows
  3. Review Dependabot PRs for security updates
  4. Package monitoring will only run when dependency files change

🔍 Detected ecosystems: python, javascript, go
⚡ Minimal CI: Audit workflow only runs when package files change
```

$ARGUMENTS
