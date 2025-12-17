# Bootstrap installers

| Platform | Script | Example |
| --- | --- | --- |
| macOS/Linux | `scripts/install.sh` | `curl -fsSL "https://raw.githubusercontent.com/adam-jackson-cf/enaible/main/scripts/install.sh?$(date +%s)" \| bash -s -- --systems codex,claude-code --scope user` |
| Windows (PowerShell 7+) | `scripts/install.ps1` | `pwsh -NoLogo -ExecutionPolicy Bypass -File scripts/install.ps1 -Systems codex,claude-code -Scope user` |

Both scripts clone (or update) the repo under `~/.enaible/sources/ai-assisted-workflows`, run `uv tool install --from <clone>/tools/enaible enaible`, and then call `enaible install <system> --scope user --mode sync` so user-level prompts stay current. Provide `--scope project --project /path/to/repo` (or `-Scope both -Project ...` in PowerShell) to hydrate a local checkout at the same time. Every run drops a short log in `~/.enaible/install-sessions/` so CI and humans can trace which settings were applied.

Common flags:

- `--systems codex,claude-code` / `-Systems codex,claude-code` — choose the systems to install (default: `codex,claude-code`).
- `--scope user|project|both` / `-Scope user|project|both` — select install scope; project/both modes require `--project PATH`.
- `--project /path/to/repo` / `-Project C:\repos\my-app` — explicit project root when targeting project scope.
- `--ref vX.Y.Z` / `-Ref vX.Y.Z` — pin to a specific git tag or branch.
- `--dry-run` / `-DryRun` — print actions without making changes (great for CI smoke tests).
