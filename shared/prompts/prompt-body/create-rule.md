# Purpose

Produce an implementation-focused rule file for a specified technology so automated code generation follows proven patterns and avoids anti-patterns.

## Variables

- `TECHNOLOGY_NAME` ← first positional argument; required (may contain spaces).
- `RULE_FILE_PATH` ← `./.claude/rules/<slugified TECHNOLOGY_NAME>.md`.
- `$ARGUMENTS` ← raw argument string for inclusion in the rule header.

## Instructions

- ALWAYS ground rules in authoritative sources (official docs → style guides → production case studies → community patterns).
- Focus exclusively on implementation guidance—omit installation or scaffolding steps.
- Include actionable code examples for every rule section; ensure examples compile or are syntactically correct.
- Highlight anti-patterns with ❌ and provide preferred alternatives with ✅.
- After writing, verify the file matches the required structure and is free of placeholders.

## Workflow

1. Prepare output directory
   - Run `mkdir -p .claude/rules && test -w .claude/rules`; exit immediately if the rules directory cannot be created or written.
2. Parse input
   - Capture `TECHNOLOGY_NAME`; prompt if missing.
   - Derive filename slug (lowercase, hyphen-separated) for `RULE_FILE_PATH`.
3. Research implementation practices
   - Collect documentation excerpts, style guides, and mature examples.
   - Note security, performance, and error-handling considerations specific to the technology.
4. Draft rule file contents
   - Structure must include:
     - Header with technology name and applicable glob patterns.
     - Sections: Core Implementation Rules, Security Rules, Performance Rules, Error Handling Rules, Anti-Patterns.
   - Provide code blocks demonstrating required patterns and forbidden examples.
   - Use imperative language (“Always”, “Never”, “Must”).
5. Write rule file
   - Create directories as needed (`.claude/rules/`).
   - Save markdown content to `RULE_FILE_PATH`.
6. Quality review
   - Re-read file for completeness, accuracy, and clarity.
   - Confirm examples align with current best practices and are consistent with earlier sections.
7. Summarize outcome
   - Report the rule sections, number of rules per section, and any references used.

## Output

```md
# RESULT

- Summary: Implementation rules for <TECHNOLOGY_NAME> created.

## FILE

- Path: .claude/rules/<slug>.md
- Sections: Core, Security, Performance, Error Handling, Anti-Patterns
- Examples Included: <yes/no>

## REFERENCES

- <Reference 1>
- <Reference 2>
```

## Examples

```bash
# Create React implementation rules
/create-rule react

# Generate Prisma ORM implementation guidance
/create-rule prisma
```
