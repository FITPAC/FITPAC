---
RFC: 0001
Title: FITPAC 1.0.0 — Formal Intent Translation Protocol for Agentic Code
Author: Paul Roy
Status: Final
Version: 1.0.0
Date: 2025-03-17
Depends-on: None
Supersedes: None
license: CC-BY-4.0
license_url: https://creativecommons.org/licenses/by/4.0/
copyright_holder: Paul Roy and FITPAC Contributors
attribution_note: Attribution required under CC BY 4.0.
adoption_status: adopted
standard_inclusion: canonical-reference
---

# RFC-0001: FITPAC 1.0.0 — Formal Intent Translation Protocol for Agentic Code

## 1. Abstract

This document specifies FITPAC (Formal Intent Translation Protocol for Agentic Code), an intermediate representation for human intent in agent-generated software. In the context of FITPAC 1.x, “formal” denotes a formalized, deterministic representation and procedure for intent and verification, not a formal-methods proof system. FITPAC defines a primitive ontology, a control grammar for specifications, a conflict-precedence model, a consultation protocol for handling ambiguity, and a round-trip verification model. The protocol is intended to enable deterministic mapping between prose intent, structured specifications, and code, with auditable evidence of alignment.

### 1.1 Conventions and Terminology

The key words **MUST**, **MUST NOT**, **SHOULD**, **MAY**, and **SHOULD NOT** in this document are to be interpreted as described in BCP 14 [RFC 2119] [RFC 8174] when they appear in ALL CAPS. These words may also appear in lower case; in that case they carry their natural language meaning and are not normative.

**Conformant vs. compliant:** **FITPAC-conformant** applies to implementations (agents, platforms, toolchains). **FITPAC-compliant** is a special case: it applies only to **FITPAC Profiles** as defined in RFC-0002. A profile is FITPAC-compliant when it satisfies the criteria in RFC-0002 §5. Implementations are described as conformant for protocol conformance; they are never described as compliant for that purpose.

### 1.2 Documentation Classes and Authority (Normative)

FITPAC uses three documentation classes:

- **RFCs (normative standards documents)**  
  Define the FITPAC protocol and conformance surface. When this RFC uses BCP 14 key words, those requirements are binding.
- **Normative references (non-RFC artifacts)**  
  Concrete files (e.g. pattern modules, `master_index.yaml`, reference schemas) that an RFC explicitly designates as normative. When this RFC (or another FITPAC RFC) states that implementations **MUST follow** a named document or file, the referenced artifact is a **normative dependency** for conformance, even if it is not itself formatted as an RFC.
- **Informative documentation (user manuals, guides, overviews)**  
  Explanatory material for humans (e.g. getting started guides, scenarios, and integrator manuals). These documents MAY recommend behaviors but do not, by themselves, create new conformance requirements.

The following rules apply:

1. **RFC precedence:** If an RFC and a non‑RFC document conflict, the RFC text is authoritative for FITPAC conformance.
2. **Normative dependency rule:** If an RFC says that a conformant implementation **MUST follow X** (where X is a specific file or document), then X (or the referenced portions of X) is a **normative reference**. Normative references MUST clearly identify their status (for example, via a `status: normative` or `status: normative-reference` front‑matter field).
3. **Informative default:** All other documents are informative by default. Informative documents SHOULD avoid introducing new uppercase BCP 14 keywords except when directly restating or citing a requirement from an RFC or normative reference (in which case they MUST include an explicit citation).
4. **Rebuildable surface:** All derived tooling (indexes, embeddings, caches, orchestration scripts) MUST be rebuildable from the RFCs plus normative references alone; they do not extend the normative surface.

An RFC labeled **Informational** MAY still contain normative requirements for FITPAC conformance when it uses BCP 14 keywords and defines conformance criteria; normativity is determined by those requirements and conformance sections, not by the Status label alone.

This RFC, together with RFC‑0002 and any future FITPAC RFCs, defines the complete normative standard. Normative references such as `00_primitive_spine.md`, `master_index.yaml`, and files under `docs/reference/` implement the standard where explicitly called out by RFCs.

### 1.3 File Naming Conventions

