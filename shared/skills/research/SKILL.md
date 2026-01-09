---
name: research
description: Conduct structured multi-domain research with validated sources, deterministic logging, and synthesized findings. USE WHEN the user needs market analysis, competitive intelligence, technical research, user research, or comprehensive multi-domain investigations.
compatibility: Requires network access for web search/fetch and Python 3.12+ for deterministic scripts.
allowed-tools: @BASH @WEB_SEARCH @WEB_FETCH @READ @WRITE
---

# Research

Run auditable, multi-domain research with deterministic logging, validation, and report assembly.

- You need market/competitive analysis with verifiable sources
- You need technical or implementation research grounded in primary docs
- You need user/behavioral synthesis with explicit evidence trails
- You must produce a report backed by logged searches and citation checks

## Need to...? Read This

| Goal                             | Reference                                                                    |
| -------------------------------- | ---------------------------------------------------------------------------- |
| Capture requirements + artifacts | [references/requirement-gathering.md](references/requirement-gathering.md)   |
| Map questions to domains         | [references/domain-mapping.md](references/domain-mapping.md)                 |
| Log searches + sources           | [references/research-execution.md](references/research-execution.md)         |
| Normalize evidence               | [references/evidence-normalization.md](references/evidence-normalization.md) |
| Validate sources + recency       | [references/source-validation.md](references/source-validation.md)           |
| Assemble analysis                | [references/analysis-assembly.md](references/analysis-assembly.md)           |
| Validate citations               | [references/citation-audit.md](references/citation-audit.md)                 |
| Structure the final report       | [references/report-structure.md](references/report-structure.md)             |
| Conduct market research          | [references/market-research.md](references/market-research.md)               |
| Research technical topics        | [references/technical-research.md](references/technical-research.md)         |
| Analyze user behavior            | [references/user-research.md](references/user-research.md)                   |

## Workflow

### Step 0: Preflight + requirements

**Purpose**: Capture the research brief and create a deterministic artifact root.

- Validate the research objective, scope, decision context, and online research constraints.
- Run `scripts/research_init.py` to write `requirements.json` under `.enaible/artifacts/research/<timestamp>/`.
- Stop and clarify missing requirements before continuing.

See [references/requirement-gathering.md](references/requirement-gathering.md).

### Step 1: Domain mapping

**Purpose**: Deterministically map each question to a research domain.

- Run `scripts/research_domain_plan.py` to generate `domain-plan.json` from `requirements.json`.
- Use `--override` only when the domain map is ambiguous or missing coverage.

See [references/domain-mapping.md](references/domain-mapping.md).

### Step 2: Execute research with logging

**Purpose**: Collect sources while logging every search and source record.

- Use `scripts/research_execute.py search` for each query and `scripts/research_execute.py source` for each source.
- Ensure every source references a question ID and has a published date (or approved undated rationale).
- Produce `evidence.json` in the artifact root.
- Use `scripts/research_execute.py batch` for CSV/JSON imports and `scripts/research_execute.py snapshot` to attach metadata snapshots when needed.

See [references/research-execution.md](references/research-execution.md) and the domain playbooks.

### Step 3: Normalize evidence

**Purpose**: Normalize publisher names and deduplicate sources before validation.

- Run `scripts/research_normalize.py` to update `evidence.json` in place.
- Re-run normalization after any new sources are logged.

See [references/evidence-normalization.md](references/evidence-normalization.md).

### Step 4: Source validation

**Purpose**: Enforce minimum source counts, recency, and diversity before synthesis.

- Run `scripts/research_validate.py` to generate `validation.json`.
- If validation fails, gather additional sources and rerun validation.

See [references/source-validation.md](references/source-validation.md).

### Step 5: Analysis + citation audit

**Purpose**: Consolidate analysis artifacts and verify citations against logged sources.

- Draft an analysis input JSON with findings, insights, recommendations, and limitations.
- Run `scripts/research_analyze.py` to generate `analysis.json`.
- Run `scripts/research_citations.py` to generate `citation-report.json`.

See [references/citation-audit.md](references/citation-audit.md).

### Step 6: Assemble the report

**Purpose**: Produce the final report from validated artifacts.

- Use `analysis.json` with validated findings and recommendations.
- Run `scripts/research_report.py` to output the final report markdown.

See [references/report-structure.md](references/report-structure.md).

## Quality Standards

- Every run must produce: `requirements.json`, `domain-plan.json`, `evidence.json`, `validation.json`, `analysis.json`, `citation-report.json`, and the final `report.md`.
- Each key finding must be backed by ≥3 sources and at least one source collected during this engagement.
- Recency rules must be enforced through `validation.json`; no report should be delivered if validation fails.
- Inline citations must map to `evidence.json` sources and pass `research_citations.py`.
- Artifacts should conform to the JSON schemas in `assets/schemas/`.
- Run evidence normalization before validation to ensure deduped sources and canonical publishers.
