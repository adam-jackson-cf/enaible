---
name: research
description: Conduct structured multi-domain research with validated sources and synthesized findings. USE WHEN the user needs market analysis, competitive intelligence, technical research, user research, or comprehensive multi-domain investigations.
compatibility: Requires network access for web search/fetch.
allowed-tools: @WEB_SEARCH @WEB_FETCH @READ @WRITE
---

# Research

Orchestrate thorough research investigations across market, technical, and user domains with validated sources and synthesized findings.

- You need competitive intelligence, market sizing, or industry analysis
- You require technical documentation research, implementation pattern analysis, or architectural review
- You want user persona development, journey mapping, or behavioral analysis
- You must synthesize findings from multiple research domains into actionable recommendations

## Need to...? Read This

| Goal                             | Reference                                                                  |
| -------------------------------- | -------------------------------------------------------------------------- |
| Gather and validate requirements | [references/requirement-gathering.md](references/requirement-gathering.md) |
| Validate sources and citations   | [references/source-validation.md](references/source-validation.md)         |
| Conduct market research          | [references/market-research.md](references/market-research.md)             |
| Research technical topics        | [references/technical-research.md](references/technical-research.md)       |
| Analyze user behavior            | [references/user-research.md](references/user-research.md)                 |
| Structure the final report       | [references/report-structure.md](references/report-structure.md)           |

## Workflow

### Step 0: Requirement Gathering

**Purpose**: Validate research scope, constraints, and output expectations before beginning.

- Confirm the research objective and specific questions to answer
- Identify scope boundaries (geographic, temporal, domain-specific)
- Establish output format requirements and decision context
- Determine applicable research domains (market, technical, user, or combination)
- Plan required online research channels (search engines, documentation portals, APIs) and confirm @WEB_SEARCH/@WEB_FETCH access is available
- Create artifact directory at `.enaible/artifacts/research/<timestamp>/`

See [references/requirement-gathering.md](references/requirement-gathering.md) for the intake checklist.

### Step 1: Domain Allocation

**Purpose**: Map research questions to appropriate research methodologies.

- Classify each research question by domain type
- For multi-domain investigations, dispatch research tasks concurrently where feasible
- Coordinate cross-domain dependencies (e.g., technical constraints affecting market sizing)

**Domain allocation matrix:**

| Question Type                              | Domain    | Reference                                                 |
| ------------------------------------------ | --------- | --------------------------------------------------------- |
| Competitor analysis, market size, pricing  | Market    | [market-research.md](references/market-research.md)       |
| API patterns, architecture, implementation | Technical | [technical-research.md](references/technical-research.md) |
| User needs, personas, journeys             | User      | [user-research.md](references/user-research.md)           |

### Step 2: Execute Research

**Purpose**: Conduct domain-specific research following established methodologies.

- Apply the appropriate research framework for each domain
- Execute fresh online research for each question using @WEB_SEARCH/@WEB_FETCH (or equivalent live data sources) unless the user explicitly prohibits external access
- Gather minimum 3 sources per key finding, ensuring at least one comes from online research conducted during this engagement
- Document source URLs, access dates, and relevance scores
- Capture conflicting information for synthesis

Detailed workflows in domain-specific reference files.

### Step 3: Source Validation

**Purpose**: Verify source quality and cross-validate key findings.

- Assess source credibility (authority, recency, bias indicators)
- Cross-validate claims across multiple independent sources
- Flag findings with single-source support
- Document validation status for each major finding

See [references/source-validation.md](references/source-validation.md) for validation criteria.

### Step 4: Synthesis

**Purpose**: Integrate findings across domains and resolve conflicts.

- Identify patterns and correlations across research domains
- Resolve conflicting findings with evidence-based reasoning
- Generate actionable insights from synthesized data
- Document confidence levels for conclusions

### Step 5: Report Generation

**Purpose**: Produce structured deliverable matching output requirements.

- Follow the report structure template for the requested format
- Include executive summary with key findings and recommendations
- Document methodology, sources, and limitations
- Provide appendices for detailed evidence

See [references/report-structure.md](references/report-structure.md) for output templates.

## Quality Standards

### Source Requirements

- Minimum 3 sources per key finding, must include citations direct to referenced material
- Diverse source types (primary data, industry reports, documentation)
- Recency appropriate to topic (prefer last 12 months for market data); rerun online searches or seek updated sources whenever findings rely on older material
- Record search terms, engines/APIs queried, and timestamps for every online research action to prove recency

### Citation Format

All findings must include inline citations: `[Source Name, Date]`

Full source details in References section of final report.

### Confidence Levels

- **High**: 3+ corroborating sources, no conflicts
- **Medium**: 2 sources or minor conflicts resolved
- **Low**: Single source or unresolved conflicts (flag explicitly)
