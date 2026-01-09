# Purpose

Standardize research deliverable formats for consistency and actionability.

## Deterministic Report Assembly

Generate the final report using the structured artifacts produced in this skill:

- `requirements.json`
- `domain-plan.json`
- `analysis.json`
- `evidence.json`

Run the report generator:

```bash
"$PYTHON_CMD" scripts/research_report.py \
  --title "<Report Title>" \
  --requirements-path "@ARTIFACT_ROOT/requirements.json" \
  --domain-plan-path "@ARTIFACT_ROOT/domain-plan.json" \
  --analysis-path "@ARTIFACT_ROOT/analysis.json" \
  --evidence-path "@ARTIFACT_ROOT/evidence.json" \
  --output-path "@ARTIFACT_ROOT/report.md"
```

### Analysis JSON format

```json
{
  "analysisAt": "2026-01-09T00:00:00Z",
  "executiveSummary": "2-3 paragraph summary",
  "findings": [
    {
      "id": "f1",
      "title": "Finding title",
      "statement": "Finding statement",
      "confidence": "high",
      "importance": "key",
      "sourceIds": ["src-001", "src-002", "src-003"]
    }
  ],
  "insights": [
    {
      "id": "i1",
      "statement": "Cross-domain insight",
      "sourceIds": ["src-001"]
    }
  ],
  "recommendations": [
    {
      "id": "r1",
      "action": "Do the thing",
      "rationale": "Why this matters",
      "priority": "high",
      "sourceIds": ["src-001"]
    }
  ],
  "limitations": ["Constraint or caveat"]
}
```

Allowed values:

- `confidence`: `high`, `medium`, `low`
- `importance`: `key`, `supporting`, `background`
- `priority`: `high`, `medium`, `low`

## Report Structure Template

```markdown
# [Research Topic]: Comprehensive Analysis

## Executive Summary

[2-3 paragraph overview of key findings and strategic recommendations]

## Table of Contents

1. Research Objectives
2. Methodology
3. Key Findings
4. Synthesis and Insights
5. Recommendations
6. Limitations and Future Research
7. References
8. Appendices

## 1. Research Objectives

- Primary research questions addressed
- Scope and boundaries defined
- Key stakeholders and decision context

## 2. Methodology

### Research Approach

- Data sources utilized (minimum 3 sources per key finding)
- Analysis methods employed
- Quality assurance measures implemented

### Domain Coverage

| Domain   | Focus Areas | Sources Consulted |
| -------- | ----------- | ----------------- |
| [Domain] | [Areas]     | [Count/types]     |

## 3. Key Findings

### 3.1 [Finding Category]

[Findings organized by theme, not by research domain]
[Each major claim with inline citations]
[Include conflicting viewpoints where relevant]

## 4. Synthesis and Insights

- Cross-cutting patterns across research domains
- Connections between different findings
- Strategic implications
- Confidence assessment

## 5. Recommendations

1. **[Priority 1]**: [Recommendation with evidence citations]
2. **[Priority 2]**: [Recommendation with justification]
3. **[Priority 3]**: [Recommendation based on synthesis]

## 6. Limitations and Future Research

- Research constraints encountered
- Areas requiring further investigation
- Confidence levels for key findings
- Recommended follow-up studies

## References

[1] Title. Author/Organization. (Date). URL: [link]
[2] Title. Author/Organization. (Date). URL: [link]
...

## Appendices

### Appendix A: Detailed Evidence

[Data tables, extended quotes, raw research notes]

### Appendix B: Search Methodology

[Queries used, databases searched, refinement process]

### Appendix C: Source Assessment

[Credibility evaluation for key sources]
```

## Executive Summary Guidelines

### Structure

1. **Context** (1-2 sentences): Why this research was conducted
2. **Key Findings** (3-5 bullets): Most important discoveries
3. **Implications** (2-3 sentences): What this means for decisions
4. **Recommendations** (2-3 bullets): Priority actions

### Length

- Executive brief: 150-250 words
- Detailed report: 300-500 words

## Findings Organization

### By Theme (Preferred)

Organize findings by topic or theme rather than by research domain or methodology. This creates a more coherent narrative.

**Good**: "Competitive Positioning", "User Adoption Barriers", "Technical Feasibility"

**Avoid**: "Market Research Findings", "Technical Research Findings", "User Research Findings"

### Evidence Integration

For each major finding:

- State the finding clearly
- Provide supporting evidence with citations
- Note confidence level if not HIGH
- Include relevant counter-evidence or limitations

## Recommendations Format

### Structure

Each recommendation should include:

1. **Action**: What to do (specific and actionable)
2. **Rationale**: Why this matters (link to findings)
3. **Evidence**: Citations supporting this recommendation
4. **Priority**: High/Medium/Low with justification

### Example

```markdown
**Recommendation**: Focus initial market entry on mid-market SaaS companies

**Rationale**: This segment shows highest growth (23% YoY) with underserved
needs that align with our differentiators [1][2].

**Evidence**: Market analysis shows mid-market represents $4.2B opportunity
[3], and user research indicates strong demand for our key features [4][5].

**Priority**: HIGH - Aligns competitive advantages with market opportunity
```

## Output Format Variations

### Executive Brief (2-3 pages)

- Executive summary only
- Top 5 findings in bullets
- Top 3 recommendations
- Key sources listed

### Detailed Report (10-20 pages)

- Full structure as templated above
- Comprehensive methodology
- All findings with evidence
- Complete appendices

### Competitive Matrix

- Tabular comparison format
- Feature/capability rows
- Competitor columns
- Scoring or assessment indicators

### Technical Assessment

- Implementation-focused structure
- Code examples where relevant
- Architecture diagrams
- Performance benchmarks
