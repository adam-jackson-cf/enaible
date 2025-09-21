# Project Rules and Behaviors

## Design Principles

- NEVER implement backward compatibility — remove legacy code rather than supporting both new and old objectives.
- NEVER create fallbacks — design flows to work as intended without fallback modes.
- NEVER over engineer — only do what’s requested; ask for approval before extra work.
- Prefer OpenCode search, @file includes, and built‑in LSP navigation for codebase understanding.
- ALWAYS prefer established libraries over bespoke code; only write bespoke code if no established library exists.
- Follow these architectural guidelines:
  - Single Responsibility: Each class/function should have one responsibility
  - Extract common logic into reusable modules when used 2+ times
  - Preserve symbol names during refactors; do not add suffixes/prefixes like “Refactored”, “Updated”, “New”, or “V2”
  - Keep functions under 30 lines

## Behavior Rules

### Context Gathering

- MUST read the full contents of any file you’re reviewing or acting upon.

### Security Requirements

- NEVER commit secrets, API keys, or credentials to version control.
- NEVER expose sensitive data (keys, secrets, credentials) in logs or outputs.

### Core Prohibitions

- NEVER use placeholders, mocking, hardcoded values, or stub implementations outside tests.
- NEVER suppress, bypass, or work around quality gates or tests.
- NEVER alter/disable tests to pass; fix root causes instead.
- NEVER rename/move failing code to avoid execution.
- NEVER delegate prohibited behavior to external services/config/modules.
- NEVER skip tasks after failure without explicit user permission.
- NEVER implement temporary fallback modes to meet requirements.
- NEVER bypass quality gates using flags like --skip or --no-verify.

### Formatting

- No Trailing Whitespace Policy: do not leave trailing spaces/tabs on any line.
