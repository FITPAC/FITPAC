# Messaging & Event Systems (Compressed)
# ID: messaging
# Module key (for fragment IDs): `messaging` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Temporal governs idempotency; boundaries governs contracts; this governs message delivery and event semantics.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Delivery Guarantee Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: messaging
category: other
```

- Primitives: DeliveryGuarantee (at_most_once, at_least_once, exactly_once), AckMode.
- Invariants: System MUST NOT claim stronger guarantee than implemented (messaging.inv.1).
- Triggers: message_lost, duplicate_delivery.
- RULE: Declare DeliveryGuarantee per message type. At-most-once: fire and forget. At-least-once: ack after processing, use IdempotencyKey (temporal.p1). Exactly-once: transactional outbox + dedupe. Document failure modes for each.

## p2: Message Schema Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: messaging
category: other
```

- Primitives: MessageSchema (version, fields, required, optional), SchemaRegistry.
- Invariants: Messages MUST validate against declared schema (messaging.inv.2).
- Triggers: schema_validation_failed, unknown_message_type.
- RULE: Register MessageSchema in SchemaRegistry. Producers validate before send. Consumers validate on receive. Use schema_evolve.p3 for compatibility rules. Unknown fields: ignore (forward compatibility) or reject (strict mode).

## p3: Topic and Partition Semantics
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: messaging
category: other
```

- Primitives: Topic (name, partition_count, retention), PartitionKey, ConsumerGroup.
- Invariants: Messages with same PartitionKey MUST be delivered in order within partition (messaging.inv.3).
- Triggers: ordering_violation, partition_rebalance.
- RULE: Declare Topic configuration. Choose PartitionKey for ordering guarantees (e.g., entity_id). Document ConsumerGroup semantics. Partition count changes require careful migration.

## p4: Backpressure Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: messaging
category: other
```

- Primitives: BackpressureStrategy (drop, buffer, throttle, reject), BufferLimit.
- Invariants: When BufferLimit exceeded, BackpressureStrategy MUST activate (messaging.inv.4).
- Triggers: buffer_overflow, producer_blocked.
- RULE: Declare BackpressureStrategy per producer and consumer. Drop: lose messages (at-most-once only). Buffer: bounded queue with spill policy. Throttle: slow producer. Reject: return error to producer.

## p5: Dead Letter Queue
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: messaging
category: other
```

- Primitives: DeadLetterQueue (DLQ), DLQPolicy (max_retries, ttl, alert_threshold).
- Invariants: Messages failing after max_retries MUST route to DLQ (messaging.inv.5).
- Triggers: message_processing_failed, dlq_threshold_exceeded.
- RULE: Configure DLQ per topic/queue. Define max_retries with exponential backoff. Messages in DLQ require manual triage or automated remediation. Alert when DLQ depth exceeds threshold.

## p6: Event Sourcing Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: messaging
category: other
```

- Primitives: EventStore, EventStream (aggregate_id), Projection, Snapshot.
- Invariants: EventStore is append-only; events immutable (messaging.inv.6).
- Triggers: event_replay_needed, projection_lag.
- RULE: If using event sourcing: events are source of truth. Projections derived from events. Snapshots for replay optimization. Define projection update semantics (sync, async, eventual). Version events per schema_evolve.p1.

## p7: Pub/Sub Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: messaging
category: other
```

- Primitives: Publisher, Subscriber, Subscription (filter, delivery_mode).
- Triggers: subscriber_lag, fanout_overhead.
- RULE: Declare Subscription semantics: push vs pull, filter criteria, delivery_mode (broadcast, competing consumers). Publishers MUST NOT assume subscriber presence. Subscribers handle redelivery.

## p8: Message Ordering
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: messaging
category: other
```

- Primitives: OrderingGuarantee (none, partition, global, causal), OrderingKey.
- Invariants: Stronger ordering increases latency and reduces throughput (messaging.inv.7).
- Triggers: ordering_violation, out_of_order_processing.
- RULE: Declare OrderingGuarantee per message type. None: best effort. Partition: ordered within OrderingKey. Global: total order (rare, expensive). Causal: happens-before preserved. Document tradeoffs.

## p9: Transactional Outbox
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: messaging
category: other
```

- Primitives: Outbox (table), OutboxRelay, DedupeStore.
- Invariants: Message publishing MUST be atomic with business transaction (messaging.inv.8).
- Triggers: orphan_message, transaction_message_mismatch.
- RULE: For exactly-once with external systems: write message to Outbox in same transaction as state change. OutboxRelay polls and publishes. DedupeStore prevents consumer duplicates. Use with temporal.p5.

## p10: Consumer Lag Monitoring
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: messaging
category: other
```

- Primitives: ConsumerLag (offset_diff, time_diff), LagThreshold.
- Triggers: consumer_lag_exceeded, processing_backlog.
- RULE: Monitor ConsumerLag per ConsumerGroup. Alert when exceeding LagThreshold. Lag indicates: slow consumer, consumer failure, or burst. Auto-scale consumers or investigate root cause.
