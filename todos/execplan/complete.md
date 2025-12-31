<file*map>
/Users/adamjackson/LocalDev/enaible
├── .github
│ ├── workflows
│ │ ├── helpers
│ │ │ └── copilot_doc_review_prompt.py +
│ │ ├── package-audit.yml *
│ │ ├── ci-quality-gates-incremental.yml
│ │ ├── copilot-doc-review.yml
│ │ └── install-smoke.yml
│ ├── hooks
│ │ └── beads-precommit.sh
│ └── dependabot.yml
├── docs
│ ├── system
│ │ ├── claude-code
│ │ │ ├── templates
│ │ │ │ ├── command.md.j2 _
│ │ │ │ ├── ...
│ │ │ ├── slash-command.md _
│ │ │ ├── commands.md
│ │ │ ├── hooks.md
│ │ │ ├── marketplaces.md
│ │ │ ├── message-formats.md
│ │ │ ├── model-configuration.md
│ │ │ ├── output-styles.md
│ │ │ ├── plugin-reference.md
│ │ │ ├── plugins.md
│ │ │ ├── settings.md
│ │ │ ├── skills.md
│ │ │ ├── state-machine.md
│ │ │ ├── subagent.md
│ │ │ ├── subagents.md
│ │ │ └── workflow-config.md
│ │ ├── codex
│ │ │ ├── templates
│ │ │ │ ├── prompt.md _
│ │ │ │ ├── prompt.md.j2 _
│ │ │ │ ├── ...
│ │ │ ├── config.md
│ │ │ ├── exec.md
│ │ │ ├── prompts.md
│ │ │ ├── sandbox.md
│ │ │ └── threads.md
│ │ ├── copilot
│ │ │ ├── templates
│ │ │ │ ├── prompt.md.j2 _
│ │ │ │ ├── ...
│ │ │ ├── agents.md
│ │ │ ├── chat-reference.md
│ │ │ ├── copilot-features.md
│ │ │ ├── instructions.md
│ │ │ └── prompts.md
│ │ ├── cursor
│ │ │ ├── templates
│ │ │ │ ├── command.md.j2 _
│ │ │ │ ├── ...
│ │ │ └── rules.md _
│ │ ├── gemini
│ │ │ └── templates
│ │ │ └── command.toml.j2 _
│ │ ├── templates
│ │ │ └── prompt.md _
│ │ └── antigravity
│ │ └── templates
│ │ └── ...
│ ├── skills.md _
│ ├── auto-doc-updates.md
│ ├── dev-logs-unified.png
│ ├── installation.md
│ ├── monitoring.md
│ └── testing.md
├── shared
│ ├── prompts
│ │ ├── AGENTS.md _
│ │ ├── create-rule.md _
│ │ ├── setup-parallel-ai.md _
│ │ ├── analyze-architecture.md
│ │ ├── analyze-code-quality.md
│ │ ├── analyze-performance.md
│ │ ├── analyze-root-cause.md
│ │ ├── analyze-security.md
│ │ ├── create-hand-off.md
│ │ ├── get-codebase-primer.md
│ │ ├── get-feature-primer.md
│ │ ├── plan-refactor.md
│ │ ├── plan-solution.md
│ │ ├── plan-ux-prd.md
│ │ ├── review-docs-drift.md
│ │ ├── setup-atuin.md
│ │ ├── setup-beads.md
│ │ ├── setup-browser-tools.md
│ │ ├── setup-code-precommit-checks.md
│ │ ├── setup-dev-monitoring.md
│ │ ├── setup-mgrep.md
│ │ ├── setup-package-monitoring.md
│ │ └── setup-react-grab.md
│ ├── skills
│ │ ├── codify-pr-reviews
│ │ │ ├── config
│ │ │ │ └── defaults.json _
│ │ │ ├── scripts
│ │ │ │ ├── fetch*comments.py * +
│ │ │ │ ├── preprocess*comments.py * +
│ │ │ │ ├── stack*analysis.py * +
│ │ │ │ ├── ...
│ │ │ ├── resources
│ │ │ │ └── ...
│ │ │ └── SKILL.md
│ │ └── AGENTS.md _
│ ├── analyzers
│ │ ├── architecture
│ │ │ ├── coupling_analysis.py +
│ │ │ ├── dependency_analysis.py +
│ │ │ ├── pattern_evaluation.py +
│ │ │ └── scalability_check.py +
│ │ ├── performance
│ │ │ ├── analyze_frontend.py +
│ │ │ ├── performance_baseline.py +
│ │ │ ├── profile_code.py +
│ │ │ ├── ruff_analyzer.py +
│ │ │ ├── semgrep_analyzer.py +
│ │ │ └── sqlglot_analyzer.py +
│ │ ├── quality
│ │ │ ├── **init**.py +
│ │ │ ├── complexity_lizard.py +
│ │ │ ├── coverage_analysis.py +
│ │ │ ├── jscpd_analyzer.py +
│ │ │ ├── pattern_classifier.py +
│ │ │ └── result_aggregator.py +
│ │ ├── root_cause
│ │ │ ├── error_patterns.py +
│ │ │ ├── README.md
│ │ │ ├── recent_changes.py +
│ │ │ └── trace_execution.py +
│ │ ├── security
│ │ │ ├── rules
│ │ │ │ └── ...
│ │ │ ├── detect_secrets_analyzer.py +
│ │ │ └── semgrep_analyzer.py +
│ │ └── **init**.py +
│ ├── config
│ │ ├── coverage
│ │ │ ├── indicators.json
│ │ │ ├── languages.json
│ │ │ └── README.md
│ │ ├── formatters
│ │ │ ├── biome.json
│ │ │ └── ruff.toml
│ │ ├── patterns
│ │ │ ├── error
│ │ │ │ └── ...
│ │ │ ├── scalability
│ │ │ │ └── ...
│ │ │ └── README.md
│ │ ├── security
│ │ │ └── detect_secrets.json
│ │ └── tech_stacks
│ │ └── tech_stacks.json
│ ├── context
│ │ ├── context_bundle_capture_claude.py +
│ │ ├── context_bundle_capture_codex.py +
│ │ ├── context_capture_config.json
│ │ ├── context_capture_utils.py +
│ │ └── sensitive_data_redactor.py +
│ ├── core
│ │ ├── base
│ │ │ ├── **init**.py +
│ │ │ ├── analyzer_base.py +
│ │ │ ├── analyzer_registry.py +
│ │ │ ├── config_factory.py +
│ │ │ ├── error_handler.py +
│ │ │ ├── fs_utils.py +
│ │ │ ├── module_base.py +
│ │ │ ├── profiler_base.py +
│ │ │ ├── README.md
│ │ │ ├── registry_bootstrap.py +
│ │ │ ├── timing_utils.py +
│ │ │ └── vendor_detector.py +
│ │ ├── cli
│ │ │ └── run_analyzer.py +
│ │ ├── config
│ │ │ └── loader.py +
│ │ ├── utils
│ │ │ ├── **init**.py +
│ │ │ ├── analysis_environment.py +
│ │ │ ├── cross_platform.py +
│ │ │ ├── output_formatter.py +
│ │ │ ├── tech_stack_detector.py +
│ │ │ └── tooling.py +
│ │ └── **init**.py +
│ ├── generators
│ │ ├── ci
│ │ │ ├── convert_analyzers_to_codeclimate.py +
│ │ │ ├── security_findings_to_markdown.py +
│ │ │ ├── setup_code_quality_ci.py +
│ │ │ └── setup_security_analysis_ci.py +
│ │ ├── **init**.py +
│ │ ├── analysis_report.py +
│ │ ├── makefile.py +
│ │ └── procfile.py +
│ ├── integration
│ │ ├── cli
│ │ │ ├── **init**.py
│ │ │ ├── evaluate_root_cause.py +
│ │ │ ├── evaluate_security.py +
│ │ │ └── run_all_analyzers.py +
│ │ └── **init**.py
│ ├── setup
│ │ ├── monitoring
│ │ │ ├── install_monitoring_dependencies.py +
│ │ │ ├── update_agents_md.py +
│ │ │ └── update_claude_md.py +
│ │ ├── security
│ │ │ ├── **init**.py +
│ │ │ └── setup_package_monitoring.py +
│ │ ├── **init**.py
│ │ ├── install_dependencies.py +
│ │ ├── requirements.txt
│ │ └── test_install.py +
│ ├── tests
│ │ ├── fixture
│ │ │ └── test_codebase
│ │ │ └── ...
│ │ ├── integration
│ │ │ ├── fixtures
│ │ │ │ └── ...
│ │ │ ├── tools
│ │ │ │ └── ...
│ │ │ ├── **init**.py
│ │ │ ├── security_expected_findings.json
│ │ │ ├── test_integration_all_analyzers.py +
│ │ │ ├── test_integration_root_cause_cli.py +
│ │ │ ├── test_integration_security_cli.py +
│ │ │ └── test_quality_analyzer.py +
│ │ ├── unit
│ │ │ ├── **init**.py
│ │ │ ├── test_analyzer_registry.py +
│ │ │ ├── test_config_loader.py +
│ │ │ ├── test_context_bundle_capture_codex.py +
│ │ │ ├── test_context_capture_utils.py +
│ │ │ ├── test_coverage_analysis.py +
│ │ │ ├── test_detect_secrets_analyzer.py +
│ │ │ ├── test_duplicate_detection.py +
│ │ │ ├── test_error_patterns.py +
│ │ │ ├── test_pattern_classifier.py +
│ │ │ ├── test_registry_bootstrap.py +
│ │ │ ├── test_result_aggregator.py +
│ │ │ ├── test_scalability_check.py +
│ │ │ └── test_tech_stack_detector_core.py +
│ │ ├── utils
│ │ │ └── builders.py +
│ │ ├── **init**.py
│ │ ├── AGENTS.md
│ │ └── conftest.py +
│ ├── utils
│ │ ├── **init**.py
│ │ ├── clean_claude_config.py +
│ │ └── path_resolver.py +
│ ├── web_scraper
│ │ ├── **init**.py +
│ │ ├── cache_manager.py +
│ │ ├── cli.py +
│ │ ├── config.py +
│ │ ├── crawler.py +
│ │ ├── error_handler.py +
│ │ ├── scraper.py +
│ │ ├── session_manager.py +
│ │ └── utils.py +
│ ├── **init**.py +
│ └── conftest.py +
├── systems
│ ├── antigravity
│ │ └── rules
│ │ └── global.antigravity.rules.md _
│ ├── claude-code
│ │ ├── rules
│ │ │ └── global.claude.rules.md _
│ │ ├── agents
│ │ ├── commands
│ │ │ ├── codify-claude-history.md
│ │ │ └── get-recent-context.md
│ │ ├── settings.json
│ │ └── statusline-worktree
│ ├── codex
│ │ ├── rules
│ │ │ └── global.codex.rules.md _
│ │ ├── prompts
│ │ │ ├── analyze-repo-orchestrator.md
│ │ │ ├── codify-codex-history.md
│ │ │ ├── get-recent-context.md
│ │ │ └── todo-background.md
│ │ └── codex-init-helpers.md
│ ├── copilot
│ │ └── rules
│ │ └── global.copilot.rules.md _
│ ├── cursor
│ │ └── rules
│ │ └── global.cursor.rules.md _
│ ├── gemini
│ │ └── rules
│ │ └── global.gemini.rules.md _
│ └── AGENTS.md _
├── tools
│ ├── enaible
│ │ ├── src
│ │ │ └── enaible
│ │ │ ├── commands
│ │ │ │ ├── **init**.py _ +
│ │ │ │ ├── analyzers.py _ +
│ │ │ │ ├── install.py _ +
│ │ │ │ ├── prompts.py _ +
│ │ │ │ └── root.py _ +
│ │ │ ├── prompts
│ │ │ │ ├── adapters.py _ +
│ │ │ │ ├── catalog.py _ +
│ │ │ │ ├── lint.py _ +
│ │ │ │ ├── renderer.py _ +
│ │ │ │ └── utils.py _ +
│ │ │ ├── runtime
│ │ │ │ └── context.py _ +
│ │ │ ├── utils
│ │ │ │ └── paths.py _ +
│ │ │ ├── **main**.py _ +
│ │ │ ├── app.py _ +
│ │ │ ├── constants.py _ +
│ │ │ ├── ...
│ │ ├── tests
│ │ │ ├── eval
│ │ │ ├── test_prompt_utils.py _ +
│ │ │ ├── test*prompts_renderer.py * +
│ │ │ ├── conftest.py +
│ │ │ ├── test*analyzers_commands.py +
│ │ │ ├── test_cli_doctor.py +
│ │ │ ├── test_cli_smoke.py +
│ │ │ ├── test_install_command.py +
│ │ │ ├── test_paths_utils.py +
│ │ │ └── test_prompts_commands.py +
│ │ ├── scripts
│ │ │ └── bump_prompt_version.py +
│ │ ├── pyproject.toml *
│ │ └── uv.lock
│ ├── parallel
│ │ ├── src
│ │ │ └── parallel
│ │ │ ├── commands
│ │ │ │ ├── **init**.py _
│ │ │ │ ├── extract.py _ +
│ │ │ │ ├── findall.py _ +
│ │ │ │ ├── search.py _ +
│ │ │ │ ├── status.py _ +
│ │ │ │ └── task.py _ +
│ │ │ ├── **init**.py _ +
│ │ │ ├── **main**.py _ +
│ │ │ ├── app.py _ +
│ │ │ ├── client.py _ +
│ │ │ └── config.py _ +
│ │ ├── pyproject.toml _
│ │ └── uv.lock
│ └── eval
│ └── src
├── scripts
│ ├── install.ps1
│ ├── install.sh
│ ├── README.md
│ ├── reset-local-install.sh
│ └── run-ci-quality-gates.sh
├── todos
│ ├── execplan
│ │ ├── code-review.md
│ │ ├── context-gathering.md
│ │ ├── create-execplan.md
│ │ ├── execplan.md
│ │ └── PLANS.md
│ ├── linear-workflow
│ │ ├── docs
│ │ │ ├── concepts.md
│ │ │ ├── integration-testing.md
│ │ │ └── workflow.md
│ │ ├── in-progress-items
│ │ │ ├── linear-acceptance-criteria-writer.md
│ │ │ ├── linear-dependency-linker.md
│ │ │ ├── linear-estimation-engine.md
│ │ │ ├── linear-hashing.md
│ │ │ ├── linear-issue-decomposer.md
│ │ │ ├── linear-issue-search.md
│ │ │ ├── linear-issue-writer.md
│ │ │ ├── linear-objective-definition.md
│ │ │ ├── linear-plan.config.json
│ │ │ ├── linear-readiness.md
│ │ │ ├── plan-linear-new-format.md
│ │ │ └── plan-linear.md
│ │ ├── bugs.txt
│ │ ├── improvements.txt
│ │ └── plan-linear-report-2025-10-01T09-48-31Z.json
│ └── mypy-strict-migration.md
├── .coveragerc
├── .gitattributes
├── .gitignore
├── .pre-commit-config.yaml
├── .prettierrc
├── .python-version
├── AGENTS.md
├── CLAUDE.md
├── enaible.png
├── mypy.ini
├── pytest.ini
├── README.md
└── requirements-dev.txt

(\* denotes selected files)
(+ denotes code-map available)
Config: depth cap 3.
</file_map>
<file_contents>
File: /Users/adamjackson/LocalDev/enaible/docs/system/copilot/templates/prompt.md.j2

```j2
{%- macro copilot_variable_value(var) -%}
{%- if var.kind == 'positional' -%}
${input:{{ var.token.lstrip('@').lower().replace('_', '-') }}}
{%- elif var.kind in ('flag', 'named') -%}
${input:{{ (var.flag_name or var.token.lstrip('@')).lstrip('--').lower().replace('_', '-') }}}
{%- else -%}
{{ var.type_text if var.type_text else '<derived>' }}
{%- endif -%}
{%- endmacro -%}

{%- macro format_copilot_variables(variables) -%}
{%- set required = variables | selectattr('kind', 'equalto', 'positional') | list -%}
{%- set optional = [] -%}
{%- for var in variables -%}
  {%- if var.kind in ['flag', 'named'] -%}
    {%- set _ = optional.append(var) -%}
  {%- endif -%}
{%- endfor -%}
{%- set derived = variables | selectattr('kind', 'equalto', 'derived') | list -%}
{%- if variables -%}
## Variables
{% if required %}

### Required

{% for var in required | sort(attribute='positional_index') -%}
- {{ var.token }} = {{ copilot_variable_value(var) }}{% if var.description %} — {{ var.description }}{% endif %}

{% endfor -%}
{% endif -%}
{%- if optional %}

### Optional (derived from $ARGUMENTS)

{% for var in optional | sort(attribute='flag_name') -%}
- {{ var.token }} = {{ copilot_variable_value(var) }}{% if var.repeatable %} [repeatable]{% endif %}{% if var.description %} — {{ var.description }}{% endif %}

{% endfor -%}
{% endif -%}
{%- if derived %}

### Derived (internal)

{% for var in derived -%}
- {{ var.token }}{% if var.description %} — {{ var.description }}{% endif %}

{% endfor -%}
{%- endif -%}
{%- endif -%}
{%- endmacro -%}

{%- set body_parts = body.split('\n## Variables\n') -%}
{%- set body_before_vars = body_parts[0].rstrip() if body_parts | length > 0 else body -%}
{%- set body_after_vars = '' -%}
{%- if body_parts | length > 1 -%}
  {%- set remaining_lines = body_parts[1].split('\n') -%}
  {%- set found_next_section = namespace(value=False) -%}
  {%- set after_lines = [] -%}
  {%- for line in remaining_lines -%}
    {%- if found_next_section.value -%}
      {%- set _ = after_lines.append(line) -%}
    {%- elif line.startswith('## ') and not line.startswith('## Variables') -%}
      {%- set found_next_section.value = True -%}
      {%- set _ = after_lines.append(line) -%}
    {%- endif -%}
  {%- endfor -%}
  {%- set body_after_vars = after_lines | join('\n') -%}
{%- endif -%}
---
description: {{ frontmatter.get('description', title) }}
agent: agent
{% if frontmatter.get('tools') %}tools: {{ frontmatter.get('tools') | tojson }}
{% endif %}---

{{ body_before_vars }}

{% if variables %}
{{ format_copilot_variables(variables) }}
{% endif %}
{%- if body_after_vars %}

{{ body_after_vars.lstrip() }}
{%- endif %}

{{ managed_sentinel }}

```

File: /Users/adamjackson/LocalDev/enaible/shared/prompts/setup-parallel-ai.md

`````md
# Purpose

Install and configure the Parallel AI CLI tool for web intelligence operations including search, content extraction, research tasks, and entity discovery.

## Variables

### Required

- (none)

### Optional (derived from $ARGUMENTS)

- @AUTO = --auto — skip STOP confirmations (auto-approve checkpoints)

### Derived (internal)

- @TOOL_DIR = <path> — tools/parallel directory path
- @SCOPE = <user|project> — installation scope from user choice
- @SYSTEMS = <filename> — system instructions file (CLAUDE.md or AGENTS.md depending on target)
- @SYSTEMS_PATH = <path> — full path to systems file based on scope

## Instructions

- ALWAYS verify Python 3.12+ and uv are available before proceeding.
- NEVER modify shell configuration files (.zshrc, .bashrc, etc.) directly.
- Install the parallel CLI tool using uv sync in the tools/parallel directory.
- Document commands in @SYSTEMS.md for reference (project or user level).
- Validate the CLI can be invoked via uv run.
- Respect STOP confirmations unless @AUTO is provided.

## Workflow

1. Check prerequisites
   - Verify uv is available: `command -v uv`
   - Check Python version: `python3 --version` (or `python --version` on systems without a `python3` shim) — must be 3.12+
   - If prerequisites missing, exit with instructions to install them.
2. Check API key
   - Look for `PARALLEL_API_KEY` in environment: `echo $PARALLEL_API_KEY`
   - If not set, **STOP (skip when @AUTO):** "PARALLEL_API_KEY not set. Get your key from platform.parallel.ai and add to shell config. Continue anyway? (y/n)"
   - If user declines, exit with instructions to add API key.
3. Install package
   - Navigate to tools/parallel: `cd @TOOL_DIR`
   - Run uv sync to install dependencies: `uv sync`
   - If installation fails, provide troubleshooting steps.
4. Verify installation
   - Test CLI works: `uv run --directory @TOOL_DIR parallel --help`
   - Verify all subcommands are available (search, extract, task, findall, status, result)
   - **STOP (skip when @AUTO):** "Parallel AI CLI installed successfully. Continue to documentation? (y/n)"
5. Update @SYSTEMS.md
   - **STOP (skip when @AUTO):** "Document Parallel AI tools at project level (./@SYSTEMS.md) or user level ({{ system.user_scope_dir }}/@SYSTEMS.md)?"
   - Based on user choice, set @SYSTEMS_PATH:
     - Project: `./@SYSTEMS.md` (repo root)
     - User: `{{ system.user_scope_dir }}/@SYSTEMS.md`
   - Add or update Parallel AI documentation section at @SYSTEMS_PATH:

   ````md
   ### When you need web intelligence or research capabilities

   If `--search`, `--extract`, `--task`, or `--findall` is included in a user request, use the Parallel AI tools.

   **Requires:** `PARALLEL_API_KEY` environment variable (get from platform.parallel.ai)

   **Usage:** `uv run --directory tools/parallel parallel <command>`

   **Available Commands:**

   - `parallel search <objective>` — Web search with natural language
     - Options: `--query/-q` (repeatable), `--max-results N`, `--format json|markdown`

   - `parallel extract <url>` — Extract content from URLs to markdown
     - Options: `--objective "focus"`, `--full-content`, `--format json|markdown`

   - `parallel task <input>` — Create enrichment/research task (async)
     - Options: `--schema "output desc"`, `--processor base|core`
     - Returns: run_id (use `parallel result` to get output)

   - `parallel findall <objective>` — Discover entities matching criteria (async)
     - Options: `--entity type`, `--condition` (repeatable), `--limit N`, `--generator base|core|pro`
     - Returns: findall_id (use `parallel status` to track)

   - `parallel status <id>` — Check async operation status
   - `parallel result <id>` — Fetch completed results

   **Example Usage:**

   ```bash
   # Search the web
   uv run --directory tools/parallel parallel search "latest AI research papers on RAG"

   # Extract content from URL
   uv run --directory tools/parallel parallel extract https://example.com --objective "key findings"

   # Generate dataset of entities
   uv run --directory tools/parallel parallel findall "AI startups in San Francisco" --entity company --limit 50
   ```
   ````
`````

````

```

```

6. Test connectivity (optional)
- **STOP (skip when @AUTO):** "Test API connectivity with a simple search? (y/n)"
- If approved and PARALLEL_API_KEY is set, run a test search:
  `uv run --directory @TOOL_DIR parallel search "test query" --max-results 1`
- Verify response is received successfully.
7. Validate setup
- Confirm CLI is accessible via uv run
- Confirm all 6 commands are available
- Provide usage examples and next steps

## Output

```md
# RESULT

- Summary: Parallel AI CLI installed and configured

## DETAILS

- Tool Directory: @TOOL_DIR
- Python Version: <version>
- API Key Status: <set|not set - configure PARALLEL_API_KEY>
- Documentation: @SYSTEMS_PATH updated

## INSTALLED COMMANDS

- parallel search — Web search with natural language
- parallel extract — Extract content from URLs
- parallel task — Create enrichment/research tasks
- parallel findall — Discover entities at scale
- parallel status — Check async operation status
- parallel result — Fetch completed results

## VALIDATION

- uv sync: ✓ Dependencies installed
- parallel --help: ✓ CLI accessible
- API connectivity: <✓ verified | ⚠ PARALLEL_API_KEY not set>

## NEXT STEPS

1. Set PARALLEL_API_KEY if not already configured:
`export PARALLEL_API_KEY="your-key-here"`
2. Test with a search: `uv run --directory tools/parallel parallel search "test query"`
3. Review @SYSTEMS_PATH for command reference
```

