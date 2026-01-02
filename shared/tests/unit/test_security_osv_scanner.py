#!/usr/bin/env python3
"""Unit tests for OSV scanner analyzer parsing."""

from analyzers.security.osv_scanner import OsvScannerAnalyzer


def test_convert_results_creates_findings():
    analyzer = OsvScannerAnalyzer()
    payload = {
        "results": [
            {
                "source": {"path": "package-lock.json", "type": "npm"},
                "packages": [
                    {
                        "package": {"name": "lodash", "version": "4.17.20"},
                        "vulnerabilities": [
                            {
                                "id": "GHSA-xxxx",
                                "summary": "Prototype pollution",
                                "severity": [{"score": "7.5", "type": "CVSS_V3"}],
                            }
                        ],
                    }
                ],
            }
        ]
    }

    findings = analyzer._convert_results(payload)

    assert len(findings) == 1
    assert findings[0]["severity"] == "high"
    assert findings[0]["file_path"] == "package-lock.json"
