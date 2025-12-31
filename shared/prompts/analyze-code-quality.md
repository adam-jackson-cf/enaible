# Purpose

Assess code quality by combining automated metrics with architectural review to surface maintainability and technical-debt risks.

## Variables

### Required

- @TARGET_PATH = $1 — path to analyze; defaults to repo root

### Optional (derived from $ARGUMENTS)

- @AUTO = --auto — skip STOP confirmations (auto-approve checkpoints)
- @MIN_SEVERITY = --min-severity — defaults to "high"; accepts critical|high|medium|low
- @EXCLUDE = --exclude [repeatable] — additional glob patterns to exclude

### Derived (internal)

- @ARTIFACT_ROOT = <derived> — timestamped artifacts directory used for analyzer outputs

## Instructions

- ALWAYS run the Enaible analyzers; never probe or invoke module scripts directly.
- Store raw analyzer reports under `.enaible/artifacts/analyze-code-quality/`; treat JSON outputs as audit evidence.
- Always read artifacts via absolute paths derived from `@ARTIFACT_ROOT` (avoid relative `.enaible/...` reads).
- Correlate quantitative metrics with qualitative observations before recommending remediation.
- Prioritize recommendations by impact and implementation effort, citing exact files and symbols.
- Capture follow-up questions or unknowns so they can be resolved before refactor work begins.
- Respect STOP confirmations unless @AUTO is provided; when auto is active, treat checkpoints as approved without altering other behavior.
- Run reconnaissance before analyzers to detect project context and auto-apply smart exclusions.
- After synthesis, explicitly identify gaps in deterministic tool coverage and backfill where possible.

## Workflow

1. **Establish artifacts directory**
   - Resolve the repo root and target path, then create the artifacts directory:

     ```bash
     PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
     TARGET_PATH="@TARGET_PATH"
     if [ -z "$TARGET_PATH" ] || [ "$TARGET_PATH" = "." ]; then
       TARGET_PATH="$PROJECT_ROOT"
     elif [ "${TARGET_PATH#/}" = "$TARGET_PATH" ]; then
       TARGET_PATH="$PROJECT_ROOT/$TARGET_PATH"
     fi
     ARTIFACT_ROOT="$PROJECT_ROOT/.enaible/artifacts/analyze-code-quality/$(date -u +%Y%m%dT%H%M%SZ)"
     mkdir -p "$ARTIFACT_ROOT"
     ```

