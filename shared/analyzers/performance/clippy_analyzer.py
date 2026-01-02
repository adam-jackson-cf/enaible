#!/usr/bin/env python3
"""
Clippy Performance Analyzer - Rust performance hints via cargo clippy.

Runs `cargo clippy --message-format=json` and maps clippy::perf findings
into the standardized finding schema.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from core.base.analyzer_base import AnalyzerConfig, BaseAnalyzer
from core.base.analyzer_registry import register_analyzer


@register_analyzer("performance:clippy")
class ClippyPerformanceAnalyzer(BaseAnalyzer):
    """Analyze Rust code with Clippy performance lints."""

    def __init__(self, config: AnalyzerConfig | None = None):
        perf_cfg = config or AnalyzerConfig(code_extensions={".rs"})
        super().__init__("performance", perf_cfg)

    def get_analyzer_metadata(self) -> dict[str, Any]:
        return {
            "name": "Clippy Performance Analyzer",
            "version": "1.0.0",
            "description": "Rust performance analysis via Clippy",
            "category": "performance",
            "priority": "medium",
        }

    def analyze(self, target_path: str | None = None):  # type: ignore[override]
        self.start_analysis()
        analyze_path = target_path or self.config.target_path
        result = self.create_result("analysis")

        if not Path(analyze_path).exists():
            result.set_error(f"Target path not found: {analyze_path}")
            return self.complete_analysis(result)

        if not shutil.which("cargo"):
            result.set_error(
                "cargo is required but not available. Install Rust toolchain."
            )
            return self.complete_analysis(result)

        cargo_root = self._find_cargo_root(Path(analyze_path))
        if cargo_root is None:
            result.set_error("Cargo.toml not found for target path.")
            return self.complete_analysis(result)

        cmd = [
            "cargo",
            "clippy",
            "--message-format=json",
        ]

        try:
            timeout = self.config.timeout_seconds or 900
            completed = subprocess.run(
                cmd,
                cwd=cargo_root,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            result.set_error(f"cargo clippy timed out: {exc}")
            return self.complete_analysis(result)

        if completed.returncode not in (0, 1):
            result.set_error(
                f"cargo clippy failed with exit code {completed.returncode}"
            )
            return self.complete_analysis(result)

        findings = self._parse_clippy_output(completed.stdout)
        files = self.scan_directory(analyze_path)
        self._add_findings_to_result(result, findings)
        self._add_metadata_to_result(result, analyze_path, files, findings)
        return self.complete_analysis(result)

    def analyze_target(self, target_path: str) -> list[dict[str, Any]]:  # type: ignore[override]
        return []

    def _find_cargo_root(self, target: Path) -> Path | None:
        if target.is_file():
            target = target.parent

        for directory in [target, *target.parents]:
            if (directory / "Cargo.toml").is_file():
                return directory
        return None

    def _parse_clippy_output(self, output: str) -> list[dict[str, Any]]:
        findings: list[dict[str, Any]] = []
        for line in output.splitlines():
            line = line.strip()
            if not line:
                continue

            try:
                message = json.loads(line)
            except json.JSONDecodeError:
                continue

            if message.get("reason") != "compiler-message":
                continue

            diagnostic = message.get("message", {}) or {}
            code_info = diagnostic.get("code") or {}
            lint_code = code_info.get("code", "")
            if not lint_code.startswith("clippy::"):
                continue

            level = diagnostic.get("level", "warning")
            severity = {"error": "high", "warning": "medium", "note": "low"}.get(
                level, "low"
            )

            span = self._select_primary_span(diagnostic.get("spans", []) or [])
            file_path = span.get("file_name", "unknown")
            line_number = int(span.get("line_start", 1))
            message_text = diagnostic.get("message", lint_code)

            findings.append(
                {
                    "title": f"Clippy: {lint_code}",
                    "description": message_text,
                    "severity": severity,
                    "file_path": file_path,
                    "line_number": line_number,
                    "recommendation": "Address the Clippy performance lint.",
                    "metadata": {"lint": lint_code, "source": "clippy"},
                }
            )

        return findings

    def _select_primary_span(self, spans: list[dict[str, Any]]) -> dict[str, Any]:
        for span in spans:
            if span.get("is_primary"):
                return span
        return spans[0] if spans else {}


if __name__ == "__main__":
    raise SystemExit(0)
