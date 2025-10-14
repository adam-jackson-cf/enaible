# Task Completion Checklist

- Ensure lint (`bunx ultracite check src`, `uv run ruff check .`), format (`bunx ultracite fix src` if needed, `uv run black --check .`), and type checks (`bunx tsc --noEmit`, `uv run mypy src`) all pass.
- Run relevant tests (`bun run test`, `PYTHONPATH=shared pytest ...`) covering unit/integration scope touched.
- Verify cyclomatic complexity remains under thresholds (use Lizard if applicable) and no new duplication issues.
- Confirm no secrets or credentials introduced; avoid fallbacks/backward compatibility.
- Document decisions in `session-notes.md` with timestamps when required and ensure design principles maintained before committing.
