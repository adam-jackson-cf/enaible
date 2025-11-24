# CLI Migration – High‑Level Discussion (enaible)

Date: 2025-10-13

## Context

- We maintain multiple systems (Claude Code, Codex) whose prompts are largely similar but differ in naming, frontmatter, and session/history handling.
- Duplication across `systems/*` increases rollout time and drift risk when adding or updating prompts/workflows.
- Shared prompts have been consolidated under `shared/prompts/*`.
- System wrapper templates have moved/been renamed to `docs/system/<system-name>/templates/*` (to be verified in the current tree; if missing, migrate existing templates accordingly).
- Some prompts currently execute Python analyzers by locating files in project/user install paths, which has proven brittle.

## Objectives

- Reduce duplication and drift across systems when introducing or updating prompts.
- Hide environment and script path details from end users.
- Provide a professional, versioned CLI that standardizes analyzer execution and prompt generation across systems.

## Agreed Direction (Summary)

- Introduce a first‑class CLI named `enaible` (Python, packaged and run via `uv`).
- Convert Python analyzer scripts into CLI subcommands so prompts call `enaible` instead of locating/running Python modules directly.
- Keep shared prompt bodies and render system‑specific wrappers via templates with a small, explicit adapter layer.
- Prefer established libraries (Typer/Click, Jinja2) and keep implementation simple and testable.

## Proposed Architecture

### CLI Surface (enaible)

- `enaible analyzers run <category:tool> --target PATH --json --out FILE [--max-files N] [--no-external]`
- `enaible analyzers list`
- `enaible prompts render -s <system|all> -p <id|all> -o <dir>`
- `enaible prompts validate|diff|sync`
- `enaible install <system>` (optional, supersedes brittle shell installers)
- `enaible doctor` (env checks, resolves analyzer availability)

Notes:

- Normalize analyzer outputs (JSON schema: tool, version, timestamps, findings[], stats, exit codes).
- Default artifacts directory: `.enaible/artifacts/<prompt>/<timestamp>/` (overrideable).

### Prompt Composition

- Source of truth for content: `shared/prompts/<prompt-id>.md` (system‑agnostic bodies).
- System templates (wrappers) live at `docs/system/<system-name>/templates/*.j2` and include:
  - System frontmatter/metadata (Claude Code, OpenCode, Codex).
  - Small system notes (session/history guidance, tool permission hints).
- Includes/snippets: `shared/prompts/includes/*.j2` for reusable fragments (e.g., session history section).
- System adapters provide data for templates (paths, config files, frontmatter, session notes).

### Remove Path‑Probing From Prompts

- Replace “locate scripts, compute PYTHONPATH, then run python -m …” blocks with a single `enaible analyzers run …` call.
- The CLI encapsulates environment resolution and module discovery; prompts become thinner and more portable across systems.

## Repository Layout (target)

- `shared/prompts/` – shared bodies (`*.md`) and `includes/*.j2`
- `docs/system/<system>/templates/` – system wrapper templates (`*.j2`)
- `tools/enaible/` – CLI package (Python, Typer/Click, Jinja2), published via `uv`
- `systems/*` – rendered outputs (managed artifacts) or synced targets

## Tooling & Packaging

- Package manager/runtime: `uv`
  - `uv sync`, `uv run enaible …`, `uv pip install --editable .` for local dev
- CLI libs: Python + Typer/Click, Jinja2; keep dependencies minimal
- Distribution: recommend `pipx` or `uv tool install` for end users

## Migration Plan (Phased)

1. Scaffold `enaible` CLI skeleton

- Commands: `analyzers run|list`, `prompts render|validate|diff|sync`, `doctor`.
- Wrap existing analyzers without changing their internal contracts.

2. Templating upgrade

- Move/confirm templates under `docs/system/<system>/templates/`.
- Add system adapters and shared `includes/`.
- Render two pilot prompts end‑to‑end (recommended: `analyze-security`, `get-primer`).

3. Prompt refactors

- Replace path‑discovery paragraphs with `enaible` invocations in bodies.
- Regenerate system variants; confirm frontmatter differences are adapter‑driven.

