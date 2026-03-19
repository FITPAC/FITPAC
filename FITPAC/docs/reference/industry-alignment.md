# Intent engineering and industry alignment

This page explains how FITPAC aligns with the problems and vocabulary used by industry experts working on **intent engineering** and the **intent gap** in enterprise AI.

## Intent gap and intent engineering

**Intent gap:** Without clear organizational intent, AI agents can optimize for measurable but wrong objectives—for example, reducing cost while damaging customer relationships. The gap is the mismatch between what the organization wants and what the agent does when intent is not made explicit and machine-readable.

**Intent engineering** is the discipline that follows prompt engineering and context engineering. It focuses on making **machine-readable organizational intent**: goal structures, delegation frameworks, escalation protocols, and feedback mechanisms so that agents act in line with organizational purpose. FITPAC implements intent engineering for agent-built software across three layers that match current industry framing.

## Three layers FITPAC addresses

### 1. Unified context infrastructure

The lack of standardized, accessible organizational knowledge for AI agents is a core problem. FITPAC provides:

- **`master_index.yaml`** — Entry point for coding agents (spec→code). It defines what to load, when (ambiguity triggers, confidence threshold), and where (pattern_map). Agents load this file first and fetch only the pattern fragments listed for the current trigger. This is the **unified context** entry point for the spec→code pipeline.
- **Prose→spec retrieval** — Implementations match user prose to patterns (triggers, category, output_type, domain in `patterns/*.md`) and load only relevant pattern bodies. Same organizational knowledge as spec→code, different retrieval path.
- **On-demand loading** — Entry points and triggers determine what gets loaded, reducing token use while keeping context standardized and vendor-agnostic.

FITPAC defines the *structure and governance* of context for agent-native development. The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) is a complementary standard for context *transport*; the two can be used together (e.g. exposing master_index and pattern fragments via MCP).

### 2. Coherent AI worker toolkit

Scaling individual AI workflows into cohesive organizational leverage requires a shared toolkit and protocol. FITPAC provides:

- **Two pipelines, one pattern set** — Prose→spec (orchestrator + Socratic LLM) and spec→code (coding agent) use the same pattern content and [primitive spine](../../00_primitive_spine.md). Only the retrieval mechanism differs (trigger index vs ambiguity_triggers).
- **Single consultation protocol** — Confidence model, trigger classification, load-only-listed-fragments, emit event (schema in `master_index.yaml`). Every workflow that adopts FITPAC behaves in a consistent, auditable way.
- **Precedence and categories** — When patterns conflict, the **value hierarchy** (precedence_hierarchy, as defined by `master_index.yaml`) and category ordering determine how the toolkit is applied.

**Organizational capability map:** Workflows can be classified as AI-ready, AI-augmented, or human-only based on which patterns and triggers apply. An organizational capability map can be derived from pattern coverage and trigger mapping—which workflows are fully spec-driven, which are partially assisted, and which remain human-only. FITPAC does not ship a separate capability-map artifact; the pattern set and master_index support defining or deriving one.

### 3. Intent engineering proper

Machine-readable expressions of organizational intent include goal structures, decision boundaries, escalation, value hierarchies, and feedback loops. FITPAC implements these as follows:

| Concept | FITPAC artifact or behavior |
|--------|----------------------------|
| **Goal translation** | Prose→spec pipeline: human objectives → agent-actionable structured spec. Primitives (Entity, Transformation, Constraint, Authority, Policy, etc.) and [satisfaction_goals](https://github.com/FITPAC/fitpac-patterns/blob/main/patterns/satisfaction_goals.md) (Goal, Trajectory, Evidenced Validation, Satisfaction Rubric) express goals in the spec schema. |
| **Decision boundaries** | When to act vs when to consult: [ambiguity_triggers](https://github.com/FITPAC/fitpac-patterns/blob/main/master_index.yaml) and confidence model (consult_threshold 0.90). [boundary_contracts](https://github.com/FITPAC/fitpac-patterns/blob/main/patterns/boundary_contracts.md): T1/T2/T3 error taxonomy, retry budget, partial-failure policy (fail-closed / fail-open / degrade). |
| **Escalation** | [SpecAmbiguityDetected](https://github.com/FITPAC/fitpac-patterns/blob/main/patterns/domain_ontology.md) and [SpecProposal](https://github.com/FITPAC/fitpac-patterns/blob/main/patterns/domain_ontology.md) (ontology p15, p16): agent stops and surfaces ambiguity or proposes a resolution for human decision. [Governance](https://github.com/FITPAC/fitpac-patterns/blob/main/patterns/governance.md): **approval tiers** (e.g. automated, human_approval, multi_party); "block and request escalation or approval" for irreversible actions. |
| **Value hierarchies** | [precedence_hierarchy](https://github.com/FITPAC/fitpac-patterns/blob/main/master_index.yaml): when two patterns conflict, **lower number wins** (1 = highest importance). Ordering is as defined by `master_index.yaml`. |
| **Feedback loops** | Round-trip (spec from prose vs spec extracted from code) and comparison are implementation-defined. **Consultation event schema** in `master_index.yaml`: what triggered, what was loaded, resolution, plain-English reasoning. Supports governance visibility and tuning. |

**Approval tiers and autonomy:** Governance defines approval tiers (automated, human_approval, multi_party). Together with SpecAmbiguityDetected/SpecProposal (agent stops for human input), FITPAC supports different levels of agent autonomy—from fully automated to human-in-the-loop—without a separate five-level autonomy model. Readers familiar with emerging work on operator / collaborator / consultant / approver / observer can map those concepts onto approval tiers and escalation behavior.

## Summary

FITPAC is a concrete implementation of intent engineering for agent-built software. It addresses the intent gap through:

1. **Unified context infrastructure** — Standardized, on-demand organizational knowledge (`master_index.yaml`; implementations may build prose→spec indexes from the pattern set).
2. **Coherent AI worker toolkit** — Shared patterns and consultation protocol across prose→spec and spec→code.
3. **Intent engineering proper** — Goal translation, decision boundaries, escalation, value hierarchies, and feedback loops expressed in the standard’s primitives, patterns, and audit trail.

For the main artifact list and usage, see the [README](https://github.com/FITPAC/fitpac-patterns/blob/main/README.md) and [Overview](../overview.md).
