# Purpose

Produce a comprehensive UX-focused Product Requirements Document (PRD) that defines personas, scope, screen architecture, flows, and acceptance criteria.

## Variables

- `PRODUCT_BRIEF` ← first positional argument describing the feature or product.
- `QUESTION_RESPONSES` ← structured answers gathered during Phase 1.
- `PRD_OUTPUT` ← final markdown document adhering to the mandated contract.
- `$ARGUMENTS` ← raw argument string.

## Instructions

- Lead with detailed discovery; gather product foundation, user insights, UX requirements, screen architecture, and onboarding details.
- Assign stable IDs (F-001, S-001, FL-001) for features, screens, and flows; reuse consistently across sections.
- Respect STOP confirmations before generating the PRD and before concluding quality validation.
- Ensure MoSCoW scope ties directly to screen architecture and flows.
- Document design principles, accessibility requirements (WCAG), interaction patterns, and content tone explicitly.

## Workflow

1. Information gathering
   - Review provided context and clarify missing areas (product concept, target users, platforms, UX/UI requirements, screens).
   - Conduct targeted question sequence covering:
     - Product foundation
     - User & market
     - UX/UI specifics
     - Screen architecture
     - Design standards
     - Onboarding experience
   - Summarize understanding and confirm key requirements with user.
   - **STOP:** “Ready to generate the PRD? (y/n)”
2. PRD generation
   - Populate the mandated PRD structure in exact order:
     1. Overview
     2. Personas
     3. Scope (MoSCoW with feature IDs)
     4. Screen Architecture (screen IDs)
     5. Key User Flows (flow IDs with trigger, preconditions, steps, alternate paths, postconditions)
     6. UX/UI Requirements (design principles, accessibility, interaction patterns, tone)
     7. Data & Analytics
     8. Non-Functional Requirements
     9. Acceptance Criteria (per feature with Gherkin-style statements)
     10. Risks & Assumptions
     11. Release Plan (milestones + validation)
   - Ensure cross-references (features ↔ screens ↔ flows) are consistent.
3. Quality validation
   - Verify checklist:
     - All MoSCoW features map to screens and flows.
     - Personas include screen usage patterns.
     - Screen architecture reflects user journeys.
     - UX specifications actionable for design.
     - Acceptance criteria cover each feature.
   - **STOP:** “PRD generated with quality validation complete.”

## Output

```md
# RESULT

- Summary: UX PRD generated for "<PRODUCT_BRIEF>".
- Document Length: <word count / sections>
- Personas: <count>
- Features: <count> (Must: <n>, Should: <n>, Could: <n>, Won't: <n>)
- Screens: <count> (Primary <n> / Secondary <n> / Admin <n>)

## DELIVERABLE

- Saved PRD: <path or inline document>
```

## Examples

```bash
# Create PRD for a new onboarding experience
/plan-ux-prd "Team onboarding dashboard"
```
