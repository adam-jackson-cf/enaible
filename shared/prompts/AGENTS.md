# Shared Prompt Authoring Guide

1. Author the source prompt in `shared/prompts/<name>.md`. Edit `docs/system/<system>/templates/` only when you need new frontmatter/layout tokens, it forms the layout for to use for the target system.

> **TEST 2025-12-22C:** Temporary marker to trigger the Copilot documentation workflow; remove after validation.

2. Run guards after any edit:

```bash
uv run --project tools/enaible enaible prompts lint
uv run --project tools/enaible enaible prompts render --prompt all --system all
uv run --project tools/enaible enaible prompts diff
```

3. Validate end-to-end: reinstall each affected system

```bash
uv run --project tools/enaible enaible install <system> --mode sync --scope project
```

Then exercise any analyzer calls via `enaible analyzers run ...` and keep artifacts under `.enaible/artifacts/<task>/<timestamp>/`.

4. Tests: add or update deterministic prompt fixtures in `shared/tests` when outputs are stable; otherwise rely on the drift checks above.

## Implementing a new shared prompt (end-to-end)

1. Establish the layout
   - Start from `docs/system/templates/prompt.md` to replicate, exactly, the shared prompt structure (Purpose → Variables → Instructions → Workflow → Output). Keep wording system-neutral so renderers can add frontmatter later.
   - For each target adapter, inspect the existing Jinja template under `docs/system/<system>/templates/*.j2` (for example `docs/system/codex/templates/prompt.md.j2`). If no suitable template exists, add one by copying the base prompt template guidance above and keeping token names aligned with the shared prompt variables.
2. Draft the shared prompt
   - Create `shared/prompts/<name>.md` matching the template outline. Declare every `@TOKEN` under `## Variables`, documenting positional/flag bindings (`@TOKEN = $N` or `@TOKEN = --flag`).
   - Avoid system-specific language or fallbacks; the rendered artifacts inherit system metadata from their adapter templates.
3. Map the prompt in the registry
   - Register the new prompt ID in `tools/enaible/src/enaible/prompts/catalog.py`. Reference the shared source path and list each target system with its `template`, `output_path`, and required `frontmatter`/`metadata`.
   - Reuse an existing `SystemPromptConfig` when possible; if the system needs new arguments or layout tokens, update its template folder first so the registry entry stays declarative.
4. Run render + drift guards
   - Execute the lint/render/diff trio listed above to regenerate `.build/rendered/<system>/...` outputs and catch token or layout issues early.
5. Validate adapters
   - Reinstall each affected system via `uv run --project tools/enaible enaible install <system> --mode sync --scope project` to confirm the prompt lands under the managed path with `<!-- generated: enaible -->` injected.
   - Exercise downstream workflows (e.g., `enaible analyzers run ...`) using the new prompt, capturing artifacts under `.enaible/artifacts/...` when needed.

## Format conventions (required)

- System-agnostic source: keep wording neutral; system wrappers add frontmatter during render.
- Variables section: use the standard bullet layout under `## Variables` with `### Required / ### Optional (derived from $ARGUMENTS) / ### Derived (internal)` and `@TOKEN = $N` / `@TOKEN = --flag` mappings. No `$` tokens elsewhere in the body.
- Token usage: all placeholders are `@TOKEN` and must be declared in Variables; lint enforces this.
- Managed sentinel: don’t add it manually—the renderer injects `<!-- generated: enaible -->` into system outputs.
- Use the exact template and pattern to mirror can be found here `docs/system/templates/prompt.md`.
