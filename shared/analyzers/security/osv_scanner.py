#!/usr/bin/env python3
"""
OSV Scanner Analyzer - Supply chain vulnerability scanning across ecosystems.

Runs osv-scanner with JSON output and maps vulnerabilities into the
standardized finding schema.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from core.base.analyzer_base import AnalyzerConfig, BaseAnalyzer
from core.base.analyzer_registry import register_analyzer


@register_analyzer("security:osv")
class OsvScannerAnalyzer(BaseAnalyzer):
    """Analyze dependencies for known vulnerabilities using osv-scanner."""

    def __init__(self, config: AnalyzerConfig | None = None):
        security_cfg = config or AnalyzerConfig()
        super().__init__("security", security_cfg)

    def get_analyzer_metadata(self) -> dict[str, Any]:
        return {
            "name": "OSV Scanner Analyzer",
            "version": "1.0.0",
            "description": "Supply chain vulnerability scanning via osv-scanner",
            "category": "security",
            "priority": "high",
        }

    def analyze(self, target_path: str | None = None):  # type: ignore[override]
        self.start_analysis()
        analyze_path = target_path or self.config.target_path
        result = self.create_result("analysis")

        target = Path(analyze_path)
        if not target.exists():
            result.set_error(f"Target path not found: {analyze_path}")
            return self.complete_analysis(result)

        if not shutil.which("osv-scanner"):
            result.set_error("osv-scanner is required but not available.")
            return self.complete_analysis(result)

        cmd = [
            "osv-scanner",
            "--format",
            "json",
            "--recursive",
            str(target),
        ]

        try:
            timeout = self.config.timeout_seconds or 600
            completed = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            result.set_error(f"osv-scanner timed out: {exc}")
            return self.complete_analysis(result)

        if completed.returncode not in (0, 1):
            result.set_error(
                f"osv-scanner failed with exit code {completed.returncode}"
            )
            return self.complete_analysis(result)

        try:
            payload = json.loads(completed.stdout or "{}")
        except json.JSONDecodeError as exc:
            result.set_error(f"Failed to parse osv-scanner JSON: {exc}")
            return self.complete_analysis(result)

        findings = self._convert_results(payload)
        files = self.scan_directory(analyze_path)
        self._add_findings_to_result(result, findings)
        self._add_metadata_to_result(result, analyze_path, files, findings)
        return self.complete_analysis(result)

    def analyze_target(self, target_path: str) -> list[dict[str, Any]]:  # type: ignore[override]
        return []

    def _convert_results(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        results = payload.get("results", []) or []
        findings: list[dict[str, Any]] = []

        for result in results:
            source = result.get("source", {}) or {}
            source_path = source.get("path", "unknown")
            packages = result.get("packages", []) or []

            for package_entry in packages:
                pkg = package_entry.get("package", {}) or {}
                pkg_name = pkg.get("name", "unknown")
                pkg_version = pkg.get("version", "")
                vulnerabilities = package_entry.get("vulnerabilities", []) or []

                for vuln in vulnerabilities:
                    vuln_id = vuln.get("id", "OSV")
                    summary = vuln.get("summary") or vuln.get("details") or vuln_id
                    severity = self._severity_from_vuln(vuln)

                    findings.append(
                        {
                            "title": f"OSV: {vuln_id}",
                            "description": summary,
                            "severity": severity,
                            "file_path": source_path,
                            "line_number": 1,
                            "recommendation": "Upgrade to a fixed version of the dependency.",
                            "metadata": {
                                "package": pkg_name,
                                "version": pkg_version,
                                "vulnerability_id": vuln_id,
                                "source": "osv-scanner",
                            },
                        }
                    )

        return findings

    def _severity_from_vuln(self, vuln: dict[str, Any]) -> str:
        severity = self._extract_database_severity(vuln)
        if severity:
            return severity
        return self._extract_score_severity(vuln)

    def _extract_database_severity(self, vuln: dict[str, Any]) -> str | None:
        """Extract severity from database_specific field."""
        database_specific = vuln.get("database_specific", {}) or {}
        severity = database_specific.get("severity")
        if not isinstance(severity, str):
            return None
        severity_map = {
            "CRITICAL": "high",
            "HIGH": "high",
            "MEDIUM": "medium",
            "LOW": "low",
        }
        return severity_map.get(severity.upper())

    def _extract_score_severity(self, vuln: dict[str, Any]) -> str:
        """Extract severity from CVSS score array."""
        scores = self._collect_scores(vuln.get("severity", []) or [])
        if not scores:
            return "medium"
        return self._score_to_severity(max(scores))

    def _collect_scores(self, severity_array: list[Any]) -> list[float]:
        """Safely extract numeric scores from severity array."""
        scores = []
        for entry in severity_array:
            score = entry.get("score") if isinstance(entry, dict) else None
            if score:
                try:
                    scores.append(float(score))
                except (ValueError, TypeError):
                    continue
        return scores

    def _score_to_severity(self, score: float) -> str:
        """Map CVSS score to severity level."""
        if score >= 7.0:
            return "high"
        if score >= 4.0:
            return "medium"
        return "low"


if __name__ == "__main__":
    raise SystemExit(0)
