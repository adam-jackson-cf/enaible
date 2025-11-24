# Commands & Analysis Reference

Enaible wraps the shared Python analyzer suite so Codex, Claude Code, and OpenCode deliver consistent findings across security, quality, architecture, performance, and root-cause categories. Use this document to understand the available tools, how to trigger them, and where evidence is stored.

## Listing analyzers

```bash
uv run --project tools/enaible enaible analyzers list
```

This emits JSON describing each registered analyzer, including its registry key (`category:name`) and the implementing class under `shared/analyzers/`.

## Running analyzers

The general invocation is:

```bash
uv run --project tools/enaible enaible analyzers run <category:key> \
  --target <path> \
  --out .enaible/artifacts/<task>/<timestamp>/<name>.json \
  [--summary] [--min-severity <level>] [--exclude '<glob>']
```

- `--target` defaults to the current directory; override it to focus on a service or package.
- `--out` writes normalized JSON to an artifact; omit it to stream to stdout.
- `--summary` produces counts without full findings (useful for triage).
- `--min-severity` accepts `critical|high|medium|low` for analyzers that grade findings.
- `--exclude` accepts repeatable glob patterns for third-party or generated paths.

Artifacts live under `.enaible/artifacts/<task>/<timestamp>/` as recommended by managed prompts.

## Analyzer catalog

| Category     | Registry Keys                                                                                                    | Typical Usage                                                                         |
| ------------ | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Security     | `security:semgrep`, `security:detect_secrets`                                                                    | OWASP-aligned scanning and secrets detection before release.                          |
| Architecture | `architecture:patterns`, `architecture:dependency`, `architecture:coupling`, `architecture:scalability`          | Evaluate layering, domain boundaries, dependency graphs, and scalability constraints. |
| Quality      | `quality:lizard`, `quality:jscpd`, `quality:coverage`, `quality:patterns`, `quality:aggregate`                   | Surface complexity, duplication, coverage gaps, and recurring anti-patterns.          |
| Performance  | `performance:baseline`, `performance:frontend`, `performance:ruff`, `performance:semgrep`, `performance:sqlglot` | Identify bottlenecks spanning backend, frontend, and data layers.                     |
| Root Cause   | `root_cause:trace_execution`, `root_cause:recent_changes`, `root_cause:error_patterns`                           | Investigate incidents, correlate commit history, and highlight repeated failures.     |

All analyzers are registered via `shared/core/base/registry_bootstrap.py` and respect the abstractions defined in `shared/core/base`.

## Integrating with managed prompts

Prompts inside `shared/prompts/` call Enaible analyzers as part of guided workflows. Examples:

- **`analyze-security`**: Runs `security:semgrep` and `security:detect_secrets` before performing gap analysis.
- **`analyze-architecture`**: Executes the architecture suite and collects evidence for pattern and coupling review.
- **`plan-refactor`**: Combines quality, architecture, and performance baselines to inform phased refactor plans.
- **`analyze-root-cause`**: Uses the root-cause analyzers to correlate errors with recent changes and trace data.

Render managed prompts with:

```bash
uv run --project tools/enaible enaible prompts render --prompt all --system all
```

The generated Markdown includes the `<!-- generated: enaible -->` sentinel to signal managed content.

## Producing CI artifacts

After running analyzers locally or inside automation, use the `enaible ci` commands to convert raw findings:

- `enaible ci convert-codeclimate` → merges analyzer JSON into a CodeClimate-compatible array.
- `enaible ci security-markdown` → renders prioritized security notes bounded by strict markers for publishing.

Example:

```bash
uv run --project tools/enaible enaible analyzers run quality:lizard --target . --out artifacts/quality_lizard.json
uv run --project tools/enaible enaible ci convert-codeclimate artifacts --out artifacts/codeclimate.json
```

## Troubleshooting

- Use `uv run --project tools/enaible enaible analyzers run --help` for option details.
- Set `ENAIBLE_DISABLE_EXTERNAL=1` to skip analyzer features requiring network or auxiliary binaries.
- Confirm the workspace with `uv run --project tools/enaible enaible doctor --json`; missing `shared/` paths or `.enaible/schema.json` will surface here.
