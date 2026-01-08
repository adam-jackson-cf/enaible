# Purpose

Assess agentic readiness and maintenance by scoring consistency, parallelizability, enforcement alignment, and principle risks using deterministic artifacts and KPI formulas.

## Variables

### Required

- @TARGET_PATH = $1 — path to analyze; defaults to repo root

### Optional (derived from $ARGUMENTS)

- @AUTO = --auto — skip STOP confirmations (auto-approve checkpoints)
- @DAYS = --days — history window for concentration and docs freshness (default 180)
- @MIN_SEVERITY = --min-severity — defaults to "low"; accepts critical|high|medium|low
- @EXCLUDE = --exclude [repeatable] — additional glob patterns to exclude

### Derived (internal)

- @ARTIFACT_ROOT = <derived> — timestamped artifacts directory for readiness evidence
- @TARGET_ABS = <derived> — absolute path to the target directory
- @PROJECT_ROOT = <derived> — absolute path to the repo root

## Instructions

- ALWAYS run Enaible analyzers via the CLI (uv + enaible); never import analyzer modules directly.
- Store raw analyzer outputs plus derived metrics under `.enaible/artifacts/analyze-agentic-readiness/`.
- Always read artifacts via absolute paths derived from `@ARTIFACT_ROOT` (avoid relative `.enaible/...` reads).
- Reuse the standard exclusion list (`dist/`, `build/`, `node_modules/`, `__pycache__/`, `.next/`, `vendor/`, `.venv/`, `.mypy_cache/`, `.ruff_cache/`, `.pytest_cache/`, `.gradle/`, `target/`, `bin/`, `obj/`, `coverage/`, `.turbo/`, `.svelte-kit/`, `.cache/`, `.enaible/artifacts/`) whenever you run analyzers or helper scripts; merge it with user-provided @EXCLUDE flags instead of editing fixtures.
- Respect `@MIN_SEVERITY` for reporting; do not rerun analyzers at a lower severity to fish for more findings.
- Run reconnaissance before analyzers so exclusions and stack detection are ready up front.
- Invoke the shared deterministic scripts for recon, inventory, risk scans, and KPI math exactly as documented; do not inline their logic in the prompt.
- Support the Enaible language targets listed in `README.md`: Python, TypeScript, Go, Rust, C#.
- Do not modify repository files; collect evidence only.
- Respect STOP confirmations unless @AUTO is provided; when auto is active, treat checkpoints as approved without altering other behavior.
- After synthesis, explicitly identify gaps in deterministic tool coverage and backfill where possible.

## Workflow

1. **Establish artifacts directory**
   - Resolve the repo root, target path, and artifact root:

     ```bash
     PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
     TARGET_PATH="@TARGET_PATH"
     if [ -z "$TARGET_PATH" ] || [ "$TARGET_PATH" = "." ]; then
       TARGET_PATH="$PROJECT_ROOT"
     elif [ "${TARGET_PATH#/}" = "$TARGET_PATH" ]; then
       TARGET_PATH="$PROJECT_ROOT/$TARGET_PATH"
     fi
     TARGET_ABS="$(cd "$TARGET_PATH" && pwd)"
     ARTIFACT_ROOT="$PROJECT_ROOT/.enaible/artifacts/analyze-agentic-readiness/$(date -u +%Y%m%dT%H%M%SZ)"
     mkdir -p "$ARTIFACT_ROOT"
     export PROJECT_ROOT TARGET_ABS ARTIFACT_ROOT
     export DAYS="@DAYS"
     TIMING_LOG="${AGENTIC_READINESS_TIMING_LOG:-/tmp/agentic_readiness_test.log}"
     : > "$TIMING_LOG"
     export AGENTIC_READINESS_TIMING_LOG="$TIMING_LOG"
     run_with_timing() {
       phase="$1"
       shift
       python shared/context/agentic_readiness/timing.py --phase "$phase" -- "$@"
     }
     ```

2. **Reconnaissance (language + repo map)**
   - Run the shared recon script to detect supported stacks, map top-level directories, and log applied exclusions:

     ```bash
     run_with_timing helper:recon python shared/context/agentic_readiness/recon_map.py "$TARGET_ABS" "$ARTIFACT_ROOT"
     ```

   - Artifacts: `recon.json`, `repo-map.json`.

