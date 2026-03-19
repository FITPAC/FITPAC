# Privacy & Data Protection (Compressed)
# ID: privacy
# Module key (for fragment IDs): `privacy_data_protection` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Security governs access control; compliance governs audit; this governs PII handling and data subject rights.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Data Classification
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: privacy
category: other
```

- Primitives: DataClass (public, internal, confidential, restricted, PII, sensitive_PII), ClassificationLabel.
- Invariants: All data stores MUST have declared DataClass (privacy_data_protection.inv.1).
- Triggers: unclassified_data, classification_mismatch.
- RULE: Classify data at creation/ingestion. PII: identifiable to individual. Sensitive PII: health, financial, biometric, children's data. Classification determines handling rules, access controls, and retention.

## p2: Consent Management
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: privacy
category: other
```

- Primitives: ConsentRecord (subject, purpose, scope, timestamp, expiry), ConsentState (granted, withdrawn, expired).
- Invariants: Processing PII requires valid ConsentRecord for declared purpose (privacy_data_protection.inv.2).
- Triggers: consent_missing, consent_expired, purpose_mismatch.
- RULE: Capture consent with specific purpose. Store ConsentRecord with timestamp and version of terms. Check consent before processing. Honor withdrawal immediately. Consent withdrawal MUST NOT require more effort than granting.

## p3: Purpose Limitation
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: privacy
category: other
```

- Primitives: ProcessingPurpose (declared, actual), PurposeBinding.
- Invariants: Data MUST NOT be processed beyond declared purpose without new consent (privacy_data_protection.inv.3).
- Triggers: purpose_violation, secondary_use_detected.
- RULE: Declare ProcessingPurpose at collection. Bind data to purpose. Secondary uses require: new consent, legal basis, or compatible purpose determination. Log purpose checks for audit.

## p4: Data Subject Rights
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: privacy
category: other
```

- Primitives: SubjectRequest (type, subject_id, verification), RequestType (access, rectification, erasure, portability, restriction).
- Invariants: SubjectRequest MUST be fulfilled within regulatory timeframe (privacy_data_protection.inv.4).
- Triggers: subject_request_received, request_overdue.
- RULE: Implement request intake with identity verification. Access: provide copy of all PII. Rectification: correct inaccurate data. Erasure: delete unless legal obligation. Portability: machine-readable export. Restriction: halt processing. Track request status and deadlines.

## p5: Right to Erasure (Deletion)
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: privacy
category: other
```

- Primitives: DeletionRequest, DeletionScope (full, partial, anonymize), DeletionConfirmation.
- Invariants: Erasure MUST propagate to all copies and processors (privacy_data_protection.inv.5).
- Triggers: erasure_request, retention_conflict, legal_hold_conflict.
- RULE: On erasure request, identify all data locations including backups, caches, logs, and third-party processors. Execute deletion or anonymization. Confirm completion. Document exceptions (legal holds, legitimate interest). Notify processors of erasure requirement.

## p6: Data Minimization
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: privacy
category: other
```

- Primitives: MinimizationPolicy (required_fields, retention_limit, aggregation_threshold).
- Invariants: System MUST NOT collect more PII than necessary for declared purpose (privacy_data_protection.inv.6).
- Triggers: overcollection, unnecessary_retention.
- RULE: Define minimum required fields per purpose. Reject collection of unnecessary fields. Implement automatic deletion or anonymization after purpose fulfilled. Aggregate or pseudonymize where individual data not required.

## p7: Anonymization and Pseudonymization
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: privacy
category: other
```

- Primitives: AnonymizationMethod (k_anonymity, differential_privacy, generalization), PseudonymizationKey.
- Invariants: Anonymized data MUST NOT be re-identifiable with reasonable effort (privacy_data_protection.inv.7).
- Triggers: re_identification_risk, anonymization_failed.
- RULE: Declare AnonymizationMethod per use case. Test re-identification risk. Pseudonymization: separate identifiers from data, protect mapping. Anonymization: irreversible. Document method and risk assessment.

## p8: Cross-Border Transfer
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: privacy
category: other
```

- Primitives: TransferMechanism (adequacy, SCCs, BCRs, consent), DataLocalization.
- Invariants: PII transfer across jurisdictions MUST have legal basis (privacy_data_protection.inv.8).
- Triggers: cross_border_transfer, localization_violation.
- RULE: Identify data residency requirements per jurisdiction. Implement TransferMechanism for cross-border flows. Some data may require DataLocalization (no transfer). Document transfer impact assessments.

## p9: Privacy by Design
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: privacy
category: other
```

- Primitives: PrivacyControl (technical, organizational), PrivacyImpactAssessment (PIA).
- Triggers: new_processing_activity, high_risk_processing.
- RULE: Conduct PIA for new processing activities involving PII. Implement PrivacyControls: encryption, access control, audit logging, minimization. Privacy settings default to most protective. Document privacy architecture decisions.

## p10: Third-Party Processor Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: privacy
category: other
```

- Primitives: ProcessorAgreement (scope, obligations, audit_rights), SubprocessorList.
- Invariants: Processors MUST be bound by equivalent privacy obligations (privacy_data_protection.inv.9).
- Triggers: processor_violation, unauthorized_subprocessor.
- RULE: Execute ProcessorAgreement before sharing PII. Include: processing scope, security requirements, audit rights, breach notification, deletion on termination. Maintain SubprocessorList. Audit processors periodically.

## p11: Breach Notification
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: privacy
category: other
```

- Primitives: BreachRecord (scope, discovery_time, notification_time, affected_subjects), NotificationObligation.
- Invariants: Breach notification MUST occur within regulatory timeframe (privacy_data_protection.inv.10).
- Triggers: breach_detected, notification_deadline.
- RULE: Define breach detection procedures. On detection, assess scope and risk. Notify regulators within required timeframe (e.g., 72 hours GDPR). Notify affected subjects if high risk. Document breach and response in BreachRecord.