```

File: /Users/adamjackson/LocalDev/enaible/tools/enaible/src/enaible/prompts/utils.py
```py
"""Utilities for parsing shared prompt metadata.

Supports the unified bullet-style Variables section using @TOKENS.

Format:

## Variables

### Required
- @TARGET_PATH = $1 — description

### Optional (derived from $ARGUMENTS)
- @MIN_SEVERITY = --min-severity
- @EXCLUDE = --exclude [repeatable]

### Derived (internal)
- @MAX_CHARS = 150000
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class VariableSpec:
 token: str
 type_text: str
 description: str
 kind: str
 required: bool
 flag_name: str | None = None
 positional_index: int | None = None
 repeatable: bool = False


_VARIABLE_HEADER_PATTERN = re.compile(
 r"^\|\s*Token(?:/Flag)?\s*\|\s*Type\s*\|\s*Description\s*\|$",
 re.IGNORECASE,
)

_H2_HEADING = re.compile(r"^##\s+variables\s*$", re.IGNORECASE)
_H3_REQUIRED = re.compile(r"^###\s+required\s*$", re.IGNORECASE)
_H3_OPTIONAL = re.compile(r"^###\s+optional(\s*\(.*\))?\s*$", re.IGNORECASE)
_H3_DERIVED = re.compile(r"^###\s+derived(\s*\(.*\))?\s*$", re.IGNORECASE)
_BULLET = re.compile(r"^[-*]\s+(.+?)\s*$")
_TOKEN_RE = re.compile(r"@([A-Z][A-Z0-9_]*)$")
_MAPPING_SPLIT = re.compile(r"\s*=\s*")
_POS_VALUE = re.compile(r"^\$(\d+)\s*(?:\[.*?\])?$")
_FLAG_VALUE = re.compile(r"^(--[a-z0-9][a-z0-9-]*)\s*(?:\[.*?\])?$", re.IGNORECASE)


def extract_variables(markdown: str) -> tuple[list[VariableSpec], str]:
 """Extract variable definitions from a markdown prompt body.

 Returns a tuple of (variables, body_without_variables_section).
 Prefers the bullet-style parser; tables are only supported when they use @TOKENS.
 """
 lines = markdown.splitlines()
 variables: list[VariableSpec] = []
 new_lines: list[str] = []

 i = 0
 while i < len(lines):
     if _H2_HEADING.match(lines[i]):
         block: list[str] = []
         while i < len(lines):
             block.append(lines[i])
             i += 1
             if i < len(lines) and lines[i].startswith("## "):
                 break

         formatted_block: list[str] | None = None
         parsed = _parse_variables_bullets(block[1:])
         if parsed:
             variables = parsed
             formatted_block = _format_variables_block(parsed)
         else:
             table_lines = [ln for ln in block if ln.strip().startswith("|")]
             if table_lines:
                 variables = _parse_variables_table(table_lines)
                 formatted_block = _format_variables_block(variables)

         if formatted_block:
             new_lines.extend(formatted_block)
         else:
             new_lines.extend(block)
         continue

     new_lines.append(lines[i])
     i += 1

 body = "\n".join(new_lines).strip("\n")
 return variables, body + "\n" if body else ""


def _format_variables_block(variables: list[VariableSpec]) -> list[str]:
 required = [var for var in variables if var.kind == "positional"]
 optional = [var for var in variables if var.kind in {"flag", "named"}]
 derived = [var for var in variables if var.kind == "derived"]

 lines: list[str] = ["## Variables", ""]

 if required:
     lines.append("### Required")
     lines.append("")
     for var in required:
         desc = f" — {var.description}" if var.description else ""
         lines.append(f"- {var.token} = ${var.positional_index}{desc}")
     lines.append("")

 if optional:
     lines.append("### Optional (derived from $ARGUMENTS)")
     lines.append("")
     for var in optional:
         repeatable = " [repeatable]" if var.repeatable else ""
         desc = f" — {var.description}" if var.description else ""
         lines.append(f"- {var.token} = {var.flag_name}{repeatable}{desc}")
     lines.append("")

 if derived:
     lines.append("### Derived (internal)")
     lines.append("")
     for var in derived:
         # For derived variables, omit the "= <value>" part
         detail = var.description or var.type_text.strip()
         suffix = f" — {detail}" if detail else ""
         lines.append(f"- {var.token}{suffix}")
     lines.append("")

 return lines


def _parse_variables_table(table_lines: Iterable[str]) -> list[VariableSpec]:
 """Parse legacy markdown table lines into VariableSpec entries.

 Only @TOKENS are allowed. $-prefixed tokens are rejected by design.
 """
 rows = [row.strip() for row in table_lines if row.strip()]
 if not rows:
     return []

 header = rows[0]
 if not _VARIABLE_HEADER_PATTERN.match(header):
     raise ValueError(
         "Variables table must have columns: Token | Type | Description"
     )

 # Skip header and alignment row if present
 start_idx = 1
 if start_idx < len(rows) and set(rows[start_idx].replace(" ", "")) <= {
     "|",
     ":",
     "-",
 }:
     start_idx += 1

 variables: list[VariableSpec] = []
 positional_counter = 0

 for row in rows[start_idx:]:
     cells = [cell.strip() for cell in row.split("|")][1:-1]
     if len(cells) != 3:
         continue
     token_cell, type_text, description = cells
     token_text = token_cell.strip()
     if token_text.startswith("`") and token_text.endswith("`"):
         token_text = token_text[1:-1].strip()
     if not token_text.startswith("@"):
         raise ValueError(
             f"Variable token must start with '@' in tables: {token_text}"
         )

     kind, required, positional_index, flag_name = _interpret_type_cell(
         type_text, positional_counter
     )
     if kind == "positional" and positional_index is None:
         positional_counter += 1
         positional_index = positional_counter
     elif kind == "positional" and positional_index is not None:
         positional_counter = positional_index

     variables.append(
         VariableSpec(
             token=token_text,
             type_text=type_text,
             description=description,
             kind=kind,
             required=required,
             flag_name=flag_name,
             positional_index=positional_index,
             repeatable="repeatable" in type_text.lower(),
         )
     )

 return variables


_POS_INDEX_RE = re.compile(r"#(\d+)")
_FLAG_RE = re.compile(r"--[a-z0-9][a-z0-9-]*", re.IGNORECASE)


def _interpret_type_cell(
 type_cell: str, current_positional_count: int
) -> tuple[str, bool, int | None, str | None]:
 text = type_cell.strip()
 lower = text.lower()

 required = "required" in lower
 optional = "optional" in lower
 if required and optional:
     required = not optional  # default to False if conflicting
 elif not required and not optional:
     required = False

 flag_name: str | None = None
 positional_index: int | None = None

 if lower.startswith("positional"):
     kind = "positional"
     match = _POS_INDEX_RE.search(lower)
     if match:
         positional_index = int(match.group(1))
 elif lower.startswith("flag"):
     kind = "flag"
     flag_match = _FLAG_RE.search(text)
     if flag_match:
         flag_name = flag_match.group(0)
 elif lower.startswith("named"):
     kind = "named"
     flag_match = _FLAG_RE.search(text)
     if flag_match:
         flag_name = flag_match.group(0)
 else:
     kind = "config"

 return kind, required, positional_index, flag_name


def _detect_section(line: str, current_section: str | None) -> str | None:
 """Detect which Variables section (required/optional/derived) a line represents."""
 if _H3_REQUIRED.match(line):
     return "required"
 if _H3_OPTIONAL.match(line):
     return "optional"
 if _H3_DERIVED.match(line):
     return "derived"
 return current_section


def _parse_variable_line(content: str) -> tuple[str, str | None, str]:
 """Parse a bullet line into token, value part, and description."""
 # Split description if provided using em dash or hyphen dash separation
 desc_split = re.split(r"\s+—\s+|\s+-\s+", content, maxsplit=1)
 mapping_part = desc_split[0].strip()
 description = desc_split[1].strip() if len(desc_split) > 1 else ""
 return mapping_part, description


def _extract_token_and_value(mapping_part: str, section: str) -> tuple[str, str | None]:
 """Extract token and value parts from mapping string."""
 parts = _MAPPING_SPLIT.split(mapping_part)
 if len(parts) == 1 and section == "derived":
     # Derived variable without explicit mapping: "@TOKEN — description"
     token_part = parts[0].strip()
     value_part = None
 elif len(parts) == 2:
     token_part, value_part = parts[0].strip(), parts[1].strip()
 else:
     return None, None
 return token_part, value_part


def _validate_token(token_part: str) -> str:
 """Validate and normalize token format."""
 tok_match = _TOKEN_RE.match(token_part)
 if not tok_match:
     raise ValueError(
         f"Invalid token '{token_part}'. Tokens must be @UPPER_SNAKE_CASE."
     )
 return f"@{tok_match.group(1)}"


def _validate_required_variable(
 token: str, value_part: str | None, positional_seen: set[int]
) -> tuple[int, str]:
 """Validate and extract positional index for required variables."""
 if not value_part:
     raise ValueError(f"Required variable '{token}' must have a mapping (e.g., $1).")
 pos_m = _POS_VALUE.match(value_part)
 if not pos_m:
     raise ValueError(f"Required variable '{token}' must map to $N (e.g., $1).")
 positional_index = int(pos_m.group(1))
 if positional_index in positional_seen:
     raise ValueError(f"Duplicate positional index ${positional_index} for {token}.")
 positional_seen.add(positional_index)
 type_text = f"positional ${positional_index} (REQUIRED)"
 return positional_index, type_text


def _validate_optional_variable(token: str, value_part: str | None) -> tuple[str, str]:
 """Validate and extract flag name for optional variables."""
 if not value_part:
     raise ValueError(
         f"Optional variable '{token}' must have a mapping (e.g., --flag)."
     )
 flag_m = _FLAG_VALUE.match(value_part)
 if not flag_m:
     raise ValueError(f"Optional variable '{token}' must map to a --flag.")
 flag_name = flag_m.group(1)
 return flag_name, "derived from @ARGUMENTS"


def _create_variable_spec(
 token: str,
 section: str,
 description: str,
 value_part: str | None,
 positional_seen: set[int],
) -> VariableSpec:
 """Create a VariableSpec from parsed components."""
 repeatable = "[repeatable]" in value_part.lower() if value_part else False

 if section == "required":
     positional_index, type_text = _validate_required_variable(
         token, value_part, positional_seen
     )
     return VariableSpec(
         token=token,
         type_text=type_text,
         description=description,
         kind="positional",
         required=True,
         flag_name=None,
         positional_index=positional_index,
         repeatable=repeatable,
     )

 if section == "optional":
     flag_name, base_type = _validate_optional_variable(token, value_part)
     repeatable_text = ", repeatable" if repeatable else ""
     type_text = f"{base_type} ({flag_name}) (optional{repeatable_text})"
     return VariableSpec(
         token=token,
         type_text=type_text,
         description=description,
         kind="flag",
         required=False,
         flag_name=flag_name,
         positional_index=None,
         repeatable=repeatable,
     )

 # derived internal
 return VariableSpec(
     token=token,
     type_text="derived (internal)",
     description=description,
     kind="derived",
     required=False,
     flag_name=None,
     positional_index=None,
     repeatable=repeatable,
 )


def _parse_variables_bullets(block_lines: Iterable[str]) -> list[VariableSpec]:
 """Parse Variables section from bullet-style markdown lines."""
 section: str | None = None
 variables: list[VariableSpec] = []
 positional_seen: set[int] = set()

 for raw in block_lines:
     line = raw.strip()
     if not line:
         continue

     # Detect section headers - if this line is a header, update section and skip
     detected = _detect_section(line, None)
     if detected is not None and detected != section:
         section = detected
         continue

     # Parse bullet lines
     m = _BULLET.match(line)
     if not m or section is None:
         continue

     content = m.group(1)

     # Skip placeholder indicating no variables in this section
     if content.strip() == "(none)":
         continue

     # Parse line components
     mapping_part, description = _parse_variable_line(content)
     token_part, value_part = _extract_token_and_value(mapping_part, section)

     # For required variables without mapping, raise error before skipping
     if token_part is None:
         # Check if this might be a required variable missing its mapping
         if section == "required":
             # Try to extract token from mapping_part directly
             tok_match = _TOKEN_RE.match(mapping_part.strip())
             if tok_match:
                 token = f"@{tok_match.group(1)}"
                 raise ValueError(
                     f"Required variable '{token}' must have a mapping (e.g., $1)."
                 )
         continue

     # Validate and normalize token
     token = _validate_token(token_part)

     # For required variables, value_part must be present
     if section == "required" and value_part is None:
         raise ValueError(
             f"Required variable '{token}' must have a mapping (e.g., $1)."
         )

     # Create variable spec
     spec = _create_variable_spec(
         token, section, description, value_part, positional_seen
     )
     variables.append(spec)

 return variables

```

File: /Users/adamjackson/LocalDev/enaible/tools/enaible/src/enaible/constants.py
```py
"""Shared constants for Enaible CLI."""

from __future__ import annotations

MANAGED_SENTINEL = "<!-- generated: enaible -->"

```

File: /Users/adamjackson/LocalDev/enaible/systems/AGENTS.md
```md
# System Adapter Playbook

Use this checklist whenever you add support for a brand-new target system (new IDE, agent runtime, etc.) so rendered prompts remain deterministic and installer sync stays safe.

1. **Scaffold folders**
- Mirror the existing adapter footprint by creating `docs/system/<system>/templates/` for Jinja templates plus system notes, and `systems/<system>/` for managed outputs.
- Rendered files land under `.build/rendered/<system>/...`; keep that structure parallel to claude-code/codex/cursor so tooling can diff reliably.
2. **Author templates**
- Base every template on `docs/system/templates/prompt.md` (Purpose, Variables, Instructions, Workflow, Output). Name templates `*.j2` (e.g., `docs/system/<system>/templates/prompt.md.j2`) and only include layout/frontmatter—not prompt copy.
- If the adapter produces multiple asset types (commands, workflows, rules), add separate `.j2` files sharing the same token names expected by shared prompts.
3. **Register in the prompt catalog**
- Update `tools/enaible/src/enaible/prompts/catalog.py` by appending a `SystemPromptConfig` entry for the new system inside each prompt definition you want exposed.
- Provide the template path, `.build/rendered/...` output path, and any required `frontmatter`/`metadata`. Keep catalog entries declarative—add new template tokens before wiring them in the registry.
4. **Hook into the installer**
- Edit `tools/enaible/src/enaible/commands/install.py` (e.g., `SYSTEM_RULES`, `ALWAYS_MANAGED_PREFIXES`) so `enaible install <system>` knows which files to sync and protect.
- Copy any additional bootstrap assets from `systems/<system>/` during install; avoid inline hacks or fallbacks.
5. **Run render + drift guards**
- Execute the standard guard trio:
  ```bash
  uv run --project tools/enaible enaible prompts lint
  uv run --project tools/enaible enaible prompts render --prompt all --system all
  uv run --project tools/enaible enaible prompts diff
  ```
- Confirm `.build/rendered/<system>/...` contains the new outputs and that `<!-- generated: enaible -->` is injected automatically.
6. **Validate installs**
- Smoke both scopes:
  ```bash
  uv run --project tools/enaible enaible install <system> --scope project --mode sync
  uv run --project tools/enaible enaible install <system> --scope user --mode sync
  ```
- Open a rendered prompt/command to verify frontmatter, variable bindings, and workflow steps survive intact. Capture analyzer dry runs under `.enaible/artifacts/<task>/<timestamp>/` when applicable.
7. **Document system quirks**
- If the adapter needs extra env setup or UX notes, add a short README snippet under `docs/system/<system>/` so future contributors inherit the constraints.
- Keep guidance aligned with repo-wide UI/guardrail conventions (shadcn/Tailwind/Radix/Lucide, no fallbacks, no legacy compatibility).

```

File: /Users/adamjackson/LocalDev/enaible/docs/system/cursor/templates/command.md.j2
```j2
{% if frontmatter %}---
{% for key, value in frontmatter.items() %}{{ key }}: {{ value }}
{% endfor %}---

{% endif %}
# {{ title }}

{{ body }}
{{ managed_sentinel }}

```

File: /Users/adamjackson/LocalDev/enaible/systems/cursor/rules/global.cursor.rules.md
```md
## **CRITICAL** Must follow Design Principles

- **ALWAYS** establish a working base project before beginging bespoke configuration and feature development, this means confirmed successful compile and run of the dev server with quality gates established - this is used as the baseline first commit.
- **ALWAYS** commit to git after the logical conclusion of task steps, use a frequent, atomic commit pattern to establish safe check points of known good implementation that can be reverted to if need.
- **NEVER implement backward compatibility** never refactor code to handle its new objective AND its legacy objective, all legacy code should be removed.
- **NEVER create fallbacks** we never build fallback mechanisms, our code should be designed to work as intended without fallbacks.
- **ALWAY KISS - Keep it simple stupid** only action what the user has requested and no more, never over engineer, if you dont have approval for expanding the scope of a task you must ask the user first.
- **ALWAYS minimise complexity** keep code Cyclomatic Complexity under 10
- **ALWAYS prefer established libraries over bespoke code** only produce bespoke code if no established library
- **ALWAYS use appropriate symbol naming when refactoring code**: When refactoring do not add prefixes/suffixes like "Refactored", "Updated", "New", or "V2" to symbol names to indicate changes.
- **ALWAYS Align UI style changes to shadcn/Tailwind/Radix patterns and Lucide assets**: For your UI stack implementation avoid bespoke classes and direct style hardcoding to objects.

## **CRITICAL** Must follow Behaviour Rules - how you carry out actions

### Security Requirements

- **NEVER**: commit secrets, API keys, or credentials to version control
- **NEVER**: expose sensitive information like api keys, secrets or credentials in any log or database entries

### Prohibit Reward Hacking

- **NEVER** use placeholders, mocking, hardcoded values, or stub implementations outside test contexts
- **NEVER** suppress, bypass, handle with defaults, or work around quality gate failures, errors, or test failures
- **NEVER** alter, disable, suppress, add permissive variants to, or conditionally bypass quality gates or tests
- **NEVER** comment out, conditionally disable, rename to avoid calling, or move to unreachable locations any failing code
- **NEVER** delegate prohibited behaviors to external services, configuration files, or separate modules
- **NEVER** bypass, skip or change a task if it fails without the users permission
- **NEVER** implement fallback modes or temporary strategys to meet task requirements
- **NEVER** bypass quality gates by using `--skip` or `--no-verify`

## **CRITICAL** Development workflow tools

If the user types --help list out bulleted list of all the available tools below, single line per tool with short description and how to invoke

### When you need to execute Long-Running Tasks

If `--tmux` is included in a users request or a request requires long runnning execution (like a dev server) or we want to defence against a bash task that may stall, you **must** use tmux.

- Run long-running services in named tmux sessions: `tmux new-session -d -s <name> '<command>'`
- Check existing: `tmux list-sessions`, Attach: `tmux attach -t <name>`, Logs: `tmux capture-pane -p -S -200 -t <name>`
- Wrap uncertain/long commands in tmux to prevent blocking
- Kill session: `tmux kill-session -t <name>`

```

File: /Users/adamjackson/LocalDev/enaible/tools/enaible/src/enaible/app.py
```py
"""Root Typer application for the Enaible CLI."""

from __future__ import annotations

import typer

app = typer.Typer(help="Unified CLI for AI-Assisted Workflows.")


@app.callback()
def main() -> None:
 """Configure top-level CLI callbacks if needed."""
 # Intentionally empty: subcommands are registered via modules.
 return None

```

File: /Users/adamjackson/LocalDev/enaible/tools/enaible/src/enaible/prompts/renderer.py
```py
"""Prompt rendering engine."""

from __future__ import annotations

import difflib
import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from ..constants import MANAGED_SENTINEL
from ..runtime.context import WorkspaceContext
from .adapters import SYSTEM_CONTEXTS, SystemRenderContext
from .catalog import CATALOG, PromptDefinition, SystemPromptConfig
from .utils import VariableSpec, extract_variables


@dataclass(frozen=True)
class RenderResult:
 prompt_id: str
 system: str
 content: str
 output_path: Path

 def write(self) -> None:
     self.output_path.parent.mkdir(parents=True, exist_ok=True)
     self.output_path.write_text(self.content)

 def diff(self) -> str:
     if not self.output_path.exists():
         return ""
     current = self.output_path.read_text().splitlines(keepends=True)
     updated = self.content.splitlines(keepends=True)
     diff_lines = list(
         difflib.unified_diff(
             current,
             updated,
             fromfile=str(self.output_path),
             tofile=f"{self.output_path} (generated)",
         )
     )
     return "".join(diff_lines)


class PromptRenderer:
 def __init__(self, context: WorkspaceContext):
     self.context = context
     self.env = Environment(
         loader=FileSystemLoader(str(context.repo_root)),
         autoescape=False,
         trim_blocks=True,
         lstrip_blocks=True,
         undefined=StrictUndefined,
     )

 def list_prompts(self) -> Sequence[PromptDefinition]:
     return list(CATALOG.values())

 def render(
     self,
     prompt_ids: Iterable[str],
     systems: Iterable[str],
     output_override: dict[str, Path | None] | None = None,
 ) -> list[RenderResult]:
     results: list[RenderResult] = []
     for prompt_id in prompt_ids:
         definition = self._get_prompt(prompt_id)
         for system in systems:
             try:
                 config = self._get_system_config(definition, system)
             except ValueError:
                 continue
             system_context = self._get_system_context(system)
             rendered_body = self._render_body(definition, system_context, config)
             variables, stripped_body = extract_variables(rendered_body)
             content = self._render_wrapper(
                 definition,
                 system_context,
                 config,
                 stripped_body,
                 variables,
             )
             output_path = self._resolve_output_path(config, system, output_override)
             results.append(
                 RenderResult(
                     prompt_id=prompt_id,
                     system=system,
                     content=self._ensure_trailing_newline(content),
                     output_path=output_path,
                 )
             )
     return results

 def _get_prompt(self, prompt_id: str) -> PromptDefinition:
     try:
         return CATALOG[prompt_id]
     except KeyError as exc:
         available = ", ".join(sorted(CATALOG.keys()))
         raise ValueError(
             f"Unknown prompt '{prompt_id}'. Available: {available}"
         ) from exc

 def _get_system_config(
     self, definition: PromptDefinition, system: str
 ) -> SystemPromptConfig:
     try:
         return definition.systems[system]
     except KeyError as exc:
         available = ", ".join(sorted(definition.systems.keys()))
         raise ValueError(
             f"Prompt '{definition.prompt_id}' does not support system '{system}'. Available: {available}"
         ) from exc

 def _get_system_context(self, system: str) -> SystemRenderContext:
     try:
         return SYSTEM_CONTEXTS[system]
     except KeyError as exc:
         available = ", ".join(sorted(SYSTEM_CONTEXTS.keys()))
         raise ValueError(
             f"Unknown system '{system}'. Available: {available}"
         ) from exc

 def _render_body(
     self,
     definition: PromptDefinition,
     system: SystemRenderContext,
     config: SystemPromptConfig,
 ) -> str:
     source_path = (self.context.repo_root / definition.source_path).resolve()
     template_path = source_path.relative_to(self.context.repo_root).as_posix()
     template = self.env.get_template(template_path)
     rendered = template.render(
         prompt=definition,
         system=system,
         metadata=config.metadata,
     )
     # Replace @SYSTEMS.md placeholder with system-specific file
     systems_file = "CLAUDE.md" if system.name == "claude-code" else "AGENTS.md"
     rendered = rendered.replace("@SYSTEMS.md", systems_file)
     return rendered

 def _render_wrapper(
     self,
     definition: PromptDefinition,
     system: SystemRenderContext,
     config: SystemPromptConfig,
     body: str,
     variables: list[VariableSpec],
 ) -> str:
     body_cleaned, _ = self._strip_legacy_title(body)

     template_path = (
         (self.context.repo_root / Path(config.template))
         .resolve()
         .relative_to(self.context.repo_root)
         .as_posix()
     )
     template = self.env.get_template(template_path)
     argument_hint = _argument_hint_from_variables(variables)
     frontmatter = dict(config.frontmatter)
     if argument_hint:
         frontmatter.setdefault("argument-hint", argument_hint)
     return template.render(
         title=definition.title,
         body=body_cleaned.strip() + "\n" if body_cleaned.strip() else "",
         prompt=definition,
         system=system,
         frontmatter=frontmatter,
         metadata=config.metadata,
         variables=variables,
         managed_sentinel=MANAGED_SENTINEL,
     )

 def _resolve_output_path(
     self,
     config: SystemPromptConfig,
     system: str,
     overrides: dict[str, Path | None] | None,
 ) -> Path:
     base = None
     if overrides is not None:
         base = overrides.get(system)
     if base is None:
         return self.context.repo_root / config.output_path
     relative = self._system_relative_output_path(config.output_path, system)
     return base / relative

 @staticmethod
 def _system_relative_output_path(path: Path, system: str) -> Path:
     # Try standard systems/<system>/ structure
     system_root = Path("systems") / system
     try:
         return path.relative_to(system_root)
     except ValueError:
         pass

     # Try .build/rendered/<system>/ structure (used by catalog)
     rendered_root = Path(".build") / "rendered" / system
     try:
         return path.relative_to(rendered_root)
     except ValueError:
         pass

     # Try generic systems/ prefix
     try:
         return path.relative_to(Path("systems"))
     except ValueError:
         return Path(path.name)

 _LEGACY_TITLE_RE = re.compile(r"^#\s+.+?\bv\d+(?:\.\d+)*\s*$", re.IGNORECASE)

 @classmethod
 def _strip_legacy_title(cls, body: str) -> tuple[str, bool]:
     lines = body.splitlines()
     idx = 0
     while idx < len(lines) and not lines[idx].strip():
         idx += 1

     removed = False
     if idx < len(lines) and cls._LEGACY_TITLE_RE.match(lines[idx].strip()):
         lines.pop(idx)
         removed = True
         while idx < len(lines) and not lines[idx].strip():
             lines.pop(idx)

     cleaned = "\n".join(lines).strip("\n")
     if cleaned:
         cleaned += "\n"
     return cleaned, removed

 @staticmethod
 def _ensure_trailing_newline(value: str) -> str:
     return value if value.endswith("\n") else f"{value}\n"


def _argument_hint_from_variables(variables: list[VariableSpec]) -> str:
 tokens: list[str] = []

 positional = [var for var in variables if var.kind == "positional"]
 positional.sort(key=lambda var: var.positional_index or 0)

 flags = [var for var in variables if var.kind in {"flag", "named"}]
 flags.sort(key=lambda var: (var.flag_name or var.token).lower())

 def _format_label(var: VariableSpec, base: str) -> str:
     label = base
     if not var.required:
         label = f"{label}?"
     return f"[{label}]"

 for var in positional:
     label = var.token.lstrip("$").lstrip("@").lower().replace("_", "-")
     tokens.append(_format_label(var, label))

 for var in flags:
     base = var.flag_name or var.token.lstrip("$").lstrip("@")
     base = base.lower()
     tokens.append(_format_label(var, base))

 return " ".join(tokens)

```

File: /Users/adamjackson/LocalDev/enaible/tools/enaible/tests/test_prompt_utils.py
```py
"""Tests for prompt utilities."""

from __future__ import annotations

import pytest
from enaible.prompts.utils import _parse_variables_bullets, extract_variables


def test_extract_variables_parses_table_and_strips_section() -> None:
 markdown = """Intro text

## Variables
| Token | Type | Description |
| ----- | ---- | ----------- |
| `@TARGET_PATH` | positional #1 (REQUIRED) | Path to analyze. |
| `@VERBOSE` | flag --verbose (OPTIONAL) | Enable verbose output. |

## Remaining
Body continues.
"""

 variables, body = extract_variables(markdown)

 assert [var.token for var in variables] == ["@TARGET_PATH", "@VERBOSE"]
 assert variables[0].kind == "positional"
 assert variables[0].required is True
 assert variables[0].positional_index == 1
 assert variables[1].kind == "flag"
 assert variables[1].flag_name == "--verbose"
 assert "## Variables" in body
 assert "### Required" in body
 assert "## Remaining" in body


def test_parse_variables_bullets_invalid_token() -> None:
 """Test that invalid tokens raise ValueError."""
 lines = [
     "### Required",
     "- @invalid-token = $1 — description",
 ]
 with pytest.raises(ValueError, match="Invalid token.*@UPPER_SNAKE_CASE"):
     _parse_variables_bullets(lines)


def test_parse_variables_bullets_duplicate_positional_index() -> None:
 """Test that duplicate positional indices raise ValueError."""
 lines = [
     "### Required",
     "- @FIRST = $1 — first",
     "- @SECOND = $1 — duplicate",
 ]
 with pytest.raises(ValueError, match="Duplicate positional index"):
     _parse_variables_bullets(lines)


def test_parse_variables_bullets_derived_only() -> None:
 """Test parsing derived-only variables without explicit mapping."""
 lines = [
     "### Derived (internal)",
     "- @MAX_CHARS — Maximum character count",
 ]
 variables = _parse_variables_bullets(lines)
 assert len(variables) == 1
 assert variables[0].token == "@MAX_CHARS"
 assert variables[0].kind == "derived"
 assert variables[0].description == "Maximum character count"
 assert variables[0].positional_index is None
 assert variables[0].flag_name is None


def test_parse_variables_bullets_repeatable_flag() -> None:
 """Test parsing repeatable optional flags."""
 lines = [
     "### Optional (derived from $ARGUMENTS)",
     "- @EXCLUDE = --exclude [repeatable] — Additional patterns to exclude",
 ]
 variables = _parse_variables_bullets(lines)
 assert len(variables) == 1
 assert variables[0].token == "@EXCLUDE"
 assert variables[0].kind == "flag"
 assert variables[0].flag_name == "--exclude"
 assert variables[0].repeatable is True


def test_parse_variables_bullets_malformed_required_missing_mapping() -> None:
 """Test that required variables without mapping raise ValueError."""
 lines = [
     "### Required",
     "- @TARGET_PATH — Missing mapping",
 ]
 with pytest.raises(ValueError, match="must have a mapping"):
     _parse_variables_bullets(lines)


def test_parse_variables_bullets_malformed_optional_invalid_flag() -> None:
 """Test that optional variables with invalid flags raise ValueError."""
 lines = [
     "### Optional (derived from $ARGUMENTS)",
     "- @VERBOSE = invalid-flag — Invalid flag format",
 ]
 with pytest.raises(ValueError, match="must map to a --flag"):
     _parse_variables_bullets(lines)


def test_parse_variables_bullets_skip_none_placeholder() -> None:
 """Test that (none) placeholders are skipped."""
 lines = [
     "### Required",
     "(none)",
     "### Optional (derived from $ARGUMENTS)",
     "- @VERBOSE = --verbose — Enable verbose output",
 ]
 variables = _parse_variables_bullets(lines)
 assert len(variables) == 1
 assert variables[0].token == "@VERBOSE"


def test_parse_variables_bullets_all_sections() -> None:
 """Test parsing all three sections (required, optional, derived)."""
 lines = [
     "### Required",
     "- @TARGET = $1 — Target path",
     "### Optional (derived from $ARGUMENTS)",
     "- @VERBOSE = --verbose — Enable verbose",
     "### Derived (internal)",
     "- @MAX_CHARS — Maximum characters",
 ]
 variables = _parse_variables_bullets(lines)
 assert len(variables) == 3
 assert variables[0].kind == "positional"
 assert variables[0].positional_index == 1
 assert variables[1].kind == "flag"
 assert variables[1].flag_name == "--verbose"
 assert variables[2].kind == "derived"

```

File: /Users/adamjackson/LocalDev/enaible/tools/enaible/src/enaible/commands/prompts.py
```py
"""Prompt command group for Enaible CLI."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from pathlib import Path, Path as _Path

import typer

from ..app import app
from ..prompts.catalog import PromptDefinition
from ..prompts.lint import lint_files
from ..prompts.renderer import PromptRenderer
from ..runtime.context import load_workspace

_prompts_app = typer.Typer(help="Render and validate managed prompts.")
app.add_typer(_prompts_app, name="prompts")


def _resolve_prompt_ids(
 catalog: dict[str, PromptDefinition], prompts: Sequence[str]
) -> list[str]:
 if not prompts or prompts == ["all"]:
     return list(catalog.keys())

 catalog_ids = set(catalog.keys())
 unknown = [prompt for prompt in prompts if prompt not in catalog_ids]
 if unknown:
     available = ", ".join(sorted(catalog_ids))
     raise typer.BadParameter(
         f"Unknown prompt(s): {', '.join(unknown)}. Available: {available}"
     )
 return list(prompts)


def _resolve_systems(
 catalog: dict[str, PromptDefinition],
 prompt_ids: Iterable[str],
 systems: Sequence[str],
) -> list[str]:
 if not systems or systems == ["all"]:
     supported: set[str] = set()
     for prompt_id in prompt_ids:
         definition = catalog[prompt_id]
         supported.update(definition.systems.keys())  # type: ignore[attr-defined]
     return sorted(supported)

 return list(systems)


def _build_overrides(
 selected_systems: list[str], out: Path | None
) -> dict[str, Path | None]:
 if out is None:
     return dict.fromkeys(selected_systems)

 overrides: dict[str, Path | None] = {}
 if len(selected_systems) == 1:
     overrides[selected_systems[0]] = out
     return overrides

 for system in selected_systems:
     overrides[system] = out / system
 return overrides


def _split_csv(value: str) -> list[str]:
 if not value or value.lower() == "all":
     return ["all"]
 return [item.strip() for item in value.split(",") if item.strip()]


@_prompts_app.command("list")
def prompts_list() -> None:
 """List prompts known to the catalog."""
 context = load_workspace()
 renderer = PromptRenderer(context)
 for definition in renderer.list_prompts():
     systems = ", ".join(sorted(definition.systems.keys()))
     typer.echo(f"{definition.prompt_id}: {definition.title} [{systems}]")


@_prompts_app.command("render")
def prompts_render(
 prompts: str = typer.Option(
     "all",
     "--prompt",
     help="Comma-separated prompt identifiers or 'all'.",
 ),
 systems: str = typer.Option(
     "all",
     "--system",
     help="Comma-separated system identifiers or 'all'.",
 ),
 out: Path | None = typer.Option(
     None,
     "--out",
     "-o",
     help="Optional override directory for rendered output.",
 ),
) -> None:
 """Render prompts for the selected systems."""
 context = load_workspace()
 renderer = PromptRenderer(context)
 catalog = {
     definition.prompt_id: definition for definition in renderer.list_prompts()
 }

 prompt_args = _split_csv(prompts)
 system_args = _split_csv(systems)

 selected_prompts = _resolve_prompt_ids(catalog, prompt_args)
 selected_systems = _resolve_systems(catalog, selected_prompts, system_args)
 overrides = _build_overrides(selected_systems, out)

 results = renderer.render(selected_prompts, selected_systems, overrides)

 for result in results:
     result.write()
     typer.echo(
         f"Rendered {result.prompt_id} for {result.system} → {result.output_path}"
     )


@_prompts_app.command("diff")
def prompts_diff(
 prompts: str = typer.Option("all", "--prompt"),
 systems: str = typer.Option("all", "--system"),
) -> None:
 """Show diffs between catalog output and current files."""
 context = load_workspace()
 renderer = PromptRenderer(context)
 catalog = {
     definition.prompt_id: definition for definition in renderer.list_prompts()
 }

 prompt_args = _split_csv(prompts)
 system_args = _split_csv(systems)

 selected_prompts = _resolve_prompt_ids(catalog, prompt_args)
 selected_systems = _resolve_systems(catalog, selected_prompts, system_args)

 results = renderer.render(selected_prompts, selected_systems)

 has_diff = False
 for result in results:
     diff_output = result.diff()
     if diff_output:
         has_diff = True
         typer.echo(diff_output)

 if has_diff:
     raise typer.Exit(code=1)


@_prompts_app.command("validate")
def prompts_validate(
 prompts: str = typer.Option("all", "--prompt"),
 systems: str = typer.Option("all", "--system"),
) -> None:
 """Validate that rendered prompts match committed files."""
 try:
     prompts_diff(prompts=prompts, systems=systems)
 except typer.Exit as exc:
     if exc.exit_code != 0:
         typer.echo("Prompt drift detected. Run `enaible prompts render` to update.")
     raise


