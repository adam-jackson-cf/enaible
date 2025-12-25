# Shared Skill Authoring Guide

1. Create a skill directory under `shared/skills/<skill-name>/` with a required `SKILL.md`.

2. Keep `SKILL.md` compliant with `docs/skills.md`:
   - YAML frontmatter with `name` and `description`.
   - `name` must match the folder name.
   - Keep the body under 500 lines when possible.

3. Add supporting files in `resources/`, `scripts/`, or `assets/` as needed.

4. Render skills for supported systems:

```bash
uv run --project tools/enaible enaible skills render --skill all --system all
```

5. Validate rendered outputs:

```bash
uv run --project tools/enaible enaible skills validate --skill all --system all
```

6. Install into a project or user scope for verification:

```bash
uv run --project tools/enaible enaible install claude-code --mode sync --scope project
uv run --project tools/enaible enaible install codex --mode sync --scope project
```
