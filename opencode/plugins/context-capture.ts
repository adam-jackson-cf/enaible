import { spawn } from "child_process"
import type { ChildProcess } from "child_process"
import * as fs from "fs"
import { promises as fsp } from "fs"
import path from "path"

type HookHandler = (payload: unknown) => Promise<void> | void

type HookRegistry = {
  on(event: string, handler: HookHandler): void
}

type CommandContext = {
  args: string[]
  write(message: string): void
  writeError?(message: string): void
}

type CommandRegistration = {
  name: string
  summary: string
  usage: string[]
  execute(ctx: CommandContext): Promise<void>
}

type PluginAPI = {
  projectRoot?: string
  hooks: HookRegistry
  commands: {
    register(command: CommandRegistration): void
  }
  logger: {
    info(message: string, meta?: unknown): void
    warn(message: string, error?: unknown): void
    error(message: string, error?: unknown): void
    debug?(message: string, meta?: unknown): void
  }
}

type PluginModule = {
  name: string
  version: string
  register(api: PluginAPI): void
}

type ContextCaptureEvent = "post-tool" | "user-prompt" | "session-start"

type CommandAction = "enable" | "disable" | "status"

const COMMAND_NAME = "setup-context-capture"
const ENABLE_FLAG_FILENAME = ".context-capture-enabled"
const PYTHON_SCRIPT = "context_bundle_capture_opencode.py"
const BASE_MODULE = "context_capture_base.py"
const REDACTOR_SCRIPT = "sensitive_data_redactor.py"
const CONFIG_FILE = "context_capture_config.json"

const EVENT_MAP: Record<string, ContextCaptureEvent> = {
  "tool.execute.after": "post-tool",
  "session.start": "session-start",
  "user.prompt.submitted": "user-prompt",
}

class ContextCaptureBridge {
  private readonly projectRoot: string
  private readonly hooksDir: string
  private readonly baseModulePath: string
  private readonly captureScriptPath: string
  private readonly redactorScriptPath: string
  private readonly configPath: string
  private readonly enableFlagPath: string
  private readonly sharedContextDir: string
  private readonly documentationPath: string
  private docCache: string | null = null
  private scriptMissingLogged = false

  constructor(private readonly api: PluginAPI) {
    this.projectRoot =
      api.projectRoot ?? process.env.OPENCODE_PROJECT_ROOT ?? process.cwd()
    this.hooksDir = path.join(this.projectRoot, ".opencode", "hooks")
    this.baseModulePath = path.join(this.hooksDir, BASE_MODULE)
    this.captureScriptPath = path.join(this.hooksDir, PYTHON_SCRIPT)
    this.redactorScriptPath = path.join(this.hooksDir, REDACTOR_SCRIPT)
    this.configPath = path.join(this.hooksDir, CONFIG_FILE)
    this.enableFlagPath = path.join(this.hooksDir, ENABLE_FLAG_FILENAME)
    const repositoryRoot = path.resolve(__dirname, "..", "..")
    this.sharedContextDir = path.join(
      repositoryRoot,
      "shared",
      "setup",
      "context",
    )
    this.documentationPath = path.join(
      repositoryRoot,
      "opencode",
      "commands",
      "setup-context-capture.md",
    )
  }

  async forward(event: ContextCaptureEvent, payload: unknown): Promise<void> {
    if (!(await this.isEnabled())) {
      return
    }

    if (!(await this.fileExists(this.captureScriptPath))) {
      if (!this.scriptMissingLogged) {
        this.api.logger.warn(
          `Context capture is enabled but ${PYTHON_SCRIPT} is missing. Run \`${COMMAND_NAME} enable\` to reinstall.`,
        )
        this.scriptMissingLogged = true
      }
      return
    }

    try {
      await this.invokePython(event, payload)
    } catch (error) {
      this.api.logger.error(
        `Context capture hook failed for event ${event}`,
        error,
      )
    }
  }

  async enable(): Promise<void> {
    await fsp.mkdir(this.hooksDir, { recursive: true })
    await this.copyFile(BASE_MODULE, false)
    await this.copyFile(PYTHON_SCRIPT, true)
    await this.copyFile(REDACTOR_SCRIPT, true)
    await this.copyFile(CONFIG_FILE, false)
    const marker = {
      enabledAt: new Date().toISOString(),
      python: this.pythonBinary(),
    }
    await fsp.writeFile(
      this.enableFlagPath,
      JSON.stringify(marker, null, 2),
      "utf8",
    )
    this.scriptMissingLogged = false
  }

