#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: render-prompts.sh -p <prompt-id>[,<prompt-id>...] [-p ...] -t <template-id> -o <output-dir>

Options:
  -p    Prompt identifier (without .md). Provide multiple -p flags or comma-separated values.
  -t    Template identifier (file name in shared/prompts/templates without .md).
  -o    Output directory for rendered files. Created if it does not exist.
  -h    Show this help message.

The script injects the prompt body into the chosen template, applies template rule directives
(<!-- rule: ... --> comments), validates the rendered output, and writes the results into
<output-dir>/<prompt-id>.<template-id>.md.
USAGE
}

PROMPTS=()
TEMPLATE_ID=""
OUTPUT_DIR=""

while getopts "p:t:o:h" opt; do
  case "${opt}" in
    p)
      IFS=',' read -ra PARTS <<<"${OPTARG}"
      for part in "${PARTS[@]}"; do
        if [[ -n "${part}" ]]; then
          PROMPTS+=("${part}")
        fi
      done
      ;;
    t)
      TEMPLATE_ID="${OPTARG}"
      ;;
    o)
      OUTPUT_DIR="${OPTARG}"
      ;;
    h)
      usage
      exit 0
      ;;
    \?)
      usage >&2
      exit 1
      ;;
  esac
done

shift $((OPTIND - 1)) || true

if [[ ${#PROMPTS[@]} -eq 0 ]]; then
  echo "[error] at least one -p <prompt-id> is required" >&2
  usage >&2
  exit 1
fi

if [[ -z "${TEMPLATE_ID}" ]]; then
  echo "[error] -t <template-id> is required" >&2
  usage >&2
  exit 1
fi

if [[ -z "${OUTPUT_DIR}" ]]; then
  echo "[error] -o <output-dir> is required" >&2
  usage >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="${SCRIPT_DIR}"
PROMPTS_DIR="$(dirname "${SCRIPT_DIR}")"
TEMPLATE_PATH="${TEMPLATE_DIR}/${TEMPLATE_ID}.md"

if [[ ! -f "${TEMPLATE_PATH}" ]]; then
  echo "[error] template not found: ${TEMPLATE_PATH}" >&2
  exit 1
fi

CURRENT_DIR="$(pwd)"
mkdir -p "${OUTPUT_DIR}"
OUTPUT_DIR_ABS="$(cd "${OUTPUT_DIR}" && pwd)"
cd "${CURRENT_DIR}"

FAILURES=0

for prompt_id in "${PROMPTS[@]}"; do
  PROMPT_PATH="${PROMPTS_DIR}/${prompt_id}.md"
  if [[ ! -f "${PROMPT_PATH}" ]]; then
    echo "[error] prompt not found: ${PROMPT_PATH}" >&2
    FAILURES=1
    continue
  fi

  OUTPUT_PATH="${OUTPUT_DIR_ABS}/${prompt_id}.${TEMPLATE_ID}.md"

  if ! python3 - <<'PY' "${TEMPLATE_PATH}" "${PROMPT_PATH}" "${OUTPUT_PATH}" "${prompt_id}" "${TEMPLATE_ID}"; then
import sys
import re
import pathlib

template_path, prompt_path, output_path, prompt_id, template_id = sys.argv[1:]
template_text = pathlib.Path(template_path).read_text()
prompt_text = pathlib.Path(prompt_path).read_text()

if '<prompt-body>' not in template_text:
    sys.stderr.write(f"[error] {prompt_id}/{template_id}: template missing <prompt-body> placeholder\n")
    sys.exit(1)

rule_pattern = re.compile(r'<!--\s*rule:\s*(.*?)\s*-->', re.IGNORECASE)
rules = rule_pattern.findall(template_text)

replacements = []
checks = []

def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', '\''):
        return value[1:-1]
    return value

errors = []

for raw in rules:
    rule = raw.strip()
    lowered = rule.lower()
    if lowered.startswith('replace '):
        payload = rule[8:].strip()
        if '=>' not in payload:
            errors.append(f"invalid replace rule '{rule}'")
            continue
        src, dst = payload.split('=>', 1)
        src = strip_quotes(src)
        dst = strip_quotes(dst)
        if not src:
            errors.append(f"replace rule missing source in '{rule}'")
            continue
        replacements.append((src, dst))
    elif lowered.startswith('must-include '):
        value = strip_quotes(rule[len('must-include '):])
        checks.append(('must-include', value))
    elif lowered.startswith('forbid '):
        value = strip_quotes(rule[len('forbid '):])
        checks.append(('forbid', value))
    else:
        errors.append(f"unsupported rule '{rule}'")

if errors:
    for msg in errors:
        sys.stderr.write(f"[error] {prompt_id}/{template_id}: {msg}\n")
    sys.exit(1)

content = template_text.replace('<prompt-body>', prompt_text)

for src, dst in replacements:
    content = content.replace(src, dst)

content = re.sub(r'<!--\s*rule:.*?-->(\r?\n)?', '', content)

if '<prompt-body>' in content:
    sys.stderr.write(f"[error] {prompt_id}/{template_id}: placeholder <prompt-body> still present after rendering\n")
    sys.exit(1)

for kind, value in checks:
    if kind == 'must-include' and value not in content:
        sys.stderr.write(f"[error] {prompt_id}/{template_id}: expected to include '{value}'\n")
        sys.exit(1)
    if kind == 'forbid' and value in content:
        sys.stderr.write(f"[error] {prompt_id}/{template_id}: forbidden text '{value}' found\n")
        sys.exit(1)

output_path = pathlib.Path(output_path)
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(content)
PY
    FAILURES=1
  else
    printf '[ok] %s -> %s\n' "${prompt_id}" "${OUTPUT_PATH}"
  fi
done

if [[ ${FAILURES} -ne 0 ]]; then
  exit 1
fi

exit 0
