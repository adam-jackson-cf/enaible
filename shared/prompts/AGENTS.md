# Shared Prompt Authoring Guide

1. Author the source prompt in `shared/prompts/<name>.md`. Edit `docs/system/<system>/templates/` only when you need new frontmatter/layout tokens.
2. Run guards after any edit:

```bash
uv run --project tools/enaible enaible prompts lint
uv run --project tools/enaible enaible prompts render --prompt all --system all
uv run --project tools/enaible enaible prompts diff
```

3. Validate end-to-end: reinstall each affected system

```bash
uv run --project tools/enaible enaible install <system> --mode sync --scope project
```

Then exercise any analyzer calls via `enaible analyzers run ...` and keep artifacts under `.enaible/artifacts/<task>/<timestamp>/`. 4) Tests: add or update deterministic prompt fixtures in `shared/tests` when outputs are stable; otherwise rely on the drift checks above.
