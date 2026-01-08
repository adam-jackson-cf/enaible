# AI-SDLC Onboarding Skill: Implementation Plan

## Context

Design output templates for a new skill (`shared/skills/onboard-ai-sdlc/`) that guides engineering leads through creating a 3-month AI adoption plan. The skill will produce an assessment report and phased plan with quick wins, blockers, and learning resources.

This plan consolidates analysis of:

- `todos/onboarding-skill/brief.md` - Original requirements
- `shared/prompts/analyze-agentic-readiness.md` - Existing readiness workflow
- `todos/agentic-readiness/rules.md` - 56 assessment rules across 9 categories
- `todos/agentic-readiness/analyse-repo.md` - Repository analysis workflow

---

## Key Inputs (from brief.md)

- **Duration**: 1-2 hours interactive → 3-month execution
- **Audience**: Engineering leads with project context
- **Tech scope**: Any stack (Python, .NET, Kotlin, TypeScript, etc.)
- **Required outputs**: Phased plan, readiness assessment, risks, blockers, support mapping
- **Tone**: Emotionless, factual

---

## Design Decisions (Confirmed)

1. **Integration**: Embedded sub-workflow - the onboarding skill orchestrates `analyze-agentic-readiness` as a sub-step, consuming its artifacts directly.

2. **Rules model**: Hybrid approach - split 56 rules into:
   - **14 INTERVIEW questions** (posed to technical lead, retained in assessment)
   - **26 AUTOMATED checks** (codebase analysis via enhanced analyze-agentic-readiness)
   - **16 HYBRID** (automated signal + human confirmation)

3. **Output format**: Master report + linked artifacts - single `index.md` as entry point.

4. **PR analysis**: Mandatory step - workflow requires GitHub access for PR history analysis. Block with clear error if unavailable.

5. **Quick wins**: Signal-driven generation - quick wins are programmatically generated from assessment gap signals (e.g., "lint not enforced" → "Add pre-commit hooks with husky").

---

## Rules Categorization Analysis

### Summary: Input Type Distribution

| Category                        | INTERVIEW | AUTOMATED | HYBRID | Total  |
| ------------------------------- | --------- | --------- | ------ | ------ |
| Verified Starting Base          | 0         | 5         | 0      | 5      |
| Implementation as Documentation | 0         | 2         | 3      | 5      |
| Coding Guidance via System Docs | 0         | 4         | 2      | 6      |
| Planning is Fundamental         | 4         | 0         | 2      | 6      |
| Context Efficiency              | 4         | 3         | 1      | 8      |
| Verification as First Class     | 1         | 4         | 2      | 7      |
| Agentic Harnesses               | 2         | 2         | 2      | 6      |
| Complement LLM with Code        | 1         | 3         | 2      | 6      |
| Observability                   | 2         | 3         | 2      | 7      |
| **TOTALS**                      | **14**    | **26**    | **16** | **56** |

### Category 1: Verified Starting Base (VSB) - 5 Rules

| ID    | Rule                                         | Category      | Rationale                                                                                   |
| ----- | -------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------- |
| VSB-1 | Project uses maintained templates/generators | **AUTOMATED** | Detectable via file inspection (package.json CLI markers, .yo-rc.json, standard structures) |
| VSB-2 | Baseline builds pass                         | **AUTOMATED** | Run build command and verify exit code 0                                                    |
| VSB-3 | Baseline tests pass                          | **AUTOMATED** | Run test command and verify exit code 0, test count > 0                                     |
| VSB-4 | Dependencies version-pinned                  | **AUTOMATED** | Check for lock files (package-lock.json, poetry.lock, go.sum, etc.)                         |
| VSB-5 | Toolchain versions pinned                    | **AUTOMATED** | Check for .nvmrc, .python-version, .tool-versions, rust-toolchain.toml                      |

### Category 2: Implementation as First Class Documentation (IFCD) - 5 Rules

| ID     | Rule                                        | Category      | Rationale                                                          |
| ------ | ------------------------------------------- | ------------- | ------------------------------------------------------------------ |
| IFCD-1 | Shared prompts exist for onboarding         | **HYBRID**    | Files detectable but quality/coverage requires human judgment      |
| IFCD-2 | No redundant documentation duplicating code | **HYBRID**    | Can detect doc presence but semantic overlap requires human review |
| IFCD-3 | AGENTS.md contains high-level repo map only | **AUTOMATED** | Line count < 200, detect verbose patterns                          |
| IFCD-4 | AGENTS.md contains non-standard workflows   | **HYBRID**    | Can detect content but relevance requires human context            |
| IFCD-5 | System docs complement automated processes  | **AUTOMATED** | Compare rules in docs against linting config rules                 |

