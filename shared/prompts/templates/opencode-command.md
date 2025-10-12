<!-- template format for opencode markdown command -->
<!-- Docs: https://opencode.ai/docs/commands/ -->
<!-- rule: replace ".claude/" => ".opencode/" -->
<!-- rule: replace "~/.claude/" => "~/.config/opencode/" -->

<!--
Opencode specific items
  Rules:
    User level ~/.config/opencode/AGENTS.md
    Project level ./AGENTS.md
  Directories:
    User level ~/.config/opencode
    Project level ./.opencode
  Settings:
    User level  ~/.config/opencode/opencode.json
    Project level ./.opencode/opencode.json
  Mcp config:
    User level  ~/.config/opencode/opencode.json

FRONTMATTER (define these in real YAML frontmatter when instantiating):
  description: One-line summary shown in slash picker
  agent: build | plan | <custom-agent-name> (defined in opencode.json or .opencode/agent/)
  model: anthropic/claude-3-5-sonnet-20241022 (optional override)
  subtask: true | false (run as a subtask)

ARGUMENTS (expansion rules):
  $1..$9: expand to first nine positional args
  $ARGUMENTS: expands to all args joined by a single space
  $$: preserved literally (emit a dollar sign)
  quoted: wrap an argument in double quotes to include spaces

TOOLS (controlled by agent/permissions):
  list: bash | edit | write | read | grep | glob | list | patch | todowrite | todoread | webfetch
  permission values: allow | ask | deny
  bash map example: {"*":"allow","git push":"ask","terraform *":"deny"}

FILE REFERENCES:
  @path includes file or directory contents in context (e.g., @shared/tests, @pytest.ini)
-->

---

description: <!-- one-line summary shown in slash picker -->
agent: <!-- build | plan | <custom-agent-name> -->
model: <!-- optional model override (e.g., anthropic/claude-3-5-sonnet-20241022) -->
subtask: <!-- true | false -->

---

<prompt-body>
