# Changelog

All notable changes to the FITPAC reference distribution are documented here.

## [1.1.0] — 2026-05-16

### Added

- **Namespaced extension `fitpac.prose_compiler`** (RFC-0006): additive pack under `FITPAC/extensions/fitpac_prose_compiler/` for a reject-first **prose → clause → obligation → normalization → binding → primitive graph → resolution** pipeline.
- Extension registration in `FITPAC/fitpac_manifest.yaml` (`extensions:`), `FITPAC/extensions/extension_registry.yaml`, and `FITPAC/master_index.yaml` (module key `fitpac.prose_compiler`, precedence **31**, fragments `fitpac.prose_compiler.p1`–`p6`).
- Normative references: [RFC-0006](rfcs/RFC-0006-FITPAC-prose-compiler-extension.md), [extension registry](FITPAC/docs/reference/extension-registry.md), and pack manifest `fitpac_prose_compiler_manifest.yaml` (SHA-256 pinned artifacts).
- Tooling: `FITPAC/tools/fitpac_prose_compiler_context.py`, `fitpac_prose_compiler_validate` (CLI + pytest), and CI workflow [`.github/workflows/fitpac-conformance.yml`](.github/workflows/fitpac-conformance.yml).

### Notes

- Core FITPAC 1.0.0 pattern modules (30 canonical modules), primitive spine, and RFC-0001–0005 semantics are unchanged; the extension is optional for hosts that only need prose→spec→code.
- RFC-0006 remains **Proposed** for community review; the pack is shipped in this distribution for implementer testing.

## [1.0.0] — 2026-03-19

- Initial public release of the FITPAC 1.0.0 reference distribution (RFCs, normative references, and reference orchestrators).
