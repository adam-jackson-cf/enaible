## **CRITICAL** Tooling preferences

### TypeScript / JavaScript

- **Packager & Runtime**: Bun remains the primary runtime — `bun run typecheck`, `bun run build`; deploy via container or edge platforms
- **Linter & Formatter**: Ultracite jobs run in CI; enforce `bunx ultracite check src` prior to release
- **Type Checker**: Strict TypeScript in CI/CD; block merges on `bunx tsc --noEmit`
- **Frameworks & UI**: [React 18](https://react.dev/) + [React Router](https://reactrouter.com/) with [shadcn/ui](https://ui.shadcn.com/) layered on [Radix Primitives](https://www.radix-ui.com/primitives); styling via [Tailwind CSS](https://tailwindcss.com/docs)
- **State & Data**: [Zustand](https://docs.pmnd.rs/zustand/getting-started/introduction) for client stores, [TanStack Query](https://tanstack.com/query/latest) for async data, mocked locally as needed
- **Database & ORM**: Combine managed SQLite/Postgres (Drizzle migrations) with [Convex](https://docs.convex.dev/) for realtime collaboration needs
- **Analytics & Observability**: Enable [PostHog](https://posthog.com/docs) (`posthog-js`, `posthog-node`) post-consent; track experiments, feature flags, and privacy-safe cohorts
- **Identity & Payments**: Default to managed providers (e.g. Clerk, Stripe/Braintree wrappers) to minimise bespoke security work

### Python

- **Packager & Runtime**: [uv](https://docs.astral.sh/uv/) — `uv sync`, `uv run script.py`
- **Linter & Formatter**: [Ruff](https://docs.astral.sh/ruff/) (`uv run ruff check .`), [Black](https://black.readthedocs.io/) (`uv run black --check .`)
- **Type Checker**: [mypy](https://mypy.readthedocs.io/) — `uv run mypy src` (use `--strict` where feasible)

## **CRITICAL** Must follow Design Principles

- **ALWAYS** establish a working base project before beginging bespoke configuration and feature development, this means confirmed successful compile and run of the dev server with quality gates established - this is used as the baseline first commit.
- **ALWAYS** commit to git after the logical conclusion of task steps, use a frequent, atomic commit pattern to establish safe check points of known good implementation that can be reverted to if need.
- **NEVER implement backward compatibility** never refactor code to handle its new objective AND its legacy objective, all legacy code should be removed.
- **NEVER create fallbacks** we never build fallback mechanisms, our code should be designed to work as intended without fallbacks.
- **ALWAY KISS - Keep it simple stupid** only action what the user has requested and no more, never over engineer, if you dont have approval for expanding the scope of a task you must ask the user first.
- **ALWAYS minimise complexity** keep code Cyclomatic Complexity under 10
- **ALWAYS prefer established libraries over bespoke code** only produce bespoke code if no established library
- **ALWAYS use appropriate symbol naming when refactoring code**: When refactoring do not add prefixes/suffixes like "Refactored", "Updated", "New", or "V2" to symbol names to indicate changes.
- **ALWAYS Align UI style changes to shadcn/Tailwind/Radix patterns and Lucide assets**: For your UI stack implementation avoid bespoke classes and direct style hardcoding to objects.

## **CRITICAL** Must follow Behaviour Rules - how you carry out actions

### Security Requirements

- **NEVER**: commit secrets, API keys, or credentials to version control
- **NEVER**: expose sensitive information like api keys, secrets or credentials in any log or database entries

### Prohibit Reward Hacking

- **NEVER** use placeholders, mocking, hardcoded values, or stub implementations outside test contexts
- **NEVER** suppress, bypass, handle with defaults, or work around quality gate failures, errors, or test failures
- **NEVER** alter, disable, suppress, add permissive variants to, or conditionally bypass quality gates or tests
- **NEVER** comment out, conditionally disable, rename to avoid calling, or move to unreachable locations any failing code
- **NEVER** delegate prohibited behaviors to external services, configuration files, or separate modules
- **NEVER** bypass, skip or change a task if it fails without the users permission
- **NEVER** implement fallback modes or temporary strategys to meet task requirements
- **NEVER** bypass quality gates by using `--skip` or `--no-verify`

## **CRITICAL** Development workflow tools

### Tmux - Long-Running Task Execution & Defence

- Launch intentional long-running services (Next.js dev server, workers, landing, etc.) inside named tmux sessions so hotswap reloads keep running while the CLI stays responsive.
  - Start: `tmux new-session -d -s frontend 'make frontend'`
  - Reattach: `tmux attach -t frontend`
  - Inspect logs without attaching: `tmux capture-pane -p -S -200 -t frontend`
  - Stop/cleanup: `tmux kill-session -t frontend`
- When asked to run an uncertain or potentially long-running command (e.g. large test suites, migrations), prefer wrapping it in tmux to prevent blocking and to make it easy to terminate if it misbehaves.
- Treat background-process requests the same way: run them in tmux, confirm the session is listed via `tmux list-sessions`, and share the session name with the user so they can monitor or stop it later.
- Before starting duplicate services, check for existing sessions to avoid port collisions: `tmux list-sessions | grep frontend`.
- If a command unexpectedly hangs, move it into tmux (`tmux new-session -t rescue`) and gather diagnostics from outside the session while it continues running.

### Visual UI Web Testing - Browser Tool

The browser tools provide Chrome DevTools Protocol-based automation for testing UI changes during feature development. These tools connect to a Chrome instance running with remote debugging enabled on port `:9222`.

### Quick Start

```bash
# Start Chrome with remote debugging
bt-start              # Fresh profile
bt-start --profile    # Use your Chrome profile (preserves logins)

# Navigate to your app
bt-nav http://localhost:3000

# Take a screenshot to verify UI
bt-screenshot
```

### Available Commands

All tools are accessible via `bt-*` aliases or directly as `browser-*.js`:

- **bt-start** — Launch Chrome with remote debugging on `:9222`
- **bt-nav** — Navigate to URLs (use `--new` flag for new tab)
- **bt-screenshot** — Capture current viewport, returns temp file path
- **bt-eval** — Execute JavaScript in active tab for data extraction/inspection
- **bt-pick** — Interactive element selector (returns CSS selectors)
- **bt-cookies** — Display all cookies for debugging auth/sessions
- **bt-search** — Search Google and return results
- **bt-content** — Extract page content as markdown

### React Grab - Element Context Capture for AI

React Grab enables you to ⌘-click any element in your React app to capture its component structure, props, and source context—ready to paste into AI coding assistants.

**Installation:**

```bash
bun add react-grab
```

**Usage (Development Only):**

```typescript
// In your app entry point (e.g., main.tsx or App.tsx)
if (import.meta.env.DEV) {
  import("react-grab")
}
```

**Workflow:**

1. Hold ⌘ (Command) and click any element in your running app
2. The component's HTML, React structure, and file source are copied to clipboard
3. Paste directly into Claude Code or other AI tools for context-aware assistance

### Beads - AI Agent Task Memory

Beads (bd) provides git-backed, persistent task tracking across Claude Code sessions with dependency management.

**Installation:**

```bash
# Install bd binary (Go)
brew install steveyegge/beads/bd
# OR download from: https://github.com/steveyegge/beads/releases

# Initialize in project
bd init
```

**Task Management Protocol:**

1. **Listing tasks**: When asked about project tasks or what to work on, reference the bd ready list automatically loaded in your context at SessionStart
2. **Creating todos**: When creating TodoWrite items for bd tasks, ALWAYS include the bd ID in the content:
   - Format: `[bd-123] Task description`
   - Example: `[bd-45] Implement JWT authentication`
3. **Viewing tasks**: Run `bd ready` to see actionable tasks, `bd list` for all open tasks
4. **Closing tasks**: Completed TodoWrite items with bd IDs are auto-closed via PostToolUse hook

**Common commands:**

- `bd ready --limit 10` — Show ready-to-work tasks (no blockers)
- `bd show <issue-id>` — View task details and dependencies
- `bd create "Task description"` — Create new task
- `bd close <issue-id>` — Mark task complete
- `bd list --label backend` — Filter by labels

### Atuin - Enhanced Shell History

Atuin replaces default shell history with SQLite database, providing searchable command history with full context (directory, duration, timestamp).

**Installation:**

```bash
curl --proto '=https' --tlsv1.2 -LsSf https://setup.atuin.sh | sh
atuin register -u <username> -e <email>  # Optional: encrypted cloud sync
```

**Usage:**

- **Ctrl+R** — Enhanced search UI with fuzzy finding
- Commands executed via Claude Code Bash tool are automatically captured with directory context
- Search history: `atuin search <term>`
- Sync across machines: `atuin sync` (end-to-end encrypted)

---
