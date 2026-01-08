"""Agentic readiness workflow orchestrator."""

from __future__ import annotations

import json
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

# Ensure shared modules are importable
# Add project root to PYTHONPATH so 'shared' package is importable
PROJECT_ROOT = Path(__file__).resolve().parents[5]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from shared.context.agentic_readiness import (  # noqa: E402
    docs_risk,
    history_docs,
    inventory_tests_gates,
    maintenance_score,
    mcp_scan,
    readiness_score,
    recon_map,
)
from shared.context.agentic_readiness.timing import (  # noqa: E402
    log_phase,
    run_command_with_timing,
)

DEFAULT_EXCLUDES = [
    "dist/",
    "build/",
    "node_modules/",
    "__pycache__/",
    ".next/",
    "vendor/",
    ".venv/",
    ".mypy_cache/",
    ".ruff_cache/",
    ".pytest_cache/",
    ".gradle/",
    "target/",
    "bin/",
    "obj/",
    "coverage/",
    ".turbo/",
    ".svelte-kit/",
    ".cache/",
    ".enaible/artifacts/",
]


def _build_exclude_args(excludes: Sequence[str]) -> list[str]:
    """Build --exclude arguments for analyzer CLI calls."""
    args: list[str] = []
    for pattern in excludes:
        args.extend(["--exclude", pattern])
    return args


def _collect_blockers(
    quality_gates: dict, docs_risk_data: dict, mcp_data: dict
) -> list[str]:
    """Collect readiness blockers from analysis results."""
    blockers = []
    if not quality_gates.get("lint_enforced"):
        blockers.append("Lint not enforced in pre-commit + CI")
    if not quality_gates.get("tests_enforced"):
        blockers.append("Integration/smoke not enforced in pre-commit + CI")
    if not quality_gates.get("parity_ok"):
        blockers.append("CI/local parity gaps detected")
    if docs_risk_data.get("risk_reasons"):
        blockers.append(f"Doc risks: {', '.join(docs_risk_data['risk_reasons'])}")
    if mcp_data.get("mcp_present"):
        blockers.append("MCP configuration present (requires review)")
    return blockers


