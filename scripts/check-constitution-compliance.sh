#!/usr/bin/env bash
# Constitution Compliance Checker
# Verifies adherence to constitution.md principles via deterministic checks

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

check_pass() {
    echo -e "${GREEN}PASS${NC}: $1"
    PASS_COUNT=$((PASS_COUNT + 1))
}

check_fail() {
    echo -e "${RED}FAIL${NC}: $1"
    FAIL_COUNT=$((FAIL_COUNT + 1))
}

check_warn() {
    echo -e "${YELLOW}WARN${NC}: $1"
    WARN_COUNT=$((WARN_COUNT + 1))
}

echo "Constitution Compliance Check"
echo "=============================="
echo ""

# 1. Complexity gate enabled
echo "1. Checking complexity gate (C901 with max-complexity=10)..."
RUFF_CONFIG="$REPO_ROOT/shared/config/formatters/ruff.toml"
if [ -f "$RUFF_CONFIG" ]; then
    if grep -q '"C901"' "$RUFF_CONFIG" && grep -q 'max-complexity = 10' "$RUFF_CONFIG"; then
        check_pass "Complexity gate enabled (C901, max=10)"
    else
        check_fail "Complexity gate not properly configured in ruff.toml"
    fi
else
    check_fail "ruff.toml not found at $RUFF_CONFIG"
fi

# 2. Pre-commit/CI parity
echo ""
echo "2. Checking pre-commit/CI parity..."
PRECOMMIT_CONFIG="$REPO_ROOT/.pre-commit-config.yaml"
CI_WORKFLOW="$REPO_ROOT/.github/workflows/ci-quality-gates-incremental.yml"
if [ -f "$PRECOMMIT_CONFIG" ] && [ -f "$CI_WORKFLOW" ]; then
    # Check both reference the same quality gates script
    if grep -q 'run-ci-quality-gates.sh' "$PRECOMMIT_CONFIG" && grep -q 'run-ci-quality-gates.sh' "$CI_WORKFLOW"; then
        check_pass "Pre-commit and CI use same quality gates script"
    else
        check_fail "Pre-commit and CI do not use the same quality gates script"
    fi
else
    check_fail "Pre-commit config or CI workflow not found"
fi

# 3. Lock files tracked
echo ""
echo "3. Checking lock files are tracked..."
cd "$REPO_ROOT"
LOCK_FILES_FOUND=0
LOCK_FILES_TRACKED=0

for lockfile in uv.lock package-lock.json yarn.lock pnpm-lock.yaml poetry.lock Pipfile.lock; do
    if [ -f "$lockfile" ]; then
        LOCK_FILES_FOUND=$((LOCK_FILES_FOUND + 1))
        if git ls-files --error-unmatch "$lockfile" >/dev/null 2>&1; then
            LOCK_FILES_TRACKED=$((LOCK_FILES_TRACKED + 1))
        fi
    fi
done

# Check tools/enaible/uv.lock specifically
if [ -f "tools/enaible/uv.lock" ]; then
    LOCK_FILES_FOUND=$((LOCK_FILES_FOUND + 1))
    if git ls-files --error-unmatch "tools/enaible/uv.lock" >/dev/null 2>&1; then
        LOCK_FILES_TRACKED=$((LOCK_FILES_TRACKED + 1))
    fi
fi

if [ "$LOCK_FILES_FOUND" -gt 0 ] && [ "$LOCK_FILES_TRACKED" -eq "$LOCK_FILES_FOUND" ]; then
    check_pass "All lock files are git-tracked ($LOCK_FILES_TRACKED/$LOCK_FILES_FOUND)"
elif [ "$LOCK_FILES_FOUND" -gt 0 ]; then
    check_warn "Some lock files not tracked ($LOCK_FILES_TRACKED/$LOCK_FILES_FOUND)"
else
    check_warn "No lock files found"
fi

# 4. Toolchain version pinned
echo ""
echo "4. Checking toolchain version pinning..."
VERSION_FILES=(.python-version .node-version .nvmrc .tool-versions rust-toolchain.toml)
VERSION_PINNED=false
for vf in "${VERSION_FILES[@]}"; do
    if [ -f "$REPO_ROOT/$vf" ]; then
        VERSION_PINNED=true
        check_pass "Toolchain version pinned via $vf"
        break
    fi
done
if [ "$VERSION_PINNED" = false ]; then
    check_warn "No toolchain version file found (.python-version, .nvmrc, etc.)"
fi

# 5. No MCP config
echo ""
echo "5. Checking for MCP configuration (should not exist)..."
MCP_FOUND=false
for mcp_path in "$REPO_ROOT/mcp.json" "$REPO_ROOT/.mcp" "$REPO_ROOT/mcp.config.json" "$REPO_ROOT/.mcp.json"; do
    if [ -e "$mcp_path" ]; then
        MCP_FOUND=true
        check_fail "MCP configuration found: $mcp_path"
    fi
done
if [ "$MCP_FOUND" = false ]; then
    check_pass "No MCP configuration found"
fi

# 6. Symbol naming (check for V2/Refactored/Updated suffixes in code)
echo ""
echo "6. Checking symbol naming conventions..."
# Search for function/class definitions with problematic suffixes (excluding .venv and node_modules)
NAMING_VIOLATIONS=$(grep -rn --include="*.py" --exclude-dir=".venv" --exclude-dir="venv" --exclude-dir="node_modules" --exclude-dir="__pycache__" -E "(def|class)\s+\w+(V2|Refactored|Updated|New|Old|Legacy)\b" "$REPO_ROOT/shared" "$REPO_ROOT/tools" 2>/dev/null || true)
if [ -n "$NAMING_VIOLATIONS" ]; then
    check_fail "Symbol naming violations found (V2/Refactored/Updated/New/Old/Legacy suffixes):"
    echo "$NAMING_VIOLATIONS" | head -10
    if [ "$(echo "$NAMING_VIOLATIONS" | wc -l)" -gt 10 ]; then
        echo "  ... and more"
    fi
else
    check_pass "No symbol naming violations found"
fi

# 7. Constitution file exists
echo ""
echo "7. Checking constitution.md exists..."
if [ -f "$REPO_ROOT/constitution.md" ]; then
    check_pass "constitution.md exists"
else
    check_fail "constitution.md not found"
fi

# 8. Pre-commit hooks installed
echo ""
echo "8. Checking pre-commit hooks..."
if [ -f "$REPO_ROOT/.git/hooks/pre-commit" ]; then
    check_pass "Pre-commit hook installed"
else
    check_warn "Pre-commit hook not installed (run 'pre-commit install')"
fi

# Summary
echo ""
echo "=============================="
echo "Summary"
echo "=============================="
echo -e "${GREEN}Passed${NC}: $PASS_COUNT"
echo -e "${RED}Failed${NC}: $FAIL_COUNT"
echo -e "${YELLOW}Warnings${NC}: $WARN_COUNT"
echo ""

if [ "$FAIL_COUNT" -gt 0 ]; then
    echo -e "${RED}Constitution compliance check FAILED${NC}"
    exit 1
else
    echo -e "${GREEN}Constitution compliance check PASSED${NC}"
    exit 0
fi
