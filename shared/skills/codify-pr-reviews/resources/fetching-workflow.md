# Purpose

Fetch pull request review comments from GitHub using the gh CLI, with a mandatory preflight approval checkpoint.

## Variables

### Required

- @REPO — repository in `owner/name` format (auto-detected from git remote when omitted)
- @DAYS_BACK — number of days to include
- @OUTPUT_PATH — output JSON path for fetched comments
- @RUN_ID — unique run identifier

### Optional

- @EXCLUDE_AUTHORS — list of bot/user logins to exclude
- @MIN_COMMENT_LENGTH — ignore comments shorter than this length

## Instructions

- Ask the user to confirm the Python command and set `PYTHON_CMD` (must be 3.12+).
- Always run the preflight checks first and STOP for user confirmation before full fetch.
- Fetch both review comments (line-level) and issue comments (general).
- Do not attempt to filter by “resolved”; capture everything in range.
- Return summary counts after preflight and after full fetch.

## Defaults

- Optional parameters fall back to `config/defaults.json` when omitted.

## Workflow

1. **Preflight check (MANDATORY)**
   - Run the deterministic preflight (script performs gh auth + sampling):
     ```bash
     "$PYTHON_CMD" scripts/fetch_comments.py \
       --preflight \
       --repo "@REPO" \
       --days-back "@DAYS_BACK"
     ```
   - **STOP** and @ASK_USER_CONFIRMATION before proceeding with full fetch.

2. **Full fetch**
   - Run the deterministic fetch (script performs listing + filtering):
     ```bash
     "$PYTHON_CMD" scripts/fetch_comments.py \
       --repo "@REPO" \
       --days-back "@DAYS_BACK" \
       --exclude-authors "@EXCLUDE_AUTHORS" \
       --min-comment-length "@MIN_COMMENT_LENGTH" \
       --output-path "@OUTPUT_PATH"
     ```

3. **Write output**
   - Save JSON to @OUTPUT_PATH.
   - Provide summary: PR count, comment count, review vs issue totals.

## Output

```json
{
  "fetchedAt": "2025-10-30T14:30:30Z",
  "repository": "owner/repo",
  "dateRange": { "start": "2025-08-01", "end": "2025-10-30" },
  "totalPRs": 45,
  "totalComments": 450,
  "pullRequests": [
    {
      "number": 123,
      "title": "Add user authentication",
      "comments": [
        {
          "id": 789,
          "type": "review",
          "author": "reviewer1",
          "body": "SQL injection vulnerability",
          "path": "backend/src/routes/auth.ts",
          "line": 45,
          "createdAt": "2025-08-15T11:20:00Z"
        }
      ]
    }
  ]
}
```