@_prompts_app.command("lint")
def prompts_lint(
 prompts: str = typer.Option("all", "--prompt"),
) -> None:
 """Lint prompt sources for @TOKEN usage and variable mapping rules."""
 context = load_workspace()
 renderer = PromptRenderer(context)
 catalog = {
     definition.prompt_id: definition for definition in renderer.list_prompts()
 }

 selected_prompts = _resolve_prompt_ids(catalog, _split_csv(prompts))
 # Collect unique source files for selected prompts
 files = {
     (context.repo_root / catalog[p].source_path).resolve() for p in selected_prompts
 }

 # Also lint unmanaged, hand-authored system prompts in systems/*
 GENERATED_SENTINEL = "<!-- generated: enaible -->"
 system_dirs = [
     context.repo_root / _Path("systems/claude-code/commands"),
     context.repo_root / _Path("systems/codex/prompts"),
     context.repo_root / _Path("systems/copilot/prompts"),
     context.repo_root / _Path("systems/cursor/rules"),
 ]
 for d in system_dirs:
     if not d.exists():
         continue
     for p in d.glob("*.md"):
         if p.name.lower() == "agents.md":
             # Skip helper docs meant for the LLM, not renderable prompts
             continue
         try:
             head = p.read_text().splitlines()[:3]
         except Exception:
             continue
         if any(GENERATED_SENTINEL in line for line in head):
             # Managed, rendered file — skip
             continue
         files.add(p.resolve())

 issues = lint_files(files)
 if not issues:
     typer.echo("prompts: lint passed")
     return
 for issue in issues:
     typer.echo(f"{issue.path}:{issue.line}: {issue.message}")
 raise typer.Exit(code=1)

```

File: /Users/adamjackson/LocalDev/enaible/tools/enaible/pyproject.toml
```toml
[project]
name = "enaible"
version = "0.1.1"
description = "Unified CLI for AI-Assisted Workflows"
requires-python = ">=3.12,<3.13"
dependencies = [
 "typer>=0.18,<0.19",
 "jinja2>=3.1,<4.0",
]

[dependency-groups]
dev = [
 "pytest>=8.3,<9.0",
 "pytest-cov>=5.0,<6.0",
 "mypy>=1.11,<2.0",
 "ruff>=0.5,<0.6",
 "types-Jinja2>=2.11.9",
]

[project.scripts]
enaible = "enaible.__main__:app"

[tool.uv]
package = true

[tool.ruff]
target-version = "py311"
line-length = 100

```

File: /Users/adamjackson/LocalDev/enaible/docs/system/claude-code/templates/command.md.j2
```j2
{% if frontmatter %}---
{% for key, value in frontmatter.items() %}{{ key }}: {{ value }}
{% endfor %}---

{% endif %}
# {{ title }}

{{ body }}
{{ managed_sentinel }}

```

File: /Users/adamjackson/LocalDev/enaible/systems/antigravity/rules/global.antigravity.rules.md
```md
## **CRITICAL** Must follow Design Principles

- **ALWAYS** establish a working base project before beginging bespoke configuration and feature development, this means confirmed successful compile and run of the dev server with quality gates established - this is used as the baseline first commit.
- **ALWAYS** commit to git after the logical conclusion of task steps, use a frequent, atomic commit pattern to establish safe check points of known good implementation that can be reverted to if need.
- **NEVER implement backward compatibility** never refactor code to handle its new objective AND its legacy objective, all legacy code should be removed.
- **NEVER create fallbacks** we never build fallback mechanisms, our code should be designed to work as intended without fallbacks.
- **ALWAY KISS - Keep it simple stupid** only action what the user has requested and no more, never over engineer, if you dont have approval for expanding the scope of a task you must ask the user first.
- **ALWAYS minimise complexity** keep code Cyclomatic Complexity under 10
- **ALWAYS prefer established libraries over bespoke code** only produce bespoke code if no established library
- **ALWAYS use appropriate symbol naming when refactoring code**: When refactoring do not add prefixes/suffixes like "Refactored", "Updated", "New", or "V2" to symbol names to indicate changes.
- **ALWAYS Align UI style changes to shadcn/Tailwind/Radix patterns and Lucide assets**: For your UI stack implementation avoid bespoke classes and direct style hardcoding to objects.

## **CRITICAL** Must follow Behaviour Rules - how you carry out actions

### Security Requirements

- **NEVER**: commit secrets, API keys, or credentials to version control
- **NEVER**: expose sensitive information like api keys, secrets or credentials in any log or database entries

### Prohibit Reward Hacking

- **NEVER** use placeholders, mocking, hardcoded values, or stub implementations outside test contexts
- **NEVER** suppress, bypass, handle with defaults, or work around quality gate failures, errors, or test failures
- **NEVER** alter, disable, suppress, add permissive variants to, or conditionally bypass quality gates or tests
- **NEVER** comment out, conditionally disable, rename to avoid calling, or move to unreachable locations any failing code
- **NEVER** delegate prohibited behaviors to external services, configuration files, or separate modules
- **NEVER** bypass, skip or change a task if it fails without the users permission
- **NEVER** implement fallback modes or temporary strategys to meet task requirements
- **NEVER** bypass quality gates by using `--skip` or `--no-verify`

## **CRITICAL** Development workflow tools

If the user types --help list out bulleted list of all the available tools below, single line per tool with short description and how to invoke

### When you need to execute Long-Running Tasks

If `--tmux` is included in a users request or a request requires long runnning execution (like a dev server) or we want to defence against a bash task that may stall, you **must** use tmux.

- Run long-running services in named tmux sessions: `tmux new-session -d -s <name> '<command>'`
- Check existing: `tmux list-sessions`, Attach: `tmux attach -t <name>`, Logs: `tmux capture-pane -p -S -200 -t <name>`
- Wrap uncertain/long commands in tmux to prevent blocking
- Kill session: `tmux kill-session -t <name>`

```

File: /Users/adamjackson/LocalDev/enaible/shared/prompts/AGENTS.md
```md
# Shared Prompt Authoring Guide

1. Author the source prompt in `shared/prompts/<name>.md`. Edit `docs/system/<system>/templates/` only when you need new frontmatter/layout tokens, it forms the layout for to use for the target system.

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

Then exercise any analyzer calls via `enaible analyzers run ...` and keep artifacts under `.enaible/artifacts/<task>/<timestamp>/`.

4. Tests: add or update deterministic prompt fixtures in `shared/tests` when outputs are stable; otherwise rely on the drift checks above.

## Implementing a new shared prompt (end-to-end)

1. Establish the layout
- Start from `docs/system/templates/prompt.md` to replicate, exactly, the shared prompt structure (Purpose → Variables → Instructions → Workflow → Output). Keep wording system-neutral so renderers can add frontmatter later.
- For each target adapter, inspect the existing Jinja template under `docs/system/<system>/templates/*.j2` (for example `docs/system/codex/templates/prompt.md.j2`). If no suitable template exists, add one by copying the base prompt template guidance above and keeping token names aligned with the shared prompt variables.
2. Draft the shared prompt
- Create `shared/prompts/<name>.md` matching the template outline. Declare every `@TOKEN` under `## Variables`, documenting positional/flag bindings (`@TOKEN = $N` or `@TOKEN = --flag`).
- Avoid system-specific language or fallbacks; the rendered artifacts inherit system metadata from their adapter templates.
3. Map the prompt in the registry
- Register the new prompt ID in `tools/enaible/src/enaible/prompts/catalog.py`. Reference the shared source path and list each target system with its `template`, `output_path`, and required `frontmatter`/`metadata`.
- Reuse an existing `SystemPromptConfig` when possible; if the system needs new arguments or layout tokens, update its template folder first so the registry entry stays declarative.
4. Run render + drift guards
- Execute the lint/render/diff trio listed above to regenerate `.build/rendered/<system>/...` outputs and catch token or layout issues early.
5. Validate adapters
- Reinstall each affected system via `uv run --project tools/enaible enaible install <system> --mode sync --scope project` to confirm the prompt lands under the managed path with `<!-- generated: enaible -->` injected.
- Exercise downstream workflows (e.g., `enaible analyzers run ...`) using the new prompt, capturing artifacts under `.enaible/artifacts/...` when needed.

## Format conventions (required)

- System-agnostic source: keep wording neutral; system wrappers add frontmatter during render.
- Variables section: use the standard bullet layout under `## Variables` with `### Required / ### Optional (derived from $ARGUMENTS) / ### Derived (internal)` and `@TOKEN = $N` / `@TOKEN = --flag` mappings. No `$` tokens elsewhere in the body.
- Token usage: all placeholders are `@TOKEN` and must be declared in Variables; lint enforces this.
- Managed sentinel: don’t add it manually—the renderer injects `<!-- generated: enaible -->` into system outputs.
- Use the exact template and pattern to mirror can be found here `docs/system/templates/prompt.md`.

```

File: /Users/adamjackson/LocalDev/enaible/tools/parallel/src/parallel/__init__.py
```py
"""
Parallel AI CLI for web intelligence operations.

Provides command-line access to Parallel AI's Search, Extract, Task, and FindAll APIs.
"""

__version__ = "0.1.0"

```

File: /Users/adamjackson/LocalDev/enaible/docs/system/codex/templates/prompt.md.j2
```j2
# {{ title }}

{{ body }}

{{ managed_sentinel }}

```

File: /Users/adamjackson/LocalDev/enaible/tools/parallel/src/parallel/client.py
```py
"""HTTP client for Parallel AI API."""

from __future__ import annotations

from typing import Any

import httpx

from .config import API_BASE, BETA_HEADER, get_api_key


def api_request(
 method: str,
 endpoint: str,
 json: dict[str, Any] | None = None,
 use_beta: bool = True,
) -> dict[str, Any]:
 """Make authenticated API request to Parallel AI.

 Args:
     method: HTTP method (GET, POST, etc.)
     endpoint: API endpoint path (e.g., "/v1beta/search")
     json: Optional JSON body for POST requests
     use_beta: Whether to include the beta header

 Returns
 -------
     JSON response from the API.

 Raises
 ------
     httpx.HTTPStatusError: If the request fails.
 """
 headers: dict[str, str] = {
     "x-api-key": get_api_key(),
     "Content-Type": "application/json",
 }
 if use_beta:
     headers["parallel-beta"] = BETA_HEADER

 with httpx.Client(timeout=60.0) as client:
     response = client.request(
         method,
         f"{API_BASE}{endpoint}",
         headers=headers,
         json=json,
     )
     response.raise_for_status()
     return response.json()  # type: ignore[no-any-return]

```

File: /Users/adamjackson/LocalDev/enaible/systems/gemini/rules/global.gemini.rules.md
```md
## **CRITICAL** Must follow Design Principles

- **ALWAYS** establish a working base project before beginging bespoke configuration and feature development, this means confirmed successful compile and run of the dev server with quality gates established - this is used as the baseline first commit.
- **ALWAYS** commit to git after the logical conclusion of task steps, use a frequent, atomic commit pattern to establish safe check points of known good implementation that can be reverted to if need.
- **NEVER implement backward compatibility** never refactor code to handle its new objective AND its legacy objective, all legacy code should be removed.
- **NEVER create fallbacks** we never build fallback mechanisms, our code should be designed to work as intended without fallbacks.
- **ALWAY KISS - Keep it simple stupid** only action what the user has requested and no more, never over engineer, if you dont have approval for expanding the scope of a task you must ask the user first.
- **ALWAYS minimise complexity** keep code Cyclomatic Complexity under 10
- **ALWAYS prefer established libraries over bespoke code** only produce bespoke code if no established library
- **ALWAYS use appropriate symbol naming when refactoring code**: When refactoring do not add prefixes/suffixes like "Refactored", "Updated", "New", or "V2" to symbol names to indicate changes.
- **ALWAYS Align UI style changes to shadcn/Tailwind/Radix patterns and Lucide assets**: For your UI stack implementation avoid bespoke classes and direct style hardcoding to objects.

## **CRITICAL** Must follow Behaviour Rules - how you carry out actions

### Security Requirements

- **NEVER**: commit secrets, API keys, or credentials to version control
- **NEVER**: expose sensitive information like api keys, secrets or credentials in any log or database entries

### Prohibit Reward Hacking

- **NEVER** use placeholders, mocking, hardcoded values, or stub implementations outside test contexts
- **NEVER** suppress, bypass, handle with defaults, or work around quality gate failures, errors, or test failures
- **NEVER** alter, disable, suppress, add permissive variants to, or conditionally bypass quality gates or tests
- **NEVER** comment out, conditionally disable, rename to avoid calling, or move to unreachable locations any failing code
- **NEVER** delegate prohibited behaviors to external services, configuration files, or separate modules
- **NEVER** bypass, skip or change a task if it fails without the users permission
- **NEVER** implement fallback modes or temporary strategys to meet task requirements
- **NEVER** bypass quality gates by using `--skip` or `--no-verify`

## **CRITICAL** Development workflow tools

If the user types --help list out bulleted list of all the available tools below, single line per tool with short description and how to invoke

### When you need to execute Long-Running Tasks

If `--tmux` is included in a users request or a request requires long runnning execution (like a dev server) or we want to defence against a bash task that may stall, you **must** use tmux.

- Run long-running services in named tmux sessions: `tmux new-session -d -s <name> '<command>'`
- Check existing: `tmux list-sessions`, Attach: `tmux attach -t <name>`, Logs: `tmux capture-pane -p -S -200 -t <name>`
- Wrap uncertain/long commands in tmux to prevent blocking
- Kill session: `tmux kill-session -t <name>`

```

File: /Users/adamjackson/LocalDev/enaible/shared/prompts/create-rule.md
```md
# Purpose

Add a single, concise rule to the appropriate global rules file based on a user request and online best practice research.

## Variables

### Required

- @REQUEST = $1 — User's question or topic for the rule (e.g., "how should I handle async errors?")

### Optional (derived from $ARGUMENTS)

- @SCOPE = --scope — `user` or `project` (default: infer from request context)
- @OUT = --out — Custom target file path (overrides system default)
- @AUTO = --auto — Skip STOP confirmations (auto-approve checkpoints)

### Derived (internal)

- @SYSTEM = <detected> — The AI system running this prompt (claude-code, copilot, cursor, codex)
- @TARGET_FILE = <resolved> — Final target file path based on system, scope, and @OUT

## Instructions

- Search online for authoritative best practices before generating the rule.
- Rules must be concise (single line where possible) with clear true/false framing.
- For conceptual rules, include a minimal code example demonstrating the correct pattern.
- Check existing rules in the target file to avoid duplicates and ensure contextual fit.
- Present the rule for user approval before appending—NEVER add without confirmation.
- If the target file doesn't exist, warn the user and suggest creating it (don't auto-create).

## Workflow

1. Analyze request
- Understand what the user wants to codify as a rule.
- Identify the technology/framework context if applicable.
2. Search online for best practices
- Prioritize: official documentation → style guides → authoritative blogs.
- Note the source for citation.
3. Detect system and determine target
- Identify which AI system is running this prompt.
- Determine scope (user vs project) based on request nature:
  - User-level: personal preferences, global patterns
  - Project-level: project-specific conventions, tech stack rules
- Resolve target file:
  - If @OUT provided, use that path.
  - Otherwise use system default:
    - Claude Code: `~/.claude/CLAUDE.md` (user) or `./CLAUDE.md` (project)
    - Copilot: `.github/copilot-instructions.md` (project only)
    - Cursor: `.cursorrules` (project only)
    - Codex: `./AGENTS.md` (project only)
4. Check target file
- If file doesn't exist: STOP, warn user, suggest creating it.
- Read existing rules to understand context and avoid duplicates.
5. Generate rule
- Format based on rule type:
  - **Syntax/value rules** (true/false framing): Single line with ALWAYS/NEVER
  - **Concept rules**: Single line + minimal code example
- Use imperative language: "ALWAYS", "NEVER", "MUST", "PREFER"
6. Present for approval
- Show the generated rule.
- Show the target file and location within it.
- Show the source reference.
- STOP for user confirmation unless @AUTO is provided.
7. Append rule
- Add to the appropriate section of the target file.
- Preserve existing formatting and structure.

## Rule Format Examples

**Syntax/value rule (true/false framing):**

```
- **ALWAYS** use `const` for variables that are never reassigned, `let` only when reassignment is required
- **NEVER** use `any` type in TypeScript; prefer `unknown` for truly unknown types
```

**Concept rule (with code example):**

```text
- **ALWAYS** handle async errors with try/catch at the boundary:
async function fetchData() {
 try { return await api.get(); }
 catch (e) { logger.error(e); throw new AppError('fetch failed', e); }
}
```

## Output

```md
# RESULT

- Summary: Rule added to <@TARGET_FILE>.
- Rule: <the concise rule text>
- Source: <reference URL or documentation>
- Scope: <user|project>
- System: <@SYSTEM>
```

```

File: /Users/adamjackson/LocalDev/enaible/docs/system/codex/templates/prompt.md
```md
<!-- template format for codex prompts -->
<!-- Docs: https://github.com/openai/codex/blob/main/docs/prompts.md -->

<!--
Codex specific items
Rules:
 User level ~/.codex/AGENTS.md
 Project level ./AGENTS.md
Directories:
 User level ~/.codex
 Project level ./.codex
Settings:
 User level  ~/.codex/config.toml
 Project level ./.codex/config.toml
Mcp config:
 User level ~/.codex/config.toml

ARGUMENTS (expansion rules):
$1..$9: expand to first nine positional args
$ARGUMENTS: expands to all args joined by a single space
$$: preserved literally (emit a dollar sign)
quoted: wrap an argument in double quotes to include spaces
-->

<prompt-body>

```

File: /Users/adamjackson/LocalDev/enaible/tools/parallel/src/parallel/config.py
```py
"""Configuration and API key management for Parallel AI."""

from __future__ import annotations

import os
import sys

API_BASE = "https://api.parallel.ai"
BETA_HEADER = "search-extract-2025-10-10"


def get_api_key() -> str:
 """Get API key from environment.

 Returns
 -------
     The PARALLEL_API_KEY value.

 Raises
 ------
     SystemExit: If the API key is not set.
 """
 key = os.environ.get("PARALLEL_API_KEY")
 if not key:
     print(
         "Error: PARALLEL_API_KEY not set.\n"
         "Get your key from https://platform.parallel.ai",
         file=sys.stderr,
     )
     sys.exit(1)
 return key

```

File: /Users/adamjackson/LocalDev/enaible/systems/claude-code/rules/global.claude.rules.md
```md
## **CRITICAL** Must follow Design Principles

- **ALWAYS** use an atomic commit pattern to establish safe reversion points.
- **NEVER implement backward compatibility** never refactor code to handle its new objective AND its legacy objective.
- **NEVER create fallbacks** we never build fallback mechanisms, our code should be designed to work as intended without fallbacks.
- **ALWAYS minimise complexity** keep code Cyclomatic Complexity under 10
- **ALWAYS use appropriate symbol naming when refactoring code**: When refactoring do not add prefixes/suffixes like "Refactored", "Updated", "New", or "V2" to symbol names to indicate changes.
- **ALWAYS Align UI style changes to shadcn/Tailwind/Radix patterns and Lucide assets**: For your UI stack implementation avoid bespoke classes and direct style hardcoding to objects.

## **CRITICAL** Must follow Behaviour Rules - how you carry out actions

### Security Requirements

- **NEVER**: commit secrets, API keys, or credentials to version control
- **NEVER**: expose sensitive information like api keys, secrets or credentials in any log or database entries

### Prohibit Reward Hacking

- **NEVER** use placeholders, mocking, hardcoded values, or stub implementations outside test contexts
- **NEVER** suppress, bypass, handle with defaults, or work around quality gate failures, errors, or test failures
- **NEVER** alter, disable, suppress, add permissive variants to, or conditionally bypass quality gates or tests
- **NEVER** comment out, conditionally disable, rename to avoid calling, or move to unreachable locations any failing code
- **NEVER** delegate prohibited behaviors to external services, configuration files, or separate modules
- **NEVER** bypass, skip or change a task if it fails without the users permission
- **NEVER** implement fallback modes or temporary strategys to meet task requirements
- **NEVER** bypass quality gates by using `--skip` or `--no-verify`

## **CRITICAL** Development workflow tools

If the user types --help list out bulleted list of all the available tools below, single line per tool with short description and how to invoke

### When you need to execute Long-Running Tasks

If `--tmux` is included in a users request or a request requires long runnning execution (like a dev server) or we want to defence against a bash task that may stall, you **must** use tmux.

- Run long-running services in named tmux sessions: `tmux new-session -d -s <name> '<command>'`
- Check existing: `tmux list-sessions`, Attach: `tmux attach -t <name>`, Logs: `tmux capture-pane -p -S -200 -t <name>`
- Wrap uncertain/long commands in tmux to prevent blocking
- Kill session: `tmux kill-session -t <name>`

```

File: /Users/adamjackson/LocalDev/enaible/tools/parallel/src/parallel/commands/task.py
```py
"""Task command for Parallel AI."""

from __future__ import annotations

from typing import Annotated

import typer

from parallel.app import app
from parallel.client import api_request


@app.command()
def task(
 input_data: Annotated[
     str, typer.Argument(help="Input data to enrich or research query")
 ],
 schema: Annotated[
     str | None,
     typer.Option("--schema", "-s", help="Output schema description"),
 ] = None,
 processor: Annotated[
     str,
     typer.Option("--processor", "-p", help="Processor type: base or core"),
 ] = "base",
) -> None:
 """Create an enrichment or research task (async).

 Returns a run_id immediately. Use 'parallel status <run_id>' to check progress
 and 'parallel result <run_id>' to fetch completed results.

 Examples
 --------
     parallel task "United Nations" --schema "founding date in MM-YYYY format"
     parallel task "OpenAI" --schema "funding rounds, valuation, key investors" --processor core
 """
 if processor not in ("base", "core"):
     print(f"Error: Invalid processor '{processor}'. Use 'base' or 'core'.")
     raise typer.Exit(1)

 payload: dict = {
     "input": input_data,
     "processor": processor,
     "task_spec": {},
 }
 if schema:
     payload["task_spec"]["output_schema"] = schema

 try:
     result = api_request("POST", "/v1/tasks/runs", json=payload, use_beta=False)

     run_id = result.get("run_id", "unknown")
     status = result.get("status", "unknown")

     print("Task created successfully!")
     print(f"  Run ID: {run_id}")
     print(f"  Status: {status}")
     print(f"\nCheck progress: parallel status {run_id}")
     print(f"Get results:    parallel result {run_id}")

 except Exception as e:
     print(f"Error: {e}", file=typer.get_text_stream("stderr"))
     raise typer.Exit(1) from None

```

File: /Users/adamjackson/LocalDev/enaible/tools/parallel/src/parallel/commands/findall.py
```py
"""FindAll command for Parallel AI."""

from __future__ import annotations

from typing import Annotated

import typer

from parallel.app import app
from parallel.client import api_request


@app.command()
def findall(
 objective: Annotated[
     str, typer.Argument(help="Natural language discovery objective")
 ],
 entity: Annotated[
     str,
     typer.Option(
         "--entity", "-e", help="Entity type (e.g., company, person, product)"
     ),
 ],
 condition: Annotated[
     list[str] | None,
     typer.Option("--condition", "-c", help="Match conditions (repeatable)"),
 ] = None,
 limit: Annotated[
     int,
     typer.Option("--limit", "-l", help="Maximum matches (5-1000)"),
 ] = 100,
 generator: Annotated[
     str,
     typer.Option("--generator", "-g", help="Generator tier: base, core, or pro"),
 ] = "base",
) -> None:
 """Discover entities matching criteria (async).

 Returns a findall_id immediately. Use 'parallel status <findall_id>' to check
 progress and 'parallel result <findall_id>' to fetch matched entities.

 Examples
 --------
     parallel findall "AI startups in SF" --entity company --limit 50
     parallel findall "ML researchers" --entity person -c "works at university" -c "published papers"
 """
 if generator not in ("base", "core", "pro"):
     print(f"Error: Invalid generator '{generator}'. Use 'base', 'core', or 'pro'.")
     raise typer.Exit(1)

 if not 5 <= limit <= 1000:
     print(f"Error: Limit must be between 5 and 1000, got {limit}.")
     raise typer.Exit(1)

 # Build match conditions from the condition flags
 match_conditions = []
 if condition:
     for i, cond in enumerate(condition, 1):
         match_conditions.append(
             {
                 "name": f"condition_{i}",
                 "description": cond,
             }
         )
 else:
     # Default condition derived from objective
     match_conditions.append(
         {
             "name": "primary_criteria",
             "description": objective,
         }
     )

 payload = {
     "objective": objective,
     "entity_type": entity,
     "match_conditions": match_conditions,
     "generator": generator,
     "match_limit": limit,
 }

 try:
     result = api_request("POST", "/v1beta/findall/runs", json=payload)

     findall_id = result.get("findall_id", "unknown")
     status_info = result.get("status", {})
     status = (
         status_info.get("status", "unknown")
         if isinstance(status_info, dict)
         else "unknown"
     )

     print("FindAll task created successfully!")
     print(f"  FindAll ID: {findall_id}")
     print(f"  Status: {status}")
     print(f"  Generator: {generator}")
     print(f"  Limit: {limit}")
     print(f"\nCheck progress: parallel status {findall_id} --type findall")
     print(f"Get results:    parallel result {findall_id} --type findall")

 except Exception as e:
     print(f"Error: {e}", file=typer.get_text_stream("stderr"))
     raise typer.Exit(1) from None

```

File: /Users/adamjackson/LocalDev/enaible/tools/enaible/src/enaible/utils/paths.py
```py
"""Cross-platform path utilities for Enaible CLI."""

from __future__ import annotations

import os
import platform
from pathlib import Path


def get_vscode_user_dir() -> Path:
 r"""Get VS Code user directory path based on the current operating system.

 Returns
 -------
     Path to VS Code user directory:
     - macOS: ~/Library/Application Support/Code/User/
     - Windows: %APPDATA%\\Code\\User\\
     - Linux: ~/.config/Code/User/

 Raises
 ------
     RuntimeError: If the operating system is not supported.
 """
 system = platform.system().lower()

 if system == "darwin":  # macOS
     return Path.home() / "Library" / "Application Support" / "Code" / "User"
 elif system == "windows":
     appdata = os.environ.get("APPDATA")
     if not appdata:
         raise RuntimeError("APPDATA environment variable not set on Windows")
     return Path(appdata) / "Code" / "User"
 elif system == "linux":
     return Path.home() / ".config" / "Code" / "User"
 else:
     raise RuntimeError(f"Unsupported operating system: {system}")

