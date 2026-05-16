# Changelog — FITPAC `fitpac.prose_compiler` pack

## 0.2.0 — 2026-05-16

- **Breaking:** extension id and module key renamed from `fitpac.prose` to `fitpac.prose_compiler`.
- Pack directory `FITPAC/extensions/fitpac_prose_compiler/`; manifest `fitpac_prose_compiler_manifest.yaml`.
- Compiler profile id `fitpac.prose_compiler.compiler_profile_v0`; Python package `fitpac_prose_compiler_validate`.
- RFC filename: `RFC-0006-FITPAC-prose-compiler-extension.md`.

## 0.1.0 — 2026-05-15

- Initial extension pack: JSON Schemas (clause, obligation frame, normalized obligation, binding outcome, resolution artifact, primitive graph), v0 inventories, binding contract subset, reference profile, validators + CLI, pytest conformance fixtures, pattern stubs, additive RFC.

## 0.1.1 — 2026-05-16

- Integrated under `FITPAC/extensions/fitpac_prose_compiler/`; RFC-0006 promoted to repository `rfcs/` (v0.1.1).
- RFC-0005 pattern module `fitpac.prose_compiler.p1`–`p6`; registered in `master_index.yaml` and `extension_registry.yaml`.
- Compiler profile renamed to `fitpac.prose_compiler.compiler_profile_v0` (distinct from RFC-0002 profiles).
- Pinned classification ontology JSON; expanded binding contract primitives; pinned `patterns/fitpac_prose_compiler.md`.
- `FITPAC/tools/fitpac_prose_compiler_context.py` for third-party path resolution; CI workflow; `generate_master_index.py` merges extensions.
