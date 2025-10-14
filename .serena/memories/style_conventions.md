# Style and Conventions

- Follow project rules in `systems/*/rules/`; TypeScript uses strict mode, Bun runtime, React + Tailwind + shadcn/ui, Zustand, TanStack Query, Drizzle ORM.
- Python uses uv for env management, Ruff + Black for lint/format, mypy (prefer strict) for typing.
- Design principles: strict SOLID adherence, DRY enforcement, minimize complexity (cyclomatic < 10), no fallbacks or backward compatibility; prefer established libraries.
- Security: never commit secrets or expose credentials; avoid placeholders/mock implementations outside tests.
- Code reading discipline: read entire files/classes before modifying; never suppress tests or quality gates.
