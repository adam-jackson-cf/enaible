#!/usr/bin/env python3
"""
GolangCI-Lint Performance Analyzer - Go performance and correctness heuristics.

Runs golangci-lint with a focused linter set and maps JSON output into
our standardized finding schema.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from core.base.analyzer_base import AnalyzerConfig, BaseAnalyzer
from core.base.analyzer_registry import register_analyzer


@register_analyzer("performance:golangci-lint")
class GolangCILintAnalyzer(BaseAnalyzer):
    """Analyze Go code with golangci-lint and surface performance findings."""

    def __init__(
        self,
        config: AnalyzerConfig | None = None,
        *,
        enabled_linters: list[str] | None = None,
    ):
        perf_cfg = config or AnalyzerConfig(code_extensions={".go"})
        super().__init__("performance", perf_cfg)
        self.enabled_linters = enabled_linters or [
            "gocritic",
            "gosimple",
            "staticcheck",
            "prealloc",
        ]

        self._linter_severity = {
            "staticcheck": "high",
            "gocritic": "medium",
            "gosimple": "low",
            "prealloc": "medium",
        }

    def get_analyzer_metadata(self) -> dict[str, Any]:
        return {
            "name": "GolangCI-Lint Performance Analyzer",
            "version": "1.0.0",
            "description": "Go performance analysis via golangci-lint",
            "category": "performance",
            "priority": "medium",
            "linters": self.enabled_linters,
        }

    def analyze(self, target_path: str | None = None):  # type: ignore[override]
        self.start_analysis()
        analyze_path = target_path or self.config.target_path
        result = self.create_result("analysis")

        if not Path(analyze_path).exists():
            result.set_error(f"Target path not found: {analyze_path}")
            return self.complete_analysis(result)

        if not shutil.which("golangci-lint"):
            result.set_error(
                "golangci-lint is required but not available. Install from https://golangci-lint.run/usage/install/"
            )
            return self.complete_analysis(result)

        cmd = [
            "golangci-lint",
            "run",
            "--out-format",
            "json",
            "--disable-all",
            *[f"--enable={linter}" for linter in self.enabled_linters],
            analyze_path,
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
            result.set_error(f"golangci-lint timed out: {exc}")
            return self.complete_analysis(result)

        if completed.returncode not in (0, 1):
            result.set_error(
                f"golangci-lint failed with exit code {completed.returncode}"
            )
            return self.complete_analysis(result)

        try:
            payload = json.loads(completed.stdout or "{}")
        except json.JSONDecodeError as exc:
            result.set_error(f"Failed to parse golangci-lint JSON: {exc}")
            return self.complete_analysis(result)

        findings = self._convert_issues(payload)
        files = self.scan_directory(analyze_path)
        self._add_findings_to_result(result, findings)
        self._add_metadata_to_result(result, analyze_path, files, findings)
        return self.complete_analysis(result)

    def analyze_target(self, target_path: str) -> list[dict[str, Any]]:  # type: ignore[override]
        return []

    def _convert_issues(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        issues = payload.get("Issues", []) or []
        findings: list[dict[str, Any]] = []

        for issue in issues:
            linter = issue.get("FromLinter", "golangci-lint")
            pos = issue.get("Pos", {}) or {}
            file_path = pos.get("Filename", "unknown")
            line = int(pos.get("Line", 1))
            text = issue.get("Text", linter)
            severity = self._linter_severity.get(linter, "low")

            findings.append(
                {
                    "title": f"GolangCI-Lint: {linter}",
                    "description": text,
                    "severity": severity,
                    "file_path": file_path,
                    "line_number": line,
                    "recommendation": "Address the lint finding to improve performance or simplicity.",
                    "metadata": {"linter": linter, "source": "golangci-lint"},
                }
            )

        return findings


if __name__ == "__main__":
    raise SystemExit(0)