### Category 3: Coding Guidance via System Docs (CGSD) - 6 Rules

| ID     | Rule                                      | Category      | Rationale                                                   |
| ------ | ----------------------------------------- | ------------- | ----------------------------------------------------------- |
| CGSD-1 | Rules are binary (true/false)             | **HYBRID**    | Can flag exception keywords but judgment needed             |
| CGSD-2 | Rules are minimal, progressive disclosure | **HYBRID**    | Line count detectable but organization quality needs review |
| CGSD-3 | Deterministic tools preferred over rules  | **AUTOMATED** | Check linter/formatter configs present                      |
| CGSD-4 | Conceptual rules include examples         | **HYBRID**    | Can detect example blocks but quality requires judgment     |
| CGSD-5 | Rules favor verifiable metrics            | **AUTOMATED** | Search for numeric thresholds vs subjective terms           |
| CGSD-6 | No redundant pattern/framework rules      | **AUTOMATED** | Search for SOLID, DRY, KISS mentions in docs                |

### Category 4: Planning is Fundamental (PIF) - 6 Rules

| ID    | Rule                                 | Category      | Rationale                                                                    |
| ----- | ------------------------------------ | ------------- | ---------------------------------------------------------------------------- |
| PIF-1 | Tasks have clear goals and non-goals | **INTERVIEW** | Team practices, not codebase artifacts                                       |
| PIF-2 | Constraints are explicit             | **INTERVIEW** | Team practices around task definition                                        |
| PIF-3 | Acceptance criteria defined          | **INTERVIEW** | Team practices around definition of done                                     |
| PIF-4 | Verification plan exists             | **HYBRID**    | Can detect test plans but workflow adherence needs interview                 |
| PIF-5 | Planning separated from execution    | **INTERVIEW** | Context management practices                                                 |
| PIF-6 | Plans reviewed before execution      | **HYBRID**    | Can detect PR review requirements in CODEOWNERS but practices need interview |

### Category 5: Context Efficiency (CE) - 8 Rules

| ID   | Rule                                   | Category      | Rationale                                                    |
| ---- | -------------------------------------- | ------------- | ------------------------------------------------------------ |
| CE-1 | Tools provide context transparency     | **HYBRID**    | Tool choice detectable but usage patterns need interview     |
| CE-2 | MCP avoided for permanent workflows    | **AUTOMATED** | Scan for MCP config files                                    |
| CE-3 | Context sessions kept lean             | **INTERVIEW** | Session management is operational practice                   |
| CE-4 | Planning and build execution separated | **INTERVIEW** | Session hygiene is operational practice                      |
| CE-5 | Planning artifacts stored externally   | **HYBRID**    | Can detect todos/plans directories but usage needs interview |
| CE-6 | System files not overly polluted       | **AUTOMATED** | Measure AGENTS.md line count                                 |
| CE-7 | Rules automated where possible         | **AUTOMATED** | Check linting coverage vs doc rules                          |
| CE-8 | Tasks encapsulated                     | **INTERVIEW** | Session hygiene practices                                    |

### Category 6: Verification as First Class Requirement (VFCR) - 7 Rules

| ID     | Rule                                     | Category      | Rationale                                                                |
| ------ | ---------------------------------------- | ------------- | ------------------------------------------------------------------------ |
| VFCR-1 | Local verification mirrors CI            | **AUTOMATED** | Compare CI commands vs local scripts/Makefile                            |
| VFCR-2 | Integration/smoke tests included         | **AUTOMATED** | Search for e2e/, integration/, playwright/, cypress/                     |
| VFCR-3 | Automated code reviews configured        | **HYBRID**    | Can detect CODEOWNERS, reviewers but LLM review standards need interview |
| VFCR-4 | Verification proportional to risk        | **INTERVIEW** | Risk assessment strategy is human judgment                               |
| VFCR-5 | Early regression detection (pre-commit)  | **AUTOMATED** | Detect .husky/, .pre-commit-config.yaml, lefthook.yml                    |
| VFCR-6 | Quality exceptions reviewed and codified | **INTERVIEW** | Exception tracking practices                                             |
| VFCR-7 | Verification cannot be bypassed          | **AUTOMATED** | Search for --no-verify, continue-on-error patterns                       |

### Category 7: Agentic Harnesses (AH) - 6 Rules

