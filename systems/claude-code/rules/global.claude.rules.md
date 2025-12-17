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
