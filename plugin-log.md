# Plugin Debug Log

## Context Capture Plugin Debug Output

The following debug output was observed during the git commit process, showing truncated output from the context-capture plugin:

```
type Co
```

This appears to be truncated debug output from the context-capture plugin, likely from an error logging statement that was cut off mid-message. The full message was probably something like:

```
Context capture hook failed for event Co...
```

## Context

This debug output was observed during the commit process for the formatter alignment work, specifically when running the pre-commit hooks. The output suggests there may have been an issue with the context-capture plugin during the git commit operation.

## Files Involved

- `opencode/plugins/context-capture.ts` - The main plugin file
- `.opencode/hooks/context_bundle_capture_opencode.py` - Python capture script
- `.opencode/hooks/context_capture_config.json` - Plugin configuration

## Timestamp

This debug output was observed on: 2025-09-24 during the formatter alignment commit process.

## Notes

The truncated nature of the output makes it difficult to determine the exact cause of the debug message. The plugin may need additional error handling or logging improvements to provide more complete error information when issues occur.
