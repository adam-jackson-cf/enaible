# todo-inspect-codebase v0.1

**Purpose**

- Explore the current project and produce a comprehensive, evidence-backed report that answers the provided `$USER_PROMPT`.

## Variables

- `$USER_PROMPT` ← first positional argument (required)
- `$TARGET_PATH` ← second positional (default `.`)
- `$DAYS` ← `--days` (default `20`)
- `$EXCLUDE_GLOBS` ← `--exclude` CSV (optional; e.g., `node_modules,dist,.git,.cache`)
- `$ARGUMENTS` ← raw argument string

## Instructions

- Read-only analysis; do not modify files, run builds, or install tools.
- Do not invoke external analyzer scripts; rely on repository contents plus lightweight file listing, search, and git inspection.
- Support every claim with specific evidence: file path and, when useful, line number and the command used.
- Do not reveal secrets; if detected, report only location and nature.
- Default to the current project (`.`) when `$TARGET_PATH` is not provided; respect `$EXCLUDE_GLOBS`.
- Use resolved variables in all commands (e.g., `rg -n --hidden <pattern> "$TARGET_PATH" ${EXCLUDE_ARG}`).

## Workflow

1. Scope & Setup

   - Resolve `$TARGET_PATH` (default `.`); capture working directory. Apply `$EXCLUDE_GLOBS` to all listings/searches.
   - Quick inventory: languages, package managers, lockfiles, top-level directories, and primary manifests/configs.
   - Illustrative commands (adjust for `--exclude`):
     - `ls -1A "$TARGET_PATH"`
     - `rg --files --hidden ${EXCLUDE_ARG}` where `$EXCLUDE_ARG` expands to combined `--glob '!{...}'`
     - Inspect key manifests selectively: `cat package.json`, `cat tsconfig.json`, `cat pyproject.toml`, `cat tailwind.config.*`, `cat drizzle.config.*`
     - Note binary lockfiles by presence only (e.g., `bun.lockb`); do not dump contents.

2. Repository Survey & Index

   - Identify entry points, apps/services, CLIs, servers, and routing surfaces.
   - Locate key configurations and framework signals (examples):
     - TypeScript: `tsconfig.json`, `tsconfig.*.json`
     - Tailwind: `tailwind.config.(ts|js|cjs)`; PostCSS config
     - UI libs: `@radix-ui/*`, `shadcn/ui`
     - State/Data: `zustand`, `@tanstack/(react-query|query-core)`
     - ORM/DB: `drizzle-orm`, `better-sqlite3`, `drizzle.config.(ts|js)`
     - Analytics: `posthog-js`, `posthog-node` (note consent gating if present)
     - Identity/Payments: `clerk`, `@clerk/*`, `stripe`, `braintree`, `better-auth`
     - Infra/CI: `Dockerfile*`, `docker-compose*`, `.github/workflows/*`
   - Illustrative queries (apply `$EXCLUDE_GLOBS` and `$TARGET_PATH`):
     - `rg -n --hidden "from\s+\"hono\"|require\(\"hono\"\)" "$TARGET_PATH" ${EXCLUDE_ARG}`
     - `rg -n --hidden "@tanstack/(react-router|router)|react-router-dom|routeTree\\.gen\\.ts" "$TARGET_PATH" ${EXCLUDE_ARG}`
     - `rg -n --hidden "from\\s+\"zustand\"|create\(.*from\\s+\"zustand\"" "$TARGET_PATH" ${EXCLUDE_ARG}`
     - `rg -n --hidden "@tanstack/(react-query|query-core)" "$TARGET_PATH" ${EXCLUDE_ARG}`
     - `rg -n --hidden "drizzle|drizzle-orm|better-sqlite3|drizzle\\.config\\.(ts|js)" "$TARGET_PATH" ${EXCLUDE_ARG}`
     - `rg -n --hidden "posthog-js|posthog-node" "$TARGET_PATH" ${EXCLUDE_ARG}`
     - `rg -n --hidden "@radix-ui/react-|shadcn/ui|tailwind\\.config\\.(ts|js|cjs)" "$TARGET_PATH" ${EXCLUDE_ARG}`
     - `rg -n --hidden "clerk|@clerk|stripe|braintree|better-auth" "$TARGET_PATH" ${EXCLUDE_ARG}`
     - `ls -1A "$TARGET_PATH/.github/workflows" 2>/dev/null`

3. Focused Deep‑Dives (LLM, file‑driven)

   - Architecture: layering, boundaries, composition roots, routing conventions; identify composition/DI points.
   - Quality: code organization, complexity hotspots (by inspection), duplication hints, code conventions.
   - Performance: obvious hotspots (N+1 risks, large payloads, tight loops, missing memoization, render thrash).
   - Security: secrets exposure patterns, authN/authZ flows, unsafe APIs or configurations.
   - Data & State: DB/ORM usage (Drizzle, SQLite), schema/migrations layout, client state (Zustand), fetch/revalidation (TanStack Query) and cache policies.
   - Visual Design & UX: component libraries (shadcn/ui, Radix), Tailwind tokens/themes, design tokens, accessibility cues (Radix patterns, ARIA), routing/loader UX, common UI primitives and patterns.
   - Tests: test layout (unit/integration/e2e), frameworks, fixtures/mocks, any coverage indicators.
   - CI/CD & Tooling: pipelines, lint/type/test commands, release/versioning, pre-commit hooks.
   - Observability: logging, metrics, feature flags, analytics initialization and consent persistence.
   - For each area, extract concrete findings and include file:line evidence and the command used to find it.

4. Git Mining (last `$DAYS`)

   - Snapshot: `git -C "$TARGET_PATH" status --short`
   - History window: `git -C "$TARGET_PATH" log --since="${DAYS} days ago" --date=iso --stat --pretty=oneline`
   - Contributors: `git -C "$TARGET_PATH" shortlog -sn --since="${DAYS} days ago"`
   - Churn hotspots: aggregate top changed files/folders; note renames and turning points.

5. Synthesis
   - Begin with a concise, direct answer to `$USER_PROMPT`.
   - Summarize key facts tied to evidence. Capture unknowns only if blocking; aim for zero open questions.

## Output

- Markdown report with these sections:
  - Title and One‑Line Answer (to `$USER_PROMPT`)
  - Repository Overview (layout, languages, manifests)
  - Architecture
  - Quality
  - Performance
  - Security
  - Data & State
  - Visual Design & UX
  - Tests
  - CI/CD & Tooling
  - Observability
  - Git Insights (20‑day default window)
  - Evidence Ledger (file:line with short note and source command)
  - Open Questions (expected empty; include only if blocking)

## Examples

- `/todo-inspect-codebase "Map data flow for refunds"`
- `/todo-inspect-codebase "Identify auth risks in API" . --exclude node_modules,dist`
- `/todo-inspect-codebase "Assess React route performance" web/`

$ARGUMENTS
