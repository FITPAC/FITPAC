# FITPAC `fitpac.prose_compiler` extension pack

Additive extension: **prose → clause → obligation → normalization → binding → primitive graph → resolution artifacts** (RFC-0006).

Normative RFC: [`../../rfcs/RFC-0006-FITPAC-prose-compiler-extension.md`](../../rfcs/RFC-0006-FITPAC-prose-compiler-extension.md).

## Layout

| Path | Contents |
|------|-----------|
| `docs/reference/fitpac_prose_compiler/` | JSON Schemas, inventories, binding contract, compiler profile |
| `patterns/fitpac_prose_compiler.md` | RFC-0005 pattern module (`fitpac.prose_compiler.p1`–`p6`) |
| `tools/` | Validators, CLI, conformance tests |

Core FITPAC (`FITPAC/patterns/`, spine, RFC-0001–0005) is **not** modified by this pack.

## Quickstart

From repository root (install deps: `jsonschema`, `PyYAML`, `pytest`):

```bash
# Resolve paths for prose→primitives consumers (RFC-0006 §6.1)
python3 FITPAC/tools/fitpac_prose_compiler_context.py
python3 FITPAC/tools/fitpac_prose_compiler_context.py --json

pip install -e FITPAC/extensions/fitpac_prose_compiler  # optional; or PYTHONPATH=FITPAC/extensions/fitpac_prose_compiler/tools

python3 FITPAC/extensions/fitpac_prose_compiler/tools/validate_artifact.py graph \
  --pack FITPAC/extensions/fitpac_prose_compiler \
  --document FITPAC/extensions/fitpac_prose_compiler/tools/tests/fixtures/valid_minimal_graph.json

pytest FITPAC/extensions/fitpac_prose_compiler/tools/tests -q

python3 FITPAC/tools/verify_manifest_hashes.py
```

## Manifest

[`fitpac_prose_compiler_manifest.yaml`](fitpac_prose_compiler_manifest.yaml) — pinned artifact SHA-256 hashes.
