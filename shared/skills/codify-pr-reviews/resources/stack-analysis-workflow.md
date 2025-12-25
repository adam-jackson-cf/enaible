# Purpose

Detect the repository technology stack and generate red-flag patterns that must always be surfaced.

## Variables

### Required

- @PROJECT_ROOT — repository root to scan
- @OUTPUT_PATH — path to write the red-flag JSON file

### Optional

- @FORCE_REFRESH — when true, regenerate even if red flags already exist

## Instructions

- Scan dependency and config files to infer backend, frontend, database, and language.
- Generate stack-specific red flags plus a universal security list.
- Cache results at @OUTPUT_PATH and only regenerate when @FORCE_REFRESH is true.
- Return a concise summary (stack + red-flag count) to the main workflow.

## Deterministic tooling

Run:

```bash
python scripts/stack_analysis.py \
  --project-root "@PROJECT_ROOT" \
  --output-path "@OUTPUT_PATH"
```

## Workflow

1. **Locate stack indicators**
   - Check `package.json`, `requirements.txt`, `go.mod`, `pom.xml`, `Gemfile`, `Cargo.toml`, `composer.json`.
   - Scan for framework-specific config (`tsconfig.json`, `vite.config.*`, `.babelrc`, `next.config.*`).

2. **Infer stack**
   - Backend: Express/Fastify/Nest (Node), FastAPI/Django/Flask (Python), Gin/Echo (Go), Spring (Java).
   - Frontend: React/Vue/Angular/Svelte plus meta frameworks (Next/Nuxt).
   - Database: SQLite/Postgres/MySQL/Mongo + ORMs (Prisma/TypeORM/Sequelize).
   - Language priority: TypeScript > Python > Go > Java > Ruby > C# > JavaScript.

3. **Generate red flags**
   - Stack-specific security patterns (SQL injection variants, bcrypt sync usage, etc.).
   - Universal red flags (hardcoded credentials, TODO security markers).

4. **Write output**
   - Save JSON to @OUTPUT_PATH.
   - If output already exists and @FORCE_REFRESH is false, reuse it.

## Output

```json
{
  "generatedAt": "2025-10-30T14:30:00Z",
  "stack": {
    "backend": "Express.js",
    "frontend": "React",
    "database": "SQLite",
    "language": "TypeScript"
  },
  "redFlags": [
    "SQL injection",
    "hardcoded secret",
    "bcrypt sync",
    "dangerouslySetInnerHTML"
  ]
}
```
