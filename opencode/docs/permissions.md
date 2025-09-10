# OpenCode.ai Permissions Documentation

**Source:** https://opencode.ai/docs/permissions/
**Scraped:** 2025-09-10

---

## Overview

OpenCode provides a granular permissions system to control AI agent actions in a codebase. By default, all operations are allowed without explicit approval, but you can configure fine-grained controls to manage what actions the AI can perform.

## Configuration

Permissions are configured in the `opencode.json` file under the `permission` key. This allows you to control various tools and operations that the AI agent can perform.

## Supported Permission Tools

The permissions system supports controlling the following tools:

1. **`edit`** - Control file editing operations
2. **`bash`** - Control bash command execution
3. **`webfetch`** - Control web content fetching

## Edit Permissions

Control file editing operations with the following options:

- **`"ask"`** - Prompt for approval before editing files
- **`"allow"`** - Allow all file editing without approval
- **`"deny"`** - Disable all file editing tools

### Example Configuration

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "edit": "ask"
  }
}
```

## Bash Command Permissions

Bash command permissions provide multiple configuration strategies for fine-grained control:

### 1. Global Approval Requirement

Require approval for all bash commands:

```json
{
  "permission": {
    "bash": "ask"
  }
}
```

### 2. Disable Specific Command Types

Block specific commands or patterns:

```json
{
  "permission": {
    "bash": {
      "terraform *": "deny"
    }
  }
}
```

### 3. Approve Specific Commands

Allow specific commands without approval:

```json
{
  "permission": {
    "bash": {
      "git status": "allow",
      "npm run build": "allow",
      "ls": "allow"
    }
  }
}
```

### 4. Wildcard Pattern Configuration

Mix approval requirements with wildcard patterns:

```json
{
  "permission": {
    "bash": {
      "git push": "ask",
      "*": "allow"
    }
  }
}
```

## WebFetch Permissions

Control web content fetching operations:

- **`"ask"`** - Prompt for approval before fetching web content
- **`"allow"`** - Allow all web fetching without approval
- **`"deny"`** - Disable all web fetching tools

```json
{
  "permission": {
    "webfetch": "ask"
  }
}
```

## Advanced Configuration Examples

### Restrictive Development Environment

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "edit": "ask",
    "bash": {
      "git status": "allow",
      "git diff": "allow",
      "git log": "allow",
      "ls": "allow",
      "cat": "allow",
      "git push": "ask",
      "rm *": "deny",
      "sudo *": "deny",
      "*": "ask"
    },
    "webfetch": "ask"
  }
}
```

### Production Safety Configuration

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "edit": "deny",
    "bash": {
      "git status": "allow",
      "git diff": "allow",
      "git log": "allow",
      "ls": "allow",
      "cat": "allow",
      "*deploy*": "deny",
      "*prod*": "deny",
      "rm *": "deny",
      "sudo *": "deny",
      "*": "ask"
    },
    "webfetch": "allow"
  }
}
```

## Key Features

- **Granular Control**: Configure permissions at both global and command-specific levels
- **Pattern Matching**: Use wildcards to match command patterns
- **Flexible Policies**: Mix different permission levels (ask, allow, deny) for different operations
- **Security First**: Default configurations can be set to require approval for sensitive operations
- **Easy Configuration**: Simple JSON-based configuration in your project's `opencode.json` file

## Best Practices

1. **Start Restrictive**: Begin with `"ask"` permissions and gradually allow specific commands as needed
2. **Block Dangerous Commands**: Always deny or require approval for potentially destructive operations like `rm`, `sudo`, deployment commands
3. **Allow Safe Operations**: Common read-only operations like `git status`, `ls`, `cat` can usually be safely allowed
4. **Use Patterns**: Leverage wildcard patterns to efficiently manage similar commands
5. **Environment-Specific**: Configure different permission levels for development vs. production environments

## Installation

Permissions are automatically available once OpenCode is installed. Simply add the `permission` configuration to your `opencode.json` file to start using them.
