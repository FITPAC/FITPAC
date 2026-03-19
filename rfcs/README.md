# FITPAC RFC Index (Formal Standards)

This directory contains the **Formal Intent Translation Protocol for Agentic Code (FITPAC)** specifications. These documents define the normative requirements for FITPAC-conformant implementations. 

FITPAC follows a **formal standards process** to ensure that the protocol remains stable, versioned, and auditable as it evolves.

---

## Protocol Governance

### RFC Lifecycle
To ensure stability for implementers, every specification moves through these stages:
- **Draft:** Initial proposal; subject to breaking changes.
- **Proposed:** Stable for testing; open for community feedback.
- **Final:** The normative standard for the current version. Changes require a new RFC or a versioned amendment.

### Source of Truth
The **normative** versions of FITPAC are defined by the RFCs in this directory. Where an RFC and supporting documentation (e.g., a blog post or user manual) disagree, **the RFC is authoritative.**

The **`FITPAC/master_index.yaml`** acts as the runtime manifest of the standard. Implementations claiming FITPAC conformance MUST treat this (or an equivalent manifest per RFC-0004) as the authoritative entry point.

---

## Active RFCs

| RFC | Title | Status | Description |
|----|----|----|----|
| [RFC-0001](RFC-0001-FITPAC-1.0.0.md) | FITPAC 1.0.0 | **Final** | Core Protocol, Conformance, and Versioning. |
| [RFC-0002](RFC-0002-FITPAC-Profile-Specification.md) | Profile Specification | **Final** | Organizational value hierarchies. |
| [RFC-0003](RFC-0003-FITPAC-Primitives-and-Spec-Schema.md) | Primitives and Spec Schema | **Final** | The grammar of Intent (REQUIRE, RULE, EMIT). |
| [RFC-0004](RFC-0004-FITPAC-Master-Index-and-Consultation.md) | Master Index and Consultation | **Final** | Runtime logic and consultation protocol. |
| [RFC-0005](RFC-0005-FITPAC-Patterns-and-Triggers.md) | Patterns and Triggers | **Final** | Taxonomy of AI coding behaviors. |

---

## How to Contribute
FITPAC is an open standard. We welcome proposals for new pattern modules or protocol improvements.
1. **Review RFC-0001** for versioning and conformance rules.
2. **Open an Issue** to discuss your proposal before drafting.
3. **Submit a Pull Request** with a new RFC using the next available number.