#!/usr/bin/env python3
"""
JSCPD Duplication Analyzer - Universal copy/paste detection via jscpd.

Runs the Node-based `jscpd` CLI through npx (or a locally vendored binary)
and maps its JSON report into our standardized finding schema.

Base profile dependency: Node + ESLint workspace now also hosts jscpd.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from core.base.analyzer_base import AnalyzerConfig, BaseAnalyzer
from core.base.analyzer_registry import register_analyzer


def _find_jscpd_binary(install_dir: Path | None = None) -> str | None:
    """Return a path or command that can execute jscpd.

    Preference order:
    1) Local vendored binary in <install_dir>/node_modules/.bin/jscpd
    2) Global npx jscpd
    3) Direct `jscpd` on PATH
    """
    if install_dir:
        candidate = (
            install_dir
            / "node_modules"
            / ".bin"
            / ("jscpd.cmd" if os.name == "nt" else "jscpd")
        )
        if candidate.exists():
            return str(candidate)

    if shutil.which("jscpd"):
        return "jscpd"

    # Prefer npx invocation if available
    if shutil.which("npx"):
        return "npx jscpd"

    return None


@register_analyzer("quality:jscpd")
class JSCPDAnalyzer(BaseAnalyzer):
    """Analyzer that shells out to jscpd and converts results to findings."""

    def __init__(
        self,
        config: AnalyzerConfig | None = None,
        *,
        min_tokens: int = 60,
        mode: str = "mild",
    ):
        super().__init__("quality", config)
        self.min_tokens = min_tokens
        self.mode = mode

        # Optionally let callers hint a local node tools directory
        self.node_tools_dir = Path(
            os.environ.get("AAW_NODE_TOOLS_DIR", "")
            or Path.cwd() / ".claude" / "eslint"
        )

    def get_analyzer_metadata(self) -> dict[str, Any]:
        return {
            "name": "JSCPD Duplication Analyzer",
            "version": "1.0.0",
            "description": "Universal copy/paste detection using jscpd",
            "category": "quality",
            "priority": "medium",
            "jscpd_min_tokens": self.min_tokens,
            "jscpd_mode": self.mode,
        }

    def analyze(self, target_path: str | None = None):  # type: ignore[override]
        self.start_analysis()
        analyze_path = target_path or self.config.target_path
        result = self.create_result("analysis")

        if not Path(analyze_path).exists():
            result.set_error(f"Target path not found: {analyze_path}")
            return self.complete_analysis(result)

        jscpd_bin = _find_jscpd_binary(
            self.node_tools_dir if self.node_tools_dir.exists() else None
        )
        if not jscpd_bin:
            result.set_error(
                "jscpd is not available. Ensure Node is installed and ESLint workspace set up, or run: \n"
                "  npm install -g jscpd\n"
            )
            return self.complete_analysis(result)

        with tempfile.TemporaryDirectory(prefix="jscpd-") as tmp:
            output_dir = Path(tmp)
            report_path = output_dir / "jscpd-report.json"
            cmd = (
                f"{jscpd_bin} --reporters json --output {output_dir} --min-tokens {self.min_tokens} "
                f"--mode {self.mode} --gitignore {analyze_path}"
            )

            try:
                p = subprocess.run(
                    cmd, shell=True, capture_output=True, text=True, timeout=300
                )
            except subprocess.TimeoutExpired as e:
                result.set_error(f"jscpd timed out: {e}")
                return self.complete_analysis(result)

            # jscpd exits with non-zero when duplicates exceed threshold; we still want the report
            if not report_path.exists():
                stderr = (p.stderr or "").strip()
                stdout = (p.stdout or "").strip()
                result.set_error(
                    f"jscpd did not produce a report. stdout={stdout[:2000]} stderr={stderr[:2000]}"
                )
                return self.complete_analysis(result)

            try:
                data = json.loads(report_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                result.set_error(f"Failed to parse jscpd JSON report: {e}")
                return self.complete_analysis(result)

            findings = self._convert_jscpd_to_findings(data)
            files = self.scan_directory(analyze_path)
            self._add_findings_to_result(result, findings)
            self._add_metadata_to_result(result, analyze_path, files, findings)
            return self.complete_analysis(result)

    # BaseAnalyzer contract (unused: jscpd runs once for the whole target)
    def analyze_target(self, target_path: str) -> list[dict[str, Any]]:  # type: ignore[override]
        return []

    def _convert_jscpd_to_findings(self, data: dict[str, Any]) -> list[dict[str, Any]]:
        findings: list[dict[str, Any]] = []
        duplicates = data.get("duplicates", []) or []
        for dup in duplicates:
            fragment_a = dup.get("firstFile", {})
            fragment_b = dup.get("secondFile", {})
            tokens = dup.get("tokens", 0)
            format_name = dup.get("format", "unknown")

            a_path = fragment_a.get("name") or fragment_a.get("file") or "unknown"
            b_path = fragment_b.get("name") or fragment_b.get("file") or "unknown"
            a_start = int(fragment_a.get("start", 1))
            b_start = int(fragment_b.get("start", 1))

            title = "Duplicate Code Block"
            description = f"Code block duplicated between {a_path}:{a_start} and {b_path}:{b_start}"
            recommendation = "Consider extracting shared logic into a function/module to remove duplication."
            meta = {
                "tokens": tokens,
                "format": format_name,
                "match": {"a": a_path, "b": b_path},
            }

            findings.append(
                {
                    "title": title,
                    "description": description,
                    "severity": "low",
                    "file_path": a_path,
                    "line_number": a_start,
                    "recommendation": recommendation,
                    "metadata": meta,
                }
            )
            findings.append(
                {
                    "title": title,
                    "description": description,
                    "severity": "low",
                    "file_path": b_path,
                    "line_number": b_start,
                    "recommendation": recommendation,
                    "metadata": meta,
                }
            )
        return findings
