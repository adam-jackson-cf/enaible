"""E2E smoke test for the agentic readiness workflow.

This test exercises the full workflow via the CLI runner as a black-box subprocess,
validating that all expected artifacts are generated and timing logs contain all phases.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

# Default fixture path
DEFAULT_FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "fixture"
    / "test_codebase"
    / "juice-shop-monorepo"
)

# Expected artifacts from the workflow
EXPECTED_ARTIFACTS = [
    "recon.json",
    "repo-map.json",
    "quality-jscpd.json",
    "architecture-coupling.json",
    "quality-lizard.json",
    "tests-inventory.json",
    "quality-gates.json",
    "docs-risk.json",
    "mcp-scan.json",
    "history-concentration.json",
    "docs-freshness.json",
    "agentic-readiness.json",
    "maintenance-score.json",
    "report.md",
]

# Expected timing phases
EXPECTED_PHASES = [
    "helper:recon",
    "analyzer:jscpd",
    "analyzer:coupling",
    "analyzer:lizard",
    "helper:inventory_tests",
    "helper:docs_risk",
    "helper:mcp_scan",
    "helper:history_docs",
    "helper:readiness_score",
    "helper:maintenance_score",
]


def _get_fixture_path() -> Path:
    """Get the fixture path from environment or use default."""
    env_path = os.environ.get("AGENTIC_READINESS_FIXTURE")
    if env_path:
        return Path(env_path).resolve()
    return DEFAULT_FIXTURE


def _get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).resolve().parents[3]


@pytest.mark.slow
def test_agentic_readiness_workflow_e2e(tmp_path: Path) -> None:
    """Test the full agentic readiness workflow via CLI subprocess."""
    fixture_path = _get_fixture_path()
    if not fixture_path.is_dir():
        pytest.skip(f"Fixture not found: {fixture_path}")

    timing_log = tmp_path / "timing.log"
    artifact_root = tmp_path / "artifacts"
    project_root = _get_project_root()

    # Prepare environment
    env = {
        **os.environ,
        "AGENTIC_READINESS_TIMING_LOG": str(timing_log),
        "PYTHONPATH": str(project_root / "shared"),
    }

    # Run the workflow via CLI
    command = [
        "uv",
        "run",
        "--directory",
        str(project_root / "tools" / "enaible"),
        "enaible",
        "workflows",
        "run",
        "analyze-agentic-readiness",
        "--target",
        str(fixture_path),
        "--artifact-root",
        str(artifact_root),
        "--auto",
    ]

    result = subprocess.run(
        command,
        env=env,
        capture_output=True,
        text=True,
        timeout=600,
        cwd=str(project_root),
    )

    # Write captured output to log file for debugging
    (tmp_path / "stdout.log").write_text(result.stdout)
    (tmp_path / "stderr.log").write_text(result.stderr)

    # Assert exit code
    assert result.returncode == 0, (
        f"Workflow failed with exit code {result.returncode}.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )

    # Assert all expected artifacts exist
    missing_artifacts = []
    for artifact in EXPECTED_ARTIFACTS:
        if not (artifact_root / artifact).exists():
            missing_artifacts.append(artifact)

    assert not missing_artifacts, (
        f"Missing artifacts: {missing_artifacts}\n"
        f"Available: {[p.name for p in artifact_root.iterdir()] if artifact_root.exists() else 'directory not created'}"
    )

    # Assert timing log contains all phases
    if timing_log.exists():
        timing_content = timing_log.read_text()
        missing_phases = []
        for phase in EXPECTED_PHASES:
            if f'"phase": "{phase}"' not in timing_content:
                missing_phases.append(phase)

        assert not missing_phases, (
            f"Missing timing phases: {missing_phases}\n"
            f"Timing log contents:\n{timing_content[:2000]}..."
        )

        # Parse and validate timing entries
        timing_entries = []
        for line in timing_content.strip().split("\n"):
            if line.strip():
                try:
                    timing_entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        # Check we have start/end pairs for phases
        starts = {e["phase"] for e in timing_entries if e.get("event") == "start"}
        ends = {e["phase"] for e in timing_entries if e.get("event") == "end"}
        unfinished = starts - ends
        assert not unfinished, f"Phases started but not finished: {unfinished}"

    # Validate readiness score structure
    readiness_path = artifact_root / "agentic-readiness.json"
    readiness_data = json.loads(readiness_path.read_text())
    assert "objective_score" in readiness_data
    assert 0 <= readiness_data["objective_score"] <= 1
    assert "signals" in readiness_data
    assert "normalized" in readiness_data

    # Validate maintenance score structure
    maintenance_path = artifact_root / "maintenance-score.json"
    maintenance_data = json.loads(maintenance_path.read_text())
    assert "objective_score" in maintenance_data
    assert 0 <= maintenance_data["objective_score"] <= 1
    assert "signals" in maintenance_data


@pytest.mark.slow
def test_agentic_readiness_workflow_list() -> None:
    """Test the workflow list command."""
    project_root = _get_project_root()
    command = [
        "uv",
        "run",
        "--directory",
        str(project_root / "tools" / "enaible"),
        "enaible",
        "workflows",
        "list",
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=60,
        cwd=str(project_root),
    )

    assert result.returncode == 0
    assert "analyze-agentic-readiness" in result.stdout


@pytest.mark.slow
def test_agentic_readiness_workflow_unknown() -> None:
    """Test that unknown workflow names are rejected."""
    project_root = _get_project_root()
    command = [
        "uv",
        "run",
        "--directory",
        str(project_root / "tools" / "enaible"),
        "enaible",
        "workflows",
        "run",
        "unknown-workflow",
        "--target",
        ".",
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=60,
        cwd=str(project_root),
    )

    assert result.returncode != 0
    assert "Unknown workflow" in result.stderr or "unknown-workflow" in result.stderr
