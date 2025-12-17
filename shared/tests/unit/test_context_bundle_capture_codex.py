#!/usr/bin/env python3

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from context.context_bundle_capture_codex import (
    DEFAULT_CONFIG,
    SessionRecord,
    _build_session_summaries,
    _filter_session_records,
)


def _operation(
    session_id: str, operation: str, timestamp: str = "2025-01-01T00:00:00Z"
):
    return {"session_id": session_id, "operation": operation, "timestamp": timestamp}


def test_filter_session_records_respects_project_root(tmp_path: Path) -> None:
    project = tmp_path / "repo"
    project.mkdir()
    elsewhere = tmp_path / "other"
    elsewhere.mkdir()

    records = [
        SessionRecord("sid-1", str(project), [_operation("sid-1", "bash")]),
        SessionRecord("sid-2", str(elsewhere), [_operation("sid-2", "bash")]),
    ]

    filtered = _filter_session_records(records, project, include_all_projects=False)
    assert [record.session_id for record in filtered] == ["sid-1"]

    include_all = _filter_session_records(records, project, include_all_projects=True)
    assert [record.session_id for record in include_all] == ["sid-1", "sid-2"]


def test_build_session_summaries_groups_counts(tmp_path: Path) -> None:
    project = tmp_path / "repo"
    project.mkdir()
    records = [
        SessionRecord(
            "sid-1",
            str(project),
            [
                _operation("sid-1", "bash"),
                _operation("sid-1", "tool_output"),
            ],
        ),
        # Duplicate session id to confirm deduplication
        SessionRecord(
            "sid-1", str(project), [_operation("sid-1", "assistant_message")]
        ),
        SessionRecord(
            "sid-2", str(tmp_path / "elsewhere"), [_operation("sid-2", "bash")]
        ),
    ]
    prompts = [
        {
            "session_id": "sid-1",
            "timestamp": "2025-01-01T00:05:00Z",
            "text": "Investigate auth bug",
        }
    ]

    summaries = _build_session_summaries(
        records,
        prompts,
        deepcopy(DEFAULT_CONFIG),
        project,
        include_all_projects=False,
    )

    assert len(summaries) == 1
    summary = summaries[0]
    assert summary["id"] == "sid-1"
    assert summary["counts"]["operations"] == 3
    assert summary["counts"]["assistant_message"] == 1
    assert summary["counts"]["bash"] == 1
    assert summary["counts"]["tool_output"] == 1
    assert summary["user_messages"][0]["text"].startswith("Investigate auth bug")
