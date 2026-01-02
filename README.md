<div align="center">
  <img src="enaible.png" alt="Enaible Logo" width="400" />

**AI-Assisted Development Workflows**

[![CI](https://img.shields.io/github/actions/workflow/status/adam-jackson-cf/enaible/ci-quality-gates-incremental.yml?branch=main&style=flat-square&label=tests)](https://github.com/adam-jackson-cf/enaible/actions/workflows/ci-quality-gates-incremental.yml)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg?style=flat-square)
![Languages](https://img.shields.io/badge/languages-Python%20%7C%20TS%20%7C%20Go%20%7C%20Rust%20%7C%20C%23-orange?style=flat-square)

### v0.2.0 | Recent Changes
- feat: add automated changelog and version bumping
- feat: add pi coding agent system support
- docs: consolidate system documentation into single READMEs
- chore: added todos
- chore: updated readme table

[Full Changelog](CHANGELOG.md)

</div>

---

## Quick Install

```bash
curl -fsSL "https://raw.githubusercontent.com/adam-jackson-cf/enaible/main/scripts/install.sh?$(date +%s)" \
  | bash -s -- --systems codex --scope user
```

> Valid `--systems` values: `codex`, `claude-code`, `copilot`, `cursor`, `gemini`, `antigravity` (use comma-separated lists for multiple scopes).
> Valid `--scope` values: `user` or `project)`
> If you choose `project`, run the script from the root of the target git repo or supply `--project /absolute/path/to/repo` so the installer can locate the project repo.

### Windows PowerShell 7+

```powershell
Invoke-WebRequest https://raw.githubusercontent.com/adam-jackson-cf/enaible/main/scripts/install.ps1 -OutFile install.ps1
pwsh -NoLogo -File .\install.ps1 -Systems claude-code -Scope user
# NB: if the download is marked as coming from the internet, run `Unblock-File .\install.ps1` before execution.
```

> Follows same flags as macOS/Linux installer, Supply `-Systems` (same valid values as above) and `-Scope`
> for project path include `-Project 'C:\path\to\repo'` so the installer can locate the project repo.

See [docs/installation.md](docs/installation.md) for manual install options and complete flag reference.

---

## Common Workflows

> These examples show how prompts combine to solve real development scenarios.

### Onboarding to a New Codebase

```bash
/get-codebase-primer                    # Understand architecture, tech stack, commands
/analyze-code-quality                   # Evaluate layering, coupling, scalability and flag improvements
/analyze-code-architecture
```

### Coding a task

```bash
/get-task-primer "authentication"       # Deep dive into specific task areas
# execute coding loop task work
/analyze-code-quality                   # Code review - evaluate layering, coupling, scalability and flag improvements (uses lizard + others)
/analyze-security                       # Code review - ensure no security issues (uses semgrep)
```

### Planning a New Task

```bash
/get-task-primer "payments"             # Gather context on related code
/plan-solution "Add Stripe integration" # Compare Conservative, Balanced, Innovative approaches
```

### Investigating Production Issues

```bash
/analyze-root-cause "API timeout errors"  # Trace through recent code changes
```

### Setting Up a New Project

```bash
/setup-dev-monitoring                   # Makefile + Procfile with central logging
/setup-code-precommit-checks            # Git hooks for quality gates
/setup-beads                            # Git-backed task tracking with Beads
```

### Preparing for Code Review / Handoff

```bash
/analyze-code-quality src/                    # Complexity metrics, technical debt signals
/plan-refactor "based on code quality report" # use code quality report to plan out least intrusive refactor
```

---

## Shared Skills

Shared skills live in `shared/skills/` and are rendered into each supported system during install. Use them by name in your request when you want a multi-step workflow or deterministic tooling.

### Example Skill Usage

```bash
"Use docs-scraper to save https://react.dev/reference/react into ./docs"
"Use codify-pr-reviews to create review codex rules from this repo"
```

---

## Quick Reference

```bash

ANALYSIS
/analyze-architecture [path] [--auto] [--verbose]
/analyze-code-quality [path] [--auto]
/analyze-security [path] [--min-severity critical|high|medium|low]
/analyze-performance [path]
/analyze-root-cause "description"

PLANNING
/plan-solution "problem" [--target-path ./] [--auto]
/plan-refactor "module" [--auto]
/plan-ux-prd "feature"
/create-hand-off

CONTEXT
/get-codebase-primer [--target-path ./]
/get-task-primer "task" [--target-path ./]
/create-rule <topic>

SETUP TOOLING
/setup-dev-monitoring /setup-browser-tools
/setup-code-precommit-checks /setup-atuin
/setup-package-monitoring /setup-mgrep
/setup-beads
/setup-react-grab

SKILLS (use by name in your request)
docs-scraper "save https://react.dev/reference/react into ./docs"
codify-pr-reviews "create review codex rules from this repo"

```

> **Tip:** Add `--auto` to skip confirmation prompts. Add `--verbose` for extended output.

---

<details>

<summary><strong>Complete Prompt Reference</strong></summary>

### Analysis

| Prompt               | Use Case                                                   |
| -------------------- | ---------------------------------------------------------- |
| analyze-architecture | Evaluate layering, coupling, and scalability trade-offs    |
| analyze-code-quality | Assess complexity, maintainability, technical debt         |
| analyze-performance  | Identify bottlenecks across backend, frontend, data layers |
| analyze-root-cause   | Investigate incidents through code changes and traces      |
| analyze-security     | OWASP-aligned scanning with gap analysis                   |

### Planning

| Prompt          | Use Case                                                                     |
| --------------- | ---------------------------------------------------------------------------- |
| plan-refactor   | Design staged refactoring with risk mitigation                               |
| plan-solution   | Develop and compare solution approaches (Conservative, Balanced, Innovative) |
| plan-ux-prd     | Create UX-focused product requirements document                              |
| create-hand-off | Generate handoff prompt for next AI session                                  |

### Setup

| Prompt                      | Use Case                                           |
| --------------------------- | -------------------------------------------------- |
| setup-dev-monitoring        | Configure Makefile/Procfile with central logging   |
| setup-package-monitoring    | Install Dependabot and CI vulnerability audits     |
| setup-browser-tools         | Install Chrome DevTools Protocol automation        |
| setup-atuin                 | Install Atuin shell history with SQLite            |
| setup-mgrep                 | Install mgrep for semantic search across code/docs |
| setup-beads                 | Initialize Beads (bd) git-backed task tracking     |
| setup-react-grab            | Install react-grab for element capture             |
| setup-code-precommit-checks | Add git hooks for language-specific quality gates  |

### Project & Task

| Prompt              | Use Case                                          |
| ------------------- | ------------------------------------------------- |
| create-rule         | Add single rule based on topic and best practices |
| get-codebase-primer | Generate project overview with architecture       |
| get-task-primer     | Explore codebase for task-specific context        |
| task-background     | Run cli task in background tmux session           |

### Shared Skills

| Skill             | Use Case                                            | Example request                                                     |
| ----------------- | --------------------------------------------------- | ------------------------------------------------------------------- |
| docs-scraper      | Scrape documentation URLs into clean markdown files | `Use docs-scraper to save https://react.dev/reference/react`        |
| codify-pr-reviews | Convert PR review comments into instruction rules   | `Use codify-pr-reviews to create review codex rules from this repo` |

### System-Specific Commands

| Command                   | System                | Example                                    | Use Case                                  |
| ------------------------- | --------------------- | ------------------------------------------ | ----------------------------------------- |
| codify-session-history    | Shared (Codex/Claude) | `/codify-session-history --days 7`         | Extract workflow standards from sessions  |
| get-recent-context        | Shared (Codex/Claude) | `/get-recent-context --search-term "auth"` | Orient on recent activity and git history |
| analyze-repo-orchestrator | Codex                 | `/analyze-repo-orchestrator`               | Parallel repo analysis with KPI scoring   |

</details>

---

<div align="center">

**[Installation Guide](docs/installation.md)** | **[Dev Monitoring](docs/monitoring.md)** | **[Testing](docs/testing.md)**

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

[Report Issues](https://github.com/adam-jackson-cf/enaible/issues) | [Request Features](https://github.com/adam-jackson-cf/enaible/discussions)

</div>
