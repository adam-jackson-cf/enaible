# Agentic Readiness Assessment Rules

Source: AI SDLC Engineering Guidelines v1 (6 January 2026)

These rules are used to assess codebase adoption and adherence to agentic engineering guidelines.

---

## 1. Implementation as First Class Documentation

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

## 2. Coding Guidance via System Docs

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

## 3. Global Context Hygiene

**Intent:** Minimize context footprint through progressive disclosure, concise system files, and deterministic scripts so sessions stay lean and auditable.

### Assessment Rules

| ID    | Rule                                                   | Signals Present                                            | Signals Absent                                |
| ----- | ------------------------------------------------------ | ---------------------------------------------------------- | --------------------------------------------- |
| GCH-1 | Tools provide context transparency                     | Visible context usage, action history                      | Obfuscated context, hidden actions            |
| GCH-2 | No persistent MCP configs for stable workflows         | Bash/scripts for permanent flows, MCP only for experiments | MCP registrations used for ongoing automation |
| GCH-3 | Sessions kept lean (<40% context)                      | Session management practices                               | Bloated, long-running sessions                |
| GCH-4 | Planning/build execution separated                     | Distinct plan vs build sessions                            | Planning and execution intermingled           |
| GCH-5 | Planning artifacts stored externally                   | Files/docs outside the session window                      | Plans only in transient context               |
| GCH-6 | System rules concise & progressive disclosure          | Minimal AGENTS.md with layered references                  | Rules crammed into single oversized files     |
| GCH-7 | Permanent workflows scripted with clear I/O            | Makefiles, CLI commands, documented inputs/outputs         | Workflows only described in prompts           |
| GCH-8 | Token usage controlled                                 | Caching, trimmed prompts, context windows monitored        | No awareness of token/latency cost            |
| GCH-9 | Tasks encapsulated (start → action → complete → reset) | Clear task boundaries and reset rituals                    | Open-ended sessions without hygiene           |

---

## 4. Verification as First Class Requirement

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

## 5. Observability - Empower LLMs with Feedback

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

| Category                        | Rule Count | Focus Area                  |
| ------------------------------- | ---------- | --------------------------- |
| Implementation as Documentation | 5          | Documentation efficiency    |
| Coding Guidance via System Docs | 6          | Rule quality and automation |
| Global Context Hygiene          | 9          | Context minimization        |
| Verification as First Class     | 7          | Quality assurance           |
| Observability                   | 7          | Feedback mechanisms         |

**Total Assessment Rules: 34**