| ID   | Rule                                 | Category      | Rationale                                                   |
| ---- | ------------------------------------ | ------------- | ----------------------------------------------------------- |
| AH-1 | System prompts visible and versioned | **AUTOMATED** | Check AGENTS.md, CLAUDE.md in git                           |
| AH-2 | Tool configuration versioned         | **AUTOMATED** | Check .cursor/, .continue/, .aider\* tracked in git         |
| AH-3 | Workflows reproducible               | **HYBRID**    | Can detect config but reproducibility needs testing         |
| AH-4 | Open-source harnesses preferred      | **INTERVIEW** | Tooling choices and constraints                             |
| AH-5 | LLM actions have visibility          | **INTERVIEW** | Logging practices for AI actions                            |
| AH-6 | Vendor lock-in avoided               | **HYBRID**    | Can detect proprietary configs but strategy needs interview |

### Category 8: Complement LLM with Deterministic Code (CLDC) - 6 Rules

| ID     | Rule                                | Category      | Rationale                                                   |
| ------ | ----------------------------------- | ------------- | ----------------------------------------------------------- |
| CLDC-1 | Permanent workflows are scripts     | **AUTOMATED** | Detect Makefile, package.json scripts, scripts/ directory   |
| CLDC-2 | Scripts have clear inputs/outputs   | **HYBRID**    | Can detect --help support but quality needs review          |
| CLDC-3 | Tooling mitigates LLM weaknesses    | **HYBRID**    | Deduplication tools detectable but strategy needs interview |
| CLDC-4 | Token costs actively reduced        | **INTERVIEW** | Operational practice                                        |
| CLDC-5 | Code duplication detection in place | **AUTOMATED** | Check for jscpd, sonar configs                              |
| CLDC-6 | God class prevention measures       | **AUTOMATED** | Check complexity thresholds in linting                      |

### Category 9: Observability (OBS) - 7 Rules

| ID    | Rule                                     | Category      | Rationale                                                     |
| ----- | ---------------------------------------- | ------------- | ------------------------------------------------------------- |
| OBS-1 | Dev logs accessible to agents            | **HYBRID**    | Can detect make targets but documented locations need review  |
| OBS-2 | Quality gates provide automated feedback | **AUTOMATED** | Run linter and verify output includes file paths/line numbers |
| OBS-3 | Pre-commit hooks configured              | **AUTOMATED** | Detect husky, pre-commit, lefthook                            |
| OBS-4 | LSP feedback explored                    | **INTERVIEW** | Tooling configuration practices                               |
| OBS-5 | Stop hooks for JIT quality checks        | **INTERVIEW** | Agent configuration practices                                 |
| OBS-6 | UI testing with screenshot capture       | **AUTOMATED** | Detect playwright.config.ts, screenshot libs                  |
| OBS-7 | Native libraries over MCP for testing    | **HYBRID**    | Can detect libs but usage patterns need interview             |

---

## analyze-agentic-readiness Coverage Gap Analysis

### Currently Covered by Existing Workflow

| Rule ID | Description                         | Covering Artifact/Script                      |
| ------- | ----------------------------------- | --------------------------------------------- |
| IFCD-5  | Docs complement automation          | `docs_risk.py`                                |
| CGSD-3  | Deterministic tools preferred       | `inventory_tests_gates.py`                    |
| CE-2    | MCP avoided for permanent workflows | `mcp_scan.py`                                 |
| CE-7    | Rules automated where possible      | `docs_risk.py`                                |
| VFCR-1  | Local verification mirrors CI       | `inventory_tests_gates.py` parity_gaps        |
| VFCR-2  | Integration tests present           | `inventory_tests_gates.py` hard_tests_present |
| VFCR-5  | Pre-commit hooks configured         | `inventory_tests_gates.py`                    |
| CLDC-1  | Permanent workflows as scripts      | `inventory_tests_gates.py`                    |
| CLDC-5  | Code duplication detection          | `quality-jscpd.json` via Enaible analyzer     |
| CLDC-6  | God class prevention                | `quality-lizard.json` via Enaible analyzer    |
| OBS-3   | Pre-commit hooks configured         | `inventory_tests_gates.py`                    |

### Partially Covered (Need Enhancement)

| Rule        | Current State            | Enhancement Needed                         |
| ----------- | ------------------------ | ------------------------------------------ |
| VSB-4       | Language detection only  | Add lock file presence check               |
| IFCD-3/CE-6 | Doc existence            | Add AGENTS.md line count threshold (< 200) |
| AH-1        | File detection           | Add git tracking verification              |
| OBS-6       | Test framework detection | Add screenshot capability detection        |

### Not Covered (New Steps Needed)

