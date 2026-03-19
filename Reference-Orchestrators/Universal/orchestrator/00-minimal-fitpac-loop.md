# Minimal FITPAC loop

Run this sequence when the user sends a message that is their idea or prose. Use the user's message as the **prose input**. Complete the full flow: Socratic round → spec → code → derive → compare → reports.

**Paths:** All paths are relative to **project root**. Ensure **FITPAC/** exists (read-only). Create **specs/**, **reports/**, **logs/**, **app/** on demand.

| What | Where |
|------|--------|
| Application code | **app/** |
| Tests | **tests/** (project root) |
| Your spec | **specs/c_spec_1.md** |
| Spec from code | **specs/d_spec_1_{session_id}.md** |
| Run report (plain language) | **reports/run_report_1_{session_id}.md** |
| Comparison report (spec vs spec) | **reports/comparison_1_{session_id}.md** and **.json** |
| Code summary | **reports/code_summary_1_{session_id}.json** |
| Consultation log | **logs/log-{session_id}.jsonl** |

**Session:** Generate one **session_id** per run (e.g. 8-char hex or `YYYYMMDD-HHMMSS`). Use **canonical_id** `"1"` and this **session_id** for all artifacts in this run.

---

## 1. Socratic round and canonical spec (be verbose)

- Treat the user's message as **prose** describing what they want to build.
- **Be verbose:** This step involves the human. Explain what you are doing and why at each stage:
  - Before asking: e.g. "I'm going to ask a few clarifying questions so the spec reflects your intent; here’s why each one matters."
  - For each question: state why you are asking it (e.g. boundaries, security, invariants) and how the answer will shape the spec.
  - Before writing the spec: briefly say how you are mapping their prose and answers to the spec structure (entities, constraints, boundaries, etc.).
  - When using defaults: state what you are defaulting and why (e.g. "You didn’t specify X; I’m assuming Y so we can proceed; you can change this in the spec and run again.").
- **Ask up to 3 clarifying questions** (Socratic style). Focus on security, invariants, and boundaries when relevant. Do not guess; surface gaps.
- **Write the canonical spec** using **only** `FITPAC/00_primitive_spine.md`. Map prose to entities, constraints, boundaries, authorities, relations, context, time (Layer 1 and Layer 2). For anything the prose does not specify, use **reasonable defaults** and state them briefly in the Design summary.
- **Spec format:** Sections 1–8 in order (Entities and ontology; Constraints and invariants; Authorities and policies; Boundaries and transactions; Temporal behavior; Goals and acceptance; Evidence and scenarios; **Design summary**). Use control vocabulary REQUIRE, RULE, EMIT, NOTE. YAML front-matter: **spec_kind** `canonical`, **canonical_id** `"1"`, **version** `1`, **schema_version** `"fitpac-spec-v1"`, **created_by** `minimal-fitpac`, **created_at** (ISO timestamp).
- **Write** **specs/c_spec_1.md** (create **specs/** if needed).
- Do **not** read `FITPAC/docs/`.

---

## 2. Code from spec

- **Input:** **specs/c_spec_1.md** (the canonical spec you just wrote).
- **Output:** Implement the behavior in **sections 1–7** of the spec under **app/** (create **app/** if needed). Put tests in **tests/** at project root. Use the Design summary (section 8) only to resolve ambiguity.
- **FITPAC consultation (minimal, mandatory):**
  - You MUST load **FITPAC/master_index.yaml** at the start of this step and follow its rules (consult_threshold, ambiguity_triggers, minimal_loading_rule, precedence_hierarchy).
  - If confidence drops to or below the consult threshold (0.90), OR any ambiguity_trigger condition is detected, OR any test fails, OR multiple equally valid implementation paths exist, you MUST consult the pattern library:
    - Use **ambiguity_triggers** to choose the trigger_rule and fragment list.
    - Use **pattern_map** to resolve module keys to paths under **FITPAC/patterns/**.
    - Load ONLY the fragment(s) listed for that trigger (do not load full pattern files; do not load FITPAC/docs).
  - When you consult, you MUST append one JSON line to **logs/log-{session_id}.jsonl** (create **logs/** if needed) with: **timestamp** (ISO 8601), **session_id**, **inflection_point**, **ambiguity_type**, **trigger_rule**, **pattern_selected** (module key and resolved pattern file path), **fragment_loaded**, **resolution_applied**, **resolution_result** (Solved | Partial | Unsolved), **confidence_before**, **confidence_after**, **contributing_factors** (array of { condition, delta } for drop conditions that applied), **reasoning** (plain-English: trigger(s) observed, fragments consulted, resolution chosen, justification for alternatives rejected, and evidence links when relevant; per RFC-0004 §7), **tokens_loaded_estimate** (optional; rough token count of fragments loaded), **schema_version** `"fitpac-audit-v1"`. One JSON object per line (jsonl).
  - **Demonstrator requirement (guarantee ≥ 1 pattern reference per run):** At least once per run, you MUST select ≥ 1 pattern fragment reference derived from **FITPAC/master_index.yaml** and append ≥ 1 JSONL entry to **logs/log-{session_id}.jsonl**.
    - If no ambiguity_trigger fired during implementation, you MUST perform a **demo consult** using the fallback fragment **spec_code_roundtrip.p1** (resolve via **pattern_map** → `patterns/spec_code_roundtrip.md`) and log it as a consultation event.
    - **Hard gate:** Before writing the final run report, verify the consultation log for this session has at least 1 line. If it has 0 lines, emit the demo consult entry and then continue.
- **Code summary:** Write **reports/code_summary_1_{session_id}.json** with at least: **canonical_id** `"1"`, **session_id**, **generated_at** (ISO), **proposed_additions** (array of SpecProposals: id, proposed_behavior, choice_rationale, pattern_reference). Create **reports/** if needed.
- **Portability:** Code in **app/** must not depend on FITPAC/, orchestrator/, logs/, reports/, or specs/ at runtime. Tests in **tests/** may import from **app/**.

---

## 3. Derive spec from code

- **Input:** Code under **app/** and **tests/**.
- **Output:** A **derived spec** that describes what the code actually does, using the **same schema** as the canonical spec (sections 1–7 for comparison; section 8 optional: "Derived spec; extracted from implementation.").
- **Sections (same order):** 1. Entities and ontology, 2. Constraints and invariants, 3. Authorities and policies, 4. Boundaries and transactions, 5. Temporal behavior, 6. Goals and acceptance, 7. Evidence and scenarios. Use REQUIRE, RULE, EMIT, NOTE. Same section titles as canonical for diff-friendliness.
- **Front-matter:** **spec_kind** `derived`, **canonical_id** `"1"`, **session_id**, **version** `1`, **schema_version** `"fitpac-spec-v1"`.
- **Write** **specs/d_spec_1_{session_id}.md**. Optionally use **reports/code_summary_1_{session_id}.json** and **logs/log-{session_id}.jsonl** to link implementation-defined choices and SpecProposals.

---

## 4. Compare canonical vs derived and write comparison report

- **Input:** **specs/c_spec_1.md** (canonical) and **specs/d_spec_1_{session_id}.md** (derived).
- **Compare** only sections 1–7. Section 8 is excluded from structural comparison.
- **Decide:** Do the specs match (normative content aligned; only cosmetic differences) or not?
- **Write** both:
  - **reports/comparison_1_{session_id}.md** — Human-readable comparison report. At the top include a **Result** section: outcome ("Specs match" or "Specs do not match") and next step. Then: Evidence and links (paths to canonical spec, derived spec, code summary, consultation log, this report), short evidence summary, metadata (canonical_id, session_id, derived_spec path). If match: summary of convergence, brief timeline. If mismatch: Additions (not in spec), Missing features, Other differences, and **Corrective actions for coding agent** (ordered list).
  - **reports/comparison_1_{session_id}.json** — Machine-readable: **schema_version** `"fitpac-spec-diff-v1"`, **canonical_id** `"1"`, **session_id**, **comparison_result** `"match"` or `"mismatch"`, **additions_not_in_canonical** (array: id, location, type, description, suggested_action), **summary** (e.g. requires_human_decision).

---

## 5. Plain-language run report for the user

- **Write** **reports/run_report_1_{session_id}.md** (or **reports/run_report.md** overwriting each run if you prefer a stable name).
- **Content (plain language):**
  - **What you asked for:** One or two sentences summarizing the user's prose.
  - **What I clarified:** The up to 3 Socratic questions you asked (and the defaults you used).
  - **What I built:** Short summary of the canonical spec (main entities, goals, boundaries).
  - **What the code does:** Short summary of the derived spec (what is actually implemented).
  - **Did it match?** Whether the specs matched or not, and one or two sentences on what differed (if anything).
  - **Where to look:** List the key artifacts: your spec (`specs/c_spec_1.md`), spec from code (`specs/d_spec_1_{session_id}.md`), code (`app/`), tests (`tests/`), comparison report (`reports/comparison_1_{session_id}.md`), this run report. Encourage the user to read the comparison report for details and to refine the spec and run again if they want changes.

---

## Response shape

In your reply to the user:

1. **Brief acknowledgment** of their idea.
2. **Socratic questions** (up to 3), with **verbose** explanation of why you are asking each one and what you will do with the answers. Note any defaults you use and why.
3. **What you did:** "I ran the minimal FITPAC loop: spec → code → derived spec → comparison. Here’s your plain-language report."
4. **Inline or paste** the key parts of **reports/run_report_1_{session_id}.md** (or the full report) so the user sees it in the chat.
5. **One-line pointer:** "Comparison report: reports/comparison_1_{session_id}.md. Code is in app/, your spec in specs/c_spec_1.md. To refine, edit the spec or answer the questions above and run again."

This minimal loop does not use **orchestrator/current_task.json** or any task file; it is stateless.
