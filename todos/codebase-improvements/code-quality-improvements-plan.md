# Code Quality Improvements: Implementation Plan

## Overview

- Objective: Reduce function length, cyclomatic complexity, and parameter count in the main codebase without changing analyzer outputs. Improve maintainability by extracting large configuration blocks, simplifying decision logic, and introducing parameter objects.
- Scope: `shared/**` (excluding `test_codebase/**`). Primary targets are the functions flagged in the report: long constructors/initializers, high CCN branches, and high-parameter signatures.
- Non‑Goals: Add new analyzer features, broaden detection scope, or introduce compatibility shims. We will not ship fallback modes or retain legacy wrappers.

## Guiding Principles

- No backward compatibility layers: remove legacy wrappers and outdated entry points.
- No fallback modes: do not continue with degraded functionality when a dependency is missing.
- Prefer established libraries over bespoke code.
- Single Responsibility: keep analyzers focused on scanning/reporting; move static patterns/config to external files.
- Extract common logic if used 3+ times.

## Context Summary (from code-quality-report)

- Long functions/constructors (High):
  - `shared/analyzers/quality/coverage_analysis.py:24` (`__init__`), `shared/analyzers/security/detect_secrets_analyzer.py:39` (`__init__`), `shared/analyzers/architecture/scalability_check.py:91` (`_init_scalability_patterns`), `shared/analyzers/root_cause/error_patterns.py:90` (`_init_error_patterns`).
- High cyclomatic complexity (High):
  - `shared/analyzers/architecture/scalability_check.py:460` (`_should_flag_scalability_issue`),
  - `shared/core/utils/tech_stack_detector.py:117` (get_simple_exclusions),
  - `shared/analyzers/quality/pattern_classifier.py:135` (`_detect_god_class.visit_ClassDef`),
  - `shared/analyzers/root_cause/error_patterns.py:645` (`_get_language_recommendation`).
- Too many parameters:
  - `shared/analyzers/quality/result_aggregator.py:667` (`get_filtered_results`),
  - `shared/analyzers/architecture/scalability_check.py:352` (`_check_scalability_patterns`),
  - `shared/analyzers/root_cause/error_patterns.py:369` (`_check_targeted_error_patterns`).

## Workstreams (Detailed)

### WS1: Coverage Analyzer – Extract Config + Remove Legacy Wrapper

- Problem
  - `TestCoverageAnalyzer.__init__` embeds large language pattern maps and generic indicators; a legacy wrapper exists at `shared/analyzers/quality/coverage_analysis.py:290`.
- Proposed Changes
  - Move language configs and indicators to `shared/config/coverage/languages.json` and `shared/config/coverage/indicators.json`.
  - Add a small loader with schema validation; keep `__init__` lean.
  - Remove legacy function `analyze_coverage(...)`.
- Affected Files
  - `shared/analyzers/quality/coverage_analysis.py:24`, `shared/analyzers/quality/coverage_analysis.py:290`.
- Deliverables
  - JSON configs; loader function; updated analyzer; deleted legacy wrapper.
- Acceptance Criteria
  - `__init__` < 50 lines; identical findings on baseline targets; no legacy wrapper.
- Risks/Mitigations
  - Config schema drift → add simple validation and example configs.

### WS2: Detect-Secrets – Strict Tool Requirement + Config Extraction

- Problem
  - Large `__init__` and permissive degraded mode in `_check_detect_secrets_availability`/`analyze_target`.
- Proposed Changes
  - Move `code_extensions`, `skip_patterns`, `plugins_used`, `filters_used` to `shared/config/security/detect_secrets.json`.
  - Remove degraded mode and environment heuristics; hard‑fail if `detect-secrets` is unavailable.
- Affected Files
  - `shared/analyzers/security/detect_secrets_analyzer.py:39`, `shared/analyzers/security/detect_secrets_analyzer.py:187`, `shared/analyzers/security/detect_secrets_analyzer.py:392`.
