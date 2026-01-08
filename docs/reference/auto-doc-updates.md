# Copilot Coding Agent: Documentation Workflow Notes

This note captures what we learned while building the Copilot-powered documentation reviewer so future GitHub Actions can reuse the same approach.

## Current Status

The workflow is intentionally disabled. The Copilot coding agent can only be invoked when attached to an issue or pull request. That means a “CI-style” check (detect doc drift and then open a ticket only if drift exists) is not possible today, because the trigger itself must already be an issue or PR. This creates an assumption that documentation work is already needed, which is the opposite of a pure detection gate.

We have kept the workflow and helper script in the repo, but it is not initialized until Copilot supports agent runs that can be triggered from CI and then decide whether to open a PR/issue.

## Limitations Blocking CI-Style Usage

- Copilot coding agent runs must be attached to a PR or issue event.
- A push-triggered “detect then decide” flow is not supported; it must open an issue/PR first to invoke the agent.
- This makes it impossible to run a neutral drift check that only files an issue when divergence is found.

## Recursion Guard & Safety Tradeoffs

To avoid recursive doc-review runs (Copilot opening PRs that then trigger more doc reviews), we rely on label-based guards. That alone is not sufficient to prevent approval prompts on forked PRs because GitHub requires approvals before any job steps run.

We attempted a less safe approach to eliminate approvals by switching to `pull_request_target`, which runs in the base-repo context. This is generally riskier because PR code can be untrusted. Our mitigation in the current workflow:

- The job checks out the base branch only.
- It fetches the PR head as a ref (`pr-head`) without checking it out.
- The helper script runs from the base branch and diffs base vs `pr-head`; no PR code is executed directly.
- Copilot-authored PRs are labeled (`copilot-doc-review`) and skipped to prevent recursion.

This is still a tradeoff, which is another reason the workflow is disabled until Copilot supports a safer CI-native agent invocation.

## Re-enabling Later

When Copilot supports CI-triggered agent runs without requiring an existing PR/issue, we can:

1. Re-enable the workflow triggers.
2. Keep the label guard to avoid recursive runs.
3. Remove `pull_request_target` usage if approval prompts are no longer an issue.
