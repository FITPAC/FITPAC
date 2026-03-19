# Performance & Scalability (Compressed)
# ID: performance
# Module key (for fragment IDs): `performance` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Budgets governs tradeoffs; boundaries governs contracts; this governs SLOs, measurement, and scaling.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: SLO Contract
```yaml
triggers: [slo_breach, error_budget_exhausted]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: performance
category: other
```

- Primitives: SLO (metric, target, window), SLI (actual measurement), ErrorBudget.
- Invariants: SLI MUST be measured and compared to SLO continuously (performance.inv.1).
- Triggers: slo_breach, error_budget_exhausted.
- RULE: Define SLOs for critical user journeys. Common SLOs: availability (99.9%), latency (p99 < 200ms), error rate (< 0.1%). Measure SLI. ErrorBudget = allowed failures per window. When budget exhausted, freeze non-essential changes.

## p2: Latency Budget
```yaml
triggers: [latency_budget_exceeded, component_slow]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: performance
category: other
```

- Primitives: LatencyBudget (total, per_component), LatencyBreakdown.
- Invariants: Sum of component budgets MUST NOT exceed total LatencyBudget (performance.inv.2).
- Triggers: latency_budget_exceeded, component_slow.
- RULE: Allocate LatencyBudget across call chain. Track LatencyBreakdown per request. Alert when component exceeds budget. Use for capacity planning. Extends budgets.p1 with detailed allocation.

## p3: Latency Percentiles
```yaml
triggers: [tail_latency_spike, percentile_breach]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: performance
category: other
```

- Primitives: LatencyPercentile (p50, p90, p99, p999), LatencyDistribution.
- Invariants: SLO MUST specify percentile, not just average (performance.inv.3).
- Triggers: tail_latency_spike, percentile_breach.
- RULE: Measure and report percentiles. p50 = median, p99 = worst 1%. Tail latency (p99, p999) often 10x median. Optimize for percentiles, not averages. Alert on percentile breaches, not average.

## p4: Throughput Contract
```yaml
triggers: [throughput_degradation, capacity_limit_reached]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: performance
category: other
```

- Primitives: ThroughputTarget (requests_per_second, transactions_per_second), ThroughputLimit.
- Invariants: System MUST handle ThroughputTarget under normal conditions (performance.inv.4).
- Triggers: throughput_degradation, capacity_limit_reached.
- RULE: Define ThroughputTarget per endpoint. Load test to verify. Set ThroughputLimit (rate limiting) to prevent overload. Document scaling behavior: linear, sub-linear, or capacity cliff.

## p5: Resource Budget
```yaml
triggers: [resource_exhaustion, memory_pressure, cpu_throttling]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: performance
category: other
```

- Primitives: ResourceBudget (cpu, memory, disk, network, connections), ResourceUtilization.
- Invariants: ResourceUtilization MUST NOT exceed ResourceBudget thresholds (performance.inv.5).
- Triggers: resource_exhaustion, memory_pressure, cpu_throttling.
- RULE: Define ResourceBudget per service. Monitor ResourceUtilization. Set thresholds (e.g., 70% CPU triggers alert, 90% triggers scale). Memory: set limits, handle OOM gracefully. Connections: pool with limits.

## p6: Auto-Scaling Contract
```yaml
triggers: [scale_out_triggered, scale_in_triggered, scaling_failed]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: performance
category: other
```

- Primitives: ScalingPolicy (metric, threshold, cooldown, min, max), ScalingAction (scale_out, scale_in).
- Invariants: Scaling MUST respect min/max bounds (performance.inv.6).
- Triggers: scale_out_triggered, scale_in_triggered, scaling_failed.
- RULE: Define ScalingPolicy: trigger metric (CPU, queue depth, custom), threshold, cooldown between actions. Test scaling behavior. Document scaling latency. Ensure stateless design or handle state during scaling.

## p7: Capacity Planning
```yaml
triggers: [capacity_warning, growth_unexpected]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: performance
category: other
```

- Primitives: CapacityModel (current, projected, headroom), GrowthRate, CapacityReview.
- Triggers: capacity_warning, growth_unexpected.
- RULE: Model current capacity and utilization. Project based on GrowthRate. Maintain headroom (e.g., 30% buffer). Regular CapacityReview (monthly/quarterly). Plan scaling ahead of demand. Document capacity assumptions.

## p8: Load Shedding
```yaml
triggers: [overload_detected, shedding_activated]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: performance
category: other
```

- Primitives: LoadSheddingPolicy (threshold, priority, action), RequestPriority.
- Invariants: Load shedding MUST preserve high-priority requests (performance.inv.7).
- Triggers: overload_detected, shedding_activated.
- RULE: When overloaded, shed low-priority requests to protect high-priority. Define RequestPriority classification. Shedding actions: reject with 503, queue for later, degrade response. Return quickly rather than timeout.

## p9: Caching Strategy
```yaml
triggers: [cache_cold, cache_stampede, low_hit_rate]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: performance
category: other
```

- Primitives: CacheHitRate, CacheMissLatency, CacheWarmup.
- Invariants: Cache MUST NOT serve stale data beyond declared staleness (performance.inv.8).
- Triggers: cache_cold, cache_stampede, low_hit_rate.
- RULE: Target CacheHitRate per cache layer. Measure CacheMissLatency impact. Implement CacheWarmup on deploy. Prevent cache stampede (thundering herd) with locking or probabilistic refresh. Extends `data_persistence.p5`.

## p10: Database Performance
```yaml
triggers: [slow_query, table_scan, index_miss]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: performance
category: other
```

- Primitives: QueryPerformance (plan, cost, execution_time), SlowQueryThreshold, IndexEfficiency.
- Triggers: slow_query, table_scan, index_miss.
- RULE: Monitor QueryPerformance. Alert on queries exceeding SlowQueryThreshold. Analyze query plans. Track IndexEfficiency. Avoid N+1 queries. Use connection pooling. Set query timeouts.

## p11: Performance Testing Contract
```yaml
triggers: [performance_regression, load_test_failed]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: performance
category: other
```

- Primitives: LoadTest (scenario, duration, load_profile), PerformanceBaseline, RegressionThreshold.
- Invariants: Performance regression beyond threshold MUST block deployment (performance.inv.9).
- Triggers: performance_regression, load_test_failed.
- RULE: Establish PerformanceBaseline via LoadTest. Run performance tests in CI/CD. Compare to baseline. Block deployment if regression exceeds RegressionThreshold. Test at expected peak load and beyond.

## p12: Cold Start Optimization
```yaml
triggers: [cold_start_latency, warmup_incomplete]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: performance
category: other
```

- Primitives: ColdStartTime, WarmupPeriod, PrewarmingStrategy.
- Triggers: cold_start_latency, warmup_incomplete.
- RULE: Measure ColdStartTime for serverless/container deployments. Define acceptable WarmupPeriod. Implement PrewarmingStrategy: keep-alive pings, pre-provisioned capacity, lazy vs eager initialization. Don't route traffic until warmed.