- Deliverables
  - JSON config; loader; fast-fail availability check; simplified `__init__`.
- Acceptance Criteria
  - Identical findings given same target and `detect-secrets` version; no fallbacks present.
- Risks/Mitigations
  - CI env without tool → add install step in CI before analyzer runs.

### WS3: Scalability Analyzer – Externalize Patterns + Lower CCN

- Problem
  - `_init_scalability_patterns` loads multiple large dictionaries; `_should_flag_scalability_issue` is a deep branch-chain; `_check_scalability_patterns` has many parameters.
- Proposed Changes
  - Move `db_patterns`, `performance_patterns`, `concurrency_patterns`, `architecture_patterns` to `shared/config/patterns/scalability/*.json`.
  - Introduce a small `FileContext` dataclass (content_lower, context_lower, lizard metrics, totals) and a strategy map `pattern_name -> predicate(ctx)` to replace `_should_flag_scalability_issue` branches.
  - Replace `_check_scalability_patterns(content, lines, file_path, pattern_dict, category)` with `_check_scalability_patterns(ctx)`.
- Affected Files
  - `shared/analyzers/architecture/scalability_check.py:91`, `shared/analyzers/architecture/scalability_check.py:352`, `shared/analyzers/architecture/scalability_check.py:460`.
- Deliverables
  - Pattern JSONs; loader; strategy predicates; simplified method signatures.
- Acceptance Criteria
  - Same findings on baseline targets; `_should_flag_scalability_issue` CCN ≤ 6; parameter count reduced.
- Risks/Mitigations
  - Predicate logic errors → add unit tests per predicate.

### WS4: Error Patterns – Externalize Patterns + Table-Driven Language Advice

- Problem
  - `_init_error_patterns` includes large dicts; `_get_language_recommendation` is nested if/elif; `_check_targeted_error_patterns` has many parameters.
- Proposed Changes
  - Move `error_patterns` and `language_patterns` to `shared/config/patterns/error/*.json`.
  - Implement table-driven language recommendations: list of `(regex, message)` per extension; first match wins.
  - Introduce `ErrorScanContext` (content, lines, file_path, error_context, relevant_patterns) to reduce parameter count.
- Affected Files
  - `shared/analyzers/root_cause/error_patterns.py:90`, `shared/analyzers/root_cause/error_patterns.py:369`, `shared/analyzers/root_cause/error_patterns.py:645`.
- Deliverables
  - Pattern JSONs; recommendation tables; context object and loader.
- Acceptance Criteria
  - Identical findings on baseline targets; CCN for `_get_language_recommendation` ≤ 5; reduced parameters.
- Risks/Mitigations
  - Regex mismatch → add tests using curated snippets.

### WS5: Tech Stack Detector – Declarative Exclusions

- Problem
  - `get_simple_exclusions` uses multiple branching blocks to add exclusions per stack.
- Proposed Changes
  - Drive exclusions from config (extend existing `shared/config/tech_stacks/tech_stacks.json` or add `shared/config/tech_stacks/exclusions.json`).
  - Compose exclusions as unions of universal + detected stacks; minimize branching.
- Affected Files
  - `shared/core/utils/tech_stack_detector.py:117`.
- Deliverables
  - Config updates; merging logic; fewer branches.
- Acceptance Criteria
  - Same exclusions computed for representative projects; CCN ≤ 6.

### WS6: Pattern Classifier – God Class Heuristics into Helpers

- Problem
  - `_detect_god_class.visit_ClassDef` bundles attribute/method counting and thresholding.
- Proposed Changes
  - Extract helpers: `count_methods(node)`, `count_unique_attrs(node)`, `compute_lines(node)`, `compute_severity(...)`.
- Affected Files
  - `shared/analyzers/quality/pattern_classifier.py:135`.
- Deliverables
  - Smaller visitor; helpers; unchanged behavior.
- Acceptance Criteria
  - Same matches on baseline corpus; CCN ≤ 6.

