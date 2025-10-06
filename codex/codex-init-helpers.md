# Codex helpers

# Codex initialisation helpers

- Use in global terminal settings files to offer shorthand start up of codex for different security policies i.e if using zsh you would put this in .zshrc file.

```bash
cdx() {
    if [[ "$1" == "update" ]]; then
        npm install -g @openai/codex@latest
    else
        codex \
            --model 'gpt-5-codex' \
            --full-auto
            --ask-for-approval on-failure \
            --search \
            "$@"
    fi
}

cdx-no-sandbox-on-failure() {
    if [[ "$1" == "update" ]]; then
        npm install -g @openai/codex@latest
    else
        codex \
            --model 'gpt-5-codex' \
            --sandbox danger-full-access \
            --ask-for-approval on-failure \
            --search \
            "$@"
    fi
}

cdx-no-sandbox-on-request() {
    if [[ "$1" == "update" ]]; then
        npm install -g @openai/codex@latest
    else
        codex \
            --model 'gpt-5-codex' \
            --sandbox danger-full-access \
            --ask-for-approval on-request \
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
            --search \
            "$@"
    fi
}
```
