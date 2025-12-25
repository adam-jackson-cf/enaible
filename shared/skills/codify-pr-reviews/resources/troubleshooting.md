# Troubleshooting

Common issues and fixes when running codify-pr-reviews.

## No patterns found

- Increase date range (e.g., 180 days).
- Lower minimum occurrence threshold.
- Lower minimum comment length.

## gh CLI not found or not authenticated

```bash
gh --version
gh auth status
```

Install and authenticate if needed:

```bash
brew install gh

# then

gh auth login
```

## Repository not detected

```bash
git remote -v
```

Ensure `origin` points to the correct GitHub repo.

## Generated rules don't match stack

- Re-run stack analysis with refresh.
- Edit red flags manually if detection is incorrect.

## Rule application failed

- Ensure instruction files exist.
- Verify target section headings.
- Confirm no uncommitted changes block edits.