| Rule   | Description                | Proposed Implementation                           |
| ------ | -------------------------- | ------------------------------------------------- |
| VSB-1  | Generator/template markers | Detect .yo-rc.json, CLI markers in package.json   |
| VSB-5  | Toolchain version files    | Check .nvmrc, .python-version, .tool-versions     |
| CGSD-5 | Verifiable metrics in docs | Search for numeric thresholds vs subjective terms |
| CGSD-6 | Redundant pattern rules    | Search for SOLID, DRY, KISS mentions              |
| VFCR-7 | Bypass patterns            | Search --no-verify, continue-on-error patterns    |
| AH-2   | Tool config tracking       | Verify .cursor/, .continue/, .aider\* git status  |
| CLDC-2 | Script documentation       | Detect --help support in custom scripts           |
| OBS-1  | Dev log access             | Detect make/npm targets for log retrieval         |
| OBS-2  | Linter output quality      | Verify linter produces file paths + line numbers  |

---

## Proposed Skill Structure

```
shared/skills/onboard-ai-sdlc/
├── SKILL.md                    # Main workflow (5-7 steps)
├── config/
│   └── defaults.json           # Thresholds, learning catalog, CF Next refs
├── references/
│   ├── requirement-gathering.md      # Intake variables & clarification
│   ├── assessment-workflow.md        # Analysis execution (calls agentic-readiness)
│   ├── plan-generation-workflow.md   # 3-month plan synthesis
│   ├── learning-resources.md         # Curated resource catalog
│   └── templates/
│       ├── assessment-report.md      # Template for assessment output
│       ├── adoption-plan.md          # Template for 3-month plan
│       ├── blockers-matrix.md        # Template for blockers/support
│       └── stakeholder-summary.md    # Template for external visibility
└── scripts/
    └── (TBD based on automation needs)
```

---

## Artifact Architecture (Finalized)

### Output Directory Structure

```
.enaible/artifacts/onboard-ai-sdlc/<TIMESTAMP>/
├── index.md                         # Master report (entry point)
├── inputs/
│   └── intake-responses.json        # Captured interview answers
├── assessment/
│   ├── assessment-report.md         # Detailed readiness assessment
│   ├── rules-assessment.json        # 56-rule evaluation results
│   ├── pr-patterns.json             # PR history analysis (MANDATORY)
│   ├── pr-patterns-summary.md       # Human-readable PR insights
│   └── [inherited from agentic-readiness]/
│       ├── agentic-readiness.json
│       ├── maintenance-score.json
│       ├── quality-gates.json
│       ├── docs-risk.json
│       ├── mcp-scan.json
│       └── ... (all analyzer outputs)
├── plan/
│   ├── adoption-plan.md             # 3-month phased plan
│   ├── quick-wins.md                # Week 1-2 immediate actions
│   └── milestones.json              # Checkpoint criteria (machine-readable)
├── blockers/
│   ├── blockers-matrix.md           # Full blocker analysis
│   └── support-requests.json        # CF Next support mapping
└── stakeholder/
    └── stakeholder-summary.md       # Executive-friendly summary
```

---

## Output Templates

### Master Index Template (`index.md`)

```markdown
# AI-SDLC Onboarding Report: {{PROJECT_NAME}}

**Generated:** {{DATE}}
**Lead:** {{LEAD_NAME}}
**Artifacts:** `.enaible/artifacts/onboard-ai-sdlc/{{TIMESTAMP}}/`

## Status Summary

| Dimension         | Score     | Status          |
| ----------------- | --------- | --------------- |
| Agentic Readiness | {{X}}/10  | {{🟢🟠🔴}}      |
| Maintenance Score | {{X}}/10  | {{🟢🟠🔴}}      |
| Team AI Fluency   | {{level}} | {{gap summary}} |
| Critical Blockers | {{count}} | {{top blocker}} |

## Quick Navigation

| Artifact                                                  | Purpose                                              |
| --------------------------------------------------------- | ---------------------------------------------------- |
| [Assessment Report](assessment/assessment-report.md)      | Detailed readiness evaluation with 56-rule breakdown |
| [Adoption Plan](plan/adoption-plan.md)                    | 3-month phased implementation roadmap                |
| [Quick Wins](plan/quick-wins.md)                          | Immediate actions for Week 1-2                       |
| [Blockers Matrix](blockers/blockers-matrix.md)            | Categorized blockers with resolution paths           |
| [Stakeholder Summary](stakeholder/stakeholder-summary.md) | Executive progress report template                   |

## Key Findings

### Ready for Agentic Work

- {{strength 1}}
- {{strength 2}}

### Critical Gaps (Must Address)

1. {{gap with blocker ID reference}}
2. {{gap}}

### Recommended Starting Point

{{Phase 1 quick win recommendation with owner suggestion}}

## Next Steps

1. Review [Quick Wins](plan/quick-wins.md) and assign owners
2. Address critical blockers in [Blockers Matrix](blockers/blockers-matrix.md)
3. Schedule bi-weekly review using [Stakeholder Summary](stakeholder/stakeholder-summary.md)
```

