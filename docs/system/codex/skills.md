# Agent Skills for Codex

> Extend Codex CLI and IDE sessions with deterministic workflows packaged as Agent Skills. Guidance sourced from the official Codex Skills documentation plus the Agent Skills open standard.

## Feature availability

- **Codex CLI & IDE**: Full support for discovering, installing, and invoking skills. The CLI exposes `/skills` plus `$skill-name` shortcuts; the IDE mirrors those controls inside the command palette.
- **Codex Web & iOS**: Can use any skill that lives in the active repository or user scope, but they currently _cannot_ trigger explicit skill selection. Ask Codex to "use <skill>" and it will load it implicitly when the description matches.
- **Execution policy**: Skills run inside whichever sandbox mode Codex is configured for (see `docs/system/codex/sandbox.md`). Grant write/network access before invoking skills that rely on scripts or API calls.

## Skill anatomy & invocation

### Directory layout

```
my-skill/
  SKILL.md          # Required instructions + metadata
  scripts/          # Optional executable helpers
  references/       # Optional deep-dive docs
  assets/           # Optional templates or static data
```

- `SKILL.md` must contain YAML frontmatter with at least `name` and `description`, followed by Markdown instructions that stay under ~500 lines. Align the structure with the shared standard in `docs/skills.md` so skills render cleanly across adapters.
- Keep every dependency under the skill directory. Codex copies skills verbatim into `~/.codex/skills/<name>/`, so relative links must remain valid.

### Frontmatter template

```yaml
---
name: skill-name
description: Describe what the skill does and the triggers ("USE WHEN …").
metadata:
  short-description: Optional user-facing summary
---
```

Add `compatibility`, `allowed-tools`, or other metadata only when you need adapter-specific constraints.

### Invocation model

Codex loads each skill’s name + description at startup (progressive disclosure). A skill activates in two ways:

1. **Explicit invocation** – Run `/skills` or start typing `$` to select a skill from the popup. On the CLI you can also type `$skill-name arguments`. (Codex web/iOS do not expose explicit selection yet.)
2. **Implicit invocation** – Codex automatically loads a skill whose description matches your request.

Once invoked, Codex streams the full `SKILL.md` plus any referenced files into context.

## Skill scopes & precedence

Codex walks the following locations **from highest to lowest precedence**. A higher scope overrides lower scopes when folder names collide.

| Scope    | Location                                             | Typical use                                                                              |
| -------- | ---------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `REPO`   | `$CWD/.codex/skills`                                 | Skills that only apply to the exact folder where you launched Codex.                     |
| `REPO`   | `$CWD/../.codex/skills`                              | Shared skills one directory above the current working tree (useful for nested services). |
| `REPO`   | `$REPO_ROOT/.codex/skills`                           | Repository-wide defaults that any subfolder inherits.                                    |
| `USER`   | `$CODEX_HOME/skills` (defaults to `~/.codex/skills`) | Personal catalog that follows the user across repos.                                     |
| `ADMIN`  | `/etc/codex/skills`                                  | Machine or container-wide skills managed by administrators.                              |
| `SYSTEM` | Bundled with Codex                                   | Built-in skills such as `$skill-creator` and `$create-plan`.                             |

Restart Codex after changing files in any location so the new metadata loads.

## Creating Codex skills

1. **Bootstrap with `$skill-creator`**: Invoke `$skill-creator` inside Codex and describe the capability you need. Codex scaffolds the folder, writes `SKILL.md`, and suggests supporting assets.
2. **(Optional) Generate a plan first**: Install `$create-plan` with `$skill-installer create-plan`. Codex will draft a plan for the skill before writing files.
3. **Manual authoring**: Create `<location>/<skill-name>/SKILL.md` yourself when you need precise control. Follow the frontmatter template above and keep the body aligned with the workflow guidance in `docs/skills.md`.
4. **Reference assets**: Place scripts in `scripts/`, detailed walkthroughs in `references/`, and templates in `assets/`. Mention them with relative links.
5. **Validate**: Run `uv run --project tools/enaible enaible skills lint` to ensure the skill meets the shared spec, then restart Codex so it reloads the new metadata.

## Installing and sharing skills

- Use the built-in installer to fetch curated skills:

  ```
  $skill-installer linear
  $skill-installer create-plan
  ```

  Codex downloads from the official catalog at <https://github.com/openai/skills> (you can point the installer at other repositories as well).

- After installing or updating a skill, restart Codex (CLI or IDE) so the new folder is indexed.
- When sharing with teammates, commit `.codex/skills/<skill-name>/` into the repo or distribute a tarball that targets one of the supported scopes listed above.

## Using Enaible shared skills with Codex

1. **Add the skill to the catalog** – Register the new skill under `tools/enaible/src/enaible/skills/catalog.py` with a `codex` entry that points at `docs/system/codex/templates/skill.md.j2` and the appropriate `.build/rendered/codex/skills/<skill>/SKILL.md` output path.
2. **Author once in `shared/skills/`** – Follow `docs/skills.md` for the canonical `SKILL.md`. Keep any Codex-specific tweaks inside the Codex Jinja template.
3. **Render & diff** – `uv run --project tools/enaible enaible skills render --system codex --skill all`, then `uv run --project tools/enaible enaible skills diff` (or inspect `.build/rendered/codex/skills/…`) to confirm managed assets are up to date.
4. **Install Codex assets** – `uv run --project tools/enaible enaible install codex --mode sync --scope project` (for repositories) or `--scope user` (to sync `~/.codex/skills`). The installer copies rendered skills plus any managed rules/prompts.
5. **Validate in Codex** – Restart Codex, run `/skills`, and confirm the rendered skill appears with the correct description. Trigger a scenario from the skill body to ensure assets load correctly.

## Troubleshooting

| Symptom                                 | Fix                                                                                                                                                                                           |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Skill does not appear in `/skills`      | Confirm the folder lives under one of the supported locations, the `name` matches the folder, and YAML frontmatter is valid. Restart Codex after edits.                                       |
| Wrong version loads                     | Remember that higher-precedence scopes override lower ones. Remove or rename duplicates in `$CODEX_HOME/skills` if you need the repo version.                                                 |
| Scripts fail at runtime                 | Document prerequisites inside the skill body (Step 0) and ensure scripts reference relative paths only. Grant the necessary sandbox permissions before running.                               |
| `$skill-installer` errors when fetching | Verify the skill name exists in <https://github.com/openai/skills> or provide a full Git URL. Network-restricted sandboxes need `--sandbox danger-full-access` or equivalent to reach GitHub. |

## References

- OpenAI Developers — [Codex Agent Skills](https://developers.openai.com/codex/skills) (retrieved 2026-01-02)
- GitHub — [openai/skills](https://github.com/openai/skills)
- Agent Skills Open Standard — <https://agentskills.io/specification>
