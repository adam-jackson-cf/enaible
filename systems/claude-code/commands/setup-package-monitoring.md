---
argument-hint: [--audit-level=critical] [--package-file=<path>] [--exclude=<path>] [--branch-protection=true]
---

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

1. **Try project-level .claude folder**:

   ```bash
   Glob: ".claude/scripts/setup/security/*.py"
   ```

2. **Try user-level .claude folder**:

   ```bash
   Bash: ls "$HOME/.claude/scripts/setup/security/"
   ```

3. **Interactive fallback if not found**:
   - List searched locations: `.claude/scripts/setup/security/` and `$HOME/.claude/scripts/setup/security/`
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

### Phase 3: Configuration Generation

1. **Multi-Ecosystem Dependabot Config**: Comprehensive dependency updates
2. **Path-Triggered CI Workflow**: Minimal auditing only when package files change
3. **Security Policy Documentation**: Updated to reflect package monitoring approach

## Key Differences from Previous Version

### What Changed:

- ❌ **Removed**: Full security scanning, dependency pinning automation, complex reporting
- ❌ **Removed**: JavaScript-only limitation
- ✅ **Added**: Multi-language support (Python, Go, Rust, .NET, TypeScript/JavaScript)
- ✅ **Added**: Smart path-based triggers (only runs when package files change)
- ✅ **Added**: Critical-only auditing to complement Dependabot
- ✅ **Added**: Multi-ecosystem Dependabot configuration

### Why This Approach:

- **No Duplication**: Dependabot handles comprehensive monitoring, CI provides safety net
- **Efficient CI**: Only runs when dependencies actually change
- **Multi-Language**: Supports entire project tech stack
- **Focused**: Critical vulnerabilities only, avoiding noise

## Output Requirements

- **Path-triggered GitHub Actions audit workflow** (runs only on package file changes)
- **Multi-ecosystem Dependabot configuration** for automated dependency updates across all languages
- **Updated security policy documentation** reflecting package monitoring approach
- **Branch protection rules configuration** (if requested)
- **Ecosystem detection summary** showing all detected languages and package managers

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
