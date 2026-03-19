# Boundary Contracts (Compressed)
# ID: boundaries
# Module key (for fragment IDs): `boundaries` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Temporal governs idempotency; resilience governs recovery; this governs boundary contracts and error taxonomy.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Contractual Boundary
```yaml
triggers: [missing_boundary_manifest]
requires_primitives: [Entity, Authority, Time, Boundary]
output_type: constraint
domain: core
category: boundary
```

- REQUIRE: `contract.yaml` (Structural, Operational, Temporal, Resiliency).

## p2: Global Error Taxonomy
```yaml
triggers: [retry_instability]
requires_primitives: [Entity, Authority, Time, Boundary]
output_type: constraint
domain: core
category: boundary
```

- T1: Actionable (Transient, Terminal, Critical).
- T2: Attribution (InvalidInput, Unauthorized, Conflict, DependencyUnavailable).
- T3: Semantic (NotFound, Timeout).

## p3: Retry Budget and Side-Effect Ledger
```yaml
triggers: [retry_instability]
requires_primitives: [Entity, Authority, Time, Boundary]
output_type: constraint
cross_refs: [temporal.p1]
domain: core
category: boundary
```

- RULE: Explicit retry budget (max attempts, backoff); idempotency key required for operations that can repeat (temporal.p1). Optionally: side-effect ledger per operation to detect duplicate application.
- Triggers: retry_instability. Prevents retries without idempotency contracts.

## p4: Temporal Containment
```yaml
triggers: [retry_instability, deadline_missed]
requires_primitives: [Entity, Authority, Time, Boundary]
output_type: constraint
domain: core
category: boundary
```

- REQUIRE: Deadline propagation.
- REQUIRE: Pre/Post side-effect cancellation checks.

## p5: Partial Failure Policy
```yaml
triggers: [partial_failure]
requires_primitives: [Entity, Authority, Time, Boundary]
output_type: constraint
domain: core
category: boundary
```

- MODES: fail-closed | fail-open | degrade.
- REQUIRE: Result annotation for missing sub-components.
