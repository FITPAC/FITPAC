---
title: FITPAC extension registry
status: normative-reference
implements: RFC-0006
license: CC-BY-4.0
---

# FITPAC extension registry

Extensions are **additive packs** registered in repository-root `FITPAC/fitpac_manifest.yaml` under `extensions:` and described in machine-readable form in [`FITPAC/extensions/extension_registry.yaml`](../../extensions/extension_registry.yaml).

The reference distribution (as of 2026-05-16) ships one registered extension: **`fitpac.prose_compiler`** at pack semver **0.2.0** (RFC-0006 status: Proposed).

`FITPAC/tools/generate_master_index.py` **merges** extension `pattern_map`, `precedence_hierarchy`, and `ambiguity_triggers` into [`master_index.yaml`](../../master_index.yaml) so regeneration does not drop extension modules.

## `fitpac.prose_compiler` (prose → primitives)

| Field | Value |
|-------|--------|
| Extension id | `fitpac.prose_compiler` |
| Pack root | `FITPAC/extensions/fitpac_prose_compiler/` |
| Pattern module | `FITPAC/extensions/fitpac_prose_compiler/patterns/fitpac_prose_compiler.md` |
| Module key | `fitpac.prose_compiler` |
| Pipeline fragments | `fitpac.prose_compiler.p1` … `fitpac.prose_compiler.p6` |
| Default compiler profile | `fitpac.prose_compiler.compiler_profile_v0` |
| Normative manifest | `FITPAC/extensions/fitpac_prose_compiler/fitpac_prose_compiler_manifest.yaml` |

### Loading from a host repository

1. Vendor or submodule the FITPAC tree so `FITPAC/fitpac_manifest.yaml` and `FITPAC/master_index.yaml` are available.
2. Resolve paths:

   ```bash
   python3 FITPAC/tools/fitpac_prose_compiler_context.py --json
   ```

3. For each pipeline stage, load the fragment from the pattern module (heading `## pN` + YAML block + body) per [pattern-index.md](pattern-index.md).
4. Validate intermediate JSON against schemas listed in the extension manifest.
