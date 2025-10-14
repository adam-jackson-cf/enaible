#!/usr/bin/env bash
set -euo pipefail

# Automated runner for the Codex /plan-exec workflow using fixture artifacts.
# Mirrors the invocation style from test-todo-background.sh, preferring cdx-exec when available.

FIXTURE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${FIXTURE_DIR}/../../../.." && pwd)"
ARTIFACT_ROOT="${REPO_ROOT}/shared/tests/integration/fixtures/plan-exec"
SPEC_PATH="${ARTIFACT_ROOT}/spec.md"
CONTEXT_PATH="${ARTIFACT_ROOT}/report.md"
PLAN_PATH="${ARTIFACT_ROOT}/execplan.md"

if [[ ! -f "${SPEC_PATH}" ]]; then
  echo "ERROR: Missing spec artifact at ${SPEC_PATH}" >&2
  exit 1
fi

if [[ ! -f "${CONTEXT_PATH}" ]]; then
  echo "ERROR: Missing context artifact at ${CONTEXT_PATH}" >&2
  exit 1
fi

mkdir -p "${ARTIFACT_ROOT}"
rm -f "${PLAN_PATH}"

PROMPT="/plan-exec --artifact ${CONTEXT_PATH} --artifact ${SPEC_PATH} --out ${PLAN_PATH}"

if command -v cdx-exec >/dev/null 2>&1; then
  CODEX_CMD=(cdx-exec --model 'gpt-5-codex' --full-auto -c 'plan_tool.enabled=false' --config 'sandbox_workspace_write.network_access=true' "${PROMPT}")
elif command -v codex >/dev/null 2>&1; then
  CODEX_CMD=(codex exec --model 'gpt-5-codex' --full-auto -c 'plan_tool.enabled=false' --config 'sandbox_workspace_write.network_access=true' "${PROMPT}")
else
  echo "ERROR: Neither cdx-exec nor codex CLI is available" >&2
  exit 1
fi

(
  cd "${REPO_ROOT}"
  "${CODEX_CMD[@]}"
)

if [[ ! -s "${PLAN_PATH}" ]]; then
  echo "ERROR: ExecPlan not created at ${PLAN_PATH}" >&2
  exit 1
fi

echo "ExecPlan generated at ${PLAN_PATH}" && head -n 3 "${PLAN_PATH}"
