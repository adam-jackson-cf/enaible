#!/usr/bin/env python3
"""Compute agentic readiness KPI from artifacts."""

import argparse
import json
from pathlib import Path

from shared.context.agentic_readiness.timing import log_phase


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def norm_lower_is_better(value: float, *, bad: float, good: float = 0.0) -> float:
    if bad == good:
        return 0.0
    return clamp((bad - value) / (bad - good))


def compute_readiness(artifact_root: Path) -> dict:
    metadata = {"artifact_root": str(artifact_root)}
    with log_phase("helper:readiness_score", metadata):
        jscpd = json.loads((artifact_root / "quality-jscpd.json").read_text())
        coupling = json.loads(
            (artifact_root / "architecture-coupling.json").read_text()
        )
        concentration = json.loads(
            (artifact_root / "history-concentration.json").read_text()
        )
        quality_gates = json.loads((artifact_root / "quality-gates.json").read_text())
        docs_risk = json.loads((artifact_root / "docs-risk.json").read_text())
        mcp_scan = json.loads((artifact_root / "mcp-scan.json").read_text())

        dup_pct = (
            jscpd.get("metadata", {})
            .get("statistics", {})
            .get("total", {})
            .get("percentage", 0.0)
        )
        coupling_values = [
            f.get("evidence", {}).get("metric_value", 0)
            for f in coupling.get("findings", [])
            if f.get("evidence", {}).get("metric_value") is not None
        ]
        coupling_score = (
            round(sum(coupling_values) / len(coupling_values), 4)
            if coupling_values
            else 0.0
        )
        concentration_ratio = concentration.get("concentration_ratio", 0.0)

        consistency = round(
            (
                norm_lower_is_better(dup_pct, bad=20.0, good=0.0)
                + norm_lower_is_better(concentration_ratio, bad=0.5, good=0.0)
            )
            / 2,
            4,
        )
        parallelizability = norm_lower_is_better(coupling_score, bad=2.0, good=0.0)
        lint_enforced = 1.0 if quality_gates.get("lint_enforced") else 0.0
        tests_enforced = 1.0 if quality_gates.get("tests_enforced") else 0.0
        ci_local_parity = 1.0 if quality_gates.get("parity_ok") else 0.0
        doc_risk = 0.0 if docs_risk.get("risk_score") == 1 else 1.0
        mcp_risk = 0.0 if mcp_scan.get("mcp_present") else 1.0

        objective = round(
            (0.20 * consistency)
            + (0.20 * parallelizability)
            + (0.20 * lint_enforced)
            + (0.20 * tests_enforced)
            + (0.10 * ci_local_parity)
            + (0.05 * doc_risk)
            + (0.05 * mcp_risk),
            4,
        )

        payload = {
            "signals": {
                "duplication_percent": dup_pct,
                "concentration_ratio": concentration_ratio,
                "coupling_score": coupling_score,
                "lint_enforced": bool(quality_gates.get("lint_enforced")),
                "tests_enforced": bool(quality_gates.get("tests_enforced")),
                "ci_local_parity": bool(quality_gates.get("parity_ok")),
                "doc_risk_reasons": docs_risk.get("risk_reasons", []),
                "mcp_present": bool(mcp_scan.get("mcp_present")),
            },
            "normalized": {
                "consistency": consistency,
                "parallelizability": parallelizability,
                "lint_enforced": lint_enforced,
                "tests_enforced": tests_enforced,
                "ci_local_parity": ci_local_parity,
                "doc_risk": doc_risk,
                "mcp_risk": mcp_risk,
            },
            "objective_score": objective,
        }
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute agentic readiness KPI")
    parser.add_argument("artifact_root", help="Artifacts root directory")
    args = parser.parse_args()

    artifact_root = Path(args.artifact_root).resolve()
    payload = compute_readiness(artifact_root)
    (artifact_root / "agentic-readiness.json").write_text(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