```

File: /Users/adamjackson/LocalDev/enaible/tools/enaible/src/enaible/commands/install.py
```py
"""System installer command for Enaible CLI."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from importlib import metadata
from pathlib import Path

import typer

from ..app import app
from ..constants import MANAGED_SENTINEL
from ..prompts.adapters import (
 SYSTEM_CONTEXTS,
 VSCODE_USER_DIR_MARKER,
 SystemRenderContext,
)
from ..prompts.renderer import PromptRenderer
from ..runtime.context import load_workspace
from ..skills.renderer import SkillRenderer
from ..utils.paths import get_vscode_user_dir

SKIP_FILES = {
 "install.sh",
 "install.ps1",
 "uninstall.sh",
 ".DS_Store",
}

SYSTEM_RULES = {
 "claude-code": ("rules/global.claude.rules.md", "CLAUDE.md"),
 "codex": ("rules/global.codex.rules.md", "AGENTS.md"),
 "copilot": ("rules/global.copilot.rules.md", "AGENTS.md"),
 "cursor": ("rules/global.cursor.rules.md", "user-rules-setting.md"),
 "gemini": ("rules/global.gemini.rules.md", "GEMINI.md"),
 "antigravity": ("rules/global.antigravity.rules.md", "GEMINI.md"),
}

ALWAYS_MANAGED_PREFIXES: dict[str, tuple[str, ...]] = {
 "claude-code": ("commands/", "agents/", "rules/", "skills/"),
 "codex": ("prompts/", "rules/", "skills/"),
 "copilot": ("prompts/",),
 "cursor": ("commands/", "rules/"),
 "gemini": ("commands/",),
 "antigravity": ("workflows/", "rules/"),
}

CHECK_DEPENDENCIES_DEFAULT = os.environ.get("ENAIBLE_SKIP_DEPENDENCY_CHECKS") != "1"


def _python_install_command(*packages: str) -> tuple[str, ...]:
 uv = shutil.which("uv")
 if uv:
     return (uv, "pip", "install", "--python", sys.executable, *packages)
 return (sys.executable, "-m", "pip", "install", *packages)


def _python_install_hint(*packages: str) -> str:
 joined = " ".join(packages)
 return f"uv pip install --python {sys.executable} {joined} (or python -m pip install {joined})"


@dataclass(frozen=True)
class PromptDependency:
 name: str
 check_commands: tuple[str, ...]
 install_command: tuple[str, ...] | None
 install_hint: str
 auto_install_env: str | None = None


SEMGRAP_DEP = PromptDependency(
 name="Semgrep",
 check_commands=("semgrep",),
 install_command=_python_install_command("semgrep"),
 install_hint=_python_install_hint("semgrep"),
 auto_install_env="AAW_AUTO_INSTALL_SEMGREP",
)

DETECT_SECRETS_DEP = PromptDependency(
 name="detect-secrets",
 check_commands=("detect-secrets",),
 install_command=_python_install_command("detect-secrets"),
 install_hint=_python_install_hint("detect-secrets"),
 auto_install_env="AAW_AUTO_INSTALL_DETECT_SECRETS",
)

Ruff_DEP = PromptDependency(
 name="Ruff",
 check_commands=("ruff",),
 install_command=_python_install_command("ruff"),
 install_hint=_python_install_hint("ruff"),
 auto_install_env="AAW_AUTO_INSTALL_RUFF",
)

LIZARD_DEP = PromptDependency(
 name="Lizard",
 check_commands=("lizard",),
 install_command=_python_install_command("lizard"),
 install_hint=_python_install_hint("lizard"),
 auto_install_env="AAW_AUTO_INSTALL_LIZARD",
)

JSCPD_DEP = PromptDependency(
 name="JSCPD",
 check_commands=("jscpd", "npx"),
 install_command=("npm", "install", "-g", "jscpd"),
 install_hint="npm install -g jscpd",
 auto_install_env="AAW_AUTO_INSTALL_JSCPD",
)

ESLINT_DEP = PromptDependency(
 name="ESLint + plugins",
 check_commands=("eslint",),
 install_command=(
     "npm",
     "install",
     "-g",
     "eslint",
     "@typescript-eslint/parser",
     "eslint-plugin-react",
     "eslint-plugin-import",
     "eslint-plugin-vue",
 ),
 install_hint="npm install -g eslint @typescript-eslint/parser eslint-plugin-react eslint-plugin-import eslint-plugin-vue",
 auto_install_env="AAW_AUTO_INSTALL_ESLINT",
)

PROMPT_DEPENDENCIES: dict[str, tuple[PromptDependency, ...]] = {
 "analyze-code-quality": (LIZARD_DEP, JSCPD_DEP),
 "analyze-performance": (Ruff_DEP, SEMGRAP_DEP, ESLINT_DEP),
 "analyze-security": (SEMGRAP_DEP, DETECT_SECRETS_DEP),
}

_PROMPT_DEP_CACHE: dict[str, bool] = {}


class InstallMode(str, Enum):
 MERGE = "merge"
 UPDATE = "update"
 SYNC = "sync"
 FRESH = "fresh"


@dataclass(slots=True)
class InstallSummary:
 actions: list[tuple[str, str]]
 skipped: list[str]

 def record(self, action: str, path: Path) -> None:
     self.actions.append((action, path.as_posix()))

 def record_skip(self, path: Path) -> None:
     self.skipped.append(path.as_posix())


@dataclass(slots=True)
class InstallSettings:
 repo_root: Path
 install_cli: bool
 cli_source: Path
 sync_shared: bool
 backup: bool
 destination_root: Path
 system: str
 mode: InstallMode
 dry_run: bool


def _setup_installation_context(
 context, system: str, target: Path, scope: str
) -> tuple[SystemRenderContext, Path, Path]:
 """Set up installation context and validate source assets."""
 system_ctx = _get_system_context(system)
 source_root = context.repo_root / "systems" / system
 if not source_root.exists():
     raise typer.BadParameter(f"Source assets missing for system '{system}'.")
 destination_root = _resolve_destination(system_ctx, target, scope)
 return system_ctx, source_root, destination_root


def _prepare_installation_environment(
 settings: InstallSettings, summary: InstallSummary
) -> None:
 """Prepare installation environment: CLI, shared workspace, backups."""
 if settings.install_cli:
     _install_cli(settings.repo_root, settings.cli_source, settings.dry_run, summary)

 if settings.sync_shared:
     _sync_shared_workspace(settings.repo_root, settings.dry_run, summary)

 if settings.backup:
     _backup_destination_folder(settings.destination_root, settings.dry_run, summary)

 if settings.mode is InstallMode.FRESH:
     _clear_destination_for_fresh_install(
         settings.system, settings.destination_root, settings.dry_run, summary
     )


def _should_skip_file(
 source_file: Path,
 destination_file: Path,
 relative_posix: str,
 system: str,
 mode: InstallMode,
 always_managed_prefixes: tuple[str, ...],
) -> bool:
 """Determine if a file should be skipped based on mode and managed status."""
 # Skip rules directory for copilot/cursor
 if system in ("copilot", "cursor") and relative_posix.startswith("rules/"):
     return True

 managed = _has_managed_sentinel(source_file) or any(
     relative_posix.startswith(prefix) for prefix in always_managed_prefixes
 )
 dest_exists = destination_file.exists()
 dest_managed = _has_managed_sentinel(destination_file) if dest_exists else managed
 if any(relative_posix.startswith(prefix) for prefix in always_managed_prefixes):
     dest_managed = True

 if mode is InstallMode.UPDATE and (not dest_exists or not dest_managed):
     return True

 return (
     mode in {InstallMode.MERGE, InstallMode.SYNC}
     and dest_exists
     and not dest_managed
 )


def _process_source_files(
 source_root: Path,
 destination_root: Path,
 system: str,
 mode: InstallMode,
 dry_run: bool,
 summary: InstallSummary,
) -> None:
 """Process and copy source files to destination based on installation mode."""
 files = _iter_source_files(source_root, system)
 always_managed_prefixes = ALWAYS_MANAGED_PREFIXES.get(system, ())

 for source_file in files:
     relative = source_file.relative_to(source_root)
     destination_file = destination_root / relative
     relative_posix = relative.as_posix()

     if _should_skip_file(
         source_file,
         destination_file,
         relative_posix,
         system,
         mode,
         always_managed_prefixes,
     ):
         summary.record_skip(relative)
         continue

     if dry_run:
         summary.record("write", destination_file)
         continue

     destination_file.parent.mkdir(parents=True, exist_ok=True)
     shutil.copy2(source_file, destination_file)
     summary.record("write", destination_file)


def _complete_installation(
 context,
 system: str,
 source_root: Path,
 destination_root: Path,
 scope: str,
 sync: bool,
 mode: InstallMode,
 dry_run: bool,
 summary: InstallSummary,
 enforce_dependencies: bool,
) -> None:
 """Complete installation: render prompts, sync, post-install, emit summary."""
 _render_managed_prompts(
     context, system, destination_root, mode, dry_run, summary, enforce_dependencies
 )
 _render_managed_skills(context, system, destination_root, mode, dry_run, summary)

 if sync:
     _sync_enaible_env(context.repo_root, dry_run, summary)

 _post_install(system, source_root, destination_root, scope, dry_run, summary)
 _set_claude_status_executable(system, destination_root, dry_run, summary)
 _emit_summary(system, destination_root, mode, summary, dry_run)


@app.command("install")
def install(
 system: str = typer.Argument(
     ..., help="System adapter to install (claude-code|codex|copilot|cursor)."
 ),
 install_cli: bool = typer.Option(
     True,
     "--install-cli/--no-install-cli",
     help="Install the Enaible CLI with `uv tool install` before copying assets.",
 ),
 cli_source: Path = typer.Option(
     Path("tools/enaible"),
     "--cli-source",
     help="Path or URL passed to `uv tool install --from`. Defaults to the local tools/enaible folder.",
 ),
 target: Path = typer.Option(
     Path("."), "--target", "-t", help="Destination root for installation."
 ),
 mode: InstallMode = typer.Option(
     InstallMode.MERGE, "--mode", "-m", case_sensitive=False
 ),
 scope: str = typer.Option(
     "project",
     "--scope",
     "-s",
     help="Installation scope (project|user). Defaults to project-level directories.",
 ),
 dry_run: bool = typer.Option(
     False, "--dry-run", help="Preview actions without writing files."
 ),
 backup: bool = typer.Option(
     True,
     "--backup/--no-backup",
     help="Create timestamped backup of target folder before install.",
 ),
 sync: bool = typer.Option(
     True,
     "--sync/--no-sync",
     help="Run `uv sync --project tools/enaible` to provision Enaible dependencies before copying assets.",
 ),
 sync_shared: bool = typer.Option(
     True,
     "--sync-shared/--no-sync-shared",
     help="Copy shared/ workspace files to ~/.enaible/workspace/shared for analyzer execution.",
 ),
 enforce_dependencies: bool = typer.Option(
     CHECK_DEPENDENCIES_DEFAULT,
     "--check-deps/--no-check-deps",
     help="Verify external analyzer dependencies before installing prompts.",
 ),
) -> None:
 """Install rendered system assets into project or user configuration directories."""
 context = load_workspace()
 summary = InstallSummary(actions=[], skipped=[])
 system_ctx, source_root, destination_root = _setup_installation_context(
     context, system, target, scope
 )

 settings = InstallSettings(
     repo_root=context.repo_root,
     install_cli=install_cli,
     cli_source=cli_source,
     sync_shared=sync_shared,
     backup=backup,
     destination_root=destination_root,
     system=system,
     mode=mode,
     dry_run=dry_run,
 )
 _prepare_installation_environment(settings, summary)

 _process_source_files(source_root, destination_root, system, mode, dry_run, summary)

 _complete_installation(
     context,
     system,
     source_root,
     destination_root,
     scope,
     sync,
     mode,
     dry_run,
     summary,
     enforce_dependencies,
 )


def _install_cli(
 repo_root: Path, cli_source: Path, dry_run: bool, summary: InstallSummary
) -> None:
 """Install the Enaible CLI using uv tool install from the given source."""
 source = cli_source if cli_source.is_absolute() else (repo_root / cli_source)
 if not source.exists():
     raise typer.BadParameter(
         f"CLI source not found at {source}. Provide a valid path with --cli-source."
     )

 cmd = ["uv", "tool", "install", "--from", str(source), "enaible"]

 if dry_run:
     summary.record("install-cli", source)
     return

 subprocess.run(cmd, cwd=repo_root, check=True)

 summary.record("install-cli", source)


def _sync_shared_workspace(
 repo_root: Path, dry_run: bool, summary: InstallSummary
) -> None:
 """Copy shared workspace assets to ~/.enaible/workspace/shared."""
 source = repo_root / "shared"
 target = Path.home() / ".enaible" / "workspace" / "shared"
 allowed_paths = [
     Path("core"),
     Path("analyzers"),
     Path("config"),
     Path("utils"),
     Path("tools") / "ai_docs_changelog.py",
     Path("setup") / "install_dependencies.py",
     Path("setup") / "requirements.txt",
     Path("setup") / "monitoring",
     Path("setup") / "security",
 ]

 if not source.exists():
     raise typer.BadParameter(
         f"Shared folder missing at {source}; cannot sync workspace."
     )

 summary_path = target if target.exists() else target.parent

 if dry_run:
     summary.record("sync-shared", summary_path)
     return

 # Reset existing workspace copy to avoid stale or excess files
 if target.exists():
     shutil.rmtree(target)
 target.mkdir(parents=True, exist_ok=True)

 # Copy while ignoring caches and pyc files
 def _ignore(_dir: str, names: list[str]) -> set[str]:
     ignored = {"__pycache__", ".pytest_cache", ".DS_Store"}
     ignored.update({name for name in names if name.endswith((".pyc", ".pyo"))})
     return ignored

 for rel_path in allowed_paths:
     src = source / rel_path
     dest = target / rel_path
     if not src.exists():
         continue
     if src.is_dir():
         shutil.copytree(src, dest, dirs_exist_ok=True, ignore=_ignore)
     else:
         dest.parent.mkdir(parents=True, exist_ok=True)
         shutil.copy2(src, dest)

 summary.record("sync-shared", target)


def _iter_source_files(root: Path, system: str) -> Iterable[Path]:
 for path in root.rglob("*"):
     if path.is_file():
         if path.name in SKIP_FILES:
             continue
         yield path


def _resolve_destination(
 system_ctx: SystemRenderContext, target: Path, scope: str
) -> Path:
 if scope.lower() == "user":
     if system_ctx.user_scope_dir == VSCODE_USER_DIR_MARKER:
         return get_vscode_user_dir()
     return Path(system_ctx.user_scope_dir).expanduser()
 if scope.lower() != "project":  # pragma: no cover - input validation
     raise typer.BadParameter("Scope must be either 'project' or 'user'.")
 return (target / system_ctx.project_scope_dir).resolve()


def _has_managed_sentinel(path: Path) -> bool:
 if not path.exists():
     return False
 try:
     with path.open("r", encoding="utf-8") as handle:
         return MANAGED_SENTINEL in handle.read()
 except UnicodeDecodeError:  # pragma: no cover - binary safety
     return False


def _emit_summary(
 system: str,
 destination_root: Path,
 mode: InstallMode,
 summary: InstallSummary,
 dry_run: bool,
) -> None:
 action_label = "Planned" if dry_run else "Completed"
 typer.echo(
     f"{action_label} Enaible install for {system} ({mode.value}) -> {destination_root}"
 )
 if summary.actions:
     for action, rel_path in summary.actions:
         typer.echo(f"  {action:8} {rel_path}")
 else:
     typer.echo("  No changes required.")

 if summary.skipped:
     typer.echo("  Skipped (unmanaged or missing targets):")
     for rel_path in summary.skipped:
         typer.echo(f"    - {rel_path}")


def _get_system_context(system: str) -> SystemRenderContext:
 try:
     return SYSTEM_CONTEXTS[system]
 except KeyError as exc:  # pragma: no cover - input validation
     available = ", ".join(sorted(SYSTEM_CONTEXTS.keys()))
     raise typer.BadParameter(
         f"Unknown system '{system}'. Available adapters: {available}."
     ) from exc


def _set_claude_status_executable(
 system: str,
 destination_root: Path,
 dry_run: bool,
 summary: InstallSummary,
) -> None:
 """Set executable permissions on Claude Code status program if installed."""
 if system != "claude-code":
     return

 status_file = destination_root / "statusline-worktree"
 if not status_file.exists():
     return

 if dry_run:
     summary.record("chmod", status_file)
     return

 status_file.chmod(0o755)
 summary.record("chmod", status_file)


def _post_install(
 system: str,
 source_root: Path,
 destination_root: Path,
 scope: str,
 dry_run: bool,
 summary: InstallSummary,
) -> None:
 rules_info = SYSTEM_RULES.get(system)
 if not rules_info:
     return

 source_rules_rel, target_name = rules_info
 source_rules = source_root / source_rules_rel
 if not source_rules.exists():
     return

 # For claude-code user scope, CLAUDE.md lives inside ~/.claude. For project scope
 # the file belongs at the project root (parent of .claude/). For antigravity,
 # GEMINI.md goes in ~/.gemini/ (parent of ~/.gemini/antigravity/).
 # For codex, target goes inside .codex directory
 # For copilot, target goes inside .github subdirectory (mirrors project scope pattern)
 if system == "claude-code":
     target_path = (
         destination_root.parent / target_name
         if scope.lower() == "project"
         else destination_root / target_name
     )
 elif system == "antigravity":
     target_path = destination_root.parent / target_name
 elif system == "copilot" and scope.lower() == "user":
     # For user-level copilot installs, place AGENTS.md in .github subdirectory
     # within VS Code user directory to mirror project scope pattern
     target_path = destination_root / ".github" / target_name
 else:
     target_path = destination_root / target_name

 if dry_run:
     summary.record("merge", target_path)
     return

 if system == "codex":
     _merge_codex_agents(target_path, source_rules)
     summary.record("merge", target_path)
     return

 if system == "copilot":
     _merge_copilot_agents(target_path, source_rules)
     summary.record("merge", target_path)
     return

 if system == "cursor":
     _create_cursor_user_rules(target_path, source_rules)
     summary.record("write", target_path)
     typer.echo(
         "\n>>> Cursor requires manual configuration:\n"
         f"    Copy the contents of {target_path}\n"
         "    into Cursor > Settings > Rules > User Rules\n"
     )
     return

 header = (
     f"# AI-Assisted Workflows v{_enaible_version()} - Auto-generated, do not edit"
 )
 rules_body = source_rules.read_text(encoding="utf-8").strip()

 if target_path.exists():
     existing = target_path.read_text(encoding="utf-8")
     if "# AI-Assisted Workflows v" in existing:
         summary.record("merged", target_path)
         return
     updated = f"{existing.rstrip()}\n\n---\n\n{header}\n\n{rules_body}\n"
 else:
     updated = f"{header}\n\n{rules_body}\n"

 target_path.parent.mkdir(parents=True, exist_ok=True)
 target_path.write_text(updated, encoding="utf-8")
 summary.record("merge", target_path)


def _render_managed_prompts(
 context,
 system: str,
 destination_root: Path,
 mode: InstallMode,
 dry_run: bool,
 summary: InstallSummary,
 enforce_dependencies: bool,
) -> None:
 renderer = PromptRenderer(context)
 definitions = [
     definition.prompt_id
     for definition in renderer.list_prompts()
     if system in definition.systems
 ]
 if not definitions:
     return

 overrides: dict[str, Path] = {system: destination_root}
 results = renderer.render(definitions, [system], overrides)

 if not dry_run:
     destination_root.mkdir(parents=True, exist_ok=True)

 for result in results:
     output_path = result.output_path
     try:
         relative = output_path.relative_to(destination_root)
     except ValueError:
         relative = output_path

     if enforce_dependencies and not _prompt_dependencies_ready(
         result.prompt_id, dry_run
     ):
         summary.record_skip(relative)
         continue

     if dry_run:
         summary.record("render", output_path)
         continue

     dest_exists = output_path.exists()
     dest_managed = _has_managed_sentinel(output_path) if dest_exists else False

     if mode is InstallMode.UPDATE and (not dest_exists or not dest_managed):
         summary.record_skip(relative)
         continue

     if (
         mode in {InstallMode.MERGE, InstallMode.SYNC}
         and dest_exists
         and not dest_managed
     ):
         summary.record_skip(relative)
         continue

     output_path.parent.mkdir(parents=True, exist_ok=True)
     output_path.write_text(result.content, encoding="utf-8")
     summary.record("render", output_path)


def _render_managed_skills(
 context,
 system: str,
 destination_root: Path,
 mode: InstallMode,
 dry_run: bool,
 summary: InstallSummary,
) -> None:
 renderer = SkillRenderer(context)
 definitions = [
     definition.skill_id
     for definition in renderer.list_skills()
     if system in definition.systems
 ]
 if not definitions:
     return

 overrides: dict[str, Path] = {system: destination_root}
 results = renderer.render(definitions, [system], overrides)

 if not dry_run:
     destination_root.mkdir(parents=True, exist_ok=True)

 for result in results:
     output_path = result.output_path
     try:
         relative = output_path.relative_to(destination_root)
     except ValueError:
         relative = output_path

     if dry_run:
         summary.record("render", output_path)
         summary.record("copy", output_path.parent)
         continue

     dest_exists = output_path.exists()
     dest_managed = _has_managed_sentinel(output_path) if dest_exists else False

     if mode is InstallMode.UPDATE and (not dest_exists or not dest_managed):
         summary.record_skip(relative)
         continue

     if (
         mode in {InstallMode.MERGE, InstallMode.SYNC}
         and dest_exists
         and not dest_managed
     ):
         summary.record_skip(relative)
         continue

     result.write()
     summary.record("render", output_path)
     summary.record("copy", output_path.parent)


def _prompt_dependencies_ready(prompt_id: str | None, dry_run: bool) -> bool:
 if not prompt_id:
     return True
 if prompt_id in _PROMPT_DEP_CACHE:
     return _PROMPT_DEP_CACHE[prompt_id]
 deps = PROMPT_DEPENDENCIES.get(prompt_id)
 if not deps:
     _PROMPT_DEP_CACHE[prompt_id] = True
     return True
 missing = [dep for dep in deps if not _dependency_available(dep)]
 if not missing:
     _PROMPT_DEP_CACHE[prompt_id] = True
     return True
 dep_names = ", ".join(dep.name for dep in missing)
 typer.secho(
     f"Prompt '{prompt_id}' requires {dep_names} which are not installed.",
     fg=typer.colors.YELLOW,
 )
 for dep in missing:
     typer.echo(f"- {dep.name}: {dep.install_hint}")
     if dep.auto_install_env:
         typer.echo(f"  Auto-install: set {dep.auto_install_env}=true")
 if dry_run:
     typer.secho(
         "Dry-run mode: dependencies not installed, prompt will be skipped.",
         fg=typer.colors.YELLOW,
     )
     _PROMPT_DEP_CACHE[prompt_id] = False
     return False
 install = _confirm_install_dependencies()
 if install:
     for dep in missing:
         _install_dependency(dep)
     missing = [dep for dep in deps if not _dependency_available(dep)]
 if missing:
     typer.secho(
         f"Dependencies still missing for '{prompt_id}'. Prompt will not be installed.",
         fg=typer.colors.RED,
     )
     _PROMPT_DEP_CACHE[prompt_id] = False
     return False
 typer.secho(
     f"All dependencies for '{prompt_id}' detected. Proceeding with install.",
     fg=typer.colors.GREEN,
 )
 _PROMPT_DEP_CACHE[prompt_id] = True
 return True


def _confirm_install_dependencies() -> bool:
 if not sys.stdin.isatty():
     typer.secho(
         "Non-interactive session: auto-attempting dependency install.",
         fg=typer.colors.CYAN,
     )
     return True
 return typer.confirm(
     "Install missing dependencies now? (Administrative privileges may be required)",
     default=False,
 )


def _install_dependency(dep: PromptDependency) -> None:
 if not dep.install_command:
     return
 typer.secho(
     f"Installing {dep.name} via: {' '.join(dep.install_command)}",
     fg=typer.colors.CYAN,
 )
 try:
     subprocess.run(dep.install_command, check=True)
 except FileNotFoundError:
     typer.secho(
         f"Installer command not found while installing {dep.name}. Please install manually: {dep.install_hint}",
         fg=typer.colors.RED,
     )
 except subprocess.CalledProcessError as exc:
     typer.secho(
         f"Failed to install {dep.name} (exit code {exc.returncode}). Please install manually.",
         fg=typer.colors.RED,
     )


def _dependency_available(dep: PromptDependency) -> bool:
 return any(shutil.which(cmd) for cmd in dep.check_commands)


def _merge_codex_agents(target_path: Path, source_rules: Path) -> None:
 start_marker = "<!-- CODEx_GLOBAL_RULES_START -->"
 end_marker = "<!-- CODEx_GLOBAL_RULES_END -->"
 header = f"# AI-Assisted Workflows (Codex Global Rules) v{_enaible_version()} - Auto-generated, do not edit"
 body = source_rules.read_text(encoding="utf-8").strip()
 block = f"{start_marker}\n{header}\n\n{body}\n{end_marker}\n"

 existing = target_path.read_text(encoding="utf-8") if target_path.exists() else ""

 if start_marker in existing and end_marker in existing:
     start = existing.index(start_marker)
     end = existing.index(end_marker) + len(end_marker)
     updated = existing[:start] + block + existing[end:]
 else:
     updated = (existing.rstrip() + "\n\n" if existing.strip() else "") + block

 target_path.parent.mkdir(parents=True, exist_ok=True)
 target_path.write_text(updated.rstrip() + "\n", encoding="utf-8")


def _merge_copilot_agents(target_path: Path, source_rules: Path) -> None:
 start_marker = "<!-- COPILOT_GLOBAL_RULES_START -->"
 end_marker = "<!-- COPILOT_GLOBAL_RULES_END -->"
 header = f"# AI-Assisted Workflows (Copilot Global Rules) v{_enaible_version()} - Auto-generated, do not edit"
 body = source_rules.read_text(encoding="utf-8").strip()
 block = f"{start_marker}\n{header}\n\n{body}\n{end_marker}\n"

 existing = target_path.read_text(encoding="utf-8") if target_path.exists() else ""

 if start_marker in existing and end_marker in existing:
     start = existing.index(start_marker)
     end = existing.index(end_marker) + len(end_marker)
     updated = existing[:start] + block + existing[end:]
 else:
     updated = (existing.rstrip() + "\n\n" if existing.strip() else "") + block

 target_path.parent.mkdir(parents=True, exist_ok=True)
 target_path.write_text(updated.rstrip() + "\n", encoding="utf-8")


def _create_cursor_user_rules(target_path: Path, source_rules: Path) -> None:
 """Create user-rules-setting.md for Cursor with instructions to copy to IDE settings."""
 header = f"# Cursor User Rules v{_enaible_version()} - Copy to Cursor > Settings > Rules > User"
 instruction = "Copy the contents below into Cursor > Settings > Rules > User Rules."
 body = source_rules.read_text(encoding="utf-8").strip()

 content = f"{header}\n\n{instruction}\n\n---\n\n{body}\n"

 target_path.parent.mkdir(parents=True, exist_ok=True)
 target_path.write_text(content, encoding="utf-8")


def _enaible_version() -> str:
 try:
     return metadata.version("enaible")
 except metadata.PackageNotFoundError:  # pragma: no cover - editable installs
     return "local"


def _sync_enaible_env(repo_root: Path, dry_run: bool, summary: InstallSummary) -> None:
 if dry_run:
     summary.record("sync", repo_root / "tools" / "enaible")
     return

 if os.environ.get("ENAIBLE_INSTALL_SKIP_SYNC") == "1":
     summary.record_skip(Path("tools/enaible (sync skipped)"))
     return

 cmd = ["uv", "sync", "--project", str(repo_root / "tools" / "enaible")]
 try:
     subprocess.run(cmd, check=True)
 except subprocess.CalledProcessError as exc:
     raise typer.BadParameter(
         "Failed to run 'uv sync --project tools/enaible'. Ensure `uv` is installed and accessible."
     ) from exc
 except FileNotFoundError as exc:
     raise typer.BadParameter(
         "Failed to run 'uv sync --project tools/enaible'. Ensure `uv` is installed and accessible."
     ) from exc

 summary.record("sync", repo_root / "tools" / "enaible")


def _backup_destination_folder(
 destination_root: Path,
 dry_run: bool,
 summary: InstallSummary,
) -> None:
 """Create a timestamped backup copy of the destination folder before any install operations."""
 if not destination_root.exists():
     return

 backup_path = _next_stash_path(destination_root, ".bak")
 if dry_run:
     summary.record("backup", backup_path)
     return

 if destination_root.is_dir():
     shutil.copytree(
         destination_root,
         backup_path,
         dirs_exist_ok=False,
         copy_function=shutil.copy2,
     )
 else:
     shutil.copy2(destination_root, backup_path)
 summary.record("backup", backup_path)


def _clear_destination_for_fresh_install(
 system: str,
 destination_root: Path,
 dry_run: bool,
 summary: InstallSummary,
) -> None:
 """Remove the destination directory for FRESH mode installs.

 For codex, the destination is preserved to retain unmanaged files (sessions, auth).
 """
 if not destination_root.exists():
     return

 # Codex preserves unmanaged files - don't clear the destination
 if system == "codex":
     return

 if dry_run:
     summary.record("remove", destination_root)
     return

 temp_path = _next_stash_path(destination_root, ".tmp")
 destination_root.rename(temp_path)
 if temp_path.is_dir():
     shutil.rmtree(temp_path)
 else:
     temp_path.unlink()
 summary.record("remove", destination_root)


def _next_stash_path(path: Path, suffix: str) -> Path:
 base_name = path.name
 candidate = path.with_name(f"{base_name}{suffix}")
 if not candidate.exists():
     return candidate

 timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
 candidate = path.with_name(f"{base_name}{suffix}-{timestamp}")
 if not candidate.exists():
     return candidate

 counter = 1
 while True:
     candidate = path.with_name(f"{base_name}{suffix}-{timestamp}-{counter}")
     if not candidate.exists():
         return candidate
     counter += 1

```

File: /Users/adamjackson/LocalDev/enaible/docs/system/gemini/templates/command.toml.j2
```j2
{% if frontmatter and frontmatter.get('description') %}description = "{{ frontmatter.description }}"
{% endif %}
prompt = '''
# {{ title }}

{{ body }}
Arguments: {{ '{{args}}' }}

{{ managed_sentinel }}
'''

```

File: /Users/adamjackson/LocalDev/enaible/systems/codex/rules/global.codex.rules.md
```md
## **CRITICAL** Must follow Design Principles

- **ALWAYS** establish a working base project before beginging bespoke configuration and feature development, this means confirmed successful compile and run of the dev server with quality gates established - this is used as the baseline first commit.
- **ALWAYS** commit to git after the logical conclusion of task steps, use a frequent, atomic commit pattern to establish safe check points of known good implementation that can be reverted to if need.
- **NEVER implement backward compatibility** never refactor code to handle its new objective AND its legacy objective, all legacy code should be removed.
- **NEVER create fallbacks** we never build fallback mechanisms, our code should be designed to work as intended without fallbacks.
- **ALWAY KISS - Keep it simple stupid** only action what the user has requested and no more, never over engineer, if you dont have approval for expanding the scope of a task you must ask the user first.
- **ALWAYS minimise complexity** keep code Cyclomatic Complexity under 10
- **ALWAYS prefer established libraries over bespoke code** only produce bespoke code if no established library
- **ALWAYS use appropriate symbol naming when refactoring code**: When refactoring do not add prefixes/suffixes like "Refactored", "Updated", "New", or "V2" to symbol names to indicate changes.
- **ALWAYS Align UI style changes to shadcn/Tailwind/Radix patterns and Lucide assets**: For your UI stack implementation avoid bespoke classes and direct style hardcoding to objects.

## **CRITICAL** Must follow Behaviour Rules - how you carry out actions

### Security Requirements

- **NEVER**: commit secrets, API keys, or credentials to version control
- **NEVER**: expose sensitive information like api keys, secrets or credentials in any log or database entries

### Prohibit Reward Hacking

- **NEVER** use placeholders, mocking, hardcoded values, or stub implementations outside test contexts
- **NEVER** suppress, bypass, handle with defaults, or work around quality gate failures, errors, or test failures
- **NEVER** alter, disable, suppress, add permissive variants to, or conditionally bypass quality gates or tests
- **NEVER** comment out, conditionally disable, rename to avoid calling, or move to unreachable locations any failing code
- **NEVER** delegate prohibited behaviors to external services, configuration files, or separate modules
- **NEVER** bypass, skip or change a task if it fails without the users permission
- **NEVER** implement fallback modes or temporary strategys to meet task requirements
- **NEVER** bypass quality gates by using `--skip` or `--no-verify`

## **CRITICAL** Development workflow tools

If the user types --help list out bulleted list of all the available tools below, single line per tool with short description and how to invoke

### When you need to execute Long-Running Tasks

If `--tmux` is included in a users request or a request requires long runnning execution (like a dev server) or we want to defence against a bash task that may stall, you **must** use tmux.

- Run long-running services in named tmux sessions: `tmux new-session -d -s <name> '<command>'`
- Check existing: `tmux list-sessions`, Attach: `tmux attach -t <name>`, Logs: `tmux capture-pane -p -S -200 -t <name>`
- Wrap uncertain/long commands in tmux to prevent blocking
- Kill session: `tmux kill-session -t <name>`

```

File: /Users/adamjackson/LocalDev/enaible/docs/system/templates/prompt.md
```md
<!--
Template Guidance:
- Comments exist for author direction only; do NOT copy them into prompt outputs.
- prompt_template is the format to implement.
- prompt_example shows examples of prompt_template usage.
- Add preflight checks inside the Workflow section only when supplementary requirements are needed beyond baseline tooling.
- Templates may include rule directives using <!-- rule: ... --> comments; `uv run --project tools/enaible enaible prompts render ...` enforces them when generating command variants.

-->

<prompt_template>

# Purpose

<!-- Describe the command objective in one sentence. -->

State the objective in one sentence. Be direct and outcome‑focused.

## Variables

<!-- Bind positional arguments or flags used by the prompt. Prefix all resolved variables with `$` to avoid ambiguity. -->

- Define explicit, @‑prefixed variable names for clarity:
- $1 → @TARGET (or domain‑specific name)
- $2 → @SCOPE (optional)
- $3 → @MESSAGE (optional)
- $4..$9 → additional specifics (document if used)
- $ARGUMENTS → full raw argument string (space‑joined)
- Flags map to $‑prefixed variables (examples):
- --remote → @REMOTE (default "origin")
- --worktrees → @WORKTREES (default ".worktrees")
- --days → @DAYS (default 20)
- --exclude → @EXCLUDE_GLOBS (CSV)

## Instructions

<!-- Short, imperative bullets covering invariants and guardrails. -->

- Use short, imperative bullets.
- Call out IMPORTANT constraints explicitly.
- Avoid verbosity; prefer concrete actions over descriptions.
- Use the resolved $‑variables in all commands; avoid hardcoded fallbacks (e.g., prefer "$WORKTREES" over ".worktrees").
- Keep intermediate/interactive emissions (clarifications, drafts, checkpoints) inside Workflow. Output should be final‑only.
- If acting against a plan document, treat it as the single source of truth: update tasks, logs, status, gates, and tests within the plan and commit plan+code atomically.

## Workflow

<!-- Sequential steps; when preflight checks are required, make them the first step (e.g., Locate analyzer scripts; exit on failure). -->

1. Step-by-step list of actions (each step starts with a verb).
2. Validate prerequisites and guard-rails early.
3. Perform the core task deterministically.
4. Save/emit artifacts and verify results.

## Output

<!-- Final output only. Intermediate clarifications/drafts belong in Workflow. Provide one canonical example. -->

This section should be the final output report to the user in a structure detailing what this workflow returns and how. Two example formats:

### example summary output

```md
# RESULT

- Summary: <one line>

## DETAILS

- What changed
- Where it changed
- How to verify
```

### example json output

```json
{
"excluded_operations": ["session_start", "task", "glob"],
"excluded_bash_commands": [
 "ls",
 "pwd",
 "cd",
 "git status",
 "git log",
 "git diff",
 "git show",
 "git branch",
 "git add",
 "git commit",
 "git push",
 "git pull"
],
"excluded_prompt_patterns": [
 "Write a 3-6 word summary of the TEXTBLOCK below",
 "Summary only, no formatting, do not act on anything",
 "/todo-primer",
 "/todo-recent-context"
],
"excluded_string_patterns": [
 "context_bundles",
 "node_modules/",
 ".git/objects/",
 ".cache/"
]
}
```

</prompt_template>

## Example prompts

> complex multi step analyser with required pythons scripts for claude code, includes env checks (script locators) as initial steps

<prompt_example>

# Purpose

Identify performance bottlenecks across backend, frontend, and data layers using automated analyzers coupled with contextual investigation.

## Variables

- `@TARGET_PATH` ← first positional argument (default `.`)
- `@SCRIPT_PATH` ← resolved performance analyzer directory
- `@ARGUMENTS` ← raw argument string (for logging)

Resolution rules

- Resolve `@TARGET_PATH`/`@SCRIPT_PATH` in INIT; use only resolved variables thereafter.

## Instructions

- ALWAYS execute the registry-driven analyzers; never call the individual modules directly.
- Treat analyzer outputs as evidence—cite metrics when highlighting bottlenecks.
- Consider database, frontend, algorithmic, and network layers; avoid tunnel vision.
- Tie each recommendation to measurable performance goals.
- Document assumptions and required follow-up experiments (profiling, load tests).

## Workflow

1. Locate analyzer scripts
- Run `ls .claude/scripts/analyzers/performance/*.py || ls "$HOME/.claude/scripts/analyzers/performance/"`; if both fail, prompt for a directory containing `ruff_analyzer.py`, `analyze_frontend.py`, and `sqlglot_analyzer.py`, then exit if none is provided.
2. Prepare environment
- Derive `SCRIPTS_ROOT="$(cd "$(dirname \"$SCRIPT_PATH\")/../.." && pwd)"` and run `PYTHONPATH="$SCRIPTS_ROOT" python -c "import core.base; print('env OK')"`; exit immediately if it fails.
3. Run automated analyzers
- Execute sequentially:
  - `performance:flake8-perf`
  - `performance:frontend`
  - `performance:sqlfluff`
- Save JSON outputs and note start/end timestamps.
4. Aggregate findings
- Parse slow hotspots (function-level metrics, lint warnings, SQL anti-patterns).
- Map findings to system components (API endpoints, React routes, SQL migrations).
5. Investigate context
- Examine code around flagged areas for caching gaps, unnecessary re-renders, unindexed queries.
- Consider infrastructure or configuration contributors (rate limits, memory caps).
6. Prioritize remediations
- Group issues by impact: critical (user-facing latency, OOM risks), high, medium.
- Recommend targeted actions (index creation, memoization, batching, background jobs).
7. Produce report
- Provide a structured summary, include metric tables, and outline validation steps (profiling, load tests).

## Output

```md
# RESULT

- Summary: Performance analysis completed for <TARGET_PATH>.

## BOTTLENECKS

| Layer    | Location              | Finding                            | Evidence Source      |
| -------- | --------------------- | ---------------------------------- | -------------------- |
| Backend  | api/orders.py#L142    | N+1 query detected                 | performance:sqlfluff |
| Frontend | src/App.tsx#L88       | Expensive re-render (missing memo) | performance:frontend |
| Database | migrations/202310.sql | Full table scan on large dataset   | performance:sqlfluff |

## RECOMMENDED ACTIONS

1. <High priority optimization with expected impact and verification plan>
2. <Secondary optimization>

## VALIDATION PLAN

- Benchmark: <command or script>
- Success Criteria: <quantitative target>

## ATTACHMENTS

- performance:flake8-perf → <path>
- performance:frontend → <path>
- performance:sqlfluff → <path>
```

</prompt_example>

```

File: /Users/adamjackson/LocalDev/enaible/tools/enaible/src/enaible/prompts/adapters.py
```py
"""System adapter metadata for prompt rendering."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class SystemRenderContext:
 name: str
 project_scope_dir: str
 user_scope_dir: str
 description: str