### WS7: Result Aggregator – Parameter Object for Filtering

- Problem
  - `get_filtered_results` takes 4 parameters (plus self), making 5.
- Proposed Changes
  - Introduce `ResultFilter` dataclass with fields `{priority, analysis_type, file_substr, min_confidence}` and a single `get_filtered_results(filter: ResultFilter)`.
- Affected Files
  - `shared/analyzers/quality/result_aggregator.py:667`.
- Deliverables
  - Dataclass; updated call sites.
- Acceptance Criteria
  - No behavior change; simpler signature.

## Phased Execution Plan

### Phase 1 (Week 1–2): Quick Wins

- WS1: Coverage – extract configs, remove legacy wrapper.
- WS3: Scalability – externalize patterns and add context object (no predicate refactor yet).
- WS4: Error Patterns – externalize patterns and add context object (no recommendation refactor yet).

### Phase 2 (Week 3–4): Structural Simplification

- WS2: Detect-Secrets – strict tool requirement + config extraction.
- WS3: Scalability – strategy predicates for `_should_flag_scalability_issue`.
- WS4: Error Patterns – table-driven `_get_language_recommendation`.
- WS7: Result Aggregator – parameter object.

### Phase 3 (Week 5–8): Hardening + Remaining Items

- WS5: Tech Stack Detector – declarative exclusions.
- WS6: Pattern Classifier – helpers for god class.
- Reinstate CI complexity gates and add snapshot regression checks.

## Progress Tracking

Use the table below to track status. Allowed values: `pending`, `in_progress`, `completed`.

| ID    | Task                                                               | Files                                                      | Status    | Owner | Notes |
| ----- | ------------------------------------------------------------------ | ---------------------------------------------------------- | --------- | ----- | ----- |
| WS1.1 | Extract coverage configs                                           | `shared/analyzers/quality/coverage_analysis.py:24`         | completed |       |       |
| WS1.2 | Remove legacy coverage wrapper                                     | `shared/analyzers/quality/coverage_analysis.py:290`        | completed |       |       |
| WS3.1 | Move scalability patterns to JSON                                  | `shared/analyzers/architecture/scalability_check.py:91`    | completed |       |       |
| WS3.2 | Add FileContext and refactor `_check_scalability_patterns`         | `shared/analyzers/architecture/scalability_check.py:352`   | completed |       |       |
| WS4.1 | Move error patterns/language patterns to JSON                      | `shared/analyzers/root_cause/error_patterns.py:90`         | completed |       |       |
| WS4.2 | Add ErrorScanContext and refactor `_check_targeted_error_patterns` | `shared/analyzers/root_cause/error_patterns.py:369`        | completed |       |       |
| WS2.1 | Extract detect-secrets config                                      | `shared/analyzers/security/detect_secrets_analyzer.py:39`  | pending   |       |       |
| WS2.2 | Remove degraded mode; hard-fail availability                       | `shared/analyzers/security/detect_secrets_analyzer.py:187` | pending   |       |       |
| WS3.3 | Strategy predicates for `_should_flag_scalability_issue`           | `shared/analyzers/architecture/scalability_check.py:460`   | pending   |       |       |
| WS4.3 | Table-driven `_get_language_recommendation`                        | `shared/analyzers/root_cause/error_patterns.py:645`        | pending   |       |       |
| WS7.1 | Introduce `ResultFilter` and update calls                          | `shared/analyzers/quality/result_aggregator.py:667`        | pending   |       |       |
| WS5.1 | Declarative exclusions for tech stacks                             | `shared/core/utils/tech_stack_detector.py:117`             | pending   |       |       |
| WS6.1 | Extract helpers in god class detector                              | `shared/analyzers/quality/pattern_classifier.py:135`       | pending   |       |       |

Add more rows as needed; keep statuses current. Consider placing this table at the top during active work for quick visibility.

## Baseline/Regression Testing Strategy

### Goals

