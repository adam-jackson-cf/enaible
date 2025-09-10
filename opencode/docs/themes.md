# Themes in OpenCode

## Terminal Requirements

For themes to display correctly, your terminal must support **truecolor** (24-bit color):

- Check support: Run `echo $COLORTERM`
- Enable truecolor: Set `COLORTERM=truecolor`
- Compatible with modern terminals like iTerm2, Alacritty, Kitty

## Built-in Themes

OpenCode includes several built-in themes:

- `system` (adapts to terminal background)
- `tokyonight`
- `everforest`
- `ayu`
- `catppuccin`
- `gruvbox`
- `kanagawa`
- `nord`
- `matrix`
- `one-dark`

## System Theme

The `system` theme:

- Generates gray scale based on terminal background
- Uses ANSI colors
- Preserves terminal defaults

## Using a Theme

Select a theme via:

- `/theme` command
- Configuration file

Example configuration:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "theme": "tokyonight"
}
```

## Custom Themes

### Theme Hierarchy

Themes are loaded from:

1. Built-in themes
2. User config directory
3. Project root directory
4. Current working directory

### Creating a Theme

Create JSON files in theme directories:

```bash
mkdir -p ~/.config/opencode/themes
vim ~/.config/opencode/themes/my-theme.json
```

### JSON Format

Supports:

- Hex colors
- ANSI colors
- Color references
- Dark/light variants
- "none" for terminal defaults

### Example Theme

A complete theme example is provided in the documentation, demonstrating a Nord-inspired color scheme with extensive customization for syntax highlighting, markdown, and UI elements.

The theme uses a JSON structure with:

- Color definitions
- Theme color mappings
- Support for dark and light variants

## Key Features

- Flexible theme system
- Customizable color palette
- Support for system and custom themes
- Truecolor compatibility

## Source

Original documentation retrieved from https://opencode.ai/docs/themes/ on 2025-09-10