# Special marker for VS Code user directory (resolved at runtime based on OS)
VSCODE_USER_DIR_MARKER = "VSCODE_USER_DIR"


SYSTEM_CONTEXTS: Mapping[str, SystemRenderContext] = {
 "claude-code": SystemRenderContext(
     name="claude-code",
     project_scope_dir=".claude",
     user_scope_dir="~/.claude",
     description="Claude Code CLI",
 ),
 "codex": SystemRenderContext(
     name="codex",
     project_scope_dir=".codex",
     user_scope_dir="~/.codex",
     description="Codex CLI",
 ),
 "copilot": SystemRenderContext(
     name="copilot",
     project_scope_dir=".github",
     user_scope_dir=VSCODE_USER_DIR_MARKER,
     description="GitHub Copilot",
 ),
 "cursor": SystemRenderContext(
     name="cursor",
     project_scope_dir=".cursor",
     user_scope_dir="~/.cursor",
     description="Cursor IDE",
 ),
 "gemini": SystemRenderContext(
     name="gemini",
     project_scope_dir=".gemini",
     user_scope_dir="~/.gemini",
     description="Gemini CLI",
 ),
 "antigravity": SystemRenderContext(
     name="antigravity",
     project_scope_dir=".agent",
     user_scope_dir="~/.gemini/antigravity",
     description="Google Antigravity IDE",
 ),
}

