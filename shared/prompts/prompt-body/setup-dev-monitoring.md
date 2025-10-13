# Purpose

Configure development monitoring by generating Makefile and Procfile orchestration, central logging, and CLAUDE.md updates tailored to the project’s runnable components.

## Variables

- `COMPONENTS[]` ← discovered runnable services (name, label, cwd, start_command, port).
- `WATCH_PATTERNS[]` ← glob patterns for non-native file watching needs.
- `SCRIPT_PATH` ← resolved monitoring script directory.
- `SCRIPTS_ROOT` ← base path for PYTHONPATH.
- `$ARGUMENTS` ← raw argument string.

## Instructions

- Discover actual start commands—never use placeholders or generic echoes.
- Exclude overlapping orchestrators when granular component commands are preferable.
- Pause for confirmation before excluding components, performing installations, or overwriting existing files.
- Ensure all services log to `./dev.log` with timestamped output (no `/dev.log` absolute path).
- Validate generated assets (Makefile, Procfile, CLAUDE.md updates) before reporting success.

## Workflow

1. Verify prerequisites
   - Run `ls .claude/scripts/setup/monitoring/*.py || ls "$HOME/.claude/scripts/setup/monitoring/install_monitoring_dependencies.py"`; if both fail, prompt for a script directory containing `install_monitoring_dependencies.py` and exit if unavailable.
   - Run `python3 --version`; exit immediately if Python 3 is unavailable.
   - Run `test -w .`; exit immediately if the project root is not writable because generated files must be saved here.
2. Project component discovery
   - Use `ls`, `glob`, and package manifests to identify runnable services (frontend, backend, workers, databases, build tools).
   - Determine true start commands from scripts, documentation, or framework defaults.
   - Assign log labels (FRONTEND, BACKEND, WORKER, etc.) and capture port information.
   - Verify each component has a runnable command; halt if any remain unresolved.
3. Component overlap analysis
   - Detect orchestrators that duplicate child services; mark for exclusion when appropriate.
   - Identify port conflicts.
   - **STOP:** “Exclude overlapping components: <list>? (y/n)” Adjust list based on user input.
4. Watch pattern analysis
   - Decide which technologies rely on native hot reload vs. external watchers.
   - Build `WATCH_PATTERNS[]` only for components lacking native watching.
   - **STOP:** “Component analysis complete. Proceed with setup? (y/n)”
5. Dependency verification
   - Resolve `SCRIPT_PATH` (project-level → user-level → prompt for path).
   - Compute `SCRIPTS_ROOT` and run `PYTHONPATH="$SCRIPTS_ROOT" python -c "import core.base; print('env OK')"`; abort on failure.
   - Execute dry-run dependency check:
     ```bash
     python "$SCRIPT_PATH"/install_monitoring_dependencies.py --dry-run
     ```
   - If tools missing, **STOP:** “Install missing core tools: <list>? (y/n)” Run full install on approval.
6. Existing file handling
   - Detect existing `Makefile` or `Procfile`.
   - **STOP:** “Existing Procfile/Makefile found. Choose action: (b)ackup, (o)verwrite, (c)ancel.”
   - Respect choice and create timestamped backups when requested.
7. Generate Makefile
   - Invoke generator with serialized `COMPONENTS[]` and `WATCH_PATTERNS[]`.
   - Ensure each target includes logging pipeline:
     ```
     2>&1 | while IFS= read -r line; do
       echo "[$(date '+%H:%M:%S')] [SERVICE] $line"
     done | tee -a ./dev.log
     ```
8. Generate Procfile
   - Use same component definitions, enforce logging pipeline, ensure Next.js commands use both `PORT` env var and `-- --port`.
9. Update CLAUDE.md
   - Run `update_claude_md.py` with component metadata to document new commands.
10. Validation

- Confirm generated files contain real commands (no placeholders).
- Check syntax (`make -n <target>`, `foreman check` if available).
- Review logging paths and port declarations.
- Summarize results and provide verification steps (`make dev`, `make status`, `tail -f ./dev.log`).

## Output

```md
# RESULT

- Summary: Development monitoring configured for <component count> components.

## COMPONENTS

- <Label> — <cwd> — <start_command> (port: <value>)

## FILES

- Makefile: <status (created/backed up + created)>
- Procfile: <status>
- CLAUDE.md: <updated sections>
- dev.log: <logging pipeline enabled>

## VALIDATION

- make dev: <pass|not run>
- make status: <pass|not run>
- make logs: <pass|not run>

## NEXT STEPS

1. Run `make dev` to start services.
2. Use `make logs` to tail `./dev.log`.
3. Review CLAUDE.md for updated workflow commands.
```

## Examples

```bash
# Configure monitoring for current repo
/setup-dev-monitoring
```