Spaces in file and artifact names are represented as follows. **Kebab-case** (hyphen `-`) is used for user-facing documents: RFCs, guides, and reference documentation (e.g. `spec-schema.md`, `getting-started.md`, `prose-to-spec.md`). **Snake_case** (underscore `_`) is used for files designed to be referenced or created by tooling: e.g. `00_primitive_spine.md`, `master_index.yaml`, canonical spec files `c_spec_1.md`, derived spec files `d_spec_1_{session_id}.md`, and pattern modules under `patterns/` (e.g. `domain_ontology.md`, `boundary_contracts.md`). Implementations and generators MUST follow this convention for normative artifacts they produce or reference.

---

## 2. Motivation

Agentic coding systems produce implementations from natural language or structured inputs. The gap between **syntactic intent** (what was said or written) and **semantic intent** (what was meant) introduces risk: agents may optimize for the former while violating the latter. Without a stable, machine-readable representation of intent, verification of "did the implementation realize what we meant?" is not systematically possible.

FITPAC addresses this by:

- Providing a **single computation model** (primitives) so that intent is expressed in implementation-agnostic terms.
- Requiring **consultation** when confidence drops or ambiguity is detected, instead of silent inference.
- Defining a **round-trip**: canonical spec → code → derived spec → comparison, so that alignment is evidenced rather than assumed.

The protocol does not prescribe storage, orchestration, or tooling; it defines the language and rules that conformant agents and toolchains must respect.

---

## 3. Definitions

### 3.1 Layer 1: Core Primitives

Every FITPAC specification and pattern is expressible as a composition of the following seven primitives. No additional atomic concepts are introduced by domain modules.

| Primitive        | Definition |
|------------------|------------|
| **Entity**       | A thing that can be identified and may have state; the unit of storage and identity. |
| **Transformation** | A change of state or a recorded occurrence; the unit of "what happened" or "what will happen." |
| **Constraint**   | A rule that must hold (invariant, legality condition, or validation rule). |
| **Authority**    | Who or what is allowed to perform an action; the unit of "who may do what." |
| **Relation**     | A link between entities or between entities and authorities (ownership, association). |
| **Context**      | Ambient or request-scoped information that affects interpretation (locale, tenant, trace). |
| **Time**         | Ordering, duration, deadlines, and time sources; the unit of "when" and "how long." |

### 3.2 Layer 2: Structural Primitives

Structural primitives are compositions of or specializations of the core primitives. Unlike the seven core primitives (Layer 1), which are sacrosanct and MUST NOT be extended or redefined, structural primitives MAY be extended by domain modules with additional compositions, provided they remain consistent with the core semantics.

| Primitive     | Definition |
|---------------|------------|
| **Transaction** | Boundary around a set of transformations that commit or roll back together. |
| **Boundary**    | Interface between contexts (service, process, trust zone); owns contract and error taxonomy. |
| **Projection**  | Derived view from entities/transformations (read model, snapshot). |
| **Capability**  | Subset of Authority; minted, scoped, and revocable. |
| **Policy**      | Structured Constraint (e.g. access rule, approval tier). |

Domain modules may constrain or specialize these primitives but MUST NOT redefine the core execution or constraint-evaluation semantics.

### 3.3 Control Grammar

Normative specification content is partitioned into exactly four semantic categories: obligations (preconditions, invariants), operational rules (control flow), outputs (events or artifacts), and non-normative commentary. Execution and comparison semantics are defined over these categories.

| Label (canonical) | Semantics | Primitive mapping |
|-------------------|-----------|-------------------|
| **REQUIRE** | Preconditions, invariants, obligations | Constraint, Policy |
| **RULE**    | Operational rules and control flow     | Transformation, Boundary, Transaction, Policy |
| **EMIT**    | Outputs, events, or artifacts produced  | Transformation, Projection |
| **NOTE**    | Non-normative commentary               | Ignored by structural diffs |

Implementations MAY use alternate labels or encodings that map 1:1 to these semantics; round-trip comparison uses the canonical semantics, not the literal string. Implementations MAY support additional headings for readability; only these four semantics are part of the control vocabulary.

---

## 4. Conflict Precedence Order

