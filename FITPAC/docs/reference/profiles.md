---
title: FITPAC profiles
status: informative
---

# Profiles and bundles

This document describes **pattern bundles and retrieval profiles** used by implementations to shape which parts of the pattern library are consulted by default. The **normative definition of FITPAC Profiles** (including conformance criteria and machine‑readable schema) is in **RFC‑0002: FITPAC Profile Specification**; readers should treat that RFC as the source of truth whenever the term “FITPAC Profile” is used in a standards or compliance context.

In this document, “profiles” are **implementation‑level bundles**: they help tools choose *which* modules and invariants to emphasize, but they:

- do **not** change pattern semantics,
- do **not** alter the FITPAC core or control grammar, and
- MUST NOT be treated as FITPAC Profiles unless they also satisfy RFC‑0002.

## 1. Concept (implementation‑level bundles)

An implementation‑level **bundle profile** is:

- a name (e.g. `high_trust_backend_saas`, `consumer_web_app`, `safety_critical_ml`),
- a set of included modules and optional rule subsets, and
- a set of required invariants and additional local constraints for retrieval and emphasis.

Bundles are declarative; they do not change pattern semantics, only which patterns and invariants are considered **in‑scope** for a given project or run.

> **Relationship to RFC‑0002:** A bundle MAY be wrapped or interpreted as a FITPAC Profile when it also satisfies the “profiles tighten; they do not loosen” rule, deterministic precedence, ambiguity protocol preservation, and round‑trip requirements in RFC‑0002. When used that way, the bundle’s configuration SHOULD be expressed using the machine‑readable schema in RFC‑0002 §6.

## 2. Bundle schema (informative)

Implementations MAY express these bundles in YAML or JSON using the following **informative** schema:

```yaml
id: high_trust_backend_saas          # stable identifier (implementation-level bundle)
label: High‑trust backend SaaS       # human‑readable name
description: >
  Bundle optimized for multi‑tenant, security‑sensitive backend services
  with strong invariants on authorization, auditing, and data isolation.

modules:
  include:
    - security
    - ontology
    - boundaries
    - satisfaction
    - temporal
    - obs
    - budgets
    - governance
  optional:
    - ml_ai_systems
    - messaging

rules:
  include: []                         # optional: explicit `module.pN` selectors
  exclude: []                         # optional: rules to omit from otherwise included modules

invariants:
  required:
    - security.inv.1
    - temporal.inv.1
  optional:
    - privacy_data_protection.inv.1

indexes:
  preferred_keys:
    - module
    - triggers
    - requires_primitives
    - domain
    - category
  notes: >
    Implementations SHOULD prioritize indexes that make security and ontology
    rules cheap to retrieve and evaluate.
```

Implementations MAY extend this schema with additional fields, but MUST NOT change the meaning of existing keys when the same bundle is also used as input to a FITPAC Profile defined per RFC‑0002.

**Invariant IDs:** The example invariant IDs in the schema use canonical module keys from `pattern_map` (e.g. `security.inv.1`, `temporal.inv.1`, `privacy_data_protection.inv.1`). Use IDs that are actually defined in the pattern modules (e.g. in `patterns/security_trust.md`, `patterns/temporal.md`); there is no single global registry. See [pattern-index.md](pattern-index.md) for how invariant identifiers are attached to modules.

## 3. Example profiles

- `high_trust_backend_saas`
  - Emphasizes `security`, `ontology`, `boundaries`, `temporal`, `governance`.
  - Requires strong invariants around authorization, auditing, and tenant isolation.
- `consumer_web_app`
  - Emphasizes `ux`, `performance`, `accessibility`, `budgets`, `obs`.
  - May treat some deep resilience and governance invariants as optional.
- `safety_critical_ml`
  - Emphasizes `ml_ai_systems`, `evidence_harness`, `schema_evolve`, `temporal`.
  - Requires invariants around data lineage, rollback, and evidence collection.

## 4. Profiles and agents

Agents and tools SHOULD:

- Ask for or infer a profile at project creation time (see [Getting started](../getting-started.md)).
- Use the profile or bundle to:
  - limit which pattern modules are consulted by default,
  - bias retrieval toward modules and invariants listed as `required`,
  - configure indexing and caching strategies (e.g. pre‑load security and ontology rules in high‑trust profiles).

When operating as **FITPAC Profiles** per RFC‑0002, configurations MUST follow the “profiles tighten; they do not loosen” rule, use a deterministic precedence hierarchy, and preserve the ambiguity protocol and round‑trip semantics. Experimental or non‑tightening profiles MUST be clearly labeled and surfaced in audit logs as described in RFC‑0002.

Implementation‑level bundles described in this document remain **advisory**, not binding: humans and agents MAY temporarily consult patterns outside the active bundle or profile, but SHOULD make such escapes explicit (e.g. \"consulting `ml_ai_systems` outside current profile\").