```

File: /Users/adamjackson/LocalDev/enaible/tools/enaible/src/enaible/prompts/catalog.py
```py
"""Prompt catalog metadata for Enaible render pipeline."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class SystemPromptConfig:
 template: str
 output_path: Path
 frontmatter: Mapping[str, str] = field(default_factory=dict)
 metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class PromptDefinition:
 prompt_id: str
 source_path: Path
 title: str
 systems: Mapping[str, SystemPromptConfig]


def _repo_path(*parts: str) -> Path:
 return Path(*parts)


CATALOG: dict[str, PromptDefinition] = {
 "analyze-security": PromptDefinition(
     prompt_id="analyze-security",
     source_path=_repo_path("shared", "prompts", "analyze-security.md"),
     title="analyze-security v1.0",
     systems={
         "claude-code": SystemPromptConfig(
             template="docs/system/claude-code/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "claude-code",
                 "commands",
                 "analyze-security.md",
             ),
             frontmatter={"argument-hint": "[target-path] [--verbose]"},
         ),
         "codex": SystemPromptConfig(
             template="docs/system/codex/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "codex", "prompts", "analyze-security.md"
             ),
             metadata={"comment": "codex prompt (frontmatter-free)"},
         ),
         "copilot": SystemPromptConfig(
             template="docs/system/copilot/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "copilot",
                 "prompts",
                 "analyze-security.prompt.md",
             ),
             frontmatter={
                 "description": "Perform a comprehensive security audit of the repository and dependencies",
                 "mode": "agent",
                 "tools": ["edit", "githubRepo", "search/codebase", "terminal"],
             },
         ),
         "cursor": SystemPromptConfig(
             template="docs/system/cursor/templates/command.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "cursor", "commands", "analyze-security.md"
             ),
         ),
         "gemini": SystemPromptConfig(
             template="docs/system/gemini/templates/command.toml.j2",
             output_path=_repo_path(
                 ".build", "rendered", "gemini", "commands", "analyze-security.toml"
             ),
             frontmatter={
                 "description": "Perform a comprehensive security audit of the repository and dependencies"
             },
         ),
         "antigravity": SystemPromptConfig(
             template="docs/system/antigravity/templates/workflow.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "antigravity",
                 "workflows",
                 "analyze-security.md",
             ),
             frontmatter={
                 "description": "Perform a comprehensive security audit of the repository and dependencies"
             },
         ),
     },
 ),
 "analyze-architecture": PromptDefinition(
     prompt_id="analyze-architecture",
     source_path=_repo_path("shared", "prompts", "analyze-architecture.md"),
     title="analyze-architecture v1.0",
     systems={
         "claude-code": SystemPromptConfig(
             template="docs/system/claude-code/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "claude-code",
                 "commands",
                 "analyze-architecture.md",
             ),
             frontmatter={"argument-hint": "[target-path]"},
         ),
         "codex": SystemPromptConfig(
             template="docs/system/codex/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "codex", "prompts", "analyze-architecture.md"
             ),
             metadata={"comment": "codex prompt (frontmatter-free)"},
         ),
         "copilot": SystemPromptConfig(
             template="docs/system/copilot/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "copilot",
                 "prompts",
                 "analyze-architecture.prompt.md",
             ),
             frontmatter={
                 "description": "Evaluate system architecture for scalability, maintainability, and best practices",
                 "mode": "agent",
                 "tools": ["githubRepo", "search/codebase"],
             },
         ),
         "cursor": SystemPromptConfig(
             template="docs/system/cursor/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "cursor",
                 "commands",
                 "analyze-architecture.md",
             ),
         ),
         "gemini": SystemPromptConfig(
             template="docs/system/gemini/templates/command.toml.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "gemini",
                 "commands",
                 "analyze-architecture.toml",
             ),
             frontmatter={
                 "description": "Evaluate system architecture for scalability, maintainability, and best practices"
             },
         ),
         "antigravity": SystemPromptConfig(
             template="docs/system/antigravity/templates/workflow.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "antigravity",
                 "workflows",
                 "analyze-architecture.md",
             ),
             frontmatter={
                 "description": "Evaluate system architecture for scalability, maintainability, and best practices"
             },
         ),
     },
 ),
 "analyze-code-quality": PromptDefinition(
     prompt_id="analyze-code-quality",
     source_path=_repo_path("shared", "prompts", "analyze-code-quality.md"),
     title="analyze-code-quality v1.0",
     systems={
         "claude-code": SystemPromptConfig(
             template="docs/system/claude-code/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "claude-code",
                 "commands",
                 "analyze-code-quality.md",
             ),
             frontmatter={"argument-hint": "[target-path]"},
         ),
         "codex": SystemPromptConfig(
             template="docs/system/codex/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "codex", "prompts", "analyze-code-quality.md"
             ),
             metadata={"comment": "codex prompt (frontmatter-free)"},
         ),
         "copilot": SystemPromptConfig(
             template="docs/system/copilot/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "copilot",
                 "prompts",
                 "analyze-code-quality.prompt.md",
             ),
             frontmatter={
                 "description": "Assess code quality and complexity, and highlight high-value refactors",
                 "mode": "agent",
                 "tools": ["githubRepo", "search/codebase", "terminal"],
             },
         ),
         "cursor": SystemPromptConfig(
             template="docs/system/cursor/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "cursor",
                 "commands",
                 "analyze-code-quality.md",
             ),
         ),
         "gemini": SystemPromptConfig(
             template="docs/system/gemini/templates/command.toml.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "gemini",
                 "commands",
                 "analyze-code-quality.toml",
             ),
             frontmatter={
                 "description": "Assess code quality and complexity, and highlight high-value refactors"
             },
         ),
         "antigravity": SystemPromptConfig(
             template="docs/system/antigravity/templates/workflow.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "antigravity",
                 "workflows",
                 "analyze-code-quality.md",
             ),
             frontmatter={
                 "description": "Assess code quality and complexity, and highlight high-value refactors"
             },
         ),
     },
 ),
 "analyze-performance": PromptDefinition(
     prompt_id="analyze-performance",
     source_path=_repo_path("shared", "prompts", "analyze-performance.md"),
     title="analyze-performance v1.0",
     systems={
         "claude-code": SystemPromptConfig(
             template="docs/system/claude-code/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "claude-code",
                 "commands",
                 "analyze-performance.md",
             ),
             frontmatter={"argument-hint": "[target-path]"},
         ),
         "codex": SystemPromptConfig(
             template="docs/system/codex/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "codex", "prompts", "analyze-performance.md"
             ),
             metadata={"comment": "codex prompt (frontmatter-free)"},
         ),
         "copilot": SystemPromptConfig(
             template="docs/system/copilot/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "copilot",
                 "prompts",
                 "analyze-performance.prompt.md",
             ),
             frontmatter={
                 "description": "Identify performance bottlenecks and propose minimal, high-impact optimizations",
                 "mode": "agent",
                 "tools": ["githubRepo", "search/codebase", "terminal"],
             },
         ),
         "cursor": SystemPromptConfig(
             template="docs/system/cursor/templates/command.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "cursor", "commands", "analyze-performance.md"
             ),
         ),
         "gemini": SystemPromptConfig(
             template="docs/system/gemini/templates/command.toml.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "gemini",
                 "commands",
                 "analyze-performance.toml",
             ),
             frontmatter={
                 "description": "Identify performance bottlenecks and propose minimal, high-impact optimizations"
             },
         ),
         "antigravity": SystemPromptConfig(
             template="docs/system/antigravity/templates/workflow.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "antigravity",
                 "workflows",
                 "analyze-performance.md",
             ),
             frontmatter={
                 "description": "Identify performance bottlenecks and propose minimal, high-impact optimizations"
             },
         ),
     },
 ),
 "analyze-root-cause": PromptDefinition(
     prompt_id="analyze-root-cause",
     source_path=_repo_path("shared", "prompts", "analyze-root-cause.md"),
     title="analyze-root-cause v1.0",
     systems={
         "claude-code": SystemPromptConfig(
             template="docs/system/claude-code/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "claude-code",
                 "commands",
                 "analyze-root-cause.md",
             ),
             frontmatter={"argument-hint": "[issue-description]"},
         ),
         "codex": SystemPromptConfig(
             template="docs/system/codex/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "codex", "prompts", "analyze-root-cause.md"
             ),
             metadata={"comment": "codex prompt (frontmatter-free)"},
         ),
         "copilot": SystemPromptConfig(
             template="docs/system/copilot/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "copilot",
                 "prompts",
                 "analyze-root-cause.prompt.md",
             ),
             frontmatter={
                 "description": "Perform root cause analysis for a defect or failure",
                 "mode": "agent",
                 "tools": ["githubRepo", "search/codebase"],
             },
         ),
         "cursor": SystemPromptConfig(
             template="docs/system/cursor/templates/command.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "cursor", "commands", "analyze-root-cause.md"
             ),
         ),
         "gemini": SystemPromptConfig(
             template="docs/system/gemini/templates/command.toml.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "gemini",
                 "commands",
                 "analyze-root-cause.toml",
             ),
             frontmatter={
                 "description": "Perform root cause analysis for a defect or failure"
             },
         ),
         "antigravity": SystemPromptConfig(
             template="docs/system/antigravity/templates/workflow.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "antigravity",
                 "workflows",
                 "analyze-root-cause.md",
             ),
             frontmatter={
                 "description": "Perform root cause analysis for a defect or failure"
             },
         ),
     },
 ),
 "plan-refactor": PromptDefinition(
     prompt_id="plan-refactor",
     source_path=_repo_path("shared", "prompts", "plan-refactor.md"),
     title="plan-refactor v1.0",
     systems={
         "claude-code": SystemPromptConfig(
             template="docs/system/claude-code/templates/command.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "claude-code", "commands", "plan-refactor.md"
             ),
             frontmatter={"argument-hint": "<refactor-scope-or-area>"},
         ),
         "codex": SystemPromptConfig(
             template="docs/system/codex/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "codex", "prompts", "plan-refactor.md"
             ),
             metadata={"comment": "codex prompt (frontmatter-free)"},
         ),
         "copilot": SystemPromptConfig(
             template="docs/system/copilot/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "copilot",
                 "prompts",
                 "plan-refactor.prompt.md",
             ),
             frontmatter={
                 "description": "Plan a minimal, high-impact refactor with clear boundaries and tests",
                 "mode": "agent",
                 "tools": ["githubRepo", "search/codebase"],
             },
         ),
         "cursor": SystemPromptConfig(
             template="docs/system/cursor/templates/command.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "cursor", "commands", "plan-refactor.md"
             ),
         ),
         "gemini": SystemPromptConfig(
             template="docs/system/gemini/templates/command.toml.j2",
             output_path=_repo_path(
                 ".build", "rendered", "gemini", "commands", "plan-refactor.toml"
             ),
             frontmatter={
                 "description": "Plan a minimal, high-impact refactor with clear boundaries and tests"
             },
         ),
         "antigravity": SystemPromptConfig(
             template="docs/system/antigravity/templates/workflow.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "antigravity",
                 "workflows",
                 "plan-refactor.md",
             ),
             frontmatter={
                 "description": "Plan a minimal, high-impact refactor with clear boundaries and tests"
             },
         ),
     },
 ),
 "plan-solution": PromptDefinition(
     prompt_id="plan-solution",
     source_path=_repo_path("shared", "prompts", "plan-solution.md"),
     title="plan-solution v1.0",
     systems={
         "claude-code": SystemPromptConfig(
             template="docs/system/claude-code/templates/command.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "claude-code", "commands", "plan-solution.md"
             ),
             frontmatter={"argument-hint": "<technical-challenge> [--critique]"},
         ),
         "codex": SystemPromptConfig(
             template="docs/system/codex/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "codex", "prompts", "plan-solution.md"
             ),
             metadata={"comment": "codex prompt (frontmatter-free)"},
         ),
         "copilot": SystemPromptConfig(
             template="docs/system/copilot/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "copilot",
                 "prompts",
                 "plan-solution.prompt.md",
             ),
             frontmatter={
                 "description": "Develop a solution plan for a technical challenge with constraints and milestones",
                 "mode": "agent",
                 "tools": ["githubRepo", "search/codebase"],
             },
         ),
         "cursor": SystemPromptConfig(
             template="docs/system/cursor/templates/command.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "cursor", "commands", "plan-solution.md"
             ),
         ),
         "gemini": SystemPromptConfig(
             template="docs/system/gemini/templates/command.toml.j2",
             output_path=_repo_path(
                 ".build", "rendered", "gemini", "commands", "plan-solution.toml"
             ),
             frontmatter={
                 "description": "Develop a solution plan for a technical challenge with constraints and milestones"
             },
         ),
         "antigravity": SystemPromptConfig(
             template="docs/system/antigravity/templates/workflow.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "antigravity",
                 "workflows",
                 "plan-solution.md",
             ),
             frontmatter={
                 "description": "Develop a solution plan for a technical challenge with constraints and milestones"
             },
         ),
     },
 ),
 "get-codebase-primer": PromptDefinition(
     prompt_id="get-codebase-primer",
     source_path=_repo_path("shared", "prompts", "get-codebase-primer.md"),
     title="get-codebase-primer v1.0",
     systems={
         "claude-code": SystemPromptConfig(
             template="docs/system/claude-code/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "claude-code",
                 "commands",
                 "get-codebase-primer.md",
             ),
         ),
         "codex": SystemPromptConfig(
             template="docs/system/codex/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "codex", "prompts", "get-codebase-primer.md"
             ),
             metadata={"comment": "codex prompt (frontmatter-free)"},
         ),
         "copilot": SystemPromptConfig(
             template="docs/system/copilot/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "copilot",
                 "prompts",
                 "get-codebase-primer.prompt.md",
             ),
             frontmatter={
                 "description": "Generate a comprehensive primer for understanding the codebase",
                 "mode": "agent",
                 "tools": ["githubRepo", "search/codebase"],
             },
         ),
         "cursor": SystemPromptConfig(
             template="docs/system/cursor/templates/command.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "cursor", "commands", "get-codebase-primer.md"
             ),
         ),
         "gemini": SystemPromptConfig(
             template="docs/system/gemini/templates/command.toml.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "gemini",
                 "commands",
                 "get-codebase-primer.toml",
             ),
             frontmatter={
                 "description": "Generate a comprehensive primer for understanding the codebase"
             },
         ),
         "antigravity": SystemPromptConfig(
             template="docs/system/antigravity/templates/workflow.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "antigravity",
                 "workflows",
                 "get-codebase-primer.md",
             ),
             frontmatter={
                 "description": "Generate a comprehensive primer for understanding the codebase"
             },
         ),
     },
 ),
 "setup-code-precommit-checks": PromptDefinition(
     prompt_id="setup-code-precommit-checks",
     source_path=_repo_path("shared", "prompts", "setup-code-precommit-checks.md"),
     title="setup-code-precommit-checks v1.0",
     systems={
         "claude-code": SystemPromptConfig(
             template="docs/system/claude-code/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "claude-code",
                 "commands",
                 "setup-code-precommit-checks.md",
             ),
         ),
         "codex": SystemPromptConfig(
             template="docs/system/codex/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "codex",
                 "prompts",
                 "setup-code-precommit-checks.md",
             ),
             metadata={"comment": "codex prompt (frontmatter-free)"},
         ),
         "copilot": SystemPromptConfig(
             template="docs/system/copilot/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "copilot",
                 "prompts",
                 "setup-code-precommit-checks.prompt.md",
             ),
             frontmatter={
                 "description": "Set up language-appropriate pre-commit hooks for the repo",
                 "mode": "agent",
                 "tools": ["githubRepo", "search/codebase", "terminal"],
             },
         ),
         "cursor": SystemPromptConfig(
             template="docs/system/cursor/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "cursor",
                 "commands",
                 "setup-code-precommit-checks.md",
             ),
         ),
         "gemini": SystemPromptConfig(
             template="docs/system/gemini/templates/command.toml.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "gemini",
                 "commands",
                 "setup-code-precommit-checks.toml",
             ),
             frontmatter={
                 "description": "Set up language-appropriate pre-commit hooks for the repo"
             },
         ),
         "antigravity": SystemPromptConfig(
             template="docs/system/antigravity/templates/workflow.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "antigravity",
                 "workflows",
                 "setup-code-precommit-checks.md",
             ),
             frontmatter={
                 "description": "Set up language-appropriate pre-commit hooks for the repo"
             },
         ),
     },
 ),
 "create-rule": PromptDefinition(
     prompt_id="create-rule",
     source_path=_repo_path("shared", "prompts", "create-rule.md"),
     title="create-rule v1.0",
     systems={
         "claude-code": SystemPromptConfig(
             template="docs/system/claude-code/templates/command.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "claude-code", "commands", "create-rule.md"
             ),
             frontmatter={"argument-hint": "<technology> [--out <path>]"},
         ),
         "codex": SystemPromptConfig(
             template="docs/system/codex/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "codex", "prompts", "create-rule.md"
             ),
             metadata={"comment": "codex prompt (frontmatter-free)"},
         ),
         "copilot": SystemPromptConfig(
             template="docs/system/copilot/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "copilot", "prompts", "create-rule.prompt.md"
             ),
             frontmatter={
                 "description": "Generate an implementation rule file for a technology",
                 "mode": "agent",
                 "tools": ["githubRepo", "search/codebase"],
             },
         ),
         "cursor": SystemPromptConfig(
             template="docs/system/cursor/templates/command.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "cursor", "commands", "create-rule.md"
             ),
         ),
         "gemini": SystemPromptConfig(
             template="docs/system/gemini/templates/command.toml.j2",
             output_path=_repo_path(
                 ".build", "rendered", "gemini", "commands", "create-rule.toml"
             ),
             frontmatter={
                 "description": "Generate an implementation rule file for a technology"
             },
         ),
         "antigravity": SystemPromptConfig(
             template="docs/system/antigravity/templates/workflow.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "antigravity",
                 "workflows",
                 "create-rule.md",
             ),
             frontmatter={
                 "description": "Generate an implementation rule file for a technology"
             },
         ),
     },
 ),
 "create-hand-off": PromptDefinition(
     prompt_id="create-hand-off",
     source_path=_repo_path("shared", "prompts", "create-hand-off.md"),
     title="create-hand-off v1.0",
     systems={
         "claude-code": SystemPromptConfig(
             template="docs/system/claude-code/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "claude-code",
                 "commands",
                 "create-hand-off.md",
             ),
         ),
         "codex": SystemPromptConfig(
             template="docs/system/codex/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "codex", "prompts", "create-hand-off.md"
             ),
             metadata={"comment": "codex prompt (frontmatter-free)"},
         ),
         "copilot": SystemPromptConfig(
             template="docs/system/copilot/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "copilot",
                 "prompts",
                 "create-hand-off.prompt.md",
             ),
             frontmatter={
                 "description": "Generate handoff prompt for next AI session",
                 "mode": "agent",
                 "tools": ["githubRepo", "search/codebase"],
             },
         ),
         "cursor": SystemPromptConfig(
             template="docs/system/cursor/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "cursor",
                 "commands",
                 "create-hand-off.md",
             ),
         ),
         "gemini": SystemPromptConfig(
             template="docs/system/gemini/templates/command.toml.j2",
             output_path=_repo_path(
                 ".build", "rendered", "gemini", "commands", "create-hand-off.toml"
             ),
             frontmatter={
                 "description": "Generate handoff prompt for next AI session"
             },
         ),
         "antigravity": SystemPromptConfig(
             template="docs/system/antigravity/templates/workflow.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "antigravity",
                 "workflows",
                 "create-hand-off.md",
             ),
             frontmatter={
                 "description": "Generate handoff prompt for next AI session"
             },
         ),
     },
 ),
 "plan-ux-prd": PromptDefinition(
     prompt_id="plan-ux-prd",
     source_path=_repo_path("shared", "prompts", "plan-ux-prd.md"),
     title="plan-ux-prd v0.3",
     systems={
         "claude-code": SystemPromptConfig(
             template="docs/system/claude-code/templates/command.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "claude-code", "commands", "plan-ux-prd.md"
             ),
             frontmatter={"argument-hint": "<product-brief>"},
         ),
         "codex": SystemPromptConfig(
             template="docs/system/codex/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "codex", "prompts", "plan-ux-prd.md"
             ),
             metadata={"comment": "codex prompt (frontmatter-free)"},
         ),
         "copilot": SystemPromptConfig(
             template="docs/system/copilot/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "copilot", "prompts", "plan-ux-prd.prompt.md"
             ),
             frontmatter={
                 "description": "Produce a UX-focused PRD from a product brief",
                 "mode": "agent",
                 "tools": ["githubRepo", "search/codebase"],
             },
         ),
         "cursor": SystemPromptConfig(
             template="docs/system/cursor/templates/command.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "cursor", "commands", "plan-ux-prd.md"
             ),
         ),
         "gemini": SystemPromptConfig(
             template="docs/system/gemini/templates/command.toml.j2",
             output_path=_repo_path(
                 ".build", "rendered", "gemini", "commands", "plan-ux-prd.toml"
             ),
             frontmatter={
                 "description": "Produce a UX-focused PRD from a product brief"
             },
         ),
         "antigravity": SystemPromptConfig(
             template="docs/system/antigravity/templates/workflow.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "antigravity",
                 "workflows",
                 "plan-ux-prd.md",
             ),
             frontmatter={
                 "description": "Produce a UX-focused PRD from a product brief"
             },
         ),
     },
 ),
 "review-docs-drift": PromptDefinition(
     prompt_id="review-docs-drift",
     source_path=_repo_path("shared", "prompts", "review-docs-drift.md"),
     title="review-docs-drift v0.1",
     systems={
         "claude-code": SystemPromptConfig(
             template="docs/system/claude-code/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "claude-code",
                 "commands",
                 "review-docs-drift.md",
             ),
         ),
         "codex": SystemPromptConfig(
             template="docs/system/codex/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "codex", "prompts", "review-docs-drift.md"
             ),
             metadata={"comment": "codex prompt (frontmatter-free)"},
         ),
         "copilot": SystemPromptConfig(
             template="docs/system/copilot/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "copilot",
                 "prompts",
                 "review-docs-drift.prompt.md",
             ),
             frontmatter={
                 "description": "Review README.md and AGENTS.md for documentation drift against recent changes",
                 "mode": "agent",
                 "tools": ["edit", "githubRepo", "search/codebase", "terminal"],
             },
         ),
         "cursor": SystemPromptConfig(
             template="docs/system/cursor/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "cursor",
                 "commands",
                 "review-docs-drift.md",
             ),
         ),
         "gemini": SystemPromptConfig(
             template="docs/system/gemini/templates/command.toml.j2",
             output_path=_repo_path(
                 ".build", "rendered", "gemini", "commands", "review-docs-drift.toml"
             ),
             frontmatter={
                 "description": "Review README.md and AGENTS.md for documentation drift against recent changes"
             },
         ),
         "antigravity": SystemPromptConfig(
             template="docs/system/antigravity/templates/workflow.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "antigravity",
                 "workflows",
                 "review-docs-drift.md",
             ),
             frontmatter={
                 "description": "Review README.md and AGENTS.md for documentation drift against recent changes"
             },
         ),
     },
 ),
 "setup-dev-monitoring": PromptDefinition(
     prompt_id="setup-dev-monitoring",
     source_path=_repo_path("shared", "prompts", "setup-dev-monitoring.md"),
     title="setup-dev-monitoring v0.4",
     systems={
         "claude-code": SystemPromptConfig(
             template="docs/system/claude-code/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "claude-code",
                 "commands",
                 "setup-dev-monitoring.md",
             ),
         ),
         "codex": SystemPromptConfig(
             template="docs/system/codex/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "codex", "prompts", "setup-dev-monitoring.md"
             ),
             metadata={"comment": "codex prompt (frontmatter-free)"},
         ),
         "copilot": SystemPromptConfig(
             template="docs/system/copilot/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "copilot",
                 "prompts",
                 "setup-dev-monitoring.prompt.md",
             ),
             frontmatter={
                 "description": "Configure development monitoring, logging, and orchestration",
                 "mode": "agent",
                 "tools": ["githubRepo", "search/codebase", "terminal"],
             },
         ),
         "cursor": SystemPromptConfig(
             template="docs/system/cursor/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "cursor",
                 "commands",
                 "setup-dev-monitoring.md",
             ),
         ),
         "gemini": SystemPromptConfig(
             template="docs/system/gemini/templates/command.toml.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "gemini",
                 "commands",
                 "setup-dev-monitoring.toml",
             ),
             frontmatter={
                 "description": "Configure development monitoring, logging, and orchestration"
             },
         ),
         "antigravity": SystemPromptConfig(
             template="docs/system/antigravity/templates/workflow.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "antigravity",
                 "workflows",
                 "setup-dev-monitoring.md",
             ),
             frontmatter={
                 "description": "Configure development monitoring, logging, and orchestration"
             },
         ),
     },
 ),
 "setup-package-monitoring": PromptDefinition(
     prompt_id="setup-package-monitoring",
     source_path=_repo_path("shared", "prompts", "setup-package-monitoring.md"),
     title="setup-package-monitoring v1.0",
     systems={
         "claude-code": SystemPromptConfig(
             template="docs/system/claude-code/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "claude-code",
                 "commands",
                 "setup-package-monitoring.md",
             ),
         ),
         "codex": SystemPromptConfig(
             template="docs/system/codex/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "codex",
                 "prompts",
                 "setup-package-monitoring.md",
             ),
             metadata={"comment": "codex prompt (frontmatter-free)"},
         ),
         "copilot": SystemPromptConfig(
             template="docs/system/copilot/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "copilot",
                 "prompts",
                 "setup-package-monitoring.prompt.md",
             ),
             frontmatter={
                 "description": "Install dependency monitoring with Dependabot and audit triggers",
                 "mode": "agent",
                 "tools": ["githubRepo", "search/codebase"],
             },
         ),
         "cursor": SystemPromptConfig(
             template="docs/system/cursor/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "cursor",
                 "commands",
                 "setup-package-monitoring.md",
             ),
         ),
         "gemini": SystemPromptConfig(
             template="docs/system/gemini/templates/command.toml.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "gemini",
                 "commands",
                 "setup-package-monitoring.toml",
             ),
             frontmatter={
                 "description": "Install dependency monitoring with Dependabot and audit triggers"
             },
         ),
         "antigravity": SystemPromptConfig(
             template="docs/system/antigravity/templates/workflow.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "antigravity",
                 "workflows",
                 "setup-package-monitoring.md",
             ),
             frontmatter={
                 "description": "Install dependency monitoring with Dependabot and audit triggers"
             },
         ),
     },
 ),
 "get-feature-primer": PromptDefinition(
     prompt_id="get-feature-primer",
     source_path=_repo_path("shared", "prompts", "get-feature-primer.md"),
     title="get-feature-primer v0.3",
     systems={
         "claude-code": SystemPromptConfig(
             template="docs/system/claude-code/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "claude-code",
                 "commands",
                 "get-feature-primer.md",
             ),
             frontmatter={"argument-hint": "<task-brief> [--target <path>]"},
         ),
         "codex": SystemPromptConfig(
             template="docs/system/codex/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "codex", "prompts", "get-feature-primer.md"
             ),
             metadata={"comment": "codex prompt (frontmatter-free)"},
         ),
         "copilot": SystemPromptConfig(
             template="docs/system/copilot/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "copilot",
                 "prompts",
                 "get-feature-primer.prompt.md",
             ),
             frontmatter={
                 "description": "Explore the codebase and produce a comprehensive analysis and todo list",
                 "mode": "agent",
                 "tools": ["githubRepo", "search/codebase", "terminal"],
             },
         ),
         "cursor": SystemPromptConfig(
             template="docs/system/cursor/templates/command.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "cursor", "commands", "get-feature-primer.md"
             ),
         ),
         "gemini": SystemPromptConfig(
             template="docs/system/gemini/templates/command.toml.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "gemini",
                 "commands",
                 "get-feature-primer.toml",
             ),
             frontmatter={
                 "description": "Explore the codebase and produce a comprehensive analysis and todo list"
             },
         ),
         "antigravity": SystemPromptConfig(
             template="docs/system/antigravity/templates/workflow.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "antigravity",
                 "workflows",
                 "get-feature-primer.md",
             ),
             frontmatter={
                 "description": "Explore the codebase and produce a comprehensive analysis and todo list"
             },
         ),
     },
 ),
 "setup-react-grab": PromptDefinition(
     prompt_id="setup-react-grab",
     source_path=_repo_path("shared", "prompts", "setup-react-grab.md"),
     title="setup-react-grab v0.1",
     systems={
         "claude-code": SystemPromptConfig(
             template="docs/system/claude-code/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "claude-code",
                 "commands",
                 "setup-react-grab.md",
             ),
             frontmatter={"argument-hint": "[--auto] [--entry-point <path>]"},
         ),
         "codex": SystemPromptConfig(
             template="docs/system/codex/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "codex", "prompts", "setup-react-grab.md"
             ),
             metadata={"comment": "codex prompt (frontmatter-free)"},
         ),
         "copilot": SystemPromptConfig(
             template="docs/system/copilot/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "copilot",
                 "prompts",
                 "setup-react-grab.prompt.md",
             ),
             frontmatter={
                 "description": "Install and configure react-grab for AI-assisted element capture",
                 "mode": "agent",
                 "tools": ["edit", "search/codebase", "terminal"],
             },
         ),
         "cursor": SystemPromptConfig(
             template="docs/system/cursor/templates/command.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "cursor", "commands", "setup-react-grab.md"
             ),
         ),
         "gemini": SystemPromptConfig(
             template="docs/system/gemini/templates/command.toml.j2",
             output_path=_repo_path(
                 ".build", "rendered", "gemini", "commands", "setup-react-grab.toml"
             ),
             frontmatter={
                 "description": "Install and configure react-grab for AI-assisted element capture"
             },
         ),
         "antigravity": SystemPromptConfig(
             template="docs/system/antigravity/templates/workflow.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "antigravity",
                 "workflows",
                 "setup-react-grab.md",
             ),
             frontmatter={
                 "description": "Install and configure react-grab for AI-assisted element capture"
             },
         ),
     },
 ),
 "setup-browser-tools": PromptDefinition(
     prompt_id="setup-browser-tools",
     source_path=_repo_path("shared", "prompts", "setup-browser-tools.md"),
     title="setup-browser-tools v0.1",
     systems={
         "claude-code": SystemPromptConfig(
             template="docs/system/claude-code/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "claude-code",
                 "commands",
                 "setup-browser-tools.md",
             ),
             frontmatter={"argument-hint": "[--auto] [--install-dir <path>]"},
         ),
         "codex": SystemPromptConfig(
             template="docs/system/codex/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "codex", "prompts", "setup-browser-tools.md"
             ),
             metadata={"comment": "codex prompt (frontmatter-free)"},
         ),
         "copilot": SystemPromptConfig(
             template="docs/system/copilot/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "copilot",
                 "prompts",
                 "setup-browser-tools.prompt.md",
             ),
             frontmatter={
                 "description": "Install Chrome DevTools Protocol automation scripts for UI testing",
                 "mode": "agent",
                 "tools": ["edit", "search/codebase", "terminal"],
             },
         ),
         "cursor": SystemPromptConfig(
             template="docs/system/cursor/templates/command.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "cursor", "commands", "setup-browser-tools.md"
             ),
         ),
         "gemini": SystemPromptConfig(
             template="docs/system/gemini/templates/command.toml.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "gemini",
                 "commands",
                 "setup-browser-tools.toml",
             ),
             frontmatter={
                 "description": "Install Chrome DevTools Protocol automation scripts for UI testing"
             },
         ),
         "antigravity": SystemPromptConfig(
             template="docs/system/antigravity/templates/workflow.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "antigravity",
                 "workflows",
                 "setup-browser-tools.md",
             ),
             frontmatter={
                 "description": "Install Chrome DevTools Protocol automation scripts for UI testing"
             },
         ),
     },
 ),
 "setup-atuin": PromptDefinition(
     prompt_id="setup-atuin",
     source_path=_repo_path("shared", "prompts", "setup-atuin.md"),
     title="setup-atuin v0.1",
     systems={
         "claude-code": SystemPromptConfig(
             template="docs/system/claude-code/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "claude-code",
                 "commands",
                 "setup-atuin.md",
             ),
             frontmatter={
                 "argument-hint": "[--auto] [--register] [--username <user>] [--email <email>]"
             },
         ),
         "codex": SystemPromptConfig(
             template="docs/system/codex/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "codex", "prompts", "setup-atuin.md"
             ),
             metadata={"comment": "codex prompt (frontmatter-free)"},
         ),
         "copilot": SystemPromptConfig(
             template="docs/system/copilot/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "copilot",
                 "prompts",
                 "setup-atuin.prompt.md",
             ),
             frontmatter={
                 "description": "Install Atuin shell history with SQLite storage and optional cloud sync",
                 "mode": "agent",
                 "tools": ["edit", "search/codebase", "terminal"],
             },
         ),
         "cursor": SystemPromptConfig(
             template="docs/system/cursor/templates/command.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "cursor", "commands", "setup-atuin.md"
             ),
         ),
         "gemini": SystemPromptConfig(
             template="docs/system/gemini/templates/command.toml.j2",
             output_path=_repo_path(
                 ".build", "rendered", "gemini", "commands", "setup-atuin.toml"
             ),
             frontmatter={
                 "description": "Install Atuin shell history with SQLite storage and optional cloud sync"
             },
         ),
         "antigravity": SystemPromptConfig(
             template="docs/system/antigravity/templates/workflow.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "antigravity", "workflows", "setup-atuin.md"
             ),
             frontmatter={
                 "description": "Install Atuin shell history with SQLite storage and optional cloud sync"
             },
         ),
     },
 ),
 "setup-mgrep": PromptDefinition(
     prompt_id="setup-mgrep",
     source_path=_repo_path("shared", "prompts", "setup-mgrep.md"),
     title="setup-mgrep v0.1",
     systems={
         "claude-code": SystemPromptConfig(
             template="docs/system/claude-code/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "claude-code",
                 "commands",
                 "setup-mgrep.md",
             ),
             frontmatter={"argument-hint": "[--auto] [--api-key <key>]"},
         ),
         "codex": SystemPromptConfig(
             template="docs/system/codex/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "codex", "prompts", "setup-mgrep.md"
             ),
             metadata={"comment": "codex prompt (frontmatter-free)"},
         ),
         "copilot": SystemPromptConfig(
             template="docs/system/copilot/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "copilot",
                 "prompts",
                 "setup-mgrep.prompt.md",
             ),
             frontmatter={
                 "description": "Install mgrep for semantic code search",
                 "mode": "agent",
                 "tools": ["terminal"],
             },
         ),
         "cursor": SystemPromptConfig(
             template="docs/system/cursor/templates/command.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "cursor", "commands", "setup-mgrep.md"
             ),
         ),
         "gemini": SystemPromptConfig(
             template="docs/system/gemini/templates/command.toml.j2",
             output_path=_repo_path(
                 ".build", "rendered", "gemini", "commands", "setup-mgrep.toml"
             ),
             frontmatter={"description": "Install mgrep for semantic code search"},
         ),
         "antigravity": SystemPromptConfig(
             template="docs/system/antigravity/templates/workflow.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "antigravity",
                 "workflows",
                 "setup-mgrep.md",
             ),
             frontmatter={"description": "Install mgrep for semantic code search"},
         ),
     },
 ),
 "setup-beads": PromptDefinition(
     prompt_id="setup-beads",
     source_path=_repo_path("shared", "prompts", "setup-beads.md"),
     title="setup-beads v0.3",
     systems={
         "claude-code": SystemPromptConfig(
             template="docs/system/claude-code/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "claude-code",
                 "commands",
                 "setup-beads.md",
             ),
             frontmatter={"argument-hint": "[--auto]"},
         ),
         "codex": SystemPromptConfig(
             template="docs/system/codex/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "codex", "prompts", "setup-beads.md"
             ),
             metadata={"comment": "codex prompt (frontmatter-free)"},
         ),
         "copilot": SystemPromptConfig(
             template="docs/system/copilot/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "copilot",
                 "prompts",
                 "setup-beads.prompt.md",
             ),
             frontmatter={
                 "description": "Install Beads (bd) for git-backed persistent task tracking",
                 "mode": "agent",
                 "tools": ["edit", "search/codebase", "terminal"],
             },
         ),
         "cursor": SystemPromptConfig(
             template="docs/system/cursor/templates/command.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "cursor", "commands", "setup-beads.md"
             ),
         ),
         "gemini": SystemPromptConfig(
             template="docs/system/gemini/templates/command.toml.j2",
             output_path=_repo_path(
                 ".build", "rendered", "gemini", "commands", "setup-beads.toml"
             ),
             frontmatter={
                 "description": "Install Beads (bd) for git-backed persistent task tracking"
             },
         ),
         "antigravity": SystemPromptConfig(
             template="docs/system/antigravity/templates/workflow.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "antigravity",
                 "workflows",
                 "setup-beads.md",
             ),
             frontmatter={
                 "description": "Install Beads (bd) for git-backed persistent task tracking"
             },
         ),
     },
 ),
 "setup-parallel-ai": PromptDefinition(
     prompt_id="setup-parallel-ai",
     source_path=_repo_path("shared", "prompts", "setup-parallel-ai.md"),
     title="setup-parallel-ai v0.1",
     systems={
         "claude-code": SystemPromptConfig(
             template="docs/system/claude-code/templates/command.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "claude-code",
                 "commands",
                 "setup-parallel-ai.md",
             ),
             frontmatter={"argument-hint": "[--auto]"},
         ),
         "codex": SystemPromptConfig(
             template="docs/system/codex/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "codex", "prompts", "setup-parallel-ai.md"
             ),
             metadata={"comment": "codex prompt (frontmatter-free)"},
         ),
         "copilot": SystemPromptConfig(
             template="docs/system/copilot/templates/prompt.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "copilot",
                 "prompts",
                 "setup-parallel-ai.prompt.md",
             ),
             frontmatter={
                 "description": "Install and configure the Parallel AI CLI for research workflows",
                 "mode": "agent",
                 "tools": ["edit", "search/codebase", "terminal"],
             },
         ),
         "cursor": SystemPromptConfig(
             template="docs/system/cursor/templates/command.md.j2",
             output_path=_repo_path(
                 ".build", "rendered", "cursor", "commands", "setup-parallel-ai.md"
             ),
         ),
         "gemini": SystemPromptConfig(
             template="docs/system/gemini/templates/command.toml.j2",
             output_path=_repo_path(
                 ".build", "rendered", "gemini", "commands", "setup-parallel-ai.toml"
             ),
             frontmatter={
                 "description": "Install and configure the Parallel AI CLI for research workflows"
             },
         ),
         "antigravity": SystemPromptConfig(
             template="docs/system/antigravity/templates/workflow.md.j2",
             output_path=_repo_path(
                 ".build",
                 "rendered",
                 "antigravity",
                 "workflows",
                 "setup-parallel-ai.md",
             ),
             frontmatter={
                 "description": "Install and configure the Parallel AI CLI for research workflows"
             },
         ),
     },
 ),
}


def list_prompts() -> Iterable[PromptDefinition]:
 return CATALOG.values()

```

File: /Users/adamjackson/LocalDev/enaible/tools/parallel/src/parallel/commands/__init__.py
```py
"""Command modules for Parallel AI CLI."""

```

File: /Users/adamjackson/LocalDev/enaible/tools/enaible/src/enaible/__main__.py
```py
"""Enaible CLI entrypoint."""

from __future__ import annotations

from .app import app

if __name__ == "__main__":
 app()

```

File: /Users/adamjackson/LocalDev/enaible/tools/enaible/src/enaible/runtime/context.py
```py
"""Workspace discovery utilities for the Enaible CLI."""

from __future__ import annotations

import importlib.resources
import os
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import typer

_SHARED_SENTINEL = Path("shared/core/base/analyzer_registry.py")
_SENTINEL_RELATIVE = Path("core/base/analyzer_registry.py")
_DEFAULT_SHARED_HOME = Path.home() / ".enaible" / "workspace" / "shared"


@dataclass(frozen=True)
class WorkspaceContext:
 """Resolved workspace paths required by the CLI."""

 repo_root: Path
 shared_root: Path
 artifacts_root: Path


def _env_path(*keys: str) -> Path | None:
 for key in keys:
     value = os.getenv(key)
     if value:
         candidate = Path(value).expanduser().resolve()
         if candidate.exists():
             return candidate
 return None


def _candidate_roots(start: Path) -> Iterable[Path]:
 yield start
 yield from start.parents

 package_relative = Path(__file__).resolve()
 yield from package_relative.parents


def _find_shared_root() -> Path | None:
 """Resolve a shared/ root containing analyzer_registry.py."""
 # Explicit env override
 env_shared = _env_path("ENAIBLE_SHARED_ROOT")
 if env_shared is not None and (env_shared / _SENTINEL_RELATIVE).exists():
     return env_shared

 # Installed workspace copy (created by installer)
 if (_DEFAULT_SHARED_HOME / _SENTINEL_RELATIVE).exists():
     return _DEFAULT_SHARED_HOME

 # Packaged resources inside the wheel (if bundled)
 try:
     pkg_shared = importlib.resources.files("enaible") / "shared"
     candidate = Path(pkg_shared)
     if (candidate / _SENTINEL_RELATIVE).exists():  # type: ignore[path-type]
         return candidate
 except Exception:  # pragma: no cover - defensive
     pass

 # Fallback to repo-relative detection later
 return None


def find_shared_root() -> Path | None:
 """Public helper to locate the shared/ workspace root."""
 return _find_shared_root()


def _find_repo_root(start: Path | None = None, require_shared: bool = True) -> Path:
 env_repo = _env_path("ENAIBLE_REPO_ROOT")
 if env_repo is not None and (
     (not require_shared) or (env_repo / _SHARED_SENTINEL).exists()
 ):
     return env_repo

 search_start = (start or Path.cwd()).resolve()
 if not require_shared:
     return search_start

 for candidate in _candidate_roots(search_start):
     if (candidate / _SHARED_SENTINEL).exists():
         return candidate

 raise typer.BadParameter(
     "Unable to locate repository root; set ENAIBLE_REPO_ROOT or run inside a checkout."
 )


def _resolve_artifacts_root(repo_root: Path) -> Path:
 artifacts = _env_path("ENAIBLE_ARTIFACTS_DIR", "ENAIBLE_ARTIFACTS_ROOT")
 if artifacts is None:
     artifacts = repo_root / ".enaible"
 artifacts.mkdir(parents=True, exist_ok=True)
 return artifacts


def load_workspace(start: Path | None = None) -> WorkspaceContext:
 """Resolve workspace paths and ensure shared modules are importable."""
 shared_root = _find_shared_root()

 # If we have a packaged/shared copy, we can relax repo discovery to the current tree.
 repo_root = _find_repo_root(start, require_shared=shared_root is None)

 if shared_root is None:
     shared_root = repo_root / "shared"
     if not shared_root.exists():
         raise typer.BadParameter(
             f"Shared analyzers folder missing at {shared_root}; repository may be incomplete."
         )

 artifacts_root = _resolve_artifacts_root(repo_root)

 if str(shared_root) not in sys.path:
     sys.path.insert(0, str(shared_root))

 existing_pythonpath = os.environ.get("PYTHONPATH", "")
 if str(shared_root) not in existing_pythonpath.split(os.pathsep):
     os.environ["PYTHONPATH"] = (
         f"{str(shared_root)}{os.pathsep}{existing_pythonpath}".strip(os.pathsep)
     )

 return WorkspaceContext(
     repo_root=repo_root,
     shared_root=shared_root,
     artifacts_root=artifacts_root,
 )

```

File: /Users/adamjackson/LocalDev/enaible/tools/parallel/src/parallel/app.py
```py
"""Root Typer application for Parallel AI CLI."""

from __future__ import annotations

import typer

app = typer.Typer(
 name="parallel",
 help="Parallel AI Web Intelligence Tools.",
 no_args_is_help=True,
)


@app.callback()
def main() -> None:
 """Parallel AI CLI - Web intelligence and research tools."""
 pass


# Import commands to register them with the app
from parallel.commands import extract, findall, search, status, task  # noqa: E402, F401

```

File: /Users/adamjackson/LocalDev/enaible/tools/enaible/tests/test_prompts_renderer.py
```py
# ruff: noqa: E402
"""Integration tests for prompt renderer."""

from __future__ import annotations

import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(PACKAGE_ROOT))

from enaible.constants import MANAGED_SENTINEL
from enaible.prompts.renderer import PromptRenderer
from enaible.runtime.context import load_workspace


def test_render_analyze_security_claude(tmp_path: Path) -> None:
 context = load_workspace()
 renderer = PromptRenderer(context)
 overrides = {"claude-code": tmp_path}
 results = renderer.render(["analyze-security"], ["claude-code"], overrides)
 assert len(results) == 1
 result = results[0]
 assert result.output_path == tmp_path / "commands" / "analyze-security.md"
 assert result.content.strip().endswith(MANAGED_SENTINEL)
 result.write()
 assert result.output_path.exists()

```

File: /Users/adamjackson/LocalDev/enaible/tools/enaible/src/enaible/prompts/lint.py
```py
from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from .utils import extract_variables

_DOLLAR_TOKEN = re.compile(r"\$[A-Z][A-Z0-9_]*")
_AT_TOKEN = re.compile(r"@([A-Z][A-Z0-9_]*)")


@dataclass(frozen=True)
class LintIssue:
 path: Path
 line: int
 message: str


def _strip_code_blocks(text: str) -> str:
 lines = text.splitlines()
 out: list[str] = []
 fenced = False
 for line in lines:
     if line.strip().startswith("```"):
         fenced = not fenced
         out.append("")
         continue
     if fenced:
         out.append("")
     else:
         # strip inline code spans as well
         out.append(re.sub(r"`[^`]*`", "", line))
 return "\n".join(out)


def lint_content(path: Path, content: str) -> list[LintIssue]:
 issues: list[LintIssue] = []
 variables, body = extract_variables(content)

 # 1) $-prefixed tokens are forbidden outside code blocks and mapping bullets
 scrubbed = _strip_code_blocks(content)
 for idx, line in enumerate(scrubbed.splitlines(), start=1):
     if line.strip().startswith(("- @", "###", "## ")):
         continue
     if _DOLLAR_TOKEN.search(line):
         issues.append(
             LintIssue(
                 path,
                 idx,
                 "Found forbidden $VAR token; use @TOKEN mapping in Variables.",
             )
         )

 # 2) Every @TOKEN in body must be declared in Variables
 declared = {v.token for v in variables}
 for idx, line in enumerate(body.splitlines(), start=1):
     for m in _AT_TOKEN.finditer(line):
         token = f"@{m.group(1)}"
         if token not in declared:
             issues.append(
                 LintIssue(path, idx, f"Undeclared token {token} used in body.")
             )

 # 3) Shape checks for variables
 for v in variables:
     if not v.token.startswith("@"):
         issues.append(
             LintIssue(path, 1, f"Variable token must start with @: {v.token}")
         )
     if v.kind == "positional" and not v.positional_index:
         issues.append(
             LintIssue(path, 1, f"Required {v.token} must map to $N index.")
         )
     if v.kind == "flag" and (not v.flag_name or not v.flag_name.startswith("--")):
         issues.append(
             LintIssue(path, 1, f"Optional {v.token} must map to a --flag.")
         )

 return issues


def lint_files(files: Iterable[Path]) -> list[LintIssue]:
 issues: list[LintIssue] = []
 for p in files:
     try:
         content = p.read_text()
     except Exception as exc:  # pragma: no cover
         issues.append(LintIssue(p, 1, f"Unable to read file: {exc}"))
         continue
     issues.extend(lint_content(p, content))
 return issues

```

File: /Users/adamjackson/LocalDev/enaible/tools/enaible/src/enaible/commands/__init__.py
```py
"""Command registrations for the Enaible CLI."""

from __future__ import annotations

import importlib
from collections.abc import Iterable

# Explicit command modules to import for side effects.
_COMMAND_MODULES: Iterable[str] = (
 "enaible.commands.root",
 "enaible.commands.analyzers",
 "enaible.commands.prompts",
 "enaible.commands.skills",
 "enaible.commands.install",
 "enaible.commands.ci",
 "enaible.commands.setup",
)


def _register_commands() -> None:
 for module_name in _COMMAND_MODULES:
     importlib.import_module(module_name)


_register_commands()

```

File: /Users/adamjackson/LocalDev/enaible/tools/parallel/src/parallel/commands/search.py
```py
"""Search command for Parallel AI."""

from __future__ import annotations

import json
from typing import Annotated

import typer

from parallel.app import app
from parallel.client import api_request


@app.command()
def search(
 objective: Annotated[str, typer.Argument(help="Natural language search objective")],
 query: Annotated[
     list[str] | None,
     typer.Option("-q", "--query", help="Search queries (repeatable)"),
 ] = None,
 max_results: Annotated[int, typer.Option(help="Maximum results to return")] = 10,
 output_format: Annotated[
     str,
     typer.Option("--format", help="Output format"),
 ] = "json",
) -> None:
 """Search the web with a natural language objective.

 Examples
 --------
     parallel search "latest AI research on RAG"
     parallel search "climate change news" -q "climate 2024" -q "global warming"
 """
 queries = list(query) if query else [objective]

 payload = {
     "objective": objective,
     "search_queries": queries,
     "max_results": max_results,
     "excerpts": {"max_chars_per_result": 10000},
 }

 try:
     result = api_request("POST", "/v1beta/search", json=payload)

     if output_format == "markdown":
         _print_search_markdown(result)
     else:
         print(json.dumps(result, indent=2))

 except Exception as e:
     print(f"Error: {e}", file=typer.get_text_stream("stderr"))
     raise typer.Exit(1) from None


def _print_search_markdown(result: dict) -> None:
 """Print search results in markdown format."""
 print("# Search Results\n")
 print(f"**Search ID:** {result.get('search_id', 'N/A')}\n")

 results = result.get("results", [])
 if not results:
     print("No results found.")
     return

 for i, item in enumerate(results, 1):
     print(f"## {i}. {item.get('title', 'Untitled')}\n")
     print(f"**URL:** {item.get('url', 'N/A')}")
     if item.get("publish_date"):
         print(f"**Published:** {item['publish_date']}")
     print()
     excerpts = item.get("excerpts", [])
     if excerpts:
         print("### Excerpts\n")
         for excerpt in excerpts:
             print(f"> {excerpt}\n")
     print("---\n")

```

File: /Users/adamjackson/LocalDev/enaible/docs/system/claude-code/slash-command.md
```md
<!-- template format for claude-code custom slash command -->
<!-- Docs: https://docs.claude.com/en/docs/claude-code/slash-commands -->

<!--
Claude specific items
Rules:
 User level ~/.claude/CLAUDE.md
 Project level ./CLAUDE.md
Directories:
 User level ~/.claude
 Project level ./.claude
Settings:
 User level  ~/.claude/settings.json
 Project level ./.claude/settings.local.json
Mcp config:
 User level ~/.claude.json

FRONTMATTER (define these in real YAML frontmatter when instantiating):
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git log:*), Bash(git diff:*); Read(./path|glob); Write(./path|glob); Edit(./path|glob); MultiEdit(./path|glob); NotebookEdit(./path|glob); NotebookRead(./path|glob); Grep; Glob; Task; TodoWrite; WebFetch; WebSearch; Write; MCP tools by exact name: mcp__server, mcp__server__tool (no wildcards)
argument-hint: [type] [scope] [message]
description: One-line summary for /help
model: claude-3-5-haiku-20241022 (inherits if omitted)
disable-model-invocation: true | false (default false)

ARGUMENTS (expansion rules):
$1..$9: expand to first nine positional args
$ARGUMENTS: expands to all args joined by a single space
$$: preserved literally (emit a dollar sign)
quoted: wrap an argument in double quotes to include spaces

TOOLS (referenceable in allowed-tools):
list: Bash | Edit | Glob | Grep | MultiEdit | NotebookEdit | NotebookRead | Read | Task | TodoWrite | WebFetch | WebSearch | Write
mcp rules: mcp__github | mcp__github__get_issue (no wildcards)

SHELL OUTPUT INJECTION:
!`<bash>` injects command output into context (requires a matching Bash(...) rule in allowed-tools)

FILE REFERENCES:
@path includes file or directory contents in context (e.g., @src, @README.md)
-->

---

allowed-tools:
argument-hint: [type] [scope] [message]
description: One-line summary for /help
model: claude-3-5-haiku-20241022 (inherits if omitted)

---

<prompt-body>

```

File: /Users/adamjackson/LocalDev/enaible/tools/enaible/src/enaible/commands/analyzers.py
```py
"""Analyzer command group for the Enaible CLI."""

from __future__ import annotations

import json
import os
import time
from collections.abc import Iterable
from pathlib import Path
from typing import TYPE_CHECKING, Any

import typer

from ..app import app
from ..models.results import AnalysisResultContext, AnalyzerRunResponse
from ..runtime.context import WorkspaceContext, load_workspace

if TYPE_CHECKING:  # pragma: no cover
 pass


_analyzers_app = typer.Typer(help="Run and inspect registered analyzers.")
app.add_typer(_analyzers_app, name="analyzers")


_registry_bootstrapped = False


def _ensure_registry_loaded(context: WorkspaceContext) -> None:
 global _registry_bootstrapped
 if _registry_bootstrapped:
     return

 # Import bootstrap module which registers analyzers via side effects.
 __import__("core.base.registry_bootstrap")
 _registry_bootstrapped = True


def _resolve_analyzer_registry() -> Any:
 from core.base import AnalyzerRegistry

 return AnalyzerRegistry


def _create_config(
 *,
 target: Path,
 min_severity: str,
 summary_mode: bool,
 max_files: int | None,
 output_format: str,
 exclude_globs: Iterable[str],
) -> Any:
 from core.base import create_analyzer_config

 config = create_analyzer_config(
     target_path=str(target),
     min_severity=min_severity,
     summary_mode=summary_mode,
     output_format=output_format,
 )

 if max_files is not None:
     config.max_files = max_files
 config.exclude_globs.update(exclude_globs)
 return config


def _collect_gitignore_patterns(search_root: Path) -> list[str]:
 """Gather gitignore patterns walking up from the search root."""
 patterns: list[str] = []
 seen_files: set[Path] = set()

 current = search_root
 if not current.exists():
     current = Path.cwd()
 elif current.is_file():
     current = current.parent

 for directory in [current, *list(current.parents)]:
     candidate = directory / ".gitignore"
     if candidate in seen_files or not candidate.is_file():
         continue

     try:
         lines = candidate.read_text(encoding="utf-8").splitlines()
     except OSError:
         continue

     for line in lines:
         stripped = line.strip()
         if not stripped or stripped.startswith("#"):
             continue
         patterns.append(stripped)

     seen_files.add(candidate)

 return patterns


def _emit_json(payload: dict[str, Any], out: Path | None) -> None:
 rendered = json.dumps(payload, indent=2)
 if out is not None:
     out.parent.mkdir(parents=True, exist_ok=True)
     out.write_text(rendered)
 else:
     typer.echo(rendered)


@_analyzers_app.command("run")
def analyzers_run(
 tool: str = typer.Argument(
     ..., help="Analyzer registry key (e.g. quality:lizard)."
 ),
 target: Path = typer.Option(Path("."), "--target", "-t", help="Path to analyze."),
 json_output: bool = typer.Option(
     True,
     "--json/--no-json",
     help="Emit normalized JSON payload (default).",
 ),
 out: Path | None = typer.Option(
     None,
     "--out",
     "-o",
     help="Optional file to write result JSON to.",
 ),
 min_severity: str = typer.Option(
     "high",
     "--min-severity",
     help="Minimum severity to include in findings.",
     show_default=True,
 ),
 max_files: int | None = typer.Option(
     None,
     "--max-files",
     help="Limit the number of files processed.",
 ),
 summary_mode: bool = typer.Option(
     False,
     "--summary",
     help="Return a severity summary only (omits full findings).",
 ),
 verbose: bool = typer.Option(
     False, "--verbose", help="Enable verbose analyzer logs."
 ),
 no_external: bool = typer.Option(
     False,
     "--no-external",
     help="Disable analyzer features requiring external dependencies (sets ENAIBLE_DISABLE_EXTERNAL=1).",
 ),
 exclude_glob: list[str] = typer.Option(
     [],
     "--exclude",
     "-x",
     help="Additional glob patterns to exclude (repeatable).",
 ),
) -> None:
 """Run a registered analyzer and emit normalized results."""
 context = load_workspace()
 _ensure_registry_loaded(context)

 registry = _resolve_analyzer_registry()

 if no_external:
     os.environ.setdefault("ENAIBLE_DISABLE_EXTERNAL", "1")

 min_severity = min_severity.lower()
 normalized_excludes = [
     pattern.strip() for pattern in exclude_glob if pattern.strip()
 ]

 gitignore_patterns = _collect_gitignore_patterns(target)

 config = _create_config(
     target=target,
     min_severity=min_severity,
     summary_mode=summary_mode,
     max_files=max_files,
     output_format="json" if json_output else "console",
     exclude_globs=normalized_excludes,
 )

 config.gitignore_patterns = gitignore_patterns

 try:
     analyzer = registry.create(tool, config=config)
 except KeyError as exc:
     raise typer.BadParameter(str(exc)) from exc

 if hasattr(analyzer, "verbose"):
     analyzer.verbose = bool(verbose)

 started = time.time()
 result = analyzer.analyze(str(target))
 finished = time.time()

 ctx = AnalysisResultContext(
     tool=tool,
     result=result,
     started_at=started,
     finished_at=finished,
     summary_mode=summary_mode,
     min_severity=min_severity,
 )
 response = AnalyzerRunResponse.from_analysis_result(ctx)

 payload = response.to_dict()

 if json_output:
     _emit_json(payload, out)
 else:
     # Analyzer handles console output internally; only write JSON when requested.
     if out is not None:
         _emit_json(payload, out)

 if len(response.findings) >= 200:
     tip = (
         "Hint: If some findings look third-party or generated, rerun with "
         "`--exclude <glob>` to filter those directories."
     )
     typer.secho(tip, err=True)

 raise typer.Exit(code=response.exit_code)


@_analyzers_app.command("list")
def analyzers_list(
 json_output: bool = typer.Option(
     True, "--json/--no-json", help="Emit JSON output."
 ),
) -> None:
 """List all registered analyzers."""
 context = load_workspace()
 _ensure_registry_loaded(context)
 registry = _resolve_analyzer_registry()

 analyzers = []
 for name, analyzer_cls in sorted(registry._registry.items()):  # type: ignore[attr-defined]
     analyzers.append(
         {
             "tool": name,
             "doc": (analyzer_cls.__doc__ or "").strip(),
             "module": f"{analyzer_cls.__module__}.{analyzer_cls.__name__}",
         }
     )

 if json_output:
     _emit_json({"analyzers": analyzers}, None)
 else:
     for entry in analyzers:
         typer.echo(f"{entry['tool']}: {entry['module']}")

```

File: /Users/adamjackson/LocalDev/enaible/tools/parallel/pyproject.toml
```toml
[project]
name = "parallel"
version = "0.1.0"
description = "CLI for Parallel AI Web Intelligence"
requires-python = ">=3.12,<3.13"
dependencies = [
 "typer>=0.18,<0.19",
 "httpx>=0.27,<0.28",
]

[dependency-groups]
dev = [
 "pytest>=8.3,<9.0",
 "pytest-cov>=5.0,<6.0",
 "mypy>=1.11,<2.0",
 "ruff>=0.5,<0.6",
]

[project.scripts]
parallel = "parallel.__main__:app"

[tool.uv]
package = true

[tool.ruff]
target-version = "py312"
line-length = 100

[tool.mypy]
python_version = "3.12"
strict = true
mypy_path = ["src"]
namespace_packages = true
packages = ["parallel"]

```

File: /Users/adamjackson/LocalDev/enaible/tools/parallel/src/parallel/__main__.py
```py
"""CLI entry point for Parallel AI tools."""

from parallel.app import app

if __name__ == "__main__":
 app()

```

File: /Users/adamjackson/LocalDev/enaible/tools/parallel/src/parallel/commands/extract.py
```py
"""Extract command for Parallel AI."""

from __future__ import annotations

import json
from typing import Annotated

import typer

from parallel.app import app
from parallel.client import api_request


@app.command()
def extract(
 url: Annotated[str, typer.Argument(help="URL to extract content from")],
 objective: Annotated[
     str | None,
     typer.Option("--objective", "-o", help="What to focus on when extracting"),
 ] = None,
 full_content: Annotated[
     bool,
     typer.Option("--full-content", "-f", help="Return full page content"),
 ] = False,
 output_format: Annotated[
     str,
     typer.Option("--format", help="Output format"),
 ] = "json",
) -> None:
 """Extract content from a URL.

 Examples
 --------
     parallel extract https://example.com
     parallel extract https://example.com --objective "key findings"
     parallel extract https://example.com --full-content
 """
 payload: dict = {
     "urls": [url],
     "excerpts": not full_content,
     "full_content": full_content,
 }
 if objective:
     payload["objective"] = objective

 try:
     result = api_request("POST", "/v1beta/extract", json=payload)

     if output_format == "markdown":
         _print_extract_markdown(result)
     else:
         print(json.dumps(result, indent=2))

 except Exception as e:
     print(f"Error: {e}", file=typer.get_text_stream("stderr"))
     raise typer.Exit(1) from None


def _print_extract_markdown(result: dict) -> None:
 """Print extraction results in markdown format."""
 print("# Extraction Results\n")
 print(f"**Extract ID:** {result.get('extract_id', 'N/A')}\n")

 results = result.get("results", [])
 if not results:
     print("No content extracted.")
     return

 for item in results:
     print(f"## {item.get('title', 'Untitled')}\n")
     print(f"**URL:** {item.get('url', 'N/A')}")
     if item.get("publish_date"):
         print(f"**Published:** {item['publish_date']}")
     print()

     if item.get("full_content"):
         print("### Content\n")
         print(item["full_content"])
     elif item.get("excerpts"):
         print("### Excerpts\n")
         for excerpt in item["excerpts"]:
             print(f"> {excerpt}\n")
     print("---\n")

```

File: /Users/adamjackson/LocalDev/enaible/tools/parallel/src/parallel/commands/status.py
```py
"""Status and result commands for Parallel AI."""

from __future__ import annotations

import json
from typing import Annotated

import typer

from parallel.app import app
from parallel.client import api_request


@app.command()
def status(
 run_id: Annotated[str, typer.Argument(help="Task run_id or FindAll findall_id")],
 run_type: Annotated[
     str | None,
     typer.Option(
         "--type",
         "-t",
         help="Run type: task or findall (auto-detected if not specified)",
     ),
 ] = None,
) -> None:
 """Check the status of an async operation.

 Examples
 --------
     parallel status trun_abc123
     parallel status fa_xyz789 --type findall
 """
 # Auto-detect type from ID prefix
 if run_type is None:
     if run_id.startswith("trun_"):
         run_type = "task"
     elif run_id.startswith("fa_"):
         run_type = "findall"
     else:
         print(
             "Error: Could not auto-detect run type. Please specify --type task or --type findall"
         )
         raise typer.Exit(1)

 try:
     if run_type == "task":
         result = api_request("GET", f"/v1/tasks/runs/{run_id}", use_beta=False)
     else:
         result = api_request("GET", f"/v1beta/findall/runs/{run_id}")

     print(json.dumps(result, indent=2))

 except Exception as e:
     print(f"Error: {e}", file=typer.get_text_stream("stderr"))
     raise typer.Exit(1) from None


@app.command()
def result(
 run_id: Annotated[str, typer.Argument(help="Task run_id or FindAll findall_id")],
 run_type: Annotated[
     str | None,
     typer.Option(
         "--type",
         "-t",
         help="Run type: task or findall (auto-detected if not specified)",
     ),
 ] = None,
 output_file: Annotated[
     str | None,
     typer.Option("--output", "-o", help="Write results to file"),
 ] = None,
 output_format: Annotated[
     str,
     typer.Option("--format", help="Output format"),
 ] = "json",
) -> None:
 """Fetch results of a completed async operation.

 For tasks, this blocks until completion and returns the enriched data.
 For findall, this returns the matched candidates.

 Examples
 --------
     parallel result trun_abc123
     parallel result fa_xyz789 --type findall --output results.json
 """
 # Auto-detect type from ID prefix
 if run_type is None:
     if run_id.startswith("trun_"):
         run_type = "task"
     elif run_id.startswith("fa_"):
         run_type = "findall"
     else:
         print(
             "Error: Could not auto-detect run type. Please specify --type task or --type findall"
         )
         raise typer.Exit(1)

 try:
     if run_type == "task":
         # Task result endpoint blocks until completion
         result = api_request(
             "GET", f"/v1/tasks/runs/{run_id}/result", use_beta=False
         )
     else:
         # FindAll returns candidates
         result = api_request("GET", f"/v1beta/findall/runs/{run_id}/candidates")

     output = json.dumps(result, indent=2)

     if output_file:
         with open(output_file, "w") as f:
             f.write(output)
         print(f"Results written to {output_file}")
     else:
         if output_format == "markdown" and run_type == "task":
             _print_task_result_markdown(result)
         elif output_format == "markdown" and run_type == "findall":
             _print_findall_result_markdown(result)
         else:
             print(output)

 except Exception as e:
     print(f"Error: {e}", file=typer.get_text_stream("stderr"))
     raise typer.Exit(1) from None


def _print_task_result_markdown(result: dict) -> None:
 """Print task results in markdown format."""
 print("# Task Result\n")

 run_info = result.get("run", {})
 if run_info:
     print(f"**Status:** {run_info.get('status', 'N/A')}\n")

 output = result.get("output", {})
 if output:
     content = output.get("content", {})
     print("## Output\n")
     print(json.dumps(content, indent=2))

     basis = output.get("basis", [])
     if basis:
         print("\n## Basis & Citations\n")
         for item in basis:
             field = item.get("field", "unknown")
             confidence = item.get("confidence", "N/A")
             reasoning = item.get("reasoning", "")
             print(f"### {field} (confidence: {confidence})\n")
             if reasoning:
                 print(f"{reasoning}\n")
             citations = item.get("citations", [])
             if citations:
                 print("**Sources:**")
                 for cite in citations:
                     print(f"- [{cite.get('title', 'N/A')}]({cite.get('url', '')})")
                 print()


def _print_findall_result_markdown(result: dict) -> None:
 """Print findall results in markdown format."""
 print("# FindAll Results\n")

 candidates = result.get("candidates", [])
 if not candidates:
     print("No candidates found.")
     return

 print(f"**Total Candidates:** {len(candidates)}\n")

 for i, candidate in enumerate(candidates, 1):
     name = candidate.get("name", f"Candidate {i}")
     print(f"## {i}. {name}\n")

     # Print all fields except name
     for key, value in candidate.items():
         if key != "name":
             print(f"- **{key}:** {value}")
     print()

```

File: /Users/adamjackson/LocalDev/enaible/tools/enaible/src/enaible/commands/root.py
```py
"""Root command definitions for Enaible CLI."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from enum import Enum
from pathlib import Path

