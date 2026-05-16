# FITPAC Standard: Master Index (`master_index.yaml`)

License: CC-BY-4.0
License URL: https://creativecommons.org/licenses/by/4.0/
Copyright Holder: Paul Roy and FITPAC Contributors
Attribution Note: Attribution required under CC BY 4.0.

The **master_index.yaml** file is the **unified context** entry point for **coding agents** (spec→code). It encodes the **Rules of the Road** that an agent MUST follow to be **FITPAC‑conformant**.

This document summarizes those rules; see the full file for exact field names and values.

---

## 1. Loading rule (entry point)

- Load **only** `master_index.yaml` as the initial configuration.
- Fetch **pattern fragments on demand** using `pattern_map` and `ambiguity_triggers`; do **not** eagerly load entire pattern files unless explicitly required.

This keeps context small and ensures all behavior flows through the same precedence, confidence, and consultation model.

---

## 2. Value hierarchy (precedence)

Field: `precedence_hierarchy`

- **1 = highest importance**. When two patterns conflict, **lower number wins**.
- The hierarchy is **as defined by `master_index.yaml`** (see [Generating the master index](#generating-the-master-index)). The reference distribution assigns precedence so that safety, integrity, and correctness modules outrank ergonomics, performance, and budgets; the exact ordering is in `precedence_hierarchy` in that file.

**FITPAC‑conformant agents MUST:**

- Treat the ordering in `precedence_hierarchy` (as defined by `master_index.yaml`) as the single value hierarchy; higher-precedence modules (e.g. security, ontology in the reference distribution) outrank lower-precedence ones (e.g. ergonomics, budgets).
- Use the precedence map to break ties when multiple patterns could apply.

The `pattern_map` in the same file includes all pattern files under `patterns/`. The primitive spine (`00_primitive_spine.md`) is a separate reference document at the FITPAC root and is not listed in `pattern_map`. This value hierarchy is how FITPAC encodes organizational priorities into machine‑readable form.

### Extension packs

The reference distribution registers the **`fitpac.prose_compiler`** extension (RFC-0006) at precedence **31** with pattern module `extensions/fitpac_prose_compiler/patterns/fitpac_prose_compiler.md`. Pack manifest: `FITPAC/extensions/fitpac_prose_compiler/fitpac_prose_compiler_manifest.yaml`, registered from the repository root `fitpac_manifest.yaml` `extensions:` list.

---

## 3. Confidence model and drop conditions

Field: `confidence_model`

- `baseline`: default confidence (0.95).
- `drop_conditions`: map from **condition** → **delta** (negative float).
- `consult_threshold`: confidence at or below which consultation is **mandatory** (0.90).

Examples of drop conditions:

- Domain and ontology: `unknown_domain_term`, `invalid_state_transition`, `missing_invariant`.
- Correctness and tests: `failed_test`, `tests_tautological_or_nondeterministic`, `refactor_without_equivalence`.
- Security and governance: `security_risk_detected`, `privilege_escalation`, `approval_required`, `irreversible_action`.
- Time and concurrency: `deadline_missed`, `concurrent_conflict`, `clock_time_misuse`, `resource_leak_risk`.
- Boundaries and dependencies: `missing_boundary_manifest`, `dependency_unpinned`, `schema_version_mismatch`.

**FITPAC‑conformant agents MUST:**

1. Start at the **baseline** confidence.
2. Apply all relevant **drop_conditions** when evidence appears (tests, static analysis, pattern triggers, etc.).
3. If resulting confidence is **≤ consult_threshold**, **enter Reference Mode** and consult the pattern library.
4. After applying patterns, **recompute confidence**. If it is still ≤ threshold, consult again or escalate (e.g. `SpecAmbiguityDetected` or `SpecProposal`).

---

## 4. Ambiguity triggers and pattern loading

Fields: `ambiguity_triggers`, `pattern_map`

- `pattern_map` ties logical modules (e.g. `security`, `ontology`, `boundaries`) to specific pattern files in `patterns/`.
- `ambiguity_triggers` maps **named conditions** (e.g. `retry_instability`, `security_risk_detected`, `unknown_domain_term`) to:
  - The **minimal list of pattern fragments** to load (e.g. `security.p1`, `ontology.p5`).
  - A short **reason** string explaining why those fragments apply.

**FITPAC‑conformant agents MUST:**

1. Detect when a situation matches an `ambiguity_triggers` key (e.g. test failure that indicates `retry_instability`).
2. Load **only** the listed pattern fragments (not whole files) using `pattern_map`.
3. Apply the decision logic from those fragments.
4. Recompute confidence and either proceed, consult again, or emit a spec‑level event (`SpecAmbiguityDetected` or `SpecProposal` per RFC-0004) when rules dictate.
5. When confidence drops due only to a drop condition (see `confidence_model.drop_conditions`), classify the situation via `ambiguity_triggers` (including dedicated entries such as `failed_test`, `invariant_uncertain`, `multi_valid_paths`, `error_taxonomy_undefined`, and `partial_effect_uncertain`) so that fragment loading remains deterministic.

This makes consultation **deterministic and auditable**, instead of arbitrary prompt engineering.

**Empty pattern lists:** Some triggers (e.g. `fragment_outdated`) map to an empty `patterns: []` list. This is **intentional**: there is no single fragment to load. The agent MUST still emit a consultation event, append an audit log entry recording that no fragments were loaded, and proceed with reduced confidence. See `consultation_protocol.minimal_loading_rule` in `master_index.yaml`.

---

## 5. Consultation protocol

Field: `consultation_protocol`

The consultation protocol defines **when** and **how** agents must consult the pattern library.

Triggers include (paraphrased from `consultation_protocol.trigger`):

- Confidence ≤ `consult_threshold`.
- Any test failure.
- An `ambiguity_trigger` condition is detected.
- An invariant violation is detected.
- Multiple equally valid implementation paths exist.

Steps (summarized from `consultation_protocol.steps`):

1. Compute confidence using `confidence_model.drop_conditions`.
2. If confidence ≤ threshold, **enter Reference Mode**.
3. Classify the ambiguity using `ambiguity_triggers`.
4. Load **only** the fragments listed for that trigger.
5. Apply the decision logic from the fragment.
6. Emit a consultation event (see Telemetry; schema in `audit_log`). Implementations may persist events; FITPAC does not define storage.
7. Recheck confidence; if still ≤ threshold, repeat from step 3.
8. If unresolvable, emit `SpecAmbiguityDetected` or `SpecProposal` (see RFC-0004 §6).

**FITPAC‑conformant agents MUST implement this loop**, not ad‑hoc \"read some docs and hope\" behavior.

---

## 6. Telemetry and consultation events

Field: `telemetry`

Consultation events are standardized under the header `FITPAC_CONSULTATION_EVENT_V1` (or an implementation-/profile-defined equivalent; see RFC-0004 §7). Required fields include:

- `inflection_point` — plain‑English description of what happened.
- `ambiguity_type`, `trigger_rule` — how the situation was classified.
- `pattern_selected`, `fragment_loaded` — which pattern and fragment were applied.
- `reasoning_delta` — what changed in the decision space after consulting.
- `resolution_applied`, `resolution_result` — what rule was applied and whether it solved the issue.
- `confidence_before`, `confidence_after`.
- `contributing_factors` — which drop conditions applied and their deltas.

**FITPAC‑conformant agents SHOULD:**

- Emit a consultation event for every consultation.
- Keep all reasoning fields in **plain English** for auditability.

---

## 7. Audit log (event schema)

Field: `audit_log`

- Defines the **format** (e.g. JSON lines) and **entry schema** for consultation events. The `file` key in `master_index.yaml` is an example default; where events are stored is implementation-defined.
- One entry is emitted per consultation.

Key requirements (RFC-0004 §7 is the source of truth):

- Each entry MUST include `inflection_point`, `resolution_applied`, confidence values, `contributing_factors`, and a **`reasoning`** field. The reasoning field MUST capture at least: the trigger condition(s) observed, fragment IDs consulted, the chosen resolution, a brief justification for why alternatives were rejected when applicable, and links or references to evidentiary artifacts when those inform the decision. Reasoning MUST be in plain language for human auditability.
- If `resolution_result` is `Unsolved`, implementations SHOULD flag for human review.

---

## 8. Extending `master_index.yaml` safely

As the pattern library and standard evolve, `master_index.yaml` may gain new modules, ambiguity triggers, and drop conditions. To preserve stability for existing FITPAC‑conformant implementations:

- **New ambiguity triggers**:
  - Every new entry under `ambiguity_triggers` MUST reference one or more existing or newly added fragments in `patterns/*.md` using stable fragment IDs (e.g. `security.p1`, `spec_code_roundtrip.p3`).
  - If a trigger has no applicable fragments yet, it MUST still be represented explicitly with an empty pattern list and a clear `reason`, so agents can log the consultation and proceed with reduced confidence.

- **Fragment ID immutability**:
  - Once a fragment ID (e.g. `ontology.p5`, `privacy_data_protection.p3`) appears in `master_index.yaml` or in any published documentation, treat it as **immutable**.
  - Do not rename module keys in `pattern_map` or renumber `pN` rules inside pattern files. Deprecate behavior via documentation or additional, higher‑precedence rules instead of removal or renumbering.

- **Adding new modules**:
  - Introduce a new module by adding a stable key to `pattern_map` and, if relevant, to `precedence_hierarchy`.
  - Module keys are the canonical names for fragment IDs; header `ID` or `domain` aliases in pattern files are for humans only and MUST NOT change the fragment IDs.

These rules ensure that new triggers and modules can be added without breaking existing agents, indexes, or audit logs.

---

## Generating the master index

The **master index** is intended to be **generated or updated** when the pattern library changes (e.g. when patterns are added or removed). Only the patterns actually present under `FITPAC/patterns/` should appear in `pattern_map`; **precedence is 1 = highest importance** (exact ordering as defined by this file) so that the most critical patterns have the lowest numbers and win in conflicts.

In normal use, you **do not hand‑author** `master_index.yaml`. Instead, you:

- generate it once if it is missing in a local install, and
- regenerate it whenever you add, remove, or rename pattern files in your local `FITPAC/patterns/` tree (including additional pattern packs you bring in yourself).

**Generator:** This repository includes a generator script that can recreate `master_index.yaml` from the pattern tree:

- **Script:** `FITPAC/tools/generate_master_index.py`
- **Discovery:** Recursively finds all `*.md` files under the patterns directory, including subdirectories. The primitive spine lives at the FITPAC root and is not under `patterns/`. Supports path-based namespacing and optional version segments (e.g. `@1.0.0` in path or filename).
- **Precedence:** Assigns precedence with 1 = highest (ordering as defined by the generator or `--precedence-override`). Unknown modules are appended in deterministic order. Use `--precedence-override` to supply a custom ranking.
- **Usage:** `python FITPAC/tools/generate_master_index.py [--patterns-dir PATH] [--output PATH] [--precedence-override YAML] [--strict] [--verbose]`

It is not required to use FITPAC to run this generator. FITPAC has no dependencies. This optional script is only used to rebuild `FITPAC/master_index.yaml` if it’s missing or if the user has added patterns.

If `master_index.yaml` is missing, run this script to generate it from the patterns directory. If you extend the pattern library beyond the base 30 pattern modules, rerun the generator so your local `master_index.yaml` reflects your extended library. The script embeds default `confidence_model`, `consultation_protocol`, `telemetry`, and `audit_log` sections so generation works without an existing file.

---

## 9. Summary

Together, the fields in `master_index.yaml` define the **operational rules** for FITPAC‑conformant agents:

- **Precedence and priorities** (value hierarchy).
- **When to doubt yourself** (drop conditions and confidence).
- **How to ask for help** (ambiguity triggers and consultation protocol).
- **How to extend the standard safely** (stable module keys and fragment IDs, additive triggers).
- **How to explain your decisions** (telemetry and audit log).

Agents that follow these rules, operate on FITPAC specs (Canonical/Derived), and build against the primitive and pattern ontology in `patterns/` satisfy the **master index portion** of the FITPAC core as defined in RFC‑0001. To be fully **FITPAC‑conformant**, implementations MUST also meet the conformance criteria in RFC‑0001 §12 and, where Profiles are supported, RFC‑0002 §11.
