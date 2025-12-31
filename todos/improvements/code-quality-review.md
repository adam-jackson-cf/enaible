# RESULT

- Summary: Code quality assessment completed for `/Users/adamjackson/LocalDev/enaible`.
- Artifacts: `.enaible/artifacts/analyze-code-quality/20251231T142226Z/`

## RECONNAISSANCE

- **Project type**: Single-project (Python toolchain)
- **Primary stack**: Python 3.12, CLI (Typer), analysis tooling
- **Detected languages**: Python (primary), Markdown (prompts)
- **Auto-excluded**: `node_modules/`, `.venv/`, `__pycache__/`, `.enaible/artifacts/`, `shared/tests/**` (user-specified)
- **Analyzers run**: quality:lizard (complexity), quality:jscpd (duplication)
- **Analyzers skipped**: None

## METRICS

| Metric                | Threshold | Worst Offender                                                                    | Value |
| --------------------- | --------- | --------------------------------------------------------------------------------- | ----- |
| Cyclomatic Complexity | 10        | `shared/context/context_bundle_capture_codex.py:367` (`extract_jsonl_operations`) | 44    |
| Cyclomatic Complexity | 10        | `shared/context/context_bundle_capture_claude.py:139` (`extract_session_full`)    | 44    |
| Cyclomatic Complexity | 10        | `shared/analyzers/performance/analyze_frontend.py:756` (`_is_false_positive`)     | 32    |
| Function Length       | 100 lines | `shared/context/context_bundle_capture_codex.py:367` (`extract_jsonl_operations`) | 168   |
| Function Length       | 100 lines | `shared/generators/ci/setup_security_analysis_ci.py:73` (`_generate_workflow`)    | 166   |
| Parameter Count       | 5         | `tools/enaible/src/enaible/commands/install.py:277` (`_complete_installation`)    | 10    |

### Summary by Severity (min-severity: high)

| Severity | Count                                  |
| -------- | -------------------------------------- |
| Critical | 0                                      |
| High     | 28                                     |
| Medium   | 183 (not shown; consult JSON artifact) |
| Low      | 0                                      |

### Duplication (jscpd)

| Metric               | Value                |
| -------------------- | -------------------- |
| Clone Pairs          | 29                   |
| Clone Fragments      | 58                   |
| High/Medium findings | 0 (all low severity) |

## INSIGHTS

- **Maintainability**: The codebase has several functions with cyclomatic complexity 3-4x above the recommended threshold of 10. The worst offenders are in context capture modules (`extract_jsonl_operations` CC=44, `extract_session_full` CC=44) which parse JSONL session logs. These monolithic parsing functions are difficult to test and modify.

- **Technical Debt**: 28 high-severity findings across complexity (CC > 20), function length (> 100 lines), and parameter count (> 7). Key debt areas:
  - Context capture modules need extraction into smaller, testable functions
  - CI workflow generators (`_generate_workflow`) are essentially template strings that could use a templating approach
  - The `_is_false_positive` function in frontend analyzer has grown to 146 lines with many conditional branches

- **Testing Coverage Signals**: 138 test functions across 13 unit test files + 10 CLI test files. Coverage is focused on analyzers and utilities. The high-complexity context capture modules (`context_bundle_capture_codex.py`, `context_bundle_capture_claude.py`) have minimal test coverage (2 tests for codex).

- **SOLID & Patterns**: Good use of base class abstractions (`BaseAnalyzer`, `BaseProfiler`, `CIModuleBase`). Registry pattern for analyzers is well-implemented. However, several functions violate Single Responsibility by combining parsing, filtering, and transformation in single methods.

## GAP ANALYSIS

| Gap Category                  | Status    | Finding                                                                                                                                                                                                                                                                                                           | Confidence |
| ----------------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| Semantic clarity              | Inspected | Function and class names are domain-appropriate (e.g., `extract_session_full`, `LizardComplexityAnalyzer`). Variable names like `op`, `ts`, `etype` in parsing code are abbreviated but contextually clear.                                                                                                       | High       |
| Appropriate abstraction level | Inspected | Base classes (`BaseAnalyzer`, `AnalyzerConfig`) provide appropriate abstraction for analyzer implementations. However, parsing functions (`extract_jsonl_operations`, `extract_session_full`) mix multiple abstraction levels—file I/O, JSON parsing, event routing, and data transformation—in single functions. | High       |
| Domain modeling fit           | Inspected | Analysis domain is well-modeled with Finding, AnalysisResult, and severity enums. Context capture domain lacks explicit models—events are handled as dictionaries rather than typed dataclasses.                                                                                                                  | Medium     |
| Error handling consistency    | Flagged   | Some high-complexity functions use broad `except Exception: pass` patterns (e.g., `context_bundle_capture_claude.py:278`), which silently swallows errors.                                                                                                                                                        | High       |

## RECOMMENDATIONS

1. **Refactor `extract_jsonl_operations` and `extract_session_full`** (shared/context/)
   - Extract event-type handlers into separate functions (e.g., `_handle_session_meta()`, `_handle_item_event()`)
   - Introduce dataclasses for event types to replace dictionary handling
   - Expected complexity reduction: CC 44 → CC < 10 per function
   - Impact: High | Effort: Medium

2. **Consolidate parameter objects for functions with 7+ parameters**
   - `_complete_installation` (10 params) → `InstallationConfig` dataclass
   - `_render_managed_prompts` (7 params) → `RenderContext` dataclass
   - `create_standard_finding` (7 params) → Already has `Finding` dataclass, use it
   - Impact: Medium | Effort: Low

3. **Improve test coverage for context capture modules**
   - Current: 2 tests for `context_bundle_capture_codex.py`
   - Target: Cover each event type handler independently
   - This becomes feasible after the refactor in recommendation #1
   - Impact: High | Effort: Medium (after refactor)

4. **Replace broad exception handlers with specific error handling**
   - Replace `except Exception: pass` with logging or specific exception types
   - Consider using `contextlib.suppress()` for intentionally ignored exceptions
   - Impact: Medium | Effort: Low

5. **Extract workflow generation templates** (shared/generators/ci/)
   - `_generate_workflow` functions (157, 166 lines) are essentially string templates
   - Consider using Jinja2 templates (already a dependency) with template files
   - Impact: Low | Effort: Medium

## ATTACHMENTS

- quality:lizard report → `.enaible/artifacts/analyze-code-quality/20251231T142226Z/quality-lizard.json`
- quality:lizard summary → `.enaible/artifacts/analyze-code-quality/20251231T142226Z/quality-lizard-summary.json`
- quality:jscpd report → `.enaible/artifacts/analyze-code-quality/20251231T142226Z/quality-jscpd.json`
