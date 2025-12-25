# system prompt

You are a senior software architect specializing in code design and implementation planning. Your role is to:

1. Analyze the requested changes and break them down into clear, actionable steps
2. Create a detailed implementation plan that includes:
   - Files that need to be modified
   - Specific code sections requiring changes
   - New functions, methods, or classes to be added
   - Dependencies or imports to be updated
   - Data structure modifications
   - Interface changes
   - Configuration updates

For each change:

- Describe the exact location in the code where changes are needed
- Explain the logic and reasoning behind each modification
- Provide example signatures, parameters, and return types
- Note any potential side effects or impacts on other parts of the codebase
- Highlight critical architectural decisions that need to be made

You may include short code snippets to illustrate specific patterns, signatures, or structures, but do not implement the full solution.

Focus solely on the technical implementation plan - exclude testing, validation, and deployment considerations unless they directly impact the architecture.

Please proceed with your analysis based on the following <user instructions>

## instructions

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
- `enaible/docs/system/cursor/rules.md`: Cursor rules format (.cursor/rules/\*.mdc) and managed sentinel.
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

## structure

/Users/adamjackson/LocalDev/enaible
├── .github
│ ├── workflows
│ │ ├── helpers
│ │ │ └── copilot*doc_review_prompt.py +
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
│ │ │ └── docs-scraper.md
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

## plan

Implementation Plan

Scope and goals

    •	Build a new shared prompt  create-rules-eval.md  that gathers rules context, generates minimal tests, and outputs an eval payload plus a human‑readable report.
    •	Implement a Python eval system in  tools/enaible  that discovers rules, invokes providers, scores rules with DeepEval + deterministic checks, and renders markdown output.
    •	Support multiple providers per run, multiple runs per provider (default 5), and average pass per rule scoring.

