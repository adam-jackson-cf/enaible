#!/usr/bin/env python3
"""Compute maintenance score from analyzer artifacts."""

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


def compute_maintenance(artifact_root: Path) -> dict:
    metadata = {"artifact_root": str(artifact_root)}
    with log_phase("helper:maintenance_score", metadata):
        jscpd = json.loads((artifact_root / "quality-jscpd.json").read_text())
        lizard = json.loads((artifact_root / "quality-lizard.json").read_text())
        concentration = json.loads(
            (artifact_root / "history-concentration.json").read_text()
        )

        dup_pct = (
            jscpd.get("metadata", {})
            .get("statistics", {})
            .get("total", {})
            .get("percentage", 0.0)
        )
        findings = lizard.get("findings", [])
        long_functions = sum(1 for f in findings if f.get("title") == "Long Function")
        cc_outliers = sum(
            1 for f in findings if f.get("title") == "High Cyclomatic Complexity"
        )
        param_outliers = sum(
            1 for f in findings if f.get("title") == "Too Many Parameters"
        )
        concentration_ratio = concentration.get("concentration_ratio", 0.0)

        objective = round(
            (0.35 * norm_lower_is_better(dup_pct, bad=20.0, good=0.0))
            + (0.20 * norm_lower_is_better(long_functions, bad=20.0, good=0.0))
            + (0.20 * norm_lower_is_better(cc_outliers, bad=10.0, good=0.0))
            + (0.15 * norm_lower_is_better(param_outliers, bad=15.0, good=0.0))
            + (0.10 * norm_lower_is_better(concentration_ratio, bad=0.5, good=0.0)),
            4,
        )

        payload = {
            "signals": {
                "duplication_percent": dup_pct,
                "long_functions": long_functions,
                "cc_outliers": cc_outliers,
                "param_outliers": param_outliers,
                "concentration_ratio": concentration_ratio,
            },
            "objective_score": objective,
        }
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute maintenance score")
    parser.add_argument("artifact_root", help="Artifacts root directory")
    args = parser.parse_args()

    artifact_root = Path(args.artifact_root).resolve()
    payload = compute_maintenance(artifact_root)
    (artifact_root / "maintenance-score.json").write_text(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
