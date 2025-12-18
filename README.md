<div align="center">
  <img src="enaible.png" alt="Enaible Logo" width="400" />

**AI-Assisted Development Workflows**

![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg?style=flat-square)
![Languages](https://img.shields.io/badge/languages-Python%20%7C%20TS%20%7C%20Go%20%7C%20Rust%20%7C%20C%23-orange?style=flat-square)

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

> Like the macOS/Linux installer, the PowerShell script prompts only when it has access to the console. Supply `-Systems`
> (same valid values as above) and `-Scope` explicitly anytime you invoke it via a pipeline or non-interactive shell. For the project scope, run the
> command from the destination repo or include `-Project 'C:\path\to\repo'` so the installer knows where to copy
> managed files.

See [docs/installation.md](docs/installation.md) for manual install options and complete flag reference.

---

## Common Workflows

> These examples show how prompts combine to solve real development scenarios.

### Onboarding to a New Codebase

```bash
/get-codebase-primer                    # Understand architecture, tech stack, commands
/analyze-architecture src/              # Evaluate layering, coupling, scalability
/get-feature-primer "authentication"    # Deep dive into specific feature areas
```

### Planning a New Feature

```bash
/get-feature-primer "payments"          # Gather context on related code
/plan-solution "Add Stripe integration" # Compare Conservative, Balanced, Innovative approaches
/analyze-security src/payments/         # Security review before implementation
```

### Investigating Production Issues

```bash
/analyze-root-cause "API timeout errors"  # Trace through recent code changes
/analyze-performance src/api/             # Identify bottlenecks and hotspots
```

### Setting Up a New Project

```bash
/setup-dev-monitoring                   # Makefile + Procfile with central logging
/setup-code-precommit-checks            # Git hooks for quality gates
/setup-task-lists                       # Git-backed task tracking with Beads
```

### Preparing for Code Review / Handoff

```bash
/analyze-code-quality src/              # Complexity metrics, technical debt signals
/create-hand-off                        # Generate context prompt for next session
```

---

## Quick Reference

```
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
  /get-feature-primer "feature" [--target-path ./]
  /create-rule <topic>

SETUP
  /setup-dev-monitoring       /setup-browser-tools
  /setup-code-precommit-checks    /setup-command-history
  /setup-package-monitoring       /setup-mgrep
  /setup-task-lists           /setup-parallel-ai
  /setup-ui-pointer
```

> **Tip:** Add `--auto` to skip confirmation prompts. Add `--verbose` for extended output.

---

## Dependencies by Workflow

| Workflow              | Required Tools                                                                                        |
| --------------------- | ----------------------------------------------------------------------------------------------------- |
| Code Quality Analysis | [Lizard](https://github.com/terryyin/lizard), [JSCPD](https://github.com/kucherenko/jscpd) (Node/npm) |
| Security Scanning     | [Semgrep](https://semgrep.dev/), [detect-secrets](https://github.com/Yelp/detect-secrets)             |
| Performance Analysis  | [Ruff](https://docs.astral.sh/ruff/), [ESLint](https://eslint.org/) + TS/React plugins (for JS/TS)    |
| All Other Prompts     | None (built-in analyzers)                                                                             |

**Prerequisites:** Git, Python 3.12+, [uv](https://docs.astral.sh/uv/) 0.4+, Node.js 18+ (for JSCPD)

---

## System-Specific Commands

| Command                   | System | Example                                    | Use Case                                  |
| ------------------------- | ------ | ------------------------------------------ | ----------------------------------------- |
| codify-claude-history     | Claude | `/codify-claude-history --days 7`          | Extract workflow standards from sessions  |
| get-recent-context        | Claude | `/get-recent-context --search-term "auth"` | Orient on recent activity and git history |
| codify-codex-history      | Codex  | `/codify-codex-history`                    | Mine sessions for recurring patterns      |
| get-recent-context        | Codex  | `/get-recent-context --days 3`             | Analyze Codex session logs                |
| analyze-repo-orchestrator | Codex  | `/analyze-repo-orchestrator`               | Parallel repo analysis with KPI scoring   |
| todo-background           | Codex  | `/todo-background "refactor auth"`         | Run task in background tmux session       |

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
| setup-command-history       | Install Atuin shell history with SQLite            |
| setup-mgrep                 | Install mgrep for semantic search across code/docs |
| setup-parallel-ai           | Install Parallel AI CLI for web intelligence       |
| setup-task-lists            | Initialize Beads (bd) git-backed task tracking     |
| setup-ui-pointer            | Install react-grab for element capture             |
| setup-code-precommit-checks | Add git hooks for language-specific quality gates  |

### Project & Feature

| Prompt              | Use Case                                          |
| ------------------- | ------------------------------------------------- |
| create-rule         | Add single rule based on topic and best practices |
| get-codebase-primer | Generate project overview with architecture       |
| get-feature-primer  | Explore codebase for feature-specific context     |

### Agents (Claude Code)

| Agent        | Specialization                     |
| ------------ | ---------------------------------- |
| docs-scraper | Fetch and convert docs to markdown |

</details>

---

<div align="center">

**[Installation Guide](docs/installation.md)** | **[Dev Monitoring](docs/monitoring.md)** | **[Testing](docs/testing.md)**

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

[Report Issues](https://github.com/adam-jackson-cf/enaible/issues) | [Request Features](https://github.com/adam-jackson-cf/enaible/discussions)

</div>