2. **Reconnaissance**
   - Glob for project markers: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`
   - Detect layout: monorepo vs single-project, primary language(s), test framework conventions
   - Record detected languages and note which analyzers will run or be skipped (with reason)
   - Auto-apply exclusions for generated/vendor directories: `dist/`, `build/`, `node_modules/`, `__pycache__/`, `.next/`, `vendor/`, `.venv/`, `.mypy_cache/`, `.ruff_cache/`, `.pytest_cache/`, `.gradle/`, `target/`, `bin/`, `obj/`, `coverage/`, `.turbo/`, `.svelte-kit/`, `.cache/`, `.enaible/artifacts/`
   - Merge with any user-provided @EXCLUDE patterns
   - Note quality conventions to check based on detected stack (e.g., linter configs, type strictness, documentation standards)
   - Log applied exclusions for final report
3. **Run automated analyzers**
   - Execute each Enaible command, storing the JSON output:

     ```bash
     ENAIBLE_REPO_ROOT="$PROJECT_ROOT" uv run --directory tools/enaible enaible analyzers run quality:lizard \
       --target "$TARGET_PATH" \
       --summary \
       --out "$ARTIFACT_ROOT/quality-lizard-summary.json" \
       @EXCLUDE

     ENAIBLE_REPO_ROOT="$PROJECT_ROOT" uv run --directory tools/enaible enaible analyzers run quality:lizard \
       --target "$TARGET_PATH" \
       --out "$ARTIFACT_ROOT/quality-lizard.json" \
       @EXCLUDE

     ENAIBLE_REPO_ROOT="$PROJECT_ROOT" uv run --directory tools/enaible enaible analyzers run quality:jscpd \
       --target "$TARGET_PATH" \
       --out "$ARTIFACT_ROOT/quality-jscpd.json" \
       @EXCLUDE
     ```

   - Use the summary report for ingestion and tables; keep the full report as audit evidence.
   - Add `--exclude "<glob>"` or adjust `--min-severity` when you need to tune scope or noise levels.
   - If either invocation fails, review available flags with `enaible analyzers run --help` before retrying.
   - If `quality:jscpd` exceeds 5 minutes, rerun it on focused scopes (e.g., `shared/`, `tools/enaible/src/enaible`) and name outputs per scope.

4. **Interpret metrics**
   - Highlight hotspots exceeding thresholds (cyclomatic complexity > 10, function length > 80 lines, parameter count > 5).
   - Prefer documented project thresholds (CONTRIBUTING, lint configs) when they differ from defaults.
   - Cross-reference duplication findings with the impacted components.
5. **Evaluate qualitative dimensions**
   - Review documentation depth, readability, adherence to SOLID principles, and test coverage signals.
   - Identify recurring code smells or anti-patterns that amplify the quantitative results.
6. **Formulate improvement plan**
   - Group recommendations by category (maintainability, testing, patterns, debt reduction) with impact/effort notes.
   - Map each action to specific files or modules and call out enabling prerequisites.
7. **Identify coverage gaps**
   - List what the analyzers checked (complexity, duplication) vs. what they cannot check
   - For each gap category:
     - Semantic clarity: inspect variable/function naming for domain meaning and intent
     - Appropriate abstraction level: review whether abstractions match problem complexity
     - Domain modeling fit: check if code structure reflects business concepts
   - If inspectable via code reading: perform targeted review, cite evidence
   - If requires runtime/external info: flag as "requires manual verification"
   - Assign confidence: High (tool + LLM agreement), Medium (LLM inference only), Low (couldn't verify)
8. **Deliver the report**
   - Summarize findings, attach metric tables, and cite evidence paths from `@ARTIFACT_ROOT`.

## Output

```md
# RESULT

- Summary: Code quality assessment completed for <@TARGET_PATH>.
- Artifacts: `.enaible/artifacts/analyze-code-quality/<timestamp>/`

## RECONNAISSANCE

- Project type: <monorepo|single-project>
- Primary stack: <languages/frameworks detected>
- Detected languages: <list>
- Auto-excluded: <patterns applied>

## METRICS

| Metric                | Threshold | Worst Offender | Value |
| --------------------- | --------- | -------------- | ----- |
| Cyclomatic Complexity | 10        | <file#Lline>   | <n>   |
| Function Length       | 80 lines  | <file#Lline>   | <n>   |
| Parameter Count       | 5         | <symbol>       | <n>   |

## INSIGHTS

- Maintainability: <observation>
- Technical Debt: <observation>
- Testing Coverage Signals: <observation>
- SOLID & Patterns: <observation>

## GAP ANALYSIS

| Gap Category                  | Status            | Finding                                     | Confidence      |
| ----------------------------- | ----------------- | ------------------------------------------- | --------------- |
| Semantic clarity              | Inspected         | <finding>                                   | High/Medium/Low |
| Appropriate abstraction level | Inspected/Flagged | <finding or "requires manual verification"> | High/Medium/Low |
| Domain modeling fit           | Inspected         | <finding>                                   | High/Medium/Low |

## RECOMMENDATIONS

1. <Highest priority action with target files>
2. <Additional actions>

## ATTACHMENTS

- quality:lizard report → `.enaible/artifacts/analyze-code-quality/<timestamp>/quality-lizard.json`
- quality:lizard summary → `.enaible/artifacts/analyze-code-quality/<timestamp>/quality-lizard-summary.json`
- quality:jscpd report → `.enaible/artifacts/analyze-code-quality/<timestamp>/quality-jscpd.json`
```
