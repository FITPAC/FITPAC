# FITPAC minimal loop — repository custom instructions

When the user's message describes **what they want to build** (idea, feature request, or prose), run the minimal FITPAC loop. Load **orchestrator/00-minimal-fitpac-loop.md** (project root) and execute the full sequence. Use the user's message as the prose input.

## FITPAC (read-only)

- **FITPAC/** contains patterns and master_index.yaml. Do **not** modify FITPAC/patterns/ or FITPAC/master_index.yaml.
- Read only **FITPAC/master_index.yaml** and **FITPAC/patterns/** (never FITPAC/docs/). Application code and artifacts live outside FITPAC.

## Paths (project root)

All paths are relative to the **project root**. Create folders on demand.

| Purpose | Location |
|--------|----------|
| Your spec (from Socratic round) | **specs/c_spec_1.md** |
| Spec extracted from code | **specs/d_spec_1_{session_id}.md** |
| Application code | **app/** |
| Tests | **tests/** |
| Run report (plain language) | **reports/run_report_1_{session_id}.md** |
| Comparison report | **reports/comparison_1_{session_id}.md** and **.json** |
| Code summary | **reports/code_summary_1_{session_id}.json** |
| Consultation log | **logs/log-{session_id}.jsonl** |

When the repo has **src/**, still write code under **app/** at project root.

## Loop sequence

1. **Load** **orchestrator/00-minimal-fitpac-loop.md** (or **src/orchestrator/00-minimal-fitpac-loop.md** if under src/).
2. **Execute** the sequence: Socratic round (verbose — explain what you are doing and why) → write **specs/c_spec_1.md** → implement under **app/** and tests in **tests/** → derive **specs/d_spec_1_{session_id}.md** → compare specs → write **reports/comparison_1_{session_id}.md** and **.json** → write **reports/run_report_1_{session_id}.md** (plain language).
3. In the Socratic step, be **verbose**: state why you are asking each question, how answers shape the spec, and what you are defaulting and why.

## When to skip

Do **not** run the loop when the message is clearly not about building something (e.g. "what is FITPAC?", "list files", "explain line 5"). Answer normally.

## Re-run and refine

- **"run again"** / **"run FITPAC again"**: Load the loop and run it again. Use **specs/c_spec_1.md** as the canonical spec (or the user's latest message as new prose if they provide it).
- **"refine"** / **"update the spec"** + feedback: Update **specs/c_spec_1.md**, then run the rest of the loop (code → derive → compare → report).

## Decision triage

- **Critical** decisions (security, authorization, API surface, invariant) with no FITPAC pattern: **stop and ask the user**. Do not guess.
- Routine or cosmetic decisions: autonomous when a pattern applies; log in the consultation log when consulting.
