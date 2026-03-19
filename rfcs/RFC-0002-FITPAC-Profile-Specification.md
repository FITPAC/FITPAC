---
RFC: 0002
Title: FITPAC Profile Specification
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

# RFC-0002: FITPAC Profile Specification

## 1. Abstract

This document specifies the FITPAC Profile system: how domain-specific and regulatory configurations constrain the base FITPAC protocol without redefining it. Profiles enable a single protocol to scale from hobbyist use to regulated domains (e.g. nuclear safety, fintech, healthcare) while preserving core invariants and interoperability. This document defines what a profile is, what makes a profile FITPAC-compliant, how profiles are represented machine-readably, and how the Reference Profile and domain profiles relate to the core.

### 1.1 Conventions and Terminology

The key words **MUST**, **MUST NOT**, **SHOULD**, **MAY**, and **SHOULD NOT** in this document are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174] when they appear in ALL CAPS.

---

## 2. Relation to RFC-0001

RFC-0001 defines the **FITPAC core**: primitives, control grammar, ambiguity protocol, round-trip verification, namespace policy, and the requirement for deterministic precedence. It introduces Profiles as an extension point (Section 13) but does not define their structure or governance.

This document (RFC-0002) defines:

- The **profile mechanism**: what a profile is, what it may and may not do.
- **FITPAC-compliant profile** criteria.
- **Machine-readable profile schema** (normative for interoperability).
- The **FITPAC Reference Profile** (default configuration for general use).
- **Domain profiles** and the distinction between certified and experimental profiles.

Implementations that support Profiles MUST conform to this specification when loading, validating, or applying a profile. Implementations that do not support Profiles MUST still conform to RFC-0001 and use the Standard Reference Hierarchy when no profile is specified.

---

## 3. Three-Layer Model

FITPAC can be thought of as three layers. Only Layer 0 is non-negotiable; Layers 1 and 2 are configurations on top of it.

### 3.1 Layer 0 — Core Protocol (Non-Negotiable)

Defined in RFC-0001. Includes:

- Seven Layer 1 primitives and Layer 2 structural primitives.
- Control grammar (four semantic categories).
- Spec ambiguity protocol (confidence, condition-to-fragment mapping, minimal loading, escalation, audit).
- Round-trip verification model and comparison report requirements.
- Namespace policy (stable module keys, fragment IDs in reference form).
- Requirement for deterministic, documented precedence when patterns conflict.

**This is FITPAC.** No profile may alter it.

### 3.2 Layer 1 — Reference Profile

The **FITPAC Reference Profile** (e.g. version 1.0.0) is the default configuration for general use: newcomers, hobbyists, and teams that want “set and forget” safety without domain-specific regulation.

It defines:

- **Standard Reference Hierarchy:** Precedence ordering (e.g. security, ontology, ux, budgets, …) with Security and Ontology above Ergonomics and Budgets. Typically embodied in the reference `master_index.yaml`.
- **Default pattern set:** The reference 30 (or current) pattern modules shipped with FITPAC.
- **Default confidence model:** e.g. baseline 0.95, consult threshold 0.90, and reference drop conditions.
- **Default ambiguity triggers:** Condition-to-fragment mappings for the reference pattern set.

An implementation that loads no profile, or that loads the Reference Profile explicitly, MUST behave as if the Standard Reference Hierarchy and reference pattern set apply. The Reference Profile is **intended to satisfy** the Standard FITPAC Profile requirements in RFC-0001 (principle-based precedence and conformance); implementations that use it without modification are FITPAC-conformant (Standard Profile) when the reference hierarchy and pattern set meet those requirements.

### 3.3 Layer 2 — Domain Profiles

**Domain profiles** constrain the protocol for specific industries, regulators, or enterprises. Examples (informative):

- FITPAC Nuclear Safety Profile 1.0.0
- FITPAC FinTech Compliance Profile 1.2.0
- FITPAC Healthcare PHI Profile 1.0.0
- FITPAC High-Assurance Aerospace Profile 2.0.0

Domain profiles:

- MAY require specific pattern modules (and forbid others or specific rules).
- MAY tighten confidence thresholds and consult thresholds.
- MAY define an explicit precedence hierarchy for the domain (e.g. nuclear safety rules above generic security).
- MAY mandate audit retention, external review, or escalation behavior.
- MUST NOT redefine primitives, alter control grammar semantics, or remove core protocol requirements.

Domain profiles are **additive constraints** on the core. They allow regulators to standardize their domain while remaining FITPAC-compliant and interoperable at the core.

---

## 4. Definition of a Profile

A **FITPAC Profile** is:

> A constrained configuration of the base FITPAC standard that adds or tightens rules but does not redefine the core.

