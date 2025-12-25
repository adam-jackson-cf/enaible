# Troubleshooting

## Missing API key

```bash
echo $PARALLEL_API_KEY
```

Set it in your shell and re-run:

```bash
export PARALLEL_API_KEY="your-key"
```

## CLI not found

```bash
uv run --directory tools/parallel parallel --help
```

If missing, run:

```bash
cd tools/parallel
uv sync
```

## Request failures

- Confirm the API key is valid at https://platform.parallel.ai
- Retry with `--max-results 1` to validate connectivity
