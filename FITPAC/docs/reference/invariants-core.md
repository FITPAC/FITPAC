---
title: Core invariants (library-level overview)
status: informative
---

# Core invariants (library-level overview)

This document is a **non‑normative convenience index** of invariants defined in the core FITPAC pattern library. It lists only invariants that have stable identifiers of the form `X.inv.N` in the published pattern modules under `patterns/`. It is **not exhaustive** and is expected to grow monotonically as new core modules and invariants are added.

- Normative rules for fragment and invariant identifiers are in [pattern-index.md](pattern-index.md) (RFC-0005). **Canonical invariant IDs use the module key from `master_index.yaml.pattern_map`** (e.g. `accessibility.inv.1`, `api_design.inv.1`), not file-header or domain aliases.
- Specs and tools MAY reference these IDs; they are not required to depend on this document.

## Accessibility (`accessibility.inv.*`)

- `accessibility.inv.1` — System MUST meet declared WCAGLevel.
- `accessibility.inv.2` — Non-text content MUST have text alternative.
- `accessibility.inv.3` — Text contrast MUST meet WCAG ratio (4.5:1 normal, 3:1 large).
- `accessibility.inv.4` — All functionality MUST be accessible via keyboard.
- `accessibility.inv.5` — ARIA usage MUST not conflict with native semantics.
- `accessibility.inv.6` — Form fields MUST have associated labels.
- `accessibility.inv.7` — Content MUST NOT flash more than 3 times per second.
- `accessibility.inv.8` — Content MUST be readable at 200% zoom without horizontal scroll.
- `accessibility.inv.9` — Errors MUST be announced and identifiable.

## API design (`api_design.inv.*`)

- `api_design.inv.1` — API style MUST be declared and consistently applied.
- `api_design.inv.2` — Resources MUST have stable, unique identifiers.
- `api_design.inv.3` — Methods MUST adhere to HTTP semantics.
- `api_design.inv.4` — Status codes MUST accurately reflect operation outcome.
- `api_design.inv.5` — Requests MUST validate against schema before processing.
- `api_design.inv.6` — Collection endpoints MUST support pagination.
- `api_design.inv.7` — Filter/sort MUST NOT expose internal fields.
- `api_design.inv.8` — Bulk operations MUST report per-item results.
- `api_design.inv.9` — Breaking changes MUST increment major version.
- `api_design.inv.10` — Rate limits MUST be documented and enforced consistently.
- `api_design.inv.11` — Protected endpoints MUST verify authentication before processing.
- `api_design.inv.12` — Replayed requests with same IdempotencyKey MUST return original response.
- `api_design.inv.13` — Webhook payloads MUST be signed for verification.
- `api_design.inv.14` — API MUST have machine-readable specification.

## Budgets (`budgets.inv.*`)

- `budgets.inv.1` — If LatencyBudget set, response within budget or return timeout.
- `budgets.inv.2` — Agent MUST stop consulting after ConsultDepthLimit; MUST stop iteration after IterationCap.

## Compliance & audit (`compliance_audit.inv.*`)

- `compliance_audit.inv.1` — AuditLog MUST be append-only and tamper-evident.
- `compliance_audit.inv.2` — Data under LegalHold MUST NOT be deleted regardless of RetentionPolicy.
- `compliance_audit.inv.3` — Mutex roles MUST NOT be assigned to same actor.
- `compliance_audit.inv.4` — Production changes MUST have approved ChangeRequest.
- `compliance_audit.inv.5` — Attestation MUST occur per AttestationSchedule.
- `compliance_audit.inv.6` — Access rights MUST be reviewed per AccessReview schedule.
- `compliance_audit.inv.7` — Signed actions MUST be verifiable by any party with public key.

## Configuration (`configuration.inv.*`)

- `configuration.inv.1` — Higher precedence ConfigSource overrides lower.
- `configuration.inv.2` — Configuration MUST validate against ConfigSchema before use.
- `configuration.inv.3` — Secrets MUST NOT appear in plain text in config files, logs, or errors.
- `configuration.inv.4` — Dynamic config changes MUST propagate within declared latency.
- `configuration.inv.5` — ConfigDrift MUST be detected and alerted.
- `configuration.inv.6` — Production secrets MUST NOT exist in non-production configs.
- `configuration.inv.7` — Every config change MUST be versioned with author and timestamp.
- `configuration.inv.8` — Configuration MUST NOT be applied if dependencies unsatisfied.
- `configuration.inv.9` — Sensitive fields MUST be redacted in logs and error messages.

