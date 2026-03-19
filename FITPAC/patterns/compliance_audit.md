# Compliance & Audit (Compressed)
# ID: compliance
# Module key (for fragment IDs): `compliance_audit` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Security governs access control; governance governs approval; this governs audit trails and regulatory compliance.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Audit Trail Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: compliance
category: other
```

- Primitives: AuditEvent (actor, action, resource, timestamp, outcome, context), AuditLog.
- Invariants: AuditLog MUST be append-only and tamper-evident (compliance_audit.inv.1).
- Triggers: audit_gap, tampering_detected.
- RULE: Define auditable actions per resource type. Capture AuditEvent before action completion. Include actor identity, action type, affected resource, timestamp (UTC), outcome (success/failure), and relevant context. Use cryptographic chaining or write-once storage.

## p2: Retention and Legal Hold
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: compliance
category: other
```

- Primitives: RetentionPolicy (min_period, max_period, jurisdiction), LegalHold.
- Invariants: Data under LegalHold MUST NOT be deleted regardless of RetentionPolicy (compliance_audit.inv.2).
- Triggers: retention_violation, legal_hold_breach.
- RULE: Declare RetentionPolicy per data classification (`data_persistence.p8`). Implement automated retention enforcement. LegalHold overrides deletion. Track LegalHold scope and expiration. Coordinate with privacy (`privacy_data_protection.p4`).

## p3: Segregation of Duties
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: compliance
category: other
```

- Primitives: Role, DutyConstraint (mutex_roles, required_approvers), DutyViolation.
- Invariants: Mutex roles MUST NOT be assigned to same actor (compliance_audit.inv.3).
- Triggers: duty_violation, privilege_conflict.
- RULE: Define DutyConstraints for sensitive operations (e.g., developer cannot deploy own code to production). Enforce at role assignment and operation execution. Log and alert on violations.

## p4: Change Management
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: compliance
category: other
```

- Primitives: ChangeRequest (requester, approvers, scope, risk), ChangeWindow, ChangeLog.
- Invariants: Production changes MUST have approved ChangeRequest (compliance_audit.inv.4).
- Triggers: unauthorized_change, change_window_violation.
- RULE: All production changes require ChangeRequest. Define approval workflow based on risk (governance.p1). Restrict changes to ChangeWindow (maintenance windows). Log all changes with before/after state.

## p5: Evidence Collection
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: compliance
category: other
```

- Primitives: ControlEvidence (control_id, evidence_type, collection_date, artifacts), ControlFramework.
- Triggers: evidence_missing, audit_preparation.
- RULE: Map controls to ControlFramework (SOC2, ISO27001, etc.). Define evidence collection frequency. Automate evidence gathering where possible. Store evidence with tamper-evident timestamps. Link to AuditEvents.

## p6: Compliance Attestation
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: compliance
category: other
```

- Primitives: Attestation (scope, framework, period, findings, attestor), AttestationSchedule.
- Invariants: Attestation MUST occur per AttestationSchedule (compliance_audit.inv.5).
- Triggers: attestation_overdue, finding_unresolved.
- RULE: Schedule attestations per framework requirements. Track findings and remediation. Attestation requires sign-off from authorized attestor. Publish attestation status to stakeholders.

## p7: Access Review
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: compliance
category: other
```

- Primitives: AccessReview (scope, reviewer, period), AccessCertification.
- Invariants: Access rights MUST be reviewed per AccessReview schedule (compliance_audit.inv.6).
- Triggers: access_review_overdue, orphan_access.
- RULE: Define AccessReview frequency per resource sensitivity. Reviewer certifies or revokes access. Remove access for terminated users immediately. Flag dormant accounts for review.

## p8: Audit Query Interface
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: compliance
category: other
```

- Primitives: AuditQuery (time_range, actor, resource, action), AuditReport.
- Triggers: investigation_request, compliance_inquiry.
- RULE: Provide standardized AuditQuery interface. Support time-range, actor, resource, and action filters. Generate AuditReport with complete chain of events. Ensure query does not modify audit data.

## p9: Non-Repudiation
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: compliance
category: other
```

- Primitives: DigitalSignature, SignatureVerification, NonRepudiationEvidence.
- Invariants: Signed actions MUST be verifiable by any party with public key (compliance_audit.inv.7).
- Triggers: signature_invalid, repudiation_attempt.
- RULE: For high-value transactions, require DigitalSignature from actor. Store signature with AuditEvent. Verification MUST NOT require actor cooperation. Use timestamping authority for temporal proof.

## p10: Compliance Dashboard
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: compliance
category: other
```

- Primitives: ComplianceMetric (control_id, status, last_check), ComplianceScore.
- Triggers: compliance_drift, control_failure.
- RULE: Aggregate compliance status across controls. Calculate ComplianceScore per framework. Alert on control failures. Provide drill-down to specific evidence and findings. Update metrics continuously or per schedule.
