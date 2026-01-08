# Specification

> The complete format specification for Agent Skills.

This document defines the Agent Skills format for shared skills in this repository and the generated adapters we ship.

## Directory + naming rules

1. Author shared skills under `shared/skills/<skill-name>/`. Rendered artifacts land under `systems/<adapter>/skills/...`; downstream runtimes install them under their own managed tree (e.g., `~/<system-folder>/skills/<skill-name>/`).
2. The folder name must match the `name` frontmatter field exactly. Names use lowercase letters, numbers, and single hyphens only; no leading, trailing, or consecutive hyphens.
3. Minimum contents: a single `SKILL.md`. Optional siblings—`scripts/`, `references/`, `assets/`—must stay inside the skill directory. Skills must never rely on files outside their own tree.
4. Keep every skill self-contained so it can be copied verbatim into another runtime without missing assets.

<Tip>
  Treat each skill directory as a portable package: anything an agent needs (templates, scripts, examples) should live alongside `SKILL.md`.
</Tip>

## SKILL.md format

The `SKILL.md` file must contain YAML frontmatter followed by Markdown instructions.

### Frontmatter (required)

```yaml theme={null}
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

With optional fields:

```yaml theme={null}
---
name: pdf-processing
description: Extract text and tables from PDF files. USE WHEN the user needs PDF parsing, form fill, or merges.
compatibility: Requires Python 3.12+, git, and internet access.
license: Apache-2.0
metadata:
  author: example-org
  version: "1.0"
allowed-tools: Bash(git:*) Bash(jq:*) Read
---
```

| Field           | Required | Constraints                                                                                                       |
| --------------- | -------- | ----------------------------------------------------------------------------------------------------------------- |
| `name`          | Yes      | 1-64 chars. Lowercase letters, numbers, single hyphens. Matches folder name; no leading/trailing/consecutive `-`. |
| `description`   | Yes      | 1-1024 chars. Describe what the skill does **and** when to use it. Include an explicit `USE WHEN ...` clause.     |
| `license`       | No       | License identifier or reference to a bundled license file.                                                        |
| `compatibility` | No       | ≤500 chars. List environment requirements (product, runtimes, packages, network, API keys).                       |
| `metadata`      | No       | Map of string keys/values for implementation-specific metadata.                                                   |
| `allowed-tools` | No       | Space-delimited list of tools pre-approved for this skill (experimental; support varies by adapter).              |

#### `name` field

- Must be 1-64 characters
- Only lowercase letters, digits, and single hyphens (`a-z`, `0-9`, `-`)
- Cannot start or end with `-`
- Cannot contain `--`
- Must match the parent directory name exactly

Valid examples:

```yaml theme={null}
name: pdf-processing
```

```yaml theme={null}
name: data-analysis
```

Invalid examples:

```yaml theme={null}
name: PDF-Processing
```

```yaml theme={null}
name: -pdf
```

```yaml theme={null}
name: pdf--processing
```

#### `description` field

- 1-1024 characters
- Describe capabilities plus triggers ("USE WHEN ...") so the dispatcher knows when to route to the skill
- Include keywords that match likely user phrasing

Good example:

```yaml theme={null}
description: Extracts text and tables from PDFs, fills PDF forms, and merges files. USE WHEN users mention PDFs, forms, or document extraction workflows.
```

Poor example:

```yaml theme={null}
description: Helps with PDFs.
```

#### `license` field

- Optional license identifier or reference to a bundled file (e.g., `LICENSE.txt`)
- Keep it short; details belong in a dedicated file if needed

#### `compatibility` field

- Optional, 1-500 characters
- Describe only the environment requirements that are **not** bundled with the skill (e.g., runtimes, packages, network access, API keys, adapter-specific constraints)
- Skip internal assets that ship with the skill (e.g., scripts inside `scripts/`) and anything already guaranteed by the base repo setup
- Mention adapters explicitly when relevant ("Designed for Claude Code")

#### `metadata` field

- Optional map from string keys to string values
- Useful for author info, versions, feature flags, or migration metadata
- Keep keys namespaced enough to avoid collisions (`enaible-author`, `enaible-version`)

#### `allowed-tools` field

- Optional space-delimited list describing pre-approved tool invocations (tool names and scopes are adapter specific)
- Format: `ToolName(arg-scope)` or bare tool name depending on adapter support
- Use sparingly; most skills rely on the global tool policy instead of whitelists
- Reference tools via the shared tokens (e.g., `@BASH`, `@READ`, `@WRITE`) instead of hardcoding system names. The renderer swaps these tokens for each adapter’s tool identifiers. See [docs/system/allowed-tools.md](./system/allowed-tools.md) for the canonical token list and per-system mappings.

Example:

```yaml
allowed-tools: @BASH(git:*) @READ(./path|glob) @WRITE
```

### Body content

The Markdown body after the frontmatter is the skill’s operational guide. Agents load the entire file when activating the skill, so prioritize clarity and brevity.

#### Body structure guidance

1. **Title block**: Begin with `# <skill-name>` followed by a short paragraph describing the mission, then a bulleted list of primary use cases.
2. **Optional quick-reference table**: Add a `## Need to...? Read This` section mapping common goals to reference files or scripts when the skill has multiple sub-workflows.
3. **Workflow**: Present the core flow as `## Workflow` with numbered `### Step N: <title>` subsections. Each step should include:
   - **Purpose** sentence
   - **When** to run (if conditional)
   - Bullet list of actions
   - Links to supporting reference files or scripts
