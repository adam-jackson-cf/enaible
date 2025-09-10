# Hook Script Performance Improvements

## Optimize Python Hook Script Performance with Compilation

### Analysis of Python Compilation Options

Python has several compilation/optimization approaches, each with different trade-offs:

### 1. **Python Bytecode Compilation (.pyc files)**

- **How it works**: Python automatically compiles .py files to .pyc bytecode files stored in `__pycache__/`
- **Performance gain**: ~10-20% faster startup (skips parsing/compilation step)
- **Implementation**: Use `py_compile` or `compileall` modules
- **Best for**: Frequently executed scripts with significant import overhead

### 2. **Cython Compilation**

- **How it works**: Compiles Python to C extensions (.so/.pyd files)
- **Performance gain**: 2-100x faster for compute-heavy code
- **Implementation**: Requires Cython installation and setup.py
- **Best for**: CPU-intensive operations, not ideal for I/O-bound scripts

### 3. **Nuitka Compilation**

- **How it works**: Compiles Python to standalone C++ executables
- **Performance gain**: 20-300% faster execution
- **Implementation**: Requires Nuitka installation
- **Best for**: Distributable binaries, complex applications

### 4. **PyPy JIT Interpreter**

- **How it works**: Alternative Python interpreter with JIT compilation
- **Performance gain**: 2-10x faster for long-running processes
- **Implementation**: Replace python3 with pypy3
- **Best for**: Long-running applications, not startup-time optimization

### Recommended Approach for Hook Script

Given that the context_bundle_capture.py hook:

- Is I/O-bound (file operations, JSON parsing)
- Runs frequently but briefly
- Has minimal computational complexity
- Needs fast startup time

**Best option: Python bytecode compilation with optimizations**

### Implementation Plan

1. **Create optimized bytecode version**:

   - Compile with optimization level 2 (-OO flag)
   - Removes docstrings and assertions for smaller size
   - Store in dedicated compiled directory

2. **Create wrapper script**:

   - Check if compiled version exists and is up-to-date
   - Use compiled version if available
   - Fallback to source if needed

3. **Hook configuration update**:
   - Update Claude Code hooks to use the wrapper
   - Maintain backward compatibility

### Expected Benefits

- **10-20% faster startup** from skipping parse/compile phase
- **Smaller memory footprint** from optimization
- **No additional dependencies** (uses standard Python)
- **Automatic fallback** if compilation fails

### Alternative: Minimal Standalone Binary (Optional Enhancement)

For maximum performance, could also create a minimal C extension using Cython for just the hot paths:

- JSON parsing
- File I/O operations
- Pattern matching

This would provide 2-5x speedup for these operations but requires more maintenance.

### Files to Create/Modify

1. `.claude/hooks/compile_hooks.py` - Compilation script
2. `.claude/hooks/hook_wrapper.sh` - Smart wrapper script
3. `.claude/hooks/__pycache_opt__/` - Optimized bytecode storage
4. Update hook configuration to use wrapper

### Implementation Example

#### compile_hooks.py

```python
#!/usr/bin/env python3
import py_compile
import os
from pathlib import Path

hooks_dir = Path(__file__).parent
cache_dir = hooks_dir / "__pycache_opt__"
cache_dir.mkdir(exist_ok=True)

# Compile with optimization level 2 (removes docstrings and assertions)
py_compile.compile(
    hooks_dir / "context_bundle_capture.py",
    cfile=cache_dir / "context_bundle_capture.cpython-311.opt-2.pyc",
    optimize=2
)
```

#### hook_wrapper.sh

```bash
#!/bin/bash
HOOK_DIR="$(dirname "$0")"
PYC_FILE="$HOOK_DIR/__pycache_opt__/context_bundle_capture.cpython-311.opt-2.pyc"
PY_FILE="$HOOK_DIR/context_bundle_capture.py"

# Use compiled version if it exists and is newer than source
if [ -f "$PYC_FILE" ] && [ "$PYC_FILE" -nt "$PY_FILE" ]; then
    exec python3 -OO "$PYC_FILE" "$@"
else
    exec python3 "$PY_FILE" "$@"
fi
```

### Performance Comparison

| Approach      | Startup Time | Execution Time | Dependencies | Maintenance |
| ------------- | ------------ | -------------- | ------------ | ----------- |
| Source .py    | Baseline     | Baseline       | None         | Low         |
| Bytecode .pyc | -20%         | Same           | None         | Low         |
| Cython .so    | -30%         | -50%           | Cython       | High        |
| Nuitka binary | -40%         | -30%           | Nuitka       | Medium      |

### Conclusion

For the context_bundle_capture.py hook, bytecode compilation offers the best balance of:

- Meaningful performance improvement (10-20% faster startup)
- Zero additional dependencies
- Minimal maintenance overhead
- Automatic fallback capability

This approach is similar to how TypeScript/Bun handle compilation, but adapted to Python's ecosystem where bytecode compilation is the standard optimization rather than transpilation to a different language.
