# Agentic Readiness Assessment Rules

Source: AI SDLC Engineering Guidelines v1 (6 January 2026)

These rules are used to assess codebase adoption and adherence to agentic engineering guidelines.

---

## 1. Verified Starting Base

**Intent:** Start from a known-good baseline before introducing agentic changes.

### Assessment Rules

| ID    | Rule                                                   | Signals Present                                                         | Signals Absent                             |
| ----- | ------------------------------------------------------ | ----------------------------------------------------------------------- | ------------------------------------------ |
| VSB-1 | Project uses maintained templates or proven generators | Package.json with established framework CLI, standard project structure | Custom scaffolding, non-standard layouts   |
| VSB-2 | Baseline builds pass before agentic work               | CI passing on main branch, build scripts present                        | Broken builds, missing build configuration |
| VSB-3 | Baseline tests pass before agentic work                | Test suite exists and passes, test coverage present                     | No tests, failing tests on main            |
| VSB-4 | Dependencies are version-pinned                        | Lock files present (package-lock.json, poetry.lock, etc.)               | Missing lock files, unpinned versions      |
| VSB-5 | Toolchain versions are pinned                          | .nvmrc, .python-version, tool-versions present                          | No version pinning for runtime/toolchain   |

---

## 2. Implementation as First Class Documentation

**Intent:** Minimize documentation overhead and doc drift risk by using implementation as the source of truth.

### Assessment Rules

| ID     | Rule                                                                | Signals Present                                       | Signals Absent                          |
| ------ | ------------------------------------------------------------------- | ----------------------------------------------------- | --------------------------------------- |
| IFCD-1 | Shared prompts exist for project onboarding                         | Onboarding prompt files, knowledge extraction prompts | Only traditional docs for onboarding    |
| IFCD-2 | No redundant documentation that duplicates inferable implementation | Minimal README, no excessive inline docs              | Extensive docs repeating code behavior  |
| IFCD-3 | AGENTS.md contains only high-level repo map                         | Concise structure overview                            | Verbose implementation details          |
| IFCD-4 | AGENTS.md contains non-standard workflows                           | Project-specific processes documented                 | Standard workflows over-documented      |
| IFCD-5 | System docs complement automated processes                          | Rules that extend linting/tooling                     | Rules that duplicate linting capability |

---

## 3. Coding Guidance via System Docs

**Intent:** Use system docs for guidance where deterministic tools are insufficient.

### Assessment Rules

| ID     | Rule                                             | Signals Present                          | Signals Absent                                 |
| ------ | ------------------------------------------------ | ---------------------------------------- | ---------------------------------------------- |
| CGSD-1 | Rules are binary (true/false) without exceptions | Clear, unambiguous rules                 | Rules with caveats and exceptions inline       |
| CGSD-2 | Rules are minimal and use progressive disclosure | Concise rule sets, layered documentation | Bloated rule files, everything upfront         |
| CGSD-3 | Deterministic tools preferred over rules         | Linting configs enforce standards        | Rules substitute for possible automation       |
| CGSD-4 | Conceptual rules include good/bad examples       | Examples accompany non-obvious rules     | Abstract rules without demonstration           |
| CGSD-5 | Rules favor verifiable metrics                   | Cyclomatic complexity limits, LOC limits | Subjective guidance ("keep it simple")         |
| CGSD-6 | No redundant pattern/framework rules             | Absence of SOLID, DRY mentions           | Explicit pattern rules already in LLM training |

---

## 4. Planning is Fundamental

**Intent:** Agentic tasks start with explicit intent, constraints, and acceptance checks.

### Assessment Rules

| ID    | Rule                                 | Signals Present                                | Signals Absent                         |
| ----- | ------------------------------------ | ---------------------------------------------- | -------------------------------------- |
| PIF-1 | Tasks have clear goals and non-goals | Documented objectives, scope boundaries        | Vague or missing task definitions      |
| PIF-2 | Constraints are explicit             | Security, compliance, client limits documented | Implicit assumptions about constraints |
| PIF-3 | Acceptance criteria defined          | Measurable success conditions                  | No definition of done                  |
| PIF-4 | Verification plan exists             | Local/CI test plan, expected outcomes          | Ad-hoc verification approach           |
| PIF-5 | Planning separated from execution    | Planning artifacts in separate context         | Large plans polluting build sessions   |
| PIF-6 | Plans reviewed before execution      | PR review process, plan approval workflow      | Direct execution without review        |

---

## 5. Context Efficiency

**Intent:** Keep context minimal to complete tasks successfully without diluting critical information.

### Assessment Rules

| ID   | Rule                                                   | Signals Present                            | Signals Absent                              |
| ---- | ------------------------------------------------------ | ------------------------------------------ | ------------------------------------------- |
| CE-1 | Tools provide context transparency                     | Visible context usage, action history      | Obfuscated context, hidden actions          |
| CE-2 | MCP avoided for permanent workflows                    | Bash implementations for stable workflows  | Heavy MCP usage for non-experimental tasks  |
| CE-3 | Context sessions kept lean (<40% threshold)            | Session management practices               | Bloated, long-running sessions              |
| CE-4 | Planning and build execution separated                 | Distinct sessions for planning vs building | Mixed planning/execution in same context    |
| CE-5 | Planning artifacts stored externally                   | Files/docs outside context window          | Plans only in session memory                |
| CE-6 | System files not overly polluted                       | Minimal AGENTS.md, progressive disclosure  | Large system files with everything included |
| CE-7 | Rules automated where possible                         | Linting/tooling over documentation         | Manual rule enforcement via docs            |
| CE-8 | Tasks encapsulated (start > action > complete > reset) | Clear task boundaries, session hygiene     | Open-ended, unbounded sessions              |

