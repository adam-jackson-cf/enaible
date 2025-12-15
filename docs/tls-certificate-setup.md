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

## Solution Options

### Option 1: Use the Setup Script (Recommended for Corporate Networks)

The `scripts/setup-uv-ca.sh` script automatically merges system and corporate CA certificates.

**For Live Installs:**

```bash
# Run the setup script (one-time setup per machine)
./scripts/setup-uv-ca.sh

# Follow the instructions to add exports to your shell profile
# Then restart your shell or source the profile
source ~/.zshrc  # or ~/.bashrc

# Now uv commands will work
uv run --project tools/enaible enaible install copilot --scope user
```

**Advantages:**
- ✅ Works for all tools (`uv`, `curl`, `requests`, `pip`)
- ✅ Persistent across sessions (via shell profile)
- ✅ Handles both system and corporate CAs automatically
- ✅ One-time setup per machine

**Disadvantages:**
- ❌ Requires manual setup script execution
- ❌ Requires corporate CA file location

### Option 2: Configure `uv` Global Settings

Set a global CA bundle path in `uv`'s configuration:

```bash
# Set the CA bundle path (use the merged bundle from setup script)
uv config set http.cabundle "$HOME/.config/claude/corp-ca-bundle.pem"

# Or point to your system CA bundle
uv config set http.cabundle "/etc/ssl/cert.pem"  # Linux
uv config set http.cabundle "/etc/ssl/certs/ca-certificates.crt"  # Alternative Linux
```

**Advantages:**
- ✅ Persistent (stored in `uv` config)
- ✅ Only affects `uv` (doesn't interfere with other tools)
- ✅ Works across all `uv` commands automatically

**Disadvantages:**
- ❌ Only works for `uv` (not `curl`, `pip`, etc.)
- ❌ Requires knowing the CA bundle path
- ❌ May need different paths per OS

**Best Use Case:** When you only need `uv` to work and want a simple, persistent solution.

### Option 3: Use `--native-tls` Flag

Tell `uv` to use the system's native TLS implementation:

```bash
uv sync --native-tls --project tools/enaible
uv tool install --native-tls --from tools/enaible enaible
```

**Advantages:**
- ✅ No configuration needed
- ✅ Uses system's built-in certificate validation
- ✅ Works if system certificates are properly configured

**Disadvantages:**
- ❌ Must be specified on every command
- ❌ Doesn't help if system certificates are missing corporate CA
- ❌ Not a permanent solution

**Best Use Case:** Quick testing or when system certificates are already configured correctly.

## Recommended Approach

### For Live Installs (End Users)

**Best Practice:** Use Option 1 (setup script) + Option 2 (uv config) together:

1. **One-time setup per machine:**
   ```bash
   ./scripts/setup-uv-ca.sh
   ```

2. **Add to shell profile** (as instructed by script):
   ```bash
   export SSL_CERT_FILE="$HOME/.config/claude/corp-ca-bundle.pem"
   export REQUESTS_CA_BUNDLE="$HOME/.config/claude/corp-ca-bundle.pem"
   export UV_HTTP_CA_BUNDLE="$HOME/.config/claude/corp-ca-bundle.pem"
   ```

3. **Configure uv specifically:**
   ```bash
   uv config set http.cabundle "$HOME/.config/claude/corp-ca-bundle.pem"
   ```

This provides:
- ✅ Coverage for all tools (via environment variables)
- ✅ Persistent `uv` configuration (via `uv config`)
- ✅ Works even if environment variables aren't set in a particular session

### For Test Environments

**Best Practice:** Use environment variables in test fixtures:

```python
@pytest.fixture(autouse=True)
def _setup_tls_certs(monkeypatch: pytest.MonkeyPatch) -> None:
    """Configure TLS certificates for tests."""
    # Option A: Use system certificates if available
    system_ca = Path("/etc/ssl/cert.pem")
    if system_ca.exists():
        monkeypatch.setenv("SSL_CERT_FILE", str(system_ca))
        monkeypatch.setenv("UV_HTTP_CA_BUNDLE", str(system_ca))

    # Option B: Use merged bundle if setup script was run
    merged_ca = Path.home() / ".config" / "claude" / "corp-ca-bundle.pem"
    if merged_ca.exists():
        monkeypatch.setenv("SSL_CERT_FILE", str(merged_ca))
        monkeypatch.setenv("UV_HTTP_CA_BUNDLE", str(merged_ca))

    # Option C: Skip TLS validation in tests (NOT RECOMMENDED for production)
    # Only use if corporate CA is not available in test environment
    # monkeypatch.setenv("UV_NATIVE_TLS", "1")
```

**Alternative for CI/CD:** Configure certificates in CI environment variables or use `--native-tls` flag in CI scripts.

## Implementation in Installer

The installer could be enhanced to:

1. **Detect TLS issues** and provide helpful error messages
2. **Auto-detect CA bundle** locations
3. **Suggest the setup script** when TLS errors occur

Example enhancement:

```python
def _sync_enaible_env(repo_root: Path, dry_run: bool, summary: InstallSummary) -> None:
    # ... existing code ...
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.decode() if exc.stderr else ""
        if "invalid peer certificate" in stderr or "UnknownIssuer" in stderr:
            raise typer.BadParameter(
                "TLS certificate validation failed. This often occurs on corporate networks.\n"
                "Solutions:\n"
                "  1. Run: ./scripts/setup-uv-ca.sh (recommended)\n"
                "  2. Or set: uv config set http.cabundle <path-to-ca-bundle>\n"
                "  3. Or use: uv sync --native-tls (temporary)\n"
                "See docs/tls-certificate-setup.md for details."
            ) from exc
        raise typer.BadParameter(
            "Failed to run 'uv sync --project tools/enaible'. Ensure `uv` is installed and accessible."
        ) from exc
```

## Quick Reference

| Scenario | Solution | Command |
|----------|----------|---------|
| **Corporate network (one-time)** | Setup script | `./scripts/setup-uv-ca.sh` |
| **uv-only fix** | uv config | `uv config set http.cabundle <path>` |
| **Quick test** | Native TLS flag | `uv sync --native-tls` |
| **Test fixtures** | Environment vars | `monkeypatch.setenv("UV_HTTP_CA_BUNDLE", path)` |

## Troubleshooting

**Q: Setup script can't find corporate CA?**
```bash
# Specify explicitly
./scripts/setup-uv-ca.sh --corp-ca /path/to/corporate-ca.pem
```

**Q: Still getting certificate errors after setup?**
```bash
# Verify the bundle exists and is readable
cat "$HOME/.config/claude/corp-ca-bundle.pem" | head -5

# Check uv is using it
uv config get http.cabundle

# Test with verbose output
UV_LOG=debug uv sync --project tools/enaible
```

**Q: Different CA bundle per project?**
```bash
# Use environment variable (overrides config)
export UV_HTTP_CA_BUNDLE="/custom/path/ca-bundle.pem"
uv sync --project tools/enaible
```


