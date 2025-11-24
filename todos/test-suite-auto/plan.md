# OpenCode Prompt E2E Automation Plan

## Context

We now have a working tmux-based harness that drives the OpenCode prompts end-to-end using the new `--auto` flag. The next step is to expand coverage so every shared prompt can be executed non-interactively against lightweight fixtures, ensuring prompt drift is caught automatically.

## Tasks

- [x] Prototype harness: run `/analyze-security … --auto` through tmux and capture logs
- [x] Add `--auto` handling to:
  - [x] `analyze-security`
  - [x] `plan-refactor`
  - [x] `plan-solution`
- [x] Extend `--auto` handling to remaining prompts
  - [x] `analyze-architecture`
  - [x] `analyze-code-quality`
  - [x] `analyze-performance`
  - [x] `analyze-root-cause`
- [x] `plan-ux-prd`
  - _Completed 2025-11-03 with consistent STOP bypass pattern._
  - [x] `create-project`
  - [x] `setup-dev-monitoring`
  - [x] `setup-package-monitoring`
  - [x] `get-feature-primer`
  - [x] others (review `shared/prompts/*.md` for STOP checkpoints)
- [x] Create minimal fixtures per prompt under `shared/tests/integration/fixtures/prompt-e2e/`
  - Added richer sample repo signals (Next.js frontend, FastAPI backend, manifests) plus plan/rules/report targets.
- [x] Update `systems/codex/prompt-manifest.json`
  - [x] Add each prompt entry with fixture arguments (including `--auto`)
  - [x] Record stable success markers per prompt
- [x] Prototype tmux-driven parallel orchestrator
  - Script: `shared/tests/integration/tools/codex_prompt_orchestrator.py`
  - Handles per-prompt tmux sessions up to configurable concurrency and performs marker validation.
- [x] Replace heavy fixture with minimal target repo for fast runs
  - New contents under `shared/tests/integration/fixtures/prompt-e2e/sample-repo/` keep the workload to a single Python module.
- [x] Validate orchestrator by running analysis prompts (max parallel 5) and reviewing summary output
  - 2025-11-03: `python shared/tests/integration/tools/codex_prompt_orchestrator.py --max-parallel 3`
- [ ] Update `.enaible/prompt-e2e/codex.json` cache once orchestrator run succeeds
- [ ] Document the orchestrator workflow in `docs/testing.md`