### 1. Assessment Report Template (`assessment-report.md`)

Purpose: Baseline agentic readiness state before planning.

```markdown
# AI-SDLC Readiness Assessment: {{PROJECT_NAME}}

**Assessment Date:** {{DATE}}
**Assessed By:** {{LEAD_NAME}}
**Artifact Root:** `.enaible/artifacts/onboard-ai-sdlc/{{TIMESTAMP}}/`

## Executive Summary

{{2-3 sentence readiness state summary}}

## Readiness Scores

| KPI               | Score    | Status     | Evidence               |
| ----------------- | -------- | ---------- | ---------------------- |
| Agentic Readiness | {{0-10}} | {{🟢🟠🔴}} | agentic-readiness.json |
| Maintenance Score | {{0-10}} | {{🟢🟠🔴}} | maintenance-score.json |

Legend: 🟢 7–10 Ready | 🟠 4–6 Gaps | 🔴 0–3 Blockers

## Category Breakdown

| Category                    | Score    | Key Gaps |
| --------------------------- | -------- | -------- |
| Verified Starting Base      | {{X/10}} | {{gaps}} |
| System Documentation        | {{X/8}}  | {{gaps}} |
| Verification Infrastructure | {{X/8}}  | {{gaps}} |
| Tooling Transparency        | {{X/4}}  | {{gaps}} |
| Workflow Automation         | {{X/4}}  | {{gaps}} |
| Observability               | {{X/6}}  | {{gaps}} |

## Enforcement Status

| Gate              | Local   | CI      | Pre-commit | Parity  |
| ----------------- | ------- | ------- | ---------- | ------- |
| Lint              | {{✓/✗}} | {{✓/✗}} | {{✓/✗}}    | {{✓/✗}} |
| Unit Tests        | {{✓/✗}} | {{✓/✗}} | {{✓/✗}}    | {{✓/✗}} |
| Integration Tests | {{✓/✗}} | {{✓/✗}} | {{✓/✗}}    | {{✓/✗}} |
| Type Checking     | {{✓/✗}} | {{✓/✗}} | {{✓/✗}}    | {{✓/✗}} |

## Team AI Fluency

| Role     | Current Level                        | Target (3mo) | Gap                 |
| -------- | ------------------------------------ | ------------ | ------------------- |
| {{role}} | {{None/Basic/Intermediate/Advanced}} | {{target}}   | {{gap description}} |

## Collaboration Patterns (from PR History)

- **Review throughput**: {{X PRs/week avg}}
- **Common review themes**: {{top 3 patterns}}
- **Automation candidates**: {{repetitive issues}}

## Critical Blockers

1. {{blocker with category: technical/knowledge/cultural/client}}
2. {{blocker}}

## Artifacts

- Assessment inputs → `.enaible/artifacts/onboard-ai-sdlc/{{TIMESTAMP}}/inputs/`
- Agentic readiness → `.enaible/artifacts/onboard-ai-sdlc/{{TIMESTAMP}}/agentic-readiness.json`
- PR analysis → `.enaible/artifacts/onboard-ai-sdlc/{{TIMESTAMP}}/pr-patterns.json`
```

### 2. Three-Month Adoption Plan Template (`adoption-plan.md`)

Purpose: Phased implementation with quick wins and milestones.

