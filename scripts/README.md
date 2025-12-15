# CLI install TLS helper

## Why this exists

The Enaible CLI installer uses `uv` to download Astral's standalone CPython builds from GitHub before it renders managed prompts. On corporate machines the shell profile often overrides `SSL_CERT_FILE`, `REQUESTS_CA_BUNDLE`, and `UV_HTTP_CA_BUNDLE` so that every HTTPS client trusts an internal TLS interception proxy. When those variables point at the internal root **only**, `uv` (via rustls) no longer trusts DigiCert, which is the public certificate authority used by GitHub/Astral. The download is rejected with `invalid peer certificate: UnknownIssuer` even though the workstation can reach GitHub in a browser.

## What the script does

`scripts/setup-uv-ca.sh` combines the stock system trust store (e.g. `/etc/ssl/cert.pem` on macOS) with your corporate root certificate. The merged PEM keeps the corporate inspector while restoring trust in public CAs, so `uv run --project tools/enaible …` can grab Astral's CPython builds without disabling any corporate controls.

Steps performed:

1. Detects the corporate CA from `CORP_CA_FILE` or the existing `SSL_CERT_FILE`/`REQUESTS_CA_BUNDLE`/`UV_HTTP_CA_BUNDLE` exports.
2. Locates the default system CA file via Python's `ssl.get_default_verify_paths()` (falls back to `/etc/ssl/cert.pem`).
3. Concatenates the two files into `~/.config/claude/corp-ca-bundle.pem` (or the path you pass with `--output`).
4. Prints the `export SSL_CERT_FILE=…` instructions so the new bundle becomes the default for future shells.

## How to use it

```bash
./scripts/setup-uv-ca.sh
# optionally specify custom paths
./scripts/setup-uv-ca.sh --corp-ca ~/.config/claude/corp-ca.pem --output ~/.config/claude/corp-ca-bundle.pem
```

If you already generated the bundle and only need to update your current shell, you can emit the exports directly without a second helper script:

```bash
source <(./scripts/setup-uv-ca.sh --exports-only --print-exports)
# include --output /custom/path if you changed the bundle destination
```

After running, add the printed exports to your shell profile (or run them inline) and re-open your terminal before invoking:

```bash
uv run --project tools/enaible enaible install copilot --mode fresh --scope user
```

For extra safety you can also pin uv to the merged bundle: `uv config set http.cabundle ~/.config/claude/corp-ca-bundle.pem`.

Because the merged file contains both trust chains, no additional approval from Astral/GitHub is required; they already present publicly trusted certificates. This script simply restores the public roots that the corporate profile overrides.
