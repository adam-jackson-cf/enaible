# System Targeting

Use this guide to select a single target system for rule formatting and resolve instruction file locations.

## Supported systems

Choose exactly one:

- `claude-code`
- `codex`
- `copilot`
- `cursor`
- `gemini`

## Instruction file mapping

### claude-code

- Project instructions: `./CLAUDE.md`
- User instructions: `~/.claude/CLAUDE.md`

Use `./CLAUDE.md` for repository-level rules unless the user explicitly requests user-scope changes.

### codex

- Project instructions: `./AGENTS.md`
- User instructions: `~/.codex/AGENTS.md`

Use `./AGENTS.md` for repository-level rules unless the user explicitly requests user-scope changes.

### copilot

- Project instructions: `.github/copilot-instructions.md`
- Path-scoped instructions: `.github/instructions/*.instructions.md`
- Agent instructions (when used by Copilot): `./AGENTS.md`

Prefer `.github/copilot-instructions.md` for general rules and `.github/instructions/*.instructions.md` for path-scoped rules.

### cursor

- Project instructions: `./AGENTS.md`
- Project rules (legacy): `./.cursorrules`
- Project rules (MDC): `./.cursor/rules/*.mdc`

Prefer `./AGENTS.md` for general rules; use `.mdc` or `.cursorrules` only when the user specifies Cursor rule formats.

### gemini

- Project instructions: `./GEMINI.md`
- User instructions: `~/.gemini/GEMINI.md`

Use `./GEMINI.md` for repository-level rules unless the user explicitly requests user-scope changes.

## Templates

Use the Copilot-specific template when targeting Copilot, and the general template for all other systems:

- [resources/templates/copilot-rule-template.md](resources/templates/copilot-rule-template.md)
- [resources/templates/rule-template.md](resources/templates/rule-template.md)
