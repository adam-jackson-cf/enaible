# OpenAI Codex System Adapter

This adapter enables enaible shared prompts and skills to render for [OpenAI Codex](https://github.com/openai/codex).

## Configuration Structure

| Scope   | Directory                      |
| ------- | ------------------------------ |
| User    | `~/.codex/` (or `$CODEX_HOME`) |
| Project | `.codex/`                      |
| Admin   | `/etc/codex/`                  |

## File Formats

### Configuration

Settings in `$CODEX_HOME/config.toml`:

```toml
model = "o3"
model_provider = "openai-chat-completions"

[model_providers.openai-chat-completions]
name = "OpenAI using Chat Completions"
base_url = "https://api.openai.com/v1"
env_key = "OPENAI_API_KEY"
wire_api = "chat"
```

**Config precedence:**

1. Command-line flags (`--model o3`)
2. Generic `-c key=value` flag
3. `$CODEX_HOME/config.toml`

### Slash Commands (Prompts)

Prompts are markdown files in `~/.codex/prompts/*.md`:

```markdown
Review this code for: $ARGUMENTS

Focus on:

- Security vulnerabilities
- Performance issues
- Code style
```

**Variables:**

- `$1` to `$9` - Positional arguments
- `$ARGUMENTS` - All arguments joined by space
- `$$` - Literal dollar sign

**Usage:** Type `/` in composer, select prompt, provide arguments

### Skills

Skills are stored in scoped directories with `SKILL.md`:

```
.codex/skills/<skill-name>/
├── SKILL.md (required)
├── scripts/
├── references/
└── assets/
```

**SKILL.md format:**

```markdown
---
name: skill-name
description: What it does. USE WHEN [trigger]
metadata:
  short-description: User-facing summary
---

# Skill Name

## Workflow

Step 1: ...
Step 2: ...
```

**Skill scopes (highest to lowest precedence):**

| Scope  | Location             |
| ------ | -------------------- |
| REPO   | `.codex/skills/`     |
| USER   | `~/.codex/skills/`   |
| ADMIN  | `/etc/codex/skills/` |
| SYSTEM | Bundled with Codex   |

**Invocation:**

- Explicit: `/skills` or `$skill-name`
- Implicit: Codex matches description to request

**Built-in skills:** `$skill-creator`, `$skill-installer`, `$create-plan`

## Sandbox Modes

| Mode           | Flags                                                   | Effect                           |
| -------------- | ------------------------------------------------------- | -------------------------------- |
| Read Only      | `--sandbox read-only`                                   | Read files only                  |
| Auto (default) | `--sandbox workspace-write`                             | Edit workspace, ask for network  |
| Full Auto      | `--full-auto`                                           | Workspace access without prompts |
| Danger Zone    | `--sandbox danger-full-access --ask-for-approval never` | No restrictions                  |

## Non-Interactive Mode

```bash
codex exec "count lines of code in this project"
codex exec --full-auto "fix all linting errors"
codex exec --json "analyze codebase" > output.jsonl
```

**Output flags:**

- Default: Streams to stderr, final message to stdout
- `--json`: JSONL events to stdout
- `-o file`: Write final message to file

## References

- [Codex GitHub](https://github.com/openai/codex)
- [Codex Config](https://github.com/openai/codex/blob/main/docs/config.md)
- [Codex Skills](https://github.com/openai/skills)
- [Codex Agent Skills](https://developers.openai.com/codex/skills)
