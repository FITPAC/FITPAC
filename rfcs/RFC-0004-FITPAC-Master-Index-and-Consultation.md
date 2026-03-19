---
RFC: 0004
Title: FITPAC Master Index and Consultation Semantics
Author: Paul Roy
Status: Final
Version: 1.0.0
Date: 2025-03-17
Depends-on: RFC-0001
Supersedes: None
license: CC-BY-4.0
license_url: https://creativecommons.org/licenses/by/4.0/
copyright_holder: Paul Roy and FITPAC Contributors
attribution_note: Attribution required under CC BY 4.0.
adoption_status: adopted
standard_inclusion: canonical-reference
---

# RFC-0004: FITPAC Master Index and Consultation Semantics

## 1. Scope

This document defines the normative semantics of the FITPAC **master index** (`FITPAC/master_index.yaml`) and the **consultation protocol** for coding agents. RFC-0001 requires a deterministic precedence hierarchy, a confidence model, ambiguity triggers, minimal fragment loading, and an audit trail; `FITPAC/docs/reference/master-index.md` and `FITPAC/master_index.yaml` implement those requirements.

This RFC makes that surface explicit and binds conformance to the behavior described here.

---

## 2. Master Index as Unified Entry Point

The file `FITPAC/master_index.yaml` is a **normative reference implementing this section**. A FITPAC-conformant implementation:

- **MUST** load `FITPAC/master_index.yaml` (or an equivalent manifest) as the **unified context entry point** for spec→code agents.
- **MUST** treat its `precedence_hierarchy`, `pattern_map`, `confidence_model`, `ambiguity_triggers`, `consultation_protocol`, `telemetry`, and `audit_log` sections as the authoritative configuration for precedence, consultation, and audit behavior.
- **MUST NOT** bypass or silently override these fields when claiming FITPAC conformance, except where a FITPAC Profile (per RFC-0002) explicitly and validly overrides them.

The descriptive document `FITPAC/docs/reference/master-index.md` is a **normative reference** that explains the intended meaning of each field; where this RFC and that document disagree, this RFC is authoritative.

### 2.1 Equivalent Manifest Contract

An **equivalent manifest** is any artifact or service that provides the same effective configuration surface as `FITPAC/master_index.yaml`. To qualify as equivalent for FITPAC conformance, it:

- **MUST** expose, at minimum, all of the following semantics:
  - `pattern_map` (stable module keys mapped to pattern module locations or identifiers).
  - `precedence_hierarchy` (a deterministic ordering of modules, with defined comparison semantics).
  - `confidence_model` (baseline, drop conditions, consult threshold).
  - `ambiguity_triggers` (named conditions mapped to fragment IDs and a human-readable reason).
  - `consultation_protocol` parameters sufficient to implement the loop in Section 6.
  - `telemetry` configuration, including the consultation event channel/header and any routing keys.
  - `audit_log` schema, including required fields and reasoning expectations.
- **MUST** be reconstructable from the normative surface (`master_index.yaml` and other normative references) or, if used as the primary source of truth, **MUST** itself be treated as a normative reference and pinned by the version-locking mechanism described in RFC-0001 Section 5.
- **MAY** be implemented as a database, service endpoint, or generated file, provided that the effective configuration observed by agents is functionally equivalent to a conformant `master_index.yaml` and is stable for the duration of a conformance claim.

---

## 3. Precedence Hierarchy

The `precedence_hierarchy` section of `master_index.yaml` defines an ordered list of modules, with **1 = highest precedence**. Implementations:

- **MUST** use this hierarchy to resolve conflicts when multiple patterns apply.
- **MUST** ensure that modules associated with safety, security, integrity, and regulatory compliance outrank modules concerned only with ergonomics, performance, or budgets, unless a FITPAC Profile explicitly and validly reorders them in a stricter, domain-specific hierarchy.

Altering the precedence hierarchy:

- **Within the Standard Profile:** is constrained by RFC-0001 (security and ontology outrank ergonomics and budgets).
- **Within a domain profile:** is allowed provided the profile satisfies RFC-0002 (profiles tighten; they do not loosen).

The mechanics of how precedence is encoded (for example, numeric ordinals, ordered lists) are defined by `master_index.yaml` and its generator but the semantics above are normative.

---

## 4. Confidence Model and Drop Conditions

The `confidence_model` section of `master_index.yaml` defines:

- a `baseline` confidence value,
- a set of `drop_conditions` (condition → delta), and
- a `consult_threshold`.

A FITPAC-conformant coding agent:

- **MUST** start at `baseline` confidence.
- **MUST** apply all relevant `drop_conditions` when evidence appears (tests, static analysis, observed errors, pattern triggers, etc.).
- **MUST** enter consultation mode when confidence is **≤ consult_threshold**, following the consultation protocol below.

