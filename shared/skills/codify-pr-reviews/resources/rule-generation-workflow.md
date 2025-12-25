# Purpose

Generate instruction rule drafts (new or strengthen) from approved patterns.

## Variables

### Required

- @PATTERNS_PATH — approved patterns JSON (`@ARTIFACT_ROOT/patterns.json`)
- @TARGET_SYSTEM — target system identifier (`claude-code`, `codex`, `copilot`, `cursor`, or `gemini`)
- @INSTRUCTION_FILES — mapping of instruction files to update (derived from @TARGET_SYSTEM)
- @OUTPUT_DIR — directory for draft rule markdown files (`@ARTIFACT_ROOT/drafts/`)

## Instructions

- Ask the user to confirm the Python command and set `PYTHON_CMD` (must be 3.12+).
- Resolve @TARGET_SYSTEM and derive @INSTRUCTION_FILES using `resources/system-targeting.md`.
- Generate drafts with clear directives and examples.
- Use positive directives (ALWAYS/NEVER) with stack-appropriate code.
- Keep instruction files under 4000 characters; split if necessary.
- Return summary of drafts by target file.

## Defaults

- Instruction file mapping falls back to `config/defaults.json`.

## Workflow

1. **Run deterministic rule generation**
   - Execute the script to draft new or strengthened rules:
     ```bash
     "$PYTHON_CMD" scripts/generate_rules.py \
       --patterns-path "@PATTERNS_PATH" \
       --instruction-files "@INSTRUCTION_FILES" \
       --output-dir "@OUTPUT_DIR" \
       --repo-root "."
     ```

2. **Review drafts**
   - For `create`: ensure a complete rule with bad/good examples.
   - For `strengthen`: ensure a clear addendum to the existing rule.

3. **User approval (Stage 7)**
   - Pause and @ASK_USER_CONFIRMATION for each draft decision.

4. **Write drafts**
   - Save to @OUTPUT_DIR using `draft-{target}-{action}-{pattern}.md` so every draft sits in `.enaible/artifacts/codify-pr-reviews/<timestamp>/drafts/`.

## Output

```text
@OUTPUT_DIR/
  draft-backend-NEW-rate-limiting.md
  draft-backend-STRENGTHEN-sql-injection.md
  draft-frontend-NEW-react-keys.md
```