def _generate_report(artifact_root: Path, target: Path) -> None:
    """Generate report.md summarizing the workflow results."""
    # Load all artifacts
    recon = json.loads((artifact_root / "recon.json").read_text())
    repo_map = json.loads((artifact_root / "repo-map.json").read_text())
    readiness = json.loads((artifact_root / "agentic-readiness.json").read_text())
    maintenance = json.loads((artifact_root / "maintenance-score.json").read_text())
    quality_gates = json.loads((artifact_root / "quality-gates.json").read_text())
    docs_risk_data = json.loads((artifact_root / "docs-risk.json").read_text())
    mcp_data = json.loads((artifact_root / "mcp-scan.json").read_text())
    tests_inv = json.loads((artifact_root / "tests-inventory.json").read_text())
    # Load history concentration (used for validation only, data in signals)
    json.loads((artifact_root / "history-concentration.json").read_text())

    signals = readiness.get("signals", {})

    # Build report sections
    lines = [
        "# Agentic Readiness Report",
        "",
        f"- **Target**: `{target}`",
        f"- **Artifacts**: `{artifact_root}`",
        f"- **Generated**: {datetime.now(UTC).isoformat()}",
        "",
        "## Reconnaissance",
        "",
        f"- **Languages detected**: {', '.join(recon.get('languages', [])) or 'None'}",
        f"- **Exclusions applied**: {len(recon.get('exclusions', []))} patterns",
        "",
        "## Implementation Map",
        "",
        "| Path | Category |",
        "|------|----------|",
    ]

    for entry in repo_map.get("entries", []):
        lines.append(f"| {entry.get('path', '')} | {entry.get('category', '')} |")

    lines.extend(
        [
            "",
            "## Signals",
            "",
            "| Signal | Value | Evidence |",
            "|--------|-------|----------|",
            f"| Duplication % | {signals.get('duplication_percent', 0):.1f}% | quality-jscpd.json |",
            f"| Coupling score | {signals.get('coupling_score', 0):.2f} | architecture-coupling.json |",
            f"| Change concentration | {signals.get('concentration_ratio', 0):.2f} | history-concentration.json |",
            f"| Lint enforced | {'Yes' if signals.get('lint_enforced') else 'No'} | quality-gates.json |",
            f"| Tests enforced | {'Yes' if signals.get('tests_enforced') else 'No'} | quality-gates.json |",
            f"| CI/local parity | {'OK' if signals.get('ci_local_parity') else 'Gaps'} | quality-gates.json |",
            f"| Doc risk reasons | {len(signals.get('doc_risk_reasons', []))} | docs-risk.json |",
            f"| MCP present | {'Yes' if signals.get('mcp_present') else 'No'} | mcp-scan.json |",
            "",
            "## Quality Gates & Tests",
            "",
            f"- **Hard tests present**: {'Yes' if tests_inv.get('hard_tests_present') else 'No'} (integration/e2e/smoke/system)",
            f"- **Lint enforced in pre-commit + CI**: {'Yes' if quality_gates.get('lint_enforced') else 'No'}",
            f"- **Tests enforced in pre-commit + CI**: {'Yes' if quality_gates.get('tests_enforced') else 'No'}",
            f"- **CI/Local parity**: {'OK' if quality_gates.get('parity_ok') else 'Gaps detected'}",
        ]
    )

    parity_gaps = quality_gates.get("parity_gaps", {})
    if parity_gaps.get("missing_in_ci"):
        lines.append(f"  - Missing in CI: {', '.join(parity_gaps['missing_in_ci'])}")
    if parity_gaps.get("missing_local"):
        lines.append(f"  - Missing locally: {', '.join(parity_gaps['missing_local'])}")

    # KPI Scoring
    obj_score = readiness.get("objective_score", 0)
    lines.extend(
        [
            "",
            "## KPI Scoring",
            "",
            "### Agentic Readiness",
            "",
            "- **Formula**: `S = round(0.7*O + 0.3*A, 1)`",
            f"- **Objective score (O)**: {obj_score:.2f}",
            "- **Anchor (A)**: _requires human judgment_",
            f"- **Readiness indicator**: {_score_indicator(obj_score * 10)}",
            "",
            "### Maintenance Score",
            "",
            f"- **Objective score (O)**: {maintenance.get('objective_score', 0):.2f}",
            f"- **Maintenance indicator**: {_score_indicator(maintenance.get('objective_score', 0) * 10)}",
            "",
            "## Readiness Blockers",
            "",
        ]
    )

    blockers = _collect_blockers(quality_gates, docs_risk_data, mcp_data)
    if blockers:
        for i, blocker in enumerate(blockers, 1):
            lines.append(f"{i}. {blocker}")
    else:
        lines.append("_No blockers identified._")

    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            "- recon.json",
            "- repo-map.json",
            "- quality-jscpd.json",
            "- quality-lizard.json",
            "- architecture-coupling.json",
            "- tests-inventory.json",
            "- quality-gates.json",
            "- docs-risk.json",
            "- mcp-scan.json",
            "- history-concentration.json",
            "- docs-freshness.json",
            "- agentic-readiness.json",
            "- maintenance-score.json",
        ]
    )

    (artifact_root / "report.md").write_text("\n".join(lines) + "\n")


def _score_indicator(score: float) -> str:
    """Return a score indicator based on the 0-10 scale."""
    if score >= 7:
        return f"{score:.1f}/10 (Good)"
    elif score >= 4:
        return f"{score:.1f}/10 (Watch)"
    else:
        return f"{score:.1f}/10 (Risk)"


def _run_analyzer(
    name: str,
    tool_key: str,
    target: Path,
    artifact_root: Path,
    min_severity: str,
    exclude_args: list[str],
) -> int:
    """Run an analyzer via CLI and return exit code."""
    output_file = artifact_root / f"{tool_key.replace(':', '-')}.json"
    command = [
        "uv",
        "run",
        "--directory",
        str(PROJECT_ROOT / "tools" / "enaible"),
        "enaible",
        "analyzers",
        "run",
        tool_key,
        "--target",
        str(target),
        "--min-severity",
        min_severity,
        "--out",
        str(output_file),
        *exclude_args,
    ]
    return run_command_with_timing(
        f"analyzer:{name}",
        command,
        metadata={"tool": tool_key, "target": str(target)},
    )


def _setup_artifact_root(artifact_root: Path | None) -> Path:
    """Set up and return the artifact directory."""
    if artifact_root is None:
        timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        artifact_root = (
            PROJECT_ROOT
            / ".enaible"
            / "artifacts"
            / "analyze-agentic-readiness"
            / timestamp
        )
    artifact_root = artifact_root.resolve()
    artifact_root.mkdir(parents=True, exist_ok=True)
    return artifact_root


