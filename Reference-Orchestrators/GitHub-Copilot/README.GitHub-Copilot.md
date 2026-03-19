# Minimal GitHub Copilot orchestrator

A **minimal** orchestrator that ships with FITPAC so GitHub Copilot users can drop these folders where they need them and start using FITPAC right away. It is a **demonstrator**—good for learning the flow and trying FITPAC without the full orchestrator. It is not intended for production as-is; you can expand or replace it to suit your needs (e.g. add step triggers, task files, or your own tooling).

## What's in this package

- **orchestrator/** — One instruction file (`00-minimal-fitpac-loop.md`) that defines the full loop.
- **github/** — **copilot-instructions.md** to copy into your repo's **.github/** so Copilot has repository-wide instructions. Copy the contents so your repo has **.github/copilot-instructions.md** (merge or replace as needed).

## Install (new user, new project)

1. **Have FITPAC in the project.** Copy or clone the **FITPAC** directory (with `patterns/`, `master_index.yaml`, and optionally `docs/`) to the project root so the path **FITPAC/** exists. The agent reads only `FITPAC/master_index.yaml` and `FITPAC/patterns/`.
2. **Install the minimal orchestrator.** From this package (e.g. the `Reference-Orchestrators/GitHub-Copilot/` folder):
   - Copy **orchestrator/** to the **project root** so the project has **orchestrator/00-minimal-fitpac-loop.md**.
   - Copy **github/copilot-instructions.md** into your repo's **.github/** directory as **.github/copilot-instructions.md** (create **.github/** if needed; merge with existing instructions or replace).
3. **Use the project** in a Copilot-enabled environment (VS Code, JetBrains, GitHub.com). No venv or external tools required.

If you prefer not to copy files manually, you can also use the repo‑level `Reference-Orchestrators/setup.sh` script where available, or open the **Universal** package and paste its instruction block directly into your Copilot **Repository Instructions** or workspace‑level configuration so Copilot knows how to run the minimal FITPAC loop.

**Note:** GitHub Copilot may not follow instructions identically every time. Keep instructions clear and imperative; refine the spec and run again if the outcome differs from what you want.

## Use

- In a Copilot chat (VS Code, JetBrains, or GitHub.com), describe what you want to build—your idea or feature request. The agent should follow the custom instructions and run the minimal FITPAC loop: load **orchestrator/00-minimal-fitpac-loop.md**, then **Socratic round** (up to 3 questions; be verbose) → **your spec** → **code** → **spec from code** → **comparison** → **plain-language run report**. The user sees the report in the chat and can read the artifacts below.
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

It is a single-instruction, stateless loop so a new user can experience prose → spec → code → derived spec → report. For the full FITPAC loop with task file, branching, and human decision, use the main **orchestrator/** and instructions at the repo root (this package does not modify those).
