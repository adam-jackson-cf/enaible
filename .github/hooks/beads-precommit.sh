#!/usr/bin/env bash
set -euo pipefail

if ! command -v bd >/dev/null 2>&1; then
  exit 0
fi

if [[ ! -d .beads ]]; then
  exit 0
fi

sync_branch="${BEADS_SYNC_BRANCH:-}"
if [[ -z "$sync_branch" && -f .beads/config.yaml ]]; then
  sync_branch=$(grep -E '^sync-branch:' .beads/config.yaml 2>/dev/null | head -1 | sed 's/^sync-branch:[[:space:]]*//; s/^"//; s/"$//')
fi
if [[ -n "$sync_branch" ]]; then
  exit 0
fi

if ! bd sync --flush-only >/dev/null 2>&1; then
  echo "Warning: Failed to flush bd changes to JSONL" >&2
  echo "Run 'bd sync --flush-only' manually to diagnose" >&2
fi

for f in .beads/beads.jsonl .beads/issues.jsonl .beads/deletions.jsonl; do
  if [[ -f "$f" ]]; then
    git add "$f" >/dev/null 2>&1 || true
  fi
fi
