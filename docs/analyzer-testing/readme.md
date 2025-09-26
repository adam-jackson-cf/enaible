# Analyzer Testing Guide

Use this reference when modifying analyzer logic or their declarative configuration. It explains where configuration lives, how to generate comparable baselines, and how to store normalized reports.

## Configuration Catalog

The analyzers now load large static data from JSON under `shared/config/`:

- `coverage/`
  - `languages.json` – language-specific coverage heuristics.
  - `indicators.json` – shared coverage scoring signals.
- `security/detect_secrets.json` – detect-secrets CLI configuration (plugins, filters, file filters). The analyzer aborts if the CLI is missing.
- `patterns/scalability/*.json` – database, performance, concurrency, and architecture pattern definitions consumed by the scalability analyzer.
- `patterns/error/patterns.json` – canonical error categories/patterns used for all languages.
- `patterns/error/language_patterns.json` – language-specific supplements (extensions → pattern lists). These layer on top of the general definitions.
- `patterns/error/error_type_map.json` – maps runtime error labels (e.g., `TypeError`) to pattern identifiers (`"__all__"` denotes every available pattern); includes default fallbacks used by the analyzer.
- `tech_stacks/tech_stacks.json` – stack definitions and exclusion rules (consumed by the tech-stack detector).

When changing any of these files, regenerate baselines and record the intent in your change notes.

## Baseline Normalization Workflow

1. Produce raw analyzer JSON (pre/post change). Example:
   ```bash
   PYTHONPATH=shared python -m core.cli.run_analyzer --analyzer architecture:scalability --target . --output-format json > tmp/scalability.json
   ```
2. Normalize the output to strip volatile fields and make diffs stable:
   ```bash
   python shared/tests/integration/tools/normalize_results.py tmp/scalability.json scalability-current.json
   ```
   - With a filename only, the normalizer writes to `docs/analyzer-testing/reports/` by default.
   - Use `--reports-dir` to override the target directory.
3. Compare the normalized outputs (`git diff`, `jq --diff`, or a JSON deep-diff). Explain any intentional change in your PR description.

### Normalizer Reference

- Script: `shared/tests/integration/tools/normalize_results.py`
- Responsibilities:
  - Drops `timestamp`, `execution_time`, and per-finding `id` fields.
  - Canonicalizes file paths relative to the repository root.
  - Sorts findings deterministically (path, line, JSON payload).
  - Honors `--reports-dir` and defaults to `docs/analyzer-testing/reports/`.
- Run `python .../normalize_results.py --help` for full usage.

## Stored Baselines

Current normalized baselines live alongside this document:

- `docs/analyzer-testing/reports/coverage-current.json`
- `docs/analyzer-testing/reports/scalability-current.json`
- `docs/analyzer-testing/reports/error-patterns-current.json`
- `docs/analyzer-testing/reports/detect-secrets-current.json`

Keep prior references (for example `*-legacy.json`) if you need to preserve historical behaviour for comparison.

## Validation Checklist

- [ ] Configuration change documented (commit/PR notes).
- [ ] Raw analyzer outputs generated before and after the modification.
- [ ] Normalized reports written to `docs/analyzer-testing/reports/`.
- [ ] Diffs reviewed; behavioural shifts explained.
- [ ] Relevant tests or static checks executed.

Following this process ensures analyzer refactors remain regression-safe and auditable.