  async disable(): Promise<void> {
    await this.removeFileIfExists(this.enableFlagPath)
  }

  async status(): Promise<{
    enabled: boolean
    scriptsPresent: boolean
    captureScriptPath: string
  }> {
    const enabled = await this.isEnabled()
    const scriptsPresent =
      (await this.fileExists(this.baseModulePath)) &&
      (await this.fileExists(this.captureScriptPath)) &&
      (await this.fileExists(this.redactorScriptPath)) &&
      (await this.fileExists(this.configPath))
    return {
      enabled,
      scriptsPresent,
      captureScriptPath: this.captureScriptPath,
    }
  }

  async renderDocumentation(): Promise<string> {
    if (this.docCache) {
      return this.docCache
    }
    try {
      const content = await fsp.readFile(this.documentationPath, "utf8")
      this.docCache = content
      return content
    } catch (error) {
      const fallback =
        "# Setup Context Capture\n\nDocumentation is missing. Ensure opencode/commands/setup-context-capture.md exists."
      this.docCache = fallback
      this.api.logger.warn(
        "Failed to load setup-context-capture documentation",
        error,
      )
      return fallback
    }
  }

  private async copyFile(
    filename: string,
    makeExecutable: boolean,
  ): Promise<void> {
    const source = path.join(this.sharedContextDir, filename)
    const destination = path.join(this.hooksDir, filename)

    try {
      await fsp.access(source, fs.constants.R_OK)
    } catch {
      throw new Error(`Missing required context capture asset: ${source}`)
    }

    await fsp.copyFile(source, destination)
    if (makeExecutable) {
      await fsp.chmod(destination, 0o755)
    }
  }

  private async removeFileIfExists(filePath: string): Promise<void> {
    try {
      await fsp.unlink(filePath)
    } catch (error) {
      if ((error as NodeJS.ErrnoException).code !== "ENOENT") {
        throw error
      }
    }
  }

  private async fileExists(filePath: string): Promise<boolean> {
    try {
      await fsp.access(filePath, fs.constants.F_OK)
      return true
    } catch {
      return false
    }
  }

  private async isEnabled(): Promise<boolean> {
    return this.fileExists(this.enableFlagPath)
  }

  private pythonBinary(): string {
    return process.env.OPENCODE_PYTHON ?? process.env.PYTHON ?? "python3"
  }

  private async invokePython(
    event: ContextCaptureEvent,
    payload: unknown,
  ): Promise<void> {
    const pythonBinary = this.pythonBinary()
    const serialized = JSON.stringify(payload ?? {})

    await new Promise<void>((resolve, reject) => {
      const child: ChildProcess = spawn(
        pythonBinary,
        [this.captureScriptPath, event],
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
    const bridge = new ContextCaptureBridge(api)

    Object.entries(EVENT_MAP).forEach(([hookName, event]) => {
      api.hooks.on(hookName, async (payload) => {
        await bridge.forward(event, payload)
      })
    })

    api.commands.register({
      name: COMMAND_NAME,
      summary:
        "Install and manage context capture hooks for session history bundling.",
      usage: [
        "opencode setup-context-capture enable",
        "opencode setup-context-capture disable",
        "opencode setup-context-capture status",
      ],
      async execute(ctx: CommandContext) {
        const errorWriter = ctx.writeError ?? ctx.write
        const action = (ctx.args[0] as CommandAction | undefined) ?? "status"
        const doc = await bridge.renderDocumentation()
        ctx.write(doc)

        if (!["enable", "disable", "status"].includes(action)) {
          errorWriter(
            `Unknown action "${ctx.args[0]}". Use one of: enable, disable, status.`,
          )
          return
        }

        if (action === "enable") {
          await bridge.enable()
          const status = await bridge.status()
          ctx.write(
            `Context capture enabled. Scripts present: ${
              status.scriptsPresent ? "yes" : "no"
            }.`,
          )
          return
        }

        if (action === "disable") {
          await bridge.disable()
          ctx.write(
            "Context capture disabled. Hooks remain installed but will not execute.",
          )
          return
        }

        const status = await bridge.status()
        const statusLine = status.enabled
          ? "Context capture is enabled."
          : "Context capture is disabled."
        ctx.write(statusLine)
        ctx.write(
          status.scriptsPresent
            ? `Hook scripts located at ${status.captureScriptPath}.`
            : "Hook scripts are missing. Run `opencode setup-context-capture enable`.",
        )
      },
    })
  },
}

export default plugin
