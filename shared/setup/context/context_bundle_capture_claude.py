#!/usr/bin/env python3
"""Claude-specific context bundle capture wrapper."""
import sys

from context_capture_base import ContextCapturePaths, ContextCaptureRunner

_CLAUDE_RUNNER = ContextCaptureRunner(
    ContextCapturePaths(
        project_dir_env="CLAUDE_PROJECT_DIR",
        context_dir_name=".claude",
    )
)


def capture_action(event_type: str) -> None:
    """Entry point preserved for existing Claude hook integrations."""
    _CLAUDE_RUNNER.capture_action(event_type)


if __name__ == "__main__" and len(sys.argv) > 1:
    capture_action(sys.argv[1])
