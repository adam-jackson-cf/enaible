#!/usr/bin/env python3
"""Opencode-specific context bundle capture wrapper."""
import json
import sys
from typing import Any

from context_capture_base import ContextCapturePaths, ContextCaptureRunner

_OPENCODE_RUNNER = ContextCaptureRunner(
    ContextCapturePaths(
        project_dir_env="OPENCODE_PROJECT_DIR",
        context_dir_name=".opencode",
    )
)


def transform_hook_payload(event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Transform Opencode hook payload to format expected by base class."""
    transformed = {"session_id": payload.get("session_id")}

    if event_type == "post-tool":
        transformed.update(
            {
                "tool_name": payload.get("tool"),
                "tool_input": payload.get("tool_input", {}),
            }
        )
    elif event_type == "user-prompt":
        transformed.update(
            {
                "prompt": payload.get("prompt", ""),
            }
        )
    elif event_type == "session-start":
        transformed.update(
            {
                "source": payload.get("source", "opencode"),
            }
        )

    return transformed


def capture_action(event_type: str) -> None:
    """Entry point for Opencode hook integrations."""
    try:
        # Read payload from stdin
        payload = json.load(sys.stdin)

        # Transform payload for base class
        transformed_payload = transform_hook_payload(event_type, payload)

        # Capture using base class
        _OPENCODE_RUNNER.capture_action(event_type, transformed_payload)
    except (json.JSONDecodeError, KeyError):
        # If payload is invalid, try with empty payload
        _OPENCODE_RUNNER.capture_action(event_type, {})


if __name__ == "__main__" and len(sys.argv) > 1:
    capture_action(sys.argv[1])