When two or more patterns or rules conflict, resolution is determined by a **value hierarchy** (precedence). The hierarchy MUST be deterministic, documented, and auditable. It is typically represented as an ordered list where **lower ordinal number denotes higher priority** (1 = highest); the representation is implementation- or profile-defined.

- To be **FITPAC-conformant**, an implementation MUST use a deterministic precedence hierarchy to resolve conflicts when multiple patterns apply. The hierarchy is defined in a master index (or equivalent manifest) or governed by a **FITPAC Profile** (see Section 13).
- In the absence of a specific Profile, conformant agents MUST use the **Standard Reference Hierarchy** defined in the master index. In the Standard Reference Hierarchy, Security and Ontology MUST outrank Ergonomics (UX) and Budgets.
- **Principle (normative):** The hierarchy encodes which concerns override which when they compete. Profiles MAY define custom hierarchies for their domain; see RFC-0002.
- **Standard FITPAC Profile:** An implementation satisfies the Standard FITPAC Profile if and only if its hierarchy ensures that constraints protecting **safety, integrity, or regulatory compliance** outrank constraints that optimize only for **convenience, performance, or resource budgets**. This is the default when using the FITPAC Reference Profile (see Section 13). Domain profiles MAY rank domain-specific patterns above generic ones (e.g. nuclear safety over generic security) and remain compliant provided the profile is FITPAC-compliant per RFC-0002.
- **Concern classes (informative):** To reduce ambiguity, higher-precedence concerns are understood to include at least: safety, security, integrity, regulatory compliance, and correctness (invariants, state legality). Lower-precedence concerns are understood to include at least: ergonomics (UX), performance (latency, throughput), and resource budgets (cost, iteration caps). Treating a lower-precedence concern (e.g. performance or cost) as if it were higher-precedence (e.g. "performance is safety") is permitted only when a **Profile** explicitly declares that mapping and documents the rationale in the profile or in audit policy; unstated rhetorical reclassification does not satisfy the Standard Profile principle.
- Implementations that use a hierarchy that does not satisfy the Standard Profile principle (e.g. convenience over safety) and are not governed by a certified domain profile SHOULD disclose this in the audit log.

*Example (informative):* Standard Reference Hierarchy ordering 1 = security, 2 = ontology, 3 = ux, 4 = budgets, … with domain-specific modules appended in a deterministic order.

---

## 5. Versioning Policy

FITPAC uses **semantic versioning** in the form **major.minor.patch** (e.g. 1.0.0).

- **Major (X.0.0):** Breaking change to the language core (primitive spine, control grammar), removal or renaming of module keys, renumbering of existing rules, or fundamental changes to the spec schema.
- **Minor (x.Y.0):** Additive or backward-compatible change (new pattern modules or rules, new triggers, new optional schema fields).
- **Patch (x.y.Z):** Non-semantic change (typos, documentation, clarifications that do not alter requirements or identifiers).

Version numbers apply independently to: (1) the language core, (2) core pattern modules, (3) the spec schema. In practice, compatible combinations of these versions are fixed for a given release and identified by a manifest.

For any distribution that claims conformance to **FITPAC 1.0.0**:

- The distribution **MUST** include a machine-readable manifest (for example, `fitpac_manifest.yaml`) that enumerates all normative references and, for each, records at least:
  - its identifier (e.g. path or URI),
  - its version string (where applicable), and
  - a content hash.
- Implementations **MUST** evaluate conformance for a given run against exactly one manifest version and **MUST** be able to identify, via that manifest, the specific versions of all normative references they used.

Distributions **MAY** embed normative references in a versioned package or add additional internal versioning schemes, but the manifest remains the normative pin for which artifacts constitute FITPAC 1.0.0 in that distribution.

**Stability:** The primitive spine, control grammar (the four semantic categories), and spec schema sections are expected to remain stable across minor and patch releases. Additive changes MUST NOT break existing conformant implementations.

---

## 6. Namespace Policy