## Data persistence (`data_persistence.inv.*`)

- `data_persistence.inv.1` — StorageType MUST be explicitly declared with justification.
- `data_persistence.inv.2` — Operations MUST NOT assume stronger consistency than declared.
- `data_persistence.inv.3` — Queries MUST have declared QueryBudget; unbounded queries forbidden.
- `data_persistence.inv.4` — Cached data MUST NOT violate ConsistencyModel.
- `data_persistence.inv.5` — On data mutation, relevant caches MUST be invalidated within declared window.
- `data_persistence.inv.6` — Cross-partition transactions MUST be explicitly declared and minimized.
- `data_persistence.inv.7` — Data past RetentionPolicy MUST be archived or deleted per policy.
- `data_persistence.inv.8` — Backup frequency MUST satisfy RPO; recovery process MUST satisfy RTO.
- `data_persistence.inv.9` — Declared constraints MUST be enforced at specified layer.

## Distributed systems (`distributed_systems.inv.*`)

- `distributed_systems.inv.1` — Advertised ConsistencyLevel MUST be guaranteed under declared failure modes.

## Error handling (`error_handling.inv.*`)

- `error_handling.inv.1` — Every error MUST be classified.
- `error_handling.inv.2` — Errors MUST carry sufficient context for diagnosis.
- `error_handling.inv.3` — Internal errors MUST NOT leak implementation details.
- `error_handling.inv.4` — Error responses MUST include trace_id for support correlation.
- `error_handling.inv.5` — System MUST correctly classify retry eligibility.
- `error_handling.inv.6` — Exceeding ErrorBudget MUST trigger action.
- `error_handling.inv.7` — User-facing errors MUST be actionable and localized.
- `error_handling.inv.8` — All errors MUST be logged with appropriate level.
- `error_handling.inv.9` — Degradation MUST maintain core functionality when possible.
- `error_handling.inv.10` — Unhandled errors MUST be caught at top level and reported.

## Evidence harness (`evidence_harness.inv.*`)

- `evidence_harness.inv.1` — Generated scenarios MUST be runnable and produce pass/fail vs EvidenceProbe.
- `evidence_harness.inv.2` — FalsificationLoop MUST stop when counterexample found and record it.

## Internationalization (`internationalization.inv.*`)

- `internationalization.inv.1` — System MUST determine user locale explicitly.
- `internationalization.inv.2` — User-visible strings MUST NOT be hardcoded.
- `internationalization.inv.3` — Plural-sensitive messages MUST use locale-appropriate plural rules.
- `internationalization.inv.4` — Date/time display MUST respect user locale and timezone.
- `internationalization.inv.5` — Number display MUST respect locale conventions.
- `internationalization.inv.6` — Currency amounts MUST display with correct symbol and precision.
- `internationalization.inv.7` — String sorting MUST use locale-appropriate collation.

## Messaging (`messaging.inv.*`)

- `messaging.inv.1` — System MUST NOT claim stronger guarantee than implemented.
- `messaging.inv.2` — Messages MUST validate against declared schema.
- `messaging.inv.3` — Messages with same PartitionKey MUST be delivered in order within partition.
- `messaging.inv.4` — When BufferLimit exceeded, BackpressureStrategy MUST activate.
- `messaging.inv.5` — Messages failing after max_retries MUST route to DLQ.
- `messaging.inv.6` — EventStore is append-only; events immutable.
- `messaging.inv.7` — Stronger ordering increases latency and reduces throughput.
- `messaging.inv.8` — Message publishing MUST be atomic with business transaction.

## ML/AI systems (`ml_ai_systems.inv.*`)

- `ml_ai_systems.inv.1` — Only validated models with status=production may serve live traffic.
- `ml_ai_systems.inv.2` — Model MUST reference specific DataLineage; no training on unversioned data.
- `ml_ai_systems.inv.3` — InferenceResponse MUST include model_version for traceability.
- `ml_ai_systems.inv.4` — Model MUST pass all ValidationThresholds before promotion.
- `ml_ai_systems.inv.5` — Drift exceeding threshold MUST trigger alert and potential retraining.
- `ml_ai_systems.inv.6` — Model MUST meet FairnessMetric thresholds for ProtectedAttributes.
- `ml_ai_systems.inv.7` — Every production model MUST have ModelCard.
- `ml_ai_systems.inv.8` — Predictions meeting ReviewTrigger MUST be routed for HumanReview.
- `ml_ai_systems.inv.9` — Previous model version MUST be available for immediate rollback.

## Networking (`networking.inv.*`)

