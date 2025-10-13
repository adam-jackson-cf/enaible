# Analysis Improvements Plan

This document tracks the dependency simplification and analyzer upgrades.

## Objectives

- [x] Replace Python-only duplication analyzer with jscpd (Node) in base profile
- [x] Move ESLint into base profile (ensure install in all installers)
- [x] Replace flake8/perflint with Ruff for Python performance
- [x] Replace SQLFluff with SQLGlot for SQL analysis
- [x] Add universal performance analyzer via Semgrep (deferred install)
- [x] Keep Lizard for cross-language complexity and add light batching/caching
- [x] Remove unused Python analyzer deps from base requirements
- [x] Update prompts, registry, and docs to reflect new analyzers
- [x] Update installers (systems/claude-code, systems/opencode, systems/codex) to set up Node tools (ESLint + jscpd)
- [x] Ensure tests and integration suite pass

## Tasks

### Analyzers

- [x] Add `quality:jscpd` at `shared/analyzers/quality/jscpd_analyzer.py`
- [x] Remove `shared/analyzers/quality/code_duplication_analyzer.py`
- [x] Add `performance:ruff` at `shared/analyzers/performance/ruff_analyzer.py`
- [x] Remove `shared/analyzers/performance/flake8_performance_analyzer.py`
- [x] Add `performance:sqlglot` at `shared/analyzers/performance/sqlglot_analyzer.py`
- [x] Remove `shared/analyzers/performance/sqlfluff_analyzer.py`
- [x] Add `performance:semgrep` at `shared/analyzers/performance/semgrep_analyzer.py` (deferred install)
- [x] Add light Lizard metrics caching to architecture analyzers

### Prompts & Registry

- [x] Update `shared/prompts/analyze-code-quality.md` to include jscpd
- [x] Update `shared/prompts/analyze-performance.md` to use Ruff + SQLGlot + Semgrep
- [x] Note deferred install in `shared/prompts/analyze-security.md`
- [x] Update `shared/core/base/registry_bootstrap.py` to register new analyzers and remove old ones

### Requirements & Utils

- [x] Trim `shared/setup/requirements.txt` to base deps (lizard, ruff, sqlglot, detect-secrets, infra)
- [x] Add tool detection helpers at `shared/core/utils/tooling.py`

### Installers

- [x] systems/claude-code/install.sh: add jscpd to Node tools, remove SQLFluff checks
- [x] systems/claude-code/install.ps1: same as above
- [x] systems/opencode/install.sh: same as above
- [x] systems/codex/install.sh: add Node tools (ESLint + jscpd) setup

### CI/Docs/Tests

- [x] Ensure CI runners have Node for base
- [x] Unit tests for Ruff/SQLGlot/jscpd mappers (minimal happy-path)
- [x] Smoke integration run on `test_codebase/*`

## Validation Checklist

- [x] All prompts execute with new analyzers
- [x] No references to flake8/perflint/sqlfluff or Python duplication analyzer
- [x] Installers set up ESLint + jscpd by default
- [x] `PYTHONPATH=shared pytest shared/tests -v` passes locally
- [x] Integration suite passes
