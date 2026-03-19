# Workflow & Process Orchestration (Compressed)
# ID: workflow
# Module key (for fragment IDs): `workflow_orchestration` (see `master_index.yaml.pattern_map`)
# Version: 1.0.0
# Status: active
# Last reviewed: 2026-02-23
# Assumptions: Temporal governs sagas; governance governs approval; this governs workflow definition and execution.
# License: CC-BY-4.0
# License URL: https://creativecommons.org/licenses/by/4.0/
# Origin: maintainer
# Adoption Status: adopted
# Standard Inclusion: canonical-reference
# Canonical Manifest Pin: FITPAC 1.0.0 reference distribution

## p1: Workflow Definition Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: workflow
category: other
```

- Primitives: Workflow (id, version, steps, transitions), WorkflowStep (action, inputs, outputs, conditions), WorkflowState.
- Invariants: Workflow MUST have defined start state and at least one terminal state (workflow_orchestration.inv.1).
- Triggers: workflow_undefined, invalid_transition.
- RULE: Define Workflow declaratively with steps and transitions. Each step has: action to perform, inputs required, outputs produced, transition conditions. Version workflows. Store definition separate from execution.

## p2: Step Execution Contract
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: workflow
category: other
```

- Primitives: StepExecution (step_id, input, output, status, start_time, end_time), ExecutionStatus (pending, running, completed, failed, skipped).
- Invariants: Step MUST transition to terminal status (completed, failed, skipped) (workflow_orchestration.inv.2).
- Triggers: step_timeout, step_failed.
- RULE: Execute step with declared inputs. Capture outputs. Record execution time. Handle failures: retry (with limits), skip (if optional), or fail workflow. Log all status transitions.

## p3: Workflow Instance Lifecycle
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: workflow
category: other
```

- Primitives: WorkflowInstance (workflow_id, instance_id, state, context), InstanceStatus (created, running, paused, completed, failed, cancelled).
- Invariants: WorkflowInstance state MUST be persisted durably (workflow_orchestration.inv.3).
- Triggers: instance_stalled, instance_orphaned.
- RULE: Create WorkflowInstance from Workflow definition. Persist state after each step. Enable resume after failures. Support pause/resume. Track instance history. Clean up completed instances per retention policy.

## p4: Parallel Execution
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: workflow
category: other
```

- Primitives: ParallelBranch (steps, join_condition), ForkJoin, ParallelResult.
- Invariants: All parallel branches MUST complete or fail before join (workflow_orchestration.inv.4).
- Triggers: branch_timeout, partial_completion.
- RULE: Define parallel execution with fork-join. Branches execute concurrently. Join condition: all-complete, any-complete, or custom. Handle partial failures: fail-fast or wait-for-all. Aggregate results at join.

## p5: Conditional Branching
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: workflow
category: other
```

- Primitives: Condition (expression, evaluation), ConditionalTransition, BranchSelector.
- Triggers: condition_evaluation_failed, no_matching_branch.
- RULE: Define conditions on transitions. Evaluate conditions against workflow context. Support: if-then-else, switch-case, guards. Default branch for unmatched conditions. Log branch decisions for debugging.

## p6: Human Task Integration
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: workflow
category: other
```

- Primitives: HumanTask (description, assignee, deadline, form), TaskAssignment, TaskCompletion.
- Invariants: HumanTask MUST have assignee and deadline (workflow_orchestration.inv.5).
- Triggers: task_assigned, task_overdue, task_completed.
- RULE: Workflow steps may require human action. Define HumanTask with form/input requirements. Assign to user or role. Track deadline. Escalate overdue tasks. Capture completion with input validation. Resume workflow on completion.

## p7: Compensation and Rollback
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: workflow
category: other
```

- Primitives: CompensatingAction (for_step, action), CompensationChain.
- Invariants: If workflow fails after side effects, compensations MUST execute (workflow_orchestration.inv.6).
- Triggers: compensation_triggered, compensation_failed.
- RULE: For each step with side effects, define CompensatingAction. On workflow failure, execute compensations in reverse order. Handle compensation failures (escalate, retry). Extends temporal.p3 (Saga) for workflow context.

## p8: Workflow Versioning
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: workflow
category: other
```

- Primitives: WorkflowVersion (major, minor, migration_path), VersionCompatibility.
- Invariants: Running instances MUST complete on their original version or migrate safely (workflow_orchestration.inv.7).
- Triggers: version_mismatch, migration_required.
- RULE: Version workflows. Running instances retain their version. New instances use latest. Define migration paths for in-flight instances if needed. Breaking changes require new major version.

## p9: Timeout and Deadline
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: workflow
category: other
```

- Primitives: WorkflowTimeout, StepTimeout, EscalationPolicy.
- Invariants: Timeout MUST trigger defined action (fail, escalate, skip) (workflow_orchestration.inv.8).
- Triggers: workflow_timeout, step_timeout.
- RULE: Define timeouts at workflow and step level. On timeout: fail step/workflow, escalate to human, or skip step. Different timeout values for different step types. Extends temporal.p2.

## p10: Workflow Observability
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: workflow
category: other
```

- Primitives: WorkflowTrace (instance_id, step_history, timing), WorkflowMetrics.
- Triggers: workflow_slow, bottleneck_detected.
- RULE: Trace workflow execution with timestamps. Measure: duration per step, total duration, wait times. Identify bottlenecks. Integrate with obs.p1 (TraceId). Provide visual workflow execution view.

## p11: Subworkflow Invocation
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: workflow
category: other
```

- Primitives: SubworkflowCall (workflow_id, inputs), SubworkflowReturn (outputs, status).
- Invariants: Subworkflow failure MUST be handled by parent workflow (workflow_orchestration.inv.9).
- Triggers: subworkflow_failed, subworkflow_timeout.
- RULE: Workflows may invoke other workflows. Pass inputs, receive outputs. Handle subworkflow failure: retry, fail parent, or compensate. Avoid deep nesting. Track parent-child relationship for tracing.

## p12: Event-Driven Workflow
```yaml
triggers: []
requires_primitives: [Entity, Authority]
output_type: constraint
domain: workflow
category: other
```

- Primitives: WorkflowTrigger (event_type, filter), EventWait (event_type, timeout, correlation).
- Triggers: event_received, event_timeout.
- RULE: Workflows may be triggered by events. Steps may wait for external events (EventWait). Define correlation to match events to instances. Handle event timeout. Use with messaging.p7 (Pub/Sub).
