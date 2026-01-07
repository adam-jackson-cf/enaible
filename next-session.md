# Handoff: Instrument agentic readiness run timing

## Starting Prompt

The last session refactored the readiness prompt to call shared deterministic scripts and aligned the integration test with those scripts/exclusions, but the juice-shop fixture is still very slow (jscpd on `frontend/src` now runs ~60–90 s and the test is still executing in the background). For the next session, please:

- Attach to the running `uv tool run --python 3.12 pytest shared/tests/integration/test_agentic_readiness_workflow.py -k juice -vv` process (pid 61488) or wait for it to finish so you can capture diagnostics.
- Enhance the readiness workflow (prompt + shared scripts) to log timestamps around each analyzer invocation and helper script execution (recon, inventory, docs-risk, MCP scan, history/docs).
- Update the integration test to emit timings for each phase and optionally write a small per-step summary to `/tmp/agentic_readiness_test.log`.
- After instrumenting, rerun the test and capture the log to identify which tool/step dominates runtime; note any actionable configuration tweaks (exclusion tweaks, analyzer flags, or scoped targets) that could shorten the slowest phase.
- Keep the standard exclusion list and shared scripts in sync so we don’t regress the deterministic behavior.

## Relevant Files

- `shared/prompts/analyze-agentic-readiness.md` — orchestrates the workflow and now builds `AUTO_EXCLUDES`; update the instructions/commands here to emit timing details or to call helper scripts that record durations.
- `shared/context/agentic_readiness/*.py` — helper scripts that currently generate artifacts; they should log (or return) their start/finish times so the prompt can summarize them.
- `shared/tests/integration/test_agentic_readiness_workflow.py` — runs jscpd/coupling/lizard plus the helper scripts; add logging around analyzer runs (and perhaps a CSV/JSON summary) so the log file shows each stage’s duration.
- `/tmp/agentic_readiness_test.log` — currently just contains the pytest banner; use this file to append analyzer timing output so you can tail it while the test runs.

## Key Context

- The current background run (pid 61488) is what you’re monitoring; it already scopes jscpd to `frontend/src`.
- The main blocker is understanding why jscpd (and possibly other analyzers) takes so long despite the exclusions; adding per-step logging will tell us whether it’s the analyzer execution or the shared scripts where we should optimize.
- After you gather the data, we can revisit thresholds (e.g., greater min-tokens, more targeted excludes) or split jscpd into scoped runs if needed.
