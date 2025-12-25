# Claude Code Instruction Rule Template

Use this template when creating or updating `CLAUDE.md` rules for Claude Code.

## Recommended file structure

````markdown
# Claude Code Project Rules

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

````

## Individual Rule Template

## Rule Title

- ALWAYS [positive directive - what to do]
- NEVER [what to avoid, if critical]
- [Additional context or specifics]

❌ BAD:
```[language]
// Example of incorrect implementation
````

✅ GOOD:

```[language]
// Example of correct implementation
```

**Note**: [Optional additional notes, edge cases, or context]

---

## Guidelines

1. **Positive framing**: Prefer "Do X" over "Don't do Y" when possible.
2. **Specific**: Include concrete details, not vague advice.
3. **Examples**: Include both bad and good code where practical.
4. **Language**: Match the project's tech stack.
5. **Concise**: 2-3 directives and focused examples per rule.
6. **File length**: Keep files under 4000 characters; split if needed.
7. **Unsupported content**: Avoid external links, product behavior changes, or formatting directives.
