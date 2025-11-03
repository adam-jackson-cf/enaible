# Purpose

Produce an implementation-focused rule file for a specified technology so automated code generation follows proven patterns and avoids anti-patterns.

## Variables

### Required

- @TECHNOLOGY = $1 — technology or framework to document

### Optional (derived from $ARGUMENTS)

- @AUTO = --auto — skip STOP confirmations (auto-approve checkpoints)
- @RULE_FILE_PATH = --out — destination path for the generated implementation rule (defaults to `rules/<slug>.md`)

### Derived (internal)

- @RULE_SLUG = <derived> — slugified @TECHNOLOGY used for default filenames

## Instructions

- ALWAYS ground rules in authoritative sources (official docs → style guides → production case studies → community patterns).
- Focus exclusively on implementation guidance—omit installation or scaffolding steps.
- Include actionable code examples for every rule section; ensure examples compile or are syntactically correct.
- Highlight anti-patterns with ❌ and provide preferred alternatives with ✅.
- After writing, verify the file matches the required structure and is free of placeholders.
- Respect STOP confirmations unless @AUTO is provided; when auto is active, treat checkpoints as approved without altering other behavior.

## Workflow

1. Research implementation practices
   - Collect documentation excerpts, style guides, and mature examples.
   - Note security, performance, and error-handling considerations specific to the technology.
2. Draft rule file contents
   - Structure must include:
     - Header with technology name and applicable glob patterns.
     - Sections: Core Implementation Rules, Security Rules, Performance Rules, Error Handling Rules, Anti-Patterns.
   - Provide code blocks demonstrating required patterns and forbidden examples.
   - Use imperative language (“Always”, “Never”, “Must”).
3. Write rule file
   - Determine the destination: use @RULE_FILE_PATH when provided, otherwise `rules/@RULE_SLUG.md`.
   - Save the markdown content to the resolved path.
4. Quality review
   - Re-read file for completeness, accuracy, and clarity.
   - Confirm examples align with current best practices and are consistent with earlier sections.
5. Summarize outcome
   - Report the rule sections, number of rules per section, and any references used.

## Output

```md
# RESULT

- Summary: Implementation rules for <@TECHNOLOGY> created.

## FILE

- Path: <resolved path or default>
- Sections: <suitable-related-sections> e.g. Core, Security, Performance, Error Handling, Anti-Patterns
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
