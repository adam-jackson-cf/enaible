---
description: Generate a foundation-first Linear project plan (or attach to existing) with decomposed, self-contained issues
---

# plan-linear v1.0

**Mindset**: "Foundation first → determinism → explicit phase gates → zero ambiguity in issue briefs."

This command converts a raw planning artifact (task outline, PRD, feature description) into a validated Linear project plan with fully enriched, dependency-linked issues. It enforces a phased workflow with explicit STOP confirmations to prevent premature creation.

## Phase Overview

| Phase | Purpose                               | Primary Subagents                                                                                                |
| ----- | ------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| 1     | Artifact Intake & Classification      | @linear-artifact-classifier                                                                                      |
| 2     | Context Harvest & Research Foundation | @linear-context-harvester, @research-coordinator (+ @technical-researcher, @docs-scraper, optional @ux-designer) |
| 3     | Design Synthesis & Decomposition      | @linear-design-synthesizer, @linear-issue-decomposer                                                             |
| 4     | Estimation & Enrichment               | @linear-estimation-engine, @linear-acceptance-criteria-writer                                                    |
| 5     | Quality Audit & Dry Run               | @linear-quality-auditor (optional @linear-orchestrator snapshot)                                                 |
| 6     | Linear Execution                      | @linear-issue-writer, @linear-dependency-linker                                                                  |

Each phase produces a structured JSON object passed forward. All transformations MUST be deterministic given identical inputs + config.

---

### Phase 0: Configuration Resolution (Implicit)

1. Resolve CONFIG_PATH (do NOT skip):
   1. Try project-level: `.opencode/linear-plan.config.json`
   2. Try user-level: `$HOME/.config/opencode/linear-plan.config.json`
   3. If neither exists → **STOP** ask user: "Provide full path to linear plan config JSON:" then validate readable JSON schema.
2. Load config → expose: `label_rules`, `complexity_weights`, `thresholds`, `decomposition`, `audit_rules`, `idempotency`.
3. If `--config <path>` supplied, override all above with that file.

> If config missing required keys → abort with remediation checklist (DO NOT infer defaults beyond hardcoded safe fallbacks in subagents).

---

### Phase 1: Artifact Intake & Classification

1. Gather / confirm user artifact. If incomplete, request missing: objectives, constraints, success criteria, known risks.
2. Invoke:

```json
@linear-artifact-classifier
{"input_mode":"{auto|tasks|prd|feature}","raw_artifact":"...user text...","config":{"glossary_terms":true}}
```

3. Receive output: `artifact_type`, `features[]`, `constraints[]`, `user_journeys[]`, `assumptions[]`, `glossary_terms[]`, `open_questions[]`.
4. Summarize extracted structure to user.

**STOP** → "Proceed to context harvest & research? (y/n)"

Abort if user declines; allow edits to raw artifact then rerun classifier.

---

### Phase 2: Context Harvest & Research Foundation

1. Invoke repository scan:

```json
@linear-context-harvester
{"paths":["."],"languages":true,"frameworks":true,"infra":true}
```

2. If novel tech decisions implied (e.g. new datastore, architecture shift), coordinate research:

```json
@research-coordinator
{"objectives":["Validate technology choices","Identify established patterns"],"domains":["architecture","performance"],"depth":"standard"}
```

> This may internally invoke @technical-researcher, @docs-scraper, optionally @ux-designer if user journeys are unclear.

3. Merge outputs into `context_profile` + `research_blueprint`.

**STOP** → "Proceed to design synthesis & decomposition? (y/n)"

---

### Phase 3: Design Synthesis & Decomposition

1. Synthesize design:

```json
@linear-design-synthesizer
{"features": [...], "context_profile": {...}, "research_blueprint": {...}}
```

> Output: `architecture_decisions[]`, `subsystem_map[]`, `foundation_tasks[]`, `sequencing_principles[]`.

2. Decompose issues foundation-first:

```json
@linear-issue-decomposer
{"features": [...], "foundation_tasks": [...], "constraints": [...], "sequencing_principles": [...], "max_depth": <config.decomposition.max_depth>}
```

> Output: `issues[]` (raw: id, provisional_title, rationale, category, parent?, deps[], risk, initial_sections{}).

**STOP** → "Proceed to estimation & enrichment? (y/n)"

---

### Phase 4: Estimation & Enrichment

1. Complexity scoring:

```json
@linear-estimation-engine
{"issues": [...], "complexity_weights": {...}, "thresholds": {...}}
```

> Output: issues with `rcs`, `size`, `oversize_flag`.

2. If `oversize_flag=true` for any issue and size > `--max-size` (or config limit), re-invoke `@linear-issue-decomposer` with `split_target_ids`.
3. Acceptance criteria + Definition of Done enrichment:

```json
@linear-acceptance-criteria-writer
{"issues": [...], "glossary_terms": [...], "project_objectives": [...]}
```

> Output: adds `acceptance_criteria[]`, `definition_of_done[]`, `implementation_guidance[]`.

**STOP** → "Proceed to audit & dry run preview? (y/n)"

---

### Phase 5: Quality Audit & Dry Run Preview

1. Audit:

```json
@linear-quality-auditor
{"issues": [...], "label_rules": {...}, "thresholds": {...}, "glossary_terms": [...], "enforce_sections": true}
```

> Output: `findings[] {severity, code, message, issue_id?}`, `label_assignments[]`, `canonical_terms[]`, `dependency_suggestions[]`.

2. Build dry-run preview JSON:

```json
PlanPreview {
  project: { existing: bool, identifier?, proposed_name? },
  totals: { issues, foundation, feature, risks },
  complexity_table: [{id,title,rcs,size}],
  labels_applied: { by_category: {...} },
  glossary: [...],
  dependencies_proposed: [...],
  audit: { errors:[], warnings:[] }
}
```

