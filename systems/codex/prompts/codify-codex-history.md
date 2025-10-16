# Purpose

Codify recurring errors, fixes, and user preferences from recent Codex sessions, then propose AGENTS.md updates for approval.

## Environment checks

- !`python --version` — Exit if Python unavailable.
- !`test -f shared/context/context_bundle_capture_codex.py` — Exit if capture script missing.
- !`PYTHONPATH=shared uv run --project tools/enaible python -c "import context.context_bundle_capture_codex; print('env OK')"` — Exit if import fails.
- !`test -d "~/.codex/sessions"` — Exit if no Codex sessions directory.

## Variables

- `DAYS` (default 7) — Lookback window.
- `UUID` — Optional session filter.
- `SEARCH_TERM` — Optional semantic filter.
- `MAX_CHARS` (default 150000) — Total history budget.
- `CHUNK_SIZE` (default 15000) — Per‑subagent input budget.
- `SESSIONS_MAX` (default 24) — Max sessions sampled.
- `MERGE_TARGET` — `project` | `user-codex`.
- `$ARGUMENTS` — Raw argument string.

## Instructions

- Use the capture script; restrict reads to `~/.codex/sessions/**`.
- Honor redaction; never print secrets.
- Enforce budgets: do not exceed `MAX_CHARS` total or `CHUNK_SIZE` per subagent.
- Sample head+tail when truncating; keep chronological order.
- Summarize into: standards, preferences, ways_of_working, approaches, notes.
- Compare against project and user rules; flag duplicates, gaps, contradictions.
- Output a merge‑ready proposal; do not auto‑edit files.

## Workflow

0. Sync (once per checkout): !`uv sync --project tools/enaible`
1. Read rules: `./AGENTS.md`, `~/.codex/AGENTS.md`.
2. Capture:

   ```bash
   PYTHONPATH=shared \
     uv run --project tools/enaible python shared/context/context_bundle_capture_codex.py \
       --days ${DAYS:-7} \
       ${UUID:+--uuid "$UUID"} \
       ${SEARCH_TERM:+--search-term "$SEARCH_TERM"} \
       --output-format json
   ```

   - Prefer `sessions[].user_messages[]` as primary signal for ways‑of‑working.
   - Keep `operations` as secondary context (assistant_message, tool_output, bash, file_change, turn.\*).

3. Build corpus: per‑session, place `user_messages` first (chronological), then append high‑signal operation headers (commands) and trimmed outputs; chunk to `CHUNK_SIZE` until `MAX_CHARS` reached.
4. Summarize: for each chunk, run `codex exec` subagent; emit YAML with `standards`, `preferences`, `ways_of_working`, `approaches`, `notes`; store temporaries in `.workspace/codify-history/`.
5. Consolidate: merge YAML; normalize text; rank by frequency; classify as Always Reinforce, Prevent, Duplicate, One‑off.
6. Compare: diff against rules; note overlaps and contradictions.
7. Propose: provide rule text, one‑line rationale, evidence (session id + timestamp), and recommended target (project or user). Await approval to apply.
8. Cleanup: !`rm -rf .workspace/codify-history || true`.

## Output

```md
# RESULT

- Summary: Proposed codified rules from Codex history (last ${DAYS:-7} days), compared to AGENTS.md; ready for review.

## DETAILS

- What changed

  - Consolidated standards, preferences, ways_of_working, and approaches (≤ ${MAX_CHARS:-150000} chars).
  - Compared to: ./AGENTS.md, ~/.codex/AGENTS.md.
  - Prepared merge‑ready rule blocks with rationale and evidence.

- Where it changed

  - Proposal: printed for copy/paste into AGENTS.md

- How to verify
  - Re‑run with different `DAYS`/`UUID` to spot‑check.
  - Confirm no duplication with existing rules; approve merge targets.
```

## Examples (optional)

```bash
/codify-codex-history
/codify-codex-history --uuid 2025-10-10T21-33-01Z --max-chars 80000 --chunk-size 8000
/codify-codex-history --search-term "drizzle migration" --days 14
```
