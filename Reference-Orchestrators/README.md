# FITPAC Reference Orchestrators

Minimal orchestrators that ship with FITPAC so you can use the FITPAC loop in your preferred IDE. Each package is a **demonstrator**—good for learning the flow; expand or replace for production.

## Quick install (recommended)

From your **project root** (with FITPAC available in the project), run the setup script for your environment.

**Unix (macOS / Linux):**

```bash
./FITPAC/Reference-Orchestrators/setup.sh
```

Or, if Reference-Orchestrators is at a different path:

```bash
./Reference-Orchestrators/setup.sh
```

**Windows (PowerShell):**

```powershell
.\FITPAC\Reference-Orchestrators\setup.ps1
```

Or:

```powershell
.\Reference-Orchestrators\setup.ps1
```

The script asks which IDE you use (Cursor, Windsurf, VS Code, GitHub Copilot, Roo Code, or Universal) and copies the correct files to your project root.

- **Unix:** Use `--force` to skip overwrite confirmations (e.g. for CI).
- **Windows:** Use `-Force` to skip overwrite confirmations (e.g. for CI).

## Supported environments

| IDE | Package | What gets copied |
|-----|---------|-------------------|
| **Cursor** | [Cursor/](Cursor/) | `.cursorrules`, `orchestrator/`, optional `.cursor/skills/` |
| **Windsurf** | [Windsurf/](Windsurf/) | `.windsurfrules`, `orchestrator/` |
| **VS Code** (Continue / Claude) | [VSCode/](VSCode/) | `.continue/`, `CLAUDE.md`, `orchestrator/` |
| **GitHub Copilot** | [GitHub-Copilot/](GitHub-Copilot/) | `.github/copilot-instructions.md`, `orchestrator/` |
| **Roo Code** | [Roo-Code/](Roo-Code/) | `.clinerules`, `orchestrator/` |
| **Universal** (JetBrains, Zed, etc.) | [Universal/](Universal/) | No copy; use **FITPAC_INSTRUCTIONS.md** — paste its contents into your AI's system prompt or custom instructions. |

## Manual install

See each package’s README for step-by-step copy instructions:

- [Cursor/README.md](Cursor/README.md)
- [Windsurf/README.md](Windsurf/README.md)
- [VSCode/README.md](VSCode/README.md)
- [GitHub-Copilot/README.md](GitHub-Copilot/README.md)
- [Roo-Code/README.md](Roo-Code/README.md)
- [Universal/README.md](Universal/README.md)

## Prerequisite

Your project must have the **FITPAC** directory at the project root (with `patterns/`, `master_index.yaml`). The agent reads only `FITPAC/master_index.yaml` and `FITPAC/patterns/`.
