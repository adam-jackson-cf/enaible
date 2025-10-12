# 2025-10-12 Codex Installer UX alignment

- Matched Codex bash installer UX with Claude's phased flow and removed redundant scripts-root prompt; scripts now default under the selected Codex home with optional override flag.
- Mirrored the experience for PowerShell, including the new Node tooling step; unable to run pwsh locally to verify execution.
- Audited OpenCode installers and confirmed they already pin scripts under the install root with phased messaging, so no changes needed; CI workflows for Codex/OpenCode PS installers remain compatible with the updated interfaces.
