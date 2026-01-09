# Purpose

Log every search and source deterministically so the research trail is auditable.

## Variables

### Required

- @ARTIFACT_ROOT — artifact root for the current run
- @QUESTION_ID — question ID from `requirements.json` / `domain-plan.json`

### Optional

- @EVIDENCE_PATH — override evidence path (defaults to `@ARTIFACT_ROOT/evidence.json`)

## Workflow

### 1. Log search queries

For each search, record the query and engine:

```bash
"$PYTHON_CMD" scripts/research_execute.py search \
  --artifact-root "@ARTIFACT_ROOT" \
  --evidence-path "@EVIDENCE_PATH" \
  --question-id "@QUESTION_ID" \
  --query "<search query>" \
  --engine "<engine or portal>"
```

### 2. Log sources

For every source you keep, record metadata:

```bash
"$PYTHON_CMD" scripts/research_execute.py source \
  --artifact-root "@ARTIFACT_ROOT" \
  --evidence-path "@EVIDENCE_PATH" \
  --question-id "@QUESTION_ID" \
  --url "https://example.com" \
  --title "Source title" \
  --source-type "official-docs" \
  --published-date "2025-11-01" \
  --origin "engagement" \
  --search-id "search-001"
```

If a source is legitimately undated, replace `--published-date` with `--undated-reason "<reason>"` and ensure validation approvals are recorded.

### 3. Batch import sources (optional)

For bulk imports, use a CSV or JSON file:

```bash
"$PYTHON_CMD" scripts/research_execute.py batch \
  --artifact-root "@ARTIFACT_ROOT" \
  --evidence-path "@EVIDENCE_PATH" \
  --input-path "sources.csv"
```

CSV headers must include: `questionId,url,title,sourceType,publishedDate,undatedReason,origin` (optional: `publisher,searchId,citationLabel,notes,retrievedAt`).

### 4. Attach a metadata snapshot (optional)

If you capture metadata during fetch, attach it to the existing source entry:

```bash
"$PYTHON_CMD" scripts/research_execute.py snapshot \
  --artifact-root "@ARTIFACT_ROOT" \
  --evidence-path "@EVIDENCE_PATH" \
  --source-id "src-001" \
  --snapshot-title "Document title" \
  --snapshot-date "2025-10-01"
```

## Outputs

- `evidence.json`
