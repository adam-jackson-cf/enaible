# Troubleshooting

## Missing API key

```bash
echo $PARALLEL_API_KEY
```

Set it in your shell and re-run:

```bash
export PARALLEL_API_KEY="your-key"
```

## Python command issues

- Ask the user which Python command to use and verify 3.12+ with `<python-cmd> --version`.
- Ensure you use the same `PYTHON_CMD` in all script calls.

## Request failures

- Confirm the API key is valid at https://platform.parallel.ai
- Retry with a minimal request, e.g. `--max-results 1`, to validate connectivity
