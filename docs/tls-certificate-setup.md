# TLS Certificate Setup for Corporate Networks

This guide explains how to handle TLS certificate validation issues when using `uv` on corporate networks that use custom certificate authorities (CAs).

## Problem

When running `uv sync` or `uv tool install` on corporate networks, you may encounter:

```
× Failed to fetch: `https://pypi.org/simple/jinja2/`
├─▶ error sending request for url
├─▶ client error (Connect)
╰─▶ invalid peer certificate: UnknownIssuer
```

This occurs because `uv` cannot validate SSL certificates when:
1. Your network uses a corporate proxy/firewall with a custom CA
2. The system CA bundle doesn't include the corporate CA
3. `uv` cannot locate the correct CA certificates

## Use the Setup Script (Recommended for Corporate Networks)

The `scripts/setup-uv-ca.sh` (macOS/Linux) and `scripts/setup-uv-ca.ps1` (Windows) scripts automatically merge system and corporate CA certificates.

**For Live Installs:**

```bash
./scripts/setup-uv-ca.sh   # macOS/Linux
# or
pwsh -File scripts/setup-uv-ca.ps1   # Windows PowerShell 7+
```

After generating the merged bundle, add the single export shown by the script to your shell profile and restart the terminal before rerunning `uv`.

**Advantages:**
- ✅ Works for all tools (`uv`, `curl`, `requests`, `pip`)
- ✅ Persistent across sessions (via shell profile)
- ✅ Handles both system and corporate CAs automatically
- ✅ One-time setup per machine

**Disadvantages:**
- ❌ Requires manual setup script execution
- ❌ Requires corporate CA file location
