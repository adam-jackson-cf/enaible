<!-- generated: enaible -->
<!-- codex prompt (frontmatter-free) -->

# analyze-code-quality v1.0

## Variables

| Token          | Type                     | Description                                       |
| -------------- | ------------------------ | ------------------------------------------------- |
| `$TARGET_PATH` | positional #1 (REQUIRED) | Path to analyze; defaults to the current project. |

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
   - Set `ARTIFACT_ROOT=".enaible/artifacts/analyze-code-quality/$(date -u +%Y%m%dT%H%M%SZ)"` and create the directory.
   - Record the artifact path for inclusion in the final report.
2. **Run automated analyzers via Enaible**

   - Execute and persist JSON output for each analyzer:

     ```bash
     uv run enaible analyzers run quality:lizard \
       --target "$TARGET_PATH" \
       --out "$ARTIFACT_ROOT/quality-lizard.json"

     uv run enaible analyzers run quality:jscpd \
       --target "$TARGET_PATH" \
       --out "$ARTIFACT_ROOT/quality-jscpd.json"
     ```

   - Use `--summary` for quick triage when dealing with very large reports; rerun without it before final delivery.

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

- Summary: Code quality assessment completed for <TARGET_PATH>.
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