- Guarantee that analyzer outputs (JSON) for representative targets are unchanged before and after refactors.
- Validate complexity reductions for targeted functions.

### Baseline Corpus

- Run against the repo itself (excluding `test_codebase/**`).
- Include small, curated files that trigger each target pattern to improve sensitivity (store under `shared/tests/integration/corpus/`).

### Commands (Baseline Snapshot Generation)

- Ensure `PYTHONPATH` includes `shared/` (repo root is fine).
- Use the registry CLI to generate JSON snapshots:
  - Coverage: `python -m core.cli.run_analyzer --analyzer quality:coverage --target . --output-format json > shared/tests/integration/baselines/pre/coverage.json`
  - Scalability: `python -m core.cli.run_analyzer --analyzer architecture:scalability --target . --output-format json > shared/tests/integration/baselines/pre/scalability.json`
  - Error Patterns (provide dummy error to satisfy requirement):
    - Example: `python shared/analyzers/root_cause/error_patterns.py . --error "TypeError in src/app.py:42" --output-format json > shared/tests/integration/baselines/pre/error_patterns.json`
  - Detect-Secrets: `python -m core.cli.run_analyzer --analyzer security:detect_secrets --target . --output-format json > shared/tests/integration/baselines/pre/detect_secrets.json`

Note: For error patterns, baseline must pass a stable `--error` string to avoid scanning unrelated files.

### Normalization For Diff

- Remove volatile fields: `timestamp`, `execution_time`, and ordering noise. Sort findings by `(analysis_type, file_path, line_number, id)`.
- Strip environment-specific fields if any.
- Suggested normalization script (store at `shared/tests/integration/tools/normalize_results.py`):
  - Read JSON, drop volatile keys, sort arrays deterministically, write normalized JSON.

### Post-Refactor Comparison

- Regenerate snapshots into `baselines/post/` with the same commands.
- Normalize both pre/post and compare with a JSON diff (`jq`/Python deep diff). Any semantic differences must be explained or fixed.

### Complexity Checks

- Lizard per target file:
  - Example: `lizard -C 999 -L 999 -a 999 shared/analyzers/architecture/scalability_check.py` to inspect CCN.
- Xenon gate (optional re-enable in CI after Phase 2): `xenon --max-absolute B --max-modules A --max-average A shared`.

### Unit Tests To Add

- Config loaders validate schema and handle missing/invalid keys.
- Strategy predicates (scalability) behave as expected for crafted snippets.
- Language recommendations resolve expected messages for crafted matches.

## CI/CD Integration

- Preconditions
  - Ensure `detect-secrets` is installed in CI before invoking security analyzer; fail fast if missing.
- Jobs
  - Run baseline analyzers (or a curated subset) and compare against committed baselines after normalization.
  - Run complexity checks and fail if targeted functions regress above thresholds.
- Artifacts
  - Upload normalized pre/post JSON and diff on failure for inspection.

## Definition of Done (per Workstream)

- All touched analyzers return identical findings on the baseline corpus.
- Targeted functions: length ≤ 50 lines (constructors/initializers) and CCN reduced to thresholds listed above.
- Parameter object refactors reduce positional parameters to ≤ 3 (excluding `self`).
- All configs moved to `shared/config/**` with schema validation and examples.
- No legacy wrappers or fallback logic remain in modified modules.

## Risks and Mitigations

- Config externalization introduces I/O and schema errors → add schema validation and unit tests; keep defaults minimal.
- Strict dependency enforcement (detect-secrets) breaks environments → document requirements; add install steps in CI.
- Snapshot flakiness → deterministic normalization and stable corpus; avoid scanning transient directories.

## Backlog (Optional)

- Minor fix (not part of primary scope): `shared/analyzers/quality/result_aggregator.py:707` uses `format.lower()` but should reference `output_format`. Address when refactoring WS7 if touched.

---

Maintainers: Update the Progress Tracking table as tasks move from `pending` → `in_progress` → `completed`. Attach links to PRs and test diffs in Notes.
