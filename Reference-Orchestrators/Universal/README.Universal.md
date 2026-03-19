# Universal FITPAC instructions

For **JetBrains**, **Zed**, or any other IDE that does not have a dedicated FITPAC orchestrator: use the **Universal** instructions so your AI assistant follows the FITPAC minimal loop.

## What's in this package

- **FITPAC_INSTRUCTIONS.md** — A single Markdown file. Copy its **contents** into your AI's System Prompt or Custom Instructions in your IDE. No file is copied to the project root by this package; the agent still needs **FITPAC/** in the project and, for the full loop, **orchestrator/00-minimal-fitpac-loop.md** (you can copy the `orchestrator/` folder from another Reference-Orchestrator, e.g. Cursor or Windsurf, if you want the agent to load the detailed loop).

## Install

1. **Have FITPAC in the project.** Copy or clone the **FITPAC** directory to the project root so **FITPAC/** exists (with `patterns/`, `master_index.yaml`).
2. **Add the instructions to your IDE.** Open **FITPAC_INSTRUCTIONS.md** from this package, copy all of its contents, and paste them into your AI's "System Prompt", "Custom Instructions", or equivalent setting in your IDE (e.g. JetBrains AI, Zed Composer).
3. **(Optional)** Copy **orchestrator/** from another Reference-Orchestrator (e.g. `Reference-Orchestrators/Cursor/orchestrator/`) to your project root so the agent can load **orchestrator/00-minimal-fitpac-loop.md** when running the loop.

## Use

When you describe what you want to build in chat, the agent should follow the FITPAC minimal loop: Socratic round → spec → code → derived spec → comparison → run report. Artifacts appear under **specs/**, **app/**, **reports/**, and **logs/** at project root as described in FITPAC_INSTRUCTIONS.md.
