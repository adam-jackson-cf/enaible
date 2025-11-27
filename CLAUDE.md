# Project: AI-Assisted Workflows

- Review and follow AGENTS.md

## When planning - use Beads (bd) for task tracking

**When to use Beads:**

- Multi-session work that needs to persist beyond current session
- Tracked deliverables the user wants visibility into
- Tasks with dependencies or blockers
- Work that should be discoverable in future sessions

**When NOT to use Beads (just use TodoWrite):**

- Single-session tasks
- Implementation steps within a larger tracked bd task
- Quick fixes or explorations

**Workflow:**

1. At session start: Check `bd ready` for pending tasks
2. When planning multi-session work: `bd create "Task description"` to get ID
3. In TodoWrite: Use `[bd-xxx] Step description` to link steps to bd task
4. On completion: Completed TodoWrite items with bd IDs auto-close via hook

**Commands:** `bd ready`, `bd show <id>`, `bd create "<title>"`, `bd close <id>`, `bd list --label <name>`

```

```