- **Module keys:** Pattern modules are identified by a **module key** (e.g. `security`, `ontology`, `api_design`). The module key is the canonical identifier for fragment resolution. Human-oriented aliases (e.g. in file headers or `domain` fields) MUST NOT replace the module key when resolving or constructing fragment IDs.
- **Fragment IDs:** Fragment IDs are stable, unambiguous identifiers for rules. The **reference form** is `<module>.pN` (e.g. `security.p1`, `ontology.p5`), where `module` is the canonical module key and `N` is the rule index. Rules within a module are ordered; renumbering or removing published indices is a breaking change. Implementations that use an alternate encoding (e.g. URIs, UUIDs) MUST provide a stable bijection to this reference form for interoperability. Fragment IDs are **immutable** once published; even when a rule is deprecated it remains addressable by its original `<module>.pN` identifier, and deprecation is done via documentation or higher-precedence rules, not removal or renumbering.
- **Path-based namespacing:** Subdirectories under the pattern tree MAY be reflected in the module key (e.g. `domain.api_design` for a file under `patterns/domain/`). This allows domain or organizational namespacing without forking the protocol.
- **Extensibility:** New modules are added by introducing a stable key in the pattern map and, if relevant, in the precedence hierarchy. Community or organizational pattern packs use distinct module keys and do not alter the core primitive set.

---

## 7. Round-Trip Verification Model

Round-trip verification provides evidence that the implemented system aligns with the specified intent. Canonical and derived specs **MUST** follow the schema defined in the FITPAC spec schema (see References) for round-trip diff alignment.

1. **Canonical spec:** A structured specification produced from human input (e.g. prose via a Socratic process). It uses the FITPAC spec schema (entities, constraints/invariants, boundaries, authorities, goals, evidence, and optionally a design summary).
2. **Code:** Implementation produced by a coding agent from the canonical spec.
3. **Derived spec:** A specification **extracted** from the code using the **same schema** as the canonical spec. Extraction only; no comparison in this step.
4. **Comparison:** The canonical and derived specs are compared. The comparison report MUST include:
   - Identifiers of the specs compared.
   - **Additions (not in spec):** every element present in the derived spec but not in the canonical spec (with id, location, description, suggested action). This section MUST appear even if empty.
   - Other differences, classified by impact. At least three levels are distinguished: **cosmetic**, **behavioral**, and **contractual** (e.g. signature changes, boundary shifts, invariant weakening/strengthening). Implementations MAY add finer categories or subclasses provided contractual (boundary/semantic) impact remains distinguishable and the Additions section is always present.

Convergence (normative content aligned, no unspecced additions) is reported as an iteration report; divergence is reported as a diff report. Contractual differences typically block or route to human decision. FITPAC does not define where or how specs and reports are stored; that is implementation-defined.

---

## 8. Spec Ambiguity Protocol

When the specification is ambiguous, multiple valid implementation paths exist, or confidence drops below a defined threshold, the agent MUST NOT silently guess. The following protocol is mandatory for conformant coding agents:

1. **Confidence model:** Implementations MUST define a confidence model comprising a baseline value and a consult threshold. When confidence is at or below the consult threshold, the agent MUST enter a consultation mode (informative name: "Reference Mode") and consult the pattern library before proceeding. *Example (informative):* baseline 0.95, consult threshold 0.90; drop conditions such as unknown domain term, failed test, security risk, or spec ambiguity reduce confidence by defined deltas.
2. **Condition-to-fragment mapping:** When a condition is detected (e.g. spec ambiguity, multiple valid paths, security risk), the agent MUST consult a deterministic mapping from that condition to a minimal set of pattern fragments (or equivalent rules), load only that set, apply it, and record the consultation. The mapping is defined by the implementation (typically via `master_index.yaml` or an equivalent manifest as defined in RFC‑0004 Section 2.1); its format and location are implementation-defined.
3. **Minimal loading:** The agent MUST load **only** the mapped pattern fragments (not entire files unless the mapping so specifies), apply the decision logic from those fragments, and record the consultation. Audit log reasoning MUST be in human-readable form for auditability and MUST, at minimum, capture: the trigger condition(s) observed, fragment IDs consulted, the chosen resolution, a brief justification for why alternatives were rejected when applicable, and links or references to evidentiary artifacts when those inform the decision. The protocol does not prescribe a specific natural language or format—implementations define what "human-readable" means (e.g. locale, structure).
4. **Escalation:** If the situation remains unresolved after consultation, the agent MUST escalate with an event that conveys either (a) **ambiguity detected** (refuse, explain, or defer) or (b) a **proposed resolution** for human approval. Event names and payloads are implementation- or profile-defined; these semantics are normative. Decisions with consequences MUST be attributed to human authority or to an explicit rule from the pattern library.
5. **Audit:** Every consultation event MUST be recorded in an audit log with at least: inflection point, trigger, fragment (or rule) loaded, resolution applied, confidence before/after, and a reasoning field that satisfies the minimum semantic payload described above. Implementations MAY include additional fields. Reasoning in the audit log MUST be human-readable as defined by the implementation.

