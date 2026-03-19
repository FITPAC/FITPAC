---
name: minimal-fitpac
description: Run the minimal FITPAC loop (Socratic round → spec → code → derive → compare → plain-language report). Use when the user says run FITPAC, minimal FITPAC, fitpac run, or do the FITPAC loop.
---

# Minimal FITPAC loop

## When to apply

Apply when the user says **run FITPAC**, **minimal FITPAC**, **fitpac run**, **do the FITPAC loop**, or similar.

## What to do

1. Load **orchestrator/00-minimal-fitpac-loop.md** (or **src/orchestrator/00-minimal-fitpac-loop.md** if the package lives under src/).
2. Use the user's **current or latest message** as the prose input (or ask for one sentence describing what they want to build if the message was only the trigger).
3. Execute the **full sequence**: Socratic round (verbose—explain what you’re doing and why) → write **specs/c_spec_1.md** → implement under **app/** → derive **specs/d_spec_1_{session_id}.md** → compare → write **reports/comparison_1_{session_id}.md** and .json → write **reports/run_report_1_{session_id}.md** (plain language).
4. In your reply, include the plain-language run report and point the user to the comparison report and artifacts (code in **app/**, spec in **specs/**, comparison report in **reports/**).
