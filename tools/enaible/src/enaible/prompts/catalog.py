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
                    ".build",
                    "rendered",
                    "claude-code",
                    "commands",
                    "analyze-security.md",
                ),
                frontmatter={"argument-hint": "[target-path] [--verbose]"},
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "codex", "prompts", "analyze-security.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "copilot",
                    "prompts",
                    "analyze-security.prompt.md",
                ),
                frontmatter={
                    "description": "Perform a comprehensive security audit of the repository and dependencies",
                    "mode": "agent",
                    "tools": ["edit", "githubRepo", "search/codebase", "terminal"],
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/command.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "cursor", "commands", "analyze-security.md"
                ),
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
                    ".build",
                    "rendered",
                    "claude-code",
                    "commands",
                    "analyze-architecture.md",
                ),
                frontmatter={"argument-hint": "[target-path]"},
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "codex", "prompts", "analyze-architecture.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "copilot",
                    "prompts",
                    "analyze-architecture.prompt.md",
                ),
                frontmatter={
                    "description": "Evaluate system architecture for scalability, maintainability, and best practices",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase"],
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/command.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "cursor",
                    "commands",
                    "analyze-architecture.md",
                ),
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
                    ".build",
                    "rendered",
                    "claude-code",
                    "commands",
                    "analyze-code-quality.md",
                ),
                frontmatter={"argument-hint": "[target-path]"},
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "codex", "prompts", "analyze-code-quality.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "copilot",
                    "prompts",
                    "analyze-code-quality.prompt.md",
                ),
                frontmatter={
                    "description": "Assess code quality and complexity, and highlight high-value refactors",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase", "terminal"],
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/command.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "cursor",
                    "commands",
                    "analyze-code-quality.md",
                ),
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
                    ".build",
                    "rendered",
                    "claude-code",
                    "commands",
                    "analyze-performance.md",
                ),
                frontmatter={"argument-hint": "[target-path]"},
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "codex", "prompts", "analyze-performance.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "copilot",
                    "prompts",
                    "analyze-performance.prompt.md",
                ),
                frontmatter={
                    "description": "Identify performance bottlenecks and propose minimal, high-impact optimizations",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase", "terminal"],
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/command.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "cursor", "commands", "analyze-performance.md"
                ),
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
                    ".build",
                    "rendered",
                    "claude-code",
                    "commands",
                    "analyze-root-cause.md",
                ),
                frontmatter={"argument-hint": "[issue-description]"},
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "codex", "prompts", "analyze-root-cause.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "copilot",
                    "prompts",
                    "analyze-root-cause.prompt.md",
                ),
                frontmatter={
                    "description": "Perform root cause analysis for a defect or failure",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase"],
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/command.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "cursor", "commands", "analyze-root-cause.md"
                ),
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
                    ".build", "rendered", "claude-code", "commands", "plan-refactor.md"
                ),
                frontmatter={"argument-hint": "<refactor-scope-or-area>"},
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "codex", "prompts", "plan-refactor.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "copilot",
                    "prompts",
                    "plan-refactor.prompt.md",
                ),
                frontmatter={
                    "description": "Plan a minimal, high-impact refactor with clear boundaries and tests",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase"],
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/command.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "cursor", "commands", "plan-refactor.md"
                ),
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
                    ".build", "rendered", "claude-code", "commands", "plan-solution.md"
                ),
                frontmatter={"argument-hint": "<technical-challenge> [--critique]"},
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "codex", "prompts", "plan-solution.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "copilot",
                    "prompts",
                    "plan-solution.prompt.md",
                ),
                frontmatter={
                    "description": "Develop a solution plan for a technical challenge with constraints and milestones",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase"],
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/command.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "cursor", "commands", "plan-solution.md"
                ),
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
                    ".build",
                    "rendered",
                    "claude-code",
                    "commands",
                    "get-codebase-primer.md",
                ),
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "codex", "prompts", "get-codebase-primer.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "copilot",
                    "prompts",
                    "get-codebase-primer.prompt.md",
                ),
                frontmatter={
                    "description": "Generate a comprehensive primer for understanding the codebase",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase"],
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/command.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "cursor", "commands", "get-codebase-primer.md"
                ),
            ),
        },
    ),
    "setup-code-precommit-checks": PromptDefinition(
        prompt_id="setup-code-precommit-checks",
        source_path=_repo_path("shared", "prompts", "setup-code-precommit-checks.md"),
        title="setup-code-precommit-checks v1.0",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "claude-code",
                    "commands",
                    "setup-code-precommit-checks.md",
                ),
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "codex",
                    "prompts",
                    "setup-code-precommit-checks.md",
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "copilot",
                    "prompts",
                    "setup-code-precommit-checks.prompt.md",
                ),
                frontmatter={
                    "description": "Set up language-appropriate pre-commit hooks for the repo",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase", "terminal"],
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/command.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "cursor",
                    "commands",
                    "setup-code-precommit-checks.md",
                ),
            ),
        },
    ),
    "apply-rule-set": PromptDefinition(
        prompt_id="apply-rule-set",
        source_path=_repo_path("shared", "prompts", "apply-rule-set.md"),
        title="apply-rule-set v1.0",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "claude-code", "commands", "apply-rule-set.md"
                ),
                frontmatter={"argument-hint": "<ruleset-name>"},
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "codex", "prompts", "apply-rule-set.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "copilot",
                    "prompts",
                    "apply-rule-set.prompt.md",
                ),
                frontmatter={
                    "description": "Load a named rule set and apply its guidance to the session",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase"],
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/command.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "cursor", "commands", "apply-rule-set.md"
                ),
            ),
        },
    ),
    "setup-project": PromptDefinition(
        prompt_id="setup-project",
        source_path=_repo_path("shared", "prompts", "setup-project.md"),
        title="setup-project v1.0",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "claude-code", "commands", "setup-project.md"
                ),
                frontmatter={"argument-hint": "<project-name> [--from-plan <file>]"},
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "codex", "prompts", "setup-project.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "copilot",
                    "prompts",
                    "setup-project.prompt.md",
                ),
                frontmatter={
                    "description": "Scaffold a new project with Better-T-Stack CLI",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase", "terminal"],
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/command.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "cursor", "commands", "setup-project.md"
                ),
            ),
        },
    ),
    "create-rule": PromptDefinition(
        prompt_id="create-rule",
        source_path=_repo_path("shared", "prompts", "create-rule.md"),
        title="create-rule v1.0",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "claude-code", "commands", "create-rule.md"
                ),
                frontmatter={"argument-hint": "<technology> [--out <path>]"},
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "codex", "prompts", "create-rule.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "copilot", "prompts", "create-rule.prompt.md"
                ),
                frontmatter={
                    "description": "Generate an implementation rule file for a technology",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase"],
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/command.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "cursor", "commands", "create-rule.md"
                ),
            ),
        },
    ),
    "create-session-notes": PromptDefinition(
        prompt_id="create-session-notes",
        source_path=_repo_path("shared", "prompts", "create-session-notes.md"),
        title="create-session-notes v1.0",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "claude-code",
                    "commands",
                    "create-session-notes.md",
                ),
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "codex", "prompts", "create-session-notes.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "copilot",
                    "prompts",
                    "create-session-notes.prompt.md",
                ),
                frontmatter={
                    "description": "Append a timestamped summary of the current session to session-notes.md",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase"],
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/command.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "cursor",
                    "commands",
                    "create-session-notes.md",
                ),
            ),
        },
    ),
    "plan-ux-prd": PromptDefinition(
        prompt_id="plan-ux-prd",
        source_path=_repo_path("shared", "prompts", "plan-ux-prd.md"),
        title="plan-ux-prd v0.3",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "claude-code", "commands", "plan-ux-prd.md"
                ),
                frontmatter={"argument-hint": "<product-brief>"},
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "codex", "prompts", "plan-ux-prd.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "copilot", "prompts", "plan-ux-prd.prompt.md"
                ),
                frontmatter={
                    "description": "Produce a UX-focused PRD from a product brief",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase"],
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/command.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "cursor", "commands", "plan-ux-prd.md"
                ),
            ),
        },
    ),
    "setup-dev-monitoring": PromptDefinition(
        prompt_id="setup-dev-monitoring",
        source_path=_repo_path("shared", "prompts", "setup-dev-monitoring.md"),
        title="setup-dev-monitoring v0.4",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "claude-code",
                    "commands",
                    "setup-dev-monitoring.md",
                ),
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "codex", "prompts", "setup-dev-monitoring.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "copilot",
                    "prompts",
                    "setup-dev-monitoring.prompt.md",
                ),
                frontmatter={
                    "description": "Configure development monitoring, logging, and orchestration",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase", "terminal"],
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/command.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "cursor",
                    "commands",
                    "setup-dev-monitoring.md",
                ),
            ),
        },
    ),
    "setup-package-monitoring": PromptDefinition(
        prompt_id="setup-package-monitoring",
        source_path=_repo_path("shared", "prompts", "setup-package-monitoring.md"),
        title="setup-package-monitoring v1.0",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "claude-code",
                    "commands",
                    "setup-package-monitoring.md",
                ),
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "codex",
                    "prompts",
                    "setup-package-monitoring.md",
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "copilot",
                    "prompts",
                    "setup-package-monitoring.prompt.md",
                ),
                frontmatter={
                    "description": "Install dependency monitoring with Dependabot and audit triggers",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase"],
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/command.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "cursor",
                    "commands",
                    "setup-package-monitoring.md",
                ),
            ),
        },
    ),
    "get-feature-primer": PromptDefinition(
        prompt_id="get-feature-primer",
        source_path=_repo_path("shared", "prompts", "get-feature-primer.md"),
        title="get-feature-primer v0.3",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "claude-code",
                    "commands",
                    "get-feature-primer.md",
                ),
                frontmatter={"argument-hint": "<task-brief> [--target <path>]"},
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "codex", "prompts", "get-feature-primer.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "copilot",
                    "prompts",
                    "get-feature-primer.prompt.md",
                ),
                frontmatter={
                    "description": "Explore the codebase and produce a comprehensive analysis and todo list",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase", "terminal"],
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/command.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "cursor", "commands", "get-feature-primer.md"
                ),
            ),
        },
    ),
    "setup-ui-pointer": PromptDefinition(
        prompt_id="setup-ui-pointer",
        source_path=_repo_path("shared", "prompts", "setup-ui-pointer.md"),
        title="setup-ui-pointer v0.1",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "claude-code",
                    "commands",
                    "setup-ui-pointer.md",
                ),
                frontmatter={"argument-hint": "[--auto] [--entry-point <path>]"},
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "codex", "prompts", "setup-ui-pointer.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "copilot",
                    "prompts",
                    "setup-ui-pointer.prompt.md",
                ),
                frontmatter={
                    "description": "Install and configure react-grab for AI-assisted element capture",
                    "mode": "agent",
                    "tools": ["edit", "search/codebase", "terminal"],
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/command.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "cursor", "commands", "setup-ui-pointer.md"
                ),
            ),
        },
    ),
    "setup-browser-tools": PromptDefinition(
        prompt_id="setup-browser-tools",
        source_path=_repo_path("shared", "prompts", "setup-browser-tools.md"),
        title="setup-browser-tools v0.1",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "claude-code",
                    "commands",
                    "setup-browser-tools.md",
                ),
                frontmatter={"argument-hint": "[--auto] [--install-dir <path>]"},
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "codex", "prompts", "setup-browser-tools.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "copilot",
                    "prompts",
                    "setup-browser-tools.prompt.md",
                ),
                frontmatter={
                    "description": "Install Chrome DevTools Protocol automation scripts for UI testing",
                    "mode": "agent",
                    "tools": ["edit", "search/codebase", "terminal"],
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/command.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "cursor", "commands", "setup-browser-tools.md"
                ),
            ),
        },
    ),
    "setup-command-history": PromptDefinition(
        prompt_id="setup-command-history",
        source_path=_repo_path("shared", "prompts", "setup-command-history.md"),
        title="setup-command-history v0.1",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "claude-code",
                    "commands",
                    "setup-command-history.md",
                ),
                frontmatter={
                    "argument-hint": "[--auto] [--register] [--username <user>] [--email <email>]"
                },
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "codex", "prompts", "setup-command-history.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "copilot",
                    "prompts",
                    "setup-command-history.prompt.md",
                ),
                frontmatter={
                    "description": "Install Atuin shell history with SQLite storage and optional cloud sync",
                    "mode": "agent",
                    "tools": ["edit", "search/codebase", "terminal"],
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/command.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "cursor",
                    "commands",
                    "setup-command-history.md",
                ),
            ),
        },
    ),
    "setup-task-lists": PromptDefinition(
        prompt_id="setup-task-lists",
        source_path=_repo_path("shared", "prompts", "setup-task-lists.md"),
        title="setup-task-lists v0.3",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "claude-code",
                    "commands",
                    "setup-task-lists.md",
                ),
                frontmatter={"argument-hint": "[--auto]"},
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "codex", "prompts", "setup-task-lists.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "copilot",
                    "prompts",
                    "setup-task-lists.prompt.md",
                ),
                frontmatter={
                    "description": "Install Beads (bd) for git-backed persistent task tracking",
                    "mode": "agent",
                    "tools": ["edit", "search/codebase", "terminal"],
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/command.md.j2",
                output_path=_repo_path(
                    ".build", "rendered", "cursor", "commands", "setup-task-lists.md"
                ),
            ),
        },
    ),
}


def list_prompts() -> Iterable[PromptDefinition]:
    return CATALOG.values()
