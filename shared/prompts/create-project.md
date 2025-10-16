# Purpose

Scaffold a new project with the Better-T-Stack CLI using either explicit technology selections or analysis of an existing todos file.

## Variables

| Token/Flag         | Type                     | Description                                                       |
| ------------------ | ------------------------ | ----------------------------------------------------------------- |
| `$PROJECT_NAME`    | positional #1 (REQUIRED) | Name of the project to scaffold.                                  |
| `$PLAN_FILE`       | positional #2 (optional) | Path to a todos/plan file when using `--from-plan`.               |
| `TECH_ARGUMENTS[]` | config (optional)        | Additional technology selections parsed from the remaining input. |

## Instructions

- ALWAYS confirm the project name and target directory before running the generator.
- NEVER guess technology mappings; derive them from explicit arguments or todos analysis.
- When analyzing todos, document the detection logic and resulting stack choices.
- Present a full configuration summary and obtain user confirmation prior to execution.
- After generation, run the project’s health checks and report outcomes.

## Workflow

1. Parse inputs
   - Extract `PROJECT_NAME`.
   - Detect `--from-plan`; set `MODE` and capture `PLAN_FILE`.
   - Collect remaining arguments into `TECH_ARGUMENTS[]`.
2. Gather requirements
   - If `MODE="plan"`:
     - Read `PLAN_FILE`.
     - Identify technology keywords (React Native, Expo, Zustand, OAuth, WebSocket, etc.).
     - Map findings to Better-T-Stack options.
   - Else `MODE="direct"`:
     - Interpret each tech choice from `$ARGUMENTS` as a technology or flag; validate against supported sets.
3. Validate environment
   - Ensure Node/NPM/Bun availability as required by the selected stack.
   - Confirm target directory (`./<PROJECT_NAME>`) does not already exist.
4. Present proposed configuration
   - Build the command:
     ```
     npx create-better-t-stack@latest <PROJECT_NAME> <mapped-flags>
     ```
   - Display a table of components (Frontend, Backend, Runtime, Database, ORM, Auth, Addons) with their mapped values.
   - **STOP:** “Project setup details ready. Proceed with Better-T-Stack initialization? (y/n)”
5. Execute scaffold
   - Run the composed CLI command.
   - Capture stdout/stderr for reporting.
6. Post-setup actions
   - `cd <PROJECT_NAME>`; install dependencies (`bun install` or tool specified in package.json).
   - Run initial quality gates: `bun run dev` (or equivalent), `bun run check-types`, `bun run build`.
7. Summarize results
   - Provide success/failure status for each command.
   - Record next steps (e.g., configure env vars, initialize git).

## Output

```md
# RESULT

- Summary: Project "<PROJECT_NAME>" scaffolded with Better-T-Stack.

## STACK

| Component | Selection | Source  |
| --------- | --------- | ------- | ------ |
| Frontend  | <value>   | <direct | todos> |
| Backend   | <value>   | <direct | todos> |
| Runtime   | <value>   | <direct | todos> |
| Database  | <value>   | <direct | todos> |

## COMMANDS RUN

- `npx create-better-t-stack@latest ...` → <pass|fail>
- `<install command>` → <pass|fail>
- `<dev command>` → <pass|fail>
- `<type/build checks>` → <pass|fail>

## NEXT STEPS <!-- optional: if no next steps dont output this section to user -->

1. <Action item (e.g., configure environment variables)>
2. <Action item>
```

## Examples

```bash
# Direct technology selection
/create-project acme-dashboard react-router hono bun sqlite drizzle

# Infer stack from todos file
/create-project mobile-app --from-plan ./.workspace/execplan.md
```
