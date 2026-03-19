# Distributed Systems (Compressed)
# ID: distributed
# Module key (for fragment IDs): `distributed_systems` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Temporal governs concurrency; resilience governs recovery; this governs distributed coordination and consistency.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Consistency Model Selection
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: distributed
category: other
```

- Primitives: ConsistencyLevel (linearizable, sequential, causal, eventual), ConsistencyScope (operation, session, system).
- Invariants: Advertised ConsistencyLevel MUST be guaranteed under declared failure modes (distributed_systems.inv.1).
- Triggers: consistency_violation, split_brain.
- RULE: Declare ConsistencyLevel per operation or data type. Linearizable: strictest, highest latency. Eventual: best availability, requires conflict resolution. Document CAP tradeoff decisions. Different operations may have different levels.

## p2: Consensus Protocol Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: distributed
category: other
```

- Primitives: ConsensusProtocol (raft, paxos, zab, custom), Quorum, LeaderElection.
- Invariants: Consensus decisions MUST survive f failures with 2f+1 nodes (distributed_systems.inv.2).
- Triggers: consensus_timeout, leader_failure, quorum_lost.
- RULE: For coordination requiring agreement (leader election, distributed transactions), use proven ConsensusProtocol. Define Quorum requirements. Handle leader failure with automatic re-election. Document failure scenarios and recovery.

## p3: Partition Handling
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: distributed
category: other
```

- Primitives: PartitionDetection (timeout, heartbeat), PartitionStrategy (stop, continue, heal).
- Invariants: System MUST detect partition within declared timeout (distributed_systems.inv.3).
- Triggers: partition_detected, partition_healed.
- RULE: Implement PartitionDetection via heartbeats or timeout. On partition: Stop (halt operations, preserve consistency), Continue (operate in partition, accept divergence), or Heal (queue operations, reconcile later). Document strategy per component.

## p4: Vector Clocks and Causality
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: distributed
category: other
```

- Primitives: VectorClock, CausalOrder, HappensBefore.
- Triggers: causality_violation, concurrent_update.
- RULE: For causal consistency, attach VectorClock to events. Compare clocks to determine HappensBefore relationship. Concurrent events (neither happens-before) require conflict resolution. Use for eventual consistency systems requiring causal ordering.

## p5: Conflict Resolution
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: distributed
category: other
```

- Primitives: ConflictType (write_write, read_write), ResolutionStrategy (last_writer_wins, merge, custom), ConflictRecord.
- Invariants: Conflicts MUST be resolved deterministically (distributed_systems.inv.4).
- Triggers: conflict_detected, resolution_failed.
- RULE: Define ResolutionStrategy per data type. Last-writer-wins: simple but may lose updates. Merge: CRDT-style automatic merge. Custom: application-specific logic. Log ConflictRecord for debugging. Test conflict scenarios.

## p6: CRDTs (Conflict-free Replicated Data Types)
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: distributed
category: other
```

- Primitives: CRDT (type: counter, set, register, map), MergeFunction.
- Invariants: CRDT merge MUST be commutative, associative, and idempotent (distributed_systems.inv.5).
- Triggers: crdt_merge, replica_sync.
- RULE: For eventually consistent data requiring automatic conflict resolution, use CRDTs. Counter: increment-only or PN-counter. Set: add-wins or remove-wins. Register: LWW or MV-register. Document chosen CRDT type and semantics.

## p7: Distributed Transaction Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: distributed
category: other
```

- Primitives: DistributedTransaction, TwoPhaseCommit (2PC), Saga (temporal.p3), TransactionCoordinator.
- Invariants: All participants MUST commit or all MUST abort (distributed_systems.inv.6).
- Triggers: transaction_timeout, participant_failure, coordinator_failure.
- RULE: For atomic cross-service operations, choose: 2PC (strong consistency, blocking), Saga (eventual consistency, compensating). Define TransactionCoordinator. Handle participant and coordinator failures. 2PC not recommended across service boundaries; prefer Saga.

## p8: Service Discovery
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: distributed
category: other
```

- Primitives: ServiceRegistry, ServiceInstance (address, port, health, metadata), DiscoveryMethod (dns, registry, sidecar).
- Invariants: Stale service instances MUST be removed within TTL (distributed_systems.inv.7).
- Triggers: service_not_found, stale_registration.
- RULE: Register ServiceInstance with health status. Implement health checks. Remove unhealthy instances. Clients discover via DNS, registry lookup, or sidecar proxy. Handle discovery failures gracefully. Cache with appropriate TTL.

## p9: Idempotent Operations
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: distributed
category: other
```

- Primitives: IdempotencyKey (from temporal.p1), IdempotencyStore, IdempotencyWindow.
- Invariants: Same IdempotencyKey applied multiple times produces same result (distributed_systems.inv.8).
- Triggers: duplicate_request, idempotency_expired.
- RULE: All mutating operations SHOULD be idempotent. Extract or generate IdempotencyKey. Check IdempotencyStore before execution. Store result for IdempotencyWindow duration. Return stored result for duplicates. Essential for at-least-once delivery (messaging.p1).

## p10: Shard Coordination
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: distributed
category: other
```

- Primitives: ShardMap (shard_id, range, owner), ShardMigration, RebalanceTrigger.
- Invariants: Each key maps to exactly one shard at any time (distributed_systems.inv.9).
- Triggers: shard_migration, hot_shard, owner_failure.
- RULE: Maintain ShardMap for routing. On rebalance: freeze affected ranges, migrate data, update ShardMap atomically, unfreeze. Handle owner failure with failover. Monitor shard load for hot shard detection.

## p11: Gossip Protocol
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: distributed
category: other
```

- Primitives: GossipMessage (type, payload, version), GossipInterval, ConvergenceTime.
- Triggers: gossip_partition, slow_convergence.
- RULE: For membership, failure detection, or metadata dissemination, use gossip. Nodes periodically exchange state with random peers. Epidemic spread ensures eventual consistency. Tune GossipInterval vs ConvergenceTime tradeoff. Handle network partitions gracefully.

## p12: Clock Synchronization
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: distributed
category: other
```

- Primitives: ClockSource (NTP, PTP, logical), MaxClockSkew, TrueTime.
- Invariants: Operations depending on time MUST account for MaxClockSkew (distributed_systems.inv.10).
- Triggers: clock_skew_exceeded, timestamp_conflict.
- RULE: Use synchronized clocks (NTP/PTP) for timestamps. Document MaxClockSkew tolerance. For ordering across nodes, use logical clocks or wait for uncertainty window (TrueTime approach). Never compare timestamps from different nodes without skew consideration.
