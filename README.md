<div align="center">
  <img src="enaible.png" alt="Enaible Logo" width="400" />

# AI Assisted Workflows

  <img src="https://img.shields.io/badge/AI_Workflows-Production_Ready-2ea44f?style=for-the-badge" alt="AI Workflows" />
  <br/>
  <br/>

  <!-- Status Badges -->

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg?style=flat-square)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg?style=flat-square)
![Tests](https://img.shields.io/badge/tests-20_analyzers-success?style=flat-square)
![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen?style=flat-square)

  <!-- Platform & Language Support -->

![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg?style=flat-square)
![Python](https://img.shields.io/badge/python-3.12-3776ab?style=flat-square&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/typescript-supported-3178c6?style=flat-square&logo=typescript&logoColor=white)
![Languages](https://img.shields.io/badge/languages-Python%20%7C%20TS%20%7C%20Go%20%7C%20Rust%20%7C%20C%23-orange?style=flat-square)

  <!-- License & Community -->

![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)
![Claude Code](https://img.shields.io/badge/Claude_Code-25_Commands-8A2BE2?style=flat-square)
![Codex Prompts](https://img.shields.io/badge/Codex-21_Prompts-FF69B4?style=flat-square)
![Copilot Prompts](https://img.shields.io/badge/Copilot-8_Prompts-0080FF?style=flat-square)
![Claude Agents](<https://img.shields.io/badge/Agents_(Claude)-32_Specialists-ff6b35?style=flat-square>)

</div>

---

## Table of Contents

- [Project Overview](#project-overview)
- [Dependencies](#dependencies)
- [Quick Start](#quick-start)
- [Available Prompts & Agents](#available-prompts--agents)
  - [Analysis](#analysis) | [Planning](#planning) | [Setup](#setup) | [Project & Feature](#project--feature) | [Utility](#utility)
  - [System-Specific Commands](#system-specific-commands) | [Agents](#agents-claude-code)

---

## Project Overview

> **Supporting AI Development Workflows with Core Principles**

The principles for this project are designed around the realities of coding with AI:

- **Lightweight** — Minimize context impact, JIT loading, external processes
- **Mitigate LLM Weaknesses** — Repeatability, predictability, duplication prevention
- **Minimize Structure** — Tools over workflows, flexibility over rigidity
- **Tool Agnostic** — Supported tools Codex, Claude Code, Copilot, Cursor, Gemini, Antigravity
- **Language Support** — Python, TypeScript, Go, Rust, C#

---

## Dependencies

- Git (command-line)
- Python 3.12.x
- `uv` 0.4 or newer
- `curl` (macOS/Linux) or PowerShell 7+ (Windows) to download the installer scripts

Install these once per workstation; the bootstrap script verifies they exist before proceeding.

---

## Quick Start

Running either installer script will:

- Clone this repository under `~/.enaible/sources/ai-assisted-workflows`.
- Install or upgrade the Enaible CLI via `uv tool install --from tools/enaible enaible`.
- Run `enaible install <system>` for each requested adapter (`codex`, `claude-code`, etc.) in the scopes you select
- Copies prompts/rules into `~/.codex`, `~/.claude`, or `<project>/.claude`.
- Capture a session log in `~/.enaible/install-sessions/` for audit trails.

## Installed dependencies to support workflows


- [`uv`](https://github.com/astral-sh/uv) — Python project/package manager we use to install the Enaible CLI and run quality gates.
- [`bun`](https://bun.sh/) — JavaScript runtime + toolkit powering the React/TanStack starter flows.
- [`Ultracite`](https://www.ultracite.ai/introduction) — Lint/format preset enforced across TypeScript and Tailwind resources.
- [`TypeScript`](https://www.typescriptlang.org/) — Strict-mode type checking for all frontend prompts and scaffolds.
- [`React`](https://react.dev/) and [`React Router`](https://reactrouter.com/) — Core UI stack referenced in Better-T-Stack workflows.
- [`shadcn/ui`](https://ui.shadcn.com/) on top of [`Radix Primitives`](https://www.radix-ui.com/primitives) — Component baseline for UI tasks.
- [`Tailwind CSS`](https://tailwindcss.com/) — Utility CSS system backing shadcn styling tokens.
- [`Zustand`](https://github.com/pmndrs/zustand) — Client-side state management for prompts requiring local stores.
- [`TanStack Query`](https://tanstack.com/query/latest) — Data fetching/cache layer that our async workflows depend on.
- [`SQLite`](https://www.sqlite.org/) + [`better-sqlite3`](https://github.com/WiseLibs/better-sqlite3) — Embedded database runtime for local-first development.
- [`Drizzle ORM`](https://orm.drizzle.team/) — Schema + migration tooling for SQLite/Postgres targets.
- [`Convex`](https://docs.convex.dev/) — Realtime collaboration backend we reference for managed deployments.
- [`PostHog`](https://posthog.com/) — Analytics/experimentation SDK initialised once consent is stored.
- [`Clerk`](https://clerk.com/) and [`Stripe`](https://stripe.com/) / [`Braintree`](https://www.braintreepayments.com/) — Managed identity and payments providers we wire into production prompts.
- [`tmux`](https://github.com/tmux/tmux) — Required multiplexer for long-running dev servers launched by automation prompts.



### macOS/Linux

```bash
curl -fsSL "https://raw.githubusercontent.com/adam-versed/ai-assisted-workflows/main/scripts/install.sh?$(date +%s)" | bash -s --
```

### Windows PowerShell 7+

```powershell
Invoke-WebRequest https://raw.githubusercontent.com/adam-versed/ai-assisted-workflows/main/scripts/install.ps1 -OutFile install.ps1
pwsh -NoLogo -File .\install.ps1 -Systems codex -Scope user
# NB: if the download is marked as coming from the internet, run `Unblock-File .\install.ps1` before execution.
```

See [docs/installation.md](docs/installation.md) for the complete flag reference and troubleshooting steps.

---

## Available Prompts & Agents

> Shared prompts work across Claude Code and Codex. System-specific commands are noted below.

### Analysis

| Prompt               | Example                             | Use Case                                              |
| -------------------- | ----------------------------------- | ----------------------------------------------------- |
| analyze-architecture | `/analyze-architecture src/`        | Evaluate layering, coupling, and scalability          |
| analyze-code-quality | `/analyze-code-quality src/`        | Assess complexity, maintainability, technical debt    |
| analyze-performance  | `/analyze-performance src/`         | Identify bottlenecks across backend, frontend, data   |
| analyze-root-cause   | `/analyze-root-cause "API timeout"` | Investigate incidents through code changes and traces |
| analyze-security     | `/analyze-security src/`            | OWASP-aligned scanning with gap analysis              |

### Planning

| Prompt          | Example                           | Use Case                                        |
| --------------- | --------------------------------- | ----------------------------------------------- |
| plan-refactor   | `/plan-refactor "auth module"`    | Design staged refactoring with risk mitigation  |
| plan-solution   | `/plan-solution "OAuth2 auth"`    | Develop and compare solution approaches         |
| plan-ux-prd     | `/plan-ux-prd "code review tool"` | Create UX-focused product requirements document |
| create-hand-off | `/create-hand-off`                | Generate handoff prompt for next AI session     |

### Setup

| Prompt                   | Example                     | Use Case                                           |
| ------------------------ | --------------------------- | -------------------------------------------------- |
| setup-dev-monitoring     | `/setup-dev-monitoring`     | Configure Makefile/Procfile with central logging   |
| setup-package-monitoring | `/setup-package-monitoring` | Install Dependabot and CI vulnerability audits     |
| setup-browser-tools      | `/setup-browser-tools`      | Install Chrome DevTools Protocol automation        |
| setup-command-history    | `/setup-command-history`    | Install Atuin shell history with SQLite            |
| setup-mgrep              | `/setup-mgrep`              | Install mgrep for semantic search across code/docs |
| setup-parallel-ai        | `/setup-parallel-ai`        | Install Parallel AI CLI for web intelligence       |
| setup-task-lists         | `/setup-task-lists`         | Initialize Beads (bd) git-backed task tracking     |
| setup-ui-pointer         | `/setup-ui-pointer`         | Install react-grab for element capture             |

### Project & Feature

| Prompt              | Example                                   | Use Case                                          |
| ------------------- | ----------------------------------------- | ------------------------------------------------- |
| setup-project       | `/setup-project api --from-todos spec.md` | Scaffold project with Better-T-Stack CLI          |
| create-rule         | `/create-rule typescript`                 | Add single rule based on topic and best practices |
| get-codebase-primer | `/get-codebase-primer`                    | Generate project overview with architecture       |
| get-feature-primer  | `/get-feature-primer "auth flow"`         | Explore codebase for feature-specific context     |

### Utility

| Prompt                      | Example                        | Use Case                                          |
| --------------------------- | ------------------------------ | ------------------------------------------------- |
| setup-code-precommit-checks | `/setup-code-precommit-checks` | Add git hooks for language-specific quality gates |

### System-Specific Commands

| Command                   | System | Example                                    | Use Case                                  |
| ------------------------- | ------ | ------------------------------------------ | ----------------------------------------- |
| codify-claude-history     | Claude | `/codify-claude-history --days 7`          | Extract workflow standards from sessions  |
| get-recent-context        | Claude | `/get-recent-context --search-term "auth"` | Orient on recent activity and git history |
| codify-codex-history      | Codex  | `/codify-codex-history`                    | Mine sessions for recurring patterns      |
| get-recent-context        | Codex  | `/get-recent-context --days 3`             | Analyze Codex session logs                |
| analyze-repo-orchestrator | Codex  | `/analyze-repo-orchestrator`               | Parallel repo analysis with KPI scoring   |
| todo-background           | Codex  | `/todo-background "refactor auth"`         | Run task in background tmux session       |

### Agents (Claude Code)

| Agent                   | Example                    | Specialization                                  |
| ----------------------- | -------------------------- | ----------------------------------------------- |
| docs-scraper            | `@docs-scraper`            | Fetch and convert docs to markdown              |
| docker-expert           | `@docker-expert`           | Advice on Container optimization and deployment |
| git-action-expert       | `@git-action-expert`       | Advice on GitHub Actions and CI/CD pipelines    |
| market-analyst          | `@market-analyst`          | Competitive intelligence and research           |
| python-expert           | `@python-expert`           | Python 3.13+ development planning               |
| rag-architecture-expert | `@rag-architecture-expert` | RAG system design and implementation            |
| research-coordinator    | `@research-coordinator`    | Multi-researcher orchestration                  |
| technical-researcher    | `@technical-researcher`    | Code repo analysis and documentation            |
| typescript-expert       | `@typescript-expert`       | TypeScript 5.7+ and Bun patterns                |
| user-researcher         | `@user-researcher`         | Persona development and journey mapping         |

---

## Quick Start & Detailed Documentation

<div align="right"><a href="#table-of-contents">back to top</a></div>

<div align="center">

|   **Category**    | **Document**                               | **Description**                               |
| :---------------: | :----------------------------------------- | :-------------------------------------------- |
|   **Setup**       | [Installation Guide](docs/installation.md) | Complete setup and configuration instructions |
| **Monitoring**    | [Dev Monitoring](docs/monitoring.md)       | Live monitoring and artifact conventions      |

---

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

[Report Issues](https://github.com/adam-versed/ai-assisted-workflows/issues) • [Request Features](https://github.com/adam-versed/ai-assisted-workflows/discussions)

</div>
