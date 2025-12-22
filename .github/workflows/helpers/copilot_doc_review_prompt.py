#!/usr/bin/env python3
"""Render the instructions file used to brief the Copilot coding agent."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

DOC_FILENAMES = {"README.md", "AGENTS.md"}
IGNORED_DIR_NAMES = {
    ".git",
    ".pytest_cache",
    ".beads",
    ".mypy_cache",
    "node_modules",
    "__pycache__",
}
COMMENT_MARKER = "<!-- copilot-doc-review -->"


def run_git(*args: str) -> str:
    """Run a git command and return stdout, raising on failure."""
    result = subprocess.run(["git", *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def discover_doc_paths() -> list[str]:
    paths: list[str] = []
    for path in Path(".").rglob("*"):
        if not path.is_file() or path.name not in DOC_FILENAMES:
            continue
        if any(part in IGNORED_DIR_NAMES for part in path.parts):
            continue
        paths.append(path.as_posix())
    return sorted(paths)


def build_diff(base: str, head: str, targets: list[str]) -> str:
    if not targets:
        return ""
    diff_output = run_git("diff", "--no-color", base, head, "--", *targets)
    return diff_output


def build_commit_summary(base: str, head: str) -> str:
    log_output = run_git("log", "--oneline", f"{base}..{head}")
    return log_output or "(no commits between refs)"


def build_diff_stat(base: str, head: str) -> str:
    stat_output = run_git("diff", "--stat", base, head)
    return stat_output or "(no file-level diffs)"


def render_prompt(args: argparse.Namespace) -> str:
    repo = args.repo
    event_name = args.event
    pr_number = args.pr_number or "n/a"
    doc_paths = discover_doc_paths()
    doc_inventory = "\n".join(f"- {path}" for path in doc_paths) or "- (no README.md or AGENTS.md files found)"
    doc_diff = build_diff(args.base, args.head, doc_paths)
    doc_diff_section = f"```diff\n{doc_diff}\n```" if doc_diff else "_No README.md or AGENTS.md edits detected in this diff; still verify for drift._"
    commit_summary = build_commit_summary(args.base, args.head)
    diff_stat = build_diff_stat(args.base, args.head)

    instructions = f"""{COMMENT_MARKER}
@copilot Please run a focused documentation audit for this change set.

## Tasking
- Inspect every `README.md` and `AGENTS.md` file for conflicts with commits introduced between `{args.base}` and `{args.head}`.
- Keep roles distinct: README.md stays end-user guidance while AGENTS.md contains developer/LLM rules—update the appropriate file rather than cross-pollinating content.
- Align voice, tone, formatting, and verbosity with existing content in each file; do not invent new sections unless necessary to resolve a conflict.
- Update documentation directly in the repo so it reflects the behavior described by the latest code and tests.
- Highlight reasoning in the pull request or issue once documentation is synchronized.

## Run Context
- Repository: `{repo}`
- Event: `{event_name}`
- Pull Request #: {pr_number}
- Workflow run: {args.run_url}
- Base ref: {args.base}
- Head ref: {args.head}

## Commit Summary
```
{commit_summary}
```

## File-Level Change Stat
```
{diff_stat}
```

## Documentation Inventory
{doc_inventory}

## README / AGENTS diff view
{doc_diff_section}

## Acceptance Criteria
1. All AGENTS.md and README.md files reflect the current code paths they document.
2. Any outdated instructions are removed instead of soft-deprecated—no fallbacks.
3. Complexity stays low; edit only what is required to restore accuracy.
4. Provide a short status reply once updates are merged.
"""
    return instructions


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Copilot doc review instructions")
    parser.add_argument("--base", required=True, help="Base git ref/sha")
    parser.add_argument("--head", required=True, help="Head git ref/sha")
    parser.add_argument("--repo", required=True, help="owner/repo slug")
    parser.add_argument("--event", required=True, help="GitHub event name")
    parser.add_argument("--run-url", required=True, help="Workflow run url")
    parser.add_argument("--output", required=True, help="File to write")
    parser.add_argument("--pr-number", help="Pull request number when present")
    args = parser.parse_args()

    prompt = render_prompt(args)
    Path(args.output).write_text(prompt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