import typer

from ..app import app
from ..runtime.context import find_shared_root, load_workspace


class ContextPlatform(str, Enum):
 """Supported context capture platforms."""

 CLAUDE = "claude"
 CODEX = "codex"


class OutputFormat(str, Enum):
 """Output formats supported by context capture scripts."""

 JSON = "json"
 TEXT = "text"


def _env_with_shared(shared_root: Path) -> dict[str, str]:
 """Return environment mapping that ensures shared/ is importable."""
 env = os.environ.copy()
 pythonpath = env.get("PYTHONPATH", "")
 if pythonpath:
     env["PYTHONPATH"] = f"{shared_root}{os.pathsep}{pythonpath}"
 else:
     env["PYTHONPATH"] = str(shared_root)
 return env


@app.command("context_capture")
def context_capture(
 platform: ContextPlatform = typer.Option(
     ...,
     "--platform",
     "-p",
     help="Target platform to capture context for.",
 ),
 days: int = typer.Option(2, help="Number of days to look back."),
 uuid: str | None = typer.Option(None, help="Filter to a specific session UUID."),
 search_term: str | None = typer.Option(
     None, help="Search for sessions containing this term."
 ),
 semantic_variations: str | None = typer.Option(
     None,
     help="JSON string describing semantic variations for search_term.",
 ),
 project_root: Path | None = typer.Option(
     None,
     help="Absolute path to project root for scoping. Defaults to current directory.",
 ),
 include_all_projects: bool = typer.Option(
     False, help="Include sessions across all projects instead of scoping to one."
 ),
 output_format: OutputFormat = typer.Option(
     OutputFormat.JSON, "--output-format", case_sensitive=False
 ),
) -> None:
 """Capture session context for Claude or Codex."""
 workspace = load_workspace()
 script_map = {
     ContextPlatform.CLAUDE: workspace.repo_root
     / "shared"
     / "context"
     / "context_bundle_capture_claude.py",
     ContextPlatform.CODEX: workspace.repo_root
     / "shared"
     / "context"
     / "context_bundle_capture_codex.py",
 }

 script_path = script_map[platform]
 if not script_path.exists():
     typer.echo(f"Context capture script not found at {script_path}", err=True)
     raise typer.Exit(code=1)

 args: list[str] = ["--days", str(days), "--output-format", output_format.value]
 if uuid:
     args.extend(["--uuid", uuid])
 if search_term:
     args.extend(["--search-term", search_term])
 if semantic_variations:
     args.extend(["--semantic-variations", semantic_variations])
 if project_root:
     args.extend(["--project-root", str(project_root)])
 if include_all_projects:
     args.append("--include-all-projects")

 env = _env_with_shared(workspace.shared_root)
 proc = subprocess.run([sys.executable, str(script_path), *args], env=env)
 raise typer.Exit(code=proc.returncode)


@app.command("docs_scrape")
def docs_scrape(
 url: str = typer.Argument(..., help="URL to scrape."),
 out: Path = typer.Argument(..., help="Destination markdown file."),
 title: str | None = typer.Option(None, "--title", help="Override document title."),
 verbose: bool = typer.Option(
     False, "--verbose", "-v", help="Enable verbose logging for the scraper."
 ),
) -> None:
 """Scrape documentation and save as markdown using the shared web scraper."""
 workspace = load_workspace()
 env = _env_with_shared(workspace.shared_root)

 cmd = [sys.executable, "-m", "web_scraper.cli"]
 if verbose:
     cmd.append("-v")
 cmd.extend(["save-as-markdown", url, str(out)])
 if title:
     cmd.extend(["--title", title])

 proc = subprocess.run(cmd, env=env)
 raise typer.Exit(code=proc.returncode)


@app.command("version")
def version() -> None:
 """Display CLI version information."""
 from importlib import metadata

 try:
     cli_version = metadata.version("enaible")
 except metadata.PackageNotFoundError:
     typer.echo("enaible (editable install not detected)", err=True)
     raise typer.Exit(code=1) from None
 else:
     typer.echo(f"enaible {cli_version}")


@app.command("doctor")
def doctor(
 json_output: bool = typer.Option(
     False,
     "--json/--no-json",
     help="Emit diagnostics as JSON instead of human-readable text.",
 ),
) -> None:
 """Run basic environment diagnostics."""
 from importlib import metadata

 report: dict[str, object] = {
     "python": platform.python_version(),
     "typer_version": metadata.version("typer"),
     "enaible_version": metadata.version("enaible"),
     "checks": {},
     "errors": [],
 }
 exit_code = 0

 checks: dict[str, bool] = report["checks"]  # type: ignore[assignment]

 shared_root = find_shared_root()
 if shared_root is None:
     checks["shared_workspace"] = False
     checks["analyzer_registry"] = False
     report["errors"].append(
         "Shared workspace not found. Re-run `enaible install ... --sync-shared`."
     )
     exit_code = 1
 else:
     checks["shared_workspace"] = True
     report["shared_root"] = str(shared_root)
     registry_stub = shared_root / "core" / "base" / "analyzer_registry.py"
     registry_exists = registry_stub.exists()
     checks["analyzer_registry"] = registry_exists
     if not registry_exists:
         report["errors"].append(
             "Analyzer registry module not found under shared/core/base."
         )
         exit_code = 1

 try:
     context = load_workspace()
 except typer.BadParameter as exc:  # pragma: no cover - defensive
     checks["workspace"] = False
     report["errors"].append(str(exc))
     context = None  # type: ignore[assignment]
 else:
     checks["workspace"] = True
     report["repo_root"] = str(context.repo_root)

 if context is not None:
     schema_path = context.repo_root / ".enaible" / "schema.json"
     schema_exists = schema_path.exists()
     checks["schema_exists"] = schema_exists

 if json_output:
     typer.echo(json.dumps(report, indent=2, sort_keys=True))
 else:
     typer.echo("Enaible Diagnostics")
     if "repo_root" in report:
         typer.echo(f"  Repo root: {report['repo_root']}")
     typer.echo(f"  Python: {report['python']}")
     typer.echo(f"  Typer: {report['typer_version']}")
     for name, passed in checks.items():
         status = "OK" if passed else "FAIL"
         typer.echo(f"  {name.replace('_', ' ').title()}: {status}")
     if report.get("errors"):
         typer.echo("Errors:")
         for err in report["errors"]:
             typer.echo(f"  - {err}")

 raise typer.Exit(code=exit_code)

```

File: /Users/adamjackson/LocalDev/enaible/systems/copilot/rules/global.copilot.rules.md
```md
## **CRITICAL** Must follow Design Principles

- **ALWAYS** establish a working base project before beginging bespoke configuration and feature development, this means confirmed successful compile and run of the dev server with quality gates established - this is used as the baseline first commit.
- **ALWAYS** commit to git after the logical conclusion of task steps, use a frequent, atomic commit pattern to establish safe check points of known good implementation that can be reverted to if need.
- **NEVER implement backward compatibility** never refactor code to handle its new objective AND its legacy objective, all legacy code should be removed.
- **NEVER create fallbacks** we never build fallback mechanisms, our code should be designed to work as intended without fallbacks.
- **ALWAY KISS - Keep it simple stupid** only action what the user has requested and no more, never over engineer, if you dont have approval for expanding the scope of a task you must ask the user first.
- **ALWAYS minimise complexity** keep code Cyclomatic Complexity under 10
- **ALWAYS prefer established libraries over bespoke code** only produce bespoke code if no established library
- **ALWAYS use appropriate symbol naming when refactoring code**: When refactoring do not add prefixes/suffixes like "Refactored", "Updated", "New", or "V2" to symbol names to indicate changes.
- **ALWAYS Align UI style changes to shadcn/Tailwind/Radix patterns and Lucide assets**: For your UI stack implementation avoid bespoke classes and direct style hardcoding to objects.

## **CRITICAL** Must follow Behaviour Rules - how you carry out actions

### Security Requirements

- **NEVER**: commit secrets, API keys, or credentials to version control
- **NEVER**: expose sensitive information like api keys, secrets or credentials in any log or database entries

### Prohibit Reward Hacking

- **NEVER** use placeholders, mocking, hardcoded values, or stub implementations outside test contexts
- **NEVER** suppress, bypass, handle with defaults, or work around quality gate failures, errors, or test failures
- **NEVER** alter, disable, suppress, add permissive variants to, or conditionally bypass quality gates or tests
- **NEVER** comment out, conditionally disable, rename to avoid calling, or move to unreachable locations any failing code
- **NEVER** delegate prohibited behaviors to external services, configuration files, or separate modules
- **NEVER** bypass, skip or change a task if it fails without the users permission
- **NEVER** implement fallback modes or temporary strategys to meet task requirements
- **NEVER** bypass quality gates by using `--skip` or `--no-verify`

## **CRITICAL** Development workflow tools

If the user types --help list out bulleted list of all the available tools below, single line per tool with short description and how to invoke

### When you need to execute Long-Running Tasks

If `--tmux` is included in a users request or a request requires long runnning execution (like a dev server) or we want to defence against a bash task that may stall, you **must** use tmux.

- Run long-running services in named tmux sessions: `tmux new-session -d -s <name> '<command>'`
- Check existing: `tmux list-sessions`, Attach: `tmux attach -t <name>`, Logs: `tmux capture-pane -p -S -200 -t <name>`
- Wrap uncertain/long commands in tmux to prevent blocking
- Kill session: `tmux kill-session -t <name>`

```

File: /Users/adamjackson/LocalDev/enaible/docs/system/cursor/rules.md
```md
# Cursor Rules Format

Cursor IDE uses `.mdc` files (MDC = Markdown with Context) for storing custom rules and instructions.

## File Structure

Cursor rules are stored in `.cursor/rules/` and use XML-style wrapper tags:

```markdown
<!-- generated: enaible -->

<rule_category>

# Title

Content goes here...
</rule_category>
```

## Rule Categories

Common rule categories include:

- `<coding>` - General coding practices and standards
- `<security>` - Security-focused rules and guidelines
- `<quality>` - Code quality and refactoring guidance
- `<performance>` - Performance optimization rules
- `<debugging>` - Debugging and troubleshooting instructions
- `<planning>` - Planning and design rules
- `<documentation>` - Documentation standards
- `<development>` - Development workflow rules
- `<configuration>` - Configuration management
- `<scaffolding>` - Project scaffolding and setup
- `<analysis>` - Code analysis guidelines

## Variable Handling

Unlike other AI coding systems, Cursor rules are **static instructions** and do not support runtime variables. All `@TOKEN` placeholders from source prompts are removed or replaced with literal values during rendering.

## Managed Files

Files with the `<!-- generated: enaible -->` sentinel are automatically managed by the enaible CLI. Do not edit these files directly - instead, modify the source prompts in `shared/prompts/` and re-render.

## Rendering Cursor Rules

```bash
# Render all prompts for Cursor
uv run enaible prompts render --system cursor

# Render specific prompt
uv run enaible prompts render --prompt analyze-security --system cursor
```

