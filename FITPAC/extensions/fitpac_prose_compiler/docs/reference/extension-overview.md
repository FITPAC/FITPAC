# `fitpac.prose_compiler` extension overview

This directory tree is an **additive** extension aligned with RFC-0001 (core invariants) and RFC-0002 (profiles tighten only). It introduces the `fitpac.prose_compiler` namespace for a **compiler-shaped** path from natural-language clauses to **inventory-backed** normalized obligations, static binding contracts, **typed primitive graphs**, and **first-class resolution artifacts**.

## Stages

1. **Clause typing** — closed `clause_role` enum; gate `normative_rule` / `schema_description` into compilation.
2. **Obligation frames** — minimal deontic units with hard completeness rules before bind.
3. **Normalization** — binding slots are **IDs from pinned inventories**, not free-text authority.
4. **Binding** — static contract per ontology primitive id; strict `bound` / `rejected` / `partial` semantics.
5. **Primitive graph** — directed edges with **committed** vs **suggested** tiering (profile-driven auto kinds).
6. **Resolution** — every rejection/low-confidence path yields traceable artifacts.

## Normative vs narrative

- **Normative:** JSON Schemas, inventories, binding tables, compiler profiles, manifest hashes ([`fitpac_prose_compiler_manifest.yaml`](../../fitpac_prose_compiler_manifest.yaml)).
- **Narrative:** `patterns/*.md` procedures MUST align with schemas; where they differ, **schemas win**.

## Tooling

See pack [README.md](../../README.md) for validation CLI and pytest location.
