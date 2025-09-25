# Installation and Setup

## 📦 Installation

### For Claude Code CLI

```bash
./claude-code/install.sh              # Install to current directory
./claude-code/install.sh ~            # Install globally
```

### For OpenCode Editor

```bash
./opencode/install.sh                 # Install to current directory
./opencode/install.sh ~               # Install globally
```

### Post-Installation Setup

```bash
/setup-dev-monitoring                 # Optional: Setup unified dev logging
/setup-package-monitoring                  # Optional: Package auditing on change looking for security risks


/add-serena-mcp                       # Recommended per project mcp lsp tool - only available in claude code as lacks LSP support
```

## 🔧 Dependencies

Due to the programmatic analysis scripts, there's quite a lot of dependencies installed.
Full list of libraries used and languages supported found here: [Analysis Scripts](analysis-scripts.md)

## Installation Details

### Installation Options

#### Claude Code CLI

```bash
# Current directory (uses ./.claude/)
./claude-code/install.sh

# User global (uses ~/.claude/)
./claude-code/install.sh ~

# Custom location
./claude-code/install.sh /my/project/path

# Advanced options
./claude-code/install.sh --dry-run       # Preview changes without making modifications
./claude-code/install.sh --verbose      # Enable detailed debug output
./claude-code/install.sh --skip-mcp     # Skip MCP tools installation (Python scripts only)
./claude-code/install.sh --skip-python  # Skip Python dependencies installation
./claude-code/install.sh --help         # Show detailed help and usage information
```

#### OpenCode Editor

```bash
# Current directory (uses ./.opencode/)
./opencode/install.sh

# User global (uses ~/.config/opencode/)
./opencode/install.sh ~

# Custom location
./opencode/install.sh /my/project/path

# Advanced options
./opencode/install.sh --dry-run       # Preview changes without making modifications
./opencode/install.sh --verbose      # Enable detailed debug output
./opencode/install.sh --skip-mcp     # Skip MCP tools installation (Python scripts only)
./opencode/install.sh --skip-python  # Skip Python dependencies installation
./opencode/install.sh --help         # Show detailed help and usage information
```

### Dependencies Installation

The installer automatically handles all dependencies:

**Python Dependencies:**

- Runs `shared/setup/install_dependencies.py` to install packages from `shared/setup/requirements.txt`
- Optionally installs CI framework dependencies from `shared/setup/ci/requirements.txt`
- Validates Python 3.11+ compatibility

**Node.js Dependencies:**

- Automatically installs ESLint and plugins via npm if not present
- Creates a `package.json` in the installation directory
- Installs comprehensive frontend analysis tools (ESLint, TypeScript, React, Vue, Svelte plugins)

**Installation Tracking:**

- Creates an installation log for clean uninstallation tracking
- Tracks which packages were pre-existing vs newly installed

### Handling Existing Installations

**Automatic Backup:** All installation options automatically create a timestamped backup of your existing installation before making any changes.

The installer automatically detects existing `.claude` directories (Claude Code) and `.opencode` or `$HOME/.config/opencode` directories (OpenCode) and offers four options:

1. **Fresh Install:** Complete replacement of existing installation
2. **Merge:** Preserve user customizations while adding new features (no overwrites)
3. **Update Workflows Only:** Update built-in commands and scripts while preserving custom commands and all other files (recommended for updates)
4. **Cancel:** Exit without changes

## Uninstalling

To safely remove AI-Assisted Workflows components while preserving your configuration directory (`.claude` or `.opencode`):

### For Claude Code installations:

```bash
# Preview what would be removed (recommended first step)
./claude-code/uninstall.sh --dry-run

# Uninstall from current directory
./claude-code/uninstall.sh

# Uninstall from specific path
./claude-code/uninstall.sh /path/to/installation

# Verbose output for detailed logging
./claude-code/uninstall.sh --verbose
```

### For OpenCode installations:

```bash
# Preview what would be removed (recommended first step)
./opencode/uninstall.sh --dry-run

# Uninstall from current directory
./opencode/uninstall.sh

# Uninstall from specific path
./opencode/uninstall.sh /path/to/installation

# Verbose output for detailed logging
./opencode/uninstall.sh --verbose
```

**Smart Uninstall Features:**

- **📦 Safe Removal**: Only removes workflow components, preserves `.claude`/`.opencode` structure and user files
- **⚠️ Dependency Tracking**: Distinguishes pre-existing vs newly installed Python packages/MCP servers using installation-log.txt
- **💾 Automatic Backups**: Creates backups of MCP configuration and platform docs before changes
- **🧹 Thorough Cleanup**: Removes **pycache** folders and empty directories
- **📝 Installation Log**: Uses installation-log.txt to provide intelligent removal warnings

The uninstaller will interactively prompt for each Python package and MCP server removal, showing whether each item was:

- **🔧 Newly installed** by AI-Assisted Workflows (safer to remove)
- **⚠️ Pre-existing** before installation (likely used by other projects - caution advised)
