# Constitution

Automated gates are the source of truth. Documentation explains; it never enforces.

## Enforcement Hierarchy

1. **Automated gates** (lint, test, CI) define and enforce rules
2. **Constitution** states principles; tools implement them
3. **Documentation** explains context; it never duplicates enforceable rules

## Core Principles

### Code Quality

Enforced by Ruff, Prettier, MyPy:

- **Complexity**: Max cyclomatic complexity 10 (Ruff C901)
- **No backward compatibility**: Never maintain legacy code paths alongside new implementations
- **No fallbacks**: Code works as designed; no defensive fallback mechanisms
- **Libraries over bespoke**: Prefer established libraries to custom implementations

### Security

- **No secrets in version control**: Never commit API keys, tokens, passwords, or credentials
- **No secrets in logs**: Never echo, print, or log sensitive values
- **Presence checks**: Use existence checks (`-n "$VAR"`) instead of printing values

### Process

- **Atomic commits**: Commit at logical conclusion points to establish safe checkpoints
- **Conventional Commits**: Use `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, `perf:` prefixes
- **Pre-commit blocks on failure**: Quality gates must block, never warn-only
- **CI mirrors local**: Same gates run locally and in CI

### AI Guidance

- **Permission to fail**: "I don't know" is a valid response; fabrication is worse than uncertainty
- **No reward hacking**: Never bypass, suppress, or work around quality gates

## Enforcement Reference

| Principle | Enforced By |
|-----------|-------------|
| Complexity limit | `ruff.toml` (C901) |
| Code style | `ruff.toml`, `.prettierrc` |
| Type safety | `mypy.ini` |
| Pre-commit gates | `.pre-commit-config.yaml` |
| CI gates | `.github/workflows/ci-quality-gates-incremental.yml` |
| Constitution compliance | `.github/workflows/constitution-compliance.yml` |
