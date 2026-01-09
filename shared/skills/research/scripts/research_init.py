#!/usr/bin/env python
"""Initialize a research run and persist requirements."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from schema_utils import validate_requirements


def load_questions(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        questions = []
        for idx, item in enumerate(payload, start=1):
            if isinstance(item, str):
                questions.append({"id": f"q{idx}", "text": item})
            elif isinstance(item, dict):
                text = item.get("text")
                if not text:
                    raise SystemExit("Each question object must include 'text'.")
                question_id = item.get("id") or f"q{idx}"
                questions.append({"id": question_id, "text": text})
            else:
                raise SystemExit("Questions file must be a list of strings or objects.")
        return questions
    raise SystemExit("Questions file must contain a JSON array.")


def build_artifact_root(repo_root: Path, override: str | None) -> Path:
    if override:
        return Path(override).expanduser()
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return repo_root / ".enaible" / "artifacts" / "research" / timestamp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize research requirements and artifact root."
    )
    parser.add_argument("--objective", required=True)
    parser.add_argument("--scope", required=True)
    parser.add_argument("--output-format", required=True)
    parser.add_argument("--decision-context", required=True)
    parser.add_argument(
        "--online-research", required=True, choices=["allowed", "disallowed"]
    )
    parser.add_argument("--question", action="append", default=[])
    parser.add_argument("--questions-file")
    parser.add_argument("--artifact-root")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--time-constraints")
    parser.add_argument("--target-audience")
    parser.add_argument("--domain-focus", action="append", default=[])
    parser.add_argument("--existing-knowledge")
    parser.add_argument("--allowed-source", action="append", default=[])
    parser.add_argument("--blocked-source", action="append", default=[])
    parser.add_argument("--notes")
    return parser.parse_args()


def collect_questions(args: argparse.Namespace) -> list[dict[str, Any]]:
    questions: list[dict[str, Any]] = []
    if args.questions_file:
        questions.extend(load_questions(Path(args.questions_file)))
    if args.question:
        for idx, text in enumerate(args.question, start=len(questions) + 1):
            questions.append({"id": f"q{idx}", "text": text})
    if not questions:
        raise SystemExit("At least one research question is required.")
    return questions


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    artifact_root = build_artifact_root(repo_root, args.artifact_root)
    artifact_root.mkdir(parents=True, exist_ok=True)

    questions = collect_questions(args)
    now = datetime.now(UTC)

    requirements = {
        "runId": f"research-{now.strftime('%Y%m%dT%H%M%SZ')}",
        "startedAt": now.isoformat().replace("+00:00", "Z"),
        "artifactRoot": str(artifact_root),
        "objective": args.objective,
        "scope": args.scope,
        "outputFormat": args.output_format,
        "decisionContext": args.decision_context,
        "onlineResearch": args.online_research,
        "questions": questions,
        "constraints": {
            "timeConstraints": args.time_constraints,
            "targetAudience": args.target_audience,
            "domainFocus": args.domain_focus or None,
            "existingKnowledge": args.existing_knowledge,
            "notes": args.notes,
        },
        "sources": {
            "allowed": args.allowed_source or None,
            "blocked": args.blocked_source or None,
        },
    }
    validate_requirements(requirements)

    output_path = artifact_root / "requirements.json"
    output_path.write_text(json.dumps(requirements, indent=2), encoding="utf-8")
    print(f"Wrote requirements to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
