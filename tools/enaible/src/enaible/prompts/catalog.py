"""Prompt catalog metadata for Enaible render pipeline."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class SystemPromptConfig:
    template: str
    output_path: Path
    frontmatter: Mapping[str, str] = field(default_factory=dict)
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class PromptDefinition:
    prompt_id: str
    source_path: Path
    title: str
    systems: Mapping[str, SystemPromptConfig]


def _repo_path(*parts: str) -> Path:
    return Path(*parts)


CATALOG: dict[str, PromptDefinition] = {
    "analyze-security": PromptDefinition(
        prompt_id="analyze-security",
        source_path=_repo_path("shared", "prompts", "analyze-security.md"),
        title="analyze-security v1.0",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    "systems", "claude-code", "commands", "analyze-security.md"
                ),
                frontmatter={"argument-hint": "[target-path] [--verbose]"},
            ),
            "opencode": SystemPromptConfig(
                template="docs/system/opencode/templates/command.md.j2",
                output_path=_repo_path(
                    "systems", "opencode", "command", "analyze-security.md"
                ),
                frontmatter={
                    "description": "Perform a security audit of the repository and dependencies",
                    "agent": "security",
                },
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "codex", "prompts", "analyze-security.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
        },
    ),
    "analyze-architecture": PromptDefinition(
        prompt_id="analyze-architecture",
        source_path=_repo_path("shared", "prompts", "analyze-architecture.md"),
        title="analyze-architecture v1.0",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    "systems", "claude-code", "commands", "analyze-architecture.md"
                ),
                frontmatter={"argument-hint": "[target-path]"},
            ),
            "opencode": SystemPromptConfig(
                template="docs/system/opencode/templates/command.md.j2",
                output_path=_repo_path(
                    "systems", "opencode", "command", "analyze-architecture.md"
                ),
                frontmatter={
                    "description": "Evaluate system architecture for scalability, maintainability, and best practices"
                },
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "codex", "prompts", "analyze-architecture.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
        },
    ),
    "analyze-code-quality": PromptDefinition(
        prompt_id="analyze-code-quality",
        source_path=_repo_path("shared", "prompts", "analyze-code-quality.md"),
        title="analyze-code-quality v1.0",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    "systems", "claude-code", "commands", "analyze-code-quality.md"
                ),
                frontmatter={"argument-hint": "[target-path]"},
            ),
            "opencode": SystemPromptConfig(
                template="docs/system/opencode/templates/command.md.j2",
                output_path=_repo_path(
                    "systems", "opencode", "command", "analyze-code-quality.md"
                ),
                frontmatter={
                    "description": "Assess code quality and complexity, and highlight high‑value refactors"
                },
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "codex", "prompts", "analyze-code-quality.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
        },
    ),
    "analyze-performance": PromptDefinition(
        prompt_id="analyze-performance",
        source_path=_repo_path("shared", "prompts", "analyze-performance.md"),
        title="analyze-performance v1.0",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    "systems", "claude-code", "commands", "analyze-performance.md"
                ),
                frontmatter={"argument-hint": "[target-path]"},
            ),
            "opencode": SystemPromptConfig(
                template="docs/system/opencode/templates/command.md.j2",
                output_path=_repo_path(
                    "systems", "opencode", "command", "analyze-performance.md"
                ),
                frontmatter={
                    "description": "Identify performance bottlenecks and propose minimal, high‑impact optimizations"
                },
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "codex", "prompts", "analyze-performance.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
        },
    ),
    "analyze-root-cause": PromptDefinition(
        prompt_id="analyze-root-cause",
        source_path=_repo_path("shared", "prompts", "analyze-root-cause.md"),
        title="analyze-root-cause v1.0",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    "systems", "claude-code", "commands", "analyze-root-cause.md"
                ),
                frontmatter={"argument-hint": "[issue-description]"},
            ),
            "opencode": SystemPromptConfig(
                template="docs/system/opencode/templates/command.md.j2",
                output_path=_repo_path(
                    "systems", "opencode", "command", "analyze-root-cause.md"
                ),
                frontmatter={
                    "description": "Perform root cause analysis for a defect or failure"
                },
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "codex", "prompts", "analyze-root-cause.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
        },
    ),
    "plan-refactor": PromptDefinition(
        prompt_id="plan-refactor",
        source_path=_repo_path("shared", "prompts", "plan-improvements.md"),
        title="plan-refactor v1.0",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    "systems", "claude-code", "commands", "plan-refactor.md"
                ),
                frontmatter={"argument-hint": "<refactor-scope-or-area>"},
            ),
            "opencode": SystemPromptConfig(
                template="docs/system/opencode/templates/command.md.j2",
                output_path=_repo_path(
                    "systems", "opencode", "command", "plan-refactor.md"
                ),
                frontmatter={
                    "description": "Plan a minimal, high‑impact refactor with clear boundaries and tests"
                },
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "codex", "prompts", "plan-refactor.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
        },
    ),
    "plan-solution": PromptDefinition(
        prompt_id="plan-solution",
        source_path=_repo_path("shared", "prompts", "plan-solution.md"),
        title="plan-solution v1.0",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    "systems", "claude-code", "commands", "plan-solution.md"
                ),
                frontmatter={"argument-hint": "<technical-challenge> [--critique]"},
            ),
            "opencode": SystemPromptConfig(
                template="docs/system/opencode/templates/command.md.j2",
                output_path=_repo_path(
                    "systems", "opencode", "command", "plan-solution.md"
                ),
                frontmatter={
                    "description": "Develop a solution plan for a technical challenge with constraints and milestones"
                },
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "codex", "prompts", "plan-solution.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
        },
    ),
    "get-codebase-primer": PromptDefinition(
        prompt_id="get-codebase-primer",
        source_path=_repo_path("shared", "prompts", "get-codebase-primer.md"),
        title="get-codebase-primer v1.0",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    "systems", "claude-code", "commands", "get-codebase-primer.md"
                ),
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "codex", "prompts", "get-codebase-primer.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
        },
    ),
}


def list_prompts() -> Iterable[PromptDefinition]:
    return CATALOG.values()
