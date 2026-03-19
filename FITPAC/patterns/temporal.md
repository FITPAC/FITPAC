# Temporal & Concurrency (Compressed)
# ID: temporal
# Module key (for fragment IDs): `temporal` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Boundaries own contract shape; temporal owns idempotency/lease semantics.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Idempotency
```yaml
triggers: [retry_instability, concurrent_conflict, implicit_constraints_omitted]
requires_primitives: [Entity, Authority, Time, Boundary]
output_type: constraint
domain: core
category: boundary
```

- Primitives: IdempotencyKey.
- Invariants: Same key applied twice → at most one observable effect (temporal.inv.1).
- Triggers: retry_instability, concurrent_conflict.
- RULE: Extract or mint IdempotencyKey from request (e.g. job+resource, request_id). Check store; if key seen and success recorded, return prior result. Else execute, store result under key.
- Failure: Duplicate effect = invariant violation. Use boundaries.p2 (T2.Conflict) if key collision.

## p2: Deadline
```yaml
triggers: [deadline_missed]
requires_primitives: [Entity, Authority, Time, Boundary]
output_type: constraint
domain: core
category: boundary
```

- Primitives: Deadline.
- Triggers: deadline_missed.
- RULE: Propagate deadline from contract or caller. Before each external call, check remaining time. If exceeded, abort; return timeout (boundaries.p2 T3.Timeout).
- Invariants: No commit after deadline expiry.

## p3: Saga
```yaml
triggers: []
requires_primitives: [Entity, Authority, Time, Boundary]
output_type: constraint
domain: core
category: boundary
```

- Primitives: Saga (steps + compensations).
- Invariants: All steps commit OR compensations restore prior state (temporal.inv.3).
- RULE: Define steps and compensations. On step failure, run compensations reverse order. Do not commit saga outcome until all committed or compensated.

## p4: Lease
```yaml
triggers: [concurrent_conflict]
requires_primitives: [Entity, Authority, Time, Boundary]
output_type: constraint
domain: core
category: boundary
```

- Primitives: Lease (holder, resource, TTL).
- Invariants: Only lease holder may commit leased resource until expiry (temporal.inv.2).
- Triggers: concurrent_conflict.
- RULE: Acquire lease with TTL before mutating resource. Reject mutation if lease missing or expired. Release or extend on completion.

## p5: Transaction Boundary
```yaml
triggers: [retry_instability, transaction_boundary_uncertain]
requires_primitives: [Entity, Authority, Time, Boundary]
output_type: constraint
domain: core
category: boundary
```

- Invariants: No external I/O inside transaction (no network, no cross-boundary call within transaction scope).
- RULE: Declare exactly-once vs at-least-once semantics per operation; use dedupe tokens or transactional outbox for exactly-once. Split transactions so external I/O is outside commit boundary.
- Triggers: transaction_boundary_uncertain, retry_instability.

## p6: Time Source Contract
```yaml
triggers: [clock_time_misuse]
requires_primitives: [Entity, Authority, Time, Boundary]
output_type: constraint
domain: core
category: boundary
```

- Primitives: TimeSource (UTC, monotonic_clock, allowed_skew).
- RULE: Use UTC for timestamps across boundaries; use monotonic clock for local ordering/duration where needed. Document allowed skew; do not compare time across services without sync.
- Triggers: clock_time_misuse, spec_ambiguity.

## p7: Bounded Concurrency and Must-Close
```yaml
triggers: [resource_leak_risk]
requires_primitives: [Entity, Authority, Time, Boundary]
output_type: constraint
domain: core
category: boundary
```

- Invariants: Bounded concurrency (max in-flight, pool size); resources MUST be closed or released (streams, cursors, handles, goroutines/tasks).
- RULE: Declare concurrency cap per operation; use structured concurrency (supervision, explicit lifecycle). No unbounded spawn; no fire-and-forget without supervision.
- Triggers: resource_leak_risk, concurrent_conflict.
