# Changelog

All notable changes to this project will be documented in this file.

## [1.1.1] - 2026-01-07

- docs: add next session handoff

## [1.1.1] - 2026-01-07

- fix: apply exclusions to readiness analyzers
- refactor: modularize agentic readiness workflow
- refactor: restore agentic readiness prompt name
- docs: align README changes and dedupe agents

## [1.1.0] - 2026-01-03

- feat: add agentic readiness prompt and speed up gates
- fix: skip installing system rules files
- fix: merge shared rules for installs
- fix: sync rules and setup docs
- chore: clarify gate python requirement and install helpers
- chore: restore uv lockfile

## [1.0.0] - 2026-01-03

- docs: document Cursor hook support
- chore: migrate docs-scraper skill

## [1.0.0] - 2026-01-02

- feat: filter README recent changes to features and breaking changes

## [0.4.0] - 2026-01-02

- feat: add research skill for multi-domain investigations
- docs: sync README with v0.3.0
- docs: enforce online research requirements in research skill

## [0.3.0] - 2026-01-02

- feat: add new analyzers and fixtures for parity
- docs: add analysis gaps implementation plan
- chore: added todos for design, bid proposal and solution analysis skills

## [0.2.0] - 2026-01-02

- feat: add automated changelog and version bumping
- feat: add pi coding agent system support
- docs: consolidate system documentation into single READMEs
- chore: added todos
- chore: updated readme table
- Fix token replacement order and standardize uv run usage
- Remove use-parallel-ai skill
- Fix datetime deprecation and JSON error handling in codify-pr-reviews
- Add codified PR review standards to AGENTS.md
- Fix docs-scraper CLI syntax to use positional arguments
- Standardize skills documentation and assets
- Add onboarding todo brief
- Simplify background report naming
- Update Claude model list
- Harden tmux session check
- Stream background output only
- Avoid persistent codex last-message files
- Fix tmux pid lookup syntax
- Limit background launch checks
- Clarify background task reporting
- Add friendly task labels and richer reports
- Harden task-background launch flow
- Fix codex reasoning config in task-background
- Add analysis improvement reports
- Render analyze-security prompt updates
- Recommend parallel analyzer execution
- Emit summary artifacts without re-running analyzers
- Align analyze prompts with artifact and severity guidance
- Enforce severity threshold guidance in analyze-code-quality
- Clarify absolute artifact paths and jscpd scoping
- Stabilize analyze-code-quality artifacts and summaries
- Harden jscpd excludes and prompt exclusions
- Remove source URL ref detection from PowerShell installer
- Sync context scripts in workspace install
- Add project root to codify session history
- Pass project root to context_capture in get-recent-context
- Revert legacy get-recent-context install handling
- Treat get-recent-context as managed legacy prompt
- Handle curl installs without BASH_SOURCE
- Require explicit ref for curl installer
- Handle missing BASH_SOURCE in installer
- Fix installer when BASH_SOURCE is unset
- Allow PowerShell installer to target non-main refs
- Allow installer to target non-main refs
- Fix analyze-root-cause list indentation
- Update README for shared prompt moves
- Move get-recent-context to shared prompt
- Unify session history codify prompt
- Rename get-feature-primer to get-task-primer
- Move task background prompt to shared catalog

## [0.1.1] - 2026-01-02

- feat: add pi coding agent system support
- fix: token replacement order and standardize uv run usage
- fix: datetime deprecation and JSON error handling in codify-pr-reviews
- fix: docs-scraper CLI syntax to use positional arguments
- chore: added todos
- chore: remove use-parallel-ai skill
- chore: add codified PR review standards to AGENTS.md
- chore: standardize skills documentation and assets
- chore: add onboarding todo brief

## [0.1.0] - 2025-12-31

- feat: add friendly task labels and richer reports
- feat: clarify background task reporting
- fix: limit background launch checks
- fix: tmux pid lookup syntax
- fix: avoid persistent codex last-message files
- fix: stream background output only
- fix: harden tmux session check
- chore: update Claude model list
- chore: simplify background report naming
