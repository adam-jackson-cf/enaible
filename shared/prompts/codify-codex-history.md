# Purpose

Codify recurring errors, fixes, and user preferences from recent Codex sessions, then propose AGENTS.md updates for approval.

## Environment checks

- !`python --version` — Exit if Python unavailable.
- !`test -f shared/context/context_bundle_capture_codex.py` — Exit if capture script missing.
- !`PYTHONPATH="shared" python -c "import context.context_bundle_capture_codex; print('env OK')"` — Exit if import fails.
- !`test -d "$HOME/.codex/sessions"` — Exit if no Codex sessions directory.

## Variables

- `DAYS` (default 7) — Lookback window.
- `UUID` — Optional session filter.
- `SEARCH_TERM` — Optional semantic filter.
- `MAX_CHARS` (default 150000) — Total history budget.
- `CHUNK_SIZE` (default 15000) — Per‑subagent input budget.
- `SESSIONS_MAX` (default 24) — Max sessions sampled.
- `MERGE_TARGET` — `project` | `user-codex` | `user-opencode`.
- `$ARGUMENTS` — Raw argument string.

## Instructions

- Use the capture script; restrict reads to `~/.codex/sessions/**`.
- Honor redaction; never print secrets or credentials.
- Enforce budgets: do not exceed `MAX_CHARS` total or `CHUNK_SIZE` per subagent.
- Sample head+tail when truncating; keep chronological order.
- Summarize into: errors, fixes, preferences, anti‑patterns.
- Compare against project and user AGENTS.md; flag duplicates, gaps, contradictions.
- Output a merge‑ready proposal; do not auto‑edit files.

## Workflow

1. Read rules: `./AGENTS.md`, `~/.codex/AGENTS.md`; normalize for comparison.
2. Capture: `PYTHONPATH=shared python shared/context/context_bundle_capture_codex.py --days ${DAYS:-7} ${UUID:+--uuid "$UUID"} ${SEARCH_TERM:+--search-term "$SEARCH_TERM"} --output-format json`.
   - Keep `assistant_message`, `tool_output`, `bash`, `file_change`, `turn.*`.
   - Select up to `SESSIONS_MAX` sessions (recency + error density).
3. Build corpus: per‑session documents in order; chunk to `CHUNK_SIZE` with head+tail sampling until `MAX_CHARS` reached.
4. Summarize: for each chunk, run `codex exec` subagent; emit YAML with `errors[]`, `fixes[]`, `preferences[]`, `notes[]`; store in `.workspace/codify-history/`.
5. Consolidate: merge YAML; normalize text; rank by frequency and severity; classify as Always Reinforce, Prevent, Duplicate, One‑off.
6. Compare: diff against rules; note overlaps and contradictions.
7. Propose: for each candidate, provide rule text, one‑line rationale, evidence (session id + timestamp), and recommended target (project or user). Await approval to apply.

## Output

```md
# RESULT

- Summary: Proposed codified rules from Codex history (last ${DAYS:-7} days), compared to AGENTS.md; ready for review.

## DETAILS

- What changed

  - Consolidated errors, fixes, preferences, and anti‑patterns (≤ ${MAX_CHARS:-150000} chars).
  - Compared to: ./AGENTS.md, ~/.codex/AGENTS.md, ~/.config/opencode/AGENTS.md.
  - Prepared merge‑ready rule blocks with rationale and evidence.

- Where it changed

  - Artifacts: ./.workspace/codify-history/\*.yaml (session summaries)
  - Proposal: printed for copy/paste into AGENTS.md

- How to verify
  - Re‑run with different `DAYS`/`UUID` to spot‑check.
  - Inspect `.workspace/codify-history/*.yaml` for accuracy and redaction.
  - Confirm no duplication with existing rules; approve merge targets.
```

## Examples (optional)

```bash
# Defaults (7‑day lookback, 150k budget)
/codify-codex-history

# Focus a session and lower budgets
/codify-codex-history --uuid 2025-10-10T21-33-01Z --max-chars 80000 --chunk-size 8000

# Filter by topic
/codify-codex-history --search-term "drizzle migration" --days 14

# Prefer user‑level Codex rules
/codify-codex-history --merge-target user-codex
```