A profile is a formal, machine-readable artifact that implementations can load in addition to (or instead of) the default Reference Profile. When a profile is active, it governs precedence, required/forbidden patterns, confidence and audit behavior, and related parameters as specified in the profile document.

---

## 5. FITPAC-Compliant Profile Criteria

A profile is **FITPAC-compliant** if and only if all of the following hold:

1. **Primitives:** It does not redefine Layer 1 or Layer 2 primitives.
2. **Control grammar:** It does not alter the semantics of the four control grammar categories (REQUIRE, RULE, EMIT, NOTE).
3. **Ambiguity protocol:** It preserves the ambiguity protocol requirements (confidence model, condition-to-fragment mapping, minimal loading, escalation semantics, audit log). It MAY tighten thresholds or add triggers.
4. **Round-trip:** It preserves round-trip verification and comparison report requirements (same schema, Additions section, classification of differences).
5. **Precedence:** It uses a deterministic, documented precedence hierarchy. It MAY replace the Standard Reference Hierarchy with a domain-specific ordering that satisfies the principle in RFC-0001 Section 4 (higher-precedence concern classes—safety, security, integrity, compliance, correctness—outrank lower-precedence ones—ergonomics, performance, budgets) or a stricter domain rule. Treating a lower-precedence concern as higher-precedence (e.g. "performance is safety") is permitted only if the profile explicitly declares that mapping and documents the rationale in the profile or audit policy; see RFC-0001 Section 4 concern classes.
6. **Additive only:** It only adds constraints or tightens existing ones; it never removes or weakens core protocol constraints. **If a profile forbids or disables a behavior that the core protocol requires** (e.g. consultation when confidence is at or below threshold, or production of the Additions section in comparison reports), **the profile is invalid** and MUST NOT be applied.

**Golden rule:** Profiles tighten; they do not loosen.

Implementations that load a profile MUST validate it against these criteria before applying it. A profile that fails any criterion MUST NOT be applied as a FITPAC profile; implementations MAY reject it or treat it as an invalid overlay.

---

## 6. Machine-Readable Profile Schema

Profiles SHOULD be machine-readable so that agents and tooling can load them without human interpretation. The following schema is normative for interoperability; implementations that consume profiles MUST accept at least this structure (additional fields are permitted).

### 6.1 Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `profile.name` | string | Canonical profile identifier (e.g. `nuclear_safety_profile`, `reference`). |
| `profile.version` | string | Semantic version of the profile (e.g. `1.0.0`). |
| `profile.based_on` | string | FITPAC core version (e.g. `FITPAC 1.0.0`) or parent profile. |

### 6.2 Optional Constraint Fields

| Field | Type | Description |
|-------|------|-------------|
| `profile.required_modules` | list of string | Module keys that MUST be loaded and applied (subset of pattern_map). |
| `profile.forbidden_patterns` | list of string | Fragment IDs in **reference form** `<module>.pN` (e.g. `ux.p3`) that MUST NOT be used. Implementations SHOULD accept only reference-form IDs for interoperability; wildcards or module-level forbidding may be defined in a future specification. |
| `profile.precedence` | list of string | Ordered list of module keys; defines the value hierarchy (1 = first = highest). Overrides Standard Reference Hierarchy when present. |
| `profile.confidence.baseline` | number | Override for baseline confidence (e.g. 0.98). |
| `profile.confidence.consult_threshold` | number | Override for consult threshold (e.g. 0.95). |
| `profile.audit.retention` | string or object | Audit log retention requirement (e.g. `"indefinite"`, or policy object). |
| `profile.audit.external_review_required` | boolean | If true, certain escalation events require external human review. |
| `profile.audit.*` | — | Additional audit-related constraints; schema may be extended by domain. |

### 6.3 Example: Domain Profile (Informative)

```yaml
profile:
  name: "nuclear_safety_profile"
  version: 1.0.0
  based_on: "FITPAC 1.0.0"

  required_modules:
    - security
    - governance
    - boundary_contracts
    - compliance_audit

  forbidden_patterns: []   # or e.g. ["ux.p3"] to disallow a specific fast-path

  precedence:
    - security
    - ontology
    - governance
    - boundary_contracts
    - compliance_audit
    - resilience
    - ux
    - budgets

  confidence:
    baseline: 0.98
    consult_threshold: 0.95

  audit:
    retention: "indefinite"
    external_review_required: true
```

### 6.4 Example: Reference Profile (Informative)

The Reference Profile may be represented explicitly or implied by the absence of a profile. When explicit:

```yaml
profile:
  name: "reference"
  version: 1.0.0
  based_on: "FITPAC 1.0.0"
  # precedence, confidence, and pattern set follow reference master_index.yaml
  # No overrides; use Standard Reference Hierarchy and default 30 patterns.
```

