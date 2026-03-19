# Minimal VS Code orchestrator

A **minimal** orchestrator that ships with FITPAC so VS Code users (with Continue or Claude/Roo) can drop these folders where they need them and start using FITPAC right away. It is a **demonstrator**—good for learning the flow and trying FITPAC without the full orchestrator. It is not intended for production as-is; you can expand or replace it to suit your needs (e.g. add step triggers, task files, or your own tooling).

## What's in this package

- **orchestrator/** — One instruction file (`00-minimal-fitpac-loop.md`) that defines the full loop.
- **.continue/rules/** — Rule file(s) for the **Continue** extension. Copy `.continue/` to project root.
- **claude/** — **CLAUDE.md** for Claude Code / Roo. Copy `claude/CLAUDE.md` to project root as **CLAUDE.md** (or copy `claude/` as **.claude/** if you use directory form).

You can use **Continue only**, **Claude/Roo only**, or **both** in the same project; the loop and paths are the same.

## Install (new user, new VS Code project)

1. **Have FITPAC in the project.** Copy or clone the **FITPAC** directory (with `patterns/`, `master_index.yaml`, and optionally `docs/`) to the project root so the path **FITPAC/** exists. The agent reads only `FITPAC/master_index.yaml` and `FITPAC/patterns/`.
2. **Install the minimal orchestrator.** From this package (e.g. the `Reference-Orchestrators/VSCode/` folder):
   - Copy **orchestrator/** to the **project root** so the project has **orchestrator/00-minimal-fitpac-loop.md**.
   - **For Continue:** Copy **.continue/** to the **project root** so you have **.continue/rules/** with the FITPAC rule.
   - **For Claude/Roo:** Copy **claude/CLAUDE.md** to the **project root** as **CLAUDE.md** (or copy the **claude/** folder into your project as **.claude/** so you have **.claude/CLAUDE.md**).
3. **Open the project in VS Code** with Continue and/or Claude Code / Roo installed. No venv or external tools required.

## Use

- In VS Code, open the AI chat (Continue or Claude/Roo) and type your idea or feature request. The agent should load **orchestrator/00-minimal-fitpac-loop.md** and run the full loop: **Socratic round** (up to 3 questions; the agent is verbose about what it's doing and why) → **your spec** → **code** → **spec from code** → **comparison** → **plain-language run report**. The user sees the report in the chat and can read the artifacts below.
- To run the loop explicitly, describe what you want to build or say "run FITPAC" or "run the FITPAC loop"; the agent will load the loop and use your message as prose input.

## Where things go (project root)

All paths are relative to the **project root**. Folders are created on demand.

| What                                            | Where                                                |
| ----------------------------------------------- | ---------------------------------------------------- |
| **Your spec** (from the Socratic round)         | **specs/c_spec_1.md**                                |
| **Spec extracted from code**                    | **specs/d_spec_1_{session_id}.md**                   |
| **Application code**                            | **app/**                                             |
| **Tests**                                       | **tests/**                                           |
| **Run report** (plain-language "what happened") | **reports/run_report_1_{session_id}.md**             |
| **Comparison report** (did spec match code?)    | **reports/comparison_1_{session_id}.md** (and .json) |
| **Code summary** (choices made while coding)    | **reports/code_summary_1_{session_id}.json**         |
| **Consultation log** (pattern lookups)          | **logs/log-{session_id}.jsonl**                      |

When this package lives under **src/**, code is still written under **app/** at project root so **src/** is not overwritten.

## Refine and re-run

- User can **edit specs/c_spec_1.md** and say "run again" to re-run the loop (code → derive → compare → report).
- User can **answer the Socratic questions** in a follow-up message; the agent can update the spec and run the rest of the loop.

## Difference from the full orchestrator

This minimal package does **not** use:

- **orchestrator/current_task.json** or the state machine
- Step triggers (/step1-prose, /step2-code, etc.)
- **metadata/** or human/autonomous iteration counters
- Session reset or "process the current task"

It is a single-instruction, stateless loop so a new user can experience prose → spec → code → derived spec → report. For the full FITPAC loop with task file, branching, and human decision, use the main **orchestrator/** and rules at the repo root (this package does not modify those).
