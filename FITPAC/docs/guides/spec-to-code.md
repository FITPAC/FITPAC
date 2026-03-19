# Spec to code

This guide describes, in practical terms, how a **coding agent** can use the pattern library when implementing from a structured spec: when to consult, what to load, and how to report. The **normative rules** for consultation and the master index live in RFC-0001 and RFC-0004 plus `FITPAC/master_index.yaml`; this page is **informative** and restates those rules in a workflow-oriented way.

## Design Summary (if present)

The spec may contain a plain-language **Design Summary** (section 8 in the [spec schema](../reference/spec-schema.md)). The coding agent should use it **only when resolving ambiguity** (e.g. multiple valid paths, Unresolved / agent-decided items). The structured spec remains authoritative; the summary is for guidance only.

## When to consult

In a typical FITPAC setup, a coding agent will **enter consultation mode** in situations such as:

- Confidence dropping at or below the consult threshold (for example, from 0.95 baseline to 0.90 or lower; see `confidence_model` in `FITPAC/master_index.yaml`).
- Any test failure during implementation.
- Detection of an ambiguity trigger (for example, `unknown_domain_term`, `retry_instability`, `security_risk_detected`, `missing_boundary_manifest`).
- Detection of an invariant violation.
- Discovery of multiple equally valid implementation paths.

The exact rules for when consultation is mandatory are defined normatively in RFC-0001 and RFC-0004 and encoded in `FITPAC/master_index.yaml`.

## Consultation protocol (workflow version)

A practical way to implement the consultation loop is:

1. **Load** `FITPAC/master_index.yaml` as your entry point.
2. **Classify** the situation using `ambiguity_triggers` — each trigger maps to a minimal list of pattern fragments (for example, `security_risk_detected` → `security.p1`, `security.p2`, `security.p5`, `security.p6`, `security.p7`).
3. **Load only** those fragments from `pattern_map`; avoid loading full pattern files unless you have a specific reason to do so.
4. **Apply** the guidance from those fragments to your current decision; if the situation is still unresolved, emit a `SpecAmbiguityDetected` or `SpecProposal` event as described in the ontology patterns.
5. **Emit** a consultation event following the schema in `FITPAC/master_index.yaml` (see `telemetry` and `audit_log`). Keep fields like **inflection_point** and **resolution_applied** in plain language so humans can audit them.
6. **Recheck** confidence; if it is still at or below the consult threshold, repeat from step 2 or escalate.

### Classifying when confidence drops

When confidence drops due only to a **drop condition** (for example `failed_test` or `invariant_uncertain`), it is still useful to classify the situation via `ambiguity_triggers` in `FITPAC/master_index.yaml` to obtain the fragment list to load. Drop conditions that are not obviously tied to an existing trigger have dedicated mappings such as `failed_test`, `invariant_uncertain`, `multi_valid_paths`, `error_taxonomy_undefined`, and `partial_effect_uncertain`, each pointing to the fragments that can help resolve the situation.

If a trigger has an empty fragment list or no fragment can be found, you should still emit a consultation event, record that no fragments were loaded, and proceed with reduced confidence, as described in the master index reference.