This protocol ensures that ambiguity is surfaced and resolved by rule or by human, not by silent invention.

---

## 9. Non-Goals

- FITPAC does not define a concrete syntax for specs (Markdown, YAML, or other representations are permitted).
- FITPAC does not define orchestration, storage, or CI integration; those are implementation-defined.
- FITPAC does not mandate a specific LLM or agent stack; it defines the protocol and ontology that any conformant implementation must respect.
- FITPAC does not replace testing or formal verification; it provides a structured intent layer and verification of spec–code alignment.

---

## 10. Security Considerations

- **Authority and capability:** The Authority and Capability primitives support explicit modeling of who may do what. Conformant implementations should enforce policy checks and delegation depth limits as specified in the pattern library (e.g. security, governance patterns).
- **Containment and provenance:** Speculation or model-inferred content that affects state or decisions should have provenance; agents should refuse or defer when required by containment patterns (e.g. SourceRequiredClaim).
- **Audit trail:** The consultation protocol and audit log produce a durable record of why decisions were made. This supports accountability and regulatory requirements but may expose sensitive reasoning; implementors should define retention and access policy for audit logs.
- **Supply chain:** Pattern and spec sources (master index, pattern files) should be integrity-protected; trust in the index and patterns is assumed by the consultation protocol.

---

## 11. References

The RFC references normative documents that define the primitive spine, spec schema, master index (or equivalent) semantics, governance, and pattern index. The paths below are for the reference distribution; implementations MAY organize or package these documents differently provided the normative content is preserved and references remain resolvable.

- FITPAC Primitive Spine: `00_primitive_spine.md` (version 1.0.0)
- FITPAC Spec Schema: `docs/reference/spec-schema.md`
- FITPAC Master Index Reference: `docs/reference/master-index.md`
- FITPAC Governance and Versioning: `docs/reference/governance-versioning.md`
- FITPAC Pattern Index: `docs/reference/pattern-index.md`
- FITPAC Manifesto (informative): `docs/manifesto.md`
- RFC-0002: FITPAC Profile Specification (profiles, schema, compliance)
- [RFC 2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC 8174] Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words

For FITPAC 1.0.0, the normative versions of these references are those identified by the version-locking mechanism described in Section 5 (for example, in `fitpac_manifest.yaml`).

---

## 12. Conformance

A system is **FITPAC-conformant** if and only if it satisfies all of the following:

1. **Primitives and grammar:** It accepts and produces specs that use the defined Layer 1 and Layer 2 primitives and the four control grammar semantics (obligations, operational rules, outputs, non-normative commentary). It does not redefine the core primitives. Implementations MAY use alternate labels that map 1:1 to these semantics.
2. **Stable identifiers:** It preserves and uses stable module keys and fragment IDs in the reference form `<module>.pN` or an equivalent encoding with a stable bijection to that form; it does not rename or renumber published identifiers.
3. **Ambiguity protocol:** It implements the spec ambiguity protocol: a confidence model with baseline and consult threshold, a deterministic condition-to-fragment mapping, minimal fragment loading, escalation with semantics of ambiguity-detected or proposal when unresolved (event names implementation- or profile-defined), and an audit log with human-readable reasoning for each consultation.
4. **Spec schema:** It produces and consumes canonical and derived specs that conform to the FITPAC spec schema (see References).
5. **Round-trip comparison:** It produces a comparison report for canonical vs derived specs that includes spec identifiers, an **Additions (not in spec)** section (present even if empty), and classification of other differences (at least cosmetic, behavioral, and contractual; finer categories MAY be added).
6. **Precedence:** When multiple patterns conflict, the system MUST resolve ties using a deterministic, documented value hierarchy. Individual implementers MAY define custom hierarchies for specific domains or use cases. The **Standard FITPAC Profile** (see below) requires that the hierarchy satisfy the principle in Section 4. Implementations whose hierarchy does not satisfy that principle SHOULD disclose this in the audit log.

