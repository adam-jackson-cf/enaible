# Session Notes — Ghostty default 3‑pane layout

Date: 2025-10-13

Changes applied to ensure Ghostty loads with a 3‑pane layout by default and to prevent the duplicate-splitting bug when launching Ghostty from within Ghostty.

## What changed

- Updated Ghostty config to avoid restoring prior window state (prevents re-splitting on next launch):
  - File: `/Users/adamjackson/Library/Application Support/com.mitchellh.ghostty/config`
  - Set `window-save-state = never` (was `always`).
- Kept `initial-command` but refined the layout script to target the newest Ghostty window explicitly and equalize splits at the end:
  - File: `/Users/adamjackson/.ghostty/claude-layout.sh`
  - Focuses the newest window (AXRaise/AXMain/AXFocused) before sending split keystrokes.
  - Performs: right split → run `lazygit` → focus left → create bottom-left split → focus top-left → equalize splits.
  - Guards with `GHOSTTY_LAYOUT_DONE` to avoid recursion.

Backups created:

- `/Users/adamjackson/Library/Application Support/com.mitchellh.ghostty/config.backup.20251013-143614`
- `/Users/adamjackson/.ghostty/claude-layout.sh.backup.20251013-143614`

## How it works

- Ghostty launches and runs `initial-command`, which calls the layout script once.
- The script selects the newest Ghostty window and issues the split sequence via Accessibility.
- `window-save-state = never` ensures startup is always the same 3‑pane layout instead of restoring prior sessions.

## Permissions

This uses `System Events` for UI scripting. If macOS prompts for Accessibility permissions, enable Ghostty (and/or your shell host) in:

System Settings → Privacy & Security → Accessibility.

## Rollback

- To restore previous behavior: set `window-save-state = always` in `/Users/adamjackson/Library/Application Support/com.mitchellh.ghostty/config` and, if desired, replace the layout script with the backup noted above.

## Optional follow-ups

- Add a shell alias to open a fresh 3‑pane window on demand:

  - Example alias in `~/.zshrc`:
    `alias g3='open -na Ghostty.app'`
  - Then hit `Cmd+N` to create a window and run `g3` for a separate instance if you want another default 3‑pane layout.

---

# Installer Notes — Codex CLI

Date: 2025-10-13

Fixed an installation path bug in the Codex installers where the Python framework was looked up at `systems/shared/` instead of the repository-level `shared/` directory.

What changed

- systems/codex/install.sh: in `copy_python_framework()`, changed the shared root resolution from `$(cd "$SCRIPT_DIR/.." && pwd)/shared` to `$(cd "$SCRIPT_DIR/../.." && pwd)/shared` (two levels up from `systems/codex/`).
- systems/codex/install.ps1: compute `$repoRoot` two levels up with `Split-Path (Split-Path $ScriptDir -Parent) -Parent` and set `$sharedRoot = Join-Path $repoRoot 'shared'`. Also improved the error message to print the full missing path.

Verification

- Ran `./systems/codex/install.sh --dry-run --verbose` and confirmed Phase [5/11] "Copy Python framework" now resolves correctly and proceeds. Dry-run succeeded end-to-end.

Impact

- Addresses the error: `Missing shared subtree: /.../systems/shared/core` observed during step [5/11] of the installer.

---

# CLI Migration Planning — Codex

## 2025-10-14T10:43Z

- Reviewed `.workspace/202510141138-cli-migration-cli-improvements/spec/spec.md` and current Codex prompt layout to shape the CLI migration ExecPlan.
- Authored `execplans/20251014-cli-migration-improvements.md` and synced a copy to `.workspace/202510141138-cli-migration-cli-improvements/plan/execplan.md` to drive follow-on implementation.

---

# visualdb PRD Draft — Codex

## 2025-10-14T15:14Z

