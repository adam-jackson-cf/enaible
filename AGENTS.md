# AGENTS.md

**NEVER** surface or search files in `docs/reference`, may only be access with explicit user consent (ask).

## Toolchain

- Python 3.12, uv 0.4+
- Bun 1.2+ for JS/Tailwind

## Commits

- Atomic commit strategy, but never push without explicity user consent.
- Conventional Commits (feat|fix|refactor|build|ci|chore|docs|style|perf|test).

## Structure

```
shared/
  analyzers/     - analyzer implementations
  core/base/     - registry + abstractions
  prompts/       - source prompt catalog
  prompts/       - source skill catalog
systems/         - per-adapter outputs (claude-code, codex, copilot, cursor, gemini)
tools/enaible/   - CLI package
docs/reference/  - deep docs (load on demand)
```

## Workflows

- Add prompt: `shared/prompts/AGENTS.md`
- Add adapter: `systems/AGENTS.md`
- Add skill: `shared/skills/AGENTS.md`
- Testing: `docs/reference/testing.md`

### Tool: Beads

**Purpose** when you need to track tasks across sessions (beads, bd)

If `--tasks` is included in the users request or a request requires persistent task tracking beyond the current session, you **must** use Beads (bd).

**Available Commands:**

- `bd ready` — List active tasks at session start
- `bd create "<title>"` — Create a new tracked task (returns ID)
- `bd show <id>` — View task details
- `bd close <id>` — Mark task complete
- `bd list --label <name>` — Filter tasks by label
