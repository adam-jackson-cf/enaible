---
description: Codify recurring errors, fixes, and preferences from recent OpenCode sessions into AGENTS.md proposals
---

# Purpose

Codify recurring errors, fixes, and user preferences from recent OpenCode sessions, then propose AGENTS.md updates for approval.

## Variables

- `DAYS` (default 7) — Lookback window.
- `UUID` — Optional session filter.
- `SEARCH_TERM` — Optional semantic filter.
- `MAX_CHARS` (default 150000) — Total history budget.
- `CHUNK_SIZE` (default 15000) — Per‑subagent input budget.
- `SESSIONS_MAX` (default 24) — Max sessions sampled.
- `MERGE_TARGET` — `project` | `user-opencode`.

## Instructions

- Verify tooling upfront: `python --version` and `uv run --project tools/enaible enaible context_capture --platform opencode --help >/dev/null` must succeed before running the workflow.
- Use the `enaible context_capture --platform opencode` command; restrict reads to `$HOME/.local/share/opencode/**`.
- Honor redaction; never print secrets.
- Enforce budgets: do not exceed `MAX_CHARS` total or `CHUNK_SIZE` per subagent.
- Sample head+tail when truncating; keep chronological order.
- Summarize into: standards, preferences, ways_of_working, approaches, notes.
- Compare against project and user rules; flag duplicates, gaps, contradictions.
- Output a merge‑ready proposal; do not auto‑edit files.

## Workflow

1. **Sync Enaible Tooling (once per checkout)**

   - Keep dependencies current before capturing history:

     ```bash
     uv sync --project tools/enaible
     ```

2. **Read Rules**

   - Load both project and user-level guidance to avoid duplicating existing standards:
     - `./AGENTS.md`
     - `~/.config/opencode/AGENTS.md`

3. **Capture Session History**

   - Gather OpenCode sessions within the lookback window, respecting optional filters:

     ```bash
     uv run --project tools/enaible enaible context_capture \
       --platform opencode \
       --days ${DAYS:-7} \
       ${UUID:+--uuid "$UUID"} \
       ${SEARCH_TERM:+--search-term "$SEARCH_TERM"} \
       --output-format json
     ```

   - Treat `sessions[].user_messages[]` as primary signal and keep `operations` data for supplementary context.

4. **Build Corpus**

   - For each session, order `user_messages` chronologically, append high-signal `assistant_messages`, and list notable `operations` (commands, file changes) before chunking to `CHUNK_SIZE` until `MAX_CHARS` is reached.

5. **Summarize (Subagent)**

   - Use `opencode exec` to turn each chunk into YAML with `standards`, `preferences`, `ways_of_working`, `approaches`, and `notes`; store temporaries under `.workspace/codify-history/`.

6. **Consolidate Findings**

   - Merge YAML outputs, normalize phrasing, rank by frequency/clarity, and classify items as Always Reinforce, Prevent, Duplicate, or One-off.

7. **Compare Against Existing Rules**

   - Diff the consolidated list with `./AGENTS.md` and `~/.config/opencode/AGENTS.md` to flag overlaps or contradictions.

8. **Propose Updates**

   - Prepare merge-ready rule blocks with rationale, evidence (session id + timestamp), and recommended target (`project` or `user-opencode`).

9. **Cleanup**

   - Remove working artifacts:

     ```bash
     rm -rf .workspace/codify-history || true
     ```

## Output

```md
# RESULT

- Summary: Proposed codified rules from OpenCode history (last ${DAYS:-7} days), compared to AGENTS.md; ready for review.

## DETAILS

- What changed

  - Consolidated standards, preferences, ways_of_working, and approaches (≤ ${MAX_CHARS:-150000} chars).
  - Compared to: ./AGENTS.md, ~/.config/opencode/AGENTS.md.
  - Prepared merge‑ready rule blocks with rationale and evidence.

- Where it changed

  - Proposal: printed for copy/paste into AGENTS.md

- How to verify
  - Re‑run with different `DAYS`/`UUID` to spot‑check.
  - Confirm no duplication with existing rules; approve merge targets.
```

## Examples (optional)

```bash
/codify-opencode-history
/codify-opencode-history --uuid 2025-10-10T21-33-01Z --max-chars 80000 --chunk-size 8000
/codify-opencode-history --search-term "drizzle migration" --days 14
```
