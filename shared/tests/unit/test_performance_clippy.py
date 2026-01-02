#!/usr/bin/env python3
"""Unit tests for Clippy performance analyzer parsing."""

import json

from analyzers.performance.clippy_analyzer import ClippyPerformanceAnalyzer


def test_parse_clippy_output_returns_findings():
    analyzer = ClippyPerformanceAnalyzer()

    message = {
        "reason": "compiler-message",
        "message": {
            "code": {"code": "clippy::unnecessary_sort_by"},
            "level": "warning",
            "message": "unnecessary sort by",
            "spans": [{"file_name": "src/lib.rs", "line_start": 8, "is_primary": True}],
        },
    }

    output = json.dumps(message)
    findings = analyzer._parse_clippy_output(output)

    assert len(findings) == 1
    assert findings[0]["file_path"] == "src/lib.rs"
    assert findings[0]["severity"] == "medium"
