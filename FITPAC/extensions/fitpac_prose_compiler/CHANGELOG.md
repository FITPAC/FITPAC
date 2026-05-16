# Changelog — FITPAC `fitpac.prose_compiler` pack

This pack is the normative home for extension id **`fitpac.prose_compiler`**: JSON Schemas, inventories, binding contracts, compiler profiles, pattern fragments, and validators. It is registered in the repository-root `FITPAC/fitpac_manifest.yaml` and merged into `FITPAC/master_index.yaml` by `FITPAC/tools/generate_master_index.py`.

## 0.2.0 — 2026-05-16

- **Namespaced extension id** `fitpac.prose_compiler` (module key, triggers `fitpac.prose_compiler:*`, ambiguity keys `fitpac_prose_compiler_*`).
- Pack root `FITPAC/extensions/fitpac_prose_compiler/`; manifest `fitpac_prose_compiler_manifest.yaml` (semver **0.2.0**).
- Pattern module `patterns/fitpac_prose_compiler.md` with fragments **p1**–**p6**; compiler profile **`fitpac.prose_compiler.compiler_profile_v0`**.
- Python package **`fitpac_prose_compiler_validate`**; path helper `FITPAC/tools/fitpac_prose_compiler_context.py`.
- Normative RFC: [`RFC-0006-FITPAC-prose-compiler-extension.md`](../../../rfcs/RFC-0006-FITPAC-prose-compiler-extension.md).

## 0.1.1 — 2026-05-16

- Integrated into the FITPAC reference distribution; RFC-0006 promoted to repository `rfcs/`.
- Registered in `master_index.yaml`, `extension_registry.yaml`, and core `fitpac_manifest.yaml` `extensions:` list.
- Pinned classification ontology JSON; expanded binding contract; CI conformance workflow.

## 0.1.0 — 2026-05-15

- Initial pack: JSON Schemas (clause through primitive graph), v0.1.0 inventories, binding contract subset, reference compiler profile, validators, pytest fixtures, pattern stubs.
