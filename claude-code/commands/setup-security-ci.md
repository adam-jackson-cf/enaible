---
argument-hint: [--setup-branch-protection] [--audit-level=moderate]
---

# setup-security-ci v2.0

**Mindset**: "Automate security gates and dependency management across all package managers"

## Behavior

Creates a comprehensive security CI pipeline with universal package manager support, dependency auditing, pinning checks, and optional branch protection rules.

## Workflow Process

### Phase 1: Package Manager Detection

1. **Detect Package Manager from Lock Files**

   ```bash
   # Detect primary package manager
   if [[ -f "package-lock.json" ]]; then
     PACKAGE_MANAGER="npm"
   elif [[ -f "yarn.lock" ]]; then
     PACKAGE_MANAGER="yarn"
   elif [[ -f "pnpm-lock.yaml" ]]; then
     PACKAGE_MANAGER="pnpm"
   elif [[ -f "bun.lockb" ]]; then
     PACKAGE_MANAGER="bun"
   else
     PACKAGE_MANAGER="none"
     echo "❌ No JavaScript package manager detected"
     echo "   Please ensure you have a lock file (package-lock.json, yarn.lock, pnpm-lock.yaml, or bun.lockb)"
     exit 1
   fi

   echo "🔍 Detected package manager: $PACKAGE_MANAGER"
   ```

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
   - Ask user: "Could not locate security setup scripts. Please provide full path to the scripts directory:"
   - Validate provided path contains expected scripts (setup_security_ci.py)
   - Set SCRIPT_PATH to user-provided location

**Pre-flight environment check (fail fast if imports not resolved):**

```bash
SCRIPTS_ROOT="$(cd "$(dirname \"$SCRIPT_PATH\")/../.." && pwd)"
PYTHONPATH="$SCRIPTS_ROOT" python -c "import core.base; print('env OK')"
```

**THEN - Execute Security CI Setup Script:**

```bash
PYTHONPATH="$SCRIPTS_ROOT" python -m setup.security.setup_security_ci \
  --package-manager "$PACKAGE_MANAGER" \
  --audit-level "${AUDIT_LEVEL:-moderate}" \
  --branch-protection "${SETUP_BRANCH_PROTECTION:-false}"
```

## Output Requirements

- Comprehensive GitHub Actions security workflow with multi-package manager support
- Dependabot configuration for automated dependency updates
- Security policy documentation with vulnerability reporting procedures
- Branch protection rules configuration (if requested)
- Initial security audit results and recommendations

$ARGUMENTS
