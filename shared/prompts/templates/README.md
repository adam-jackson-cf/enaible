# Prompt Templates & Renderer

This directory stores the reusable prompt-body templates and tooling for stamping the
command-specific versions used across Claude Code, Codex, and OpenCode.

## Files

- `*.md` – template files with inline HTML comments that describe platform rules and
  optional `<!-- rule: ... -->` directives. These directives are consumed automatically
  by the renderer.
- `render-prompts.sh` – helper script that merges one or more prompt bodies with one
  of the templates while applying/validating the rule directives.

## Usage

1. Edit or create the base prompt in `shared/prompts/<prompt-id>.md` following the
   template structure defined in `prompt-body.md`.
2. Run the renderer from the repo root (or any directory):

   ```bash
   ./shared/prompts/templates/render-prompts.sh \
     -p plan-linear,analyze-architecture \
     -t claude-code-command \
     -o out/claude
   ```

   Arguments:

   - `-p` accepts a comma-separated list or multiple flags for prompt IDs (without `.md`).
   - `-t` is the template ID (filename in this directory without `.md`).
   - `-o` is the output directory; it will be created if missing.

3. The script renders `<output>/<prompt-id>.<template-id>.md`, applies any rule
   directives (e.g., `.claude/` → `.opencode/`), and fails fast if a rule is violated
   or a placeholder remains unresolved.

## Template Rules

- Always keep platform-specific guidance inside HTML comments so the renderer can
  parse them without affecting the output.
- Use `<!-- rule: replace "find" => "replacement" -->` to enforce value swaps.
- Use `must-include` / `forbid` directives when the rendered prompt must contain or
  omit specific substrings.
- Document additional expectations in comment blocks so future prompts adhere to
  the same conventions.
