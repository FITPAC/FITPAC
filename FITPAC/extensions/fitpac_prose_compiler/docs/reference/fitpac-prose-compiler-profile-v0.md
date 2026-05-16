# Compiler profile `fitpac.prose_compiler.compiler_profile_v0`

Source: [`fitpac_prose_compiler/profiles/fitpac.prose_compiler.compiler_profile_v0.yaml`](fitpac_prose_compiler/profiles/fitpac.prose_compiler.compiler_profile_v0.yaml)

This is a **fitpac.prose_compiler compiler profile** (RFC-0006 §5). It is **not** a FITPAC Profile per RFC-0002.

| Knob | Value | Effect |
|------|-------|--------|
| `clause_confidence_min` | `0.65` | Emit `resolution_artifact` when clause confidence falls below this threshold. |
| `allow_partial_spine_emission` | `false` | Partial binding outcomes cannot imply spine-ready nodes without explicit draft flags. |
| `allow_auto_refines_edges` | `false` | `refines` is not auto-emittable as a committed edge unless enabled. |
| `auto_emittable_edge_kinds` | `exception_to`, `conditional_on`, `evidenced_by` | Only these kinds may appear with `committed: true` on edges (unless `refines` is allow-listed). |
| `require_dag` | `false` | Cycle detection for codegen is optional at v0. |

Validators enforce edge tiering and partial policy using the selected profile file.
