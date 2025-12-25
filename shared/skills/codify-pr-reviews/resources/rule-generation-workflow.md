# Purpose

Generate instruction rule drafts (new or strengthen) from approved patterns.

## Variables

### Required

- @PATTERNS_PATH — approved patterns JSON
- @INSTRUCTION_FILES — mapping of instruction files to update
- @OUTPUT_DIR — directory for draft rule markdown files

## Instructions

- Generate drafts with clear directives and examples.
- Use positive directives (ALWAYS/NEVER) with stack-appropriate code.
- Keep instruction files under 4000 characters; split if necessary.
- Return summary of drafts by target file.

## Defaults

- Instruction file mapping falls back to `config/defaults.json`.

## Deterministic tooling

```bash
python scripts/generate_rules.py \
  --patterns-path "@PATTERNS_PATH" \
  --output-dir "@OUTPUT_DIR" \
  --repo-root "."
```

## Workflow

1. **Load approved patterns**
   - Read @PATTERNS_PATH.

2. **Generate drafts**
   - For `create`: build a complete rule with bad/good examples.
   - For `strengthen`: generate an addendum for the existing rule.

3. **Assign targets**
   - Choose backend/frontend/repository/security instruction file based on pattern category.

4. **User approval (Stage 7)**
   - Pause and @ASK_USER_CONFIRMATION for each draft decision.

5. **Write drafts**
   - Save to @OUTPUT_DIR using `draft-{target}-{action}-{pattern}.md`.

## Output

```text
@OUTPUT_DIR/
  draft-backend-NEW-rate-limiting.md
  draft-backend-STRENGTHEN-sql-injection.md
  draft-frontend-NEW-react-keys.md
```
