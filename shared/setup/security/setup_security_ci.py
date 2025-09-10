#!/usr/bin/env python3
"""
Security CI Setup Script.

Comprehensive security CI pipeline generator with universal package manager support,
dependency auditing, pinning checks, and optional branch protection rules.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Import base framework components for import validation
try:
    # Import modules to validate environment but don't use them
    import core.base.analyzer_base  # noqa: F401
    import core.utils.output_formatter  # noqa: F401
except ImportError as e:
    print(f"❌ Failed to import framework components: {e}")
    print("Ensure PYTHONPATH is set to the package root")
    sys.exit(1)


class SecurityCISetup:
    """Main security CI setup implementation."""

    def __init__(
        self,
        package_manager: str,
        audit_level: str = "moderate",
        setup_branch_protection: bool = False,
    ):
        self.package_manager = package_manager
        self.audit_level = audit_level
        self.setup_branch_protection = setup_branch_protection
        self.templates_dir = Path(__file__).parent / "templates"

        # Validate audit level
        valid_levels = ["info", "low", "moderate", "high", "critical"]
        if self.audit_level not in valid_levels:
            raise ValueError(
                f"Invalid audit level: {self.audit_level}. Valid levels: {valid_levels}"
            )

    def run(self) -> dict:
        """Execute the security CI setup process."""
        print(
            f"🔧 Setting up security CI for {self.package_manager} with audit level: {self.audit_level}"
        )

        results = {
            "package_manager": self.package_manager,
            "audit_level": self.audit_level,
            "branch_protection": self.setup_branch_protection,
            "files_created": [],
            "warnings": [],
            "errors": [],
        }

        try:
            # Create .github directory
            self._ensure_github_directory()

            # Generate workflow
            workflow_path = self._generate_security_workflow()
            results["files_created"].append(str(workflow_path))

            # Generate dependabot config
            dependabot_path = self._generate_dependabot_config()
            if dependabot_path:
                results["files_created"].append(str(dependabot_path))

            # Generate security policy
            security_path = self._generate_security_policy()
            results["files_created"].append(str(security_path))

            # Generate audit-ci config
            audit_ci_path = self._generate_audit_ci_config()
            results["files_created"].append(str(audit_ci_path))

            # Setup branch protection if requested
            if self.setup_branch_protection:
                self._setup_branch_protection(results)

            # Generate summary
            self._print_setup_summary(results)

        except Exception as e:
            results["errors"].append(str(e))
            print(f"❌ Error during setup: {e}")

        return results

    def _ensure_github_directory(self):
        """Create .github/workflows directory if it doesn't exist."""
        Path(".github/workflows").mkdir(parents=True, exist_ok=True)

    def _generate_security_workflow(self) -> Path:
        """Generate the main security workflow file."""
        workflow_path = Path(".github/workflows/package-security.yml")

        # Backup existing workflow
        if workflow_path.exists():
            backup_path = workflow_path.with_suffix(".yml.bak")
            print(f"⚠️  Existing {workflow_path} found. Backing up to {backup_path}")
            workflow_path.rename(backup_path)

        # Generate workflow content
        workflow_content = self._get_workflow_template()

        with open(workflow_path, "w") as f:
            f.write(workflow_content)

        print(f"✅ Created {workflow_path}")
        return workflow_path

    def _get_workflow_template(self) -> str:
        """Get the GitHub Actions workflow template."""
        return f"""name: Package Security Audit

on:
  push:
    branches: [main, master, develop]
  pull_request:
    branches: [main, master]
  schedule:
    # Weekly scan on Monday at 9 AM UTC
    - cron: "0 9 * * 1"
  workflow_dispatch: # Manual trigger

inputs:
  audit-level:
    description: 'Audit severity level'
    required: false
    default: '{self.audit_level}'
    type: choice
    options:
      - info
      - low
      - moderate
      - high
      - critical

jobs:
  detect-package-managers:
    runs-on: ubuntu-latest
    outputs:
      managers: ${{{{ steps.detect.outputs.managers }}}}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Detect package managers
        id: detect
        run: |
          managers=()
          if [[ -f "package-lock.json" ]]; then managers+=("npm"); fi
          if [[ -f "yarn.lock" ]]; then managers+=("yarn"); fi
          if [[ -f "pnpm-lock.yaml" ]]; then managers+=("pnpm"); fi
          if [[ -f "bun.lockb" ]]; then managers+=("bun"); fi

          # Convert array to JSON
          printf -v managers_json '%s,' "${{managers[@]}}"
          managers_json="[\\"${{managers_json%,}}\\"]"
          managers_json="${{managers_json//,/\\",\\"}}"

          echo "managers=${{managers_json}}" >> $GITHUB_OUTPUT
          echo "Detected package managers: ${{managers_json}}"

  security-audit:
    needs: detect-package-managers
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18.x, 20.x]
        package-manager: ${{{{ fromJSON(needs.detect-package-managers.outputs.managers) }}}}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js ${{{{ matrix.node-version }}}}
        uses: actions/setup-node@v4
        with:
          node-version: ${{{{ matrix.node-version }}}}
          cache: ${{{{ matrix.package-manager }}}}

      - name: Install dependencies
        run: |
          case "${{{{ matrix.package-manager }}}}" in
            npm)
              npm ci --ignore-scripts
              ;;
            yarn)
              yarn install --frozen-lockfile --ignore-scripts
              ;;
            pnpm)
              npm install -g pnpm
              pnpm install --frozen-lockfile --ignore-scripts
              ;;
            bun)
              npm install -g bun
              bun install --frozen-lockfile
              ;;
          esac

      - name: Run security audit
        id: audit
        continue-on-error: true
        run: |
          AUDIT_LEVEL="${{{{ inputs.audit-level || '{self.audit_level}' }}}}"
          echo "Running ${{{{ matrix.package-manager }}}} audit with level: $AUDIT_LEVEL"

          case "${{{{ matrix.package-manager }}}}" in
            npm)
              npm audit --audit-level=$AUDIT_LEVEL --json > audit-report.json 2>&1 || echo "audit_failed=true" >> $GITHUB_OUTPUT
              npm audit --audit-level=$AUDIT_LEVEL > audit-report.txt 2>&1 || true
              ;;
            yarn)
              yarn audit --level $AUDIT_LEVEL --json > audit-report.json 2>&1 || echo "audit_failed=true" >> $GITHUB_OUTPUT
              yarn audit --level $AUDIT_LEVEL > audit-report.txt 2>&1 || true
              ;;
            pnpm)
              pnpm audit --audit-level $AUDIT_LEVEL --json > audit-report.json 2>&1 || echo "audit_failed=true" >> $GITHUB_OUTPUT
              pnpm audit --audit-level $AUDIT_LEVEL > audit-report.txt 2>&1 || true
              ;;
            bun)
              # Bun has limited audit support, use npm audit as fallback
              echo "Bun audit support limited, using npm audit..." > audit-report.txt
              npm audit --audit-level=$AUDIT_LEVEL --json > audit-report.json 2>&1 || echo "audit_failed=true" >> $GITHUB_OUTPUT
              npm audit --audit-level=$AUDIT_LEVEL >> audit-report.txt 2>&1 || true
              ;;
          esac

      - name: Check dependency pinning
        id: pinning
        run: |
          echo "🔍 Checking for unpinned dependencies..."

          if [[ -f "package.json" ]]; then
            # Find dependencies with version ranges
            UNPINNED=$(grep -E '\\"\\^|\\"~|\\"\\*|\\"latest' package.json | grep -v devDependencies || true)

            if [[ -n "$UNPINNED" ]]; then
              echo "⚠️ Found unpinned dependencies:"
              echo "$UNPINNED"
              echo "unpinned_found=true" >> $GITHUB_OUTPUT

              # Save unpinned deps to file
              echo "## Unpinned Dependencies Found" > unpinned-report.md
              echo "The following dependencies are not pinned to exact versions:" >> unpinned-report.md
              echo '```json' >> unpinned-report.md
              echo "$UNPINNED" >> unpinned-report.md
              echo '```' >> unpinned-report.md
              echo "" >> unpinned-report.md
              echo "Consider pinning these dependencies to exact versions for security and reproducibility." >> unpinned-report.md
            else
              echo "✅ All dependencies are properly pinned"
              echo "unpinned_found=false" >> $GITHUB_OUTPUT
            fi
          fi

      - name: Generate summary report
        if: always()
        run: |
          echo "## Security Audit Summary - ${{{{ matrix.package-manager }}}} (Node ${{{{ matrix.node-version }}}})" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY

          if [[ -f "audit-report.txt" ]]; then
            echo "### Audit Results" >> $GITHUB_STEP_SUMMARY
            echo '```' >> $GITHUB_STEP_SUMMARY
            head -50 audit-report.txt >> $GITHUB_STEP_SUMMARY
            echo '```' >> $GITHUB_STEP_SUMMARY
          fi

          if [[ -f "unpinned-report.md" ]]; then
            cat unpinned-report.md >> $GITHUB_STEP_SUMMARY
          fi

      - name: Upload audit reports
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: security-reports-${{{{ matrix.package-manager }}}}-${{{{ matrix.node-version }}}}
          path: |
            audit-report.json
            audit-report.txt
            unpinned-report.md
          retention-days: 30

      - name: Comment PR with results
        if: github.event_name == 'pull_request' && (steps.audit.outputs.audit_failed == 'true' || steps.pinning.outputs.unpinned_found == 'true')
        uses: actions/github-script@v7
        with:
          script: |
            let comment = `## 🔒 Security Audit Results - ${{{{ matrix.package-manager }}}}\\n\\n`;

            if ('${{{{ steps.audit.outputs.audit_failed }}}}' === 'true') {{
              const fs = require('fs');
              if (fs.existsSync('audit-report.txt')) {{
                const auditReport = fs.readFileSync('audit-report.txt', 'utf8');
                comment += `### ⚠️ Security Vulnerabilities Found\\n\\n<details><summary>View Audit Report</summary>\\n\\n\\`\\`\\`\\n${{auditReport.slice(0, 2000)}}\\n\\`\\`\\`\\n</details>\\n\\n`;
              }}
            }}

            if ('${{{{ steps.pinning.outputs.unpinned_found }}}}' === 'true') {{
              if (fs.existsSync('unpinned-report.md')) {{
                const unpinnedReport = fs.readFileSync('unpinned-report.md', 'utf8');
                comment += unpinnedReport + '\\n';
              }}
            }}

            github.rest.issues.createComment({{
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            }});

      - name: Fail on security issues
        if: steps.audit.outputs.audit_failed == 'true'
        run: |
          echo "❌ Security audit failed with level: ${{{{ inputs.audit-level || '{self.audit_level}' }}}}"
          exit 1

  create-pinning-pr:
    needs: [detect-package-managers, security-audit]
    runs-on: ubuntu-latest
    if: contains(needs.security-audit.result, 'success') && github.event_name != 'pull_request'

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20.x'

      - name: Check for unpinned dependencies and create PR
        env:
          GH_TOKEN: ${{{{ secrets.GITHUB_TOKEN }}}}
        run: |
          if [[ -f "package.json" ]]; then
            # Check if unpinned dependencies exist
            UNPINNED=$(grep -E '\\"\\^|\\"~|\\"\\*|\\"latest' package.json | grep -v devDependencies || true)

            if [[ -n "$UNPINNED" ]]; then
              echo "Creating branch for dependency pinning..."

              # Create new branch
              BRANCH_NAME="security/pin-dependencies-$(date +%Y%m%d-%H%M%S)"
              git checkout -b "$BRANCH_NAME"

              # Pin dependencies by installing and updating package.json
              npm install --package-lock-only --save-exact

              # Check if changes were made
              if git diff --quiet package.json; then
                echo "No changes needed - dependencies already pinned"
                exit 0
              fi

              # Commit changes
              git config user.name "github-actions[bot]"
              git config user.email "github-actions[bot]@users.noreply.github.com"
              git add package.json package-lock.json
              git commit -m "security: pin dependencies to exact versions

              This automated commit pins all dependencies to exact versions
              to improve security and ensure reproducible builds.

              🤖 Generated by package-security workflow"

              # Push branch
              git push origin "$BRANCH_NAME"

              # Create PR
              gh pr create \\
                --title "🔒 Security: Pin dependencies to exact versions" \\
                --body "## Security Improvement: Dependency Pinning

This automated PR pins all production dependencies to exact versions for improved security and reproducibility.

### Changes Made:
- Removed version ranges (^, ~, *, latest) from package.json
- Updated package-lock.json with exact versions
- Ensures consistent installations across environments

### Security Benefits:
- Prevents automatic updates to potentially vulnerable versions
- Eliminates dependency confusion attacks via version ranges
- Ensures reproducible builds across all environments

### Review Checklist:
- [ ] Verify all tests pass with pinned versions
- [ ] Confirm application functionality is unaffected
- [ ] Check that no critical functionality depends on version ranges

**Note**: After merging, remember to regularly update dependencies through Dependabot or manual updates to get security patches.

🤖 Auto-generated by the package-security workflow" \\
                --head "$BRANCH_NAME" \\
                --base main

              echo "✅ Created PR for dependency pinning: $BRANCH_NAME"
            else
              echo "✅ All dependencies are already pinned"
            fi
          fi
"""

    def _generate_dependabot_config(self) -> Path | None:
        """Generate Dependabot configuration if it doesn't exist."""
        dependabot_path = Path(".github/dependabot.yml")

        if dependabot_path.exists():
            print(f"⚠️  {dependabot_path} already exists, skipping...")
            return None

        dependabot_content = f"""version: 2
updates:
  # {self.package_manager.upper()} dependencies
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "04:00"
    open-pull-requests-limit: 10
    groups:
      # Group non-security updates
      dependencies:
        dependency-type: "production"
        update-types: ["minor", "patch"]
      dev-dependencies:
        dependency-type: "development"
        update-types: ["minor", "patch"]
    # Security updates are handled separately (immediate)
    labels:
      - "dependencies"
      - "security"
    commit-message:
      prefix: "deps"
      prefix-development: "deps-dev"
      include: "scope"
    reviewers:
      - "@me"  # Replace with actual reviewers
    assignees:
      - "@me"  # Replace with actual assignees
"""

        with open(dependabot_path, "w") as f:
            f.write(dependabot_content)

        print(f"✅ Created {dependabot_path}")
        return dependabot_path

    def _generate_security_policy(self) -> Path:
        """Generate SECURITY.md documentation."""
        security_path = Path("SECURITY.md")
        current_date = datetime.now().strftime("%Y-%m-%d")

        security_content = f"""# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < Latest| :x:                |

## Reporting a Vulnerability

Please report security vulnerabilities by emailing: **security@yourorganization.com**

### Response Times

- **Critical**: Within 24 hours
- **High**: Within 3 days
- **Medium/Low**: Within 1 week

## Automated Security Scanning

This repository uses comprehensive automated security scanning:

### 1. Continuous Monitoring
- **GitHub Dependabot**: Monitors for vulnerable dependencies
- **Automatic PRs**: Created immediately for security updates
- **Weekly Updates**: Regular dependency updates every Monday

### 2. CI/CD Validation
- **Package Manager Audits**: Security scans on every PR and push
- **Multi-Package Manager Support**: npm, yarn, pnpm, bun
- **Audit Level**: {self.audit_level} (blocks {self.audit_level}+ severity vulnerabilities)
- **Matrix Testing**: Node.js 18.x and 20.x versions

### 3. Dependency Pinning
- **Automatic Detection**: Identifies unpinned dependencies
- **Automated PRs**: Creates PRs to pin dependencies to exact versions
- **Security Benefits**: Prevents dependency confusion and ensures reproducible builds

## Severity Thresholds

### Build Blocking
- **info**: ALL vulnerabilities block builds
- **low**: Low+ severity vulnerabilities block builds
- **moderate**: Moderate+ severity vulnerabilities block builds _(default)_
- **high**: Only high and critical vulnerabilities block builds
- **critical**: Only critical vulnerabilities block builds

### Current Configuration
- **Audit Level**: `{self.audit_level}`
- **Weekly Scans**: Every Monday at 9 AM UTC
- **Automatic Pinning**: Enabled for unpinned dependencies

## False Positives

If you encounter false positives that are blocking development:

1. **Verify the vulnerability** is indeed a false positive
2. **Document the reasoning** for why it's not applicable
3. **Add to allowlist** in audit-ci configuration
4. **Create an issue** to track the decision

## Security Best Practices

### For Contributors
- Keep dependencies up to date
- Review Dependabot PRs promptly
- Don't ignore security warnings
- Pin dependencies to exact versions
- Use `npm ci` instead of `npm install` in CI

### For Maintainers
- Review security PRs within 24 hours
- Merge critical security updates immediately
- Monitor security audit workflow results
- Update this policy as needed

## Workflow Configuration

The security workflow (`.github/workflows/package-security.yml`) includes:

- **Triggers**: Push, PR, weekly schedule, manual dispatch
- **Package Managers**: Automatic detection and appropriate auditing
- **Reports**: Uploaded as artifacts with 30-day retention
- **PR Comments**: Automatic comments on security issues
- **Branch Protection**: {'Enabled' if self.setup_branch_protection else 'Optional enforcement of security checks'}

## Emergency Procedures

### Critical Vulnerability Response
1. **Immediate Response**: Apply patches or workarounds within 24 hours
2. **Create Hotfix**: Deploy fix to production immediately
3. **Update Dependencies**: Merge security updates
4. **Verify Fix**: Ensure vulnerability is resolved
5. **Document**: Record incident and response in security log

### Contact Information
- **Security Team**: security@yourorganization.com
- **On-Call**: Available 24/7 for critical issues
- **Escalation**: CTO/Security Lead for high-severity issues

---

_Last Updated: {current_date}_
_Security Workflow Version: 2.0_
"""

        with open(security_path, "w") as f:
            f.write(security_content)

        print(f"✅ Created {security_path}")
        return security_path

    def _generate_audit_ci_config(self) -> Path:
        """Generate audit-ci configuration for advanced control."""
        audit_ci_path = Path(".audit-ci.json")

        audit_ci_config = {
            self.audit_level.lower(): True,
            "allowlist": [],
            "report-type": "full",
            "output-format": "text",
            "registry": "https://registry.npmjs.org",
            "package-manager": "auto",
            "pass-enoaudit": False,
            "show-not-found": True,
            "directory": "./",
            "summary": True,
        }

        with open(audit_ci_path, "w") as f:
            json.dump(audit_ci_config, f, indent=2)

        print(f"✅ Created {audit_ci_path}")
        return audit_ci_path

    def _setup_branch_protection(self, results: dict):
        """Set up branch protection rules via GitHub API."""
        print("🔧 Setting up branch protection rules...")

        # Check if gh CLI is available
        if not self._check_command("gh"):
            error_msg = "GitHub CLI (gh) not found. Please install gh to use --setup-branch-protection"
            results["errors"].append(error_msg)
            print(f"❌ {error_msg}")
            print("   Visit: https://cli.github.com/")
            return

        # Check if authenticated
        try:
            subprocess.run(["gh", "auth", "status"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            error_msg = "Not authenticated with GitHub CLI. Please run 'gh auth login'"
            results["errors"].append(error_msg)
            print(f"❌ {error_msg}")
            return

        try:
            # Get repository information
            repo_url = subprocess.check_output(
                ["git", "config", "--get", "remote.origin.url"], text=True
            ).strip()

            # Parse repo owner/name from URL
            if "github.com" in repo_url:
                parts = repo_url.split("/")
                repo_name = parts[-1].replace(".git", "")
                repo_owner = parts[-2]
            else:
                raise ValueError("Unable to parse GitHub repository information")

            # Determine main branch
            try:
                main_branch = (
                    subprocess.check_output(
                        ["git", "symbolic-ref", "refs/remotes/origin/HEAD"], text=True
                    )
                    .strip()
                    .replace("refs/remotes/origin/", "")
                )
            except subprocess.CalledProcessError:
                main_branch = "main"

            print(
                f"Setting up branch protection for: {repo_owner}/{repo_name} (branch: {main_branch})"
            )

            # Setup branch protection
            protection_config = {
                "required_status_checks": {
                    "strict": True,
                    "contexts": ["security-audit"],
                },
                "enforce_admins": False,
                "required_pull_request_reviews": {
                    "dismiss_stale_reviews": True,
                    "require_code_owner_reviews": False,
                    "required_approving_review_count": 1,
                },
                "restrictions": None,
                "allow_force_pushes": False,
                "allow_deletions": False,
            }

            # Execute GitHub API call
            cmd = [
                "gh",
                "api",
                f"repos/{repo_owner}/{repo_name}/branches/{main_branch}/protection",
                "--method",
                "PUT",
            ]

            for key, value in protection_config.items():
                cmd.extend(["--field", f"{key}={json.dumps(value)}"])

            subprocess.run(cmd, check=True)
            print("✅ Branch protection rules configured successfully")

        except Exception as e:
            error_msg = f"Failed to configure branch protection rules: {e}"
            results["errors"].append(error_msg)
            print(f"❌ {error_msg}")

    def _check_command(self, command: str) -> bool:
        """Check if a command is available in PATH."""
        try:
            subprocess.run([command, "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _print_setup_summary(self, results: dict):
        """Print final setup summary."""
        print()
        print("🎉 Security CI setup completed successfully!")
        print()
        print("📁 Generated Files:")
        for file_path in results["files_created"]:
            file_name = Path(file_path).name
            if "package-security.yml" in file_name:
                print(f"  - {file_path} (security workflow)")
            elif "dependabot.yml" in file_name:
                print(f"  - {file_path} (dependency updates)")
            elif "SECURITY.md" in file_name:
                print(f"  - {file_path} (security policy documentation)")
            elif ".audit-ci.json" in file_name:
                print(f"  - {file_path} (advanced audit configuration)")

        print()
        print("🔧 Configuration:")
        print(f"  - Package Manager: {self.package_manager}")
        print(f"  - Audit Level: {self.audit_level}")
        print(f"  - Branch Protection: {self.setup_branch_protection}")

        if results["warnings"]:
            print()
            print("⚠️  Warnings:")
            for warning in results["warnings"]:
                print(f"  - {warning}")

        if results["errors"]:
            print()
            print("❌ Errors:")
            for error in results["errors"]:
                print(f"  - {error}")

        print()
        print("🚀 Next Steps:")
        print("  1. Commit and push these files to activate the workflow")
        print("  2. Check the 'Actions' tab in GitHub to see the workflow run")
        print("  3. Review any initial security findings")
        print("  4. Merge any Dependabot PRs as appropriate")
        if self.setup_branch_protection:
            print("  5. Verify branch protection rules are active in repo settings")
        print()
        print("📖 For more information, see the generated SECURITY.md file")


def main():
    """Run the security CI setup script."""
    parser = argparse.ArgumentParser(
        description="Setup comprehensive security CI pipeline for JavaScript projects"
    )
    parser.add_argument(
        "--package-manager",
        required=True,
        choices=["npm", "yarn", "pnpm", "bun", "none"],
        help="Primary package manager detected in the project",
    )
    parser.add_argument(
        "--audit-level",
        default="moderate",
        choices=["info", "low", "moderate", "high", "critical"],
        help="Security audit severity level (default: moderate)",
    )
    parser.add_argument(
        "--branch-protection",
        default="false",
        help="Setup branch protection rules (true/false)",
    )

    args = parser.parse_args()

    # Handle package manager validation
    if args.package_manager == "none":
        print("❌ No JavaScript package manager detected")
        print(
            "   Please ensure you have a lock file (package-lock.json, yarn.lock, pnpm-lock.yaml, or bun.lockb)"
        )
        sys.exit(1)

    # Convert branch protection string to boolean
    setup_branch_protection = args.branch_protection.lower() == "true"

    try:
        # Initialize and run setup
        setup = SecurityCISetup(
            package_manager=args.package_manager,
            audit_level=args.audit_level,
            setup_branch_protection=setup_branch_protection,
        )

        results = setup.run()

        # Exit with error code if there were errors
        if results["errors"]:
            sys.exit(1)

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