**Standard FITPAC Profile.** In addition to the six requirements above, an implementation satisfies the **Standard FITPAC Profile** if and only if its precedence hierarchy ensures that constraints protecting safety, integrity, or regulatory compliance outrank constraints that optimize only for convenience, performance, or resource budgets (see Section 4). This profile is the reference for auditability and regulatory alignment. Implementations that use a different hierarchy MAY still be FITPAC-conformant but MUST NOT claim Standard Profile compliance unless they meet this requirement.

Implementations that satisfy all six requirements may be described as **FITPAC-conformant**. Implementations that also satisfy the Standard FITPAC Profile may be described as **FITPAC-conformant (Standard Profile)** or equivalent. This RFC is part of the FITPAC 1.0.0 standard.

---

### 12.1 Conformance Inputs for FITPAC 1.0.0

For clarity, this section summarizes the inputs that a serious implementer MUST or SHOULD use when claiming conformance to FITPAC 1.0.0.

**Required RFCs (core protocol stack):**

- RFC‑0001: FITPAC 1.0.0 — Formal Intent Translation Protocol for Agentic Code.
- RFC‑0002: FITPAC Profile Specification.
- RFC‑0003: FITPAC Primitive and Spec Schema Reference.
- RFC‑0004: FITPAC Master Index and Consultation Semantics.
- RFC‑0005: FITPAC Pattern and Trigger Grammar.

**Required normative references (all conformant systems):**

- Primitive spine: `00_primitive_spine.md`.
- Spec schema: `docs/reference/spec-schema.md`.

**Additional required inputs for spec→code coding agents:**

- Master index reference: `docs/reference/master-index.md`.
- Master index configuration: `master_index.yaml` (or equivalent manifest as defined in RFC‑0004).
- Pattern index: `docs/reference/pattern-index.md`.
- Trigger taxonomy: `docs/reference/trigger-taxonomy.md`.
- Pattern modules: `patterns/*.md`.

**Version pinning:**

- For FITPAC 1.0.0, implementations **MUST** tie these inputs to a specific, version-locked set of normative references using the mechanism in Section 5 (for example, a `fitpac_manifest.yaml` that records versions or hashes). Profiles MAY introduce additional required inputs but MUST NOT remove or weaken any of the requirements above.

---

## 13. Profiles and Extensibility

FITPAC is designed to support domain-specific constraints and governance requirements through **Profiles**. Profiles allow serious practitioners and regulators to further constrain the protocol without forking it.

### 13.1 Definition

A **FITPAC Profile** is a formal, machine-readable configuration that constrains the base protocol for a specific domain (e.g. healthcare, nuclear safety, fintech). Profiles add rules and tighten constraints; they do not redefine the core.

### 13.2 What Profiles May Do

Profiles MAY:

- Tighten confidence thresholds (e.g. higher baseline, stricter consult threshold).
- Mandate specific pattern modules or forbid certain patterns or fallbacks.
- Define custom precedence hierarchies for the domain.
- Require specific audit behavior (e.g. retention, external review).
- Add domain-specific ambiguity triggers and condition-to-fragment mappings.

### 13.3 What Profiles Must Not Do

Profiles MUST NOT:

- Redefine Layer 1 or Layer 2 primitives.
- Alter the semantics of the control grammar (REQUIRE, RULE, EMIT, NOTE).
- Remove or weaken mandatory protocol requirements (ambiguity protocol, round-trip verification, stable identifiers, deterministic precedence).
- Change the semantic meaning of the control vocabulary.

**Golden rule:** Profiles tighten; they do not loosen.

### 13.4 Reference

The schema, compliance criteria, and governance for FITPAC Profiles are specified in **RFC-0002: FITPAC Profile Specification**. The default configuration for general use (e.g. the 30-pattern reference set and Standard Reference Hierarchy) is the **FITPAC Reference Profile**, which is also defined there.
