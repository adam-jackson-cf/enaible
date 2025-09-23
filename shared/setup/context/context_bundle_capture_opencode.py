#!/usr/bin/env python3
"""Opencode-specific context bundle capture wrapper."""
import sys

from context_capture_base import ContextCapturePaths, ContextCaptureRunner

_OPENCODE_RUNNER = ContextCaptureRunner(
    ContextCapturePaths(
        project_dir_env="OPENCODE_PROJECT_DIR",
        context_dir_name=".opencode",
    )
)


def capture_action(event_type: str) -> None:
    """Entry point for Opencode hook integrations."""
    _OPENCODE_RUNNER.capture_action(event_type)


if __name__ == "__main__" and len(sys.argv) > 1:
    capture_action(sys.argv[1])
