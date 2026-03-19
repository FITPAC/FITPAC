# Configuration Management (Compressed)
# ID: config
# Module key (for fragment IDs): `configuration` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Security governs secrets; deployment governs environments; this governs config sources and validation.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Configuration Source Hierarchy
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: config
category: other
```

- Primitives: ConfigSource (default, file, environment, remote, override), ConfigPrecedence.
- Invariants: Higher precedence ConfigSource overrides lower (configuration.inv.1).
- Triggers: config_conflict, source_unavailable.
- RULE: Define ConfigPrecedence (typically: defaults < file < env < remote < explicit override). Document precedence clearly. Log effective configuration at startup. Handle source unavailability gracefully with fallback.

## p2: Configuration Schema
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: config
category: other
```

- Primitives: ConfigSchema (fields, types, constraints, defaults), SchemaValidation.
- Invariants: Configuration MUST validate against ConfigSchema before use (configuration.inv.2).
- Triggers: config_validation_failed, unknown_field.
- RULE: Define ConfigSchema with types, required fields, constraints (ranges, patterns). Validate on load. Reject invalid configuration with clear error. Unknown fields: warn or reject based on policy. Generate documentation from schema.

## p3: Secret Management
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: config
category: other
```

- Primitives: Secret (value, rotation_policy, access_log), SecretStore, SecretReference.
- Invariants: Secrets MUST NOT appear in plain text in config files, logs, or errors (configuration.inv.3).
- Triggers: secret_exposed, rotation_due, access_anomaly.
- RULE: Store secrets in SecretStore (vault, KMS, secrets manager). Config contains SecretReference, not values. Fetch secrets at runtime. Implement rotation without restart. Log secret access for audit (`compliance_audit.p1`). Extends security.p6.

## p4: Dynamic Configuration
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: config
category: other
```

- Primitives: DynamicConfig (key, value, version), ConfigUpdate, UpdatePropagation.
- Invariants: Dynamic config changes MUST propagate within declared latency (configuration.inv.4).
- Triggers: config_change, propagation_delay.
- RULE: Identify which configs can change dynamically without restart. Implement config watching or polling. Define propagation latency SLO. Handle partial propagation (some instances updated, others not). Version configs for consistency.

## p5: Configuration Drift Detection
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: config
category: other
```

- Primitives: ExpectedConfig, ActualConfig, ConfigDrift.
- Invariants: ConfigDrift MUST be detected and alerted (configuration.inv.5).
- Triggers: drift_detected, manual_override.
- RULE: Define ExpectedConfig from source control. Periodically compare to ActualConfig. Alert on ConfigDrift. Investigate: intentional override or error? Manual overrides require audit trail (governance.p2). Reconcile drift.

## p6: Environment-Specific Configuration
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: config
category: other
```

- Primitives: EnvironmentConfig (env_name, overrides), ConfigTemplate.
- Invariants: Production secrets MUST NOT exist in non-production configs (configuration.inv.6).
- Triggers: environment_mismatch, secret_leak.
- RULE: Use ConfigTemplate with environment-specific overrides. Separate secrets per environment. Never copy production secrets to staging. Document environment-specific behaviors. Test with production-like config in staging.

## p7: Feature Configuration
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: config
category: other
```

- Primitives: FeatureConfig (feature_id, enabled, parameters), FeatureTargeting.
- Triggers: feature_misconfigured, targeting_error.
- RULE: Separate feature configuration from infrastructure configuration. Define FeatureTargeting rules (user segments, percentages). Enable gradual rollout. Quick disable (kill switch) without deployment. Coordinate with deployment.p8.

## p8: Configuration Versioning
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: config
category: other
```

- Primitives: ConfigVersion (hash, timestamp, author), ConfigHistory.
- Invariants: Every config change MUST be versioned with author and timestamp (configuration.inv.7).
- Triggers: config_rollback_needed, unauthorized_change.
- RULE: Version control all configuration. Track ConfigHistory. Enable rollback to previous ConfigVersion. Require approval for production config changes (governance.p1). Audit who changed what when.

## p9: Configuration Dependencies
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: config
category: other
```

- Primitives: ConfigDependency (config_a requires config_b), DependencyValidation.
- Invariants: Configuration MUST NOT be applied if dependencies unsatisfied (configuration.inv.8).
- Triggers: dependency_missing, circular_dependency.
- RULE: Declare ConfigDependencies. Validate dependencies on load. Fail fast if dependency missing. Detect circular dependencies. Document dependency graph.

## p10: Sensitive Configuration Handling
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: config
category: other
```

- Primitives: SensitiveField (field_name, handling_rule), RedactionPolicy.
- Invariants: Sensitive fields MUST be redacted in logs and error messages (configuration.inv.9).
- Triggers: sensitive_data_logged.
- RULE: Mark SensitiveFields in ConfigSchema. Apply RedactionPolicy when logging or displaying config. Never include in stack traces. Use masking in debug output. Extends security.p6.

## p11: Configuration Testing
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: config
category: other
```

- Primitives: ConfigTest (scenario, expected_behavior), ConfigTestSuite.
- Triggers: config_test_failed.
- RULE: Test configuration changes before deployment. Include: valid configs load correctly, invalid configs rejected with clear errors, feature flags behave as expected, environment-specific configs don't leak. Run ConfigTestSuite in CI.
