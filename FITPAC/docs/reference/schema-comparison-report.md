# RFC and `master_index.yaml` Schema Comparison Report

**Purpose:** Compare the audit/consultation schema required by the RFCs with the schema defined in `master_index.yaml` and emitted by `FITPAC/tools/generate_master_index.py`. No changes were made; this is a findings report for a follow-up decision.

---

## 1. RFC Requirements (RFC-0004 §7, RFC-0001 §8)

### Consultation event / audit log (normative)

Implementations **MUST** include:

- `inflection_point`
- `ambiguity_type`
- `trigger_rule`
- `fragment_loaded`
- `resolution_applied`
- `resolution_result`
- `confidence_before`
- `confidence_after`
- `contributing_factors`
- **A reasoning field** that captures at least:
  - the trigger condition(s) observed
  - fragment IDs consulted
  - the chosen resolution
  - a brief justification for why alternatives were rejected when applicable
  - links or references to evidentiary artifacts when those inform the decision

Reasoning MUST be human-readable; event header/channel name is implementation- or profile-defined.

---

## 2. master_index.yaml and Generator Schema

### audit_log.entry_schema (current)

- `timestamp`
- `session_id`
- `inflection_point`
- `ambiguity_type`
- `trigger_rule`
- `fragment_loaded`
- `resolution_applied`
- `resolution_result`
- `confidence_before`
- `confidence_after`
- `tokens_loaded_estimate`
- `contributing_factors`

**Missing:** There is **no** `reasoning` (or equivalent) field in `audit_log.entry_schema`. The rules section says "Reasoning MUST be in plain English" but the schema does not define a field for it.

### telemetry.report_format.fields (current)

Includes `reasoning_delta`: "Plain English. What changed in the decision space after consulting the pattern?"

- **Semantics differ from RFC:** `reasoning_delta` describes *what changed* after consultation. The RFC requires a reasoning field that captures *trigger conditions, fragments consulted, resolution, justification for alternatives rejected, and references to evidence*. So `reasoning_delta` is a subset or different angle, not a direct implementation of the required reasoning payload.

---

## 3. generate_master_index.py

- **Location:** `FITPAC/tools/generate_master_index.py`
- **Role:** Builds `pattern_map`, `precedence_hierarchy`, and `ambiguity_triggers` from the pattern tree; embeds **hardcoded** `confidence_model`, `consultation_protocol`, `telemetry`, and `audit_log` via `get_embedded_defaults()` (lines 262–366).
- **Primitive spine:** The script excludes `00_primitive_spine.md` when scanning the patterns directory (line 241: `rel.name == "00_primitive_spine.md" or rel.parts[0] == "00_primitive_spine.md"`).
- **Audit schema:** The embedded `audit_log.entry_schema` in `get_embedded_defaults()` matches the current `master_index.yaml`: it does **not** include a `reasoning` field. So any regenerated `master_index.yaml` will continue to omit the RFC-required reasoning field unless the script is updated.

---

## 4. Which Schema Is Better?

| Criterion | RFC | master_index.yaml / generator |
|----------|-----|-------------------------------|
| **Authority** | Normative; defines conformance. | Implementation/default; must satisfy RFC. |
| **Reasoning** | Explicit requirement for a single reasoning field with minimum semantics (trigger, fragments, resolution, justification, evidence links). | No dedicated reasoning field in audit log; telemetry has `reasoning_delta` with narrower semantics. |
| **Completeness** | Lists required fields; implementations MAY add more. | Adds `timestamp`, `session_id`, `tokens_loaded_estimate`; omits required reasoning. |
| **Clarity** | High-level semantics; implementation-defined format/locale. | Concrete field names and types; good for tooling and parsing. |

**Conclusion:** The **RFC schema is better** for conformance and auditability because:

1. It explicitly requires a **reasoning** field with well-defined minimum semantics, which supports accountability and regulatory needs. The current `master_index.yaml`/generator schema does not expose this in the audit log entry schema.
2. Implementations can still add implementation-specific fields (e.g. `timestamp`, `session_id`, `tokens_loaded_estimate`) on top of the RFC-required set.
3. Aligning the manifest and generator with the RFC (e.g. adding a `reasoning` field to `audit_log.entry_schema` with semantics matching RFC-0004 §7) would make the default distribution conformant and avoid ambiguity for implementers.

**Recommendation:** Prefer the RFC as the source of truth. Update `master_index.yaml` and `generate_master_index.py`’s `get_embedded_defaults()` so that `audit_log.entry_schema` includes a `reasoning` field whose description matches the RFC’s minimum payload (trigger conditions observed, fragment IDs consulted, chosen resolution, justification for alternatives rejected, links/references to evidentiary artifacts). Optionally, keep `reasoning_delta` in telemetry for “what changed” and add `reasoning` in the audit log for the full required payload.
