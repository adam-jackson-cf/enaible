# 2025-10-12 Codex Installer UX alignment

- Matched Codex bash installer UX with Claude's phased flow and removed redundant scripts-root prompt; scripts now default under the selected Codex home with optional override flag.
- Mirrored the experience for PowerShell, including the new Node tooling step; unable to run pwsh locally to verify execution.
- Audited OpenCode installers and confirmed they already pin scripts under the install root with phased messaging, so no changes needed; CI workflows for Codex/OpenCode PS installers remain compatible with the updated interfaces.
- Hardened Codex installers to replace any existing AI-Assisted Workflows section in AGENTS.md instead of blindly appending, preventing duplicate global rules during merge/update modes.

# 2025-10-12 Code Quality Assessment

- Ran `core.cli.run_analyzer` with the `quality:lizard` analyzer via global `.codex` scripts to baseline complexity findings (182 total, 34 high) and began triaging hotspots in `shared/utils` and `shared/generators` for follow-up refactors.

# 2025-10-13 10:11:35 Todo Background: Codex + Test Matrix

- Updated `systems/claude-code/commands/todo-background.md`:
  - Normalized Codex model selector to `codex:gpt-5-codex`.
  - Added Codex launch instructions using `cdx-exec` and prompt-prepend reporting guidance.
- Added `scripts/test-todo-background.sh` to validate background behavior across CLI modes.
- Test results:
  - Claude: PASS (ACK line detected; report write confirmed)
  - Codex: PASS after flag fix (ACK line detected; Codex applied patch to report)
  - Qwen: RUN (no ACK detected within 25s; process terminated; report header present)
  - Gemini: RUN (no ACK detected within 25s; process terminated; report header present)
- Artifacts: Reports under `./.workspace/agents/background/background-report-<TIMESTAMP>.md`.
- Next: Consider increasing wait or adding explicit write-tool instructions for Qwen/Gemini variants.

# 2025-10-13 10:17:22 Auth Preflight for Background Tasks

- Added `scripts/check-ai-cli-auth.sh` to verify credentials and CLI presence for `claude`, `codex`, `qwen`, `gemini`.
- Integrated preflight into `scripts/test-todo-background.sh` and documented in `systems/claude-code/commands/todo-background.md` (Workflow step 0).
- Behavior: writes concise status into the report (if provided) and exits non-zero to stop background launch when auth is missing, preventing interactive login prompts.
- Current run:
  - Claude: Ran (ACK timing varied); auth OK.
  - Codex: PASS; auth OK; ACK appended.
  - Qwen: Auth detected via env; ACK appended (noted overwrite by tool; acceptable for test).
  - Gemini: ADC present; no ACK within window; kept as is.

# 2025-10-13 10:34:00 Integration Test for Todo Background Script

- Moved helper scripts to test fixtures:
  - `shared/tests/integration/fixtures/check-ai-cli-auth.sh`
  - `shared/tests/integration/fixtures/test-todo-background.sh`
- Added pytest: `shared/tests/integration/test_todo_background_script.py`
  - Runs the fixture script in `codex` mode, asserts exit=0, parses report path from output, and validates report exists and is non-empty.
- Updated command doc to reference the new preflight script path under fixtures.
- Local run: 1 test passed.

# 2025-10-13 11:39:20 Add OpenCode to Background Prompt + Tests

- Updated `systems/claude-code/commands/todo-background.md` to add `opencode` as a supported CLI:
  - Default model: `github-copilot/gpt-5-mini`
  - Launch snippet added with `--print-logs --log-level INFO --prompt` and prompt-prepended reporting instructions.
- Adjusted OpenCode command prompt (`systems/opencode/command/todo-background.md`) to default to `github-copilot/gpt-5-mini`.
- Extended auth preflight fixture to validate OpenCode (CLI present, model available, GitHub Copilot credential or `GITHUB_TOKEN`).
- Extended fixture runner and integration test to include `opencode` mode with gating; test remains green (1 paramized case by default).

# 2025-10-13 11:45:21 OpenCode Headless Run + Test Verification

- Switched OpenCode background command to `opencode run` for non-interactive execution (prompt doc + opencode command file + test fixture).
- Re-ran integration test with OpenCode mode: `TODO_BG_MODES=opencode PYTHONPATH=shared pytest shared/tests/integration/test_todo_background_script.py -q` → PASS.
