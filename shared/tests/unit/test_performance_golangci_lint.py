#!/usr/bin/env python3
"""Unit tests for GolangCI-Lint performance analyzer parsing."""

from analyzers.performance.golangci_lint_analyzer import GolangCILintAnalyzer


def test_convert_issues_maps_severity():
    analyzer = GolangCILintAnalyzer()
    payload = {
        "Issues": [
            {
                "FromLinter": "staticcheck",
                "Pos": {"Filename": "main.go", "Line": 12},
                "Text": "should use strings.Builder",
            }
        ]
    }

    findings = analyzer._convert_issues(payload)

    assert len(findings) == 1
    assert findings[0]["severity"] == "high"
    assert findings[0]["file_path"] == "main.go"
