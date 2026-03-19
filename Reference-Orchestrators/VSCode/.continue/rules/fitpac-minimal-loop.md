---
name: minimal-fitpac
description: Run the minimal FITPAC loop when the user describes what they want to build. Load orchestrator/00-minimal-fitpac-loop.md and execute the full sequence (Socratic → spec → code → derive → compare → reports).
---

# Minimal FITPAC loop rule

## When to apply

When the user's message describes **what they want to build** (their idea, feature request, or prose): load **orchestrator/00-minimal-fitpac-loop.md** (relative to project root; if missing, try **src/orchestrator/00-minimal-fitpac-loop.md**) and **execute the full sequence** in that file. Use the user's message as the prose input.

## FITPAC (read-only)

- **FITPAC/** is the standard directory (patterns, master_index.yaml). Do **not** modify FITPAC/patterns/ or FITPAC/master_index.yaml.
- Agents **read** only FITPAC/master_index.yaml and FITPAC/patterns/ (never FITPAC/docs/). Application code and artifacts live outside FITPAC.

## Where things go (project root)

All paths are relative to the **project root**. Create folders on demand.

| Purpose | Location |
|--------|----------|
| **Your spec** (from the Socratic round) | **specs/c_spec_1.md** |
| **Spec extracted from code** | **specs/d_spec_1_{session_id}.md** |
| **Application code** | **app/** |
| **Tests** | **tests/** |
| **Run report** (plain-language "what happened") | **reports/run_report_1_{session_id}.md** |
| **Comparison report** (did spec match code?) | **reports/comparison_1_{session_id}.md** (and .json) |
| **Code summary** (choices made while coding) | **reports/code_summary_1_{session_id}.json** |
| **Consultation log** (pattern lookups) | **logs/log-{session_id}.jsonl** |

When the package lives under **src/**, code is still written under **app/** at project root.

## Skip the loop

Do **not** run the loop when the user's message is clearly not about building something (e.g. "what is FITPAC?", "list files", "explain line 5"). Answer normally.

## Re-run or refine

- **"run again"** / **"run FITPAC again"** / **"do another run"**: Load the loop and run it again. Use **specs/c_spec_1.md** as the canonical spec (or the user's latest message as new prose if they provide it).
- **"refine"** / **"update the spec"** + feedback: Update **specs/c_spec_1.md**, then run the rest of the loop (code → derive → compare → report).

## Decision triage

- **Critical** decisions (security, authorization, API surface, invariant) with no FITPAC pattern: **stop and ask the user** (e.g. SpecAmbiguityDetected). Do not guess.
- Routine or cosmetic decisions: autonomous when a pattern applies; log in the consultation log when consulting.
