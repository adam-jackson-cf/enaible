# Purpose

Assess code quality by combining automated metrics with architectural review to surface maintainability and technical-debt risks.

## Variables

- `TARGET_PATH` ← first positional argument; defaults to `.`.
- `SCRIPT_PATH` ← resolved path to the quality analyzer directory.
- `$ARGUMENTS` ← full raw argument string.

## Instructions

- ALWAYS run the registry-driven analyzer (`quality:lizard`) instead of stand-alone tools.
- Capture raw complexity metrics (cyclomatic complexity, function length, parameter counts) for transparency.
- Cross-reference quantitative results with observed design patterns before making recommendations.
- Prioritize remediation by impact and ease, citing exact files and symbols.
- Do not proceed if analyzer scripts are missing or imports fail.

## Workflow

1. Locate analyzer scripts
   - Run `ls .claude/scripts/analyzers/quality/*.py || ls "$HOME/.claude/scripts/analyzers/quality/"`; if both fail, prompt the user for a path containing `complexity_lizard.py` and exit if none is provided.
2. Set environment context
   - Compute `SCRIPTS_ROOT="$(cd "$(dirname "$SCRIPT_PATH")/../.." && pwd)"`.
   - Run `PYTHONPATH="$SCRIPTS_ROOT" python -c "import core.base; print('env OK')"`; exit immediately if it fails.
3. Execute automated analysis
   - Run `PYTHONPATH="$SCRIPTS_ROOT" python -m core.cli.run_analyzer --analyzer quality:lizard --target "$TARGET_PATH" --output-format json`.
   - Persist the JSON output for later reference.
4. Interpret metrics
   - Identify hotspots exceeding thresholds (e.g., cyclomatic complexity > 10, function length > 80 lines).
   - Detect duplicated code blocks and high parameter counts.
5. Evaluate qualitative dimensions
   - Examine documentation coverage, readability, adherence to SOLID principles, and test coverage signals.
   - Highlight technical-debt themes (code smells, anti-patterns, refactor opportunities).
6. Formulate improvement plan
   - Group recommendations by category: maintainability, testing, patterns, debt reduction.
   - Include quick wins vs. strategic refactors.
7. Deliver report
   - Summarize key findings, attach metric tables, and map recommendations to affected modules.

## Output

```md
# RESULT

- Summary: Code quality assessment completed for <TARGET_PATH>.

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

- quality:lizard report → <path>
```

## Examples

```bash
# Run quality analysis on entire repo
/analyze-code-quality .

# Focus on a specific package
/analyze-code-quality packages/service
```
