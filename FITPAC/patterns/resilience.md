# Resilience & Recovery (Compressed)
# ID: resilience
# Module key (for fragment IDs): `resilience` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Boundaries own partial-failure policy (p6); resilience owns circuit and recovery.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Circuit Breaker
```yaml
triggers: [circuit_open, resource_leak_risk]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- Primitives: CircuitState (closed, open, half_open).
- Invariants: When open, no new calls to protected dependency (resilience.inv.1).
- Triggers: circuit_open, retry_instability.
- RULE: Track failures per dependency. On threshold set state open. Reject new calls with circuit_open. After cooldown try half_open; on success close. Log state transitions.

## p2: Reconciliation
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- Primitives: ReconciliationRun, target invariants.
- Invariants: ReconciliationRun MUST restore invariants or escalate (resilience.inv.2).
- Triggers: partial_failure.
- RULE: Define target invariants. Periodically or on trigger run: read state, compare to target, apply corrective actions. If cannot restore escalate (alert, manual).

## p3: Rollback
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- Primitives: RollbackPlan (steps to undo).
- RULE: For reversible ops maintain RollbackPlan. On failure after commit execute rollback reverse order. If rollback fails escalate.