### 6.5 Loading Order

When an implementation loads FITPAC with a profile:

1. Load FITPAC core (RFC-0001 semantics).
2. Load the profile document and validate it against Section 5.
3. Apply profile constraints: required/forbidden patterns, precedence overlay, confidence overlay, audit requirements.
4. Load pattern modules and master index (or profile-supplied mappings) consistent with the profile. The result MUST be a valid, deterministic configuration that satisfies both RFC-0001 and this specification.

---

## 7. Certified vs Experimental Profiles

To prevent silent weakening of safety, profiles are categorized as follows.

### 7.1 Certified (Standard) Profiles

**Certified profiles** are approved or recognized by the FITPAC governing body (or a designated authority). They:

- MUST maintain or strengthen the safety posture implied by the Standard Reference Hierarchy (safety, integrity, regulatory compliance outrank convenience, performance, resource budgets).
- MUST preserve all core protocol invariants.
- MAY only add constraints or tighten thresholds.

Certified profiles are suitable for regulated domains and for claims of “FITPAC-conformant (Profile: X).”

### 7.2 Experimental Profiles

**Experimental profiles** are not certified. They:

- MAY change precedence or relax certain defaults for research or optimization (e.g. performance-first experiments).
- MUST be clearly labeled as experimental (e.g. `profile.experimental: true` or equivalent).
- MUST cause implementations to disclose in the audit log that an experimental profile is in use and that it may not satisfy the Standard Profile principle.

This prevents silent weakening: users and auditors can see that a non-standard profile was applied.

### 7.3 Profile Identification

Profiles SHOULD identify their status (certified vs experimental) in the machine-readable document, e.g.:

- `profile.certified: true` and optionally `profile.certifying_authority: "FITPAC"` or domain regulator.
- `profile.experimental: true` for experiments.

Implementations that apply an experimental profile SHOULD log the profile name and version in the audit trail for each run.

---

## 8. Sharing and Compatibility

Profiles can be shared between users and organizations. For compatibility:

- **Schema:** Profiles that conform to the schema in Section 6 can be consumed by any implementation that supports RFC-0002.
- **Versioning:** Profiles use semantic versioning. A profile’s `based_on` ties it to a FITPAC core version; when the core is upgraded, profiles may need to be updated and re-validated.
- **Naming:** Profile names (e.g. `nuclear_safety_profile`) SHOULD be unique within a sharing scope to avoid collisions. Namespacing (e.g. `org.foo.nuclear_safety`) is recommended for non-official profiles.

Domain-wide standardization (e.g. all nuclear licensees use the same profile) is achieved by adopting a single, certified domain profile and distributing it through the same channels as the pattern library or regulatory guidance.

---

## 9. Why Profiles Matter

Without profiles:

- Enterprises and regulators would fork FITPAC or publish “FITPAC-compatible” guidance that diverges.
- Vendors would ship custom precedence and constraints with no common schema.
- The result would be compliant-but-incompatible ecosystems.

With profiles:

- The core remains one protocol (RFC-0001).
- The Reference Profile gives a simple default (Layer 1).
- Domain profiles (Layer 2) let regulators and enterprises standardize their domain without leaving FITPAC.
- Certified vs experimental labeling prevents silent weakening and supports auditability.

Profiles are not a threat to FITPAC; they are the mechanism by which FITPAC becomes infrastructure that scales across risk tiers and domains.

---

## 10. References

- RFC-0001: FITPAC 1.0.0 — Formal Intent Translation Protocol for Agentic Code
- FITPAC Master Index Reference: `docs/reference/master-index.md`
- FITPAC Governance and Versioning: `docs/reference/governance-versioning.md`
- [RFC 2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC 8174] Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words

---

## 11. Conformance

An implementation that supports FITPAC Profiles:

- MUST validate any loaded profile against the criteria in Section 5 before applying it.
- MUST apply only FITPAC-compliant profiles (or reject non-compliant ones).
- MUST support the machine-readable schema in Section 6 (at least the required fields and the optional constraint fields it claims to support).
- MUST reject a profile that uses fields the implementation does not support if ignoring those fields could weaken constraints (e.g. `forbidden_patterns`, `audit.external_review_required`). This prevents silently dropping constraint-strengthening fields while still claiming the profile was loaded.
- MUST document which profiles it supports (e.g. Reference, and any bundled or loadable domain profiles).
- When an experimental profile is applied, SHOULD record in the audit log that an experimental profile was used and its name and version.

A profile document is **RFC-0002-compliant** if it satisfies the schema in Section 6 and the criteria in Section 5. A FITPAC-compliant profile (per Section 5) that also conforms to this schema is suitable for sharing and for use in FITPAC-conformant implementations.
