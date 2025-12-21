# Mypy Strict Profile Migration Plan

Goal: migrate the entire repo to a single strict `mypy.ini` profile without introducing stubs, placeholders, or behavior regressions, while keeping cyclomatic complexity under 10 per function and preserving all existing CLI/analyzer functionality.

## Phase 0 – Baseline + Guardrails

- Confirm current gates: run `scripts/run-ci-quality-gates.sh` and note failing areas.
- Snapshot key metrics (mypy warnings count, affected modules) to compare after each phase.
- Create instrumentation checklist (files touched, tests to rerun, bd issue ID) so changes are auditable.

## Phase 1 – Config Unification (non-strict default + per-package strict)

- Move CLI `[tool.mypy]` settings into root `mypy.ini` and scope them under `[mypy-tools.enaible.*]`.
- Ensure shared packages import via `shared.*` with package `__init__.py` files.
- Update CI + local hook script to run a single `uv run mypy --config-file mypy.ini shared tools/enaible/src` command.
- Verify CLI remains strict by intentionally seeding a missing type and ensuring mypy fails in this phase.

## Phase 2 – Analyzer Core Hardening

- Target shared/core/\* first: add missing type hints, narrow return types, and break up complex helpers (>10 branches) into helpers to keep complexity under 10.
- Remove `Any` propagation from registries, validation rules, and config loaders; prefer TypedDict/dataclasses.
- Expand unit tests covering analyzer registry outputs to ensure new annotations match runtime behavior.

## Phase 3 – Domain Analyzer Modules

- Migrate analyzers one domain at a time (security → performance → architecture → root_cause) to strict mode by tightening function signatures and adding helper types.
- Avoid stubs; rely on concrete helper modules or TypedDicts for shared schemas.
- After each domain, temporarily enable `strict = true` via `mypy.ini` overrides for that package and fix reported issues before moving on.

## Phase 4 – CLI + Installer Parity

- Once shared modules are strict, remove per-package overrides so the entire config runs with global strict settings.
- Re-run CLI workflows (`enaible prompts lint`, `enaible install codex`, etc.) to confirm strict typing didn’t break runtime behavior.
- Update `scripts/run-ci-quality-gates.sh` to fail fast when any mypy warning appears.

## Phase 5 – Final Verification + Cleanup

- Delete any temporary overrides, confirm only one strict `mypy.ini` remains.
- Run full quality gates + targeted analyzer tests + sampled prompt renders to ensure no regressions.
- Document lessons learned and required ongoing maintenance steps in `AGENTS.md`.
