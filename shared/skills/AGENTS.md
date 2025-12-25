# Shared Skill Authoring Guide

1. Author the skill source in `shared/skills/<skill-name>/SKILL.md`. Edit `docs/system/<system>/templates/` only when you need new layout tokens; templates define the rendered wrapper for each system.

2. Run guards after any edit:

```bash
uv run --project tools/enaible enaible skills lint
uv run --project tools/enaible enaible skills render --skill all --system all
uv run --project tools/enaible enaible skills diff
```

3. Validate end-to-end: reinstall each affected system.

```bash
uv run --project tools/enaible enaible install claude-code --mode sync --scope project
uv run --project tools/enaible enaible install codex --mode sync --scope user
```

4. Tests: add or update deterministic skill fixtures in `shared/tests` when outputs are stable; otherwise rely on the drift checks above.

## Implementing a new shared skill (end-to-end)

1. Establish the layout
   - Start from `docs/skills.md` for frontmatter rules and conventions.
   - For each target adapter, inspect the existing Jinja template under `docs/system/<system>/templates/*.j2` (for example `docs/system/codex/templates/skill.md.j2`). If no suitable template exists, add one by copying the base skill template and keeping token names aligned with the shared skill frontmatter.
2. Draft the shared skill
   - Create `shared/skills/<skill-name>/SKILL.md` with required frontmatter fields and a concise body. Keep long guidance in `resources/` via progressive disclosure.
   - Avoid system-specific language; rendered artifacts inherit system metadata from adapter templates.
3. Add supporting assets
   - Put executable helpers in `scripts/` and references in `resources/`. Keep scripts self-contained and document required environment setup in the resources.
4. Map the skill in the registry
   - Register the new skill ID in `tools/enaible/src/enaible/skills/catalog.py`. Reference the shared source path and list each target system with its `template` and `output_path`.
5. Run render + drift guards
   - Execute the lint/render/diff trio listed above to regenerate `.build/rendered/<system>/...` outputs and catch metadata or layout issues early.
6. Validate adapters
   - Reinstall each affected system to confirm the skill lands under the managed path with `<!-- generated: enaible -->` injected.

## Format conventions (required)

- System-agnostic source: keep wording neutral; system wrappers add frontmatter during render.
- Frontmatter: must satisfy `docs/skills.md` rules; `name` must match the folder name.
- Managed sentinel: don’t add it manually—the renderer injects `<!-- generated: enaible -->` into system outputs.
- Tool markers: use `@ASK_USER_CONFIRMATION` in skill resources where user approval is required; renderers replace it per system.
- Keep `SKILL.md` concise; use `resources/` for detailed workflows and `scripts/` for deterministic helpers.
