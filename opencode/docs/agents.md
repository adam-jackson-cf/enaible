# OpenCode Agents Documentation

_Scraped from https://opencode.ai/docs/agents/ on 2025-09-21_

## Overview

Configure and use specialized agents.

Agents are specialized AI assistants that can be configured for specific tasks and workflows. They allow you to create focused tools with custom prompts, models, and tool access.

> **Tip**: Use the plan agent to analyze code and review suggestions without making any code changes.

You can switch between agents during a session or invoke them with the `@` mention.

## Types

There are two types of agents in opencode; primary agents and subagents.

### Primary Agents

Primary agents are the main assistants you interact with directly. You can cycle through them using the **Tab** key, or your configured `switch_agent` keybind. These agents handle your main conversation and can access all configured tools.

> **Tip**: You can use the **Tab** key to switch between primary agents during a session.

opencode comes with two built-in primary agents, **Build** and **Plan**.

### Subagents

Subagents are specialized assistants that primary agents can invoke for specific tasks. You can also manually invoke them by **@ mentioning** them in your messages.

opencode comes with one built-in subagent, **General**.

## Built-in Agents

opencode comes with two built-in primary agents and one built-in subagent.

### Build

**Mode**: `primary`

Build is the **default** primary agent with all tools enabled. This is the standard agent for development work where you need full access to file operations and system commands.

### Plan

**Mode**: `primary`

A restricted agent designed for planning and analysis. We use a permission system to give you more control and prevent unintended changes. By default, all of the following are set to `ask`:

- `file edits`: All writes, patches, and edits
- `bash`: All bash commands

This agent is useful when you want the LLM to analyze code, suggest changes, or create plans without making any actual modifications to your codebase.

### General

**Mode**: `subagent`

A general-purpose agent for researching complex questions, searching for code, and executing multi-step tasks. Use when searching for keywords or files and you're not confident you'll find the right match in the first results.

---

_Note: This documentation was scraped from the OpenCode website. Some content may have been truncated during the scraping process. For the most up-to-date and complete documentation, please visit https://opencode.ai/docs/agents/_
