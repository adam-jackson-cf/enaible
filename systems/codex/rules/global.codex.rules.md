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
