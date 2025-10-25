# Provenance Governance (Local Runner)

This repository can trigger a local Provenance analysis using the self-hosted runner stack defined in `../provenance`.

## Prerequisites

- Run `make docker-start` inside the `provenance` repo to launch Redis, the API, and the dockerised GitHub Actions runner.
- Ensure the repo secrets are set:
  - `PROVENANCE_API_URL` → `http://provenance:8000`
  - `PROVENANCE_API_TOKEN` → token issued by the local Provenance API
- Install and authenticate GitHub CLI (`gh auth login`) with scopes `repo`, `workflow`, `admin:repo_hook` on the machine hosting the runner stack.

## Usage

1. Add the label `provenance` to the pull request you want to analyse.
2. GitHub dispatches the workflow `.github/workflows/provenance-selfhosted.yml` to the local runner (`self-hosted`, `provenance`, `docker`).
3. The job checks out this repo and the Provenance tooling, runs the diff analysis, and uploads SARIF findings back to GitHub.
4. Remove the label to stop subsequent runs, or stop the stack with `make docker-stop` once testing is complete.

The workflow is opt-in, so existing CI remains unchanged unless the label is present.
