# Contributing to FITPAC

FITPAC (Formal Intent Translation Protocol for Agentic Code) is an open standard. Contributions help evolve the protocol and documentation so implementers can build consistent, auditable agentic systems.

## Scope: Core repo vs. community patterns

This repository is the **FITPAC core** distribution. It contains:

- RFCs that define the FITPAC standard
- Core documentation (manuals, guides, white paper)
- Core FITPAC files (plain-English YAML) required to describe FITPAC-compliant specs
- A **minimum “bootstrap” set** of patterns required for baseline operation and examples

### Pattern contributions
We **encourage** pattern contributions, but **new community patterns are not accepted into this core repository**.

Instead, community pattern modules should be submitted to the **FITPAC Community Patterns** repository (maintained under the FITPAC umbrella):

- Community patterns repo: https://github.com/FITPAC/FITPAC-Community-Patterns

If you are unsure whether something belongs in core vs. community patterns, open an issue in this repo first and we will route it.

## License (required)

By submitting a pull request (PR) or other contribution to this repository, you agree that your contribution is licensed under the terms of the repository’s license: **Creative Commons Attribution 4.0 (CC-BY 4.0)**.

- Repository license: `LICENSE`
- CC-BY 4.0: https://creativecommons.org/licenses/by/4.0/

You also confirm that you have the necessary rights to grant this license for your contribution.

## DCO / CLA stance

No additional DCO or CLA is required beyond the CC-BY 4.0 license grant in the License section above.

## How contributions are organized (normative vs informative)

FITPAC distinguishes between:

- **RFCs (normative standards):** protocol requirements and conformance surfaces.
- **Normative references (non-RFC artifacts):** concrete files that RFCs may explicitly require for conformance.
- **Informative documentation:** guides and explanations that may recommend behavior but do not, by themselves, add conformance requirements.

In case of conflict, **RFC text is authoritative**.

## Contribution workflow

### 1. Decide what you’re changing

Use these buckets to keep review efficient:

- **Protocol change (normative):** add a new RFC (or a versioned amendment).
- **Docs improvement (informative):** update guides under `docs/**` or root documentation.
- **Core maintenance:** small fixes to core YAML files or tooling used to rebuild essential artifacts.

> Note: New pattern modules should go to the community patterns repository, not this repo.

### 2. Open an issue before drafting (recommended)

For proposals that might change the standard, please open an issue to:
- summarize the change,
- state whether it is additive or breaking, and
- list impacted modules/files.

### 3. For RFCs: follow the RFC lifecycle

FITPAC RFCs live in `rfcs/` (or the root, depending on repo layout). If an RFC lifecycle document exists, follow it; otherwise open an issue describing the change.

## Pull request checklist

Before submitting a PR, please ensure:
- You link the PR to an issue (if you opened one).
- You indicate whether the change is:
  - **normative** (RFC/protocol) or
  - **informative** (docs/guides) or
  - **core maintenance**
- You include a brief rationale for why the change is needed.
- You confirm your change respects CC-BY 4.0 licensing expectations (see License section above).

## Maintainer review

This repository is currently maintained by **Paul Roy**.

The maintainer may request revisions, ask for additional details, or suggest moving a contribution to the community patterns repository if it falls outside the scope of the core distribution.