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
    if pyenv which python3.12 >/dev/null 2>&1; then
        UV_PYTHON="$(pyenv which python3.12)"
    fi
fi
if [[ -z "$UV_PYTHON" ]] && command -v python3.12 >/dev/null 2>&1; then
    UV_PYTHON="$(command -v python3.12)"
fi

if [[ -z "$UV_PYTHON" ]]; then
    echo "Python 3.12 is required to run quality gates. Configure pyenv or set UV_PYTHON to a 3.12 binary." >&2
    exit 1
fi

uv_project_run() {
    uv run --project "$ROOT_DIR/tools/enaible" --python "$UV_PYTHON" "$@"
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
STEP_LABELS=()
STEP_DURATIONS=()
TOOLS_VENV_DIR="$TMP_DIR/uv-tools-venv"
TOOLS_HASH_FILE="$TMP_DIR/uv-tools.hash"
TOOL_PACKAGES=(
    ruff
    pytest
    pytest-cov
    pytest-xdist
    pytest-timeout
    mypy
)
run_step() {
    local label="$1"
    shift
    echo "[ci-quality] ${label}"
    local start
    start="$(date +%s)"
    "$@"
    local end
    end="$(date +%s)"
    STEP_LABELS+=("$label")
    STEP_DURATIONS+=("$((end - start))")
}

sha256_stream() {
    if command -v shasum >/dev/null 2>&1; then
        shasum -a 256 | awk '{print $1}'
    else
        sha256sum | awk '{print $1}'
    fi
}

sha256_file() {
    if command -v shasum >/dev/null 2>&1; then
        shasum -a 256 "$1" | awk '{print $1}'
    else
        sha256sum "$1" | awk '{print $1}'
    fi
}

print_timing_summary() {
    if (( ${#STEP_LABELS[@]} == 0 )); then
        return
    fi
    echo
    echo "[ci-quality] Timing summary"
    local total=0
    for i in "${!STEP_LABELS[@]}"; do
        local duration="${STEP_DURATIONS[$i]}"
        total=$((total + duration))
        printf "[ci-quality]  - %s: %ss\n" "${STEP_LABELS[$i]}" "$duration"
    done
    printf "[ci-quality]  - total: %ss\n" "$total"
}

ensure_tools_venv() {
    local tools_hash
    tools_hash="$(
        printf '%s\n' "${TOOL_PACKAGES[@]}" "$UV_PYTHON" | sha256_stream
    )"
    if [[ -f "$TOOLS_HASH_FILE" ]] && [[ -d "$TOOLS_VENV_DIR" ]] && [[ "$(cat "$TOOLS_HASH_FILE")" == "$tools_hash" ]]; then
        echo "[ci-quality] Tool venv up to date"
        return
    fi
    rm -rf "$TOOLS_VENV_DIR"
    uv venv --python "$UV_PYTHON" "$TOOLS_VENV_DIR"
    uv pip install --python "$TOOLS_VENV_DIR/bin/python" "${TOOL_PACKAGES[@]}"
    echo "$tools_hash" > "$TOOLS_HASH_FILE"
}

cleanup() {
    rm -f "$COVERAGE_FILE"
    print_timing_summary
}
trap cleanup EXIT

run_step "Prompts/skills lint + validate" uv_project_run bash -lc '
  set -euo pipefail
  enaible prompts lint
  enaible prompts validate
  enaible skills lint
  enaible skills validate
'

run_step "Prepare shared tool venv" ensure_tools_venv

prettier_files=()
while IFS= read -r -d '' file; do
    case "$file" in
        shared/tests/fixture/*) continue ;;
    esac
    prettier_files+=("$file")
done < <(git ls-files -z "*.md" "*.yml" "*.yaml")

if [[ "$MODE" == "fix" ]]; then
    run_step "Ruff format + lint (fix)" bash -lc "
      set -euo pipefail
      \"$TOOLS_VENV_DIR/bin/ruff\" format --config shared/config/formatters/ruff.toml --force-exclude
      \"$TOOLS_VENV_DIR/bin/ruff\" check . --config shared/config/formatters/ruff.toml --fix --force-exclude
    "

    if (( ${#prettier_files[@]} )); then
        run_step "Prettier (fix)" npx --yes prettier --cache --cache-location "$TMP_DIR/prettier-cache" --write "${prettier_files[@]}"
    fi

    if [[ "$AUTO_STAGE" == "true" ]]; then
        echo "[ci-quality] Staging fixes"
        git diff --cached --name-only --diff-filter=d | xargs -r git add
    fi
else
    run_step "Ruff format + lint (check)" bash -lc "
      set -euo pipefail
      \"$TOOLS_VENV_DIR/bin/ruff\" format --config shared/config/formatters/ruff.toml --check --force-exclude
      \"$TOOLS_VENV_DIR/bin/ruff\" check . --config shared/config/formatters/ruff.toml --no-fix --force-exclude
    "

    if (( ${#prettier_files[@]} )); then
        run_step "Prettier (check)" npx --yes prettier --cache --cache-location "$TMP_DIR/prettier-cache" --check "${prettier_files[@]}"
    fi
fi

run_step "Shared analyzer unit tests + coverage + mypy" bash -lc "
  set -euo pipefail
  \"$TOOLS_VENV_DIR/bin/pytest\" -q shared/tests/unit -n auto --dist=loadfile --timeout=60 \
    --cov=core.base.analyzer_registry \
    --cov=core.base.validation_rules \
    --cov=core.config.loader \
    --cov=core.utils.architectural_pattern_detector \
    --cov=core.utils.tech_stack_detector \
    --cov-report=term-missing \
    --cov-fail-under=85
  \"$TOOLS_VENV_DIR/bin/mypy\" --config-file mypy.ini
"

enaible_hash_inputs=(
    "$ROOT_DIR/tools/enaible/uv.lock"
    "$ROOT_DIR/tools/enaible/pyproject.toml"
)
enaible_hash="$(
    {
        sha256_file "${enaible_hash_inputs[0]}"
        sha256_file "${enaible_hash_inputs[1]}"
    } | sha256_stream
)"
enaible_hash_file="$TMP_DIR/enaible-uv.hash"
enaible_env_dir="$ROOT_DIR/tools/enaible/.venv"
run_step "Enaible CLI tests (uv)" bash -lc "
  set -euo pipefail
  if [[ -f \"$enaible_hash_file\" ]] && [[ -d \"$enaible_env_dir\" ]] && [[ \"\$(cat \"$enaible_hash_file\")\" == \"$enaible_hash\" ]]; then
    echo \"[ci-quality] Enaible deps unchanged; skipping uv sync\"
  else
    uv sync --project \"$ROOT_DIR/tools/enaible\" --frozen
    echo \"$enaible_hash\" > \"$enaible_hash_file\"
  fi
  uv run --project \"$ROOT_DIR/tools/enaible\" --python \"$UV_PYTHON\" python -m pytest tools/enaible/tests -v
"

echo "[ci-quality] Completed successfully"
