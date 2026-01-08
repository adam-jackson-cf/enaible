#!/usr/bin/env python3
"""Analyze documentation risk for agentic readiness."""

import argparse
import json
from pathlib import Path

from shared.context.agentic_readiness.timing import log_phase

AGENT_TERMS = {"llm", "ai", "agent", "assistant"}
REVIEW_TERMS = {
    "review",
    "code review",
    "review criteria",
    "review checklist",
    "review standards",
}
ENFORCE_MODALS = {"must", "required", "should", "shall", "never"}
ENFORCE_TERMS = {
    "lint",
    "format",
    "style",
    "typecheck",
    "mypy",
    "ruff",
    "eslint",
    "prettier",
    "flake8",
    "golangci",
    "clippy",
    "test",
    "ci",
    "pre-commit",
    "precommit",
    "gate",
}

DOC_CANDIDATES = [
    "README.md",
    "CONTRIBUTING.md",
    "AGENTS.md",
    "ARCHITECTURE.md",
]

DOC_ROOTS = [
    "docs",
    "documentation",
    "handbook",
    "runbooks",
    "guides",
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(errors="ignore")
    except Exception:
        return ""


def generate_docs_risk(
    root: Path, artifact_root: Path, quality_gates_path: Path
) -> None:
    metadata = {
        "target": str(root),
        "artifact_root": str(artifact_root),
        "quality_gates": str(quality_gates_path),
    }
    with log_phase("helper:docs_risk", metadata):
        quality_gates = json.loads(quality_gates_path.read_text())
        lint_config_present = bool(quality_gates.get("lint_config_present"))

        doc_files: list[Path] = []
        for rel in DOC_CANDIDATES:
            candidate = root / rel
            if candidate.exists():
                doc_files.append(candidate)
        for rel in DOC_ROOTS:
            root_dir = root / rel
            if root_dir.exists():
                doc_files.extend(sorted(root_dir.rglob("*.md")))
        doc_files = list(dict.fromkeys(doc_files))

        enforceable_hits: list[str] = []
        review_standards_present = False
        for doc in doc_files:
            text = read_text(doc)
            lower = text.lower()
            if (
                lower
                and any(term in lower for term in AGENT_TERMS)
                and any(term in lower for term in REVIEW_TERMS)
            ):
                review_standards_present = True
            for line in lower.splitlines():
                if any(modal in line for modal in ENFORCE_MODALS) and any(
                    term in line for term in ENFORCE_TERMS
                ):
                    enforceable_hits.append(str(doc))
                    break

        auto_included_docs = (
            [str(root / "AGENTS.md")] if (root / "AGENTS.md").exists() else []
        )
        guidance_present = bool(doc_files)
        doc_rules_unenforced = bool(enforceable_hits) and not lint_config_present

        risk_reasons: list[str] = []
        if auto_included_docs:
            risk_reasons.append("auto_included_docs_present")
        if enforceable_hits:
            risk_reasons.append("enforceable_rules_in_docs")
        if doc_rules_unenforced:
            risk_reasons.append("doc_rules_without_lint_config")
        if guidance_present and not review_standards_present:
            risk_reasons.append("missing_llm_review_standards")

        payload = {
            "doc_files": [str(p) for p in doc_files],
            "doc_roots": [str(root / rel) for rel in DOC_ROOTS],
            "auto_included_docs": auto_included_docs,
            "enforceable_hits": enforceable_hits,
            "review_standards_present": review_standards_present,
            "doc_rules_unenforced": doc_rules_unenforced,
            "risk_reasons": risk_reasons,
            "risk_score": 1 if risk_reasons else 0,
        }
        (artifact_root / "docs-risk.json").write_text(json.dumps(payload, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute documentation risk artifacts")
    parser.add_argument("target", help="Absolute path to analyzed target")
    parser.add_argument("artifact_root", help="Artifacts root directory")
    parser.add_argument(
        "quality_gates", help="Path to quality-gates.json for lint context"
    )
    args = parser.parse_args()

    root = Path(args.target).resolve()
    artifact_root = Path(args.artifact_root).resolve()
    artifact_root.mkdir(parents=True, exist_ok=True)
    generate_docs_risk(root, artifact_root, Path(args.quality_gates).resolve())


if __name__ == "__main__":
    main()
