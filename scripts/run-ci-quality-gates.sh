#!/usr/bin/env bash
# Runs the same quality gates defined in ci-quality-gates-incremental.yml so developers
# can replicate GitHub Actions locally (used by git pre-commit hook as well).

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )/.." && pwd)"
TMP_DIR="$ROOT_DIR/.enaible/tmp/ci-quality"
mkdir -p "$TMP_DIR"

MODE="check"
AUTO_STAGE=false

usage() {
    cat <<'USAGE'
Usage: scripts/run-ci-quality-gates.sh [--fix] [--stage]

Options:
  --fix     Apply auto-fixes where supported (ruff, prettier, ruff format).
  --stage   Stage tracked file changes after fixes (requires git).
  --help    Show this help text.
USAGE
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --fix)
            MODE="fix"
            ;;
        --stage)
            AUTO_STAGE=true
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            usage
            exit 1
            ;;
    esac
    shift
done

require_cmd() {
    command -v "$1" >/dev/null 2>&1 || {
        echo "Missing required command: $1" >&2
        exit 1
    }
}

require_cmd git
require_cmd uv
require_cmd npx

UV_PYTHON=""
if command -v pyenv >/dev/null 2>&1; then
    UV_PYTHON="$(pyenv which python)"
fi

uv_run() {
    if [[ -n "$UV_PYTHON" ]]; then
        uv run --python "$UV_PYTHON" "$@"
    else
        uv run "$@"
    fi
}

cd "$ROOT_DIR"
export PYTHONPATH="${ROOT_DIR}/shared${PYTHONPATH:+:${PYTHONPATH}}"
if [[ -n "${PYTEST_ADDOPTS:-}" ]]; then
    export PYTEST_ADDOPTS="$PYTEST_ADDOPTS --cache-clear"
else
    export PYTEST_ADDOPTS="--cache-clear"
fi
COVERAGE_FILE="$(mktemp "$TMP_DIR/coverage.XXXXXX")"
export COVERAGE_FILE
cleanup() {
    rm -f "$COVERAGE_FILE"
}
trap cleanup EXIT

prettier_files=()
while IFS= read -r -d '' file; do
    case "$file" in
        shared/tests/fixture/*) continue ;;
    esac
    prettier_files+=("$file")
done < <(git ls-files -z "*.md" "*.yml" "*.yaml")

if [[ "$MODE" == "fix" ]]; then
    echo "[ci-quality] Ruff format (fix)"
    uv_run --with ruff ruff format --config shared/config/formatters/ruff.toml

    echo "[ci-quality] Ruff lint (fix)"
    uv_run --with ruff ruff check . --config shared/config/formatters/ruff.toml --fix

    if (( ${#prettier_files[@]} )); then
        echo "[ci-quality] Prettier (fix)"
        npx --yes prettier --write "${prettier_files[@]}"
    fi

    if [[ "$AUTO_STAGE" == "true" ]]; then
        echo "[ci-quality] Staging tracked fixes"
        git add -u
    fi
else
    echo "[ci-quality] Ruff format (check)"
    uv_run --with ruff ruff format --config shared/config/formatters/ruff.toml --check

    echo "[ci-quality] Ruff lint (check)"
    uv_run --with ruff ruff check . --config shared/config/formatters/ruff.toml --no-fix

    if (( ${#prettier_files[@]} )); then
        echo "[ci-quality] Prettier (check)"
        npx --yes prettier --check "${prettier_files[@]}"
    fi
fi

echo "[ci-quality] Running shared analyzer unit tests + coverage"
uv_run --with pytest --with pytest-cov --with pytest-xdist --with pytest-timeout pytest -q shared/tests/unit -n auto --dist=loadfile --timeout=60 \
    --cov=core.base.analyzer_registry \
    --cov=core.base.validation_rules \
    --cov=core.config.loader \
    --cov=core.utils.architectural_pattern_detector \
    --cov=core.utils.tech_stack_detector \
    --cov-report=term-missing \
    --cov-fail-under=85

echo "[ci-quality] Mypy type check"
PYTHONPATH="$PYTHONPATH" uv_run --with mypy mypy --config-file mypy.ini

echo "[ci-quality] Enaible CLI tests (uv)"
uv sync --project "$ROOT_DIR/tools/enaible" --frozen
uv run --project "$ROOT_DIR/tools/enaible" python -m pytest tools/enaible/tests -v

echo "[ci-quality] Completed successfully"
