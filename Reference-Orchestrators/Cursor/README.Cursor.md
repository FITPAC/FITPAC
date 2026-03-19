# Minimal Cursor orchestrator

A **minimal** orchestrator that ships with FITPAC so Cursor users can drop these folders where they need them and start using FITPAC right away. It is a **demonstrator**—good for learning the flow and trying FITPAC without the full orchestrator. It is not intended for production as-is; you can expand or replace it to suit your needs (e.g. add step triggers, task files, or your own tooling).

## What’s in this package

- **orchestrator/** — One instruction file (`00-minimal-fitpac-loop.md`) that defines the full loop.
- **cursorrules/** — A `.cursorrules` file to copy to project root so the agent runs the loop when the user types their idea.
- **cursor/** — Optional skill and README to copy into `.cursor/` for an explicit “run FITPAC” trigger.

## Install (new user, new Cursor project)

1. **Have FITPAC in the project.** Copy or clone the **FITPAC** directory (with `patterns/`, `master_index.yaml`, and optionally `docs/`) to the project root so the path **FITPAC/** exists. The agent reads only `FITPAC/master_index.yaml` and `FITPAC/patterns/`.
2. **Install the minimal orchestrator.** From this package (e.g. the `src/` folder or a copied `minimal-fitpac/` folder):
  - Copy **orchestrator/** to the **project root** so the project has **orchestrator/00-minimal-fitpac-loop.md**.
  - Copy the file **cursorrules/.cursorrules** to the **project root** as **.cursorrules** (replace or create).
  - (Optional) Copy **cursor/skills/** into the project’s **.cursor/skills/** so the “minimal FITPAC” skill is available.
3. **Open the project in Cursor.** No venv or external tools required.

If you prefer not to copy files manually, you can also use the repo‑level `Reference-Orchestrators/setup.sh` script, which performs this installation for you, or copy the equivalent **Universal** instructions into Cursor’s **Custom Instructions** so the agent knows how to run the minimal FITPAC loop.

## Use

- User types their idea or feature request in Cursor Chat. The agent runs the full loop: **Socratic round** (up to 3 questions; the agent is verbose about what it’s doing and why) → **your spec** → **code** → **spec from code** → **comparison** → **plain-language run report**. The user sees the report in the chat and can read the artifacts below.
- **Explicit trigger (if skill installed):** User says “run FITPAC” or “minimal FITPAC”; the agent loads the same loop and runs it, using the user’s previous or current message as prose.

## Where things go (project root)

All paths are relative to the **project root**. Folders are created on demand.


| What                                            | Where                                                |
| ----------------------------------------------- | ---------------------------------------------------- |
| **Your spec** (from the Socratic round)         | **specs/c_spec_1.md**                                |
| **Spec extracted from code**                    | **specs/d_spec_1_{session_id}.md**                   |
| **Application code**                            | **app/**                                             |
| **Tests**                                       | **tests/**                                           |
| **Run report** (plain-language “what happened”) | **reports/run_report_1_{session_id}.md**             |
| **Comparison report** (did spec match code?)    | **reports/comparison_1_{session_id}.md** (and .json) |
| **Code summary** (choices made while coding)    | **reports/code_summary_1_{session_id}.json**         |
| **Consultation log** (pattern lookups)          | **logs/log-{session_id}.jsonl**                      |


When this package lives under **src/**, code is still written under **app/** at project root so **src/** is not overwritten.

## Refine and re-run

- User can **edit specs/c_spec_1.md** and say “run again” to re-run the loop (code → derive → compare → report).
- User can **answer the Socratic questions** in a follow-up message; the agent can update the spec and run the rest of the loop.

## Difference from the full orchestrator

This minimal package does **not** use:

- **orchestrator/current_task.json** or the state machine
- Step triggers (/step1-prose, /step2-code, etc.)
- **metadata/** or human/autonomous iteration counters
- Session reset or “process the current task”

It is a single-instruction, stateless loop so a new user can experience prose → spec → code → derived spec → report. For the full FITPAC loop with task file, branching, and human decision, use the main **orchestrator/** and **.cursorrules** at the repo root (this package does not modify those).
