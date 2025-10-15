"""System adapter metadata for prompt rendering."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class SystemRenderContext:
    name: str
    project_scope_dir: str
    user_scope_dir: str
    description: str


SYSTEM_CONTEXTS: Mapping[str, SystemRenderContext] = {
    "claude-code": SystemRenderContext(
        name="claude-code",
        project_scope_dir=".claude",
        user_scope_dir="~/.claude",
        description="Claude Code CLI",
    ),
    "opencode": SystemRenderContext(
        name="opencode",
        project_scope_dir=".opencode",
        user_scope_dir="~/.config/opencode",
        description="OpenCode CLI",
    ),
    "codex": SystemRenderContext(
        name="codex",
        project_scope_dir=".codex",
        user_scope_dir="~/.codex",
        description="Codex CLI",
    ),
}
