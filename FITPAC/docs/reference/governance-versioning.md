---
title: Governance, versioning, and conformance
status: normative-reference
implements: RFC-0001
license: CC-BY-4.0
license_url: https://creativecommons.org/licenses/by/4.0/
copyright_holder: Paul Roy and FITPAC Contributors
attribution_note: Attribution required under CC BY 4.0.
---

# Governance, versioning, and conformance

This document defines how the FITPAC language, pattern library, and spec schema are versioned and evolved, and what it means for an implementation to be FITPAC‑conformant.

## 1. Versioning surfaces

Version numbers apply independently to:

- **Language core** — the primitive spine and control grammar:
  - e.g. `Language v1.0.0`.
- **Core pattern modules** — semantic versions per module:
  - e.g. `security v1.0.0`, `ontology v1.0.0`, `boundaries v1.0.0`.
- **Spec schema** — the Canonical/Derived spec schema:
  - e.g. `SpecSchema v1.0.0`.

Normative reference version pinning (identifier, version, content hash) is defined by RFC-0001 Section 5 and is typically recorded in a distribution manifest (e.g. `fitpac_manifest.yaml`). Runtime configuration (pattern map, precedence, confidence model) lives in `master_index.yaml`. Documentation and tooling SHOULD reference both as appropriate.

### 1.1 Version number semantics

FITPAC uses **semantic versioning** in the form **major.minor.patch** (e.g. `1.0.0`):

- **Major (1.x.x → 2.x.x):** Breaking change to the language or core. Examples: changes to the primitive spine or control grammar, removal or renaming of module keys in the pattern library, renumbering of existing rules, or fundamental changes to the spec schema. Implementations may need significant updates to remain conformant.
- **Minor (x.1.x → x.2.x):** Additive or backward-compatible change to a surface. Examples: new pattern modules or rules (`pN+1`), new triggers or taxonomy entries, new optional schema fields. Existing conformant implementations continue to work; new behavior is opt-in or additive.
- **Patch (x.x.1 → x.x.2):** Non-semantic change. Examples: typographical fixes, documentation-only updates, clarifications that do not alter requirements or identifiers. No impact on conformance or tooling.

When in doubt, prefer the smallest bump that accurately describes the change.

### 1.2 Compatibility rules

- **Additive changes** (backwards compatible):
  - Adding new pattern modules or rules (`pN+1`).
  - Adding new triggers or namespaced taxonomy entries.
  - Adding new optional fields to schemas.
- **Breaking changes**:
  - Renaming or removing module keys in `pattern_map`.
  - Renumbering existing rules (`pN`).
  - Changing the meaning of existing triggers or invariant IDs.
  - Removing or fundamentally changing spec schema sections.

Breaking changes MUST be treated as new major versions (e.g. `v2.0.0`) and SHOULD go through the governance process below.

## 2. Governance model

Evolving the language and core library follows a lightweight proposal process:

1. **Proposal document**
   - Describes the change (new primitives, grammar tweaks, new core modules, deprecations).
   - Classifies the change as additive or breaking.
   - Lists affected modules, invariants, and tooling.
2. **Review**
   - Core maintainers review for coherence with the primitive spine and control grammar.
   - Implementors of major tools/agents are invited to comment on impact.
3. **Staged rollout**
   - Additive changes MAY be merged behind clear version markers and release notes.
   - Potentially breaking changes SHOULD:
     - be introduced in parallel with the old surface (e.g. mark old rules as deprecated),
     - specify migration guidance, and
     - define a deprecation period.
4. **Deprecation and removal**
   - Deprecated rules and modules remain addressable by their original IDs.
   - New rules or modules carry the updated behavior.

Surfaces expected to remain stable for years:

- primitive spine (`00_primitive_spine.md`),
- control grammar (`REQUIRE`, `RULE`, `EMIT`, `NOTE`),
- spec schema sections (`entities`, `invariants`, `boundaries`, `goals`, etc.).

Faster‑moving surfaces:

- additional pattern modules and rules,
- profiles,
- derived indexing strategies.

## 3. Conformance

This section describes **language and surface conformance**; the full protocol conformance criteria are defined in RFC‑0001 §12 (FITPAC 1.0.0) and, for Profiles, RFC‑0002 §11.

An implementation is **FITPAC‑conformant with respect to the language core and reference library** if it:

1. **Understands the language core**
   - Correctly interprets the primitives and structural primitives from `00_primitive_spine.md`.
   - Respects the control grammar for pattern/spec sections as defined in `docs/reference/spec-schema.md`.
2. **Uses pattern metadata and taxonomy correctly**
   - Parses and applies pattern metadata fields (`id`, `triggers`, `requires_primitives`, `output_type`, `domain`, `category`, optional `produces`, `cross_refs`) as defined in `docs/reference/pattern-index.md`.
   - Uses the trigger taxonomy in `docs/reference/trigger-taxonomy.md` for retrieval and matching.
3. **Produces and consumes Canonical and Derived specs**
   - Can emit Canonical specs from prose using the spec schema.
   - Can extract Derived specs from code using the same schema.
   - Can compare Canonical vs Derived specs and produce a report with at least:
     - spec identifiers,
     - an **Additions (not in spec)** section,
     - classification of other differences as cosmetic, behavioral, or contractual.
4. **Respects identifiers and stability guarantees**
   - Treats module keys, fragment IDs, and invariant IDs as stable within a given version.
   - Does not synthesize new stable IDs without going through the governance process.

Implementations that also satisfy the conformance criteria in RFC‑0001 §12 and RFC‑0002 §11 MAY describe themselves as **FITPAC‑conformant** (and, where applicable, **FITPAC‑conformant (Standard Profile)**).

## 4. Conformance suite (outline)

The FITPAC conformance suite outline is guidance for distributions that choose to publish a runnable, automated conformance harness (including canonical test vectors and expected comparison outcomes).

The FITPAC 1.0.0 reference distribution in this repo primarily ships normative references and reference orchestrators; it does not, by itself, ship an executable conformance harness or canonical suite artifacts. As a result, the outline below is **not a requirement** for this distribution—only a specification of what a full runnable suite SHOULD include when provided.

When a distribution provides an executable conformance suite, the suite SHOULD include:

- A small set of representative pattern modules and specs:
  - security‑focused backend,
  - consumer web app,
  - ML‑heavy system.
- For each:
  - Canonical specs,
  - reference implementations (code),
  - reference Derived specs,
  - expected comparison reports.

An implementation passes the suite if, for each case, it:

- Produces Derived specs that are structurally equivalent to the reference, and
- Produces comparison reports whose **semantic classifications** (additions, behavioral vs contractual changes) match the reference, up to allowed formatting differences.

