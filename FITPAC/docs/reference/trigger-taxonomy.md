---
title: FITPAC trigger and condition taxonomy
status: normative-reference
implements: RFC-0005
license: CC-BY-4.0
license_url: https://creativecommons.org/licenses/by/4.0/
copyright_holder: Paul Roy and FITPAC Contributors
attribution_note: Attribution required under CC BY 4.0.
---

# Trigger and condition taxonomy

This document defines the **canonical trigger and condition vocabulary** used by pattern rules and specs. It is the single reference for the `triggers` field in rule metadata and for structured \"when\"/\"if\" clauses in prose.

The taxonomy is **extensible by namespace**, but the core lists and structure in this file are normative.

## 1. Structure

Triggers and conditions are grouped by the primitives in `00_primitive_spine.md` and by common sections in the spec schema:

- **Entity / Transformation / Time** — lifecycle and temporal triggers.
- **Boundary / Transaction** — IO and interaction triggers.
- **Authority / Policy / Constraint** — access control and legality.
- **Context** — environment, locale, tenant, deployment.

Each entry has the form:

```text
<namespace?>:<name>[:<qualifier>]
```

- `<namespace>` — Optional domain/module namespace (e.g. `messaging`, `ml_ai`, `a11y`). Omitted for core triggers.
- `<name>` — Short, stable identifier.
- `<qualifier>` — Optional refinement (e.g. `timeout`, `rate_limit`).

Examples: `on_write`, `on_error:timeout`, `precondition:authority`, `invariant:state_legality`, `messaging:queue_backlog_high`.

## 2. Core trigger taxonomy

### 2.1 Entity and transformation triggers

- `on_create` — A new entity is created.
- `on_update` — An existing entity is updated (state change).
- `on_delete` — An entity is deleted or tombstoned.
- `on_read` — An entity or projection is read.
- `on_projection_refresh` — A projection or materialized view is rebuilt or updated.

These map primarily to **Entity**, **Transformation**, and **Projection** primitives.

### 2.2 Temporal triggers

- `on_deadline` — A deadline or due date is reached.
- `on_timer` — A periodic or one‑shot timer fires.
- `on_idle` — A resource or actor has been idle longer than a threshold.
- `on_time_skew_detected` — Clock or time‑source drift is detected beyond an allowed bound.

These map primarily to the **Time** primitive and temporal patterns.

### 2.3 Boundary and interaction triggers

- `on_request` — An inbound request crosses a boundary (API call, message, RPC).
- `on_response` — A response is produced and leaves a boundary.
- `on_retry` — A retry is scheduled or attempted.
- `on_backoff` — Backoff policy is applied.
- `on_timeout` — A boundary or transaction times out.

These map to **Boundary** and **Transaction** primitives.

### 2.4 Error and resilience triggers

- `on_error` — An error is observed (generic).
- `on_error:timeout` — A timeout error occurs.
- `on_error:transient` — A transient/retryable error occurs.
- `on_error:permanent` — A permanent/non‑retryable error occurs.
- `on_circuit_open` — A circuit breaker opens.
- `on_circuit_half_open` — A circuit breaker transitions to half‑open.
- `on_circuit_close` — A circuit breaker closes again.

These connect primarily to `error_handling`, `resilience`, and `boundaries` modules.

### 2.5 Authority and policy triggers

- `precondition:authority` — A required authority or capability must be present.
- `precondition:approval` — A required approval tier or quorum must be satisfied.
- `precondition:scope` — A scope or audience restriction must hold.
- `postcondition:audit_log` — An action must be recorded in audit or evidence harness.

These map to **Authority**, **Constraint**, **Policy**, and governance modules.

### 2.6 Invariant and legality triggers

- `invariant:state_legality` — State transitions must respect ontology legality rules.
- `invariant:privacy_budget` — Privacy budget or data‑sharing limits must hold.
- `invariant:temporal_consistency` — Temporal ordering or staleness bounds must hold.
- `invariant:authz_consistency` — Authorization decisions must be consistent with declared policy.

These attach to **Constraint** primitives and typically reference `X.inv.N` invariants.

## 3. Conditions

Conditions refine when triggers apply. They reuse the same vocabulary but are usually expressed in prose:

- **Examples**:
  - \"when `on_write` to a high‑risk entity\"
  - \"if `on_error:timeout` during a saga step\"
  - \"while `invariant:state_legality` is at risk\"

Implementations SHOULD:

- Normalize any structured conditions they can detect back to these trigger identifiers.
- Preserve free‑form prose when normalization is not possible, without inventing new identifiers.

## 4. Extension mechanism

Domain modules MAY extend the taxonomy by introducing namespaced entries:

- `messaging:queue_backlog_high`
- `ml_ai:model_drift_detected`
- `a11y:contrast_ratio_low`

Extension rules:

1. The `<namespace>` MUST be a canonical module key from `master_index.yaml.pattern_map` (e.g. `messaging`, `ml_ai_systems`, `accessibility`).
2. New entries MUST be documented in that module’s pattern file and SHOULD be summarized in its own \"Trigger extensions\" section.
3. Extensions MUST NOT redefine the meaning of a core (unnamespaced) trigger; they can only refine or add.

## 5. Usage in rule metadata

- `triggers` entries in pattern YAML MUST be drawn from:
  - this core list, or
  - documented namespaced extensions (e.g. `messaging:...`, `ml_ai_systems:...`).
- Implementations MAY support temporary, project‑local triggers, but SHOULD either:
  - map them to existing taxonomy entries, or
  - explicitly mark them as experimental and avoid baking them into stable specs.

This keeps retrieval, matching, and disambiguation stable as the pattern library grows to millions of rules.

