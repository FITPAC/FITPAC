---
title: FITPAC conformance checklist
status: informative
---

# FITPAC conformance checklist

This checklist summarizes the main conformance requirements from RFC-0001, RFC-0002, RFC-0003, RFC-0004, and RFC-0005 so you can quickly assess whether an implementation is **FITPAC-conformant**. For precise language, always refer back to the RFCs.

## 1. Language core and primitives

- [ ] Implementation understands and uses the Layer 1 and Layer 2 primitives from `00_primitive_spine.md` (see RFC-0003).
- [ ] No new Layer 1 primitives are introduced, and existing primitive semantics are not redefined.

## 2. Control grammar and spec schema

- [ ] Canonical and Derived specs follow the logical schema in `docs/reference/spec-schema.md` (entities, invariants, boundaries, authorities, goals, evidence).
- [ ] Specs use or map to the control grammar (REQUIRE, RULE, EMIT, NOTE) for structured content.
- [ ] Comparison reports between Canonical and Derived specs include:
  - [ ] Identifiers of the specs being compared.
  - [ ] An **Additions (not in spec)** section (present even if empty).
  - [ ] Classification of other differences as at least cosmetic, behavioral, and contractual.

## 3. Master index and consultation

- [ ] Coding agents load `FITPAC/master_index.yaml` as the unified context entry point.
- [ ] The implementation respects:
  - [ ] `precedence_hierarchy` for resolving conflicts between patterns.
  - [ ] `pattern_map` for locating modules and fragments.
  - [ ] `confidence_model` for baseline, drop conditions, and consult threshold.
  - [ ] `ambiguity_triggers` and `consultation_protocol` for when and how to consult.
- [ ] The consultation loop is implemented (classify, load minimal fragments, apply, emit event, recompute confidence, repeat or escalate).

## 4. Telemetry and audit

- [ ] Consultation events follow the schema in `master_index.yaml.telemetry` and `master_index.yaml.audit_log`.
- [ ] Each consultation event includes inflection point, trigger, fragments loaded, resolution applied, confidence before/after, and contributing factors.
- [ ] Reasoning fields are recorded in plain language suitable for human review.

## 5. Patterns and triggers

- [ ] Pattern modules under `patterns/*.md` use sequential `pN` rule numbering; once published, rule indices MUST NOT be renumbered. Gaps MAY exist due to deprecation; deprecated rules MUST remain present and clearly marked (see RFC-0005).
- [ ] Each rule includes required metadata fields (`triggers`, `requires_primitives`, `output_type`, `domain`, `category`) as described in `docs/reference/pattern-index.md`.
- [ ] Fragment IDs use `<module>.pN` where `<module>` is the key from `master_index.yaml.pattern_map`.
- [ ] Trigger values in pattern metadata are drawn from the taxonomy in `docs/reference/trigger-taxonomy.md` or documented namespaced extensions.

## 6. Stability and evolution

- [ ] Module keys and fragment IDs are treated as immutable once published.
- [ ] Additive changes (new modules, new rules, new triggers) do not break existing conformant implementations.
- [ ] Breaking changes (renaming modules, renumbering rules, changing primitive semantics) are treated as major version changes and go through an explicit migration path.

## 7. Profiles (if supported)

- [ ] Loaded profiles satisfy RFC-0002 (profiles tighten; they do not loosen the core).
- [ ] Profiles use a deterministic precedence hierarchy and preserve the ambiguity protocol and round-trip semantics.
- [ ] Experimental or non-standard profiles are clearly labeled and surfaced in audit logs.

If you can check all the relevant boxes above for your implementation and environment, you are likely **FITPAC-conformant**; for formal claims or certification, review the detailed conformance sections in RFC-0001 and RFC-0002.

