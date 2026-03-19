# Deployment & Release (Compressed)
# ID: deployment
# Module key (for fragment IDs): `deployment` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Governance governs approval; resilience governs rollback; this governs deployment mechanics and release safety.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Deployment Strategy Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: deployment
category: other
```

- Primitives: DeploymentStrategy (rolling, blue_green, canary, recreate), DeploymentConfig.
- Invariants: DeploymentStrategy MUST be declared per service (deployment.inv.1).
- Triggers: deployment_strategy_undefined, deployment_failed.
- RULE: Declare DeploymentStrategy based on: downtime tolerance, rollback speed, resource cost. Rolling: gradual replacement. Blue-green: instant switch. Canary: progressive traffic shift. Recreate: full stop-start (only for stateful with exclusive access).

## p2: Health Check Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: deployment
category: other
```

- Primitives: HealthCheck (type, endpoint, interval, threshold), HealthStatus (healthy, degraded, unhealthy).
- Invariants: Instances MUST pass HealthCheck before receiving traffic (deployment.inv.2).
- Triggers: health_check_failed, instance_unhealthy.
- RULE: Define HealthCheck types: Liveness (process alive), Readiness (can serve traffic), Startup (initialization complete). Configure intervals and failure thresholds. Unhealthy instances removed from load balancer. Document health check dependencies.

## p3: Graceful Shutdown
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: deployment
category: other
```

- Primitives: ShutdownSignal, DrainPeriod, ShutdownHook.
- Invariants: Instance MUST complete in-flight requests before termination (deployment.inv.3).
- Triggers: shutdown_signal_received, drain_timeout.
- RULE: On ShutdownSignal: stop accepting new requests, complete in-flight requests within DrainPeriod, execute ShutdownHooks (close connections, flush buffers), then terminate. If DrainPeriod exceeded, force terminate and log incomplete requests.

## p4: Canary Analysis
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: deployment
category: other
```

- Primitives: CanaryMetrics (error_rate, latency, custom), CanaryThreshold, CanaryVerdict (promote, rollback, pause).
- Invariants: Canary promotion requires CanaryMetrics within CanaryThreshold (deployment.inv.4).
- Triggers: canary_degradation, canary_threshold_exceeded.
- RULE: Route percentage of traffic to canary. Collect CanaryMetrics. Compare to baseline (current production). If metrics degrade beyond threshold, automatic rollback. Manual approval for promotion or configure auto-promote after observation window.

## p5: Rollback Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: deployment
category: other
```

- Primitives: RollbackTrigger (manual, automatic), RollbackTarget (previous_version, known_good), RollbackTime.
- Invariants: Rollback MUST restore previous working state within RollbackTime (deployment.inv.5).
- Triggers: deployment_failed, post_deploy_degradation.
- RULE: Define RollbackTrigger conditions (error rate spike, health check failures). Maintain RollbackTarget (previous artifact, database state if applicable). Test rollback procedure. Rollback MUST NOT require forward-only migrations. Use resilience.p3 for rollback execution.

## p6: Environment Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: deployment
category: other
```

- Primitives: Environment (dev, staging, prod), EnvironmentConfig, EnvironmentInvariant.
- Invariants: Production config MUST NOT leak to non-production; vice versa (deployment.inv.6).
- Triggers: config_leak, environment_mismatch.
- RULE: Define Environment tiers with isolation. Staging mirrors production (data shape, scale factor). Environment-specific secrets MUST NOT be shared. Document EnvironmentInvariants (e.g., prod has monitoring, staging allows debug endpoints).

## p7: Artifact Provenance
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: deployment
category: other
```

- Primitives: Artifact (version, hash, build_source), BuildAttestation, ArtifactRegistry.
- Invariants: Only attested Artifacts from ArtifactRegistry may deploy to production (deployment.inv.7).
- Triggers: unattested_artifact, provenance_missing.
- RULE: Build pipeline produces Artifact with hash and BuildAttestation (source commit, builder identity, timestamp). Store in ArtifactRegistry. Deployment verifies attestation before proceeding. Extends containment.p2 for code artifacts.

## p8: Feature Flag Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: deployment
category: other
```

- Primitives: FeatureFlag (name, state, rollout_percentage, targeting), FlagLifecycle (active, deprecated, removed).
- Invariants: Deprecated flags MUST be removed within FlagLifecycle window (deployment.inv.8).
- Triggers: stale_flag, flag_conflict.
- RULE: Use FeatureFlags for gradual rollout, A/B testing, kill switches. Define targeting rules (user segment, region). Track flag dependencies. Deprecated flags trigger removal reminder. Remove dead code paths when flag removed.

## p9: Database Migration Safety
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: deployment
category: other
```

- Primitives: Migration (version, up, down, reversible), MigrationLock, MigrationState.
- Invariants: Migrations MUST be backward compatible during rollout window (deployment.inv.9).
- Triggers: migration_failed, migration_lock_timeout.
- RULE: Migrations follow expand-contract (schema_evolve.p4). No breaking changes until old code fully retired. Acquire MigrationLock before execution. Test migration and rollback in staging. Long-running migrations use online DDL or background jobs.

## p10: Deployment Window
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: deployment
category: other
```

- Primitives: DeploymentWindow (allowed_times, blackout_periods), ChangeFreeze.
- Invariants: Production deployments MUST occur within DeploymentWindow unless emergency (deployment.inv.10).
- Triggers: deployment_outside_window, change_freeze_violation.
- RULE: Define DeploymentWindow based on traffic patterns, support availability. ChangeFreeze during critical periods (holidays, major events). Emergency deployments require governance.p2 Override with audit trail.

## p11: Progressive Delivery
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: deployment
category: other
```

- Primitives: DeliveryStage (internal, beta, GA), StageGate (criteria, approver).
- Triggers: stage_gate_failed, premature_promotion.
- RULE: Define DeliveryStages with increasing exposure. Internal: team only. Beta: opt-in users. GA: all users. Each stage has StageGate criteria (quality metrics, feedback threshold). Promotion requires gate passage or explicit override.