```markdown
# AI-SDLC Adoption Plan: {{PROJECT_NAME}}

**Plan Generated:** {{DATE}}
**Plan Owner:** {{LEAD_NAME}}
**Review Cycle:** Bi-weekly

## Plan Summary

| Phase        | Duration   | Focus     | Success Metric |
| ------------ | ---------- | --------- | -------------- |
| Foundation   | Weeks 1-4  | {{focus}} | {{metric}}     |
| Expansion    | Weeks 5-8  | {{focus}} | {{metric}}     |
| Optimization | Weeks 9-12 | {{focus}} | {{metric}}     |

## Quick Wins (Week 1-2)

| #   | Action     | Owner     | Effort           | Impact          |
| --- | ---------- | --------- | ---------------- | --------------- |
| 1   | {{action}} | {{owner}} | {{Low/Med/High}} | {{description}} |
| 2   | {{action}} | {{owner}} | {{Low/Med/High}} | {{description}} |
| 3   | {{action}} | {{owner}} | {{Low/Med/High}} | {{description}} |

---

## Phase 1: Foundation (Weeks 1-4)

### Objectives

- {{objective}}

### Week 1-2: {{Theme}}

| Task     | Owner     | Dependencies | Resources                |
| -------- | --------- | ------------ | ------------------------ |
| {{task}} | {{owner}} | {{deps}}     | [{{resource}}]({{link}}) |

**Checkpoint**: {{acceptance criteria}}

### Week 3-4: {{Theme}}

| Task     | Owner     | Dependencies | Resources                |
| -------- | --------- | ------------ | ------------------------ |
| {{task}} | {{owner}} | {{deps}}     | [{{resource}}]({{link}}) |

**Checkpoint**: {{acceptance criteria}}

**Phase 1 Success Criteria:**

- [ ] {{criterion}}
- [ ] {{criterion}}

---

## Phase 2: Expansion (Weeks 5-8)

### Objectives

- {{objective}}

### Week 5-6: {{Theme}}

| Task     | Owner     | Dependencies | Resources                |
| -------- | --------- | ------------ | ------------------------ |
| {{task}} | {{owner}} | {{deps}}     | [{{resource}}]({{link}}) |

**Checkpoint**: {{acceptance criteria}}

### Week 7-8: {{Theme}}

| Task     | Owner     | Dependencies | Resources                |
| -------- | --------- | ------------ | ------------------------ |
| {{task}} | {{owner}} | {{deps}}     | [{{resource}}]({{link}}) |

**Checkpoint**: {{acceptance criteria}}

**Phase 2 Success Criteria:**

- [ ] {{criterion}}
- [ ] {{criterion}}

---

## Phase 3: Optimization (Weeks 9-12)

### Objectives

- {{objective}}

### Week 9-10: {{Theme}}

| Task     | Owner     | Dependencies | Resources                |
| -------- | --------- | ------------ | ------------------------ |
| {{task}} | {{owner}} | {{deps}}     | [{{resource}}]({{link}}) |

**Checkpoint**: {{acceptance criteria}}

### Week 11-12: {{Theme}}

| Task     | Owner     | Dependencies | Resources                |
| -------- | --------- | ------------ | ------------------------ |
| {{task}} | {{owner}} | {{deps}}     | [{{resource}}]({{link}}) |

**Checkpoint**: {{acceptance criteria}}

**Phase 3 Success Criteria:**

- [ ] {{criterion}}
- [ ] {{criterion}}

---

## Adoption Metrics

| Metric                  | Baseline     | Target (3mo) | Measurement       |
| ----------------------- | ------------ | ------------ | ----------------- |
| AI tool usage (team %)  | {{X%}}       | {{Y%}}       | Survey/telemetry  |
| Agentic readiness score | {{X}}        | {{Y}}        | Re-run assessment |
| Code review turnaround  | {{X hrs}}    | {{Y hrs}}    | GitHub metrics    |
| {{custom metric}}       | {{baseline}} | {{target}}   | {{method}}        |

## Governance

- **Plan Review**: Bi-weekly with {{stakeholder}}
- **Blocker Escalation**: {{escalation path}}
- **Metric Reporting**: Monthly to {{audience}}
```

### 3. Blockers & Support Matrix Template (`blockers-matrix.md`)

Purpose: Clear visibility for stakeholders on what needs resolution.

```markdown
# Blockers & Support Requirements: {{PROJECT_NAME}}

**Generated:** {{DATE}}
**Status Review Frequency:** Weekly

## Blocker Summary

| Category        | Count | Critical | Requires External |
| --------------- | ----- | -------- | ----------------- |
| Technical       | {{n}} | {{n}}    | {{n}}             |
| Knowledge       | {{n}} | {{n}}    | {{n}}             |
| Cultural        | {{n}} | {{n}}    | {{n}}             |
| Client/External | {{n}} | {{n}}    | {{n}}             |

---

## Technical Blockers

| ID  | Blocker     | Impact           | Resolution | Owner     | CF Next Support    |
| --- | ----------- | ---------------- | ---------- | --------- | ------------------ |
| T-1 | {{blocker}} | {{High/Med/Low}} | {{action}} | {{owner}} | {{support needed}} |

## Knowledge Blockers

| ID  | Blocker     | Affected Roles | Resolution        | Resources                |
| --- | ----------- | -------------- | ----------------- | ------------------------ |
| K-1 | {{blocker}} | {{roles}}      | {{learning path}} | [{{resource}}]({{link}}) |

## Cultural Blockers

| ID  | Blocker     | Symptom                 | Resolution   | Champion            |
| --- | ----------- | ----------------------- | ------------ | ------------------- |
| C-1 | {{blocker}} | {{observable behavior}} | {{approach}} | {{change champion}} |

## Client/External Blockers

| ID  | Blocker     | Constraint            | Escalation Path | Status                        |
| --- | ----------- | --------------------- | --------------- | ----------------------------- |
| E-1 | {{blocker}} | {{constraint detail}} | {{path}}        | {{Open/In Progress/Resolved}} |

---

## CF Next Support Requests

| Request     | Priority     | Skill/Artifact Needed | Contact             |
| ----------- | ------------ | --------------------- | ------------------- |
| {{request}} | {{P1/P2/P3}} | {{artifact or SME}}   | {{cf next contact}} |

## SME Consultation Needs

| Domain     | Question/Need | Preferred SME     | Status                         |
| ---------- | ------------- | ----------------- | ------------------------------ |
| {{domain}} | {{question}}  | {{sme name/role}} | {{Pending/Scheduled/Complete}} |
```