---

## 6. Verification as First Class Requirement

**Intent:** Verification at all stages via deterministic actions that cannot be bypassed.

### Assessment Rules

| ID     | Rule                                     | Signals Present                           | Signals Absent                     |
| ------ | ---------------------------------------- | ----------------------------------------- | ---------------------------------- |
| VFCR-1 | Local verification mirrors CI            | Matching test/lint configs locally and CI | Divergent local vs CI verification |
| VFCR-2 | Integration/smoke tests included         | E2E or integration test presence          | Unit tests only                    |
| VFCR-3 | Automated code reviews configured        | PR review automation, LLM review rules    | Manual-only code review            |
| VFCR-4 | Verification proportional to risk        | Risk-based test coverage                  | One-size-fits-all verification     |
| VFCR-5 | Early regression detection               | Pre-commit hooks, fast feedback loops     | Late-stage only verification       |
| VFCR-6 | Quality exceptions reviewed and codified | Exception tracking, rule updates          | Ad-hoc exception handling          |
| VFCR-7 | Verification cannot be bypassed          | No skip flags, enforced gates             | Bypassable quality checks          |

---

## 7. Agentic Harnesses

**Intent:** Prefer transparent, inspectable tooling where prompts and execution are visible.

### Assessment Rules

| ID   | Rule                                 | Signals Present                             | Signals Absent                         |
| ---- | ------------------------------------ | ------------------------------------------- | -------------------------------------- |
| AH-1 | System prompts visible and versioned | Versioned prompt files, visible configs     | Hidden or proprietary prompts          |
| AH-2 | Tool configuration versioned         | Config in source control                    | Unversioned tool settings              |
| AH-3 | Workflows reproducible               | Same inputs produce same outputs            | Non-deterministic workflows            |
| AH-4 | Open-source harnesses preferred      | OSS tooling where practical                 | Proprietary lock-in without mitigation |
| AH-5 | LLM actions have visibility          | Logging, audit trails for AI actions        | Black-box AI operations                |
| AH-6 | Vendor lock-in avoided               | Portable configurations, abstraction layers | Deep vendor-specific integrations      |

---

## 8. Complement LLM with Deterministic Code

**Intent:** Minimize context pollution with code-based workflows; mitigate LLM weaknesses.

### Assessment Rules

| ID     | Rule                                     | Signals Present                            | Signals Absent                        |
| ------ | ---------------------------------------- | ------------------------------------------ | ------------------------------------- |
| CLDC-1 | Permanent workflows are scripts/commands | Makefile, task runners, shell scripts      | Workflows only in prompts/docs        |
| CLDC-2 | Scripts have clear inputs/outputs        | Documented CLI interfaces                  | Implicit or undocumented I/O          |
| CLDC-3 | Tooling mitigates LLM weaknesses         | Deduplication tools, structure enforcement | Reliance on LLM consistency           |
| CLDC-4 | Token costs actively reduced             | Efficient context usage, caching           | No consideration for token efficiency |
| CLDC-5 | Code duplication detection in place      | Automated review catches duplicates        | Manual duplicate detection only       |
| CLDC-6 | God class prevention measures            | Size limits, complexity checks             | No structural guardrails              |

---

## 9. Observability - Empower LLMs with Feedback

**Intent:** Provide mechanisms for LLMs to get feedback and course correct.

### Assessment Rules

| ID    | Rule                                     | Signals Present                                        | Signals Absent                       |
| ----- | ---------------------------------------- | ------------------------------------------------------ | ------------------------------------ |
| OBS-1 | Dev logs accessible to agents            | Make commands for log access, documented log locations | Logs inaccessible or undocumented    |
| OBS-2 | Quality gates provide automated feedback | Linting with actionable output, test feedback          | Silent or unclear failures           |
| OBS-3 | Pre-commit hooks configured              | Husky, pre-commit, or equivalent present               | No pre-commit validation             |
| OBS-4 | LSP feedback explored                    | Language server integration                            | No symbol-level feedback             |
| OBS-5 | Stop hooks for JIT quality checks        | Agent stop hooks configured                            | No just-in-time verification         |
| OBS-6 | UI testing with screenshot capture       | Playwright, component capture libraries                | No visual regression capability      |
| OBS-7 | Native libraries over MCP for testing    | Direct library usage (React Grab, etc.)                | MCP wrappers for standard operations |

---

## Summary: Assessment Categories

| Category                               | Rule Count | Focus Area                  |
| -------------------------------------- | ---------- | --------------------------- |
| Verified Starting Base                 | 5          | Project foundation quality  |
| Implementation as Documentation        | 5          | Documentation efficiency    |
| Coding Guidance via System Docs        | 6          | Rule quality and automation |
| Planning is Fundamental                | 6          | Task structure and review   |
| Context Efficiency                     | 8          | Context management          |
| Verification as First Class            | 7          | Quality assurance           |
| Agentic Harnesses                      | 6          | Tooling transparency        |
| Complement LLM with Deterministic Code | 6          | Workflow automation         |
| Observability                          | 7          | Feedback mechanisms         |

**Total Assessment Rules: 56**
