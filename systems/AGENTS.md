# System Adapter Playbook

Use this checklist whenever you add support for a brand-new target system (new IDE, agent runtime, etc.) so rendered prompts remain deterministic and installer sync stays safe.

> **TEST 2025-12-22D:** Temporary line to trigger Copilot doc workflow validation; remove after confirming automation.

1. **Scaffold folders**
   - Mirror the existing adapter footprint by creating `docs/system/<system>/templates/` for Jinja templates plus system notes, and `systems/<system>/` for managed outputs.
   - Rendered files land under `.build/rendered/<system>/...`; keep that structure parallel to claude-code/codex/cursor so tooling can diff reliably.
2. **Author templates**
   - Base every template on `docs/system/templates/prompt.md` (Purpose, Variables, Instructions, Workflow, Output). Name templates `*.j2` (e.g., `docs/system/<system>/templates/prompt.md.j2`) and only include layout/frontmatter—not prompt copy.
   - If the adapter produces multiple asset types (commands, workflows, rules), add separate `.j2` files sharing the same token names expected by shared prompts.
3. **Register in the prompt catalog**
   - Update `tools/enaible/src/enaible/prompts/catalog.py` by appending a `SystemPromptConfig` entry for the new system inside each prompt definition you want exposed.
   - Provide the template path, `.build/rendered/...` output path, and any required `frontmatter`/`metadata`. Keep catalog entries declarative—add new template tokens before wiring them in the registry.
4. **Hook into the installer**
   - Edit `tools/enaible/src/enaible/commands/install.py` (e.g., `SYSTEM_RULES`, `ALWAYS_MANAGED_PREFIXES`) so `enaible install <system>` knows which files to sync and protect.
   - Copy any additional bootstrap assets from `systems/<system>/` during install; avoid inline hacks or fallbacks.
5. **Run render + drift guards**
   - Execute the standard guard trio:
     ```bash
     uv run --project tools/enaible enaible prompts lint
     uv run --project tools/enaible enaible prompts render --prompt all --system all
     uv run --project tools/enaible enaible prompts diff
     ```
   - Confirm `.build/rendered/<system>/...` contains the new outputs and that `<!-- generated: enaible -->` is injected automatically.
6. **Validate installs**
   - Smoke both scopes:
     ```bash
     uv run --project tools/enaible enaible install <system> --scope project --mode sync
     uv run --project tools/enaible enaible install <system> --scope user --mode sync
     ```
   - Open a rendered prompt/command to verify frontmatter, variable bindings, and workflow steps survive intact. Capture analyzer dry runs under `.enaible/artifacts/<task>/<timestamp>/` when applicable.
7. **Document system quirks**
   - If the adapter needs extra env setup or UX notes, add a short README snippet under `docs/system/<system>/` so future contributors inherit the constraints.
   - Keep guidance aligned with repo-wide UI/guardrail conventions (shadcn/Tailwind/Radix/Lucide, no fallbacks, no legacy compatibility).
