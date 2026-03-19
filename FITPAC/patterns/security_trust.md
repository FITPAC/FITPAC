# Security & Trust (Compressed)
# ID: security
# Module key (for fragment IDs): `security` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Governance owns approval; this governs identity, capability, and trust boundaries.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Non-Negotiable Invariants
```yaml
triggers: [security_risk_detected]
requires_primitives: [Authority, Constraint, Policy]
output_type: policy
domain: core
category: security
```

- NO string concat in DB queries (use params).
- NO untrusted input without schema validation.
- NO cross-boundary calls without Trust Bridge.
- NO sensitive ops if ThreatModel is expired.

## p2: Capability Minting Gate
```yaml
triggers: [security_risk_detected]
requires_primitives: [Authority, Constraint, Policy]
output_type: policy
domain: core
category: security
```

- REQUIRE: `threat_context` in all minting requests.
- DENY: If capability violates mitigations for active threats.

## p3: Delegation Constraints
```yaml
triggers: [privilege_escalation]
requires_primitives: [Authority, Constraint, Policy]
output_type: policy
domain: core
category: security
```

- MAX_DEPTH: 2 (default).
- NO loops.
- NO cross-boundary delegation without explicit Bridge.

## p4: IOContract
```yaml
triggers: [untyped_output_sink]
requires_primitives: [Authority, Constraint, Policy]
output_type: policy
domain: core
category: security
```

- INPUT: Must map to schema.
- OUTPUT: Must have declared encoder (e.g., escape_html, parameterized_sql).

## p5: URL Allowlist and SSRF Mitigation
```yaml
triggers: [security_risk_detected]
requires_primitives: [Authority, Constraint, Policy]
output_type: policy
domain: core
category: security
```

- RULE: No fetch-by-URL without allowlist; no user-controlled URL to internal or metadata IPs. Use URL allowlist contract; block DNS rebinding; restrict egress by policy.
- Triggers: security_risk_detected (SSRF, unsafe URL fetch).

## p6: Redaction and Never-Log
```yaml
triggers: [security_risk_detected]
requires_primitives: [Authority, Constraint, Policy]
output_type: policy
domain: core
category: security
```

- RULE: Declare redaction rules and never-log fields in contract; never log secrets, tokens, or PII in plain text. Redact in errors and stack traces.
- Triggers: security_risk_detected (secrets mishandling).

## p7: Safe Deserialization and Parsing
```yaml
triggers: [security_risk_detected]
requires_primitives: [Authority, Constraint, Policy]
output_type: policy
domain: core
category: security
```

- RULE: Allowed parser list and safe modes only; no vulnerable deserializers, no unsafe YAML/XML entity expansion. Use safe parsing options; validate size and depth.
- Triggers: security_risk_detected (unsafe deserialization).
