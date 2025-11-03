# Roadmap

This document tracks progress toward fully productizing the Enaible automation stack across Codex, Claude Code, and OpenCode.

## Principle scorecard

| Principle               | Status  | Notes                                                                                                        |
| ----------------------- | ------- | ------------------------------------------------------------------------------------------------------------ |
| Lightweight tooling     | 🟢 80%  | Enaible consolidates install + analyzer flows; remaining work focuses on pruning legacy scripts.             |
| Mitigate LLM weaknesses | 🟡 60%  | Managed prompts enforce structured workflows; additional validation around long-running sessions is planned. |
| Minimize structure      | 🟢 80%  | Prompt catalog keeps workflows modular; future work will simplify custom prompt overrides.                   |
| LLM agnostic            | 🟢 80%  | Core flows target Codex, Claude Code, and OpenCode; adapters for additional CLIs are on the backlog.         |
| Language coverage       | 🟢 100% | Analyzer suite spans Python, TypeScript, SQL, and cross-language heuristics.                                 |

## 2025 milestones

### Q4 2025 (in progress)

- ✅ Ship Enaible installer (`enaible install <system>`) with project and user scopes.
- ✅ Convert analyzer workflows to Typer commands with normalized JSON outputs.
- 🔄 Expand managed prompt catalog to cover remaining historical slash commands.
- 🔄 Document analyzer usage, installation, monitoring, and agent orchestration (this documentation set).
- 🔲 Add automated regression tests for render/install flows in CI (pending).

### Q1 2026 (planned)

- Finalize multi-repo installation story with remote target support baked into `enaible install`.
- Add performance baselines for Bun/TanStack stacks and integrate with Ultracite linting defaults.
- Harden provenance integration with the optional `../provenance` stack and publish quick-start instructions.
- Provide migration playbooks for teams moving from legacy prompt sets to the consolidated Enaible catalog.

## Backlog

- Codex/OpenCode prompt parity for context capture helpers.
- Additional analyzer adapters (e.g., Semgrep security bundles for specific languages, linter bridges for Go/Rust).
- Enhanced artifact schema validation stored in `.enaible/schema.json`.
- Rich CLI telemetry to surface prompt drift and analyzer health inside the `enaible doctor` report.

Progress updates are captured in commits tagged with `docs:` or `enaible:` and summarized quarterly in `todos/` planning notes.