3. **Run analyzers (consistency + coupling + complexity)**
   - Build an auto-exclusion array from the recon list and merge it with any caller-supplied `@EXCLUDE` flags:

     ```bash
     AUTO_EXCLUDES=(
       "--exclude" "dist/"
       "--exclude" "build/"
       "--exclude" "node_modules/"
       "--exclude" "__pycache__/"
       "--exclude" ".next/"
       "--exclude" "vendor/"
       "--exclude" ".venv/"
       "--exclude" ".mypy_cache/"
       "--exclude" ".ruff_cache/"
       "--exclude" ".pytest_cache/"
       "--exclude" ".gradle/"
       "--exclude" "target/"
       "--exclude" "bin/"
       "--exclude" "obj/"
       "--exclude" "coverage/"
       "--exclude" ".turbo/"
       "--exclude" ".svelte-kit/"
       "--exclude" ".cache/"
       "--exclude" ".enaible/artifacts/"
     )
     ```

   - Execute each Enaible command, storing JSON output beneath @ARTIFACT_ROOT:

     ```bash
     run_with_timing analyzer:jscpd env ENAIBLE_REPO_ROOT="$PROJECT_ROOT" uv run --directory tools/enaible enaible analyzers run quality:jscpd \
       --target "$TARGET_ABS" \
       --min-severity "@MIN_SEVERITY" \
       --out "$ARTIFACT_ROOT/quality-jscpd.json" \
       "${AUTO_EXCLUDES[@]}" \
       @EXCLUDE

     run_with_timing analyzer:coupling env ENAIBLE_REPO_ROOT="$PROJECT_ROOT" uv run --directory tools/enaible enaible analyzers run architecture:coupling \
       --target "$TARGET_ABS" \
       --min-severity "@MIN_SEVERITY" \
       --out "$ARTIFACT_ROOT/architecture-coupling.json" \
       "${AUTO_EXCLUDES[@]}" \
       @EXCLUDE

     run_with_timing analyzer:lizard env ENAIBLE_REPO_ROOT="$PROJECT_ROOT" uv run --directory tools/enaible enaible analyzers run quality:lizard \
       --target "$TARGET_ABS" \
       --min-severity "@MIN_SEVERITY" \
       --out "$ARTIFACT_ROOT/quality-lizard.json" \
       "${AUTO_EXCLUDES[@]}" \
       @EXCLUDE
     ```

4. **Inventory tests and quality gates (local + CI parity + enforcement)**
   - Run the shared inventory script to enumerate test directories/frameworks and capture CI/local/pre-commit gate coverage:

     ```bash
     run_with_timing helper:inventory python shared/context/agentic_readiness/inventory_tests_gates.py "$TARGET_ABS" "$ARTIFACT_ROOT"
     ```

   - Artifacts: `tests-inventory.json`, `quality-gates.json` (with lint/test enforcement, parity gaps, and gate hits).

5. **Documentation risk + review standards**
   - Run the docs-risk script to flag enforceable guidance that isn’t encoded in linting and capture LLM review standards:

     ```bash
     run_with_timing helper:docs_risk python shared/context/agentic_readiness/docs_risk.py "$TARGET_ABS" "$ARTIFACT_ROOT" "$ARTIFACT_ROOT/quality-gates.json"
     ```

   - Artifact: `docs-risk.json` (includes risk reasons plus lists of docs and hits).

6. **Scan for MCP configuration**
   - Run the MCP scan script; MCP registration is an automatic readiness risk:

     ```bash
     run_with_timing helper:mcp_scan python shared/context/agentic_readiness/mcp_scan.py "$TARGET_ABS" "$ARTIFACT_ROOT"
     ```

   - Artifact: `mcp-scan.json`.

7. **Compute concentration + docs freshness**
   - Use the shared Git-based script (respects @DAYS window) to capture change concentration plus documentation freshness:

     ```bash
     run_with_timing helper:history_docs python shared/context/agentic_readiness/history_docs.py "$TARGET_ABS" "$ARTIFACT_ROOT" "${DAYS:-180}"
     ```

   - Artifacts: `history-concentration.json`, `docs-freshness.json` (used later for maintenance).