- Completed discovery Q&A with stakeholder for the visualdb explorer board prototype.
- Authored `docs/prds/visualdb-prd.md` covering personas, MoSCoW scope, flows, UX requirements, and acceptance criteria with consistent feature/screen IDs.
- Noted that the prototype stores only target URLs plus layout metadata, excludes authentication, analytics, and accessibility commitments for this iteration.

---

# visualdb PRD Source Request — Codex

## 2025-10-14T15:16Z

- Captured the original `/plan-ux-prd` request content and stored it verbatim in `docs/prds/spec.md` for reference alongside the generated PRD.

---

# visualdb Embedding Research — Codex

## 2025-10-14T16:55Z

- Investigated whiteboard foundations (Excalidraw, tldraw, React Flow) and documented licensing plus extensibility trade-offs.
- Researched embed strategies for YouTube, X (Twitter) posts, and generic webpages, including iframe restrictions and fallback patterns.
- Summarized findings with citations in `docs/prds/tech-research.md`, outlining recommended architecture and next steps for the proof of concept.

# CLI Migration ExecPlan Refresh — Codex

## 2025-10-14T16:20Z

- Followed `create-execplan` v0.3 workflow with artifacts at `.workspace/202510141201-cli-migration-cli-improvements/*` and recorded Balanced plan favoring the Typer + uv approach.
- Authored `execplans/20251014-cli-migration-cli-improvements.md` and synced copy to `.workspace/202510141201-cli-migration-cli-improvements/plan/execplan.md`; added citations for Typer, uv, and Jinja2 usage.
- Captured comparative solution analysis in `.workspace/202510141201-cli-migration-cli-improvements/plan/plan-solution.md` to document why dual-mode wrappers were rejected.

## 2025-10-14T16:45Z

- Queried `codex --help` and `codex exec --help`, confirmed `gpt-5-codex` as the supported non-interactive model; smoketest run generated and removed `shared/tests/integration/fixtures/codex-cli-help-check.txt`.
- Relocated CLI migration spec/inspect artifacts to `shared/tests/integration/fixtures/cli-migration-cli-improvements/` and backed up the previous ExecPlan baseline.
- Authored `shared/tests/integration/fixtures/run-create-execplan.sh` to invoke `/create-execplan` via Codex, reusing the fixture invocation pattern; script now regenerates the plan file under fixtures for automated verification.

# Enaible ExecPlan Generation — Codex

## 2025-10-14T19:24Z

- Generated `execplans/20251014-enaible-cli-migration.md` from latest Enaible migration report/spec and copied to `tests/integration/fixtures/execplan/execplan.md` per /create-execplan request.
- Logged Typer + Jinja2 decisions and risks within the plan; no CLI code changes yet pending approval.

## 2025-10-14T19:45Z

- Created follow-up plan `execplans/20251014-enaible-cli-foundation.md` to capture refined scope for Enaible phase-one delivery and synced identical content to `tests/integration/fixtures/execplan/execplan.md` per latest /create-execplan run.
- Documented updated success criteria, risks, and quality gates reflecting CLI JSON normalization, template adapters, and CI drift enforcement expectations.

# Enaible ExecPlan Fixture Refresh — Codex

## 2025-10-14T20:21Z

- Regenerated `execplans/20251014-enaible-cli-migration.md` from updated spec/report fixtures and mirrored the content to `shared/tests/integration/fixtures/execplan/execplan.md` for integration coverage.
- Captured current acceptance criteria, quality gates, and risk mitigations ensuring migration stays aligned with no-fallback directive ahead of implementation work.

# Enaible Readiness Snapshot — Codex

## 2025-10-14T22:27Z

- Produced a two-paragraph readiness snapshot on analyzer centralization, prompt templating, and CI guardrails for the Enaible CLI migration at `shared/tests/integration/fixtures/scout/report.md`.

# Enaible Plan-Exec Fixture — Codex

## 2025-10-14T22:57Z

- Generated `shared/tests/integration/fixtures/plan-exec/execplan.md` from latest Enaible migration spec/report per `/plan-exec` request, aligning success criteria and concrete step checklist with Typer + Jinja2 architecture.