3. If any `audit.errors` → report and **STOP** (must remediate before creation). Do not proceed automatically.

**STOP** → "Create/Update Linear now? (y/n)" (Use `--dry-run` to stop here always.)

---

### Phase 6: Linear Execution & Dependency Linking

If `--dry-run` set → skip and print PlanPreview JSON.

1. Create project if needed:

```json
@linear-issue-writer
{"mode":"project_init_if_absent","project_name":"...","project_description":"...","artifact_hash":"..."}
```

2. Create / update issues idempotently:

```json
@linear-issue-writer
{"mode":"issue_batch","project_id":"...","issues": [...], "label_assignments": [...], "hash_footer": true}
```

> Output: `created_issue_ids[]`, `skipped_issue_ids[]`, `hash_index{}`.

3. Dependency linking (blocking edges):

```json
@linear-dependency-linker
{"project_id":"...","dependencies": [...], "strategy":"blocker"}
```

4. Post-creation verification (re-fetch subset by IDs to confirm labels & descriptions contain expected footers).

**STOP** → "Plan creation complete. Output summary ready."

---

## Minimal Idempotency Interface

The command only inspects:

- Issue body footer markers: `<!-- plan-hash:... -->` + `<!-- plan-version:1 -->`
- Project description footer: `<!-- linear-plan-meta: artifact-hash=<sha256>; version=1 -->`

Hash computation & section assembly are owned entirely by subagents (decomposer, estimation, acceptance, writer). The command never recomputes hashes—only matches.

---

## Body Section Contract (Reference Only)

Canonical issue body assembly rules live in `opencode/agent/linear-issue-writer.md`. The config (`opencode/linear.plan.config.json`) may include a `sections_order` and `footer_format` for validation or future tooling, but the writer spec is the source of truth—if any divergence arises, the writer spec governs. The orchestrator never reorders or formats sections; it transports structured fields to the writer.

Section production responsibilities (exact case-sensitive keys):

- Decomposer: `Context`, `Scope` (in `initial_sections`)
- Estimation Engine: `Estimation` object (`size`, `rcs`, optional `oversize_flag` upstream only for control flow)
- Acceptance Criteria Writer: `Implementation Guidance`, `Definition of Done` (array), `Acceptance Criteria` (array)
- Auditor: Reads all sections (no mutation); validates presence of mandatory sections when `enforce_sections=true`
- Writer (assembly only): Assembles `Dependencies` from upstream ids, adds `Labels`, `Risks & Mitigations`, `Terminology References`, optional `Branch & PR Guidance`, plus HTML footers (`plan-hash`, `plan-version`, `project-id`).

Contract Rules:

- Upstream subagents MUST NOT emit footer markers.
- Section keys must match exactly; unknown keys are passed through but will appear after canonical sections when rendered (avoid introducing new ones without updating writer spec).
- Orchestrator does not compute or verify hashes beyond matching footers (see Minimal Idempotency Interface).

If a future section is added, update only the writer spec and (optionally) this contract summary—do not embed full templates here.

---

## Subagent Invocation Reference (Summary)

| Subagent                           | Required Input Keys            | Critical Output Keys                                      |
| ---------------------------------- | ------------------------------ | --------------------------------------------------------- |
| @linear-artifact-classifier        | raw_artifact, input_mode       | features[], constraints[], user_journeys[]                |
| @linear-context-harvester          | paths[]                        | frameworks[], languages[], existing_modules[]             |
| @linear-design-synthesizer         | features[], context_profile    | architecture_decisions[], foundation_tasks[]              |
| @linear-issue-decomposer           | features[], foundation_tasks[] | issues[] (raw)                                            |
| @linear-estimation-engine          | issues[], complexity_weights   | issues[] (rcs,size)                                       |
| @linear-acceptance-criteria-writer | issues[], glossary_terms[]     | issues[] enriched (acceptance_criteria, DoD)              |
| @linear-quality-auditor            | issues[], label_rules          | findings[], label_assignments[], dependency_suggestions[] |
| @linear-issue-writer               | project/issue batch payload    | created_issue_ids[], skipped_issue_ids[]                  |
| @linear-dependency-linker          | dependencies[], project_id     | applied_edges[], cycle_warnings[]                         |

> All subagents MUST return machine-parsable JSON root objects (no prose wrappers). If an error occurs, return `{ "error": { "code": "...", "message": "..." } }`.

---

## Failure Policy

- Any `audit.errors` → abort before creation.
- Permission/rate limit from Linear → surface and abort; do NOT retry automatically.
- Missing required section in enriched issue → mark as error `ISSUE_SECTION_MISSING`.
- Dependency cycle attempt → remove newest edge and record warning.

---

## $ARGUMENTS

- `--project <identifier>` Existing Linear project (UUID | URL | exact name); omit to create new
- `--input-mode {auto|tasks|prd|feature}` Artifact hint (default: auto)
- `--estimate-style {tshirt|none}` (default: tshirt) controls size mapping emission
- `--max-size <XS|S|M|L>` Enforced upper bound before forced split (default from config)
- `--config <path>` Override default config resolution
- `--dry-run` Produce PlanPreview only; skip Linear mutations

---

## Usage Examples

Dry run new project from PRD text:

```bash
/plan-linear --input-mode prd --estimate-style tshirt --dry-run
```

Attach to existing project (idempotent re-run skipping existing issues):

```bash
/plan-linear --project "ENG Roadmap 2025" --max-size M
```

---

## Post-Run Guidance

- Adjust thresholds & label rules in config; re-run for deterministic diffs.
- Always resolve audit warnings before expanding scope.
- For iterative expansion, append new features to original artifact; maintain same artifact base to preserve stable hashes.

---
