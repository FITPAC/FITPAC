---
title: Indexing and lookup architecture
status: normative-reference
license: CC-BY-4.0
license_url: https://creativecommons.org/licenses/by/4.0/
copyright_holder: Paul Roy and FITPAC Contributors
attribution_note: Attribution required under CC BY 4.0.
---

# Indexing and lookup architecture

This document describes how to index and retrieve FITPAC patterns and invariants at **library scale** (millions of rules), while keeping a small normative surface and leaving implementation details flexible.

## 1. Normative vs derived indexes

This page is a **normative reference** that elaborates the indexing and lookup expectations implied by RFC‑0001 (core protocol) and RFC‑0002 (profiles). It does not introduce new protocol requirements beyond those RFCs; instead, it specifies how to build **derived indexes** that remain faithful to the normative surface.

FITPAC distinguishes between:

- **Normative artifacts**
  - `master_index.yaml` (including `pattern_map`, precedence, and consultation protocol).
  - Pattern files under `patterns/*.md`.
  - Canonical and Derived specs that follow `docs/reference/spec-schema.md`.
- **Derived indexes**
  - Any additional data structures built for fast lookup:
    - inverted indexes over `triggers`, `requires_primitives`, `domain`, `category`,
    - embeddings and vector indexes,
    - caches and materialized views.

Only the normative artifacts are part of the standard. Derived indexes:

- MUST NOT change fragment IDs, module keys, or invariant identifiers.
- MUST be **rebuildable** from the normative surface.

## 2. Recommended key-based retrieval surfaces

Implementations SHOULD support fast lookup on at least:

- `id` — exact fragment ID (`<module>.pN`).
- `triggers` — to support prose→pattern matching.
- `requires_primitives` — to support primitive‑driven querying.
- `domain` and `category` — for coarse filtering and retrieval ordering.
- invariant identifiers (`<module>.inv.N`) — where present.

At scale, these SHOULD provide **O(1)** or **O(log n)** lookup:

- For example, via hash maps keyed by `id`, and sharded inverted indexes for `triggers` and `requires_primitives`.
- Sequential scans of all pattern files SHOULD be reserved for maintenance or debugging, not the hot path of the orchestration loop.

## 3. Geometric growth and sharding

To support millions of rules and many domains:

- **Name and package libraries** in a way that allows:
  - domain‑focused bundles (e.g. `fitpac-core`, `fitpac-ml`, `fitpac-infra`),
  - versioned pattern packs (e.g. `fitpac-core@1.0.0`).
- **Shard derived indexes** along meaningful boundaries:
  - by module key (e.g. `security`, `ontology`, `boundaries`),
  - by profile (e.g. \"high‑trust backend\" bundle),
  - by domain group (e.g. UX vs infra vs ML).

Agents SHOULD:

- Load only the shards they need for the active profile and current query.
- Be prepared to lazy‑load or page in additional shards when a query crosses boundaries (e.g. from `security` into `messaging`).

## 4. Diff and comparison tooling contracts

Comparison and diff tools operate over **normalized representations** of specs and patterns:

- Minimal JSON/YAML representation for a pattern rule:

```yaml
id: security.p1
triggers: [on_write, precondition:authority]
requires_primitives: [Entity, Authority, Constraint]
output_type: constraint
domain: core
category: security
produces: WriteOwnerConstraint
cross_refs: [ontology.p5]
```

- Minimal JSON/YAML representation for a spec section SHOULD follow `docs/reference/spec-schema.md` (entities, invariants, boundaries, etc.) and may attach:
  - references to pattern IDs (`<module>.pN`),
  - references to invariant IDs (`<module>.inv.N`) where available.

Diff tools SHOULD:

- Compare Canonical vs Derived specs using these normalized forms.
- Use invariant IDs and pattern IDs as **anchors** when present, falling back to structured content when not.

Implementations are free to add richer representations (e.g. ASTs, IRs, embeddings), but those are outside the normative contract.