### 4. Stakeholder Summary Template (`stakeholder-summary.md`)

Purpose: Executive-friendly progress report for directors/CF Next.

```markdown
# AI-SDLC Adoption: {{PROJECT_NAME}} Status

**Report Date:** {{DATE}}
**Period:** {{start}} – {{end}}
**Lead:** {{LEAD_NAME}}

## Status: {{🟢 On Track | 🟠 At Risk | 🔴 Blocked}}

### Progress Summary

| Phase        | Status     | Progress      | Notes     |
| ------------ | ---------- | ------------- | --------- |
| Foundation   | {{status}} | {{X/Y tasks}} | {{notes}} |
| Expansion    | {{status}} | {{X/Y tasks}} | {{notes}} |
| Optimization | {{status}} | {{X/Y tasks}} | {{notes}} |

### Key Metrics

| Metric          | Baseline | Current | Target | Trend   |
| --------------- | -------- | ------- | ------ | ------- |
| Readiness Score | {{X}}    | {{Y}}   | {{Z}}  | {{↑↓→}} |
| Team AI Usage   | {{X%}}   | {{Y%}}  | {{Z%}} | {{↑↓→}} |

### Highlights

- {{accomplishment}}
- {{accomplishment}}

### Blockers Requiring Attention

- {{blocker with owner and ask}}

### Support Received from CF Next

- {{support and outcome}}

### Next Period Focus

- {{focus area}}
- {{focus area}}
```

---

## Interview Questions (Intake Phase)

The following 11 question areas collect human context that cannot be automated:

### Planning & Task Management (PIF-1 to PIF-6)

1. **Task Definition Process**
   - Q: "How are tasks defined before starting agentic work? Do you use templates with explicit goals, non-goals, and acceptance criteria?"
   - Maps to: PIF-1, PIF-2, PIF-3

2. **Planning vs Execution Separation**
   - Q: "Do you separate planning sessions from build execution, or work in long combined sessions? Where are planning artifacts stored?"
   - Maps to: PIF-5, CE-4, CE-5

3. **Review Workflow**
   - Q: "Are plans reviewed before execution? Is there a PR review or approval workflow for agentic task plans?"
   - Maps to: PIF-6, VFCR-3

### Context Management (CE-1 to CE-8)

4. **Session Hygiene**
   - Q: "What is your typical session length? Do you actively manage context window usage?"
   - Maps to: CE-3, CE-8

5. **Tool Transparency**
   - Q: "Which agentic tools are you using? Do they provide visibility into context usage and action history?"
   - Maps to: CE-1, AH-5

### Verification & Quality (VFCR-4, VFCR-6)

6. **Risk-Based Testing**
   - Q: "How do you determine test coverage needs? Is verification proportional to feature risk?"
   - Maps to: VFCR-4

7. **Exception Handling**
   - Q: "How are quality gate exceptions handled - tracked and codified, or ad-hoc?"
   - Maps to: VFCR-6

### Tooling Choices (AH-4, AH-5, AH-6)

8. **Harness Selection**
   - Q: "What agentic harnesses/tools does the team use? Are there proprietary lock-in concerns? Do you have logging/audit trails for LLM actions?"
   - Maps to: AH-4, AH-5, AH-6

### Operational Practices (CLDC-4, OBS-4, OBS-5)

9. **Token Efficiency**
   - Q: "Is token cost a consideration? Do you use caching or context optimization techniques?"
   - Maps to: CLDC-4

10. **LLM Feedback Mechanisms**
    - Q: "What feedback mechanisms are configured for agent self-correction? LSP integration? Stop hooks?"
    - Maps to: OBS-4, OBS-5

### Team Context

11. **Agentic Experience & Constraints**
    - Q: "What is the team's experience level with agentic workflows? (New / Experimenting / Established)"
    - Q: "Are there specific constraints on tools or approaches (security policies, approved vendor lists)?"
    - Q: "Does the team favor minimal documentation (implementation as docs) or comprehensive documentation?"
    - Maps to: Team AI Fluency assessment

---

## Quick Wins Template (Signal-Driven)