def _run_mcp_scan(target: Path, artifact_root: Path) -> None:
    """Run MCP scan phase with timing instrumentation."""
    metadata = {"target": str(target), "artifact_root": str(artifact_root)}
    with log_phase("helper:mcp_scan", metadata):
        matches = mcp_scan.scan_mcp(target)
        (artifact_root / "mcp-scan.json").write_text(
            json.dumps({"matches": matches, "mcp_present": bool(matches)}, indent=2)
        )


def _run_docs_risk_phase(target: Path, artifact_root: Path, errors: list[str]) -> None:
    """Run documentation risk analysis phase."""
    quality_gates_path = artifact_root / "quality-gates.json"
    if not quality_gates_path.exists():
        errors.append("docs_risk: quality-gates.json not found")
        return
    try:
        docs_risk.generate_docs_risk(target, artifact_root, quality_gates_path)
    except Exception as exc:
        errors.append(f"docs_risk: {exc}")


def _run_scoring_phases(artifact_root: Path, target: Path, errors: list[str]) -> None:
    """Run readiness score, maintenance score, and report generation."""
    try:
        readiness_payload = readiness_score.compute_readiness(artifact_root)
        (artifact_root / "agentic-readiness.json").write_text(
            json.dumps(readiness_payload, indent=2)
        )
    except Exception as exc:
        errors.append(f"readiness_score: {exc}")

    try:
        maintenance_payload = maintenance_score.compute_maintenance(artifact_root)
        (artifact_root / "maintenance-score.json").write_text(
            json.dumps(maintenance_payload, indent=2)
        )
    except Exception as exc:
        errors.append(f"maintenance_score: {exc}")

    try:
        _generate_report(artifact_root, target)
    except Exception as exc:
        errors.append(f"report: {exc}")


def run_workflow(
    target: Path,
    artifact_root: Path | None = None,
    days: int = 180,
    min_severity: str = "low",
    excludes: Sequence[str] | None = None,
) -> int:
    """Execute the agentic readiness workflow.

    Args:
        target: Path to the codebase to analyze.
        artifact_root: Optional custom artifact directory. If not provided,
            creates a timestamped directory under .enaible/artifacts/.
        days: History window for concentration and docs freshness.
        min_severity: Minimum severity for analyzer findings.
        excludes: Additional glob patterns to exclude.

    Returns
    -------
        Exit code: 0 on success, 1 on failure.
    """
    target = target.resolve()
    all_excludes = list(DEFAULT_EXCLUDES) + list(excludes or [])
    exclude_args = _build_exclude_args(all_excludes)
    artifact_root = _setup_artifact_root(artifact_root)

    errors: list[str] = []

    # Phase 1: Reconnaissance
    try:
        recon_map.generate_recon(target, artifact_root)
    except Exception as exc:
        errors.append(f"recon: {exc}")

    # Phase 2: Run analyzers
    for name, tool_key in [
        ("jscpd", "quality:jscpd"),
        ("coupling", "architecture:coupling"),
        ("lizard", "quality:lizard"),
    ]:
        exit_code = _run_analyzer(
            name, tool_key, target, artifact_root, min_severity, exclude_args
        )
        if exit_code != 0:
            errors.append(f"analyzer:{name} exited with code {exit_code}")

    # Phase 3: Inventory tests and quality gates
    try:
        inventory_tests_gates.generate_inventory(target, artifact_root)
    except Exception as exc:
        errors.append(f"inventory: {exc}")

    # Phase 4: Documentation risk
    _run_docs_risk_phase(target, artifact_root, errors)

    # Phase 5: MCP scan
    try:
        _run_mcp_scan(target, artifact_root)
    except Exception as exc:
        errors.append(f"mcp_scan: {exc}")

    # Phase 6: History concentration and docs freshness
    try:
        history_docs.generate_history_docs(target, artifact_root, days)
    except Exception as exc:
        errors.append(f"history_docs: {exc}")

    # Phases 7-9: Scoring and report
    _run_scoring_phases(artifact_root, target, errors)

    # Report results
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Workflow completed. Artifacts: {artifact_root}")
    print(f"Report: {artifact_root / 'report.md'}")
    return 0
