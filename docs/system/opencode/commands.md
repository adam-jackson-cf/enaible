# OpenCode Commands Documentation

**Source:** https://opencode.ai/docs/commands/
**Scraped:** 2025-09-21 12:40:25

---

## Intro

Get started with opencode.

**opencode** is an AI coding agent built for the terminal.
![opencode TUI with the opencode theme](https://opencode.ai/docs/_astro/screenshot.Bs5D4atL_ZvsvFu.webp)

---

#### Prerequisites

To use opencode, you’ll need:

1. A modern terminal emulator, such as:

- [WezTerm](https://wezterm.org), cross-platform
- [Alacritty](https://alacritty.org), cross-platform
- [Ghostty](https://ghostty.org), Linux and macOS
- [Kitty](https://sw.kovidgoyal.net/kitty/), Linux and macOS

2. API keys for the LLM providers you want to use.

---

## Install

The easiest way to install opencode is through the install script:

```bash
curl -fsSL https://opencode.ai/install | bash
```

You can also install it with the following:

- Using Node.js

  ```bash
  npm install -g opencode-ai
  ```

  ```bash
  bun install -g opencode-ai
  ```

  ```bash
  pnpm install -g opencode-ai
  ```

  ```bash
  yarn global add opencode-ai
  ```

- Using Homebrew on macOS and Linux

  ```bash
  brew install sst/tap/opencode
  ```

- Using Paru on Arch Linux
  ```bash
  paru -S opencode-bin
  ```

### Windows

- Using Chocolatey

  ```powershell
  choco install opencode
  ```

- Using WinGet

  ```powershell
  winget install opencode
  ```

- Using Scoop

  ```powershell
  scoop bucket add extras
  scoop install extras/opencode
  ```

- Using NPM
  ```powershell
  npm install -g opencode-ai
  ```

Support for installing opencode on Windows using Bun is currently in progress. You can also grab the binary from the [Releases](https://github.com/sst/opencode/releases).

---

## Configure

With opencode you can use any LLM provider by configuring their API keys. If you are new to using LLM providers, we recommend using [opencode zen](https://opencode.ai/docs/zen) — a curated list of models tested by the opencode team.

1. Run:

```bash
opencode auth login
```

Select "opencode" and open https://opencode.ai/auth. 2. Sign in, add billing details, and copy your API key. 3. Paste your API key when prompted.

Alternatively, you can select one of the other providers. [Learn more](https://opencode.ai/docs/providers#directory).

---

## Initialize

Navigate to the project you want to work on:

```bash
cd /path/to/project
```

Run opencode:

```bash
opencode
```

Initialize opencode for the project:

```bash
/init
```

This analyzes your project and creates an `AGENTS.md` file in the project root. Commit `AGENTS.md` to Git — it helps opencode understand your project structure and patterns.

---

## Usage

You are now ready to use opencode to work on your project. If you are new to AI coding agents, here are examples.

### Ask questions

Ask opencode to explain the codebase or fuzzy-search for files using `@`:

```text
How is authentication handled in @packages/functions/src/api/index.ts
```

### Add features

Ask opencode to create a plan (Plan mode disables change-making). Switch to Plan mode with the Tab key.

Example prompt (Plan mode):

```text
When a user deletes a note, we'd like to flag it as deleted in the database.

Then create a screen that shows all the recently deleted notes.

From this screen, the user can undelete a note or permanently delete it.
```

Iterate on the plan and provide images or references by dragging them into the terminal.

When ready, switch back to Build mode (Tab) and ask it to make the changes.

Example (Build mode):

```text
Sounds good! Go ahead and make the changes.
```

### Make changes

For straightforward changes, ask opencode to implement them directly:

```text
We need to add authentication to the /settings route. Take a look at how this is handled in the /notes route in @packages/functions/src/notes.ts and implement the same logic in @packages/functions/src/settings.ts
```

Provide sufficient context so opencode makes the correct changes.

### Undo changes

If a change isn't what you wanted, use `/undo` to revert it:

```text
/undo
```

You can run `/undo` multiple times. To redo, use `/redo`:

```text
/redo
```

---

## Share

Conversations can be shared with your team:

```text
/share
```

This creates a link to the conversation and copies it to your clipboard. Conversations are not shared by default. Example conversation: https://opencode.ai/s/4XP1fce5

---

## Customize

To make opencode your own, consider:

- picking a theme: https://opencode.ai/docs/themes
- customizing keybinds: https://opencode.ai/docs/keybinds
- configuring formatters: https://opencode.ai/docs/formatters
- creating custom commands: https://opencode.ai/docs/commands
- editing the opencode config: https://opencode.ai/docs/config

---

© [Anomaly Innovations Inc.](https://anoma.ly)
Last updated — Sep 21, 2025
