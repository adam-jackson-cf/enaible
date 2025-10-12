# Purpose

Convert an unstructured planning artifact into a Linear-ready plan by orchestrating gated subagents, clarification loops, hashing, and optional mutation.

## Variables

- `TASK_INPUT` ← value passed to `--task` (string, file path, or stdin).
- `PROJECT_ID` ← `--linear-project-id` (optional).
- `CONFIG_PATH` ← explicit `--config` path (optional).
- `ESTIMATE_STYLE` ← value from `--estimate-style` (default `tshirt`).
- `MAX_SIZE` ← value from `--max-size` (default from config).
- `DRY_RUN` ← boolean flag when `--dry-run` present.
- `AUTO_MODE` ← boolean flag when `--auto` present.
- `DIFF_BASE` ← value from `--diff` (optional).
- `$ARGUMENTS` ← raw argument string.

## Instructions

- ALWAYS validate arguments and configuration before invoking subagents; reject unknown flags.
- NEVER mutate Linear issues unless readiness is confirmed, the user approves, and `--dry-run` is absent.
- Maintain deterministic artifacts: stable ordering, consistent slug generation, hash integrity.
- Pause at every confirmation gate (`objective`, `readiness`, `transfer`) unless `AUTO_MODE` is active.
- Trust `@agent-linear-hashing` for all hash computations and differencing; do not recompute locally.

## Workflow

1. Prepare workspace
   - Run `mkdir -p .workspace && test -w .workspace`; exit immediately if the planning workspace cannot be created or written.
2. Parse and validate arguments
   - Ensure `--task` present; error with exit code 1 otherwise.
   - Normalize optional flags (`--linear-project-id`, `--config`, `--estimate-style`, `--max-size`, `--dry-run`, `--auto`, `--diff`).
3. Initialize workspace
   - Confirm `.workspace` directory exists; create if missing.
   - Resolve configuration by checking explicit `--config`, then `.claude/linear-plan.config.json`, then `$HOME/.claude/linear-plan.config.json`; exit with `CONFIG_NOT_FOUND` if none are available.
   - Compute `config_fingerprint = sha256(sorted JSON excluding volatile fields)`; abort on missing mandatory keys (`label_rules`, `complexity_weights`, `thresholds`, `decomposition`, `audit_rules`, `idempotency`).
4. Acquire artifact
   - Resolve `TASK_INPUT` from argument value or stdin/file content.
   - On empty artifact, emit `EMPTY_ARTIFACT` error envelope and exit with code 1.
5. Objective definition
   - Invoke `@agent-linear-objective-definition` with the raw artifact.
   - Derive `cycle_slug = kebab_case(task_objective)`; create `.workspace/<cycle_slug>` (`CYCLE_DIR`).
   - Persist `linear-objective-definition-output.json` within `CYCLE_DIR`.
6. Clarification loop
   - Summarize objective, purpose, affected users, requirements, constraints, and open questions.
   - Collect user responses to `open_questions`; append to `cycle_plan_report.json.objective.clarifications`.
   - **STOP:** “Objective frame prepared. Provide clarifications or type proceed to continue.” Wait unless `AUTO_MODE`.
7. Autonomous planning loop
   - Sequentially invoke subagents, storing `<agent>-input.md`, `<agent>-summary.md`, `<agent>-output.json` inside `CYCLE_DIR`:
     1. `@agent-linear-issue-decomposer`
     2. If `ESTIMATE_STYLE=tshirt`, `@agent-linear-estimation-engine`
     3. `@agent-linear-acceptance-criteria-writer`
     4. `@agent-linear-hashing`
   - Update `cycle_plan_report.json` after each invocation.
   - Abort with exit code 4 on structural integrity violations.
8. Readiness check
   - Invoke `@agent-linear-readiness`; append findings to the report.
   - If `ready=false`, exit with code 2 unless remediation requested.
   - **STOP:** “Plan formed and readiness check successful, proceed with transfer to Linear? (y/n)” Await confirmation unless `AUTO_MODE`.
9. Optional mutation (executed only when approved and not `DRY_RUN`)
   - Preflight duplicates with `@agent-linear-issue-search` when `PROJECT_ID` provided.
   - Invoke `@agent-linear-issue-writer` followed by `@agent-linear-dependency-linker`.
   - Validate hashes unchanged; append mutation results to the report.
   - On mutation failures, emit exit code 3.
10. Finalization

- Persist `cycle_plan_report.json` and any diff info (`DIFF_BASE`).
- Surface summary, readiness state, mutation results, and artifact locations.

## Output

```md
# Cycle Plan Report

- Summary: Plan created for "<task_objective>" (slug: <cycle_slug>).
- Readiness: <ready|not ready> (findings: <count>)
- Mutation: <skipped|completed|dry-run>

## ARTIFACTS

- Report: .workspace/<cycle_slug>/cycle_plan_report.json
- Objective: .workspace/<cycle_slug>/linear-objective-definition-output.json
- Issue Graph: .workspace/<cycle_slug>/@agent-linear-issue-decomposer-output.json
- Hashes: .workspace/<cycle_slug>/@agent-linear-hashing-output.json

## EXIT CODES

- 0: Success (planning complete; mutation optional)
- 1: Argument/config validation failure
- 2: Readiness failure or blocking validation
- 3: Linear mutation failure
- 4: Structural integrity violation

## NEXT STEPS

- For readiness=false: address findings and rerun planning.
- For mutation skipped: rerun with `--auto` or user approval when ready.
```

## Examples

```bash
# Plan from inline artifact with estimation
/plan-linear --task "Implement OAuth2 integration" --estimate-style tshirt

# Plan using artifact file and skip mutation
/plan-linear --task ./docs/auth-plan.md --linear-project-id LINPROJ-123 --dry-run
```
