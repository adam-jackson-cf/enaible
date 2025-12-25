# Cursor Rule Template

Use this template when creating or updating Cursor rules for the repository.

## Recommended file structure (AGENTS.md)

````markdown
# Cursor Project Rules

Brief description of the rules in this file.

## Core Directives

- ALWAYS [positive directive]
- NEVER [avoidance directive, if critical]
- [Additional context or specifics]

## Examples

❌ BAD:

```[language]
// Example of incorrect implementation
```
````

✅ GOOD:

```[language]
// Example of correct implementation
```

```

## Optional MDC rule structure

If the user explicitly requests Cursor MDC rules (`.cursor/rules/*.mdc`), create a focused rule file with the same directive + example pattern.

## Guidelines

1. **Positive framing**: Prefer "Do X" over "Don't do Y" when possible.
2. **Specific**: Include concrete details, not vague advice.
3. **Examples**: Include both bad and good code where practical.
4. **Language**: Match the project's tech stack.
5. **Concise**: 2-3 directives and focused examples per rule.
6. **File length**: Keep files under 4000 characters; split if needed.
7. **Unsupported content**: Avoid external links, product behavior changes, or formatting directives.
```
