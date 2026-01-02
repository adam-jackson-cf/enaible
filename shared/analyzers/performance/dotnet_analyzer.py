#!/usr/bin/env python3
"""
Dotnet Performance Analyzer - C# performance hints via dotnet build analyzers.

Runs `dotnet build` with analyzers enabled and maps performance-related
CA rules into the standardized finding schema.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from core.base.analyzer_base import AnalyzerConfig, BaseAnalyzer
from core.base.analyzer_registry import register_analyzer

_PERF_CA_CODES = {
    "CA1806",
    "CA1810",
    "CA1812",
    "CA1822",
    "CA1823",
    "CA1824",
    "CA1825",
    "CA1826",
    "CA1827",
    "CA1828",
    "CA1830",
    "CA1841",
    "CA1845",
    "CA1851",
    "CA1852",
    "CA1859",
}

_WARNING_PATTERN = re.compile(
    r"^(?P<file>[^()]+)\((?P<line>\d+),(?P<col>\d+)\):\s+"
    r"(?P<level>warning|error)\s+(?P<code>CA\d+):\s+(?P<message>.+?)\s+\[(?P<project>.+)\]$"
)


@register_analyzer("performance:dotnet")
class DotnetPerformanceAnalyzer(BaseAnalyzer):
    """Analyze C# code with dotnet build analyzers for performance issues."""

    def __init__(self, config: AnalyzerConfig | None = None):
        perf_cfg = config or AnalyzerConfig(code_extensions={".cs"})
        super().__init__("performance", perf_cfg)

    def get_analyzer_metadata(self) -> dict[str, Any]:
        return {
            "name": "Dotnet Performance Analyzer",
            "version": "1.0.0",
            "description": "C# performance analysis via dotnet build analyzers",
            "category": "performance",
            "priority": "medium",
            "rules": sorted(_PERF_CA_CODES),
        }

    def analyze(self, target_path: str | None = None):  # type: ignore[override]
        self.start_analysis()
        analyze_path = target_path or self.config.target_path
        result = self.create_result("analysis")

        target = Path(analyze_path)
        if not target.exists():
            result.set_error(f"Target path not found: {analyze_path}")
            return self.complete_analysis(result)

        if not shutil.which("dotnet"):
            result.set_error("dotnet CLI is required but not available.")
            return self.complete_analysis(result)

        project_or_solution = self._resolve_dotnet_target(target)
        if project_or_solution is None:
            result.set_error("No .sln or .csproj found for target path.")
            return self.complete_analysis(result)

        cmd = [
            "dotnet",
            "build",
            str(project_or_solution),
            "/p:RunAnalyzers=true",
            "/p:EnforceCodeStyleInBuild=true",
        ]

        try:
            timeout = self.config.timeout_seconds or 900
            completed = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            result.set_error(f"dotnet build timed out: {exc}")
            return self.complete_analysis(result)

        if completed.returncode != 0:
            result.set_error(
                f"dotnet build failed with exit code {completed.returncode}"
            )
            return self.complete_analysis(result)

        output = "\n".join([completed.stdout or "", completed.stderr or ""])
        findings = self._parse_build_output(output, project_or_solution)
        files = self.scan_directory(analyze_path)
        self._add_findings_to_result(result, findings)
        self._add_metadata_to_result(result, analyze_path, files, findings)
        return self.complete_analysis(result)

    def analyze_target(self, target_path: str) -> list[dict[str, Any]]:  # type: ignore[override]
        return []

    def _resolve_dotnet_target(self, target: Path) -> Path | None:
        if target.is_file() and target.suffix in {".sln", ".csproj"}:
            return target

        root = target if target.is_dir() else target.parent
        solutions = sorted(root.glob("*.sln"))
        if solutions:
            return solutions[0]

        projects = sorted(root.glob("*.csproj"))
        if projects:
            return projects[0]

        solutions = sorted(root.rglob("*.sln"))
        if solutions:
            return solutions[0]

        projects = sorted(root.rglob("*.csproj"))
        if projects:
            return projects[0]

        return None

    def _parse_build_output(
        self, output: str, fallback_path: Path
    ) -> list[dict[str, Any]]:
        findings: list[dict[str, Any]] = []

        for line in output.splitlines():
            match = _WARNING_PATTERN.match(line.strip())
            if not match:
                continue

            code = match.group("code")
            if code not in _PERF_CA_CODES:
                continue

            level = match.group("level")
            severity = "high" if level == "error" else "medium"
            file_path = match.group("file")
            line_number = int(match.group("line"))
            message = match.group("message")

            findings.append(
                {
                    "title": f"Dotnet Analyzer: {code}",
                    "description": message,
                    "severity": severity,
                    "file_path": file_path or str(fallback_path),
                    "line_number": line_number,
                    "recommendation": "Address the analyzer warning to improve performance.",
                    "metadata": {"rule": code, "source": "dotnet"},
                }
            )

        return findings


if __name__ == "__main__":
    raise SystemExit(0)
