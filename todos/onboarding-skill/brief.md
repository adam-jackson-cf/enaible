# Engineering Leads AI-SDLC Migration Prompt Brief

## Context

- Objective: Design a new workflow (undecided if prompt `@shared/prompts/AGENTS.md` or skill based `@shared/skills/AGENTS.md`) that guides engineering leads through creating a three-month AI adoption plan, emphasizing gradual rollout, quick wins, offers learning support and clarity on blockers or CF Next support needs.
- Audience: Engineering leads embedded with client teams; they possess full project context, access to codebases, CF Next documentation, SMEs, and AI tooling subscriptions (GitHub Copilot, Gemini, etc.).
- Constraint: Before drafting the workflow/prompt, document all interview findings and further explore engineering-lead requirements.

## Assets & References

- CF Next initiative outputs (playbooks, case studies, tooling experiments across planning, development, testing, design implementation, self-healing tests, etc.).
- Upcoming list of specific CF Next artifacts to be supplied later for direct referencing.

## Detailed Q&A on new workflow

1. **Q:** What is the primary outcome you want engineering leads to achieve after running this new prompt?
   **A:** Produce a phased three-month AI adoption plan with quick wins, clear blockers, and CF Next support needs.
2. **Q:** Who exactly will run the prompt?
   **A:** Engineering leads with support—they hold the relevant project/context knowledge and asset access.
3. **Q:** In what context will they run it?
   **A:** While projects are already in flight, focusing on adapting existing workflows to incorporate AI.
4. **Q:** How much time should they invest in running it vs. executing the plan?
   **A:** About 1–2 hours of interactive prompt work; plan execution spans the three-month window.
5. **Q:** What outputs are expected?
   **A:** A step-by-step plan, capability/agentic readiness assessment, risks, blockers, and support mapping.
6. **Q:** What immediate decisions should the prompt enable?
   **A:** Where to start and which leader/team member should own each plan task.
7. **Q:** What constraints must be respected?
   **A:** Project-specific constraints surfaced via the prompt’s questioning.
8. **Q:** Which stakeholders are impacted beyond the lead?
   **A:** Entire delivery teams, CF Next members, and directors.
9. **Q:** What tech stacks must the prompt handle?
   **A:** Virtually anything—web, mobile, SaaS, cloud across Python, .NET, Kotlin, TypeScript, etc.
10. **Q:** Are there mandated AI practices?
    **A:** Leads have GitHub Copilot and Gemini; experimentation is allowed within budget.
11. **Q:** How should foundational vs. high-impact AI workflows be prioritized?
    **A:** Dynamically, based on team familiarity and technical constraints gathered.
12. **Q:** Desired readiness assessment granularity?
    **A:** Uncertain—prompt should adapt as needed.
13. **Q:** Should KPIs be included?
    **A:** Yes, ideally.
14. **Q:** How will success be evaluated?
    **A:** Adoption coverage, qualitative feedback, and effort reduction due to AI usage.
15. **Q:** Do leads already know client constraints?
    **A:** Yes; prompt must ask targeted questions to capture impact.
16. **Q:** Should it recommend specific CF Next resources?
    **A:** Yes—ideally cite specific case studies (list forthcoming).
17. **Q:** What depth of code analysis is required?
    **A:** In-depth, similar to the analyze-repo-orchestrator approach.
18. **Q:** Compare against best practices or just gather facts?
    **A:** Gather current state, highlight AI friction, and propose changes plus quick wins.
19. **Q:** How much automation is desired?
    **A:** Automate everything possible, reusing existing repo prompts.
20. **Q:** How to handle areas outside the lead’s control?
    **A:** Flag them as blockers/risks in the report.
21. **Q:** What defines quick wins?
    **A:** Focus on high-effort pain points identified per project.
22. **Q:** Should team composition changes be considered?
    **A:** No—stick to processes/tooling.
23. **Q:** How should SME input be incorporated?
    **A:** Produce a report that clearly shows where SMEs can help.
24. **Q:** Any mandatory risk categories?
    **A:** None specific, but note general skepticism and immature verification practices.
25. **Q:** Required inputs?
    **A:** Repo path, available docs, verbal answers for team composition.
26. **Q:** Specific CF Next artifacts to include?
    **A:** Yes (list to be supplied).
27. **Q:** Preferred plan structure?
    **A:** Phased, e.g., month-by-month.
