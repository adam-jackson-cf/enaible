## <!-- generated: enaible -->

description: Assess code quality and complexity, and highlight high‑value refactors
argument-hint: [target-path] [--exclude?] [--min-severity?]

---

# analyze-code-quality v1.0

## Variables

### Required

- @TARGET_PATH = $1 — path to analyze; defaults to repo root

### Optional (derived from $ARGUMENTS)

- @MIN_SEVERITY = --min-severity — defaults to "high"; accepts critical|high|medium|low

- @EXCLUDE = --exclude [repeatable] — additional glob patterns to exclude

# Purpose

Assess code quality by combining automated metrics with architectural review to surface maintainability and technical-debt risks.

## Instructions

- ALWAYS run the Enaible analyzers; never probe or invoke module scripts directly.
- Store raw analyzer reports under `.enaible/artifacts/analyze-code-quality/`; treat JSON outputs as audit evidence.
- Correlate quantitative metrics with qualitative observations before recommending remediation.
- Prioritize recommendations by impact and implementation effort, citing exact files and symbols.
- Capture follow-up questions or unknowns so they can be resolved before refactor work begins.

## Workflow

1. **Establish artifacts directory**
   - Set `ARTIFACT_ROOT=".enaible/artifacts/code-quality/$(date -u +%Y%m%dT%H%M%SZ)"` and create it.
2. **Run automated analyzers**

   - Execute each Enaible command, storing the JSON output:

     ```bash
     uv run --project tools/enaible enaible analyzers run quality:lizard \
       --target "@TARGET_PATH" \
       --out "$ARTIFACT_ROOT/quality-lizard.json"

     uv run --project tools/enaible enaible analyzers run quality:jscpd \
       --target "@TARGET_PATH" \
       --out "$ARTIFACT_ROOT/quality-jscpd.json"
     ```

   - Use `--summary` for quick triage when dealing with very large reports; rerun without it before final delivery.
   - Add `--exclude "<glob>"` or adjust `--min-severity` when you need to tune scope or noise levels.
   - If either invocation fails, review available flags with `uv run --project tools/enaible enaible analyzers run --help` before retrying.

3. **Interpret metrics**
   - Highlight hotspots exceeding thresholds (cyclomatic complexity > 10, function length > 80 lines, parameter count > 5).
   - Cross-reference duplication findings with the impacted components.
4. **Evaluate qualitative dimensions**
   - Review documentation depth, readability, adherence to SOLID principles, and test coverage signals.
   - Identify recurring code smells or anti-patterns that amplify the quantitative results.
5. **Formulate improvement plan**
   - Group recommendations by category (maintainability, testing, patterns, debt reduction) with impact/effort notes.
   - Map each action to specific files or modules and call out enabling prerequisites.
6. **Deliver the report**
   - Summarize findings, attach metric tables, and cite evidence paths from `ARTIFACT_ROOT`.

## Output

```md
# RESULT

- Summary: Code quality assessment completed for <@TARGET_PATH>.
- Artifacts: `.enaible/artifacts/analyze-code-quality/<timestamp>/`

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

## RECOMMENDATIONS

1. <Highest priority action with target files>
2. <Additional actions>

## ATTACHMENTS

- quality:lizard report → `.enaible/artifacts/analyze-code-quality/<timestamp>/quality-lizard.json`
- quality:jscpd report → `.enaible/artifacts/analyze-code-quality/<timestamp>/quality-jscpd.json`
```

## Examples

```bash
# Run quality analysis on entire repo
/analyze-code-quality .

# Focus on a specific package
/analyze-code-quality packages/service
```
