# Purpose

Standardize the intake process to ensure complete research briefs before investigation begins.

## Variables

### Required

- @RESEARCH_OBJECTIVE — Clear description of what the research should accomplish
- @SCOPE — What to include/exclude in the investigation
- @OUTPUT_FORMAT — Depth of analysis and presentation needs
- @DECISION_CONTEXT — How the research findings will be used
- @ONLINE_RESEARCH — `allowed` or `disallowed`
- @QUESTIONS — list of concrete research questions

### Optional

- @TIME_CONSTRAINTS — Deadline requirements and urgency level
- @TARGET_AUDIENCE — Who will consume the research
- @DOMAIN_FOCUS — Specific industry or domain emphasis
- @EXISTING_KNOWLEDGE — Assumptions to validate or build upon
- @ALLOWED_SOURCES — Approved sources or domains
- @BLOCKED_SOURCES — Sources or domains to avoid

## Instructions

- Verify ALL minimum requirements are provided before proceeding
- Confirm online research expectations: allowed domains/APIs, required search engines, and any restrictions on external data collection
- If requirements are missing, request clarification using the template below
- Establish artifact directory for all research outputs and note approved web-research channels
- Run the requirements initializer to persist inputs in `requirements.json`

## Minimum Information Checklist

**MUST HAVE - Request clarification if missing:**

1. **Research Objective**: What specific questions should the research answer?
2. **Scope and Boundaries**: Geographic, temporal, or domain-specific limits?
3. **Output Format**: Executive brief, detailed report, competitive matrix, or other?
4. **Decision Context**: What decisions will be informed by this research?
5. **Online Research Permissions**: Approved domains/search engines, compliance guardrails, and freshness expectations

**HELPFUL CONTEXT (not blocking):**

- Target audience for the research
- Preferred source types (academic, industry, user-generated)
- Budget or time constraints
- Existing knowledge or hypotheses to validate
- Known embargoed domains or data sources to avoid

## Clarification Request Template

If minimum requirements are missing:

```markdown
I need additional information to conduct effective research. Please provide:

**Missing Critical Information:**

- [List specific missing requirements]

**Additional Context (Optional but Helpful):**

- [List helpful context that would improve the research]

Once I have this information, I'll proceed with the appropriate research methodology.
```

## Initialize the research run

```bash
"$PYTHON_CMD" scripts/research_init.py \
  --objective "@RESEARCH_OBJECTIVE" \
  --scope "@SCOPE" \
  --output-format "@OUTPUT_FORMAT" \
  --decision-context "@DECISION_CONTEXT" \
  --online-research "@ONLINE_RESEARCH" \
  --question "<question 1>" \
  --question "<question 2>"
```

This command writes `requirements.json` under `.enaible/artifacts/research/<timestamp>/` and prints the path.

For large question sets, provide a JSON array via `--questions-file`.

## Scope Definition Examples

**Geographic**: "Focus on North American market only" vs "Global analysis"
**Temporal**: "Current state (last 12 months)" vs "5-year trend analysis"
**Domain**: "B2B SaaS only" vs "All software delivery models"
**Competitor count**: "Top 5 direct competitors" vs "Full competitive landscape"

## Output Format Options

- **Executive Brief**: 2-3 pages, key findings and recommendations only
- **Detailed Report**: Comprehensive analysis with methodology and appendices
- **Competitive Matrix**: Tabular comparison of key attributes
- **Technical Assessment**: Implementation-focused with code examples
- **User Research Summary**: Personas, journey maps, and behavioral insights
