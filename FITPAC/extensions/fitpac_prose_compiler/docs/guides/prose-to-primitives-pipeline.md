# Prose → primitives graph — operator runbook

Part of the **`fitpac.prose_compiler`** namespaced extension (RFC-0006). For registry fields and discovery, see [Extension registry](../../../../docs/reference/extension-registry.md) or run `python3 FITPAC/tools/fitpac_prose_compiler_context.py --json` from the repository root.

## Inputs

- Source document reference (`doc_ref`) and extracted spans with structural context.
- Active extension pack root (`FITPAC/extensions/fitpac_prose_compiler/`) and manifest-pinned inventory version (`v0.1.0`).
- Compiler profile id: `fitpac.prose_compiler.compiler_profile_v0`.

## Artifact chain

1. Emit `clause` JSON per span (Stage 1).
2. For gated clauses, emit `obligation_frame` records (Stage 2).
3. Resolve slots to inventory ids → `normalized_obligation` with `normalization_status` (Stage 2.5).
4. Run static binding contract → `binding_outcome` (Stage 3).
5. Assemble `primitive_graph` with nodes/edges and optional embedded `normalized_obligations` / `binding_outcomes` (Stage 4).
6. Queue `resolution_artifact` for every non-silent rejection (Stage 5).

## Validation

```bash
python3 FITPAC/extensions/fitpac_prose_compiler/tools/validate_artifact.py graph \
  --pack FITPAC/extensions/fitpac_prose_compiler \
  --document path/to/graph.json
```

Exit `0` only when JSON Schema validation and extension rules pass.

## Failure modes (telemetry)

Use stable `failure_mode` strings (examples): `low_confidence_clause`, `unknown_action_sense`, `scope_ambiguous`, `wrong_actor`, `object_out_of_scope`, `condition_unparseable`.

## Compiler-grade export

Set `compiler_grade_ready: true` on a graph **only** when:

- JSON validates.
- No `resolution_artifact` with `resolution_status: open` remains for the exported slice.
- No spine node marks `compiler_grade_ready: false` while the graph claims ready.

LLM-backed stages SHOULD record model id/version in run metadata outside this pack when claiming reproducibility.
