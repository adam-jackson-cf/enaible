from __future__ import annotations

import json
from pathlib import Path

import pytest
from analyzers.architecture.coupling_analysis import CouplingAnalyzer
from analyzers.quality.complexity_lizard import LizardComplexityAnalyzer
from analyzers.quality.jscpd_analyzer import JSCPDAnalyzer
from core.base.analyzer_base import create_analyzer_config

from shared.context.agentic_readiness import (
    docs_risk,
    history_docs,
    inventory_tests_gates,
    maintenance_score,
    mcp_scan,
    readiness_score,
    recon_map,
)


@pytest.mark.slow
def test_agentic_readiness_workflow_juice_shop(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[3]
    target = (
        project_root
        / "shared"
        / "tests"
        / "fixture"
        / "test_codebase"
        / "juice-shop-monorepo"
    )
    assert target.is_dir(), f"Expected fixture at {target}"

    artifact_root = tmp_path / "agentic-readiness"
    artifact_root.mkdir(parents=True, exist_ok=True)

    jscpd_result = _run_jscpd(target)
    (artifact_root / "quality-jscpd.json").write_text(jscpd_result.to_json())

    coupling_result = _run_coupling(target)
    (artifact_root / "architecture-coupling.json").write_text(coupling_result.to_json())

    lizard_result = _run_lizard(target)
    (artifact_root / "quality-lizard.json").write_text(lizard_result.to_json())

    recon_map.generate_recon(target, artifact_root)
    inventory_tests_gates.generate_inventory(target, artifact_root)
    docs_risk.generate_docs_risk(
        target,
        artifact_root,
        artifact_root / "quality-gates.json",
    )
    matches = mcp_scan.scan_mcp(target)
    (artifact_root / "mcp-scan.json").write_text(
        json.dumps({"matches": matches, "mcp_present": bool(matches)}, indent=2)
    )
    history_docs.generate_history_docs(target, artifact_root, 180)

    readiness_payload = readiness_score.compute_readiness(artifact_root)
    (artifact_root / "agentic-readiness.json").write_text(
        json.dumps(readiness_payload, indent=2)
    )

    maintenance_payload = maintenance_score.compute_maintenance(artifact_root)
    (artifact_root / "maintenance-score.json").write_text(
        json.dumps(maintenance_payload, indent=2)
    )

    assert (artifact_root / "recon.json").exists()
    assert (artifact_root / "repo-map.json").exists()
    assert readiness_payload["objective_score"] >= 0
    assert readiness_payload["objective_score"] <= 1
    assert maintenance_payload["objective_score"] >= 0
    assert maintenance_payload["objective_score"] <= 1


def _run_jscpd(target: Path):
    config = create_analyzer_config(
        target_path=str(target),
        min_severity="low",
        output_format="json",
    )
    config.timeout_seconds = 300
    analyzer = JSCPDAnalyzer(config=config)
    result = analyzer.analyze(str(target))
    if not result.success:
        message = (result.error_message or "").lower()
        if "jscpd is not available" in message:
            pytest.skip("jscpd not available in environment")
        pytest.fail(result.error_message or "jscpd analysis failed")
    return result


def _run_coupling(target: Path):
    config = create_analyzer_config(
        target_path=str(target),
        min_severity="low",
        output_format="json",
    )
    config.max_files = 1200
    analyzer = CouplingAnalyzer(config=config)
    result = analyzer.analyze(str(target))
    assert result.success, result.error_message
    return result


def _run_lizard(target: Path):
    config = create_analyzer_config(
        target_path=str(target),
        min_severity="low",
        output_format="json",
    )
    config.max_files = 600
    analyzer = LizardComplexityAnalyzer(config=config)
    if not getattr(analyzer, "lizard_available", True):
        pytest.skip("Lizard CLI is not available in this environment")
    result = analyzer.analyze(str(target))
    assert result.success, result.error_message
    return result
