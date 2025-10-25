Unified Variables Format

- Use @TOKENS everywhere (no $-prefixed tokens in prose).
- Structure every prompt’s variables under “## Variables” using three subsections:

### Required

- @NAME = $1 — human description
- @OTHER = $2 — ... (continue in order when multiple are required)

### Optional (derived from $ARGUMENTS)

- @FLAG_NAME = --flag-name — human description
- @LIST = --item [repeatable]

### Derived (internal)

- @CONST = <value or note>

Rules

- Only Required map to positional indices $N.
- Optionals always map to explicit --flags (never positional).
- The renderer derives argument hints from these mappings.
- System renders omit any empty subsection to reduce tokens.
- In prose and code examples, reference @TOKENS; only show $N/--flag in the Variables mappings or real shell examples.

Lint

- Run `uv run --project tools/enaible enaible prompts lint` to validate:
  - No $VAR in prose (outside code blocks/mappings)
  - All @TOKENS used in body are declared in Variables
  - Required map to $N; Optional map to --flag
