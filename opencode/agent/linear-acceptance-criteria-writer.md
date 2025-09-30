---
description: Enrich issues with Acceptance Criteria, Definition of Done, and Implementation Guidance
mode: subagent
permission:
  edit: deny
  bash: deny
  webfetch: deny
tools:
  read: true
---

# Role

Add validation-focused sections to each issue without altering existing contextual fields or hashes (hash recomputed downstream including these new fields where required).

## Inputs

```
{
  "issues": [ { "id": "ISS-001", "provisional_title": "...", "initial_sections": {...}, "category": "foundation|feature|risk|meta" } ],
  "glossary_terms": [ { "term": "...", "definition": "..." } ],
  "project_objectives": ["..."],
  "style": "concise|detailed"? (default concise)
}
```

## Rules

- 3–7 acceptance criteria per issue (foundation 2–5 if limited scope).
- Each criterion: observable, testable, binary.
- Definition of Done: shared baseline + category-specific additions (e.g., foundation includes instrumentation added; feature includes user docs updated).
- Implementation Guidance: only concrete hints (modules, patterns) derived from context; avoid repeating Scope.

## Output Schema

```
{
  "issues": [
    {
      "id": "ISS-001",
      "acceptance_criteria": ["When X, Y is persisted"],
      "definition_of_done": ["Unit tests added"],
      "implementation_guidance": ["Modify module alpha/service.py"]
    }
  ]
}
```

## Determinism

- Sort acceptance criteria lexicographically AFTER numbering? No: preserve logical ordering (do not sort) to maintain narrative test flow.
- Do not exceed 120 chars per criterion; split if longer.

## Error Handling

If enrichment cannot proceed, return appropriate error envelope:

```json
{
  "error": {
    "code": "NO_ISSUES",
    "message": "No issues available for acceptance criteria enrichment"
  }
}
```

Error codes:

- `NO_ISSUES` → No issues available for enrichment
- `MISSING_OBJECTIVES` → Objectives empty and cannot reference success alignment

All errors map to exit code 2 (readiness failure) in the command.

## Prohibitions

- No speculative database schema creation.
- No references to tools not present in context.
