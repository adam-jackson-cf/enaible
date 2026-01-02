# Analysis Gaps - Implementation Plan

## Goal

Close language parity gaps across analysis prompts for the supported languages in README.md (Python, TypeScript, Go, Rust, C#). This plan is written so a new session can take it from 0 to 1.

## Scope

Covers analysis prompts in `shared/prompts/`:

- `analyze-architecture.md`
- `analyze-code-quality.md`
- `analyze-performance.md`
- `analyze-root-cause.md`
- `analyze-security.md`

Primary gaps found:

- Architecture: weak pattern coverage for Go/Rust/C#, missing C# dependency parsing.
- Performance: no Go/Rust/C# analyzers; Python/TS are much stronger.
- Root cause: language-specific error patterns only for .py/.js/.java; trace patterns are Python/JS oriented.
- Security: largely covered by Semgrep, but no multi-language supply-chain scanning (general gap, not language-specific).

## Required Baseline (Do First)

The project rules require a baseline before new work.

1. Confirm project root and requirements:
   - `pwd` should be repo root.
   - `python --version` should be 3.12.x.
   - `uv --version` should be >= 0.4.
2. Establish baseline quality gates (must pass before changes):
   ```bash
   bash scripts/run-ci-quality-gates.sh --fix --stage
   ```
3. If the repo has a dev server, run and confirm it starts cleanly. If not applicable, note it in the work log.
4. Create the baseline commit once the gates pass (per repo rules).

## Phase 1 - Architecture Parity

### 1.1 Add C# dependency parsing

Add support for NuGet manifests in `shared/analyzers/architecture/dependency_analysis.py`.

- Parse:
  - `*.csproj` (XML: `<PackageReference Include="X" Version="Y" />`)
  - `packages.config` (XML: `<package id="X" version="Y" />`)
  - `Directory.Packages.props` (XML: `<PackageVersion Include="X" Version="Y" />`)
  - `nuget.config` (optional, for sources only; do not treat as deps)
- Extend `dependency_files` map and add parsers for new formats.
- Ensure `code_extensions` include `.csproj`, `.props`, `.config` if needed.
- Record usage analysis for C# using `using` statements (already in coupling analyzer); use that mapping for unused-dependency detection if applicable.

### 1.2 Expand architecture pattern coverage for Go/Rust/C#

Update `shared/analyzers/architecture/pattern_evaluation.py`.

- Extend `_init_language_patterns` to include:
  - Go: `func`, `type`, `import` patterns
  - Rust: `fn`, `struct`, `use` patterns
  - C#: `class`, `interface`, `using`, `async` patterns
- Add language-specific indicators for common patterns:
  - Singleton: static instance (C#), `lazy_static` (Rust), `var instance` + `sync.Once` (Go)
  - Factory: `func NewX`, `type XFactory` (Go), `impl X { fn new }` (Rust), `class XFactory` (C#)
  - Repository/Service: naming conventions in those languages
- Keep regex limits and timeouts unchanged to avoid hangs.

### 1.3 Expand scalability pattern indicators for Go/Rust/C#

Update `shared/config/patterns/scalability/*.json` to include language-specific markers.

- `performance.json`:
  - Go: `time.Sleep`, `http.Get`, `os.Open`, `bufio.NewScanner` (sync I/O)
  - Rust: `std::thread::sleep`, `std::fs::read_to_string`
  - C#: `Thread.Sleep`, `.Result`, `.Wait()`, `File.ReadAllText`
- `concurrency.json`:
  - Go: `sync.Mutex`, `sync.RWMutex`, `WaitGroup`
  - Rust: `Mutex`, `RwLock`, `Arc<Mutex` patterns
  - C#: `lock (`, `Monitor.Enter`, `SemaphoreSlim`
- `database.json`:
  - C#: `DbSet<T>.ToList()` without pagination, `ExecuteReader` loops
  - Go/Rust ORM patterns if present (keep minimal and safe)

## Phase 2 - Performance Parity

### 2.1 Go performance analyzer

Add `shared/analyzers/performance/golangci_lint_analyzer.py`.

- Use `golangci-lint run --out-format json` and parse findings.
- Enable perf-relevant linters (at least `gocritic`, `gosimple`, `staticcheck`), but do not add fallback behaviors.
- Register as `performance:golangci-lint`.
- Update `shared/prompts/analyze-performance.md` to run this analyzer when Go is detected (presence of `go.mod` or `*.go`).

### 2.2 Rust performance analyzer

Add `shared/analyzers/performance/clippy_analyzer.py`.

- Use `cargo clippy --message-format=json` and parse for `clippy::perf` and related lints.
- Register as `performance:clippy`.
- Update `shared/prompts/analyze-performance.md` to run this analyzer when Rust is detected (`Cargo.toml`).

### 2.3 C# performance analyzer

Add `shared/analyzers/performance/dotnet_analyzers.py`.

- Prefer `dotnet format analyzers --severity` or `dotnet build` with analyzers enabled.
- Parse analyzer output for performance-related rules (e.g., CA1822, CA1823, CA1845).
- Register as `performance:dotnet`.
- Update `shared/prompts/analyze-performance.md` to run when C# is detected (`*.csproj`, `*.sln`).

## Phase 3 - Root Cause Parity

### 3.1 Expand error patterns for Go/Rust/C#

Update `shared/config/patterns/error/language_patterns.json`.

- Add `.go`, `.rs`, `.cs` keys with minimal but meaningful patterns:
  - Go: `panic(`, unchecked `err` (`if err != nil` missing), `goroutine` leaks
  - Rust: `unwrap()`, `expect()`, `panic!(`
  - C#: `NullReferenceException` patterns, `async void`, `.Result` deadlocks

### 3.2 Expand trace patterns for Go/Rust/C#

Update `shared/analyzers/root_cause/trace_execution.py`.

- Extend `self.patterns` with:
  - Go: `func main(`, `http.HandleFunc`, `gin.Default` routes
  - Rust: `fn main(`, `actix_web::`, `tokio::main`
  - C#: `static void Main`, `[HttpGet]`, `[HttpPost]`

### 3.3 Recent changes analyzer coverage

Update `shared/analyzers/root_cause/recent_changes.py`.

- Add C# dependency files to `dependency_changes` patterns (`.csproj`, `packages.config`, `Directory.Packages.props`).

## Phase 4 - Security Coverage (Cross-Language)

### 4.1 Add SCA analyzer

Add a supply-chain analyzer for all languages to close the general gap.

- Candidate: `osv-scanner` (multi-language, OSV database).
- Add `shared/analyzers/security/osv_scanner.py` and register `security:osv`.
- Update `shared/prompts/analyze-security.md` to run `security:osv` and list SCA results in the report.

## Phase 5 - Prompt Updates

Update `shared/prompts/*` to include new analyzers and detection rules.

- `analyze-architecture.md`: call out new C# dependency support and expanded patterns.
- `analyze-performance.md`: add Go/Rust/C# analyzer invocations with recon gating.
- `analyze-root-cause.md`: mention expanded language patterns and artifacts.
- `analyze-security.md`: include SCA analyzer output in findings and attachments.

## Phase 6 - Tests and Validation

1. Add unit tests for new parsers and regex patterns where possible:
   - Dependency parsing (C# manifests)
   - Analyzer JSON parsing (golangci-lint, clippy, dotnet)
   - Fixtures:
     - Reuse existing `shared/tests/fixture/test_codebase/vulnerable-apps/test-csharp/VulnerableWebApp.csproj`
     - Add minimal `packages.config` and `Directory.Packages.props` fixtures under `shared/tests/fixture/test_codebase/vulnerable-apps/test-csharp/`
2. Run full gates (required):
   ```bash
   bash scripts/run-ci-quality-gates.sh --fix --stage
   ```
3. Create atomic commits after each logical phase (per repo rules).

## Acceptance Criteria

- Architecture analyzer reports include C# dependencies and show pattern findings in Go/Rust/C#.
- Performance analyzer runs a language-specific tool for Go/Rust/C# and reports findings.
- Root cause analysis recognizes Go/Rust/C# patterns and error signatures.
- Security analysis includes SCA results.
- All quality gates pass.

## File Touch Map

- `shared/analyzers/architecture/dependency_analysis.py`
- `shared/analyzers/architecture/pattern_evaluation.py`
- `shared/config/patterns/scalability/*.json`
- `shared/analyzers/performance/` (new files)
- `shared/config/patterns/error/language_patterns.json`
- `shared/analyzers/root_cause/trace_execution.py`
- `shared/analyzers/root_cause/recent_changes.py`
- `shared/analyzers/security/` (new file)
- `shared/prompts/analyze-architecture.md`
- `shared/prompts/analyze-performance.md`
- `shared/prompts/analyze-root-cause.md`
- `shared/prompts/analyze-security.md`

## Notes / Constraints

- Do not add fallback modes or bypass quality gates.
- Prefer established tools (golangci-lint, clippy, dotnet analyzers, osv-scanner).
- Keep cyclomatic complexity under 10 in new code paths.
- Do not introduce new prompt tokens without declaring them in Variables sections.

## Proposed Additions (Post-Phase or Parallel)

- **NuGet lockfile support**: parse `packages.lock.json` to surface resolved versions and lock drift.
- **ProjectReference awareness**: parse `<ProjectReference Include="...">` in `.csproj` to map internal module dependencies for architecture analysis.
- **Directory.Build.props**: include for shared `PackageReference` entries if present.
- **C# usage mapping**: expand dependency usage scans to recognize `using Namespace;` for unused dependency detection.
- **Language-specific tests**: add fixtures for `*.csproj`, `packages.config`, and `Directory.Packages.props` parsing.