28. **Q:** How should spec-driven development be treated?
    **A:** Encourage trying it for structured conversations while acknowledging overhead.
29. **Q:** Any red-line policies?
    **A:** Follow GDPR/data rules; expect initial parallel human/AI workflows.
30. **Q:** Should observability/telemetry adjustments be suggested?
    **A:** Yes, if useful.
31. **Q:** Balance between CF Next guidance and team context?
    **A:** Heavily favor team-specific context with CF Next as starting points.
32. **Q:** Are secondary deliverables required?
    **A:** No—the main plan suffices.
33. **Q:** Capture governance/approval flows?
    **A:** Yes.
34. **Q:** Should budgeting guidance be included?
    **A:** No.
35. **Q:** How to handle vendor/tooling constraints?
    **A:** Log them as risks/blockers.
36. **Q:** Consider dependencies on non-engineering functions?
    **A:** Yes—map feature stages and contributors.
37. **Q:** Include change-management steps?
    **A:** No.
38. **Q:** Desired tone?
    **A:** Emotionless, factual.
39. **Q:** Reference existing successful migrations?
    **A:** Not yet—this prompt is the starting point (case studies exist separately).
40. **Q:** Additional reporting/compliance needs?
    **A:** None beyond standard expectations.

## Additional Reflections & Needs

- **AI fluency gap**: Many engineering leads may have limited exposure to AI tooling. The prompt should assess confidence levels, propose foundational enablement steps, and sequence recommendations so leads can onboard themselves before steering team adoption.
- **Curated learning resources**: Planning outputs must cite vetted articles, videos, and documentation (AI and traditional engineering) aligned to identified gaps—for example, introducing linting or verification practices with tool comparisons tailored to the team’s stack. References must be drawn from a centralized, CF Next–maintained resource list so every team gets consistent materials.
- **Onboarding mindset**: Treat the three-month plan like a dual onboarding program (lead + team). Highlight where proposed practices benefit both manual and AI-driven workflows, including evidence/rationale to counter skepticism and build trust.
- **Repo history review**: Incorporate git commit/PR analysis to surface collaboration patterns, review throughput, and repeated quality issues. Extend or adapt logic from `shared/skills/codify-pr-reviews` so insights feed into the adoption plan (e.g., automation targets, consistency improvements, repetitive task offloading).
- **Principled personalization**: Anchor the prompt on reusable CF Next principles/practices, then tailor an AI-enabled SDLC plan (up to three months) to each team’s context. Plans must include exercises or learning links, adoption metrics, and phased implementation guidance covering planning through execution. Adoption metrics/KPIs should reuse a centrally managed catalog so measurement stays comparable across teams.
- **Stakeholder transparency**: Ensure outputs summarize context, required support, and blockers (knowledge, cultural, technical, client-driven) so external stakeholders understand how to assist and track progress.

## Reference Design Guidance

- **@systems/codex/prompts/analyze-repo-orchestrator.md** — Demonstrates a tmux-based, parallel analyzer orchestration that produces evidence-backed KPI scoring plus standardized reporting. Useful to mirror for our process so the new prompt can coordinate repo inspections, capture artifacts under timestamped roots, and synthesize readiness scores with explicit checkpoints.
- **@shared/prompts/analyze-architecture.md** — Shows a deterministic architecture review flow that sets up artifact directories, runs Enaible analyzers (patterns, dependency, coupling, scalability), and ties findings back to domain boundaries and risks. Provides a template for structured reconnaissance, analyzer execution, and evidence-cited recommendations we can echo in our readiness assessments.
- **@shared/prompts/analyze-code-quality.md** — Covers deterministic code-quality evaluation using Enaible analyzers (complexity, duplication) plus qualitative gap analysis. Demonstrates how to blend metric tables, hotspot callouts, and prioritized remediation—patterns we can reuse when assessing maturity before AI adoption.
- **@.codex/skills/codify-pr-reviews/SKILL.md** — Documents the workflow for mining GitHub PR review history into actionable rules. Highlights how to fetch, preprocess, and summarize historical review signals, which we can adapt to surface collaboration patterns, repetitive issues, and automation candidates inside the AI-SDLC adoption plan.

## Next Steps

1. Await list of specific CF Next artifacts/case studies to reference.
2. Further explore engineering lead support requirements.
3. Decide what type of workflow is to be created (prompt or skill)
4. Once additional insights/artifacts are logged here, proceed to design.
