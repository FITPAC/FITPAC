# JSON Schema catalog — `fitpac.prose_compiler`

All machine-normative types live under `docs/reference/fitpac_prose_compiler/schema/`.

| Schema | `$id` suffix | Purpose |
|--------|----------------|---------|
| [common.definitions.json](fitpac_prose_compiler/schema/common.definitions.json) | `common.definitions.json` | Shared enums and `source_span`. |
| [clause.schema.json](fitpac_prose_compiler/schema/clause.schema.json) | `clause.schema.json` | Stage 1 clause typing. |
| [obligation_frame.schema.json](fitpac_prose_compiler/schema/obligation_frame.schema.json) | `obligation_frame.schema.json` | Stage 2 obligation IR. |
| [normalized_obligation.schema.json](fitpac_prose_compiler/schema/normalized_obligation.schema.json) | `normalized_obligation.schema.json` | Stage 2.5 inventory-backed slots. |
| [binding_outcome.schema.json](fitpac_prose_compiler/schema/binding_outcome.schema.json) | `binding_outcome.schema.json` | Stage 3 binding result + telemetry. |
| [suggested_edge.schema.json](fitpac_prose_compiler/schema/suggested_edge.schema.json) | `suggested_edge.schema.json` | Non-committed edge suggestion payload. |
| [resolution_artifact.schema.json](fitpac_prose_compiler/schema/resolution_artifact.schema.json) | `resolution_artifact.schema.json` | Stage 5 unresolvedness queue. |
| [primitive_graph.schema.json](fitpac_prose_compiler/schema/primitive_graph.schema.json) | `primitive_graph.schema.json` | Stage 4 graph export + optional embedded norms/outcomes. |

Validators additionally enforce profile edge tiers, inventory referential integrity, binding contracts, and `compiler_grade_ready` rules (see `tools/fitpac_prose_compiler_validate/`).