Profiles may **tighten** these values (higher baseline, higher consult threshold, additional drop conditions) but **MUST NOT** weaken them in ways that violate RFC-0001 or RFC-0002.

---

## 5. Ambiguity Triggers and Fragment Loading

The `ambiguity_triggers` section in `master_index.yaml` maps **named conditions** to:

- a minimal set of pattern fragments to load (for example, `security.p1`, `ontology.p5`), and
- a human-readable reason.

Implementations:

- **MUST** classify situations using `ambiguity_triggers` whenever consultation is entered (for example, when confidence falls to or below `consult_threshold` or multiple valid implementation paths exist).
- **SHOULD** take into account evidence such as test failures and invariant violations when determining which trigger applies.
- **MUST** load **only** the fragments listed for the active trigger, using `pattern_map` to locate pattern files.
- **MAY** chain multiple triggers where appropriate, but each consultation step **MUST** be associated with a specific trigger and fragment set.

Triggers that map to an empty fragment list (for example, `fragment_outdated`) are intentional; agents **MUST** still emit a consultation event and proceed with reduced confidence.

---

## 6. Consultation Protocol

The `consultation_protocol` section of `master_index.yaml` defines a loop that a FITPAC-conformant coding agent **MUST** implement:

1. Compute confidence using `confidence_model.drop_conditions`.
2. If confidence ≤ `consult_threshold`, enter **Reference Mode**.
3. Classify the situation using `ambiguity_triggers` to obtain a list of fragments.
4. Load only those fragments via `pattern_map`.
5. Apply the decision logic from those fragments.
6. Emit a consultation event (see Telemetry and Audit log).
7. Recompute confidence.
8. If confidence is still ≤ `consult_threshold`, repeat from step 3; if unresolvable, emit a spec-level ambiguity event (for example, `SpecAmbiguityDetected` or `SpecProposal`).

Implementations **MUST NOT** replace this loop with ad-hoc “best-effort” reading of arbitrary documentation when claiming FITPAC conformance.

---

## 7. Telemetry and Audit Log

The `telemetry` and `audit_log` sections of `master_index.yaml` define:

- the default consultation event header or channel name (for example, `FITPAC_CONSULTATION_EVENT_V1`),
- required fields for each consultation event,
- the entry schema for the audit log, and
- expectations around plain-English reasoning.

Implementations:

- **MUST** include required fields such as `inflection_point`, `ambiguity_type`, `trigger_rule`, `fragment_loaded`, `resolution_applied`, `resolution_result`, `confidence_before`, `confidence_after`, `contributing_factors`, and a reasoning field that captures at least: the trigger condition(s) observed, fragment IDs consulted, the chosen resolution, and a brief justification for why alternatives were rejected when applicable, plus links or references to evidentiary artifacts when those inform the decision.
- **SHOULD** keep reasoning fields in plain language that is understandable to human reviewers in their target environment; the exact event header or channel name is implementation- or profile-defined, but the presence and semantics of these fields are normative.
- **MUST** treat the audit log as append-only and record one entry per consultation event.
- **MUST NOT** record secrets, credentials, private keys, or other sensitive authentication material in cleartext in audit log entries, and **SHOULD** support redaction or structured fields to avoid leaking regulated personal data.

Profiles or local policies may add retention and external review requirements, but they do not weaken these core obligations.

---

## 8. Generation and Extension of `master_index.yaml`

The descriptive rules in `FITPAC/docs/reference/master-index.md` and the generator script `FITPAC/tools/generate_master_index.py` specify how to:

- discover pattern files,
- assign precedence,
- wire new modules and triggers into `pattern_map` and `ambiguity_triggers`, and
- preserve fragment ID immutability.

Normatively:

- Once a fragment ID (for example, `ontology.p5`, `privacy_data_protection.p3`) appears in `master_index.yaml` or in published documentation, it **MUST** be treated as immutable.
- Module keys in `pattern_map` **MUST NOT** be renamed once published; deprecation is done by documentation and higher-precedence rules, not removal or renumbering.
- New modules and triggers **MAY** be added, but new triggers **MUST** reference either existing or newly added fragment IDs, or explicitly use an empty list with a clear reason.

---

## 9. Normative References

The following artifacts are normative references for this RFC:

- `FITPAC/master_index.yaml` — authoritative machine-readable configuration for precedence, patterns, confidence model, triggers, consultation, telemetry, and audit log.
- `FITPAC/docs/reference/master-index.md` — normative reference that explains and elaborates the semantics of the master index fields.

If a distribution relocates these artifacts, equivalent files **MUST** be provided and clearly associated with this RFC for the distribution to remain FITPAC-conformant. For FITPAC 1.0.0, the normative versions of these artifacts are those identified by the version-locking mechanism described in RFC-0001 Section 5 (for example, in `fitpac_manifest.yaml`).

