# Purpose

Ensure research quality through rigorous source assessment and cross-validation.

## Source Credibility Criteria

### Authority Assessment

- **Institutional backing**: Academic institutions, established research firms, government agencies
- **Domain expertise**: Author credentials, organizational reputation
- **Editorial process**: Peer review, editorial oversight, fact-checking standards
- **Track record**: Historical accuracy and reliability

### Recency Requirements

| Topic Type            | Preferred Age | Maximum Age |
| --------------------- | ------------- | ----------- |
| Market data           | < 6 months    | 12 months   |
| Technology trends     | < 12 months   | 24 months   |
| User behavior         | < 12 months   | 24 months   |
| Academic research     | < 24 months   | 5 years     |
| Foundational concepts | Any age       | Any age     |

### Bias Indicators

- **Funding sources**: Who sponsored the research?
- **Organizational interest**: Does the source benefit from particular findings?
- **Editorial stance**: Known political or commercial leanings?
- **Methodology transparency**: Are methods clearly documented?

## Cross-Validation Requirements

### Minimum Source Counts

- **Key findings**: 3+ independent sources required (at least one gathered via current online research during this engagement)
- **Supporting claims**: 2+ sources preferred
- **Background context**: 1 authoritative source acceptable

### Validation Process

1. Identify core claims requiring validation
2. Run fresh online searches (unless explicitly disallowed) to locate independent corroboration
3. Note alignment or conflict between sources
4. Document validation status for each claim along with search terms, engines/APIs, and access dates

## Deterministic Validation Workflow

### Required inputs

- `requirements.json`
- `domain-plan.json`
- `evidence.json` (normalized)

### Run validation

```bash
"$PYTHON_CMD" scripts/research_validate.py \
  --requirements-path "@ARTIFACT_ROOT/requirements.json" \
  --domain-plan-path "@ARTIFACT_ROOT/domain-plan.json" \
  --evidence-path "@ARTIFACT_ROOT/evidence.json" \
  --output-path "@ARTIFACT_ROOT/validation.json"
```

The validator fails fast if minimum source counts, recency, or diversity requirements are not met.

Use `--allow-undated <question-id>` or `--allow-single-type <question-id>` only when explicitly approved, and capture the rationale in the final report limitations.

### Conflict Resolution

When sources conflict:

1. Assess relative authority of conflicting sources
2. Check for methodological differences explaining variance
3. Note the conflict explicitly in findings
4. Provide reasoned assessment of most likely truth
5. Assign lower confidence level to conflicted findings

## Single-Source Exception Documentation

When only one source exists:

```markdown
**Single-Source Finding**

- Claim: [statement]
- Source: [citation]
- Reason for single source: [explanation]
- Confidence: LOW
- Recommendation: [additional research needed / acceptable for context]
```

## Citation Format Standards

### Inline Citations

Use bracketed references: `[Source Name, Date]`

Example: "The market grew 15% year-over-year [Gartner, 2025]"

### Full Reference Format

```
[#] Title. Author/Organization. (Date). URL: [link]
```

Example:

```
[1] Cloud Computing Market Analysis 2025. Gartner Research. (January 2025). URL: https://example.com/report
```

### Source Type Indicators

- [R] = Research report / Industry analysis
- [A] = Academic / Peer-reviewed
- [O] = Official documentation / Primary source
- [N] = News / Trade publication
- [C] = Community / User-generated

## Confidence Level Assignment

| Level  | Criteria                                                      | Indicator        |
| ------ | ------------------------------------------------------------- | ---------------- |
| HIGH   | 3+ corroborating sources, no conflicts, authoritative sources | No flag needed   |
| MEDIUM | 2 sources, or minor conflicts resolved                        | Note in findings |
| LOW    | Single source, or unresolved conflicts                        | Flag explicitly  |
