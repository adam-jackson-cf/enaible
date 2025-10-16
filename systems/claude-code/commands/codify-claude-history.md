---
description: "Codify lessons from recent Claude sessions (user/assistant prompts) into personal workflow guidance"
argument-hint: [--uuid UUID] [--search-term TERM] [--days N]
allowed-tools: ["Task", "Read", "Write", "Bash", "Grep", "Glob", "LS"]
---

# Codify Claude History — Lessons & Habits

Derive standards, preferences, ways of working, and approaches from recent Claude session prompts, then propose user-level updates to `~/.claude/CLAUDE.md`.

## Usage

```bash
/codify-claude-history [--days 7] [--uuid <ID>] [--search-term <TEXT>]
```

## Variables

- `DAYS` (default 7): Lookback window for sessions
- `UUID`: Optional session id filter
- `SEARCH_TERM`: Optional semantic filter

## Instructions

- Use the Enaible `context_capture` command (Claude platform) to gather raw history.
- Prefer `sessions[].user_messages` (and `assistant_messages` when present) as the primary signal; treat `operations` as secondary context.
- Focus on standards, preferences, ways_of_working, approaches; ignore tool errors unless they imply a rule.
- Propose user-level changes only; do not edit project files here.

## Workflow

1. Prepare Enaible environment

   - !`uv sync --project tools/enaible`

2. Capture (7-day default)

   - ```
     uv run --project tools/enaible enaible context_capture \
       --platform claude \
       --days ${DAYS:-7} \
       ${UUID:+--uuid "$UUID"} \
       ${SEARCH_TERM:+--search-term "$SEARCH_TERM"} \
       --output-format json
     ```
   - Input fields: `sessions[].user_messages[]`, `sessions[].assistant_messages[]`, `operations[]` (for file footprints)

3. Build corpus

   - For each session: place `user_messages` first (chronological), then 0–2 `assistant_messages` (trimmed), then a short list of file paths from `operations` (file tool ops only).
   - Chunk to ~12k per segment, total ≤ ~200k.

4. Summarize (subagent)

   - Invoke a focused summarizer via Task tool:
     - Return YAML with keys: `standards`, `preferences`, `ways_of_working`, `approaches`, `notes` (lists of short items).
     - No prose or code blocks.

5. Consolidate & propose

   - Merge YAML across chunks; sort by frequency and clarity.
   - Produce a merge-ready block for `~/.claude/CLAUDE.md` under “Personal Workflow Habits”.
   - STOP → "Apply to ~/.claude/CLAUDE.md? (y/n)"

6. Cleanup
   - !`rm -rf .workspace/codify-history || true`

## Output

```md
# RESULT

- Summary: Proposed personal workflow updates derived from Claude history (last ${DAYS:-7} days).

## DETAILS

- What changed: Consolidated lessons (standards, preferences, ways_of_working, approaches)
- Where it changed: proposal to append in `~/.claude/CLAUDE.md`
- How to verify: Review session evidence by session id + timestamps; re-run with different `--days`/`--uuid` if needed
```

## Examples

```bash
/codify-claude-history --days 7
/codify-claude-history --uuid 4c0b21b6-b728-46b8-a0d6-b954dd7485ad
/codify-claude-history --search-term "electron traffic lights"
```
