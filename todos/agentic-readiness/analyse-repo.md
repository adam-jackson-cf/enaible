# Agentic Readiness: Repository Analysis Workflow

Analyze a target repository for adherence to agentic engineering guidelines.

## Objective

Assess a codebase against measurable agentic readiness criteria and produce a scored report with actionable findings.

## Target Repository

`{{TARGET_REPO_PATH}}`

---

## Analysis Checks

Execute each check category in sequence. Record pass/fail/partial status and evidence.

### 1. Verified Starting Base

#### VSB-1: Project Scaffolding Quality

**Check:** Determine if project uses established templates/generators.

```
- Look for generator markers: .yo-rc.json, angular.json (CLI), vite.config.*, next.config.*, etc.
- Check package.json for framework CLI metadata
- Assess project structure against framework conventions
```

**Pass criteria:** Standard framework structure detected OR documented template source.

#### VSB-2: Build Passes

**Check:** Execute build and verify success.

```bash
# Attempt common build commands
npm run build || yarn build || pnpm build || make build || ./gradlew build || cargo build
```

**Pass criteria:** Build exits with code 0.

#### VSB-3: Tests Pass

**Check:** Execute test suite and verify success.

```bash
# Attempt common test commands
npm test || yarn test || pnpm test || make test || pytest || cargo test
```

**Pass criteria:** Tests exit with code 0, test count > 0.

#### VSB-4: Dependencies Version-Pinned

**Check:** Verify lock files exist and are committed.

```
- package-lock.json, yarn.lock, pnpm-lock.yaml (Node)
- poetry.lock, Pipfile.lock, requirements.txt with pinned versions (Python)
- Cargo.lock (Rust), go.sum (Go), Gemfile.lock (Ruby)
```

**Pass criteria:** Appropriate lock file exists AND is tracked in git.

#### VSB-5: Toolchain Versions Pinned

**Check:** Verify runtime/toolchain version specifications exist.

```
- .nvmrc, .node-version (Node)
- .python-version, .tool-versions (Python/asdf)
- rust-toolchain.toml (Rust)
- Dockerfile with pinned base images
```

**Pass criteria:** At least one toolchain version file present.

---

### 2. System Documentation Quality

#### IFCD-3: AGENTS.md Conciseness

**Check:** If AGENTS.md (or CLAUDE.md, copilot-instructions.md) exists, assess content.

```
- Measure line count (target: <200 lines)
- Check for high-level structure vs verbose implementation details
- Identify redundant content that duplicates linting/tooling
```

**Pass criteria:** System doc exists AND line count <200 AND no verbose implementation docs.

#### IFCD-5: System Docs Complement Automation

**Check:** Rules in system docs should not duplicate what linting enforces.

```
- Extract rules from AGENTS.md/CLAUDE.md
- Compare against eslint/prettier/ruff/pylint config
- Flag duplicates (e.g., "use semicolons" when eslint enforces it)
```

**Pass criteria:** <20% rule overlap with linting configuration.

#### CGSD-3: Deterministic Tools Preferred

**Check:** Verify linting and formatting tools are configured.

```
- ESLint, Prettier, Biome (JS/TS)
- Ruff, Black, Pylint, mypy (Python)
- rustfmt, clippy (Rust)
- golangci-lint (Go)
```

**Pass criteria:** At least one linter AND one formatter configured.

#### CGSD-5: Rules Use Verifiable Metrics

**Check:** Analyze system doc rules for measurability.

```
- Search for numeric thresholds (complexity limits, LOC limits, etc.)
- Flag subjective guidance without metrics ("keep it simple", "be careful")
```

**Pass criteria:** >50% of rules have verifiable criteria.

---

### 3. Verification Infrastructure

#### VFCR-1: Local Verification Mirrors CI

**Check:** Compare local and CI configurations.

```
- Extract test/lint commands from CI (.github/workflows/, .gitlab-ci.yml, etc.)
- Compare against package.json scripts or Makefile
- Flag commands present in CI but not locally runnable
```

**Pass criteria:** All CI verification steps can be run locally.

#### VFCR-2: Integration Tests Present

**Check:** Identify test types beyond unit tests.

```
- Search for e2e/, integration/, cypress/, playwright/, __e2e__/
- Check for test files with integration/e2e in name
- Look for test database or service setup scripts
```

**Pass criteria:** Integration or E2E test directory/files exist.

#### VFCR-5: Pre-commit Hooks Configured

**Check:** Verify pre-commit hook setup.

```
- .husky/ directory with pre-commit hook
- .pre-commit-config.yaml
- lefthook.yml
- package.json with husky/lint-staged config
```

**Pass criteria:** Pre-commit hook configuration present.

#### VFCR-7: Quality Gates Cannot Be Bypassed

**Check:** Search for bypass patterns in CI and scripts.

