# Copilot Coding Agent: Documentation Workflow Notes

This note captures what we learned while building the Copilot-powered documentation reviewer so future GitHub Actions can reuse the same approach.

## 1. Workflow Triggers and Scope

- Use `pull_request` for every PR event you want Copilot to inspect (`opened`, `reopened`, `synchronize`, `ready_for_review`), plus `push` on `refs/heads/main` so merged commits still get a doc sweep.
- Keep push execution tightly scoped. During validation we temporarily allowed a throwaway branch to exercise the push path, but the final workflow only runs pushes on `main`.
- Guard against Copilot's own follow-up PRs. The workflow bails out whenever `github.actor == 'app/copilot-swe-agent'` or when the PR has the `copilot-doc-review` label. Label only Copilot-authored PRs with `copilot-doc-review` so the recursion guard can identify them while leaving human PRs unaffected.

## 2. Preparing the Brief

- Centralize brief generation in a helper (`.github/workflows/helpers/copilot_doc_review_prompt.py`) that:
  - Enumerates every `README.md` and `AGENTS.md` across the repo (skipping caches/fixtures).
  - Builds commit summaries, diff stats, and a targeted diff block.
  - Writes the instructions markdown (`copilot-doc-review.md`) that both PR comments and push issues reference.
- Include explicit guidance in the brief about roles (README = end-user guidance, AGENTS = developer/LLM rules) so Copilot edits the right file.

## 3. PAT & Assignment Requirements

- GitHub only accepts `agent_assignment` payloads from user PATs. Store a PAT with `repo` scope as the `COPILOT_ASSIGNMENT_TOKEN` repository secret.
- Fail fast on pushes if the secret is missing; the workflow prints a clear error so maintainers know to add the PAT.
- Use `actions/github-script` with the PAT to open/refresh a `copilot-doc-review` issue, including:
  - `agent_assignment` block specifying `target_repo`, `base_branch`, and task instructions.
  - `assignees: ['copilot-swe-agent[bot]']` so the coding agent actually picks up the issue.

## 4. Avoiding Duplicated Noise

- PR leg uses `peter-evans/create-or-update-comment` with `comment-id: copilot-doc-review` so the automation edits a single standing comment instead of spamming every update.
- Push leg reuses the single issue tagged `copilot-doc-review`. When new commits land, the workflow updates the same issue instead of filing duplicates.
- Copilot-authored PRs (e.g., branch `copilot/audit-docs-for-changes`) still need human approval to run Actions; expect the yellow "Workflows awaiting approval" banner and have a maintainer press "Approve workflows to run". The workflow automatically labels those PRs with `copilot-doc-review` so the recursion guard can skip them while leaving human PRs unaffected.

## 5. Quality Gates & Local Feedback

- Pre-commit is wired to `scripts/run-ci-quality-gates.sh --fix --stage`, so every commit executes linting, tests, prompt validation, and formatter steps before push.
- Keep AGENTS/README docs aligned with the workflow. We documented the PAT requirement, skip guard, and push-scope bullets inside `AGENTS.md` so contributors understand how to set up new Actions.

## 6. Testing Strategy

- When validating changes, create a disposable branch and add temporary markers inside the AGENTS docs so Copilot has something to diff. Remove those markers once automation is confirmed.
- After testing, delete temporary branches and revert any broadened push scopes to avoid lingering background runs.

## 7. Reusing the Pattern

To build a new Copilot-driven workflow (for example, auto-updating API docs):

1. Copy the structure from `.github/workflows/copilot-doc-review.yml`.
2. Write a helper script that collects just the files the agent should touch.
3. Set up the PAT + issue assignment block with instructions tailored to the new doc set.
4. Add concise documentation (AGENTS-style) explaining:
   - Trigger conditions.
   - Required secrets.
   - Guardrails (no recursive Copilot runs, no fallback modes).
5. Test on a temporary branch, then lock push execution down to `main`.

Following this checklist ensures new GitHub Actions can enlist the Copilot coding agent without falling into infinite loops or missing the required authentication pieces. The existing documentation reviewer serves as a working example you can mirror for other automation goals.