```markdown
# Quick Wins: {{PROJECT_NAME}}

**Generated:** {{DATE}}
**Time to Value:** Week 1-2

## Priority Actions

| #   | Signal Gap | Quick Win | Effort | Impact | Owner |
| --- | ---------- | --------- | ------ | ------ | ----- |

{{FOR EACH GAP in assessment-gaps WHERE effort=low}}
| {{n}} | {{gap.rule_id}}: {{gap.description}} | {{gap.quick_win}} | Low | {{gap.impact}} | TBD |
{{END FOR}}

## Signal-to-Action Mapping

| Assessment Signal               | Quick Win Action                   | Resources                |
| ------------------------------- | ---------------------------------- | ------------------------ |
| Lint not enforced in pre-commit | Add husky + lint-staged            | [Pre-commit Setup Guide] |
| No lock files present           | Generate and commit lock files     | Stack-specific docs      |
| AGENTS.md > 200 lines           | Refactor to progressive disclosure | [System Doc Guidelines]  |
| No integration tests            | Add smoke test for critical path   | [Testing Patterns]       |
| MCP config present              | Migrate to bash scripts            | [MCP Migration Guide]    |
| No toolchain version pinning    | Add .nvmrc/.python-version         | Stack-specific docs      |
| CI/local parity gaps            | Align local scripts with CI        | [Parity Checklist]       |

## Implementation Notes

- Each quick win is derived from assessment signals in `rules-assessment.json`
- Effort estimated from typical implementation complexity
- Impact based on readiness score contribution weight
```

---

## PR Analysis Artifact Templates

### pr-patterns.json (Machine-Readable)

```json
{
  "analysis_period": "{{start_date}} - {{end_date}}",
  "total_prs_analyzed": "{{count}}",
  "metrics": {
    "avg_review_turnaround_hours": "{{n}}",
    "avg_comments_per_pr": "{{n}}",
    "self_merge_percentage": "{{n}}"
  },
  "review_patterns": [
    {
      "pattern": "{{pattern_name}}",
      "frequency": "{{count}}",
      "examples": ["PR#123: {{example}}"]
    }
  ],
  "automation_candidates": [
    {
      "issue": "{{repeated issue}}",
      "frequency": "{{count}}",
      "recommendation": "{{automation suggestion}}"
    }
  ]
}
```

### pr-patterns-summary.md (Human-Readable)

```markdown
# PR History Analysis: {{PROJECT_NAME}}

**Period:** {{start_date}} - {{end_date}}
**PRs Analyzed:** {{count}}

## Review Throughput

| Metric                | Value     | Benchmark |
| --------------------- | --------- | --------- |
| Avg review turnaround | {{X}} hrs | < 24 hrs  |
| Avg comments per PR   | {{X}}     | 2-5       |
| Self-merge rate       | {{X}}%    | < 10%     |

## Common Review Themes

1. **{{theme}}** ({{frequency}} occurrences)
   - Example: PR#123 - "{{comment excerpt}}"
   - Recommendation: {{action}}

## Automation Candidates

Issues that appear repeatedly and could be automated:

| Issue     | Frequency     | Suggested Automation                         |
| --------- | ------------- | -------------------------------------------- |
| {{issue}} | {{count}} PRs | {{linter rule / pre-commit hook / CI check}} |

## Insights for Adoption Plan

- {{insight relevant to agentic workflow adoption}}
```

---

## Implementation Roadmap

### Phase 1: Define Skill Structure

- Create `shared/skills/onboard-ai-sdlc/SKILL.md` with workflow phases
- Create `config/intake-questions.json` with structured interview format
- Create output templates in `references/templates/`

### Phase 2: Add PR Analysis Step

- Integrate `codify-pr-reviews` pattern into workflow
- Create `pr_analysis.py` helper script
- Add GitHub access validation (fail fast if unavailable)

### Phase 3: Enhance analyze-agentic-readiness

- Add 9 new detection capabilities to existing helper scripts
- Update `readiness_score.py` to incorporate new signals
- Add 56-rule assessment output artifact (`rules-assessment.json`)

### Phase 4: Implement Signal-Driven Quick Wins

- Create gap-to-action mapping configuration
- Generate quick-wins.md from assessment signals
- Include resource links from CF Next catalog

### Phase 5: Implement Workflow Orchestration

- Intake phase: Collect interview responses → `intake-responses.json`
- Analysis phase: Run enhanced agentic-readiness + PR analysis → assessment artifacts
- Synthesis phase: Generate plan from assessment + intake context
- Output phase: Produce master index + linked artifacts

### Verification

- Run full workflow against a test repository
- Verify all 56 rules are assessed (automated + interview combined)
- Validate artifact links resolve correctly
- Test stakeholder summary generation
- Verify PR analysis blocks appropriately when GitHub unavailable
