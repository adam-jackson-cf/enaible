# Agent Orchestration

Enaible packages managed prompts and rulebooks that surface as commands or agents inside Codex, Claude Code, and OpenCode. This guide summarizes the catalog and explains how assets are generated.

## Architecture overview

- **Source of truth**: Prompt definitions live in `shared/prompts/*.md` and reference reusable templates in `docs/system/**/templates/`.
- **Renderer**: `uv run --project tools/enaible enaible prompts render` processes the catalog and emits managed Markdown containing the sentinel `<!-- generated: enaible -->`.
- **Installation**: `enaible install <system>` copies rendered prompts, helper docs, and rulebooks into `.codex/` or `.claude/` depending on scope.
- **Runtime**: When a developer triggers a managed command (e.g., `/analyze-security` inside Claude Code), the prompt instructs the CLI to call Enaible analyzers and store artifacts under `.enaible/`.

## Prompt catalog

| Prompt                 | Purpose                                                                                             | Systems            |
| ---------------------- | --------------------------------------------------------------------------------------------------- | ------------------ |
| `analyze-security`     | Runs Semgrep and Detect Secrets, performs gap analysis, and builds a remediation roadmap.           | Codex, Claude Code |
| `analyze-architecture` | Evaluates patterns, coupling, dependencies, and scalability to surface structural risks.            | Codex, Claude Code |
| `analyze-code-quality` | Combines complexity and duplication metrics to highlight maintainability hotspots.                  | Codex, Claude Code |
| `analyze-performance`  | Reviews backend, frontend, and SQL performance signals with actionable remediation steps.           | Codex, Claude Code |
| `analyze-root-cause`   | Guides incident investigations by correlating recent changes, error patterns, and execution traces. | Codex, Claude Code |
| `plan-refactor`        | Produces a phased refactor plan with rollback, metrics, and analyzer evidence.                      | Codex, Claude Code |
| `plan-solution`        | Generates conservative, balanced, and innovative solution options with comparative analysis.        | Codex, Claude Code |
| `get-codebase-primer`  | Creates onboarding primers covering architecture, commands, testing, and recent git history.        | Codex, Claude Code |

Managed prompts embed workflow instructions that call the Enaible CLI directly (e.g., `uv run --project tools/enaible enaible analyzers run ...`).

## Rulebooks & standards

Each system ships with a global rulebook merged into the developer’s environment during installation:

- Codex → `systems/codex/rules/global.codex.rules.md`
- Claude Code → `systems/claude-code/rules/global.claude.rules.md`

These files codify stack preferences (Bun, Ultracite, strict TypeScript), design principles (KISS, no fallbacks, SOLID adherence), and operational rules (tmux usage, no quality gate bypassing).

## Adding or updating prompts

1. Author or edit the source Markdown under `shared/prompts/`.
2. If new variables or formatting are required, adjust Jinja templates in `docs/system/<system>/templates/`.
3. Render prompts for all systems:

   ```bash
   uv run --project tools/enaible enaible prompts render --prompt all --system all
   ```

4. Inspect output with `enaible prompts diff` and commit regenerated files.
5. Run `enaible install <system>` to refresh managed assets in your local environment.

## Debugging agents

- Run `uv run --project tools/enaible enaible prompts lint` to validate token usage and variable mappings.
- Use `enaible prompts diff` to surface drift between rendered output and committed files.
- When prompts call analyzers, run them manually with `enaible analyzers run` to confirm configuration.
- Regenerate after modifying templates or prompt source files; managed files should never be hand-edited.
