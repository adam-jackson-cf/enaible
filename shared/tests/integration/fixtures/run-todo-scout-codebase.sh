#!/usr/bin/env bash
set -euo pipefail

# Automated runner for the Codex /todo-scout-codebase workflow using a fixture spec.
# Mirrors the CLI invocation approach from test-todo-background.sh, preferring cdx-exec when available.

FIXTURE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${FIXTURE_DIR}/../../../.." && pwd)"
ARTIFACT_ROOT="${REPO_ROOT}/shared/tests/integration/fixtures/scout"
SPEC_PATH="${ARTIFACT_ROOT}/spec.md"
REPORT_PATH="${ARTIFACT_ROOT}/report.md"

if [[ ! -f "${SPEC_PATH}" ]]; then
  echo "ERROR: Missing spec artifact at ${SPEC_PATH}" >&2
  exit 1
fi

mkdir -p "${ARTIFACT_ROOT}"
rm -f "${REPORT_PATH}"

USER_PROMPT="$(tr '\n' ' ' < "${SPEC_PATH}")"
DAYS_DEFAULT="${DAYS:-20}"
COMMAND="/prompts:todo-scout-codebase USER_PROMPT=\"${USER_PROMPT}\" TARGET_PATH=\".\" OUT=\"${REPORT_PATH}\" DAYS=\"${DAYS_DEFAULT}\" EXCLUDE_GLOBS=\"test_codebase\""

if command -v cdx-exec >/dev/null 2>&1; then
  CODEX_CMD=(cdx-exec --model 'gpt-5-codex' --full-auto -c 'plan_tool.enabled=false' --config 'sandbox_workspace_write.network_access=true' "${COMMAND}")
elif command -v codex >/dev/null 2>&1; then
  CODEX_CMD=(codex exec --model 'gpt-5-codex' --full-auto -c 'plan_tool.enabled=false' --config 'sandbox_workspace_write.network_access=true' "${COMMAND}")
else
  echo "ERROR: Neither cdx-exec nor codex CLI is available" >&2
  exit 1
fi

(
  cd "${REPO_ROOT}"
  "${CODEX_CMD[@]}"
)

if [[ ! -s "${REPORT_PATH}" ]]; then
  echo "ERROR: Report not created at ${REPORT_PATH}" >&2
  exit 1
fi

echo "Inspect report generated at ${REPORT_PATH}" && head -n 5 "${REPORT_PATH}"
