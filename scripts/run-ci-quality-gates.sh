#!/usr/bin/env bash
# Runs the same quality gates defined in ci-quality-gates-incremental.yml so developers
# can replicate GitHub Actions locally (used by pre-commit as well).

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )/.." && pwd)"
TMP_DIR="$ROOT_DIR/.enaible/tmp/ci-quality"
mkdir -p "$TMP_DIR"

require_cmd() {
    command -v "$1" >/dev/null 2>&1 || {
        echo "Missing required command: $1" >&2
        exit 1
    }
}

require_cmd python3
require_cmd pytest
require_cmd ruff
require_cmd mypy
require_cmd uv

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

echo "[ci-quality] Running shared analyzer unit tests + coverage"
pytest -q shared/tests/unit -n auto --dist=loadfile --timeout=60 \
    --cov=core.base.analyzer_registry \
    --cov=core.base.validation_rules \
    --cov=core.config.loader \
    --cov=core.utils.architectural_pattern_detector \
    --cov=core.utils.tech_stack_detector \
    --cov-report=term-missing \
    --cov-fail-under=85

echo "[ci-quality] Ruff lint"
ruff check . --config shared/config/formatters/ruff.toml

echo "[ci-quality] Mypy type check"
PYTHONPATH="$PYTHONPATH" mypy --config-file mypy.ini

echo "[ci-quality] Enaible CLI tests (uv)"
uv sync --project "$ROOT_DIR/tools/enaible" --frozen
uv run --project "$ROOT_DIR/tools/enaible" python -m pytest tools/enaible/tests -v

echo "[ci-quality] Completed successfully"
