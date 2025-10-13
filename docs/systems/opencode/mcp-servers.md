# OpenCode AI MCP Servers Documentation

**Source:** https://opencode.ai/docs/mcp-servers/
**Scraped:** 2025-09-10 21:53:54

---

[Skip to content](https://opencode.ai/docs/mcp-servers/#_top)
[ ![](https://opencode.ai/docs/_astro/logo-dark.NCybiIc5.svg) ![](https://opencode.ai/docs/_astro/logo-light.YQ6q6zRd.svg) opencode ](https://opencode.ai/)
[Home](https://opencode.ai/)[Docs](https://opencode.ai/docs/)
[ ](https://github.com/sst/opencode)[ ](https://opencode.ai/discord)
Search ` `⌘``K` `
Cancel
Clear

- [ Intro ](https://opencode.ai/docs/)
- [ Config ](https://opencode.ai/docs/config/)
- [ Providers ](https://opencode.ai/docs/providers/)
- [ Enterprise ](https://opencode.ai/docs/enterprise/)
- [ Troubleshooting ](https://opencode.ai/docs/troubleshooting/)
- Usage
  - [ TUI ](https://opencode.ai/docs/tui/)
  - [ CLI ](https://opencode.ai/docs/cli/)
  - [ IDE ](https://opencode.ai/docs/ide/)
  - [ Zen ](https://opencode.ai/docs/zen/)
  - [ Share ](https://opencode.ai/docs/share/)
  - [ GitHub ](https://opencode.ai/docs/github/)
  - [ GitLab ](https://opencode.ai/docs/gitlab/)
- Configure
  - [ Rules ](https://opencode.ai/docs/rules/)
  - [ Agents ](https://opencode.ai/docs/agents/)
  - [ Models ](https://opencode.ai/docs/models/)
  - [ Themes ](https://opencode.ai/docs/themes/)
  - [ Keybinds ](https://opencode.ai/docs/keybinds/)
  - [ Commands ](https://opencode.ai/docs/commands/)
  - [ Formatters ](https://opencode.ai/docs/formatters/)
  - [ Permissions ](https://opencode.ai/docs/permissions/)
  - [ LSP Servers ](https://opencode.ai/docs/lsp/)
  - [ MCP servers ](https://opencode.ai/docs/mcp-servers/)
- Develop
  - [ SDK ](https://opencode.ai/docs/sdk/)
  - [ Server ](https://opencode.ai/docs/server/)
  - [ Plugins ](https://opencode.ai/docs/plugins/)

[GitHub](https://github.com/sst/opencode)[Dscord](https://opencode.ai/discord)
Select theme Dark Light Auto
On this page
Overview

- [ Overview ](https://opencode.ai/docs/mcp-servers/#_top)
- [ Install ](https://opencode.ai/docs/mcp-servers/#install)
- [ Configure ](https://opencode.ai/docs/mcp-servers/#configure)
- [ Initialize ](https://opencode.ai/docs/mcp-servers/#initialize)
- [ Usage ](https://opencode.ai/docs/mcp-servers/#usage)
  - [ Ask questions ](https://opencode.ai/docs/mcp-servers/#ask-questions)
  - [ Add features ](https://opencode.ai/docs/mcp-servers/#add-features)
  - [ Make changes ](https://opencode.ai/docs/mcp-servers/#make-changes)
  - [ Undo changes ](https://opencode.ai/docs/mcp-servers/#undo-changes)
- [ Share ](https://opencode.ai/docs/mcp-servers/#share)
- [ Customize ](https://opencode.ai/docs/mcp-servers/#customize)

## On this page

- [ Overview ](https://opencode.ai/docs/mcp-servers/#_top)
- [ Install ](https://opencode.ai/docs/mcp-servers/#install)
- [ Configure ](https://opencode.ai/docs/mcp-servers/#configure)
- [ Initialize ](https://opencode.ai/docs/mcp-servers/#initialize)
- [ Usage ](https://opencode.ai/docs/mcp-servers/#usage)
  - [ Ask questions ](https://opencode.ai/docs/mcp-servers/#ask-questions)
  - [ Add features ](https://opencode.ai/docs/mcp-servers/#add-features)
  - [ Make changes ](https://opencode.ai/docs/mcp-servers/#make-changes)
  - [ Undo changes ](https://opencode.ai/docs/mcp-servers/#undo-changes)
- [ Share ](https://opencode.ai/docs/mcp-servers/#share)
- [ Customize ](https://opencode.ai/docs/mcp-servers/#customize)

# Intro

Get started with opencode.
[**opencode**](https://opencode.ai/) is an AI coding agent built for the terminal.
![opencode TUI with the opencode theme](https://opencode.ai/docs/_astro/screenshot.Bs5D4atL_ZvsvFu.webp)
Let’s get started.

---

#### [Prerequisites](https://opencode.ai/docs/mcp-servers/#prerequisites)

To use opencode, you’ll need:

1. A modern terminal emulator like:
   - [WezTerm](https://wezterm.org), cross-platform
   - [Alacritty](https://alacritty.org), cross-platform
   - [Ghostty](https://ghostty.org), Linux and macOS
   - [Kitty](https://sw.kovidgoyal.net/kitty/), Linux and macOS
2. API keys for the LLM providers you want to use.

---

## [Install](https://opencode.ai/docs/mcp-servers/#install)

The easiest way to install opencode is through the install script.
Terminal window```

curl-fsSLhttps://opencode.ai/install|bash

````

You can also install it with the following:
  * **Using Node.js**
    * [ npm ](https://opencode.ai/docs/mcp-servers/#tab-panel-0)
    * [ Bun ](https://opencode.ai/docs/mcp-servers/#tab-panel-1)
    * [ pnpm ](https://opencode.ai/docs/mcp-servers/#tab-panel-2)
    * [ Yarn ](https://opencode.ai/docs/mcp-servers/#tab-panel-3)
Terminal window```


npminstall-gopencode-ai


````

Terminal window```

buninstall-gopencode-ai

````

Terminal window```


pnpminstall-gopencode-ai


````

Terminal window```

yarnglobaladdopencode-ai

````

  * **Using Homebrew on macOS and Linux**
Terminal window```


brewinstallsst/tap/opencode


````

- **Using Paru on Arch Linux**
  Terminal window```

paru-Sopencode-bin

````



#### [Windows](https://opencode.ai/docs/mcp-servers/#windows)
Right now the automatic installation methods do not work properly on Windows. However you can grab the binary from the [Releases](https://github.com/sst/opencode/releases).
* * *
## [Configure](https://opencode.ai/docs/mcp-servers/#configure)
With opencode you can use any LLM provider by configuring their API keys.
We recommend signing up for [Claude Pro](https://www.anthropic.com/news/claude-pro) or [Max](https://www.anthropic.com/max), it’s the most cost-effective way to use opencode.
Once you’ve signed up, run `opencode auth login` and select Anthropic.
Terminal window```


$opencodeauthlogin




┌Addcredential



│



◆Selectprovider




│●Anthropic (recommended)




│○OpenAI




│○Google




│○AmazonBedrock




│○Azure




│○DeepSeek




│○Groq




│...



└

````

Alternatively, you can select one of the other providers. [Learn more](https://opencode.ai/docs/providers#directory).

---

## [Initialize](https://opencode.ai/docs/mcp-servers/#initialize)

Now that you’ve configured a provider, you can navigate to a project that you want to work on.
Terminal window```

cd/path/to/project

````

And run opencode.
Terminal window```

opencode

````

Next, initialize opencode for the project by running the following command.

```

/init

```

This will get opencode to analyze your project and create an `AGENTS.md` file in the project root.
You should commit your project’s `AGENTS.md` file to Git.
This helps opencode understand the project structure and the coding patterns used.

---

## [Usage](https://opencode.ai/docs/mcp-servers/#usage)

You are now ready to use opencode to work on your project. Feel free to ask it anything!
If you are new to using an AI coding agent, here are some examples that might help.

---

### [Ask questions](https://opencode.ai/docs/mcp-servers/#ask-questions)

You can ask opencode to explain the codebase to you.
Use the `@` key to fuzzy search for files in the project.

```


How is authentication handled in @packages/functions/src/api/index.ts


```

This is helpful if there’s a part of the codebase that you didn’t work on.

---

### [Add features](https://opencode.ai/docs/mcp-servers/#add-features)

You can ask opencode to add new features to your project. Though we first recommend asking it to create a plan.

1. **Create a plan**
   opencode has a _Plan mode_ that disables its ability to make changes and instead suggest _how_ it’ll implement the feature.
   Switch to it using the **Tab** key. You’ll see an indicator for this in the lower right corner.

```

<TAB>

```

Now let’s describe what we want it to do.

```

When a user deletes a note, we'd like to flag it as deleted in the database.


Then create a screen that shows all the recently deleted notes.


From this screen, the user can undelete a note or permanently delete it.

```

You want to give opencode enough details to understand what you want. It helps to talk to it like you are talking to a junior developer on your team.
Give opencode plenty of context and examples to help it understand what you want. 2. **Iterate on the plan**
Once it gives you a plan, you can give it feedback or add more details.

```

We'd like to design this new screen using a design I've used before.


[Image #1] Take a look at this image and use it as a reference.

```

Drag and drop images into the terminal to add them to the prompt.
opencode can scan any images you give it and add them to the prompt. You can do this by dragging and dropping an image into the terminal. 3. **Build the feature**
Once you feel comfortable with the plan, switch back to _Build mode_ by hitting the **Tab** key again.

```

<TAB>

```

And asking it to make the changes.

```


Soundsgood!Goaheadandmakethechanges.


```

---

### [Make changes](https://opencode.ai/docs/mcp-servers/#make-changes)

For more straightforward changes, you can ask opencode to directly build it without having to review the plan first.

```

We need to add authentication to the /settings route. Take a look at how this is



handled in the /notes route in @packages/functions/src/notes.ts and implement




the same logic in @packages/functions/src/settings.ts


```

You want to make sure you provide a good amount of detail so opencode makes the right changes.

---

### [Undo changes](https://opencode.ai/docs/mcp-servers/#undo-changes)

Let’s say you ask opencode to make some changes.

```


Can you refactor the function in @packages/functions/src/api/index.ts?


```

But you realize that it is not what you wanted. You **can undo** the changes using the `/undo` command.

```

/undo

```

opencode will now revert the changes you made and show your original message again.

```


Can you refactor the function in @packages/functions/src/api/index.ts?


```

From here you can tweak the prompt and ask opencode to try again.
You can run `/undo` multiple times to undo multiple changes.
Or you **can redo** the changes using the `/redo` command.

```

/redo

```

---

## [Share](https://opencode.ai/docs/mcp-servers/#share)

The conversations that you have with opencode can be [shared with your team](https://opencode.ai/docs/share).

```

/share

```

This will create a link to the current conversation and copy it to your clipboard.
Conversations are not shared by default.
Here’s an [example conversation](https://opencode.ai/s/4XP1fce5) with opencode.

---

## [Customize](https://opencode.ai/docs/mcp-servers/#customize)

And that’s it! You are now a pro at using opencode.
To make it your own, we recommend [picking a theme](https://opencode.ai/docs/themes), [customizing the keybinds](https://opencode.ai/docs/keybinds), [configuring code formatters](https://opencode.ai/docs/formatters), [creating custom commands](https://opencode.ai/docs/commands), or playing around with the [opencode config](https://opencode.ai/docs/config).
[](https://github.com/sst/opencode/edit/dev/packages/web/src/content/docs/index.mdx)[](https://github.com/sst/opencode/issues/new)[](https://opencode.ai/discord)
© [Anomaly Innovations Inc.](https://anoma.ly)
Last updated — Sep 9, 2025
