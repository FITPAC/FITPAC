# Data Persistence & Storage (Compressed)
# ID: persistence
# Module key (for fragment IDs): `data_persistence` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Security governs access control; temporal governs transactions; this governs storage semantics and consistency.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Storage Type Selection
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: persistence
category: other
```

- Primitives: StorageType (relational, document, key_value, graph, time_series, blob), SelectionCriteria.
- Invariants: StorageType MUST be explicitly declared with justification (data_persistence.inv.1).
- Triggers: storage_type_mismatch, performance_degradation.
- RULE: Declare StorageType based on: access patterns (read/write ratio), consistency needs, query complexity, scale requirements. Document selection rationale. Changing StorageType requires migration plan (schema_evolve.p4).

## p2: Consistency Model Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: persistence
category: other
```

- Primitives: ConsistencyModel (strong, eventual, causal, read_your_writes), ConsistencyScope.
- Invariants: Operations MUST NOT assume stronger consistency than declared (data_persistence.inv.2).
- Triggers: consistency_violation, stale_read.
- RULE: Declare ConsistencyModel per data store and per operation type. Strong consistency for financial transactions, eventual for analytics. Document staleness bounds for eventual consistency.

## p3: Query Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: persistence
category: other
```

- Primitives: QueryPattern (lookup, scan, aggregate, join), QueryBudget (max_rows, max_time).
- Invariants: Queries MUST have declared QueryBudget; unbounded queries forbidden (data_persistence.inv.3).
- Triggers: query_timeout, resource_exhaustion.
- RULE: Every query type declares expected QueryPattern and QueryBudget. Use parameterized queries only (security.p1). Queries exceeding budget return partial results with continuation token or fail with budget_exceeded.

## p4: Index Strategy
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: persistence
category: other
```

- Primitives: Index (columns, type, purpose), IndexInvariant.
- Triggers: slow_query, missing_index.
- RULE: Declare indexes required for each QueryPattern. Document read vs write tradeoff. Index changes require migration plan. Monitor index usage; remove unused indexes.

## p5: Caching Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: persistence
category: other
```

- Primitives: CacheLayer (local, distributed, CDN), CachePolicy (TTL, invalidation_strategy), CacheKey.
- Invariants: Cached data MUST NOT violate ConsistencyModel (data_persistence.inv.4).
- Triggers: cache_inconsistency, cache_miss_storm.
- RULE: Declare CacheLayer and CachePolicy per data type. Invalidation strategies: TTL, event-driven, write-through, write-behind. For strong consistency, use write-through or no cache. Document cache-aside patterns explicitly.

## p6: Cache Invalidation
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: persistence
category: other
```

- Primitives: InvalidationEvent, InvalidationScope (key, pattern, all).
- Invariants: On data mutation, relevant caches MUST be invalidated within declared window (data_persistence.inv.5).
- Triggers: stale_cache, cache_inconsistency.
- RULE: Map mutations to InvalidationEvents. Define InvalidationScope (narrow preferred). For distributed caches, account for propagation delay. Use versioned cache keys for atomic updates.

## p7: Sharding and Partitioning
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: persistence
category: other
```

- Primitives: PartitionKey, PartitionStrategy (hash, range, geographic), ShardMap.
- Invariants: Cross-partition transactions MUST be explicitly declared and minimized (data_persistence.inv.6).
- Triggers: hot_partition, cross_shard_query.
- RULE: Declare PartitionKey selection criteria. Avoid monotonic keys for hash partitioning. Document cross-partition query patterns. Use saga (temporal.p3) for cross-partition transactions.

## p8: Data Lifecycle
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: persistence
category: other
```

- Primitives: RetentionPolicy (duration, archive_tier, deletion_strategy), DataLifecycleState.
- Invariants: Data past RetentionPolicy MUST be archived or deleted per policy (data_persistence.inv.7).
- Triggers: retention_exceeded, storage_quota.
- RULE: Declare RetentionPolicy per data type. Implement automated lifecycle transitions. Legal holds override retention deletion. Coordinate with compliance (compliance_audit.p2).

## p9: Backup and Recovery
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: persistence
category: other
```

- Primitives: BackupSchedule, RecoveryPointObjective (RPO), RecoveryTimeObjective (RTO).
- Invariants: Backup frequency MUST satisfy RPO; recovery process MUST satisfy RTO (data_persistence.inv.8).
- Triggers: backup_failed, recovery_needed.
- RULE: Declare RPO and RTO per data store. Implement backup schedule meeting RPO. Test recovery procedures regularly. Document point-in-time recovery capabilities.

## p10: Data Integrity Constraints
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: persistence
category: other
```

- Primitives: IntegrityConstraint (unique, foreign_key, check, custom), ConstraintEnforcement (database, application, both).
- Invariants: Declared constraints MUST be enforced at specified layer (data_persistence.inv.9).
- Triggers: constraint_violation, data_corruption.
- RULE: Declare IntegrityConstraints in spec. Prefer database enforcement for critical constraints. Application-layer for cross-store constraints. Test constraint enforcement in evidence_harness.
