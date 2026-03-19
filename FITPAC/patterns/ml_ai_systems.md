# ML/AI Systems (Compressed)
# ID: ml_ai
# Module key (for fragment IDs): `ml_ai_systems` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Containment governs speculation; compliance governs audit; this governs model lifecycle, inference, and AI-specific concerns.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Model Lifecycle Contract
```yaml
triggers: [model_promotion, model_deprecation, model_failure]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: ml_ai
category: other
```

- Primitives: ModelVersion (id, training_date, metrics, status), ModelStatus (training, validating, staging, production, deprecated, archived).
- Invariants: Only validated models with status=production may serve live traffic (ml_ai_systems.inv.1).
- Triggers: model_promotion, model_deprecation, model_failure.
- RULE: Define lifecycle stages. Training produces candidate. Validation checks metrics against thresholds. Staging tests integration. Production serves traffic. Deprecated models phased out. Archive retains for audit/reproducibility.

## p2: Training Data Lineage
```yaml
triggers: [data_lineage_missing, data_drift_detected]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: ml_ai
category: other
```

- Primitives: DataLineage (sources, transformations, version, snapshot_id), DataContract.
- Invariants: Model MUST reference specific DataLineage; no training on unversioned data (ml_ai_systems.inv.2).
- Triggers: data_lineage_missing, data_drift_detected.
- RULE: Capture DataLineage: source datasets, preprocessing steps, feature engineering, sampling. Version snapshots. Store lineage with ModelVersion. Enables reproducibility and debugging. Coordinate with `privacy_data_protection.p3` for PII in training data.

## p3: Inference Contract
```yaml
triggers: [inference_timeout, low_confidence, model_version_mismatch]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: ml_ai
category: other
```

- Primitives: InferenceRequest (input, model_version, timeout), InferenceResponse (output, confidence, latency, model_version).
- Invariants: InferenceResponse MUST include model_version for traceability (ml_ai_systems.inv.3).
- Triggers: inference_timeout, low_confidence, model_version_mismatch.
- RULE: Define input schema and output schema per model. Include confidence scores where applicable. Set timeout budgets (budgets.p1). Log inference requests for monitoring. Handle model unavailability gracefully (resilience.p1).

## p4: Model Validation Gate
```yaml
triggers: [validation_failed, metric_regression]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: ml_ai
category: other
```

- Primitives: ValidationMetric (accuracy, precision, recall, F1, custom), ValidationThreshold, ValidationReport.
- Invariants: Model MUST pass all ValidationThresholds before promotion (ml_ai_systems.inv.4).
- Triggers: validation_failed, metric_regression.
- RULE: Define ValidationMetrics per model type. Set thresholds based on business requirements. Compare candidate to champion model. Generate ValidationReport. Block promotion if thresholds not met. Include fairness metrics (p7).

## p5: Champion-Challenger
```yaml
triggers: [challenger_outperforms, challenger_underperforms]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: ml_ai
category: other
```

- Primitives: ChampionModel (current production), ChallengerModel (candidate), TrafficSplit.
- Triggers: challenger_outperforms, challenger_underperforms.
- RULE: Deploy ChallengerModel alongside ChampionModel with TrafficSplit. Compare metrics on same traffic. Promote challenger if metrics better after observation window. Rollback challenger if degradation. Automate or require human approval.

## p6: Drift Detection
```yaml
triggers: [drift_detected, model_staleness]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: ml_ai
category: other
```

- Primitives: DriftType (data_drift, concept_drift, prediction_drift), DriftMetric, DriftThreshold.
- Invariants: Drift exceeding threshold MUST trigger alert and potential retraining (ml_ai_systems.inv.5).
- Triggers: drift_detected, model_staleness.
- RULE: Monitor input distribution (data drift), prediction distribution (prediction drift), and actual outcomes (concept drift). Compare to training distribution. Alert when DriftMetric exceeds DriftThreshold. Schedule retraining or investigation.

