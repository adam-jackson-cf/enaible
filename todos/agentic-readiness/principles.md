# Agentic Readiness Principles

- Linting enforcement: linting must block commits in both pre-commit and CI.
- Linting default: any rule that can be enforced via linting must live in linting; guidance/rules docs must never be the sole source for enforceable rules.
- Code quality and style enforcement: quality/style rules are enforced through linting, not guidance/rules docs (for example, AGENTS.md).
- Test enforcement: integration/smoke tests are the primary readiness signal and must be wired into both pre-commit and CI; tests must execute real implementations with tangible outputs (not mock-driven).
- Deterministic tooling over docs: rules should be encoded in executable gates/configs (CI, lint, test runners); documentation is never a positive signal by default.
- Documentation scope: docs only cover behavior that cannot be inferred from code, and may provide high-level area maps (no file-level pointers).
- Documentation naming: LLM-targeted docs must avoid standard auto-included names (for example, AGENTS.md); standard names are flagged for investigation and can reduce readiness when misused.
- Doc usage affects scoring: if docs encode enforceable rules or describe code-inferable behavior, it is a readiness risk and should reduce KPI when confirmed.
- MCP prohibition: any MCP configuration/registration in the repo is problematic and flagged as a readiness risk.
- CI/local parity: any mismatch between local gates and CI gates is a readiness risk.
- Guidance/rules must include standards criteria for LLM code reviews.

## Summary

- `shared/prompts/analyze-agentic-readiness.md`: Defines a deterministic, artifact-driven readiness and maintenance assessment. It enforces CLI-only analyzer use, writes all evidence under `@ARTIFACT_ROOT`, and does not mutate the repo. The workflow is prescriptive and traceable: recon, analyzers (jscpd, coupling, lizard), tests/gates/enforcement, documentation risk, MCP scan, git-based concentration and docs freshness, KPI formulas, and a structured report.
- `shared/tests/integration/test_agentic_readiness_workflow.py`: Reproduces the prompt logic deterministically on a fixture repo and validates key invariants (scores in [0,1], evidence files exist). It uses analyzers directly in test context (as allowed in tests), then applies the same recon/inventory/scoring logic for parity, with explicit skip logic for missing CLI tooling.
- `shared/prompts/analyze-code-quality.md`: Shows the standard shared prompt structure and the evidence-first pattern: CLI analyzers only, artifacts under `.enaible/artifacts/...`, recon before analyzers, and explicit coverage gap analysis.
- `shared/prompts/AGENTS.md`: Documents how to create and register new shared prompts: author `shared/prompts/<name>.md`, register in `tools/enaible/src/enaible/prompts/catalog.py`, run lint/render/diff, and install to sync managed outputs.

## analysis

Here’s what I’d change in shared/prompts/analyze-agentic-readiness.md to align with todos/agentic-readiness/principles.md and make the assessment explicitly about migration readiness to those principles (vs. generic readiness):

### Add/adjust signals to reflect principles, not just presence of docs

- Lint enforcement (critical): add a dedicated signal that verifies linting blocks commits and CI (e.g., presence of pre-commit hook + CI job that runs lint and fails on violations). Current quality-gates.json only detects “lint mentioned somewhere.” That should become a hard, evidence-backed gate.
- Lint default as source of truth: detect rules encoded in lint configs vs docs. Flag any rules text found in AGENTS.md/CONTRIBUTING.md/README.md that appears to describe enforceable rules not mirrored in lint configs. That should reduce readiness.
- Test enforcement priority: explicitly detect integration/smoke tests wired into both pre-commit and CI, not just presence of hard-test dirs. The principle says these are primary readiness signals.
- CI/local parity (strict): treat any parity_gaps as a readiness penalty rather than just a reported gap. It’s explicitly a risk.

### Invert/penalize documentation signals

- Docs should not be positive signals by default: the current guidelines_score rewards presence of docs. Per principles, docs are neutral or a risk if they encode enforceable behavior. Replace
  - If docs only provide high-level maps and non-inferable behavior → neutral
- Doc naming risk: add a check for AGENTS.md and other “auto-included” names. The principles say those are flagged for investigation; that should reduce readiness when present.
- Doc exposure scoring: currently only checks docs presence and references. Add a “doc-overreach” detector (heuristic search for “must/required/should” + tooling terms) to flag where docs are the only enforcement.

- Right now the KPI is generic (duplication/coupling/docs freshness). Add principle compliance deltas:
  - Lint blocking in pre-commit + CI (binary)
  - CI/local parity (binary)

### Update output to explicitly state migration blockers

- Add a “Migration blockers” section that maps directly to principles:
  - “Linting not blocking commits in pre-commit and CI”
  - “CI/local gate mismatch”
  - “Hard tests not wired into gates”
  - “Docs encode enforceable rules”
  - “MCP config present”
- This makes the output actionable for moving toward the principles.

### Concrete prompt edits (where)

- In Step 4 (Inventory tests & gates): expand to parse pre-commit config and CI workflows for explicit fail-on-lint steps; compute parity and “lint blocking” boolean.
- In Step 5 (Guidelines/guardrails/docs exposure): switch guidelines_score to a doc-risk detection heuristic and add agents.md penalty.
- Add a new Step for MCP scan (e.g., scan for mcp.json, .mcp/, mcp.config, or known MCP registration references).
