# Observability & Diagnostics (Compressed)
# ID: obs
# Module key (for fragment IDs): `obs` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Boundaries own contract; obs is instrumentation only.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Trace Context
```yaml
triggers: [trace_correlation_needed]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- Primitives: TraceId, SpanId.
- Invariants: Every log line in request scope MUST carry TraceId (obs.inv.1).
- Triggers: trace_correlation_needed, partial_failure.
- RULE: Accept or create TraceId at entry. Create SpanId for this unit. Propagate both in headers/context to callees. Attach to all logs and error reports.

## p2: Probes
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- Primitives: Probe (timestamp, boundary_name, outcome, latency).
- Invariants: At boundary exit (outgoing call, DB, queue), record Probe with TraceId+SpanId (obs.inv.2).
- RULE: At each boundary record Probe; include success/failure and latency. Link to TraceId.

## p3: Causal Log
```yaml
triggers: [trace_correlation_needed]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: core
category: boundary
```

- Primitives: CausalLog (cause_chain, TraceId).
- Triggers: error_taxonomy_undefined, trace_correlation_needed.
- RULE: On failure include cause chain (nested exception or cause IDs). One structured causal record per failure; link to TraceId.