8. **Compute Agentic Readiness KPI**
   - Run the readiness score script (consumes analyzer + inventory artifacts) to generate `agentic-readiness.json`:

     ```bash
     run_with_timing helper:readiness_score python shared/context/agentic_readiness/readiness_score.py "$ARTIFACT_ROOT"
     ```

   **Scoring Primer**
   - Formula: `S = round(0.7*O + 0.3*A, 1)`
   - Anchor A (single definition): `10/8/5/2/0 = Excellent/Strong/Adequate/Weak/Critical`
   - Normalization: each signal → `[0,1]` by clamping between good (=1) and bad (=0); lower-is-better uses `norm = clamp((bad − x)/(bad − good))`
   - Objective score: `O = Σ w_i * norm_i` (weights sum to 1)

   **Agentic Readiness**
   - Signals (w): consistency `0.20`; parallelizability `0.20`; lint_enforced `0.20`; tests_enforced `0.20`; ci_local_parity `0.10`; doc_risk `0.05`; mcp_risk `0.05`
   - Thresholds (bad ≥): dup `20%`; coupling `2.0`; concentration `0.5`
   - Normalization: lower is better for structural signals; enforcement/parity/risk are binary (`1` good, `0` bad)
   - Use artifact-derived signals only; anchors are reviewer judgment applied once per KPI

9. **Compute Maintenance Score**
   - Run the maintenance score script to generate `maintenance-score.json` (duplication + complexity + concentration signals):

     ```bash
     run_with_timing helper:maintenance_score python shared/context/agentic_readiness/maintenance_score.py "$ARTIFACT_ROOT"
     ```

   - Interpretation guidance mirrors the readiness scoring (objective score only; anchors applied during reporting).

10. **Deliver report**

- Summarize agentic readiness and maintenance, include KPI scores, list contributing signals, and reference artifact files directly.
- Call out gaps in lint/test enforcement, CI/local parity, doc risks, and MCP findings.

## Output

```md
# RESULT

- Summary: Agentic readiness assessment completed for <@TARGET_PATH>.
- Artifacts: `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/`

## RECONNAISSANCE

- Supported languages detected: <Python | TypeScript | Go | Rust | C#>
- Auto-excluded: <patterns applied>

## IMPLEMENTATION MAP

| Path  | Category |
| ----- | -------- | -------- | ---- | ----- | ---- | ------ |
| <dir> | <apps    | frontend | libs | tests | docs | other> |

## SIGNALS

| Signal               | Value | Evidence                   |
| -------------------- | ----- | -------------------------- |
| Duplication %        | <n>   | quality-jscpd.json         |
| Coupling score       | <n>   | architecture-coupling.json |
| Change concentration | <n>   | history-concentration.json |
| Lint enforced        | <0/1> | quality-gates.json         |
| Tests enforced       | <0/1> | quality-gates.json         |
| CI/local parity OK   | <0/1> | quality-gates.json         |
| Doc risk reasons     | <n>   | docs-risk.json             |
| MCP present          | <0/1> | mcp-scan.json              |

## QUALITY GATES & TESTS

- Hard tests present: <yes/no> (integration/e2e/smoke/system)
- Lint enforced in pre-commit + CI: <yes/no>
- Integration/smoke enforced in pre-commit + CI: <yes/no>
- CI/Local parity gaps: <summary>

## KPI SCORING

- Formula: `S = round(0.7*O + 0.3*A, 1)`
- Objective score (O): <n>
- Anchor (A): <10/8/5/2/0>
- Agentic Readiness score (S): <n>
- Legend: 🟢 7–10 Good, 🟠 4–6 Watch, 🔴 0–3 Risk

## READINESS BLOCKERS

1. <lint not enforced in pre-commit + CI>
2. <integration/smoke not enforced in pre-commit + CI>
3. <CI/local parity gaps>
4. <docs encode enforceable rules or missing review standards>
5. <MCP configuration present>

## MAINTENANCE SCORE

- Formula: `S = round(0.7*O + 0.3*A, 1)`
- Objective score (O): <n>
- Anchor (A): <10/8/5/2/0>
- Maintenance score (S): <n>

## RISKS & GAPS

1. <risk or missing evidence>
2. <risk>

## RECOMMENDATIONS

1. <highest impact readiness improvement>
2. <follow-on improvement>

## ATTACHMENTS

- recon → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/recon.json`
- repo map → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/repo-map.json`
- quality:jscpd → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/quality-jscpd.json`
- quality:lizard → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/quality-lizard.json`
- architecture:coupling → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/architecture-coupling.json`
- tests inventory → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/tests-inventory.json`
- quality gates → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/quality-gates.json`
- docs risk → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/docs-risk.json`
- mcp scan → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/mcp-scan.json`
- history concentration → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/history-concentration.json`
- docs freshness → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/docs-freshness.json`
- readiness score → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/agentic-readiness.json`
- maintenance score → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/maintenance-score.json`
```
