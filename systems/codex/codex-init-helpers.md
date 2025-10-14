# Codex helpers

# Codex initialisation helpers

- Use in global terminal settings files to offer shorthand start up of codex for different security policies i.e if using zsh you would put this in .zshrc file.

```bash
# Codex helper
cdx-no-sandbox() {
    if [[ "$1" == "update" ]]; then
        npm install -g @openai/codex@latest
    else
        codex \
            --model 'gpt-5-codex' \
            --sandbox danger-full-access \
            --ask-for-approval on-failure \
            -c model_reasoning_summary_format=experimental \
            --search \
            "$@"
    fi
}

cdx-no-sandbox-request() {
    if [[ "$1" == "update" ]]; then
        npm install -g @openai/codex@latest
    else
        codex \
            --model 'gpt-5-codex' \
            --sandbox danger-full-access \
            --ask-for-approval on-request \
            -c model_reasoning_summary_format=experimental \
            --search \
            "$@"
    fi
}

cdx-exec() {
    if [[ "$1" == "update" ]]; then
        npm install -g @openai/codex@latest
    else
        codex exec \
            --model 'gpt-5-codex' \
            --sandbox workspace-write \
            --config 'sandbox_workspace_write.network_access=true' \
            "$@"
    fi
}
```
