# fitpac.prose_compiler — prose compiler pipeline (RFC-0005 module)
# ID: fitpac.prose_compiler
# Module key (for fragment IDs): `fitpac.prose_compiler` (see `master_index.yaml.pattern_map`)
# Version: 0.2.0
# Status: active
# License: CC-BY-4.0
# Implements: RFC-0006

## p1 : Clause typing (Stage 1)

```yaml
triggers:
  - fitpac.prose_compiler:low_clause_confidence
  - spec_ambiguity
requires_primitives: [Context, Constraint]
output_type: mapping
domain: fitpac.prose_compiler
category: domain
```

Assign every candidate span a **closed** `clause_role` before ontology work begins.

- **Inputs:** span text; structural context (section depth, heading trail, block type, parent block, numbering).
- **Outputs:** `fitpac.prose_compiler:clause` JSON per `clause.schema.json`.
- **MUST:** Roles MUST be one of: `normative_rule`, `schema_description`, `header`, `example`, `rationale`, `document_metadata`, `unknown`.
- **MUST:** Only `normative_rule` and `schema_description` MAY enter obligation parsing without explicit compiler profile override.
- **MUST:** If `unknown` or confidence below `clause_confidence_min`, emit `resolution_artifact` (no silent drop).
- **MAY:** Use prompted LLM with schema validation and few-shot ledger examples.

## p2 : Obligation parsing (Stage 2)

```yaml
triggers:
  - spec_ambiguity
  - fitpac.prose_compiler:open_resolution
requires_primitives: [Constraint, Authority, Transformation]
output_type: mapping
domain: fitpac.prose_compiler
category: domain
```

Decompose gated clauses into **one `obligation_frame` per minimal normative unit**.

- **MUST:** Preserve `split_from_span_ids` when splitting.
- **MUST:** `actor` and `action` MUST be non-null strings for automatic binding; otherwise emit `resolution_artifact`.
- **MUST:** Split incompatible deontics at coordination boundaries; never merge.
- **MUST:** Ambiguous scope/negation → `resolution_artifact` with `failure_mode` such as `scope_ambiguous`.
- **MUST:** Unresolved `anaphora_flags` block binding until resolution or HITL slot fill.
- **Outputs:** `obligation_frame` JSON per `obligation_frame.schema.json`.

## p3 : Normalization (Stage 2.5)

```yaml
triggers:
  - unknown_domain_term
  - fitpac.prose_compiler:binding_rejected
requires_primitives: [Entity, Constraint, Context]
output_type: mapping
domain: fitpac.prose_compiler
category: domain
```

Map language variance to **inventory-backed IDs** so binding is checkable.

- **MUST:** `action_sense_id`, `actor_normalized`, `object_kind` on bind path MUST exist in manifest-pinned inventories.
- **MUST:** Free-text lemmas live only under `non_binding_gloss`.
- **MUST:** If lookup would require guessing, set `normalization_status: unresolved` and open `resolution_artifact`.
- **Outputs:** `normalized_obligation` JSON per `normalized_obligation.schema.json`.

## p4 : Ontology binding (Stage 3)

```yaml
triggers:
  - fitpac.prose_compiler:binding_rejected
  - missing_invariant
requires_primitives: [Constraint, Policy, Authority]
output_type: decision
domain: fitpac.prose_compiler
category: invariant
```

Map normalized frames to **at most one** ontology primitive using the static binding contract.

- **MUST:** Consult `binding/binding_contract_v0.yaml` for slot rules.
- **MUST:** Outcomes are `bound`, `rejected`, or `partial` with telemetry `failure_mode`.
- **MUST:** `rejected` MUST NOT emit spine primitive nodes.
- **MUST:** `partial` sets `partial_flags.compiler_grade_ready: false` and obeys `allow_partial_spine_emission`.
- **Outputs:** `binding_outcome` JSON per `binding_outcome.schema.json`.

## p5 : Primitive graph assembly (Stage 4)

```yaml
triggers:
  - spec_ambiguity
requires_primitives: [Constraint, Relation, Transformation]
output_type: mapping
domain: fitpac.prose_compiler
category: domain
```

Produce a typed, directed graph as the **codegen-oriented** artifact for a slice.

- **MUST:** Every committed edge has non-empty provenance (`span_ids`, `frame_ids`, or `user_resolution_id`).
- **MUST:** Committed edge kinds ⊆ profile `auto_emittable_edge_kinds` (+ optional `refines` when allow-listed).
- **MUST:** Non-auto kinds use `committed: false` or `suggested_edges` on `resolution_artifact`.
- **MUST:** `spine_primitive` nodes MUST NOT set `draft: true`.
- **Outputs:** `primitive_graph` JSON per `primitive_graph.schema.json`.

## p6 : Resolution and HITL (Stage 5)

```yaml
triggers:
  - fitpac.prose_compiler:open_resolution
  - spec_ambiguity
requires_primitives: [Context, Constraint]
output_type: decision
domain: fitpac.prose_compiler
category: domain
produces: SpecAmbiguityDetected
```

Make unresolvedness **first-class**, traceable, and queueable.

- **MUST:** Every rejection from Stages 1–4 yields `resolution_artifact` or explicit draft (non-committing) object.
- **MUST:** Track `resolution_status` (`open` | `deferred` | `resolved`) with optional `resolved_by_ledger_id`.
- **MUST:** Attach `suggested_edges` for candidate links withheld from committed export.
- **MUST:** `compiler_grade_ready: true` only when no open artifacts affect the exported slice and graph validators pass.
