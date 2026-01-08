#!/usr/bin/env python3
"""Generate history concentration and docs freshness artifacts."""

import argparse
import json
import subprocess
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from shared.context.agentic_readiness.timing import log_phase


def run_git_command(args: list[str]) -> list[str]:
    try:
        output = subprocess.check_output(args, text=True)
    except subprocess.CalledProcessError as exc:
        raise SystemExit(f"git command failed: {exc}") from exc
    return output.splitlines()


def history_concentration(root: Path, days: int) -> dict:
    log_cmd = [
        "git",
        "-C",
        str(root),
        "log",
        f"--since={days} days ago",
        "--name-only",
        "--pretty=format:",
    ]
    files = [line for line in run_git_command(log_cmd) if line.strip()]
    counts = Counter(files)
    total = sum(counts.values())
    top10 = sum(c for _, c in counts.most_common(10))
    concentration = round(top10 / total, 4) if total else 0.0
    return {
        "window_days": days,
        "total_file_touches": total,
        "top10_file_touches": top10,
        "concentration_ratio": concentration,
    }


def docs_freshness(root: Path) -> dict:
    doc_candidates = [
        root / "README.md",
        root / "CONTRIBUTING.md",
        root / "AGENTS.md",
        root / "docs",
    ]
    doc_paths = [p for p in doc_candidates if p.exists()]
    doc_age_days = 999
    last_doc_ts = None
    if doc_paths:
        args = ["git", "-C", str(root), "log", "-1", "--format=%ct", "--"] + [
            str(p) for p in doc_paths
        ]
        lines = run_git_command(args)
        if lines:
            ts = lines[0].strip()
            if ts:
                last_doc_ts = int(ts)
                doc_age_days = int(
                    (datetime.now(UTC).timestamp() - last_doc_ts) / 86400
                )
    return {
        "candidates": [str(p) for p in doc_candidates],
        "present": [str(p) for p in doc_paths],
        "last_doc_commit_unix": last_doc_ts,
        "doc_age_days": doc_age_days,
    }


def generate_history_docs(root: Path, artifact_root: Path, days: int) -> None:
    metadata = {"target": str(root), "artifact_root": str(artifact_root), "days": days}
    with log_phase("helper:history_docs", metadata):
        (artifact_root / "history-concentration.json").write_text(
            json.dumps(history_concentration(root, days), indent=2)
        )
        (artifact_root / "docs-freshness.json").write_text(
            json.dumps(docs_freshness(root), indent=2)
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate history/docs artifacts")
    parser.add_argument("target", help="Absolute path to analyzed target")
    parser.add_argument("artifact_root", help="Artifacts root directory")
    parser.add_argument(
        "days", type=int, nargs="?", default=180, help="History window in days"
    )
    args = parser.parse_args()

    root = Path(args.target).resolve()
    artifact_root = Path(args.artifact_root).resolve()
    artifact_root.mkdir(parents=True, exist_ok=True)
    generate_history_docs(root, artifact_root, args.days)


if __name__ == "__main__":
    main()
