Analyzer unification is staged behind the Typer-based `enaible` CLI, which will wrap `shared/core/cli/run_analyzer` to emit normalized JSON and remove per-system path discovery so Claude Code, OpenCode, and Codex share one invocation surface.

Prompt templating shifts shared bodies into `shared/prompts` while adapters feed `docs/system/<system>/templates/*.j2`, and the plan wires CI to render and diff managed outputs so prompts that call `enaible analyzers run` stay drift-free alongside the CLI’s lint, type, test, duplication, and complexity gates.
