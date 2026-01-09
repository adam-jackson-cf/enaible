# Agentic Readiness Repo Improvement Plan

We will extend this plan as new gaps against `docs/reference/todos/agentic-readiness/agentic-guidance.md` emerge. Each section below tracks one currently known misalignment plus the concrete remediation steps.

## 1. README Documentation Overload

- **Issue**: `README.md` repeats the full prompt catalog, command reference, and workflow tables that already exist in the generated artifacts/CLI help, conflicting with IFCD-2 and CE-6 (implementation should be the source of truth, system docs must stay lean).
- **Plan**:
  1. Trim the README “Common Workflows,” “Complete Prompt Reference,” and skills tables down to short orientation blurbs.
  2. Replace the removed sections with links to deterministically generated references (e.g., `enaible prompts list`, rendered prompt docs).
  3. Add a guard in the docs release checklist that blocks PRs which reintroduce long-form prompt catalogs into README.md.

## 2. `get-codebase-primer` Prompt (Lack of Deterministic Steps)

- **Issue**: `shared/prompts/get-codebase-primer.md` tells agents to manually read docs and analyze architecture without using repo-provided analyzers or logging artifacts, violating CGSD-3 and CLDC-1.
- **Plan**:
  1. Introduce a Step 0 that runs scripted recon (`shared/context/...` helpers) and writes artifacts to `.enaible/artifacts/get-codebase-primer/<run>/`.
  2. Require the Enaible CLI analyzers (architecture, code-quality, security) to populate the sections that are currently pure narration.
  3. Update the output template so every claim cites the produced artifacts instead of inline prose.
  4. Add lint to ensure prompts referencing “Deep Analysis” also enumerate the deterministic commands they depend on.

## 3. Research Skill (Deterministic Scaffold Required)

- **Issue**: `shared/skills/research` is entirely prose-driven; no deterministic scripts capture requirements, log searches, or assemble reports. This conflicts with CLDC-1/2 and VFCR-5.
- **Detailed Plan**:
  1. **Preflight Script & Artifact Root**
     - Add `scripts/research_init.py` to create `ARTIFACT_ROOT`, record request metadata, and emit `requirements.json`.
     - Amend `SKILL.md` Step 0 to mandate running this script before any research begins.
  2. **Deterministic Domain Mapping**
     - Build `scripts/research_domain_plan.py` that classifies each research question using a ruleset (`references/domain-map.yaml`) and produces `domain-plan.json`.
     - Document an override workflow so agents adjust domains via CLI flags rather than free-form edits; all overrides saved under `ARTIFACT_ROOT`.
  3. **Search Execution Logging**
     - Provide `scripts/research_execute.py` that wraps @WEB_SEARCH/@WEB_FETCH calls, logging query, engine, timestamp, and resulting URL into `search-log.json`.
     - Make this a blocking step; Step 2 cannot proceed unless the log confirms ≥3 sources per key question.
  4. **Validation & Citation Enforcement**
     - Create `scripts/research_validate.py` to enforce minimum source counts, recency windows, and confidence tagging, failing fast if requirements aren’t met.
     - Add `scripts/research_citations.py` to verify that every synthesized finding maps to logged sources.
  5. **Deterministic Report Assembly**
     - Replace the prose “Report Generation” step with `scripts/research_report.py` that inputs validated artifacts and emits the final markdown/JSON deliverable.
     - Update `references/report-structure.md` to describe the script’s CLI flags and expected schema rather than manual formatting instructions.
  6. **Skill Documentation Updates**
     - Revise `SKILL.md` to reference each script explicitly, keeping the progressive disclosure pattern from `shared/skills/skills.md`.
     - Expand the “Quality Standards” section to require attaching `requirements.json`, `domain-plan.json`, `search-log.json`, validation output, and report artifacts to every handoff.

## 4. `get-task-primer` Prompt (Manual Recon Without Artifacts)

- **Issue**: `shared/prompts/get-task-primer.md` instructs broad manual exploration (“dispatch parallel task agents,” adhoc `ls/rg/git` usage) but never requires Enaible analyzers or artifact capture, violating CGSD-3 plus CLDC-1/CLDC-2 (permanent workflows must rely on deterministic commands).
- **Plan**:
  1. Add a Step 0 mirroring other analyzer prompts that resolves @TARGET_PATH, builds `.enaible/artifacts/get-task-primer/<timestamp>/`, and exports the directory for downstream steps.
  2. Replace the “Deep Analysis” prose with explicit CLI invocations (architecture/code-quality/security analyzers) scoped by @TARGET_PATH + @EXCLUDE_GLOBS, storing JSON outputs beneath the artifact root.
  3. Pipe all git history/status commands into dated artifact files so findings are auditable rather than purely narrative.
  4. Update the output template to cite artifact filenames and require referencing analyzer findings instead of freehand descriptions.

## 5. Codify PR Reviews (Favor Deterministic Enforcement Before Docs)

- **Issue**: The skill currently drives agents to strengthen system doc rules first, even when gaps could be solved by lint/tests, clashing with CGSD-3 and IFCD-5.
- **Plan**:
  1. Update `shared/skills/codify-pr-reviews/SKILL.md` to require tooling/doc inventory + coverage comparison before drafting system rules, and to record enforcement choices in `approved-enforcement.json`.
  2. Add deterministic helpers for `patterns.json`, tooling inventory, doc rules inventory, coverage comparison, and enforcement outputs so tooling vs doc paths are explicit before any drafting occurs.
  3. Modify rule templates and drafting to include a “Deterministic enforcement?” section that cites `coverage.json` when tooling is feasible.
  4. Ensure the apply step logs whether changes went into tooling, docs, or both, applying updates from `tooling-changes.md/.json` alongside doc edits.

We will append new sections here as we discover additional deviations from the agentic readiness guidance.
