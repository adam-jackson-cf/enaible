#!/bin/bash
# AI-Assisted Workflows Uninstall Script
# Removes AI-Assisted Workflows components while preserving .claude directory structure

set -euo pipefail

# Script configuration
SCRIPT_VERSION="1.0.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="/tmp/ai-workflows-uninstall.log"

# Default settings
DRY_RUN="false"
VERBOSE="false"
TARGET_PATH=""

# Global arrays for installation log tracking
PRE_EXISTING_PYTHON=()
NEWLY_INSTALLED_PYTHON=()

# Usage and help
show_usage() {
    cat << 'EOF'
AI-Assisted Workflows Uninstaller

USAGE:
    ./uninstall.sh [TARGET_PATH] [OPTIONS]

ARGUMENTS:
    TARGET_PATH     Directory containing .claude/ to uninstall from
                   Examples:
                     ~/                    (User global: ~/.claude/)
                     ./myproject           (Project local: ./myproject/.claude/)
                     /path/to/project      (Custom path: /path/to/project/.claude/)
                   Default: current directory

OPTIONS:
    -h, --help      Show this help message
    -v, --verbose   Enable verbose output
    -n, --dry-run   Show what would be removed without making changes

EXAMPLES:
    # Uninstall from current project
    ./uninstall.sh

    # Uninstall from user global installation
    ./uninstall.sh ~

    # Dry run to see what would be removed
    ./uninstall.sh --dry-run

DESCRIPTION:
    This script removes AI-Assisted Workflows components while preserving
    the .claude directory structure and any user-added files:

    - Removes workflow command files
    - Removes agent prompt files
    - Removes analysis scripts
    - Removes rule files
    - Cleans up auxiliary files (logs, helpers)
    - Removes sections from claude.md
    - Optionally removes Python packages (interactive)
EOF
}

# Initialize log file
init_log() {
    echo "" > "$LOG_FILE"
    log "AI-Assisted Workflows Uninstaller (v$SCRIPT_VERSION) started"
    log "Current directory: $(pwd)"
    log "Script directory: $SCRIPT_DIR"
    log "Command line: $0 $*"
}

# Logging functions
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log_verbose() {
    if [[ "$VERBOSE" == "true" ]]; then
        log "$@"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
    fi
}

log_error() {
    echo "[ERROR] $*" | tee -a "$LOG_FILE" >&2
}

# Platform detection
detect_platform() {
    case "$(uname -s)" in
        Darwin*)
            PLATFORM="macos"
            ;;
        Linux*)
            PLATFORM="linux"
            ;;
        CYGWIN*|MINGW*|MSYS*)
            PLATFORM="windows"
            ;;
        *)
            log_error "Unsupported platform: $(uname -s)"
            exit 1
            ;;
    esac
    log_verbose "Detected platform: $PLATFORM"
}

# Find and validate .claude installation
find_claude_installation() {
    # Set target path for .claude directory
    if [[ -z "$TARGET_PATH" ]]; then
        TARGET_PATH="$(pwd)"
    fi

    # Handle path ending with .claude
    if [[ "$TARGET_PATH" == */.claude ]]; then
        CLAUDE_DIR="$TARGET_PATH"
        log_verbose "Target path already ends with .claude, using it directly"
    else
        CLAUDE_DIR="$TARGET_PATH/.claude"
        log_verbose "Looking for .claude in target path"
    fi

    log "Checking for AI-Assisted Workflows installation at: $CLAUDE_DIR"

    if [[ ! -d "$CLAUDE_DIR" ]]; then
        log_error "No .claude directory found at: $CLAUDE_DIR"
        echo "Please specify the correct path containing your .claude installation"
        exit 1
    fi

    # Check if this looks like our installation
    local our_files_found=0

    # Check for our command files
    if [[ -f "$CLAUDE_DIR/commands/plan-solution.md" ]]; then
        ((our_files_found++))
    fi

    # Check for our scripts
    if [[ -d "$CLAUDE_DIR/scripts/core" ]] || [[ -d "$CLAUDE_DIR/scripts/analyzers" ]]; then
        ((our_files_found++))
    fi

    # Check for our rules
    if [[ -f "$CLAUDE_DIR/rules/global.claude.rules.md" ]]; then
        ((our_files_found++))
    fi

    if [[ $our_files_found -eq 0 ]]; then
        log_error "No AI-Assisted Workflows components found at: $CLAUDE_DIR"
        echo "This doesn't appear to be a AI-Assisted Workflows installation"
        exit 1
    fi

    log "Found AI-Assisted Workflows installation ($our_files_found components detected)"
}

