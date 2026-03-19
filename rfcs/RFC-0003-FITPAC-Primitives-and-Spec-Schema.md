---
RFC: 0003
Title: FITPAC Primitive and Spec Schema Reference
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

# RFC-0003: FITPAC Primitive and Spec Schema Reference

## 1. Scope

This document consolidates the **primitive ontology** and the **spec schema** for FITPAC. RFC-0001 defines primitives and spec behavior at a high level and normatively references:

- `FITPAC/00_primitive_spine.md` (primitive set and core semantics), and
- `FITPAC/docs/reference/spec-schema.md` (canonical and derived spec schema, comparison rules, and control grammar).

This RFC makes those dependencies explicit, defines which parts are normative for conformance, and describes how they evolve.

---

## 2. Primitive Spine (Normative Summary)

The **primitive spine** is defined normatively by `FITPAC/00_primitive_spine.md` (a normative reference implementing this section). A FITPAC-conformant implementation:

- **MUST** treat the following as the complete set of Layer 1 primitives:
  - Entity, Transformation, Constraint, Authority, Relation, Context, Time.
- **MUST** treat the following as Layer 2 **structural primitives** built from Layer 1:
  - Transaction, Boundary, Projection, Capability, Policy.
- **MUST NOT** introduce new Layer 1 primitives or redefine the semantics of the existing ones.
- **MAY** define domain-specific aliases or composite concepts, provided they can be expressed purely in terms of the primitive spine and do not alter its semantics.

The file `FITPAC/00_primitive_spine.md` is the **canonical, versioned artifact** for the primitive spine. Changes that:

- rename a primitive,
- change the meaning of a primitive, or
- introduce or remove a Layer 1 primitive

are **breaking changes** to the FITPAC core and **MUST** be reflected as a major version bump to the FITPAC standard.

In case of discrepancy between this summary and RFC‑0001, RFC‑0001 is authoritative for primitive definitions; `FITPAC/00_primitive_spine.md` is authoritative for canonical phrasing and extended semantics.

---

## 3. Spec Schema (Canonical and Derived Specs)

The logical schema for FITPAC specs is defined in `FITPAC/docs/reference/spec-schema.md`, which is a **normative reference implementing this section**.

Implementations:

- **MUST** represent both **Canonical** and **Derived** specs using a schema that is compatible with the structure described in `spec-schema.md` (entities and ontology, constraints and invariants, authorities and policies, boundaries and transactions, temporal behavior, goals and acceptance, evidence and scenarios).
- **MUST** produce comparison reports that:
  - identify the specs being compared,
  - include an **Additions (not in spec)** section (present even if empty), and
  - classify other differences at least as cosmetic vs behavioral vs contractual.
- **MUST NOT** redefine the semantics of the control grammar (REQUIRE, RULE, EMIT, NOTE) when interpreting or generating spec documents.

The exact concrete representation (Markdown sections, YAML frontmatter, JSON, etc.) is implementation-defined, but the **logical content and semantics** described in `spec-schema.md` are normative.

In case of discrepancy between this summary and RFC‑0001, RFC‑0001 is authoritative for protocol-level behavior; `FITPAC/docs/reference/spec-schema.md` is authoritative for the detailed schema structure.

---

## 4. Control Grammar

The control grammar in `spec-schema.md` (section 6) defines the **closed set of semantic labels** for structured spec content:

- REQUIRE, RULE, EMIT, NOTE.

Implementations:

- **MUST** treat these four labels as the complete control vocabulary for execution and comparison semantics.
- **MAY** support additional headings for readability, but such headings **MUST** be treated as comments that do not alter the semantics of the underlying primitives or control flow.

Pattern rule bodies in `FITPAC/patterns/*.md` **MAY** use these labels or express their semantics in free-form prose; `spec-schema.md` and `pattern-index.md` together define the normative interpretation of these bodies.

---

## 5. Versioning and Evolution

The primitive spine and spec schema are versioned as independent, semantic-versioned components that are intended to be compatible with specific FITPAC core versions. Compatible combinations are fixed for a given distribution and pinned via the manifest described in RFC‑0001 Section 5:

- Changes that **add new optional sections** or fields to the spec schema, without altering existing semantics, are **minor** or **patch** changes and **MUST NOT** break existing conformant implementations.
- Changes that **remove or rename** primitives or spec sections, or alter their meaning, are **major** changes and **MUST** be accompanied by a core version bump.

Implementations:

- **SHOULD** record which version of the primitive spine and spec schema they target (for example, by tracking the FITPAC core version and associated manifest entry).
- **MAY** support multiple schema versions concurrently, but comparisons and conformance checks **MUST** be performed against a single, well-defined version at a time (as identified in the manifest for that run).

For the spec schema specifically:

- Unknown or additional fields in spec documents **MUST** be ignored for protocol-level processing but **SHOULD** be preserved on round-trip where technically feasible.
- New required fields or sections **MUST NOT** be introduced without a corresponding major version bump of the core/spec schema.
- New optional fields or sections MAY be added in minor or patch versions, provided existing semantics are not altered.
- Removal or renaming of existing fields or sections is considered a breaking change and therefore requires a major version bump.

---

## 6. Normative References

The following files are normative references for this RFC:

- `FITPAC/00_primitive_spine.md` — canonical primitive spine and core semantics.
- `FITPAC/docs/reference/spec-schema.md` — spec schema (Canonical and Derived), comparison rules, and control grammar.

If these files are moved or renamed in a distribution, equivalent artifacts **MUST** be provided and clearly associated with this RFC for the distribution to remain FITPAC-conformant. For FITPAC 1.0.0, the normative versions of these files are those identified by the version-locking mechanism described in RFC-0001 Section 5 (for example, in `fitpac_manifest.yaml`).

