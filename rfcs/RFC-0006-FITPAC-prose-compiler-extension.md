---
RFC: 0006
Title: FITPAC `fitpac.prose_compiler` additive extension
Author: Paul Roy
Status: Proposed
Version: 0.2.0
Date: 2026-05-16
Depends-on:
  - RFC-0001
  - RFC-0002
  - RFC-0003
  - RFC-0004
  - RFC-0005
Supersedes: None
license: CC-BY-4.0
license_url: https://creativecommons.org/licenses/by/4.0/
copyright_holder: Paul Roy and FITPAC Contributors
attribution_note: Attribution required under CC BY 4.0.
adoption_status: proposed
standard_inclusion: extension-pack
---

# RFC-0006: FITPAC `fitpac.prose_compiler` additive extension

## 1. Abstract

This document specifies the **fitpac.prose_compiler** extension: schemas, inventories, binding contracts, primitive graphs, and resolution artifacts for a **reject-first** pipeline from natural-language clauses to spine-referenced primitives. The extension is additive to FITPAC 1.0.0 and **MUST NOT** redefine Layer 1/Layer 2 primitives or control grammar semantics.

## 2. Motivation

Natural-language specifications under-determine obligations. Extract-then-classify pipelines emit speculative primitives. This extension requires **parse obligation structure first**, **normalize to inventory ids**, **bind or reject**, then emit **graph-ready** primitives with explicit edges or **resolution artifacts**.

## 3. Namespace and pack root

- Logical types use the prefix **`fitpac.prose_compiler:*`**.
- JSON Schemas live under `FITPAC/extensions/fitpac_prose_compiler/docs/reference/fitpac_prose_compiler/schema/`.
- The **pack root** is `FITPAC/extensions/fitpac_prose_compiler/`.
- Version pinning uses `FITPAC/extensions/fitpac_prose_compiler/fitpac_prose_compiler_manifest.yaml`, registered from the repository root `fitpac_manifest.yaml` `extensions:` list.

## 4. Normative authority

1. JSON Schemas are the **source of truth** for field names and closed enums.
2. Versioned YAML inventories under `docs/reference/fitpac_prose_compiler/data/<version>/` are the **sole authority** for binding-relevant sense/actor/kind ids.
3. `binding/binding_contract_v0.yaml` declares slot requirements per **ontology primitive id** (opaque string referencing the pinned classification ontology).
4. `fitpac_prose_compiler_manifest.yaml` pins SHA-256 for every normative file in the pack.
5. Pattern module `FITPAC/extensions/fitpac_prose_compiler/patterns/fitpac_prose_compiler.md` (**MUST** follow RFC-0005 `## pN` + YAML metadata). If pattern prose conflicts with schema, implementations **MUST** follow schema.

## 5. Compiler profiles (not RFC-0002 FITPAC Profiles)

**fitpac.prose_compiler compiler profiles** (e.g. `fitpac.prose_compiler.compiler_profile_v0`) configure clause confidence thresholds, partial spine emission, and the **auto-emittable committed edge** set. They are **not** FITPAC Profiles per RFC-0002 and **MUST NOT** be loaded as RFC-0002 profile documents. They **MUST NOT** introduce new spine primitive ids; they only constrain extension emission.

## 6. Master index integration (RFC-0004)

Implementations that support the extension **MUST** treat the following as registered in `FITPAC/master_index.yaml`:

| Field | Entry |
|-------|--------|
| `pattern_map.fitpac.prose_compiler` | `extensions/fitpac_prose_compiler/patterns/fitpac_prose_compiler.md` |
| `precedence_hierarchy` | Module key `fitpac.prose_compiler` at ordinal **31** (lowest in reference distribution; does not outrank security or ontology) |
| `ambiguity_triggers` | `fitpac_prose_compiler_low_clause_confidence` → `fitpac.prose_compiler.p1`; `fitpac_prose_compiler_binding_rejected` → `fitpac.prose_compiler.p4`; `fitpac_prose_compiler_open_resolution` → `fitpac.prose_compiler.p6` |

Namespaced triggers are documented in `FITPAC/docs/reference/trigger-taxonomy.md` §4.1.

Machine-readable registration for tooling: `FITPAC/extensions/extension_registry.yaml` (merged by `generate_master_index.py`; see `FITPAC/docs/reference/extension-registry.md`).

## 6.1 Prose→primitives consumer contract

Third-party **prose-primitive** processes that embed FITPAC **MUST**:

1. Load repository-root `fitpac_manifest.yaml` and resolve `extensions[]` where `id == fitpac.prose_compiler`.
2. Load `FITPAC/master_index.yaml` and resolve `pattern_map.fitpac.prose_compiler` to the pattern module path (relative to `FITPAC/`).
3. Load pattern fragments **`fitpac.prose_compiler.p1` through `fitpac.prose_compiler.p6`** on demand (RFC-0005 fragment-on-demand).
4. Load normative JSON Schemas and inventories from the extension pack manifest (`fitpac_prose_compiler_manifest.yaml`).
5. Use compiler profile id **`fitpac.prose_compiler.compiler_profile_v0`** unless a domain-specific successor profile is documented in the extension pack.

Optional helper: `python3 FITPAC/tools/fitpac_prose_compiler_context.py` prints resolved paths and fragment ids for the active pack version.

## 7. Registration in `fitpac_manifest.yaml`

The repository root manifest **MUST** include an `extensions:` entry:

```yaml
extensions:
  - id: fitpac.prose_compiler
    semver: 0.2.0
    manifest: FITPAC/extensions/fitpac_prose_compiler/fitpac_prose_compiler_manifest.yaml
    sha256: <hash of extension manifest bytes>
```

RFC-0006 is pinned under `normative_references.rfcs` alongside RFC-0001–0005.

## 8. Pipeline stages (informative summary)

| Stage | Artifact | Pattern fragment |
|-------|----------|------------------|
| 1 | `fitpac.prose_compiler:clause` | `fitpac.prose_compiler.p1` |
| 2 | `fitpac.prose_compiler:obligation_frame` | `fitpac.prose_compiler.p2` |
| 2.5 | `fitpac.prose_compiler:normalized_obligation` | `fitpac.prose_compiler.p3` (normalization) |
| 3 | `fitpac.prose_compiler:binding_outcome` | `fitpac.prose_compiler.p4` |
| 4 | `fitpac.prose_compiler:primitive_graph` | `fitpac.prose_compiler.p5` |
| 5 | `fitpac.prose_compiler:resolution_artifact` | `fitpac.prose_compiler.p6` |

Stage numbering in schemas uses normalization as 2.5; pattern `p3` covers normalization, `p4` binding (see pattern module).

## 9. Determinism and LLM stages

Stages 1–2 **MAY** use LLMs; **validated JSON** is the contract surface. Reproducibility claims **MUST** include pinned pack hashes, inventory versions, binding contract version, and model metadata recorded by the orchestrator (out of band for this RFC).

## 10. Downstream consumers

A `primitive_graph` with `compiler_grade_ready: true` is the input to later **c_spec** / codegen stages (RFC-0003 control grammar). This RFC does not define graph→`c_spec` translation; that remains a separate consumer.

## 11. Security and governance

Resolution artifacts may contain sensitive prose snippets; treat graphs as **policy-bearing data**. Implementations **SHOULD** redact secrets at span capture time.

## 12. Migration

Minor semver bumps **MAY** extend enums and inventories with backward-compatible additions. Major bumps **MAY** rename fields with explicit migration notes in the extension `CHANGELOG.md`.