- `networking.inv.1` — Protocol MUST match communication requirements.
- `networking.inv.2` — Connections MUST be returned to pool or closed.
- `networking.inv.3` — Traffic MUST NOT route to unhealthy instances.
- `networking.inv.4` — Stale registrations MUST expire within TTL.
- `networking.inv.5` — DNS TTL MUST be honored for caching.
- `networking.inv.6` — Connections MUST use TLS ≥ declared minimum version.
- `networking.inv.7` — Retries MUST NOT exceed configured attempts.
- `networking.inv.8` — ConnectTimeout + ReadTimeout MUST NOT exceed caller's deadline.
- `networking.inv.9` — Requests exceeding RateLimit MUST be rejected with 429.
- `networking.inv.10` — Traffic MUST NOT flow between zones without explicit FirewallRule.

## Observability (`obs.inv.*`)

- `obs.inv.1` — Every log line in request scope MUST carry TraceId.
- `obs.inv.2` — At boundary exit, record Probe with TraceId+SpanId.

## Performance (`performance.inv.*`)

- `performance.inv.1` — SLI MUST be measured and compared to SLO continuously.
- `performance.inv.2` — Sum of component budgets MUST NOT exceed total LatencyBudget.
- `performance.inv.3` — SLO MUST specify percentile, not just average.
- `performance.inv.4` — System MUST handle ThroughputTarget under normal conditions.
- `performance.inv.5` — ResourceUtilization MUST NOT exceed ResourceBudget thresholds.
- `performance.inv.6` — Scaling MUST respect min/max bounds.
- `performance.inv.7` — Load shedding MUST preserve high-priority requests.
- `performance.inv.8` — Cache MUST NOT serve stale data beyond declared staleness.
- `performance.inv.9` — Performance regression beyond threshold MUST block deployment.

## Schema evolution (`schema_evolve.inv.*`)

- `schema_evolve.inv.1` — Clients within DeprecationWindow MUST be accepted.
- `schema_evolve.inv.2` — After DeprecationWindow deprecated path MUST be rejected with clear error.

## Privacy & data protection (`privacy_data_protection.inv.*`)

- `privacy_data_protection.inv.1` — All data stores MUST have declared DataClass.
- `privacy_data_protection.inv.2` — Processing PII requires valid ConsentRecord for declared purpose.
- `privacy_data_protection.inv.3` — Data MUST NOT be processed beyond declared purpose without new consent.
- `privacy_data_protection.inv.4` — SubjectRequest MUST be fulfilled within regulatory timeframe.
- `privacy_data_protection.inv.5` — Erasure MUST propagate to all copies and processors.
- `privacy_data_protection.inv.6` — System MUST NOT collect more PII than necessary for declared purpose.
- `privacy_data_protection.inv.7` — Anonymized data MUST NOT be re-identifiable with reasonable effort.
- `privacy_data_protection.inv.8` — PII transfer across jurisdictions MUST have legal basis.
- `privacy_data_protection.inv.9` — Processors MUST be bound by equivalent privacy obligations.
- `privacy_data_protection.inv.10` — Breach notification MUST occur within regulatory timeframe.

## Resilience (`resilience.inv.*`)

- `resilience.inv.1` — When open, no new calls to protected dependency.
- `resilience.inv.2` — ReconciliationRun MUST restore invariants or escalate.

## Temporal & concurrency (`temporal.inv.*`)

- `temporal.inv.1` — Same key applied twice → at most one observable effect.
- `temporal.inv.2` — Only lease holder may commit leased resource until expiry.
- `temporal.inv.3` — All saga steps commit OR compensations restore prior state.

## Workflow orchestration (`workflow_orchestration.inv.*`)

- `workflow_orchestration.inv.1` — Workflow MUST have defined start state and at least one terminal state.
- `workflow_orchestration.inv.2` — Step MUST transition to terminal status (completed, failed, skipped).
- `workflow_orchestration.inv.3` — WorkflowInstance state MUST be persisted durably.
- `workflow_orchestration.inv.4` — All parallel branches MUST complete or fail before join.
- `workflow_orchestration.inv.5` — HumanTask MUST have assignee and deadline.
- `workflow_orchestration.inv.6` — If workflow fails after side effects, compensations MUST execute.
- `workflow_orchestration.inv.7` — Running instances MUST complete on their original version or migrate safely.
- `workflow_orchestration.inv.8` — Timeout MUST trigger defined action (fail, escalate, skip).
- `workflow_orchestration.inv.9` — Subworkflow failure MUST be handled by parent workflow.