```
- --no-verify, --skip-hooks in scripts
- continue-on-error: true in CI without justification
- if: always() on verification steps
- Disabled rules in linting configs (rule: 0, rule: off)
```

**Pass criteria:** No bypass patterns OR all bypasses have documented justification.

---

### 4. Tooling Transparency

#### AH-1: System Prompts Visible and Versioned

**Check:** Verify prompt files are in source control.

```
- AGENTS.md, CLAUDE.md, copilot-instructions.md in git
- .github/copilot-instructions.md tracked
- Custom prompt files in prompts/ or similar
```

**Pass criteria:** System prompt files exist AND are git-tracked.

#### AH-2: Tool Configuration Versioned

**Check:** Verify AI tool configs are committed.

```
- .cursor/, .continue/, .aider* configs
- mcp.json, claude_desktop_config.json (if used)
- AI-related VS Code settings in .vscode/
```

**Pass criteria:** Tool configuration files are git-tracked (not gitignored).

---

### 5. Workflow Automation

#### CLDC-1: Permanent Workflows as Scripts

**Check:** Identify scriptified workflows.

```
- Makefile with documented targets
- package.json scripts section
- scripts/ directory with shell scripts
- justfile, taskfile.yml
```

**Pass criteria:** Task runner present with >5 defined tasks.

#### CLDC-2: Scripts Have Clear Inputs/Outputs

**Check:** Assess script documentation.

```
- --help support on custom scripts
- Comments/headers describing purpose
- README section on available commands
```

**Pass criteria:** Primary scripts have documented usage.

---

### 6. Observability Infrastructure

#### OBS-1: Dev Logs Accessible to Agents

**Check:** Verify log access mechanisms.

```
- Make/npm targets for log retrieval
- Documented log locations in system docs
- Log aggregation scripts
```

**Pass criteria:** At least one documented method to access dev logs.

#### OBS-2: Quality Gates Provide Feedback

**Check:** Verify linting produces actionable output.

```bash
# Run linter and verify output format
npm run lint 2>&1 | head -20
```

**Pass criteria:** Linter output includes file paths, line numbers, and rule IDs.

#### OBS-3: Pre-commit Hooks Configured

**Check:** (Same as VFCR-5 - shared check)

---

## Scoring Methodology

### Per-Check Scoring

- **Pass (2 points):** Fully meets criteria with evidence
- **Partial (1 point):** Partially meets criteria or missing minor elements
- **Fail (0 points):** Does not meet criteria or not present

### Category Weights

| Category                    | Checks | Max Points | Weight |
| --------------------------- | ------ | ---------- | ------ |
| Verified Starting Base      | 5      | 10         | 25%    |
| System Documentation        | 4      | 8          | 15%    |
| Verification Infrastructure | 4      | 8          | 25%    |
| Tooling Transparency        | 2      | 4          | 10%    |
| Workflow Automation         | 2      | 4          | 10%    |
| Observability               | 3      | 6          | 15%    |

### Overall Score Calculation

```
weighted_score = Σ (category_score / max_category_score) × category_weight × 100
```

### Readiness Levels

| Score Range | Level    | Interpretation                                |
| ----------- | -------- | --------------------------------------------- |
| 80-100      | High     | Ready for autonomous agentic work             |
| 60-79       | Medium   | Suitable for supervised agentic work          |
| 40-59       | Low      | Requires improvements before agentic adoption |
| 0-39        | Critical | Significant gaps; establish foundations first |

---

## Output Format

Generate a report with the following structure:

```markdown
# Agentic Readiness Report: {{PROJECT_NAME}}

**Analysis Date:** {{DATE}}
**Overall Score:** {{SCORE}}/100 ({{LEVEL}})

## Summary

{{2-3 sentence summary of readiness state}}

## Category Scores

| Category                    | Score | Status            |
| --------------------------- | ----- | ----------------- |
| Verified Starting Base      | X/10  | PASS/PARTIAL/FAIL |
| System Documentation        | X/8   | PASS/PARTIAL/FAIL |
| Verification Infrastructure | X/8   | PASS/PARTIAL/FAIL |
| Tooling Transparency        | X/4   | PASS/PARTIAL/FAIL |
| Workflow Automation         | X/4   | PASS/PARTIAL/FAIL |
| Observability               | X/6   | PASS/PARTIAL/FAIL |

## Detailed Findings

### Critical Issues (Must Fix)

{{List items scoring 0 that block agentic adoption}}

### Improvements (Should Fix)

{{List items scoring 1 that reduce effectiveness}}

### Strengths

{{List items scoring 2 that enable agentic work}}

## Recommendations

{{Prioritized list of actions to improve readiness}}
```

---

## Execution Notes

1. Run checks in order; some depend on earlier results
2. Record evidence (file paths, command outputs) for each check
3. Use partial scores when criteria are ambiguously met
4. Note any checks that cannot be evaluated due to project type
5. Adjust weights if certain categories don't apply to project type
