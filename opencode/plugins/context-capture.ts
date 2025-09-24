import { spawn } from "child_process"
import type { ChildProcess } from "child_process"
import * as path from "path"

type HookHandler = (payload: unknown) => Promise<void> | void

type HookRegistry = {
  on(event: string, handler: HookHandler): void
}

type PluginAPI = {
  projectRoot?: string
  hooks: HookRegistry
  logger: {
    info(message: string, meta?: unknown): void
    warn(message: string, error?: unknown): void
    error(message: string, error?: unknown): void
  }
}

type PluginModule = {
  name: string
  version: string
  register(api: PluginAPI): void
}

const PYTHON_SCRIPT = "context_bundle_capture_opencode.py"
const HOOK_DIR = ".opencode/hooks"

class ContextCapturePlugin {
  constructor(private readonly api: PluginAPI) {
    this.projectRoot =
      api.projectRoot ?? process.env.OPENCODE_PROJECT_ROOT ?? process.cwd()
  }

  async forward(eventType: string, payload: unknown): Promise<void> {
    try {
      await this.invokePython(eventType, payload)
    } catch (error) {
      this.api.logger.error(
        `Context capture hook failed for event ${eventType}`,
        error,
      )
    }
  }

  private pythonBinary(): string {
    return process.env.OPENCODE_PYTHON ?? process.env.PYTHON ?? "python3"
  }

  private async invokePython(
    eventType: string,
    payload: unknown,
  ): Promise<void> {
    const pythonBinary = this.pythonBinary()
    const scriptPath = path.join(this.projectRoot, HOOK_DIR, PYTHON_SCRIPT)
    const serialized = JSON.stringify(payload ?? {})

    await new Promise<void>((resolve, reject) => {
      const child: ChildProcess = spawn(
        pythonBinary,
        [scriptPath, eventType],
        {
          cwd: this.projectRoot,
          env: {
            ...process.env,
            OPENCODE_PROJECT_ROOT: this.projectRoot,
            OPENCODE_PROJECT_DIR: this.projectRoot,
          },
          stdio: ["pipe", "pipe", "pipe"],
        },
      )

      let stderr = ""

      if (!child.stdin) {
        reject(new Error("Context capture process stdin unavailable"))
        return
      }

      child.stdin.write(serialized)
      child.stdin.end()

      child.stderr?.on("data", (chunk: string | Uint8Array) => {
        stderr += chunk.toString()
      })

      child.on("close", (code: number | null) => {
        if (code && code !== 0) {
          const error = new Error(
            `Context capture script exited with code ${code}${
              stderr ? `: ${stderr.trim()}` : ""
            }`,
          )
          reject(error)
          return
        }
        if (stderr.trim()) {
          this.api.logger.warn(
            `Context capture emitted warnings: ${stderr.trim()}`,
          )
        }
        resolve()
      })

      child.on("error", (error: Error) => {
        reject(error)
      })
    })
  }
}

const plugin: PluginModule = {
  name: "context-capture",
  version: "1.0.0",
  register(api: PluginAPI) {
    const capturePlugin = new ContextCapturePlugin(api)

    // Register hooks for context capture
    api.hooks.on("tool.execute.after", async (payload) => {
      await capturePlugin.forward("post-tool", payload)
    })

    api.hooks.on("session.start", async (payload) => {
      await capturePlugin.forward("session-start", payload)
    })

    api.hooks.on("user.prompt.submitted", async (payload) => {
      await capturePlugin.forward("user-prompt", payload)
    })
  },
}

export default plugin
