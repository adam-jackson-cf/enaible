# 2025-10-12 Codex Installer UX alignment

- Matched Codex bash installer UX with Claude's phased flow and removed redundant scripts-root prompt; scripts now default under the selected Codex home with optional override flag.
- Mirrored the experience for PowerShell, including the new Node tooling step; unable to run pwsh locally to verify execution.
- Audited OpenCode installers and confirmed they already pin scripts under the install root with phased messaging, so no changes needed; CI workflows for Codex/OpenCode PS installers remain compatible with the updated interfaces.
- Hardened Codex installers to replace any existing AI-Assisted Workflows section in AGENTS.md instead of blindly appending, preventing duplicate global rules during merge/update modes.

# 2025-10-12 Code Quality Assessment

- Ran `core.cli.run_analyzer` with the `quality:lizard` analyzer via global `.codex` scripts to baseline complexity findings (182 total, 34 high) and began triaging hotspots in `shared/utils` and `shared/generators` for follow-up refactors.
