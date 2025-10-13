# Installation and Setup

## 📦 Installation

### For Claude Code CLI

```bash
./systems/claude-code/install.sh              # Install to current directory
./systems/claude-code/install.sh ~            # Install globally
```

### For OpenCode Editor

```bash
./systems/opencode/install.sh                 # Install to current directory
./systems/opencode/install.sh ~               # Install globally
```

### Post-Installation Setup

```bash
/setup-dev-monitoring                 # Optional: Setup unified dev logging (Claude • OpenCode • Codex)
/setup-package-monitoring             # Optional: Package auditing for dependency security (Claude • OpenCode • Codex)
/setup-serena-mcp                     # Recommended MCP LSP integration across all CLIs
```

## 🔧 Dependencies

Due to the programmatic analysis scripts, there's quite a lot of dependencies installed.
Full list of libraries used and languages supported found here: [Analysis Scripts](analysis-scripts.md)

## Installation Details

### Installation Options

#### Claude Code CLI

```bash
# Current directory (uses ./.claude/)
./systems/claude-code/install.sh

# User global (uses ~/.claude/)
./systems/claude-code/install.sh ~

# Custom location
./systems/claude-code/install.sh /my/project/path

# Advanced options
./systems/claude-code/install.sh --dry-run       # Preview changes without making modifications
./systems/claude-code/install.sh --verbose      # Enable detailed debug output
./systems/claude-code/install.sh --skip-mcp     # Skip MCP tools installation (Python scripts only)
./systems/claude-code/install.sh --skip-python  # Skip Python dependencies installation
./systems/claude-code/install.sh --help         # Show detailed help and usage information
```

#### OpenCode Editor

```bash
# Current directory (uses ./.opencode/)
./systems/opencode/install.sh

# User global (uses ~/.config/opencode/)
./systems/opencode/install.sh ~

# Custom location
./systems/opencode/install.sh /my/project/path

# Advanced options
./systems/opencode/install.sh --dry-run       # Preview changes without making modifications
./systems/opencode/install.sh --verbose      # Enable detailed debug output
./systems/opencode/install.sh --skip-mcp     # Skip MCP tools installation (Python scripts only)
./systems/opencode/install.sh --skip-python  # Skip Python dependencies installation
./systems/opencode/install.sh --help         # Show detailed help and usage information
```

### For Codex CLI

```bash
# Interactive install (choose scope and scripts location)
./systems/codex/install.sh                   # Recommended; copies prompts/rules and scripts

# Non-interactive targets
./systems/codex/install.sh ~                 # User global (uses ~/.codex/)
./systems/codex/install.sh /my/project/path  # Custom (creates <path>/.codex)

# Advanced options
./systems/codex/install.sh --dry-run         # Preview changes without making modifications
./systems/codex/install.sh --verbose         # Enable detailed debug output
./systems/codex/install.sh --skip-python     # Skip Python dependencies installation
./systems/codex/install.sh --mode fresh|merge|update|cancel  # Existing install handling
```

Notes

- All prompts (including programmatic ones that invoke Python) are installed.
- Programmatic prompts require Python 3.11+ and the scripts root (default `$CODEX_HOME/scripts`).
- The installer adds trust entries for your chosen `CODEX_HOME` and `SCRIPTS_ROOT` in `$CODEX_HOME/config.toml` and ensures `chrome-devtools` MCP is present.
- To minimize sandbox prompts, prefer placing scripts within the project (e.g., `./.codex/scripts`) and run Codex with workspace write.

### Dependencies Installation

The installer automatically handles all dependencies:

**Python Dependencies:**

- Runs `shared/setup/install_dependencies.py` to install packages from `shared/setup/requirements.txt`
- Optionally installs CI framework dependencies from `shared/setup/ci/requirements.txt`
- Validates Python 3.11+ compatibility

**Node.js Dependencies (all platforms):**

- Installs ESLint and plugins when needed
- Creates a local `package.json` for ESLint workspace when required

**Installation Tracking:**

- Creates an installation log for clean uninstallation tracking
- Tracks which packages were pre-existing vs newly installed

### Handling Existing Installations

**Automatic Backup:** All installation options automatically create a timestamped backup of your existing installation before making any changes.

The installers automatically detect existing `.claude` (Claude Code), `.opencode`/`$HOME/.config/opencode` (OpenCode), and `.codex` directories (Codex CLI) and offer four options:

1. **Fresh Install:** Complete replacement of existing installation
2. **Merge:** Preserve user customizations while adding new features (no overwrites)
3. **Update Workflows Only:** Update built-in commands and scripts while preserving custom commands and all other files (recommended for updates)
4. **Cancel:** Exit without changes

## Uninstalling

To safely remove AI-Assisted Workflows components while preserving your configuration directory (`.claude` or `.opencode`):

### For Claude Code installations:

```bash
# Preview what would be removed (recommended first step)
./systems/claude-code/uninstall.sh --dry-run

# Uninstall from current directory
./systems/claude-code/uninstall.sh

# Uninstall from specific path
./systems/claude-code/uninstall.sh /path/to/installation

# Verbose output for detailed logging
./systems/claude-code/uninstall.sh --verbose
```

### For OpenCode installations:

```bash
# Preview what would be removed (recommended first step)
./systems/opencode/uninstall.sh --dry-run

# Uninstall from current directory
./systems/opencode/uninstall.sh

# Uninstall from specific path
./systems/opencode/uninstall.sh /path/to/installation

# Verbose output for detailed logging
./systems/opencode/uninstall.sh --verbose
```

### For Codex installations:

```bash
# Preview what would be removed (recommended first step)
./.codex/uninstall.sh --dry-run

# Uninstall from current directory
./.codex/uninstall.sh

# Uninstall from specific path
./.codex/uninstall.sh /path/to/installation

# Verbose output for detailed logging
./.codex/uninstall.sh --verbose
```

**Smart Uninstall Features:**

- **📦 Safe Removal**: Only removes workflow components, preserves `.claude`/`.opencode`/`.codex` structure and user files
- **⚠️ Dependency Tracking**: Distinguishes pre-existing vs newly installed Python packages/MCP servers using installation-log.txt
- **💾 Automatic Backups**: Creates backups of MCP configuration and platform docs before changes
- **🧹 Thorough Cleanup**: Removes **pycache** folders and empty directories
- **📝 Installation Log**: Uses installation-log.txt to provide intelligent removal warnings

The uninstaller will interactively prompt for each Python package and MCP server removal, showing whether each item was:

- **🔧 Newly installed** by AI-Assisted Workflows (safer to remove)
- **⚠️ Pre-existing** before installation (likely used by other projects - caution advised)
