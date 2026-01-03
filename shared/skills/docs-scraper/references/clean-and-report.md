# Clean, Attribute, and Report

## Clean & normalize

1. Remove navigation-only sections (sidebars, breadcrumbs, footers) while preserving anchors for real documentation.
2. Consolidate duplicate headings. Ensure the hierarchy progresses with `#`, `##`, `###` without skipping levels.
3. Keep all code blocks exactly as scraped, including language hints.
4. Rewrite relative links into absolute URLs when they would otherwise break outside the original site.
5. Save the cleaned markdown back to the same file under `@ARTIFACT_ROOT/output/`.

> Tip: When large sections must be deleted, leave an HTML comment so reviewers know the omission was intentional, e.g. `<!-- Removed marketing carousel -->`.

## Source attribution

- Verify the `Source:` line reflects the final URL (after redirects) for each markdown file.
- Confirm the `Scraped:` timestamp is in UTC and matches the capture date; update it if manual edits occur on a later day.
- When you merge multiple pages into one artifact, add a bulleted list of sources below the header so downstream users can trace provenance.
- Never remove the Source/Scraped block—even when the user requests a raw copy—because the audit log depends on it.

## Save & report

1. Keep every output in `@ARTIFACT_ROOT/output/` and every log in `@ARTIFACT_ROOT/logs/`. Do not leak files elsewhere.
2. Assemble a brief run summary covering:
   - URLs requested vs. successfully scraped
   - Output filenames and sizes
   - Log paths for each capture
   - Manual workarounds or fallbacks
3. Highlight any follow-ups (e.g., authentication blockers, missing sections) so the user can take action.
4. Attach the summary and key logs to your final response or ticket per workspace conventions.
