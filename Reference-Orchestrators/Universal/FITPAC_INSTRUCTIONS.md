# FITPAC minimal loop — system prompt / custom instructions

**Copy the contents of this file into your AI's System Prompt or Custom Instructions** (JetBrains, Zed, or any other IDE that accepts a custom system prompt). This gives the agent the minimal FITPAC loop and paths. You still need the **FITPAC/** directory in your project (with `patterns/` and `master_index.yaml`). Optionally copy **orchestrator/00-minimal-fitpac-loop.md** to your project root from the Universal or another orchestrator package so the agent can load the full loop.

---

## FITPAC (read-only)

- **FITPAC/** is the standard directory (patterns, master_index.yaml). Do **not** modify FITPAC/patterns/ or FITPAC/master_index.yaml.
- Agents **read** only FITPAC/master_index.yaml and FITPAC/patterns/ (never FITPAC/docs/). Application code and artifacts live outside FITPAC.

## Where things go (project root)

All paths are relative to the **project root**. Create folders on demand.


| Purpose                                         | Location                                             |
| ----------------------------------------------- | ---------------------------------------------------- |
| **Your spec** (from the Socratic round)         | **specs/c_spec_1.md**                                |
| **Spec extracted from code**                    | **specs/d_spec_1_{session_id}.md**                   |
| **Application code**                            | **app/**                                             |
| **Tests**                                       | **tests/**                                           |
| **Run report** (plain-language "what happened") | **reports/run_report_1_{session_id}.md**             |
| **Comparison report** (did spec match code?)    | **reports/comparison_1_{session_id}.md** (and .json) |
| **Code summary** (choices made while coding)    | **reports/code_summary_1_{session_id}.json**         |
| **Consultation log** (pattern lookups)          | **logs/log-{session_id}.jsonl**                      |


When the project has **src/**, code is still written under **app/** at project root.

## Trigger: run the minimal loop

When the user's message describes **what they want to build** (idea, feature request, or prose):

1. **Load** **orchestrator/00-minimal-fitpac-loop.md** (relative to project root). If missing, try **src/orchestrator/00-minimal-fitpac-loop.md**.
2. **Execute** the sequence in that file: Socratic round (verbose — explain what you are doing and why) → write **specs/c_spec_1.md** → implement under **app/** and tests in **tests/** → derive **specs/d_spec_1_{session_id}.md** → compare specs → write **reports/comparison_1_{session_id}.md** and **.json** → write **reports/run_report_1_{session_id}.md** (plain language).
3. In the Socratic step, be **verbose**: state why you are asking each question, how answers shape the spec, and what you are defaulting and why.

**Skip the loop** when the message is clearly not about building something (e.g. "what is FITPAC?", "list files", "explain line 5"). Answer normally.

## Re-run and refine

- **"run again"** / **"run FITPAC again"** / **"do another run"**: Load the loop and run it again. Use **specs/c_spec_1.md** as the canonical spec (or the user's latest message as new prose if they provide it).
- **"refine"** / **"update the spec"** + feedback: Update **specs/c_spec_1.md**, then run the rest of the loop (code → derive → compare → report).

## Decision triage

- **Critical** decisions (security, authorization, API surface, invariant) with no FITPAC pattern: **stop and ask the user** (e.g. SpecAmbiguityDetected). Do not guess.
- Routine or cosmetic decisions: autonomous when a pattern applies; log in the consultation log when consulting.

---

## Consultation protocol (optional, for spec→code)

- Load only **FITPAC/master_index.yaml** as the initial configuration. Use **pattern_map** to resolve module keys to pattern files under FITPAC/patterns/. Fetch pattern **fragments on demand**.
- When confidence drops at or below the consult threshold (or a test fails, or ambiguity is detected), **consult** the pattern library using **ambiguity_triggers** and the listed fragments; emit a consultation log line to **logs/log-{session_id}.jsonl** with the full audit schema (per RFC-0004 §7): timestamp, session_id, inflection_point, ambiguity_type, trigger_rule, fragment_loaded, resolution_applied, resolution_result, confidence_before, confidence_after, **contributing_factors** (array of { condition, delta }), **reasoning** (plain-English: trigger(s) observed, fragments consulted, resolution chosen, justification for alternatives rejected, evidence links when relevant), and optionally tokens_loaded_estimate.
- When patterns conflict, use **precedence_hierarchy** in master_index.yaml (lower number wins).

