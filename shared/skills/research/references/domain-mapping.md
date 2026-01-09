# Purpose

Map research questions to deterministic domains using a controlled keyword/regex map.

## Variables

### Required

- @REQUIREMENTS_PATH — requirements JSON (`@ARTIFACT_ROOT/requirements.json`)
- @OUTPUT_PATH — domain plan JSON (`@ARTIFACT_ROOT/domain-plan.json`)

### Optional

- @DOMAIN_MAP_PATH — domain map (`assets/domain-map.json`)
- @RECENCY_POLICY_PATH — recency policy (`assets/recency-policy.json`)
- @OVERRIDE — question override in the form `question_id=domain[,domain]`

## Workflow

1. **Run domain mapping**

   ```bash
   "$PYTHON_CMD" scripts/research_domain_plan.py \
     --requirements-path "@REQUIREMENTS_PATH" \
     --output-path "@OUTPUT_PATH" \
     --recency-policy-path "@RECENCY_POLICY_PATH"
   ```

2. **Handle ambiguity**
   - If the script reports ambiguous or missing matches, rerun with `--override`:

   ```bash
   "$PYTHON_CMD" scripts/research_domain_plan.py \
     --requirements-path "@REQUIREMENTS_PATH" \
     --output-path "@OUTPUT_PATH" \
     --override "q2=technical" \
     --override "q3=market"
   ```

## Output

- `domain-plan.json` with per-question `primaryDomain`, `recencyPolicy`, and expected source types.
