# Agent Orchestration System

Platform support: Available for Claude Code and OpenCode. Prompts live in `claude-code/agents` and `opencode/agent`; parity is maintained where possible. Codex CLI currently executes single-agent workflows, so these subagents are not yet exposed there.

The overall approach taken with subagents as seeing them as specific context managers for a given task - the ideas is to break off items that can be self contained tasks where we are only interested in the result, rather than polluting the context with the process.

## 🚀 Core Orchestration Agents

| Agent                  | Role                | Responsibility                         | Platforms         |
| :--------------------- | :------------------ | :------------------------------------- | :---------------- |
| **plan-manager**       | 📋 Project Manager  | Task state and progress tracking       | Claude • OpenCode |
| **senior-developer**   | 💻 Developer        | Cross-platform implementation          | Claude • OpenCode |
| **solution-validator** | ✅ Architect        | Pre-implementation validation          | Claude • OpenCode |
| **quality-monitor**    | 🔍 QA Engineer      | Dynamic quality gate detection         | Claude • OpenCode |
| **git-manager**        | 🌿 DevOps           | Version control operations             | Claude • OpenCode |
| **documenter**         | 📚 Technical Writer | Documentation discovery and management | Claude • OpenCode |
| **log-monitor**        | 📊 SRE              | Runtime error detection                | Claude • OpenCode |
| **problem-escalation** | 🎯 Escalation       | Critical failure handling              | Claude • OpenCode |

## 🧠 Engineering Specialists

| Agent                       | Specialization         | Purpose                                       | Platforms         |
| :-------------------------- | :--------------------- | :-------------------------------------------- | :---------------- |
| **python-expert**           | Python Development     | Expert planning for Python tasks              | Claude • OpenCode |
| **typescript-expert**       | TypeScript Development | Expert planning for TypeScript tasks          | Claude • OpenCode |
| **docker-expert**           | Containerization       | Docker containerization and orchestration     | Claude • OpenCode |
| **terraform-gcp-expert**    | Infrastructure         | Terraform and GCP infrastructure planning     | Claude • OpenCode |
| **git-action-expert**       | CI/CD & GitHub Actions | CI/CD pipeline and GitHub Actions specialist  | Claude • OpenCode |
| **rag-architecture-expert** | RAG Systems            | Architecture planning for RAG implementations | Claude • OpenCode |

## 📝 Research & Analysis

| Agent                    | Specialization      | Purpose                                    | Platforms         |
| :----------------------- | :------------------ | :----------------------------------------- | :---------------- |
| **user-researcher**      | User Research       | User behavior analysis and market research | Claude • OpenCode |
| **market-analyst**       | Market Intelligence | Competitor and market analysis             | Claude • OpenCode |
| **technical-researcher** | Technical Research  | Code analysis and implementation research  | Claude • OpenCode |
| **research-coordinator** | Research Management | Multi-agent research workflow coordination | Claude • OpenCode |
| **docs-scraper**         | Documentation       | Web documentation scraping and processing  | Claude • OpenCode |

## 🎨 Design & User Experience

| Agent           | Specialization | Purpose                              | Platforms         |
| :-------------- | :------------- | :----------------------------------- | :---------------- |
| **ux-designer** | UX Design      | User experience design and planning  | Claude • OpenCode |
| **ux-reviewer** | UX Analysis    | User interface review and validation | Claude • OpenCode |

## ⚡ Delegation Handlers (Claude Code)

| Agent              | Purpose                   | Platforms |
| :----------------- | :------------------------ | :-------- |
| **gemini-handler** | Context-heavy analysis    | Claude    |
| **qwen-handler**   | Tool-intensive operations | Claude    |

## ⚡ Free Tier Agent Maximization

**Strategic subagents that extend Claude Code session uptime by leveraging free AI CLI tools:**

| Agent                     | Specialization            | Free Tier Benefits                                 |
| :------------------------ | :------------------------ | :------------------------------------------------- |
| **@agent-gemini-handler** | 🧠 Context-Heavy Analysis | 1,000 requests/day • 1M token context • OAuth      |
| **@agent-qwen-handler**   | 🔧 Tool-Heavy Operations  | 2,000 requests/day • Request-based billing • OAuth |

**Smart Delegation Triggers:**

- **Context-heavy tasks** (>5 files, >50k tokens) → `@agent-gemini-handler`
- **Tool-intensive workflows** (>100 operations, batch processing) → `@agent-qwen-handler`
- **Automatic fallback** to direct Claude Code execution on agent limits

## Todo Orchestration

The `/todo-build` command executes complete build workflows using intelligent sub-agent coordination with quality gates (Claude Code and OpenCode).

### Usage

```bash
/todo-build <IMPLEMENTATION_PLAN_PATH> [--prototype] [--parallel] [--max-retries=3]
```

### Workflow Orchestration Logic

The system follows a comprehensive orchestration workflow:

1. **Initial Setup** - Parse implementation plan and create task registry
2. **Main Orchestration Loop** - Execute continuous task processing through all phases until all tasks completed
3. **Task Selection** - Get next highest priority pending task in current phase
4. **Validation** - Validate technical approach with appropriate quality expectations
5. **Implementation** - Implement feature and check for runtime errors
6. **Quality Verification** - Execute dynamic quality gates based on tech stack
7. **Commit** - Attempt to commit changes with proper error handling
8. **Failure Escalation** - Escalate to problem-escalation agent after 3 failures

### Key Features

- **Continuous Orchestration**: Single command runs entire workflow to completion
- **Dynamic Quality Gates**: Adapts to project tech stack automatically
- **Prototype Mode Support**: Automatic test skipping with --prototype flag
- **Intelligent Failure Handling**: 3 failures → problem-escalation → 2 attempts → human escalation
- **State Persistence**: Progress tracked throughout execution
- **Phase Testing Plans**: Automatic generation of user testing plans after each phase

## Todo Worktree Implementation

The `/todo-build-worktree` command provides a structured workflow to transform vague todos into implemented features using git worktrees and subagent assignment (Claude Code and OpenCode).

### Workflow Phases

1. **INIT** - Check for task resume, initialize project description if needed
2. **SELECT** - Choose a todo from todos/todos.md and create a git worktree
3. **REFINE** - Research codebase and refine implementation plan
4. **IMPLEMENT** - Execute the implementation plan with validation
5. **COMMIT** - Create PR and clean up worktree

This approach supports task isolation, resumption, and clean commit history.
