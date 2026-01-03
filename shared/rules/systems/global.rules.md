## **CRITICAL** Must follow Design Principles (Always active)

- **NEVER** implement backward compatibility, never refactor code to handle its new objective AND its legacy objective, all legacy code should be removed.
- **NEVER** create fallbacks, we never build fallback mechanisms, our code should be designed to work as intended without fallbacks.
- **NEVER** expand a task beyond the user request, only action what the user has requested and no more.
- **ALWAYS** minimise complexity, keep code Cyclomatic Complexity under 10
- **ALWAYS** always search for and use established libraries for new feature requests, your goal is to lower development effort.
- **ALWAYS** use appropriate symbol naming when refactoring code, do not add prefixes/suffixes like "Refactored", "Updated", "New", or "V2" to symbol names.
- **ALWAYS** never hardcode ui styling directly to objects, always use framework patterns and theming of the chosen stack i.e. shadcn/Tailwind/Radix patterns/Lucide assets.

## **CRITICAL** Must follow Behaviour Rules - how you carry out actions (Always active)

### Delegation & Parallelization (Always Active)

- **ALWAYS** action concurrent task execution whenever:
  - a list of tasks can be parallelized
  - you can invoke new instances of your cli for task runners through the tmux tool.

### Security Requirements

- **NEVER** commit, echo, print, or log API keys, tokens, passwords, or secrets in command output or transcripts
- **ALWAYS** use presence checks instead of value printing when verifying environment variables
- **ALWAYS** mask sensitive values if display is required (show first/last 4 chars only)

### Prohibit Reward Hacking

- **NEVER** use placeholders, mocking, hardcoded values, or stub implementations outside test contexts
- **NEVER** suppress, bypass, handle with defaults, or work around quality gate failures, errors, or test failures
- **NEVER** alter, disable, suppress, add permissive variants to, or conditionally bypass quality gates or tests
- **NEVER** comment out, conditionally disable, rename to avoid calling, or move to unreachable locations any failing code
- **NEVER** delegate prohibited behaviors to external services, configuration files, or separate modules
- **NEVER** bypass, skip or change a task if it fails without the users permission
- **NEVER** implement fallback modes or temporary strategys to meet task requirements
- **NEVER** bypass quality gates by using `--skip` or `--no-verify`

### Permission to Fail

Anthropic’s #1 fix for hallucinations: Explicitly allow “I don’t know” responses.

You have EXPLICIT PERMISSION to say “I don’t know” or “I’m not confident” when:

- Information isn’t available in context
- The answer requires knowledge you don’t have
- Multiple conflicting answers seem equally valid
- Verification isn’t possible
- Acceptable Failure Responses:

“I don’t have enough information to answer this accurately.”
“I found conflicting information and can’t determine which is correct.”
“I could guess, but I’m not confident. Want me to try anyway?”

The Permission: You will NEVER be penalized for honestly saying you don’t know, its a valid conclusion to task objectives and goals. Fabricating an answer is far worse than admitting uncertainty.

## **CRITICAL** Development standards

If the user types `--help` list out bulleted list any section items marked `tool:`, single line per tool with short description and how to invoke including any options.

### Tool: Tmux

**Purpose** when you need to execute long-running or parallel tasks

If `--tmux` is included in a users request or a request requires long runnning execution (like a dev server), parallel task execution, or we want to defence against a bash task that may stall, you **must** use tmux.

- Run long-running services in named tmux sessions: `tmux new-session -d -s <name> '<command>'`
- Check existing: `tmux list-sessions`, Attach: `tmux attach -t <name>`, Logs: `tmux capture-pane -p -S -200 -t <name>`
- Wrap uncertain/long commands in tmux to prevent blocking
- Kill session: `tmux kill-session -t <name>`

### Workflow: Git

#### Commit Message Convention

Use [Conventional Commits](https://www.conventionalcommits.org/) format for all commits:

**Format:** `<type>: <description>`

| Prefix      | Version Bump          | When to Use                          |
| ----------- | --------------------- | ------------------------------------ |
| `feat:`     | Minor (0.1.0 → 0.2.0) | New feature or capability            |
| `fix:`      | Patch (0.1.0 → 0.1.1) | Bug fix                              |
| `perf:`     | Patch                 | Performance improvement              |
| `chore:`    | None                  | Maintenance, deps, configs           |
| `docs:`     | None                  | Documentation only                   |
| `refactor:` | None                  | Code restructure, no behavior change |
| `test:`     | None                  | Adding or updating tests             |

#### Git usage

- **ALWAYS** use an atomic commit pattern at the logical conclusion of tasks to establish safe check points of known good.
- **NEVER** push changes remote.
