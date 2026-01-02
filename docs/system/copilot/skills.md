# Agent Skills for GitHub Copilot

> Teach Copilot Chat, the Copilot coding agent, and the Copilot CLI how to run specialized workflows using the Agent Skills open standard.

## Feature availability

GitHub documents Agent Skills in [About Agent Skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills). Today they are available to:

- **Copilot coding agent** (PR automation worker)
- **Copilot CLI** (public preview with data protection)
- **Copilot Chat agent mode** inside VS Code Insiders (stable VS Code support is rolling out)

Skills currently load at the **repository scope only**. Organization- and enterprise-level skill catalogs are planned but not generally available yet.

## Directory layout and scope

Repository skills live under `.github/skills/<skill-name>/`:

```
.github/
└── skills/
    └── codify-pr-reviews/
        ├── SKILL.md
        ├── references/
        │   └── stack-analysis-workflow.md
        ├── scripts/
        │   └── fetch_comments.py
        └── assets/
            └── template.json
```

Copilot also reads Agent Skills from `.claude/skills/` (personal or project). We continue to install shared skills into `.github/skills/` so Copilot and other Agent-Skills-compliant runtimes stay in sync.

**Skill directory naming**:

- Lowercase letters, digits, single hyphens only (must match the `name` frontmatter field)
- Exactly one `SKILL.md` per directory (required)
- Optional: `references/`, `scripts/`, `assets/`, `config/`

## `SKILL.md` requirements

Copilot follows the same Agent Skills open standard we already use for Claude Code and Codex:

- YAML frontmatter with at least `name` and `description`
  - `description` must include a clear “USE WHEN …” trigger so Copilot knows when to load the skill
  - `allowed-tools` is accepted but currently ignored by Copilot (only Claude Code enforces tool gating). Still reference tools via the shared tokens (`@BASH`, `@READ`, etc.) so other systems render correctly.
- Markdown body organized per [`docs/skills.md`](../skills.md)
  - Title block, bullet list of use cases
  - Optional “Need to…?” quick reference table
  - `## Workflow` with numbered `Step N` sections; embed detailed instructions inside `references/` files for progressive disclosure
  - Keep the main file under ~500 lines
- Supporting files live alongside `SKILL.md` and are referenced with relative links (for example, `references/fetching-workflow.md`)

## Creating a Copilot skill

1. **Create the directory**: `mkdir -p .github/skills/<skill-name>`
2. **Author `SKILL.md`** using the shared template (frontmatter, mission paragraph, workflow). Follow the open standard described in `docs/skills.md`.
3. **Add supporting material** (`references/`, `scripts/`, `assets/`) when the workflow requires detailed steps, forms, or deterministic helpers.
4. **Commit and share**: Skill directories are versioned with your repo; teammates pick them up on the next pull.
5. **Test**: In Copilot Chat or the coding agent, describe a scenario covered by your skill. Copilot will automatically inject the skill content when the `description` matches the request. Because skills are model-invoked, you do not call them manually.

## Using shared skills via Enaible

To expose a shared skill to Copilot:

1. **Add the system to the skill catalog** (`tools/enaible/src/enaible/skills/catalog.py`) with a `copilot` entry that points to `docs/system/copilot/templates/skill.md.j2` and renders into `.build/rendered/copilot/skills/<skill>/SKILL.md`.
2. **Provide a template**: `docs/system/copilot/templates/skill.md.j2` simply emits the shared frontmatter/body plus the managed sentinel. Keep templates presentation-free so shared copy remains system-agnostic.
3. **Render & diff**: `uv run --project tools/enaible enaible skills render --system copilot --skill all` followed by `enaible skills diff` to confirm `.build/rendered/copilot/skills` is up to date.
4. **Install**: `enaible install copilot --scope project --mode sync` copies generated skills into `.github/skills/…`. For VS Code user scope, the installer resolves the per-user Copilot directory automatically.
5. **Validate**: Reload Copilot Chat or restart VS Code. Ask “List available skills” to confirm Copilot can see the new entries, then run a scenario from the skill description.

These steps parallel the workflow in [`shared/skills/AGENTS.md`](../../shared/skills/AGENTS.md): author once in `shared/skills/`, render via templates into each adapter, and rely on the installer to publish into managed directories.

## Troubleshooting

| Symptom                   | Fix                                                                                                                                                                             |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Skill never appears       | Confirm the description includes concrete triggers (“USE WHEN …”), file lives under `.github/skills/<name>/SKILL.md`, and YAML syntax is valid.                                 |
| Copilot loads wrong skill | Make descriptions more specific so requests disambiguate similar capabilities.                                                                                                  |
| Scripts fail              | Document prerequisites inside the skill body (Step 0) and reference deterministic helpers in `scripts/`. Copilot can execute scripts residing alongside the skill once invoked. |
| Need to restrict tools    | Copilot currently ignores `allowed-tools`. Leave the field in place for cross-system interoperability, but assume Copilot can access its default tool bundles.                  |

## References

- GitHub Docs — [About Agent Skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)
- Agent Skills Open Standard — <https://github.com/agentskills/agentskills>
