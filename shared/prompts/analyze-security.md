# Purpose

Execute a comprehensive security assessment that blends automated OWASP-aligned scanning with contextual gap analysis, risk prioritization, and actionable remediation tasks.

## Variables

- `TARGET_PATH` ← first positional argument; defaults to `.`.
- `VERBOSE_MODE` ← boolean flag set when `--verbose` is provided.
- `SCRIPT_PATH` ← resolved security analyzer directory.
- `$ARGUMENTS` ← complete raw argument string for logging.

## Instructions

- ALWAYS conduct automated scanning before manual analysis; abort if scripts or imports fail.
- Enforce every STOP confirmation (`Automated`, `Gap Assessment`, `Risk Prioritization`, `Todo Transfer`) before proceeding.
- Map findings to OWASP Top 10 categories, business impact, and exploitability.
- Maintain immutable evidence—store JSON results, command transcripts, and severity scoring.
- In `VERBOSE_MODE`, include exhaustive vulnerability details, gap tables, and remediation notes.

## Workflow

1. Locate analyzer scripts
   - Run `ls .claude/scripts/analyzers/security/*.py || ls "$HOME/.claude/scripts/analyzers/security/"`; if both fail, prompt the user for a directory containing `semgrep_analyzer.py` and `detect_secrets_analyzer.py`, and exit if none is provided.
2. Prepare environment
   - Compute `SCRIPTS_ROOT="$(cd "$(dirname "$SCRIPT_PATH")/../.." && pwd)"` and run `PYTHONPATH="$SCRIPTS_ROOT" python -c "import core.base; print('env OK')"`; exit immediately if it fails.
3. Phase 1 — Automated Security Assessment
   - Execute sequentially:
     - `security:semgrep` (installs on-demand if permitted)
     - `security:detect_secrets`
   - Summarize findings against OWASP categories.
   - **STOP:** “Automated security analysis complete. Proceed with gap assessment? (y/n)”
4. Phase 2 — Gap Assessment & Contextual Analysis
   - Review coverage vs. OWASP Top 10 and stack-specific concerns.
   - Perform targeted searches or manual inspections for uncovered areas (auth flows, configuration, data flow).
   - Document technology-specific validations (e.g., Django CSRF, React XSS mitigations, Express headers).
   - **STOP:** “Gap assessment and contextual analysis complete. Proceed with risk prioritization? (y/n)”
5. Phase 3 — Risk Prioritization & Reporting
   - Combine automated and contextual findings.
   - Prioritize vulnerabilities (Critical/High/Medium/Low) using impact and likelihood.
   - Draft remediation roadmap (Phase 1 critical fixes, Phase 2 high priorities, Phase 3 hardening).
   - **STOP:** “Security analysis complete and validated. Transfer findings to todos.md? (y/n)”
6. Phase 4 — Quality Validation & Task Transfer
   - Confirm quality gates:
     - OWASP Top 10 coverage verified.
     - Script outputs processed and validated.
     - Technology-specific patterns reviewed.
     - Business logic risks evaluated.
   - Upon approval, append remediation tasks to `todos.md` following the provided checklist format.
   - Document whether transfer occurred or was declined.

## Output

```md
# RESULT

- Summary: Security analysis completed for <TARGET_PATH>.

## FINDINGS

| Severity | Category (OWASP)            | Location / Asset                | Description                          | Evidence Source         |
| -------- | --------------------------- | ------------------------------- | ------------------------------------ | ----------------------- |
| CRITICAL | A01: Injection              | services/api/user.py#L120       | Unsanitized SQL string concatenation | security:semgrep        |
| HIGH     | A02: Cryptographic Failures | config/settings.py#L45          | Hardcoded API key                    | security:detect_secrets |
| MEDIUM   | A05: SSRF                   | infra/terraform/modules/network | Missing egress restrictions          | Gap Assessment          |

## RISK SUMMARY

- Scorecard: <overall risk score or narrative>
- Blocking Issues: <list of critical/high items>
- Recommended Timeline: <immediate / short-term / long-term>

## REMEDIATION ROADMAP

### Phase 1: Critical Security Issues

- [ ] <Task with owner and file path>

### Phase 2: High Priority Security Issues

- [ ] <Task>

### Phase 3: Security Hardening

- [ ] <Task>

## ATTACHMENTS

- security:semgrep → <path>
- security:detect_secrets → <path>
- Gap Analysis Notes → <path>
```

## Examples

```bash
# Run default security assessment
/analyze-security .

# Include verbose gap tables and detailed findings
/analyze-security services/web --verbose
```
