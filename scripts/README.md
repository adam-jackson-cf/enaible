# CLI install TLS helper

## Why this exists

The Enaible CLI installer uses `uv` to download Astral's standalone CPython builds from GitHub before it renders managed prompts. On corporate machines the shell profile often overrides `SSL_CERT_FILE`, `REQUESTS_CA_BUNDLE`, and `UV_HTTP_CA_BUNDLE` so that every HTTPS client trusts an internal TLS interception proxy. When those variables point at the internal root **only**, `uv` (via rustls) no longer trusts DigiCert, which is the public certificate authority used by GitHub/Astral. The download is rejected with `invalid peer certificate: UnknownIssuer` even though the workstation can reach GitHub in a browser.

## What the script does

`scripts/setup-uv-ca.sh` (macOS/Linux) and `scripts/setup-uv-ca.ps1` (Windows) combine the stock system trust store with your corporate root certificate. The merged PEM keeps the corporate inspector while restoring trust in public CAs, so `uv run --project tools/enaible …` can grab Astral's CPython builds without disabling any corporate controls.

Steps performed:

1. Detect the corporate CA from `--corp-ca PATH` (preferred) or the existing `SSL_CERT_FILE` export.
2. Locate the default system CA file via Python's `ssl.get_default_verify_paths()` (falls back to platform defaults).
3. Concatenate the two files into `~/.config/claude/corp-ca-bundle.pem` (or the path you pass with `--output` / `-Output`).
4. Print the `SSL_CERT_FILE` instructions so the new bundle becomes the default for future shells.

## How to use it

macOS/Linux:

```bash
./scripts/setup-uv-ca.sh --corp-ca ~/.config/claude/corp-ca.pem --output ~/.config/claude/corp-ca-bundle.pem
# or rely on $SSL_CERT_FILE if it's already set
./scripts/setup-uv-ca.sh
```

Windows (PowerShell 7+):

```powershell
pwsh -File scripts/setup-uv-ca.ps1 -CorpCA C:\certs\corp-root.pem -Output $env:USERPROFILE\.config\claude\corp-ca-bundle.pem
# or rely on $Env:SSL_CERT_FILE if it's already pointing at the corporate chain
pwsh -File scripts/setup-uv-ca.ps1
```

If you already generated the bundle and only need to update your current shell, you can emit the exports directly:

```bash
source <(./scripts/setup-uv-ca.sh --exports-only --print-exports)
# include --output /custom/path if you changed the bundle destination
```

```powershell
pwsh -File scripts/setup-uv-ca.ps1 -ExportsOnly -PrintExports
# include -Output C:\custom\bundle.pem if you changed the destination
```

After running, add the printed export to your shell profile (or run it inline) and re-open your terminal before invoking:

```bash
uv run --project tools/enaible enaible install copilot --mode fresh --scope user
```

For extra safety you can also pin uv to the merged bundle: `uv config set http.cabundle ~/.config/claude/corp-ca-bundle.pem`.

Because the merged file contains both trust chains, no additional approval from Astral/GitHub is required; they already present publicly trusted certificates. This script simply restores the public roots that the corporate profile overrides.

---

# Bootstrap installers

| Platform | Script | Example |
| --- | --- | --- |
| macOS/Linux | `scripts/install.sh` | `curl -fsSL "https://raw.githubusercontent.com/adam-versed/ai-assisted-workflows/main/scripts/install.sh?$(date +%s)" \| bash -s -- --systems codex,claude-code --scope user` |
| Windows (PowerShell 7+) | `scripts/install.ps1` | `pwsh -NoLogo -ExecutionPolicy Bypass -File scripts/install.ps1 -Systems codex,claude-code -Scope user` |

Both scripts clone (or update) the repo under `~/.enaible/sources/ai-assisted-workflows`, run `uv tool install --from <clone>/tools/enaible enaible`, and then call `enaible install <system> --scope user --mode sync` so user-level prompts stay current. Provide `--scope project --project /path/to/repo` (or `-Scope both -Project ...` in PowerShell) to hydrate a local checkout at the same time. Every run drops a short log in `~/.enaible/install-sessions/` so CI and humans can trace which settings were applied.

Common flags:

- `--systems codex,claude-code` / `-Systems codex,claude-code` — choose the systems to install (default: `codex,claude-code`).
- `--scope user|project|both` / `-Scope user|project|both` — select install scope; project/both modes require `--project PATH`.
- `--project /path/to/repo` / `-Project C:\repos\my-app` — explicit project root when targeting project scope.
- `--ref vX.Y.Z` / `-Ref vX.Y.Z` — pin to a specific git tag or branch.
- `--dry-run` / `-DryRun` — print actions without making changes (great for CI smoke tests).