4. CI guardrails

- `enaible prompts render --systems all --prompts all --out ._generated`.
- `enaible prompts diff` must be empty; fail build if drift detected.

5. Optional installers

- Implement `enaible install <system>` to replace shell installers.

## Risks / Considerations

- Template paths: verify `docs/system/<system>/templates/*` exists; reconcile any legacy locations.
- Analyzer contracts: stabilize JSON schema and exit codes before broad rollout.
- Backward compatibility: prompts should not attempt legacy path probing once converted (avoid dual modes).
- Performance: ensure `uv run enaible …` is fast for frequent prompt workflows.

## Open Decisions

- Keep Codex prompts frontmatter‑free or normalize minimal metadata across systems?
- Final artifact directory convention (`.enaible/` vs project‑specific)?
- Scope of `install <system>` in v1 (commands only vs full rules/agents/assets)?

## Next Actions

- Re‑index current repo for new prompt/template locations and confirm `docs/system/<system>/templates/*` presence.
- Scaffold `tools/enaible/` (Typer/Click + Jinja2) managed by `uv`.
- Implement `analyzers run` wrapping existing analyzers; define normalized JSON schema and exit codes.
- Add system adapters and migrate two pilot prompts.
- Wire CI drift check for rendered outputs.

---

Authoring notes from discussion:

- Prefer established libraries; minimize complexity.
- Rename CLI to `enaible`; avoid multi‑mode fallbacks in prompts—let the CLI own environment and discovery.

## Decisions (Resolved 2025-10-13)

1. Codex frontmatter

- Keep Codex outputs frontmatter‑free by default to match its conventions. The Codex adapter emits no YAML frontmatter; optional metadata may appear only as an HTML comment for internal tooling.

2. Artifact directory convention

- Use `.enaible/` at the repository/project root for local artifacts (e.g., `.enaible/artifacts/<prompt>/<timestamp>/…`). This is system‑agnostic and avoids overloading `.claude/` or `.codex/`.

3. Scope of `enaible install <system>` v1

- Full system assets in v1. Included objects: commands/prompts, agents, rules, settings/configs, and any plugin assets present under `systems/<system>/`.
- Modes: `fresh|merge|update|sync` with dry‑run and backup flags. Behavior mirrors existing shell installers but centralized in the CLI.

4. Technology choices

- Python CLI, packaged and executed with `uv`. Internal components use Typer (or Click) + Jinja2. Keep dependencies lean.

5. Template locations

- Standardize on `docs/system/<system>/templates/*.j2` for wrappers. If the path doesn’t exist yet, `enaible prompts migrate-templates` will create it and relocate legacy templates.

6. One‑off system‑specific prompts

- Supported. Authors can create prompts directly under `systems/<system>/(commands|command|prompts)/` without going through shared bodies.
- Unmanaged vs managed:
  - Files without the header `<!-- generated: enaible -->` are unmanaged (author‑owned) and never overwritten by render/sync.
  - Generated files include that header and can be safely re‑rendered.
- Install behavior: `enaible install <system>` copies both managed and unmanaged prompts. Unmanaged files are preserved on subsequent updates unless `--fresh` is used.

7. Install/copy destinations and precedence

- Destinations by adapter:
  - User scope: `~/.claude`, `~/.codex`.
  - Project scope: `./.claude`, `./.codex` beneath a provided target path.
- Precedence & safety:
  - `merge` updates managed files, preserves unmanaged and user‑modified files.
  - `update` overwrites managed files when fingerprints match prior generated state; warns otherwise.
  - `fresh` replaces everything after confirmation/backups.
  - `sync` aligns destination with current rendered state for managed files; never deletes unmanaged by default.

8. Prompt/analyzer interaction

- Prompts must call `enaible analyzers run …`; legacy path‑probing blocks are removed to avoid dual modes.

9. CI enforcement

- CI renders all prompts and fails if `enaible prompts diff` detects drift in managed files. Unmanaged files are excluded from drift enforcement.