Plan overview (actionable sequence)

    •	Step 1: Confirm agent rule file locations by cross‑referencing install artifacts in  docs/system/*  and  systems/* .
    •	Step 2: Define the shared prompt structure and tokens per  shared/prompts/AGENTS.md .
    •	Step 3: Add eval package modules (registry, parser, test builder, providers, scorers, orchestrator, reporter).
    •	Step 4: Add CLI entrypoint for evals with multi‑provider and multi‑run support.
    •	Step 5: Register the prompt in the catalog and ensure system templates are compatible.

───────
Shared Prompt Design

File and location

    •	Location:  shared/prompts/create-rules-eval.md 
    •	Template structure: Purpose → Variables → Instructions → Workflow → Output (exact match with  docs/system/templates/prompt.md )

Variables (tokens)

    •	Required:  @AGENT = $1 ,  @PROVIDERS = $2 
    •	Optional:  @RUNS = --runs ,  @PROJECT_ROOT = --project-root ,  @OS = --os 
    •	Derived:  @RULES_CONTEXT  (computed by orchestrator),  @RULES_PATHS  (computed by orchestrator)

Instructions and logic

    •	Rules discovery: Use  @RULES_PATHS  and  @RULES_CONTEXT  injected by the eval system; do not re‑discover within the LLM.
    •	Test creation: One minimal test per rule; avoid extra context; target single rule at a time.
    •	Scoring decision: Determine whether each rule is deterministic (pattern check) or semantic (LLM‑judge via DeepEval).
    •	Output: Provide a structured payload for the eval system plus a markdown report.

Output schema (example)

rules_eval:
agent: "@AGENT"
providers: ["cli:claude", "api:openai:gpt-4o"]
runs: 5
rules: - id: "R1"
text: "Never use any in TypeScript"
directive: "NEVER"
determinism: "deterministic"
tests: - rule_id: "R1"
prompt: "Write a TypeScript function..."
expected: "No usage of `any`"
scorer: "pattern"
report:
summary: "..."
notes: "..."

Side effects

    •	Prompt must be system‑agnostic and avoid fallbacks; any missing inputs should be errors handled by the eval system, not the prompt.

───────
Eval System Architecture

1. Agent registry

   • Location:  tools/enaible/src/enaible/evals/agent_registry.py 
   • Change: Add  AgentSpec  and  AGENT_REGISTRY .
   • Logic: Resolve user and project rule paths using OS‑neutral  Path.home()  and project root.
   • Signature:

@dataclass(frozen=True)
class AgentSpec:
name: str
user_paths: list[str]
project_paths: list[str]
glob_paths: list[str]

    •	Side effects: If no rules found for an agent, error out (no fallbacks).

2. Rules discovery and parsing

   • Location:  tools/enaible/src/enaible/evals/rules_parser.py 
   • Change: Extract normalized rules from markdown.
   • Logic: Parse headings and bullet lists; detect directives (ALWAYS/NEVER/MUST/SHOULD/PREFER); tag determinism.
   • Signature:

@dataclass(frozen=True)
class Rule:
id: str
source_path: str
text: str
directive: str
determinism: Literal["deterministic", "semantic"]

    •	Side effects: Conservative parsing avoids false positives; ambiguous rules marked semantic.

3. Test construction (minimal)

   • Location:  tools/enaible/src/enaible/evals/scenario_builder.py 
   • Change: Build a minimal prompt per rule.
   • Logic: Generate the smallest possible scenario that exercises the rule.
   • Signature:

@dataclass(frozen=True)
class TestCase:
rule_id: str
prompt: str
expected: str | None
scorer: Literal["pattern", "llm_judge"]

4. Provider abstraction

   • Location:  tools/enaible/src/enaible/evals/providers.py 
   • Change: Parse provider specs and implement CLI/API execution.
   • Logic: Use deval‑style provider abstraction for local CLI harness; API providers use official SDKs.
   • Signature:

@dataclass(frozen=True)
class ProviderSpec:
kind: Literal["cli", "api"]
name: str
model: str | None
api_key: str | None

    •	Side effects: Missing CLI binary or API key causes immediate error.

5. Scoring

   • Location:  tools/enaible/src/enaible/evals/scorers.py 
   • Change: Deterministic checks + DeepEval semantic scoring.
   • Logic: Pattern matching for deterministic rules; DeepEval GEval for semantic rules.
   • Signature:

def score_pattern(rule: Rule, response: str) -> bool: ...
def score_llm(rule: Rule, response: str, judge_provider: ProviderClient) -> bool: ...

6. Orchestrator

   • Location:  tools/enaible/src/enaible/evals/orchestrator.py 
   • Change: End‑to‑end flow across providers and runs.
   • Logic: For each provider, run each test  runs  times; compute per‑rule pass rate; final percent = mean(pass_rate per rule) \* 100.
   • Signature:

def run_eval(agent: str, providers: list[ProviderSpec], runs: int) -> EvalReport: ...

    •	Side effects: Increased cost with multiple runs; minimal tests mitigate.

7. Reporting (markdown)

   • Location:  tools/enaible/src/enaible/evals/reporter.py 
   • Change: Render human‑readable markdown.
   • Logic: Per‑provider section with overall score and per‑rule pass rates.
   • Signature:

def render_markdown(report: EvalReport) -> str: ...

───────
CLI Integration

Command entrypoint

    •	Location:  tools/enaible/src/enaible/commands/evals.py 
    •	Interface:

enaible evals run <agent> --provider cli:claude --provider api:openai:gpt-4o --runs 5
enaible evals list-agents
enaible evals list-rules <agent>

    •	Behavior:  --provider  is repeatable;  --runs  defaults to 5; outputs markdown to stdout or  --output .

Registry update

    •	Location:  tools/enaible/src/enaible/commands/__init__.py 
    •	Change: Add  enaible.commands.evals  to  _COMMAND_MODULES .

───────
Prompt Registration and Templates

Catalog entry

    •	Location:  tools/enaible/src/enaible/prompts/catalog.py 
    •	Change: Register  create-rules-eval  with correct template and output paths per system.

Template alignment

    •	Location:  docs/system/<system>/templates/*.j2  if new tokens or layout changes are needed.
    •	Logic: Only update templates if the shared prompt introduces new layout tokens.

───────
Dependencies and configuration

Dependencies

    •	Location:  tools/enaible/pyproject.toml 
    •	Change: Add  deepeval  and API SDKs in an optional dependency group, for example  [project.optional-dependencies].evals .

Side effects

    •	Optional dependencies avoid forcing LLM SDK installs for non‑eval users.

───────
Rules file discovery (agent‑specific)

Sources to confirm

    •	Location:  docs/system/claude-code ,  docs/system/codex ,  docs/system/gemini ,  docs/system/cursor , and  systems/*/rules 
    •	Logic: Use each system’s install guide to confirm user‑level locations and project‑level files.

Expected rule file mapping (draft)

    •	codex:  ~/.codex/AGENTS.md ,  .codex/AGENTS.md 
    •	claude-code:  ~/.claude/CLAUDE.md ,  CLAUDE.md 
    •	gemini:  ~/.gemini/GEMINI.md ,  .gemini/GEMINI.md 
    •	cursor:  ~/.cursor/rules/*.mdc ,  .cursorrules ,  .cursor/rules/*.mdc 

───────
Open questions (if you want me to resolve before implementing)

    •	Should the eval use one provider as the judge for semantic scoring, or reuse the tested provider for LLM‑judge prompts?   Yes, a single provider should be set as the judge of all (this should be configurable and use the same provider declarations approach we use for the test participants)
    •	Do you want an aggregate summary across providers, or strictly per‑provider reports only?  A single report with per provider average score (benchmark) across the test runs.
    •	Should rules from user + project scope be deduplicated if text matches, or evaluated as distinct sources? Yes, deduped if exact text match.

Please also explore the setup-parallel-ai.md prompt and tools/parallel folder - I would rather keep our eval system in a separate tools/eval folder than in the the tools/enaible - but for python scripts to assist the prompt that are not part of the eval system we should use the shared/\* directory where appropriate