```

File: /Users/adamjackson/LocalDev/enaible/shared/skills/codify-pr-reviews/scripts/stack_analysis.py
```py
#!/usr/bin/env python3
"""Detect stack signals and generate red-flag patterns."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


def load_defaults(config_path: Path) -> dict[str, Any]:
 if not config_path.exists():
     return {}
 return json.loads(config_path.read_text(encoding="utf-8"))


def read_requirements(path: Path) -> set[str]:
 packages: set[str] = set()
 if not path.exists():
     return packages
 for line in path.read_text(encoding="utf-8").splitlines():
     stripped = line.strip()
     if not stripped or stripped.startswith("#"):
         continue
     name = re.split(r"[<>=!~]", stripped, maxsplit=1)[0].strip()
     if name:
         packages.add(name.lower())
 return packages


def read_package_json(path: Path) -> set[str]:
 packages: set[str] = set()
 if not path.exists():
     return packages
 data = json.loads(path.read_text(encoding="utf-8"))
 for key in ("dependencies", "devDependencies", "peerDependencies"):
     deps = data.get(key, {}) or {}
     for name in deps.keys():
         packages.add(name.lower())
 return packages


def scan_extensions(root: Path, extensions: set[str], limit: int = 500) -> bool:
 count = 0
 for path in root.rglob("*"):
     if path.is_file() and path.suffix.lower() in extensions:
         return True
     count += 1
     if count >= limit:
         break
 return False


def detect_stack(project_root: Path) -> dict[str, str]:
 deps = read_package_json(project_root / "package.json")
 py_deps = read_requirements(project_root / "requirements.txt")
 go_mod = (project_root / "go.mod").read_text(encoding="utf-8") if (project_root / "go.mod").exists() else ""
 pom = (project_root / "pom.xml").exists()
 gemfile = (project_root / "Gemfile").exists()

 stack: dict[str, str] = {}

 backend_map = {
     "express": "Express.js",
     "fastify": "Fastify",
     "@nestjs/core": "NestJS",
     "koa": "Koa",
     "hapi": "Hapi",
 }
 for pkg, name in backend_map.items():
     if pkg in deps:
         stack["backend"] = name
         break

 if "backend" not in stack:
     if "fastapi" in py_deps:
         stack["backend"] = "FastAPI"
     elif "django" in py_deps:
         stack["backend"] = "Django"
     elif "flask" in py_deps:
         stack["backend"] = "Flask"
     elif "gin" in go_mod:
         stack["backend"] = "Gin"
     elif "echo" in go_mod:
         stack["backend"] = "Echo"
     elif pom:
         stack["backend"] = "Spring Boot"
     elif gemfile:
         stack["backend"] = "Rails"

 frontend_map = {
     "react": "React",
     "vue": "Vue",
     "@angular/core": "Angular",
     "svelte": "Svelte",
 }
 for pkg, name in frontend_map.items():
     if pkg in deps:
         stack["frontend"] = name
         break

 if "next" in deps:
     stack["frontend"] = "Next.js (React)"
 if "nuxt" in deps:
     stack["frontend"] = "Nuxt (Vue)"

 database_map = {
     "sqlite3": "SQLite",
     "better-sqlite3": "SQLite",
     "pg": "PostgreSQL",
     "postgres": "PostgreSQL",
     "mysql": "MySQL",
     "mysql2": "MySQL",
     "mongodb": "MongoDB",
 }
 for pkg, name in database_map.items():
     if pkg in deps:
         stack["database"] = name
         break

 if "prisma" in deps:
     stack["database"] = f"{stack.get('database', 'Database')} (via Prisma)"
 if "typeorm" in deps:
     stack["database"] = f"{stack.get('database', 'Database')} (via TypeORM)"
 if "sequelize" in deps:
     stack["database"] = f"{stack.get('database', 'Database')} (via Sequelize)"

 if (project_root / "tsconfig.json").exists() or scan_extensions(project_root, {".ts", ".tsx"}):
     stack["language"] = "TypeScript"
 elif scan_extensions(project_root, {".py"}):
     stack["language"] = "Python"
 elif scan_extensions(project_root, {".go"}):
     stack["language"] = "Go"
 elif scan_extensions(project_root, {".java"}):
     stack["language"] = "Java"
 elif scan_extensions(project_root, {".rb"}):
     stack["language"] = "Ruby"
 elif scan_extensions(project_root, {".cs"}):
     stack["language"] = "C#"
 else:
     stack["language"] = "JavaScript"

 return stack


def build_red_flags(stack: dict[str, str]) -> list[str]:
 flags: list[str] = [
     "hardcoded password",
     "hardcoded secret",
     "hardcoded api key",
     "sql injection",
     "todo: security",
     "fixme: security",
 ]

 backend = stack.get("backend", "").lower()
 frontend = stack.get("frontend", "").lower()
 language = stack.get("language", "").lower()

 if "express" in backend or "fastify" in backend or "nestjs" in backend:
     flags.extend(["bcrypt sync", "eval(", "new Function("])

 if "react" in frontend:
     flags.extend(["dangerouslySetInnerHTML", "key={index}", "missing key prop"])

 if "python" in language:
     flags.extend(["pickle.loads", "eval(", "exec("])

 if "typescript" in language:
     flags.extend(["any type", "as any", "@ts-ignore"])

 return sorted({flag.lower() for flag in flags})


def main() -> int:
 parser = argparse.ArgumentParser(description="Detect project stack and generate red flags.")
 parser.add_argument("--project-root", default=".")
 parser.add_argument("--output-path", required=True)
 parser.add_argument("--force-refresh", action="store_true")
 parser.add_argument("--config", default=str(Path(__file__).resolve().parents[1] / "config" / "defaults.json"))
 args = parser.parse_args()

 project_root = Path(args.project_root).resolve()
 output_path = Path(args.output_path).resolve()

 if output_path.exists() and not args.force_refresh:
     print(f"Using existing red flags at {output_path}")
     return 0

 defaults = load_defaults(Path(args.config))

 stack = detect_stack(project_root)
 red_flags = build_red_flags(stack)

 payload: dict[str, Any] = {
     "generatedAt": datetime.utcnow().isoformat() + "Z",
     "projectRoot": str(project_root),
     "stack": stack,
     "redFlags": red_flags,
     "defaults": {
         "defaultDaysBack": defaults.get("defaultDaysBack"),
         "defaultMinOccurrences": defaults.get("defaultMinOccurrences"),
         "defaultMinCommentLength": defaults.get("defaultMinCommentLength"),
     },
 }

 output_path.parent.mkdir(parents=True, exist_ok=True)
 output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
 print(f"Wrote red flags to {output_path}")
 return 0


if __name__ == "__main__":
 raise SystemExit(main())

```

File: /Users/adamjackson/LocalDev/enaible/.github/workflows/package-audit.yml
```yml
name: Package Audit

on:
pull_request:
 paths:
   - "requirements*.txt"
   - "requirements-dev.txt"
   - "pyproject.toml"
   - "Pipfile*"
   - "setup.py"
   - "setup.cfg"
workflow_dispatch:
 inputs:
   audit-level:
     description: "Audit severity level"
     required: false
     default: "critical"
     type: choice
     options:
       - info
       - low
       - moderate
       - high
       - critical

jobs:
audit-changed-packages:
 runs-on: ubuntu-latest
 if: github.event_name == 'pull_request'
 steps:
   - name: Checkout code
     uses: actions/checkout@8ade135a41bc03ea155e62e844d188df1ea18608 # v4.1.0

   - name: Detect changed package files
     id: changes
     uses: dorny/paths-filter@de90cc6fb38fc0963ad72b210f1f284cd68cea36 # v3.0.2
     with:
       filters: |
         python:
           - 'requirements*.txt'
           - 'requirements-dev.txt'
           - 'pyproject.toml'
           - 'Pipfile*'
           - 'setup.py'
           - 'setup.cfg'

   - name: Audit Python (if changed)
     if: steps.changes.outputs.python == 'true'
     run: |
       python -m pip install --upgrade pip
       pip install pip-audit
       pip-audit --vulnerability-service osv --strict || {
         # Only fail on CRITICAL vulnerabilities
         pip-audit --format json --output audit.json
         if jq -e '.vulnerabilities[] | select(.severity == "CRITICAL")' audit.json > /dev/null; then
           echo "Critical Python vulnerabilities found"
           exit 1
         fi
         exit 0
       }

   - name: Comment on PR if critical issues found
     if: failure()
     uses: actions/github-script@ed597411d8f924073f98dfc5c65a23a2325f34cd # v8.0.0
     env:
       AUDIT_LEVEL: ${{ inputs.audit-level || 'critical' }}
     with:
       script: |
         const auditLevel = process.env.AUDIT_LEVEL;
         await github.rest.issues.createComment({
           issue_number: context.issue.number,
           owner: context.repo.owner,
           repo: context.repo.repo,
           body: `⛔ Critical security vulnerabilities detected in dependencies (audit level: ${auditLevel}). Please review and fix before merging.`
         });

```

File: /Users/adamjackson/LocalDev/enaible/shared/skills/codify-pr-reviews/config/defaults.json
```json
{
"defaultDaysBack": 90,
"defaultExcludeAuthors": [
 "dependabot",
 "dependabot[bot]",
 "github-actions",
 "github-actions[bot]",
 "renovate",
 "renovate[bot]"
],
"defaultMinOccurrences": 3,
"defaultSemanticThreshold": 0.85,
"defaultMinCommentLength": 20,
"categories": [
 "security",
 "error-handling",
 "type-safety",
 "performance",
 "accessibility",
 "react-patterns",
 "api-design",
 "database",
 "testing",
 "code-style"
],
"instructionFiles": {
 "repository": ".github/copilot-instructions.md",
 "backend": ".github/instructions/backend.instructions.md",
 "frontend": ".github/instructions/frontend.instructions.md",
 "vsCodeSecurity": ".vscode/rules/security-patterns.md",
 "vsCodeGeneral": ".vscode/rules/general-guidelines.md",
 "vsCodeTesting": ".vscode/rules/testing-standards.md"
}
}

```

File: /Users/adamjackson/LocalDev/enaible/shared/skills/codify-pr-reviews/scripts/fetch_comments.py
```py
#!/usr/bin/env python3
"""Fetch PR review comments via gh CLI."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


def run(cmd: list[str]) -> str:
 result = subprocess.run(cmd, capture_output=True, text=True)
 if result.returncode != 0:
     raise RuntimeError(result.stderr.strip() or "Command failed")
 return result.stdout


def parse_repo() -> str:
 output = run(["git", "remote", "get-url", "origin"]).strip()
 if output.endswith(".git"):
     output = output[:-4]
 if output.startswith("git@github.com:"):
     return output.replace("git@github.com:", "")
 if "github.com/" in output:
     return output.split("github.com/")[-1]
 raise RuntimeError("Unable to parse GitHub repo from git remote origin")


def load_defaults(config_path: Path) -> dict[str, Any]:
 if not config_path.exists():
     return {}
 return json.loads(config_path.read_text(encoding="utf-8"))


def load_prs(repo: str, start_date: str, limit: int = 1000) -> list[dict[str, Any]]:
 output = run(
     [
         "gh",
         "pr",
         "list",
         "--repo",
         repo,
         "--state",
         "all",
         "--search",
         f"created:>={start_date}",
         "--json",
         "number,title,author,createdAt,state,mergedAt",
         "--limit",
         str(limit),
     ]
 )
 return json.loads(output or "[]")


def fetch_comments(repo: str, pr_number: int, comment_type: str) -> list[dict[str, Any]]:
 endpoint = f"repos/{repo}/pulls/{pr_number}/comments"
 if comment_type == "issue":
     endpoint = f"repos/{repo}/issues/{pr_number}/comments"
 output = run(["gh", "api", endpoint])
 return json.loads(output or "[]")


def normalize_author(author: str | None) -> str:
 return (author or "").lower().strip()


def main() -> int:
 parser = argparse.ArgumentParser(description="Fetch PR review comments via gh CLI.")
 parser.add_argument("--repo", default="")
 parser.add_argument("--days-back", type=int, default=None)
 parser.add_argument("--exclude-authors", default="")
 parser.add_argument("--min-comment-length", type=int, default=None)
 parser.add_argument("--output-path", default="")
 parser.add_argument("--preflight", action="store_true")
 parser.add_argument("--sample-prs", type=int, default=5)
 parser.add_argument(
     "--config",
     default=str(Path(__file__).resolve().parents[1] / "config" / "defaults.json"),
 )
 args = parser.parse_args()

 defaults = load_defaults(Path(args.config))
 days_back = args.days_back or defaults.get("defaultDaysBack", 90)
 exclude_authors = args.exclude_authors.split(",") if args.exclude_authors else defaults.get("defaultExcludeAuthors", [])
 exclude_set = {normalize_author(a) for a in exclude_authors}
 min_length = args.min_comment_length or defaults.get("defaultMinCommentLength", 20)

 repo = args.repo or parse_repo()
 start_date = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")

 prs = load_prs(repo, start_date)
 if args.preflight:
     sample = prs[: args.sample_prs]
     sample_count = len(sample)
     sample_comments = 0
     if sample:
         comments = fetch_comments(repo, sample[0]["number"], "review")
         sample_comments = len(comments)
     summary = {
         "repo": repo,
         "startDate": start_date,
         "samplePRs": sample_count,
         "sampleComments": sample_comments,
     }
     print(json.dumps(summary, indent=2))
     return 0

 pull_requests: list[dict[str, Any]] = []
 total_comments = 0
 review_count = 0
 issue_count = 0

 for pr in prs:
     pr_number = pr["number"]
     review_comments = fetch_comments(repo, pr_number, "review")
     issue_comments = fetch_comments(repo, pr_number, "issue")

     comments: list[dict[str, Any]] = []
     for comment in review_comments:
         author = normalize_author(comment.get("user", {}).get("login"))
         body = (comment.get("body") or "").strip()
         if author in exclude_set or len(body) < min_length:
             continue
         review_count += 1
         comments.append(
             {
                 "id": comment.get("id"),
                 "type": "review",
                 "author": author,
                 "body": body,
                 "path": comment.get("path"),
                 "line": comment.get("line"),
                 "createdAt": comment.get("created_at"),
             }
         )

     for comment in issue_comments:
         author = normalize_author(comment.get("user", {}).get("login"))
         body = (comment.get("body") or "").strip()
         if author in exclude_set or len(body) < min_length:
             continue
         issue_count += 1
         comments.append(
             {
                 "id": comment.get("id"),
                 "type": "issue",
                 "author": author,
                 "body": body,
                 "createdAt": comment.get("created_at"),
             }
         )

     if comments:
         pull_requests.append(
             {
                 "number": pr_number,
                 "title": pr.get("title"),
                 "author": pr.get("author", {}).get("login"),
                 "createdAt": pr.get("createdAt"),
                 "state": pr.get("state"),
                 "comments": comments,
             }
         )
         total_comments += len(comments)

 payload = {
     "fetchedAt": datetime.utcnow().isoformat() + "Z",
     "repository": repo,
     "dateRange": {
         "start": start_date,
         "end": datetime.utcnow().strftime("%Y-%m-%d"),
     },
     "totalPRs": len(prs),
     "totalComments": total_comments,
     "reviewComments": review_count,
     "issueComments": issue_count,
     "pullRequests": pull_requests,
 }

 if args.output_path:
     output_path = Path(args.output_path)
     output_path.parent.mkdir(parents=True, exist_ok=True)
     output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
     print(f"Wrote comments to {output_path}")
 else:
     print(json.dumps(payload, indent=2))

 return 0


if __name__ == "__main__":
 raise SystemExit(main())

```

File: /Users/adamjackson/LocalDev/enaible/shared/skills/codify-pr-reviews/scripts/preprocess_comments.py
```py
#!/usr/bin/env python3
"""Deduplicate and group PR comments."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


def load_defaults(config_path: Path) -> dict[str, Any]:
 if not config_path.exists():
     return {}
 return json.loads(config_path.read_text(encoding="utf-8"))


def load_red_flags(path: Path) -> list[str]:
 if not path.exists():
     return []
 data = json.loads(path.read_text(encoding="utf-8"))
 return [flag.lower() for flag in data.get("redFlags", [])]


def normalize(text: str) -> str:
 return re.sub(r"\s+", " ", text.strip().lower())


def tokenize(text: str) -> set[str]:
 return set(re.findall(r"[a-z0-9]+", text.lower()))


def jaccard(a: set[str], b: set[str]) -> float:
 if not a or not b:
     return 0.0
 return len(a & b) / len(a | b)


def flatten_comments(payload: dict[str, Any]) -> list[dict[str, Any]]:
 comments: list[dict[str, Any]] = []
 for pr in payload.get("pullRequests", []):
     for comment in pr.get("comments", []):
         comments.append(
             {
                 "pr": pr.get("number"),
                 "body": comment.get("body", ""),
                 "author": comment.get("author"),
                 "path": comment.get("path"),
                 "line": comment.get("line"),
             }
         )
 if comments:
     return comments
 return payload.get("comments", [])


def group_exact(comments: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
 groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
 for comment in comments:
     key = normalize(comment.get("body", ""))
     groups[key].append(comment)
 return list(groups.values())


def group_by_similarity(groups: list[list[dict[str, Any]]], threshold: float) -> list[list[dict[str, Any]]]:
 clustered: list[list[dict[str, Any]]] = []
 rep_tokens: list[set[str]] = []

 for group in groups:
     rep = normalize(group[0].get("body", ""))
     tokens = tokenize(rep)
     placed = False
     for idx, existing in enumerate(clustered):
         if jaccard(tokens, rep_tokens[idx]) >= threshold:
             existing.extend(group)
             rep_tokens[idx] = tokenize(normalize(existing[0].get("body", "")))
             placed = True
             break
     if not placed:
         clustered.append(list(group))
         rep_tokens.append(tokens)

 return clustered


def main() -> int:
 parser = argparse.ArgumentParser(description="Group and deduplicate PR comments.")
 parser.add_argument("--input-path", required=True)
 parser.add_argument("--red-flags-path", required=True)
 parser.add_argument("--output-path", required=True)
 parser.add_argument("--min-occurrences", type=int, default=None)
 parser.add_argument("--semantic-threshold", type=float, default=None)
 parser.add_argument(
     "--config",
     default=str(Path(__file__).resolve().parents[1] / "config" / "defaults.json"),
 )
 args = parser.parse_args()

 defaults = load_defaults(Path(args.config))
 min_occurrences = args.min_occurrences or defaults.get("defaultMinOccurrences", 3)
 semantic_threshold = args.semantic_threshold or defaults.get("defaultSemanticThreshold", 0.85)

 payload = json.loads(Path(args.input_path).read_text(encoding="utf-8"))
 comments = flatten_comments(payload)
 red_flags = load_red_flags(Path(args.red_flags_path))

 exact_groups = group_exact(comments)
 fuzzy_threshold = min(0.95, semantic_threshold + 0.05)
 fuzzy_groups = group_by_similarity(exact_groups, fuzzy_threshold)
 semantic_groups = group_by_similarity(fuzzy_groups, semantic_threshold)

 comment_groups = []
 kept = 0
 for group in semantic_groups:
     representative = group[0].get("body", "").strip()
     occurrences = len(group)
     normalized = normalize(representative)
     is_red_flag = any(flag in normalized for flag in red_flags)
     if occurrences < min_occurrences and not is_red_flag:
         continue
     kept += occurrences
     comment_groups.append(
         {
             "id": re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")[:40],
             "representative": representative,
             "occurrences": occurrences,
             "isRedFlag": is_red_flag,
             "examples": group[:5],
         }
     )

 output = {
     "processedAt": datetime.utcnow().isoformat() + "Z",
     "inputComments": len(comments),
     "outputGroups": len(comment_groups),
     "keptComments": kept,
     "filteredOut": len(comments) - kept,
     "commentGroups": comment_groups,
     "stats": {
         "exactGroups": len(exact_groups),
         "fuzzyGroups": len(fuzzy_groups),
         "semanticGroups": len(semantic_groups),
         "minOccurrences": min_occurrences,
         "semanticThreshold": semantic_threshold,
     },
 }

 out_path = Path(args.output_path)
 out_path.parent.mkdir(parents=True, exist_ok=True)
 out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
 print(f"Wrote grouped comments to {out_path}")
 return 0


if __name__ == "__main__":
 raise SystemExit(main())

```

File: /Users/adamjackson/LocalDev/enaible/docs/skills.md
```md
# Specification

> The complete format specification for Agent Skills.

This document defines the Agent Skills format.

## Directory structure

A skill is a directory containing at minimum a `SKILL.md` file:

```
skill-name/
└── SKILL.md          # Required
```

<Tip>
You can optionally include [additional directories](#optional-directories) such as `scripts/`, `references/`, and `assets/` to support your skill.
</Tip>

## SKILL.md format

The `SKILL.md` file must contain YAML frontmatter followed by Markdown content.

### Frontmatter (required)

```yaml  theme={null}
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

With optional fields:

```yaml  theme={null}
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents.
license: Apache-2.0
metadata:
author: example-org
version: "1.0"
---
```

| Field           | Required | Constraints                                                                                                       |
| --------------- | -------- | ----------------------------------------------------------------------------------------------------------------- |
| `name`          | Yes      | Max 64 characters. Lowercase letters, numbers, and hyphens only. Must not start or end with a hyphen.             |
| `description`   | Yes      | Max 1024 characters. Non-empty. Describes what the skill does and when to use it.                                 |
| `license`       | No       | License name or reference to a bundled license file.                                                              |
| `compatibility` | No       | Max 500 characters. Indicates environment requirements (intended product, system packages, network access, etc.). |
| `metadata`      | No       | Arbitrary key-value mapping for additional metadata.                                                              |
| `allowed-tools` | No       | Space-delimited list of pre-approved tools the skill may use. (Experimental)                                      |

#### `name` field

The required `name` field:

* Must be 1-64 characters
* May only contain unicode lowercase alphanumeric characters and hyphens (`a-z` and `-`)
* Must not start or end with `-`
* Must not contain consecutive hyphens (`--`)
* Must match the parent directory name

Valid examples:

```yaml  theme={null}
name: pdf-processing
```

```yaml  theme={null}
name: data-analysis
```

```yaml  theme={null}
name: code-review
```

Invalid examples:

```yaml  theme={null}
name: PDF-Processing  # uppercase not allowed
```

```yaml  theme={null}
name: -pdf  # cannot start with hyphen
```

```yaml  theme={null}
name: pdf--processing  # consecutive hyphens not allowed
```

#### `description` field

The required `description` field:

* Must be 1-1024 characters
* Should describe both what the skill does and when to use it
* Should include specific keywords that help agents identify relevant tasks

Good example:

```yaml  theme={null}
description: Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.
```

Poor example:

```yaml  theme={null}
description: Helps with PDFs.
```

#### `license` field

The optional `license` field:

* Specifies the license applied to the skill
* We recommend keeping it short (either the name of a license or the name of a bundled license file)

Example:

```yaml  theme={null}
license: Proprietary. LICENSE.txt has complete terms
```

#### `compatibility` field

The optional `compatibility` field:

* Must be 1-500 characters if provided
* Should only be included if your skill has specific environment requirements
* Can indicate intended product, required system packages, network access needs, etc.

Examples:

```yaml  theme={null}
compatibility: Designed for Claude Code (or similar products)
```

```yaml  theme={null}
compatibility: Requires git, docker, jq, and access to the internet
```

<Note>
Most skills do not need the `compatibility` field.
</Note>

#### `metadata` field

The optional `metadata` field:

* A map from string keys to string values
* Clients can use this to store additional properties not defined by the Agent Skills spec
* We recommend making your key names reasonably unique to avoid accidental conflicts

Example:

```yaml  theme={null}
metadata:
author: example-org
version: "1.0"
```

#### `allowed-tools` field

The optional `allowed-tools` field:

* A space-delimited list of tools that are pre-approved to run
* Experimental. Support for this field may vary between agent implementations

Example:

```yaml  theme={null}
allowed-tools: Bash(git:*) Bash(jq:*) Read
```

### Body content

The Markdown body after the frontmatter contains the skill instructions. There are no format restrictions. Write whatever helps agents perform the task effectively.

Recommended sections:

* Step-by-step instructions
* Examples of inputs and outputs
* Common edge cases

Note that the agent will load this entire file once it's decided to activate a skill. Consider splitting longer `SKILL.md` content into referenced files.

## Optional directories

### scripts/

Contains executable code that agents can run. Scripts should:

* Be self-contained or clearly document dependencies
* Include helpful error messages
* Handle edge cases gracefully

Supported languages depend on the agent implementation. Common options include Python, Bash, and JavaScript.

### references/

Contains additional documentation that agents can read when needed:

* `REFERENCE.md` - Detailed technical reference
* `FORMS.md` - Form templates or structured data formats
* Domain-specific files (`finance.md`, `legal.md`, etc.)

Keep individual [reference files](#file-references) focused. Agents load these on demand, so smaller files mean less use of context.

### assets/

Contains static resources:

* Templates (document templates, configuration templates)
* Images (diagrams, examples)
* Data files (lookup tables, schemas)

## Progressive disclosure

Skills should be structured for efficient use of context:

1. **Metadata** (\~100 tokens): The `name` and `description` fields are loaded at startup for all skills
2. **Instructions** (\< 5000 tokens recommended): The full `SKILL.md` body is loaded when the skill is activated
3. **Resources** (as needed): Files (e.g. those in `scripts/`, `references/`, or `assets/`) are loaded only when required

Keep your main `SKILL.md` under 500 lines. Move detailed reference material to separate files.

## File references

When referencing other files in your skill, use relative paths from the skill root:

```markdown  theme={null}
See [the reference guide](references/REFERENCE.md) for details.

Run the extraction script:
scripts/extract.py
```

Keep file references one level deep from `SKILL.md`. Avoid deeply nested reference chains.

## Validation

Use the [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) reference library to validate your skills:

```bash  theme={null}
skills-ref validate ./my-skill
```

This checks that your `SKILL.md` frontmatter is valid and follows all naming conventions.


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://agentskills.io/llms.txt
```

File: /Users/adamjackson/LocalDev/enaible/shared/skills/AGENTS.md
```md
# Shared Skill Authoring Guide

1. Create a skill directory under `shared/skills/<skill-name>/` with a required `SKILL.md`.

2. Keep `SKILL.md` compliant with `docs/skills.md`:
- YAML frontmatter with `name` and `description`.
- `name` must match the folder name.
- Keep the body under 500 lines when possible.
- Keep the instructions light and concise, details are through progressive disclosure of documents within `resources/`

3. Add supporting files in `resources/`, `scripts/`, `assets/`, or `config/` as needed.

4. Render skills for supported systems:

```bash
uv run --project tools/enaible enaible skills render --skill all --system all
```

5. Validate rendered outputs:

```bash
uv run --project tools/enaible enaible skills validate --skill all --system all
```

6. Install into a project or user scope for verification:

```bash
uv run --project tools/enaible enaible install claude-code --mode sync --scope project
uv run --project tools/enaible enaible install codex --mode sync --scope user
```

```
</file_contents>
<git_diff>
diff --git a/shared/skills/AGENTS.md b/shared/skills/AGENTS.md
index cdd9a13..848c009 100644
--- a/shared/skills/AGENTS.md
+++ b/shared/skills/AGENTS.md
@@ -6,8 +6,9 @@
 - YAML frontmatter with `name` and `description`.
 - `name` must match the folder name.
 - Keep the body under 500 lines when possible.
+   - Keep the instructions light and concise, details are through progressive disclosure of documents within `resources/`

-3. Add supporting files in `resources/`, `scripts/`, or `assets/` as needed.
+3. Add supporting files in `resources/`, `scripts/`, `assets/`, or `config/` as needed.

4. Render skills for supported systems:

@@ -25,5 +26,5 @@ uv run --project tools/enaible enaible skills validate --skill all --system all

```bash
uv run --project tools/enaible enaible install claude-code --mode sync --scope project
-uv run --project tools/enaible enaible install codex --mode sync --scope project
+uv run --project tools/enaible enaible install codex --mode sync --scope user
```

</git_diff>
<meta prompt 1 = "[Review]">
You are reviewing code changes with git diffs included in the prompt. Focus on ensuring the changes are sound, clean, intentional, and void of regressions.

**Primary Review Goals:**

1. **Verify Change Correctness**:
	- Confirm the changes achieve their intended purpose
	- Check for unintended side effects or regressions
	- Validate edge cases are handled properly
	- Ensure error paths are covered

2. **Code Quality & Cleanliness**:
	- Is the code readable and self-documenting?
	- Are the changes minimal and focused?
	- Do they follow existing patterns in the codebase?
	- Are there any code smells or anti-patterns?

3. **Intentionality Check**:
	- Does every change have a clear purpose?
	- Are there any accidental modifications?
	- Is there dead code being introduced?
	- Are the commit boundaries logical?

4. **Potential Issues to Flag**:
	- Performance degradations
	- Security vulnerabilities
	- Race conditions or concurrency issues
	- Resource leaks (memory, file handles, etc.)
	- Breaking changes to internal APIs

5. **Constructive Suggestions**:
	- Alternative approaches that might be cleaner
	- Opportunities to reduce complexity
	- Missing test coverage for critical paths
	- Documentation gaps for complex logic

**Review Format:**
- Start with a summary of what the changes accomplish
- List any critical issues that must be addressed
- Note minor improvements that would enhance quality
- Acknowledge what's done particularly well
- End with specific, actionable next steps if needed

Remember: The git diff shows what changed, and the file contents show the full context. Use both to understand the complete picture.
</meta prompt 1>
<user_instructions>
<taskname="Rules Eval System"/>
<task>
Build a new shared prompt `shared/prompts/create-rules-eval.md` (Purpose → Variables → Instructions → Workflow → Output) and add an eval system (user prefers separate `tools/eval` package instead of `tools/enaible`) that discovers rules, builds minimal tests, runs multi-provider/multi-run evals, scores deterministic vs semantic rules (DeepEval), and renders a markdown report plus eval payload. Register the prompt in the catalog. Rule discovery paths must align with system install rules and docs. Providers can be multiple per run, runs default 5, overall score is per-provider average of per-rule pass rates. Deduplicate rules by exact text match. Judge provider is configurable and distinct from test providers.
</task>

<architecture>
- Prompt rendering flow: `enaible/tools/enaible/src/enaible/prompts/catalog.py` (CATALOG entries) + `enaible/tools/enaible/src/enaible/prompts/renderer.py` (Jinja templates) + `enaible/tools/enaible/src/enaible/prompts/lint.py` + `enaible/tools/enaible/src/enaible/prompts/utils.py` (Variables parsing).
- CLI structure: root Typer app in `enaible/tools/enaible/src/enaible/app.py` + command modules in `enaible/tools/enaible/src/enaible/commands/*.py` registered via `enaible/tools/enaible/src/enaible/commands/__init__.py`.
- System install + rule file mapping: `enaible/tools/enaible/src/enaible/commands/install.py` has `SYSTEM_RULES` and `_post_install` logic for where rule files land.
- System adapter contexts in `enaible/tools/enaible/src/enaible/prompts/adapters.py` (project/user scope dirs).
- Prompt templates: base guidance `enaible/docs/system/templates/prompt.md`; system wrappers in `enaible/docs/system/*/templates/*.j2`.
</architecture>

<selected_context>
- `enaible/shared/prompts/AGENTS.md`: shared prompt authoring rules (Variables section format, lint/validate workflow).
- `enaible/shared/prompts/create-rule.md`: example shared prompt structure and variable usage.
- `enaible/shared/prompts/setup-parallel-ai.md` + `enaible/tools/parallel/src/parallel/*`: explored per request; use as reference for separate tool packaging (avoid `tools/enaible` for eval system per user).
- `enaible/docs/system/templates/prompt.md`: canonical prompt structure (Purpose → Variables → Instructions → Workflow → Output).
- `enaible/docs/system/claude-code/slash-command.md`: CLAUDE.md user/project locations.
- `enaible/docs/system/codex/templates/prompt.md`: AGENTS.md user/project locations.
- `enaible/docs/system/cursor/rules.md`: Cursor rules format (.cursor/rules/*.mdc) and managed sentinel.
- `enaible/docs/system/*/templates/*.j2`: system render wrappers (codex, claude, cursor, copilot, gemini).
- `enaible/tools/enaible/src/enaible/prompts/catalog.py` (sliced: top + tail with last entries): where new prompt registry entry goes; tail ends at `setup-parallel-ai`.
- `enaible/tools/enaible/src/enaible/commands/install.py` (sliced): `SYSTEM_RULES`, `ALWAYS_MANAGED_PREFIXES`, and `_post_install` path handling for CLAUDE/Codex/Copilot/Cursor/Gemini/Antigravity.
- `enaible/tools/enaible/pyproject.toml`: dependency groups for optional eval deps (deepeval, SDKs).
- `enaible/tools/enaible/src/enaible/commands/analyzers.py` + `enaible/tools/enaible/src/enaible/commands/prompts.py`: CLI command patterns.
- `enaible/tools/enaible/tests/test_prompt_utils.py`, `enaible/tools/enaible/tests/test_prompts_renderer.py`: prompt parsing/rendering test style.
- `enaible/systems/*/rules/global.*.rules.md`: representative rule formats (headings + bullet rules) for parser expectations.
- `enaible/systems/AGENTS.md`: system adapter playbook (install/render alignment).
</selected_context>

<relationships>
- New shared prompt must conform to `enaible/docs/system/templates/prompt.md` and the Variables parsing enforced by `enaible/tools/enaible/src/enaible/prompts/utils.py`/`lint.py`.
- Prompt registry entry lives in `enaible/tools/enaible/src/enaible/prompts/catalog.py` and will render through system templates in `enaible/docs/system/*/templates/*.j2`.
- Rule discovery paths should mirror `SYSTEM_RULES` + `_post_install` in `enaible/tools/enaible/src/enaible/commands/install.py` and system docs (CLAUDE.md, AGENTS.md, GEMINI.md, Cursor rules).
</relationships>

<ambiguities>
- None.
</ambiguities>

</user_instructions>
````