4. **Step 0 (preflight)**: Include only if prerequisites exist beyond the default repo/toolchain state. State how to fail fast when prerequisites are missing.
5. Keep `SKILL.md` under ~500 lines. Move deeper, step-by-step instructions (including any checkpoint or approval requirements) into files inside `references/` or `assets/` to preserve context budget.

Document at a high level in `SKILL.md` when human approval is required, but reserve the detailed checkpoint flow for the referenced files that describe each step.

#### Workflow example (abbreviated)

```markdown
# Codify PR Reviews

- You want to codify recurring feedback into instruction rules.
- You need human approval before rules change.

## Workflow

### Step 0: Preflight checks

**Purpose**: Ensure required inputs exist before any processing.

### Step 1: Establish run directories

**Purpose**: Create deterministic artifact roots.
```

Adopt this pattern for every shared skill so adapters render consistent experiences.

## Optional directories

### scripts/

Executable helpers the skill can invoke. Scripts should:

- Be self-contained or describe dependencies explicitly
- Provide clear error messages and exit codes
- Target portable runtimes (Python, Bash, Node) supported by all adapters that ship the skill

### references/

Supplemental documentation loaded on demand:

- Deep workflows, troubleshooting, templates, or forms
- Keep files focused and under control; agents fetch them individually
- Document success criteria, examples, and any mandatory checkpoint instructions in these files using markers like `@ASK_USER_CONFIRMATION`

### assets/

Static resources and templates (images, JSON schemas, lookup tables). Reference them with relative paths from `SKILL.md`.

## Progressive disclosure

Design every skill for staged loading:

1. **Metadata (~100 tokens)**: `name` + `description` let dispatchers decide whether to activate the skill.
2. **Instructions (< 500 lines)**: The full `SKILL.md` body provides the high-level workflow and pointers to deeper references.
3. **References (as needed)**: Agents load files from `scripts/`, `references/`, or `assets/` only when a workflow step calls for them.
4. **Reference depth**: Detailed references should declare success criteria, common pitfalls, examples, and any approval checkpoints so agents can verify outcomes without reopening `SKILL.md` repeatedly.

## File references

Reference supporting files with relative links from the skill root:

```markdown theme={null}
See [stack analysis workflow](references/stack-analysis.md) before Step 2.
Run `scripts/extract.py` to gather evidence.
```

Keep reference chains shallow—`SKILL.md` → reference file → (optional) asset. Avoid multi-hop nesting. Place checkpoint requirements or expected outputs inside the referenced document.

## Validation

Use `enaible skills lint` to confirm your skill meets the standard:

```bash theme={null}
uv run --project tools/enaible enaible skills lint
uv run --project tools/enaible enaible skills validate
```

---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://agentskills.io/llms.txt