# Remove workflow command files
remove_command_files() {
    log "Checking for workflow command files..."

    if [[ ! -d "$CLAUDE_DIR/commands" ]]; then
        log_verbose "No commands directory found"
        return 0
    fi

    # List of our command files
    local our_commands=(
        "add-code-precommit-checks.md"
        "analyze-architecture.md"
        "analyze-code-quality.md"
        "analyze-performance.md"
        "analyze-root-cause.md"
        "analyze-security.md"
        "apply-rule-set.md"
        "clean-history.md"
        "codify-claude-history.md"
        "create-project.md"
        "create-rule.md"
        "create-session-notes.md"
        "get-primer.md"
        "get-recent-context.md"
        "plan-linear-v2.md"
        "plan-linear.md"
        "plan-refactor.md"
        "plan-solution.md"
        "plan-ux-prd.md"
        "setup-dev-monitoring.md"
        "setup-package-monitoring.md"
        "setup-serena-mcp.md"
        "todo-background.md"
        "todo-build-worktree.md"
        "todo-build.md"
    )

    local files_to_remove=()

    # Check which of our files exist
    for cmd in "${our_commands[@]}"; do
        if [[ -f "$CLAUDE_DIR/commands/$cmd" ]]; then
            files_to_remove+=("$cmd")
        fi
    done

    if [[ ${#files_to_remove[@]} -eq 0 ]]; then
        log "No workflow command files found to remove"
        return 0
    fi

    echo ""
    echo "Found ${#files_to_remove[@]} workflow command files:"
    for file in "${files_to_remove[@]}"; do
        echo "  - $file"
    done
    echo ""

    if [[ "$DRY_RUN" == "true" ]]; then
        log "Would remove ${#files_to_remove[@]} command files"
        return 0
    fi

    read -p "Remove these command files? (y/n): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        local removed_count=0
        for file in "${files_to_remove[@]}"; do
            if rm "$CLAUDE_DIR/commands/$file" 2>/dev/null; then
                log_verbose "Removed command file: $file"
                ((removed_count++))
            else
                log_error "Failed to remove command file: $file"
            fi
        done
        log "Removed $removed_count command files"
    else
        log "Skipped removing command files"
    fi
}

# Remove agent prompt files
remove_agent_files() {
    log "Checking for agent prompt files..."

    if [[ ! -d "$CLAUDE_DIR/agents" ]]; then
        log_verbose "No agents directory found"
        return 0
    fi

    local our_agents=(
        "docker-expert.md"
        "docs-scraper.md"
        "documenter.md"
        "gemini-handler.md"
        "git-action-expert.md"
        "git-manager.md"
        "linear-acceptance-criteria-writer.md"
        "linear-dependency-linker.md"
        "linear-estimation-engine.md"
        "linear-hashing.md"
        "linear-issue-decomposer.md"
        "linear-issue-search.md"
        "linear-issue-writer.md"
        "linear-objective-definition.md"
        "linear-readiness.md"
        "log-monitor.md"
        "market-analyst.md"
        "plan-manager.md"
        "problem-escalation.md"
        "python-expert.md"
        "quality-monitor.md"
        "qwen-handler.md"
        "rag-architecture-expert.md"
        "research-coordinator.md"
        "senior-developer.md"
        "solution-validator.md"
        "technical-researcher.md"
        "terraform-gcp-expert.md"
        "typescript-expert.md"
        "user-researcher.md"
        "ux-designer.md"
        "ux-reviewer.md"
    )

    local files_to_remove=()
    for agent in "${our_agents[@]}"; do
        if [[ -f "$CLAUDE_DIR/agents/$agent" ]]; then
            files_to_remove+=("$agent")
        fi
    done

    if [[ ${#files_to_remove[@]} -eq 0 ]]; then
        log "No agent prompt files found to remove"
        return 0
    fi

    echo ""
    echo "Found ${#files_to_remove[@]} agent prompt files:"
    for file in "${files_to_remove[@]}"; do
        echo "  - agents/$file"
    done
    echo ""

    if [[ "$DRY_RUN" == "true" ]]; then
        log "Would remove ${#files_to_remove[@]} agent prompt files"
        return 0
    fi

    read -p "Remove these agent prompt files? (y/n): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        local removed_count=0
        for file in "${files_to_remove[@]}"; do
            if rm "$CLAUDE_DIR/agents/$file" 2>/dev/null; then
                log_verbose "Removed agent file: $file"
                ((removed_count++))
            else
                log_error "Failed to remove agent file: $file"
            fi
        done

        if [[ -d "$CLAUDE_DIR/agents" ]] && [[ -z "$(ls -A "$CLAUDE_DIR/agents")" ]]; then
            rmdir "$CLAUDE_DIR/agents" 2>/dev/null && log_verbose "Removed empty agents directory"
        fi

        log "Removed $removed_count agent prompt files"
    else
        log "Skipped removing agent prompt files"
    fi
}

# Remove script directories
remove_script_directories() {
    log "Checking for analysis script directories..."

    if [[ ! -d "$CLAUDE_DIR/scripts" ]]; then
        log_verbose "No scripts directory found"
        return 0
    fi

    # List of our script directories and files
    local our_scripts=(
        "scripts/analyzers"
        "scripts/config"
        "scripts/context"
        "scripts/core"
        "scripts/generators"
        "scripts/setup"
        "scripts/utils"
        "scripts/web_scraper"
        "eslint"
    )

    local items_to_remove=()

    # Check which of our script items exist
    for item in "${our_scripts[@]}"; do
        if [[ -e "$CLAUDE_DIR/$item" ]]; then
            items_to_remove+=("$item")
        fi
    done

    if [[ ${#items_to_remove[@]} -eq 0 ]]; then
        log "No workflow script directories found to remove"
        return 0
    fi

    echo ""
    echo "Found ${#items_to_remove[@]} script directories/files:"
    for item in "${items_to_remove[@]}"; do
        if [[ -d "$CLAUDE_DIR/$item" ]]; then
            echo "  - $item (directory)"
        else
            echo "  - $item (file)"
        fi
    done
    echo ""

    if [[ "$DRY_RUN" == "true" ]]; then
        log "Would remove ${#items_to_remove[@]} script items"
        return 0
    fi

    read -p "Remove these script directories and files? (y/n): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        local removed_count=0
        for item in "${items_to_remove[@]}"; do
            if rm -rf "$CLAUDE_DIR/$item" 2>/dev/null; then
                log_verbose "Removed script item: $item"
                ((removed_count++))
            else
                log_error "Failed to remove script item: $item"
            fi
        done

        # Clean up __pycache__ folders in scripts directory
        if [[ -d "$CLAUDE_DIR/scripts" ]]; then
            find "$CLAUDE_DIR/scripts" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
            log_verbose "Cleaned up __pycache__ folders"
        fi

        # Remove scripts directory if it's empty or only contains __pycache__
        if [[ -d "$CLAUDE_DIR/scripts" ]]; then
            # Remove any remaining __pycache__ folders
            find "$CLAUDE_DIR/scripts" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

            # Check if scripts directory is empty or only contains empty subdirectories
            if [[ -z "$(find "$CLAUDE_DIR/scripts" -type f)" ]]; then
                rm -rf "$CLAUDE_DIR/scripts" 2>/dev/null && log_verbose "Removed empty scripts directory"
            fi
        fi

        log "Removed $removed_count script items"
    else
        log "Skipped removing script directories"
    fi
}

# Remove miscellaneous helper files
remove_misc_files() {
    log "Checking for auxiliary workflow files..."

    local candidates=(
        "installation-log.txt"
        "linear-plan.config.json"
        "statusline-worktree"
    )

    local files_to_remove=()
    for item in "${candidates[@]}"; do
        if [[ -e "$CLAUDE_DIR/$item" ]]; then
            files_to_remove+=("$item")
        fi
    done

    # Only remove settings.json if it matches the distributed template
    if [[ -f "$CLAUDE_DIR/settings.json" && -f "$SCRIPT_DIR/settings.json" ]]; then
        if cmp -s "$CLAUDE_DIR/settings.json" "$SCRIPT_DIR/settings.json"; then
            files_to_remove+=("settings.json")
        else
            log_verbose "settings.json appears to be customized; leaving in place"
        fi
    fi

    if [[ ${#files_to_remove[@]} -eq 0 ]]; then
        log "No auxiliary workflow files found to remove"
        return 0
    fi

    echo ""
    echo "Found ${#files_to_remove[@]} auxiliary files:"
    for item in "${files_to_remove[@]}"; do
        echo "  - $item"
    done
    echo ""

    if [[ "$DRY_RUN" == "true" ]]; then
        log "Would remove ${#files_to_remove[@]} auxiliary files"
        return 0
    fi

    read -p "Remove these auxiliary files? (y/n): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        local removed_count=0
        for item in "${files_to_remove[@]}"; do
            if rm -rf "$CLAUDE_DIR/$item" 2>/dev/null; then
                log_verbose "Removed auxiliary file: $item"
                ((removed_count++))
            else
                log_error "Failed to remove auxiliary file: $item"
            fi
        done
        log "Removed $removed_count auxiliary files"
    else
        log "Skipped removing auxiliary files"
    fi
}

# Remove rule files
remove_rule_files() {
    log "Checking for rule files..."

    if [[ ! -d "$CLAUDE_DIR/rules" ]]; then
        log_verbose "No rules directory found"
        return 0
    fi

    # List of our rule files
    local our_rules=(
        "global.claude.rules.md"
        "minimal.intrusion.rules.md"
        "rapid.prototype.rules.md"
        "tdd.rules.md"
    )

    local files_to_remove=()

    # Check which of our rule files exist
    for rule in "${our_rules[@]}"; do
        if [[ -f "$CLAUDE_DIR/rules/$rule" ]]; then
            files_to_remove+=("$rule")
        fi
    done

    if [[ ${#files_to_remove[@]} -eq 0 ]]; then
        log "No rule files found to remove"
        return 0
    fi

    echo ""
    echo "Found ${#files_to_remove[@]} rule files:"
    for file in "${files_to_remove[@]}"; do
        echo "  - rules/$file"
    done
    echo ""

    if [[ "$DRY_RUN" == "true" ]]; then
        log "Would remove ${#files_to_remove[@]} rule files"
        return 0
    fi

    read -p "Remove these rule files? (y/n): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        local removed_count=0
        for file in "${files_to_remove[@]}"; do
            if rm "$CLAUDE_DIR/rules/$file" 2>/dev/null; then
                log_verbose "Removed rule file: $file"
                ((removed_count++))
            else
                log_error "Failed to remove rule file: $file"
            fi
        done
        log "Removed $removed_count rule files"

        # Remove rules directory if it's empty
        if [[ -d "$CLAUDE_DIR/rules" ]] && [[ -z "$(ls -A "$CLAUDE_DIR/rules")" ]]; then
            rmdir "$CLAUDE_DIR/rules" 2>/dev/null && log_verbose "Removed empty rules directory"
        fi
    else
        log "Skipped removing rule files"
    fi
}

# Remove sections from claude.md
remove_claude_md_sections() {
    log "Checking for our sections in claude.md..."

    if [[ ! -f "$CLAUDE_DIR/claude.md" ]]; then
        log_verbose "No claude.md file found"
        return 0
    fi

    local marker="# AI-Assisted Workflows v"

    if ! grep -q "$marker" "$CLAUDE_DIR/claude.md"; then
        log "No AI-Assisted Workflows sections found in claude.md"
        return 0
    fi

    echo ""
    echo "Found AI-Assisted Workflows section in claude.md (header starts with '$marker')."
    echo ""

    if [[ "$DRY_RUN" == "true" ]]; then
        log "Would remove AI-Assisted Workflows section from claude.md"
        return 0
    fi

    read -p "Remove the AI-Assisted Workflows section from claude.md? (y/n): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        local backup_file="${CLAUDE_DIR}/claude.md.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$CLAUDE_DIR/claude.md" "$backup_file"
        log_verbose "Created backup: $(basename "$backup_file")"

        CLAUDE_MD="$CLAUDE_DIR/claude.md" SECTION_MARKER="$marker" python3 - <<'PY'
import os
from pathlib import Path

path = Path(os.environ["CLAUDE_MD"])
marker = os.environ["SECTION_MARKER"]
text = path.read_text(encoding="utf-8")
idx = text.find(marker)
if idx == -1:
    raise SystemExit(0)
trimmed = text[:idx].rstrip()
if trimmed:
    trimmed += '\n'
path.write_text(trimmed, encoding="utf-8")
PY

        log "Removed AI-Assisted Workflows section from claude.md"
        echo "Backup saved as: $(basename "$backup_file")"
    else
        log "Skipped removing claude.md section"
    fi
}

# Read installation log for better removal warnings
read_installation_log() {
    local log_file="$CLAUDE_DIR/installation-log.txt"

    # Initialize arrays
    PRE_EXISTING_PYTHON=()
    NEWLY_INSTALLED_PYTHON=()

    if [[ ! -f "$log_file" ]]; then
        log_verbose "No installation log found, using default warnings"
        return 0
    fi

    log_verbose "Reading installation log for safer removal..."

    # Read pre-existing Python packages
    local in_section=""
    while IFS= read -r line; do
        case "$line" in
            "[PRE_EXISTING_PYTHON_PACKAGES]")
                in_section="pre_python"
                ;;
            "[NEWLY_INSTALLED_PYTHON_PACKAGES]")
                in_section="new_python"
                ;;
            "["*"]")
                in_section=""
                ;;
            *)
                if [[ -n "$line" && ! "$line" =~ ^[[:space:]]*# ]]; then
                    case "$in_section" in
                        "pre_python")
                            PRE_EXISTING_PYTHON+=("$line")
                            ;;
                        "new_python")
                            NEWLY_INSTALLED_PYTHON+=("$line")
                            ;;
                    esac
                fi
                ;;
        esac
    done < "$log_file"

    log_verbose "Found installation log: ${#PRE_EXISTING_PYTHON[@]} pre-existing Python packages, ${#NEWLY_INSTALLED_PYTHON[@]} newly installed"
}

# Interactive Python package removal
remove_python_packages() {
    log "Checking for Python packages to remove..."

    # Check if requirements.txt exists in our script directory
    local requirement_files=()
    if [[ -f "$CLAUDE_DIR/scripts/setup/requirements.txt" ]]; then
        requirement_files+=("$CLAUDE_DIR/scripts/setup/requirements.txt")
    fi
    if [[ -f "$CLAUDE_DIR/scripts/setup/ci/requirements.txt" ]]; then
        requirement_files+=("$CLAUDE_DIR/scripts/setup/ci/requirements.txt")
    fi

    if [[ ${#requirement_files[@]} -eq 0 ]]; then
        log_verbose "No requirements files found, skipping Python package removal"
        return 0
    fi

    # Extract package names from requirements files (remove version constraints)
    local packages=()
    for requirements_file in "${requirement_files[@]}"; do
        while IFS= read -r line; do
            [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
            local pkg=$(echo "$line" | sed 's/[>=<].*//' | tr -d ' ')
            [[ -n "$pkg" ]] && packages+=("$pkg")
        done < "$requirements_file"
    done

    if [[ ${#packages[@]} -gt 0 ]]; then
        local unique_packages=()
        declare -A seen_pkgs=()
        for pkg in "${packages[@]}"; do
            if [[ -z "${seen_pkgs[$pkg]:-}" ]]; then
                unique_packages+=("$pkg")
                seen_pkgs[$pkg]=1
            fi
        done
        packages=("${unique_packages[@]}")
    fi

    if [[ ${#packages[@]} -eq 0 ]]; then
        log "No Python packages found in requirements.txt"
        return 0
    fi

    # Check which packages are actually installed
    local installed_packages=()
    for pkg in "${packages[@]}"; do
        if python3 -m pip show "$pkg" &>/dev/null; then
            installed_packages+=("$pkg")
        fi
    done

    if [[ ${#installed_packages[@]} -eq 0 ]]; then
        log "No installed Python packages found to remove"
        return 0
    fi

    echo ""
    echo "Found ${#installed_packages[@]} Python packages that could be removed:"

    # Categorize packages based on installation log
    local pre_existing=()
    local newly_installed=()
    local unknown=()

    for pkg in "${installed_packages[@]}"; do
        if [[ ${#PRE_EXISTING_PYTHON[@]} -gt 0 ]] && [[ " ${PRE_EXISTING_PYTHON[*]} " =~ " $pkg " ]]; then
            pre_existing+=("$pkg")
        elif [[ ${#NEWLY_INSTALLED_PYTHON[@]} -gt 0 ]] && [[ " ${NEWLY_INSTALLED_PYTHON[*]} " =~ " $pkg " ]]; then
            newly_installed+=("$pkg")
        else
            unknown+=("$pkg")
        fi
    done

    # Show packages with appropriate warnings
    if [[ ${#newly_installed[@]} -gt 0 ]]; then
        echo ""
        echo "📦 Newly installed by AI-Assisted Workflows (safer to remove):"
        for pkg in "${newly_installed[@]}"; do
            echo "  - $pkg"
        done
    fi

    if [[ ${#pre_existing[@]} -gt 0 ]]; then
        echo ""
        echo "⚠️  Pre-existing packages (likely used by other projects - CAUTION advised):"
        for pkg in "${pre_existing[@]}"; do
            echo "  - $pkg"
        done
    fi

    if [[ ${#unknown[@]} -gt 0 ]]; then
        echo ""
        echo "❓ Unknown status packages (no installation log available):"
        for pkg in "${unknown[@]}"; do
            echo "  - $pkg"
        done
    fi

    echo ""
    echo "⚠️  WARNING: Only remove packages you're certain aren't needed by other projects!"
    echo "    Pre-existing packages were already installed before AI-Assisted Workflows."
    echo ""

    if [[ "$DRY_RUN" == "true" ]]; then
        log "Would prompt to remove ${#installed_packages[@]} Python packages"
        return 0
    fi

    local removed_count=0
    for pkg in "${installed_packages[@]}"; do
        # Show appropriate warning based on package status
        local warning=""
        if [[ ${#PRE_EXISTING_PYTHON[@]} -gt 0 ]] && [[ " ${PRE_EXISTING_PYTHON[*]} " =~ " $pkg " ]]; then
            warning=" (⚠️  PRE-EXISTING - likely used elsewhere)"
        elif [[ ${#NEWLY_INSTALLED_PYTHON[@]} -gt 0 ]] && [[ " ${NEWLY_INSTALLED_PYTHON[*]} " =~ " $pkg " ]]; then
            warning=" (📦 newly installed by workflows)"
        fi

        echo -n "Remove Python package '$pkg'$warning? (y/n): "
        read -n 1 -r
        echo

        if [[ $REPLY =~ ^[Yy]$ ]]; then
            if python3 -m pip uninstall -y "$pkg" &>/dev/null; then
                log_verbose "Removed Python package: $pkg"
                ((removed_count++))
            else
                log_error "Failed to remove Python package: $pkg"
            fi
        else
            log_verbose "Skipped Python package: $pkg"
        fi
    done

    if [[ $removed_count -gt 0 ]]; then
        log "Removed $removed_count Python packages"
    else
        log "No Python packages were removed"
    fi
}


# Parse command line arguments
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            -v|--verbose)
                VERBOSE="true"
                shift
                ;;
            -n|--dry-run)
                DRY_RUN="true"
                shift
                ;;
            -*)
                log_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
            *)
                if [[ -z "$TARGET_PATH" ]]; then
                    TARGET_PATH="$1"
                else
                    log_error "Multiple target paths specified"
                    exit 1
                fi
                shift
                ;;
        esac
    done
}

# Show uninstall summary
show_summary() {
    echo ""
    echo "🧹 AI-Assisted Workflows uninstall completed!"
    echo ""
    echo "Installation location: $CLAUDE_DIR"
    echo ""
    echo "What was processed:"
    echo "  ✓ Workflow command files checked/removed"
    echo "  ✓ Agent prompt files checked/removed"
    echo "  ✓ Analysis script directories checked/removed"
    echo "  ✓ Auxiliary files cleaned up"
    echo "  ✓ Rule files checked/removed"
    echo "  ✓ claude.md sections checked/removed"
    echo "  ✓ Python packages offered for removal"
    echo ""
    echo "The .claude directory structure has been preserved."
    echo "Check the log for details: $LOG_FILE"
    echo ""
}

# Main execution function
main() {
    init_log
    parse_arguments "$@"
    detect_platform

    log "Starting AI-Assisted Workflows uninstall (v$SCRIPT_VERSION)"

    if [[ "$DRY_RUN" == "true" ]]; then
        echo "🔍 DRY RUN MODE - No changes will be made"
        echo ""
    fi

    # Find and validate installation
    find_claude_installation

    # Read installation log for better removal warnings
    read_installation_log

    echo ""
    echo "🧹 AI-Assisted Workflows Uninstaller"
    echo "===================================="
    echo ""
    echo "This will selectively remove AI-Assisted Workflows components from:"
    echo "  $CLAUDE_DIR"
    echo ""
    echo "The .claude directory and any user-added files will be preserved."
    echo ""

    if [[ "$DRY_RUN" != "true" ]]; then
        read -p "Continue with uninstall? (y/n): " -n 1 -r
        echo
        echo ""

        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log "Uninstall cancelled by user"
            echo "Uninstall cancelled."
            exit 0
        fi
    fi

    # Remove components
    remove_command_files
    remove_agent_files
    remove_script_directories
    remove_misc_files
    remove_rule_files
    remove_claude_md_sections
    remove_python_packages

    if [[ "$DRY_RUN" != "true" ]]; then
        show_summary
    else
        echo ""
        echo "Dry run completed - no changes were made"
        echo "Run without --dry-run to perform the actual uninstall"
    fi
}

# Run main function with all arguments
main "$@"
