# Overview

## Purpose

FITPAC assumes that correctness in software must be defined **externally** by behavior and outcomes, not by code structure. It provides an **ontology + protocol** that any agent stack can share:

- An **ontology**: primitives and pattern modules that describe entities, transformations, constraints, authorities, relations, context, time, boundaries, goals, and evidence.
- A **protocol**: how agents load that ontology on demand, how they resolve conflicts via a value hierarchy, and how they report decisions (event schema is defined in `master_index.yaml`; storage and policy are up to the implementation).

> **Here to actually use FITPAC in a project?**  
> Start with the three concrete workflows in `getting-started.md` (Zero → Spec, Audit, Pattern), then come back here when you want the conceptual model.

The library is **navigable by humans** and **efficient for agents**: entry points and triggers determine what gets loaded, reducing token use. Consultation semantics are defined in the master index; reasoning must be in **plain English** where the schema requires it.

FITPAC implements **intent engineering** for agent-built software—addressing the **intent gap** via unified context and machine-readable intent (goal translation, decision boundaries, escalation, value hierarchies). See [Intent engineering and industry alignment](reference/industry-alignment.md) for how FITPAC maps to industry terminology.

## Language and protocol

### Primitive spine (foundation)

The **primitive spine** (`00_primitive_spine.md` at the FITPAC root) is the foundation of the language: Layer 1 (Entity, Transformation, Constraint, Authority, Relation, Context, Time), Layer 2 (Transaction, Boundary, Projection, Capability, Policy), and core semantics. All patterns extend these primitives.

### Value hierarchy (precedence)

When two patterns conflict, **lower number wins**. Precedence **1 = highest importance**; the exact ordering is as defined by `master_index.yaml`.

### Consultation discipline

A **coding agent** loads `master_index.yaml`. When confidence drops at or below the consult threshold (0.90), or a test fails, or an ambiguity/invariant violation is detected, it enters **Reference Mode**: it classifies using `ambiguity_triggers`, loads only the listed pattern fragments from `pattern_map`, applies the pattern, and rechecks confidence. When multiple patterns conflict, the agent uses `precedence_hierarchy` (as defined by `master_index.yaml`) as the **single value hierarchy** for resolving conflicts.

Implementations may persist consultation events; FITPAC defines the **event schema** (see `master_index.yaml` under `telemetry` and `audit_log`) but not where or how events are stored.

## Why this is more than syntax

FITPAC is not a new programming language or a set of code snippets. It is a way to **describe everything a program does** in a form that both humans and agents can reason about:

- **State and ontology:** What entities exist, how they relate, and which states are legal (see `patterns/domain_ontology.md`).
- **Transformations and constraints:** What can change, under which conditions, and what invariants must never be violated.
- **Authority and governance:** Who is allowed to act, under what policies (see `patterns/security_trust.md`, `patterns/governance.md`).
- **Boundaries and time:** Where the system shares data or control with other systems, and how retries, deadlines, leases, and concurrency are handled (see `patterns/boundary_contracts.md`, `patterns/temporal.md`).
- **Goals and evidence:** What it means for the system to be successful, and how that success is measured (see `patterns/satisfaction_goals.md`, `patterns/evidence_harness.md`).

By organizing codebases and agent workflows around these primitives and patterns, teams gain a **single, shared language** for behavior that can survive rewrites, new agent stacks, and infrastructure changes.

## Key artifacts (in the repo)

| Artifact | Role |
|----------|------|
| `master_index.yaml` | Entry point for coding agents: precedence (value hierarchy), drop conditions, confidence model, ambiguity triggers, pattern map, consultation protocol, event schema. Can be regenerated from the pattern set using the generator in `tools/generate_master_index.py`. |
| `patterns/*.md` | Source of truth for pattern languages. |
| [Spec schema](reference/spec-schema.md) | Logical schema for specs (entities, invariants, boundaries, goals, control grammar). |
| [Prose to spec](guides/prose-to-spec.md), [Spec to code](guides/spec-to-code.md) | Guides for retrieval and consultation procedure. |
