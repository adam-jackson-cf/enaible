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
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "codex", "prompts", "analyze-security.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "copilot", "prompts", "analyze-security.prompt.md"
                ),
                frontmatter={
                    "description": "Perform a comprehensive security audit of the repository and dependencies",
                    "mode": "agent",
                    "tools": ["edit", "githubRepo", "search/codebase", "terminal"],
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/rule.mdc.j2",
                output_path=_repo_path(
                    "systems", "cursor", "rules", "analyze-security.mdc"
                ),
                frontmatter={},
                metadata={"rule_category": "security"},
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
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "codex", "prompts", "analyze-architecture.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "copilot", "prompts", "analyze-architecture.prompt.md"
                ),
                frontmatter={
                    "description": "Evaluate system architecture for scalability, maintainability, and best practices",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase"],
                    "cursor": SystemPromptConfig(
                        template="docs/system/cursor/templates/rule.mdc.j2",
                        output_path=_repo_path(
                            "systems", "cursor", "rules", "analyze-architecture.mdc"
                        ),
                        frontmatter={},
                        metadata={"rule_category": "analysis"},
                    ),
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/rule.mdc.j2",
                output_path=_repo_path(
                    "systems", "cursor", "rules", "analyze-architecture.mdc"
                ),
                frontmatter={},
                metadata={"rule_category": "analysis"},
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
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "codex", "prompts", "analyze-code-quality.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "copilot", "prompts", "analyze-code-quality.prompt.md"
                ),
                frontmatter={
                    "description": "Assess code quality and complexity, and highlight high-value refactors",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase", "terminal"],
                    "cursor": SystemPromptConfig(
                        template="docs/system/cursor/templates/rule.mdc.j2",
                        output_path=_repo_path(
                            "systems", "cursor", "rules", "analyze-code-quality.mdc"
                        ),
                        frontmatter={},
                        metadata={"rule_category": "quality"},
                    ),
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/rule.mdc.j2",
                output_path=_repo_path(
                    "systems", "cursor", "rules", "analyze-code-quality.mdc"
                ),
                frontmatter={},
                metadata={"rule_category": "quality"},
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
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "codex", "prompts", "analyze-performance.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "copilot", "prompts", "analyze-performance.prompt.md"
                ),
                frontmatter={
                    "description": "Identify performance bottlenecks and propose minimal, high-impact optimizations",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase", "terminal"],
                    "cursor": SystemPromptConfig(
                        template="docs/system/cursor/templates/rule.mdc.j2",
                        output_path=_repo_path(
                            "systems", "cursor", "rules", "analyze-performance.mdc"
                        ),
                        frontmatter={},
                        metadata={"rule_category": "performance"},
                    ),
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/rule.mdc.j2",
                output_path=_repo_path(
                    "systems", "cursor", "rules", "analyze-performance.mdc"
                ),
                frontmatter={},
                metadata={"rule_category": "performance"},
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
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "codex", "prompts", "analyze-root-cause.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "copilot", "prompts", "analyze-root-cause.prompt.md"
                ),
                frontmatter={
                    "description": "Perform root cause analysis for a defect or failure",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase"],
                    "cursor": SystemPromptConfig(
                        template="docs/system/cursor/templates/rule.mdc.j2",
                        output_path=_repo_path(
                            "systems", "cursor", "rules", "analyze-root-cause.mdc"
                        ),
                        frontmatter={},
                        metadata={"rule_category": "debugging"},
                    ),
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/rule.mdc.j2",
                output_path=_repo_path(
                    "systems", "cursor", "rules", "analyze-root-cause.mdc"
                ),
                frontmatter={},
                metadata={"rule_category": "debugging"},
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
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "codex", "prompts", "plan-refactor.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "copilot", "prompts", "plan-refactor.prompt.md"
                ),
                frontmatter={
                    "description": "Plan a minimal, high-impact refactor with clear boundaries and tests",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase"],
                    "cursor": SystemPromptConfig(
                        template="docs/system/cursor/templates/rule.mdc.j2",
                        output_path=_repo_path(
                            "systems", "cursor", "rules", "plan-refactor.mdc"
                        ),
                        frontmatter={},
                        metadata={"rule_category": "planning"},
                    ),
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/rule.mdc.j2",
                output_path=_repo_path(
                    "systems", "cursor", "rules", "plan-refactor.mdc"
                ),
                frontmatter={},
                metadata={"rule_category": "planning"},
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
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "codex", "prompts", "plan-solution.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "copilot", "prompts", "plan-solution.prompt.md"
                ),
                frontmatter={
                    "description": "Develop a solution plan for a technical challenge with constraints and milestones",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase"],
                    "cursor": SystemPromptConfig(
                        template="docs/system/cursor/templates/rule.mdc.j2",
                        output_path=_repo_path(
                            "systems", "cursor", "rules", "plan-solution.mdc"
                        ),
                        frontmatter={},
                        metadata={"rule_category": "planning"},
                    ),
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/rule.mdc.j2",
                output_path=_repo_path(
                    "systems", "cursor", "rules", "plan-solution.mdc"
                ),
                frontmatter={},
                metadata={"rule_category": "planning"},
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
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "copilot", "prompts", "get-codebase-primer.prompt.md"
                ),
                frontmatter={
                    "description": "Generate a comprehensive primer for understanding the codebase",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase"],
                    "cursor": SystemPromptConfig(
                        template="docs/system/cursor/templates/rule.mdc.j2",
                        output_path=_repo_path(
                            "systems", "cursor", "rules", "get-codebase-primer.mdc"
                        ),
                        frontmatter={},
                        metadata={"rule_category": "documentation"},
                    ),
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/rule.mdc.j2",
                output_path=_repo_path(
                    "systems", "cursor", "rules", "get-codebase-primer.mdc"
                ),
                frontmatter={},
                metadata={"rule_category": "documentation"},
            ),
        },
    ),
    "add-code-precommit-checks": PromptDefinition(
        prompt_id="add-code-precommit-checks",
        source_path=_repo_path("shared", "prompts", "add-code-precommit-checks.md"),
        title="add-code-precommit-checks v1.0",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    "systems", "claude-code", "commands", "add-code-precommit-checks.md"
                ),
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "codex", "prompts", "add-code-precommit-checks.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems",
                    "copilot",
                    "prompts",
                    "add-code-precommit-checks.prompt.md",
                ),
                frontmatter={
                    "description": "Set up language-appropriate pre-commit hooks for the repo",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase", "terminal"],
                    "cursor": SystemPromptConfig(
                        template="docs/system/cursor/templates/rule.mdc.j2",
                        output_path=_repo_path(
                            "systems",
                            "cursor",
                            "rules",
                            "add-code-precommit-checks.mdc",
                        ),
                        frontmatter={},
                        metadata={"rule_category": "development"},
                    ),
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/rule.mdc.j2",
                output_path=_repo_path(
                    "systems", "cursor", "rules", "add-code-precommit-checks.mdc"
                ),
                frontmatter={},
                metadata={"rule_category": "development"},
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
                    "systems", "claude-code", "commands", "apply-rule-set.md"
                ),
                frontmatter={"argument-hint": "<ruleset-name>"},
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "codex", "prompts", "apply-rule-set.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "copilot", "prompts", "apply-rule-set.prompt.md"
                ),
                frontmatter={
                    "description": "Load a named rule set and apply its guidance to the session",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase"],
                    "cursor": SystemPromptConfig(
                        template="docs/system/cursor/templates/rule.mdc.j2",
                        output_path=_repo_path(
                            "systems", "cursor", "rules", "apply-rule-set.mdc"
                        ),
                        frontmatter={},
                        metadata={"rule_category": "configuration"},
                    ),
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/rule.mdc.j2",
                output_path=_repo_path(
                    "systems", "cursor", "rules", "apply-rule-set.mdc"
                ),
                frontmatter={},
                metadata={"rule_category": "configuration"},
            ),
        },
    ),
    "create-project": PromptDefinition(
        prompt_id="create-project",
        source_path=_repo_path("shared", "prompts", "create-project.md"),
        title="create-project v1.0",
        systems={
            "claude-code": SystemPromptConfig(
                template="docs/system/claude-code/templates/command.md.j2",
                output_path=_repo_path(
                    "systems", "claude-code", "commands", "create-project.md"
                ),
                frontmatter={"argument-hint": "<project-name> [--from-plan <file>]"},
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "codex", "prompts", "create-project.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "copilot", "prompts", "create-project.prompt.md"
                ),
                frontmatter={
                    "description": "Scaffold a new project with Better-T-Stack CLI",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase", "terminal"],
                    "cursor": SystemPromptConfig(
                        template="docs/system/cursor/templates/rule.mdc.j2",
                        output_path=_repo_path(
                            "systems", "cursor", "rules", "create-project.mdc"
                        ),
                        frontmatter={},
                        metadata={"rule_category": "scaffolding"},
                    ),
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/rule.mdc.j2",
                output_path=_repo_path(
                    "systems", "cursor", "rules", "create-project.mdc"
                ),
                frontmatter={},
                metadata={"rule_category": "scaffolding"},
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
                    "systems", "claude-code", "commands", "create-rule.md"
                ),
                frontmatter={"argument-hint": "<technology> [--out <path>]"},
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path("systems", "codex", "prompts", "create-rule.md"),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "copilot", "prompts", "create-rule.prompt.md"
                ),
                frontmatter={
                    "description": "Generate an implementation rule file for a technology",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase"],
                    "cursor": SystemPromptConfig(
                        template="docs/system/cursor/templates/rule.mdc.j2",
                        output_path=_repo_path(
                            "systems", "cursor", "rules", "create-rule.mdc"
                        ),
                        frontmatter={},
                        metadata={"rule_category": "configuration"},
                    ),
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/rule.mdc.j2",
                output_path=_repo_path("systems", "cursor", "rules", "create-rule.mdc"),
                frontmatter={},
                metadata={"rule_category": "configuration"},
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
                    "systems", "claude-code", "commands", "create-session-notes.md"
                ),
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "codex", "prompts", "create-session-notes.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems",
                    "copilot",
                    "prompts",
                    "create-session-notes.prompt.md",
                ),
                frontmatter={
                    "description": "Append a timestamped summary of the current session to session-notes.md",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase"],
                    "cursor": SystemPromptConfig(
                        template="docs/system/cursor/templates/rule.mdc.j2",
                        output_path=_repo_path(
                            "systems", "cursor", "rules", "create-session-notes.mdc"
                        ),
                        frontmatter={},
                        metadata={"rule_category": "documentation"},
                    ),
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/rule.mdc.j2",
                output_path=_repo_path(
                    "systems", "cursor", "rules", "create-session-notes.mdc"
                ),
                frontmatter={},
                metadata={"rule_category": "documentation"},
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
                    "systems", "claude-code", "commands", "plan-ux-prd.md"
                ),
                frontmatter={"argument-hint": "<product-brief>"},
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path("systems", "codex", "prompts", "plan-ux-prd.md"),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "copilot", "prompts", "plan-ux-prd.prompt.md"
                ),
                frontmatter={
                    "description": "Produce a UX-focused PRD from a product brief",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase"],
                    "cursor": SystemPromptConfig(
                        template="docs/system/cursor/templates/rule.mdc.j2",
                        output_path=_repo_path(
                            "systems", "cursor", "rules", "plan-ux-prd.mdc"
                        ),
                        frontmatter={},
                        metadata={"rule_category": "planning"},
                    ),
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/rule.mdc.j2",
                output_path=_repo_path("systems", "cursor", "rules", "plan-ux-prd.mdc"),
                frontmatter={},
                metadata={"rule_category": "planning"},
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
                    "systems", "claude-code", "commands", "setup-dev-monitoring.md"
                ),
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "codex", "prompts", "setup-dev-monitoring.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems",
                    "copilot",
                    "prompts",
                    "setup-dev-monitoring.prompt.md",
                ),
                frontmatter={
                    "description": "Configure development monitoring, logging, and orchestration",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase", "terminal"],
                    "cursor": SystemPromptConfig(
                        template="docs/system/cursor/templates/rule.mdc.j2",
                        output_path=_repo_path(
                            "systems", "cursor", "rules", "setup-dev-monitoring.mdc"
                        ),
                        frontmatter={},
                        metadata={"rule_category": "development"},
                    ),
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/rule.mdc.j2",
                output_path=_repo_path(
                    "systems", "cursor", "rules", "setup-dev-monitoring.mdc"
                ),
                frontmatter={},
                metadata={"rule_category": "development"},
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
                    "systems",
                    "claude-code",
                    "commands",
                    "setup-package-monitoring.md",
                ),
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "codex", "prompts", "setup-package-monitoring.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems",
                    "copilot",
                    "prompts",
                    "setup-package-monitoring.prompt.md",
                ),
                frontmatter={
                    "description": "Install dependency monitoring with Dependabot and audit triggers",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase"],
                    "cursor": SystemPromptConfig(
                        template="docs/system/cursor/templates/rule.mdc.j2",
                        output_path=_repo_path(
                            "systems", "cursor", "rules", "setup-package-monitoring.mdc"
                        ),
                        frontmatter={},
                        metadata={"rule_category": "development"},
                    ),
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/rule.mdc.j2",
                output_path=_repo_path(
                    "systems", "cursor", "rules", "setup-package-monitoring.mdc"
                ),
                frontmatter={},
                metadata={"rule_category": "development"},
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
                    "systems", "claude-code", "commands", "get-feature-primer.md"
                ),
                frontmatter={"argument-hint": "<task-brief> [--target <path>]"},
            ),
            "codex": SystemPromptConfig(
                template="docs/system/codex/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems", "codex", "prompts", "get-feature-primer.md"
                ),
                metadata={"comment": "codex prompt (frontmatter-free)"},
            ),
            "copilot": SystemPromptConfig(
                template="docs/system/copilot/templates/prompt.md.j2",
                output_path=_repo_path(
                    "systems",
                    "copilot",
                    "prompts",
                    "get-feature-primer.prompt.md",
                ),
                frontmatter={
                    "description": "Explore the codebase and produce a comprehensive analysis and todo list",
                    "mode": "agent",
                    "tools": ["githubRepo", "search/codebase", "terminal"],
                    "cursor": SystemPromptConfig(
                        template="docs/system/cursor/templates/rule.mdc.j2",
                        output_path=_repo_path(
                            "systems", "cursor", "rules", "get-feature-primer.mdc"
                        ),
                        frontmatter={},
                        metadata={"rule_category": "analysis"},
                    ),
                },
            ),
            "cursor": SystemPromptConfig(
                template="docs/system/cursor/templates/rule.mdc.j2",
                output_path=_repo_path(
                    "systems", "cursor", "rules", "get-feature-primer.mdc"
                ),
                frontmatter={},
                metadata={"rule_category": "analysis"},
            ),
        },
    ),
}


def list_prompts() -> Iterable[PromptDefinition]:
    return CATALOG.values()