## p7: Fairness and Bias Contract
```yaml
triggers: [bias_detected, fairness_violation]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: ml_ai
category: other
```

- Primitives: ProtectedAttribute (race, gender, age, etc.), FairnessMetric (demographic_parity, equalized_odds, calibration), BiasThreshold.
- Invariants: Model MUST meet FairnessMetric thresholds for ProtectedAttributes (ml_ai_systems.inv.6).
- Triggers: bias_detected, fairness_violation.
- RULE: Identify ProtectedAttributes relevant to use case. Measure FairnessMetrics on validation data. Set BiasThreshold per metric. Document fairness assessment. Block deployment if thresholds violated. Coordinate with compliance.

## p8: Explainability Contract
```yaml
triggers: [explanation_required, unexplainable_prediction]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: ml_ai
category: other
```

- Primitives: ExplanationType (feature_importance, counterfactual, attention, SHAP), ExplainabilityRequirement.
- Triggers: explanation_required, unexplainable_prediction.
- RULE: Define ExplainabilityRequirement per use case (regulatory, user trust, debugging). Implement appropriate ExplanationType. High-stakes decisions (loan, medical) may require human-readable explanations. Store explanations with predictions for audit.

## p9: Model Card
```yaml
triggers: [model_card_missing, model_card_outdated]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: ml_ai
category: other
```

- Primitives: ModelCard (description, intended_use, limitations, metrics, fairness, training_data, ethical_considerations).
- Invariants: Every production model MUST have ModelCard (ml_ai_systems.inv.7).
- Triggers: model_card_missing, model_card_outdated.
- RULE: Create ModelCard documenting: purpose, intended use cases, known limitations, performance metrics, fairness evaluation, training data description, ethical considerations. Update on model changes. Publish for stakeholders.

## p10: Inference Batching and Caching
```yaml
triggers: [batch_timeout, cache_invalidation]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: ml_ai
category: other
```

- Primitives: BatchConfig (max_batch_size, max_wait_time), InferenceCache (TTL, key_strategy).
- Triggers: batch_timeout, cache_invalidation.
- RULE: For throughput optimization, batch inference requests. Configure max_batch_size and max_wait_time tradeoff. Cache deterministic predictions with appropriate TTL. Define cache key strategy. Invalidate cache on model update.

## p11: Human-in-the-Loop
```yaml
triggers: [review_required, review_backlog]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: ml_ai
category: other
```

- Primitives: ReviewTrigger (low_confidence, high_stakes, random_sample), HumanReview (reviewer, decision, feedback).
- Invariants: Predictions meeting ReviewTrigger MUST be routed for HumanReview (ml_ai_systems.inv.8).
- Triggers: review_required, review_backlog.
- RULE: Define ReviewTrigger criteria. Low confidence predictions queued for human review. High-stakes decisions may require human approval. Random sample for quality monitoring. Capture HumanReview feedback for model improvement.

## p12: Model Rollback
```yaml
triggers: [model_degradation, production_incident]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: ml_ai
category: other
```

- Primitives: ModelRollback (from_version, to_version, reason), RollbackCriteria.
- Invariants: Previous model version MUST be available for immediate rollback (ml_ai_systems.inv.9).
- Triggers: model_degradation, production_incident.
- RULE: Retain previous model versions in deployable state. Define RollbackCriteria (error rate, latency, fairness regression). Automated rollback on criteria breach or manual trigger. Log rollback events. Investigate root cause before re-promoting.

## p13: Feedback Loop Contract
```yaml
triggers: [feedback_delayed, feedback_missing]
requires_primitives: [Entity, Authority]
output_type: constraint
domain: ml_ai
category: other
```

- Primitives: FeedbackSignal (ground_truth, user_feedback, implicit_signal), FeedbackLatency.
- Triggers: feedback_delayed, feedback_missing.
- RULE: Define how ground truth or feedback is collected. Specify FeedbackLatency (immediate, delayed, never for some predictions). Use feedback for model evaluation, retraining triggers, and continuous improvement. Handle delayed feedback in evaluation metrics.
