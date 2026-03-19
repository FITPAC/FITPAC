# Error Handling & Recovery (Compressed)
# ID: errors
# Module key (for fragment IDs): `error_handling` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Boundaries governs taxonomy; resilience governs recovery; this governs error semantics, propagation, and user experience.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Error Classification
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: errors
category: other
```

- Primitives: ErrorClass (operational, programmer, system), ErrorSeverity (debug, info, warning, error, critical).
- Invariants: Every error MUST be classified (error_handling.inv.1).
- Triggers: unclassified_error, severity_mismatch.
- RULE: Classify errors: Operational (expected, recoverable: validation, not found), Programmer (bugs: null pointer, type error), System (infrastructure: OOM, disk full). Severity guides response. Extends boundaries.p2 taxonomy.

## p2: Error Context Enrichment
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: errors
category: other
```

- Primitives: ErrorContext (error_id, timestamp, trace_id, user_context, operation), ContextChain.
- Invariants: Errors MUST carry sufficient context for diagnosis (error_handling.inv.2).
- Triggers: context_missing, untraceable_error.
- RULE: Enrich errors with: unique error_id, timestamp, trace_id (obs.p1), user/request context, operation being performed. Build ContextChain for nested errors. Avoid losing inner cause when wrapping.

## p3: Error Propagation
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: errors
category: other
```

- Primitives: PropagationPolicy (wrap, unwrap, translate, absorb), ErrorBoundary.
- Invariants: Internal errors MUST NOT leak implementation details (error_handling.inv.3).
- Triggers: error_leak, propagation_lost.
- RULE: At ErrorBoundary: Wrap (add context, preserve cause), Unwrap (extract inner), Translate (map to boundary's taxonomy), Absorb (handle and don't propagate). Internal errors (stack traces, SQL) stay internal. Return user-friendly errors.

## p4: Error Response Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: errors
category: other
```

- Primitives: ErrorResponse (code, message, details, trace_id), ErrorFormat (RFC7807, custom).
- Invariants: Error responses MUST include trace_id for support correlation (error_handling.inv.4).
- Triggers: inconsistent_error_format.
- RULE: Standardize ErrorResponse format (prefer RFC7807 Problem Details). Include: machine-readable code, human-readable message, additional details, trace_id. Document error codes in API spec. Same format across all endpoints.

## p5: Retryable vs Terminal
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: errors
category: other
```

- Primitives: RetryableError (transient, retriable_after), TerminalError (requires_intervention).
- Invariants: System MUST correctly classify retry eligibility (error_handling.inv.5).
- Triggers: retry_terminal, no_retry_transient.
- RULE: Retryable: 503, timeout, connection reset, rate limited. Terminal: 400, 401, 403, 404, business rule violation. Include Retry-After header when applicable. Client retry policy depends on classification. Extends networking.p7.

## p6: Error Budgets
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: errors
category: other
```

- Primitives: ErrorBudget (allowed_errors, window), ErrorRate, BudgetStatus.
- Invariants: Exceeding ErrorBudget MUST trigger action (error_handling.inv.6).
- Triggers: budget_exceeded, budget_warning.
- RULE: Define ErrorBudget per service/endpoint. Calculate ErrorRate over sliding window. Budget = 100% - SLO (e.g., 99.9% SLO = 0.1% error budget). When exhausted: freeze changes, investigate, remediate. Extends performance.p1.

## p7: User-Facing Errors
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: errors
category: other
```

- Primitives: UserError (message, action, support_reference), ErrorLocalization.
- Invariants: User-facing errors MUST be actionable and localized (error_handling.inv.7).
- Triggers: cryptic_error, unlocalized_error.
- RULE: User errors should: explain what happened, suggest action, provide support reference. Localize messages (see `internationalization.p2` in the i18n module). Avoid jargon. Never expose stack traces, SQL, or internal IDs to users. A/B test error messages for clarity.

## p8: Error Logging
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: errors
category: other
```

- Primitives: ErrorLog (level, structured_data, stack_trace), LogLevel.
- Invariants: All errors MUST be logged with appropriate level (error_handling.inv.8).
- Triggers: unlogged_error, log_flood.
- RULE: Log errors with: severity level, structured context, stack trace (for programmer errors). Avoid log flooding (dedupe similar errors). Sample high-volume errors. Redact sensitive data (security.p6). Link to trace (obs.p1).

## p9: Error Aggregation
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: errors
category: other
```

- Primitives: ErrorAggregate (signature, count, first_seen, last_seen, sample), ErrorSignature.
- Triggers: new_error_type, error_spike.
- RULE: Group similar errors by ErrorSignature (message template, stack trace, error code). Track frequency. Alert on: new error types, error rate spikes. Sample representative instances. Prioritize by impact (frequency × severity).

## p10: Graceful Degradation
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: errors
category: other
```

- Primitives: DegradationLevel (full, reduced, minimal, unavailable), DegradationResponse.
- Invariants: Degradation MUST maintain core functionality when possible (error_handling.inv.9).
- Triggers: dependency_failure, degradation_activated.
- RULE: On errors, degrade gracefully: cache stale data, disable non-essential features, return partial results with warning. Define DegradationLevels. Communicate degradation to users. Log degradation events. Extends boundaries.p5.

## p11: Circuit Breaker Integration
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: errors
category: other
```

- Primitives: CircuitBreakerError, CircuitState (from resilience.p1).
- Triggers: circuit_open, circuit_reset.
- RULE: When circuit opens, fail fast with CircuitBreakerError. Return cached response or degraded mode, not generic error. Include time until retry. Monitor circuit state transitions. Extends resilience.p1 with error handling specifics.

## p12: Panic and Unhandled Errors
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: errors
category: other
```

- Primitives: PanicHandler, UnhandledError, CrashReport.
- Invariants: Unhandled errors MUST be caught at top level and reported (error_handling.inv.10).
- Triggers: unhandled_panic, process_crash.
- RULE: Install global PanicHandler. Catch unhandled errors before process exit. Generate CrashReport with state snapshot. Restart gracefully. Alert on panics. Never swallow panics silently. Post-mortem analysis required.

## p13: Error Testing
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: errors
category: other
```

- Primitives: ErrorScenario, FaultInjection, ChaosTest.
- Triggers: error_handling_untested.
- RULE: Test error paths: inject faults, verify correct classification, propagation, user messages. Test: network failures, timeouts, invalid input, resource exhaustion. Include error scenarios in evidence_harness. Chaos testing for resilience.
