#!/usr/bin/env python3
"""
Generate FITPAC master_index.yaml from the pattern tree.

Recursively scans the patterns directory (including subdirectories), parses
pattern files for rule metadata, and emits a complete master_index.yaml with
pattern_map, precedence_hierarchy, and ambiguity_triggers. Supports path-based
namespacing and optional version segments (e.g. @1.0.0 in path or filename).

Usage:
  python tools/generate_master_index.py [--patterns-dir PATH] [--output PATH]
       [--precedence-override YAML] [--strict] [--verbose]

If master_index.yaml is missing, run this script to regenerate it from patterns.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]

# Default precedence order for known core modules (1 = highest).
# Unknown modules are appended after these in alphabetical order.
# This ordering encodes the Standard Reference Hierarchy described in RFC-0001
# and RFC-0002: safety, security, integrity, correctness, and regulatory
# compliance outrank ergonomics (UX), performance, and budgets.
KNOWN_PRECEDENCE_ORDER = [
    # Tier 1 – security and core correctness
    "security",
    "ontology",
    "containment",
    "boundaries",
    "governance",
    # Tier 2 – correctness and verification
    "satisfaction",
    "evidence_harness",
    "temporal",
    "spec_code_roundtrip",
    # Tier 3 – resilience, trust, and evolution
    "resilience",
    "deps_trust",
    "schema_evolve",
    # Tier 4 – compliance and audit
    "privacy_data_protection",
    "compliance_audit",
    "accessibility",
    # Tier 5 – operational and design
    "obs",
    "error_handling",
    "api_design",
    "messaging",
    "data_persistence",
    "networking",
    "distributed_systems",
    "configuration",
    # Tier 6 – lower-precedence concerns per RFC-0001
    "budgets",
    "ux",
    "performance",
    "deployment",
    # Tier 7 – domain-specific extensions
    "ml_ai_systems",
    "workflow_orchestration",
    "internationalization",
]

# Map from pattern filename (stem) to canonical module key for pattern_map.
# Used when discovery finds "security_trust.md" -> key "security", etc.
FILENAME_TO_MODULE_KEY: dict[str, str] = {
    "security_trust": "security",
    "domain_ontology": "ontology",
    "boundary_contracts": "boundaries",
    "satisfaction_goals": "satisfaction",
    "ui_ux": "ux",
}

# All trigger keys that must appear in ambiguity_triggers (seed).
AMBIGUITY_TRIGGER_KEYS = [
    "unknown_domain_term",
    "conflicting_mappings",
    "invalid_state_transition",
    "missing_invariant",
    "retry_instability",
    "partial_failure",
    "security_risk_detected",
    "privilege_escalation",
    "spec_ambiguity",
    "irreversible_action",
    "untyped_output_sink",
    "missing_boundary_manifest",
    "deadline_missed",
    "concurrent_conflict",
    "trace_correlation_needed",
    "budget_exceeded",
    "schema_version_mismatch",
    "dependency_unpinned",
    "circuit_open",
    "approval_required",
    "speculation_without_source",
    "falsification_loop",
    "fragment_outdated",
    "write_ownership_unspecified",
    "implicit_constraints_omitted",
    "transaction_boundary_uncertain",
    "clock_time_misuse",
    "resource_leak_risk",
    "tests_tautological_or_nondeterministic",
    "refactor_without_equivalence",
    "failed_test",
    "invariant_uncertain",
    "multi_valid_paths",
    "error_taxonomy_undefined",
    "partial_effect_uncertain",
]

# Default ambiguity_triggers (fragment lists) when we cannot infer from rules.
# Used when a trigger key has no matching rules; we keep a minimal default for known triggers.
DEFAULT_AMBIGUITY_TRIGGERS: dict[str, dict[str, Any]] = {
    "unknown_domain_term": {"patterns": ["ontology.p5", "ontology.p7"], "reason": "Term has no Ontology Mapping Contract."},
    "conflicting_mappings": {"patterns": ["ontology.p5", "ontology.p6"], "reason": "Same term maps differently across contexts."},
    "invalid_state_transition": {"patterns": ["ontology.p3", "satisfaction.p4"], "reason": "Event triggers undefined (State, Event) transition."},
    "missing_invariant": {"patterns": ["ontology.p4", "ontology.p7"], "reason": "Required invariant not found in Global Invariant Registry."},
    "retry_instability": {"patterns": ["boundaries.p2", "boundaries.p3", "boundaries.p4", "temporal.p1", "temporal.p5"], "reason": "Retry loop detected or idempotency key missing."},
    "partial_failure": {"patterns": ["boundaries.p5", "satisfaction.p2"], "reason": "Some dependencies failed; partial result detected."},
    "security_risk_detected": {"patterns": ["security.p1", "security.p2", "security.p5", "security.p6", "security.p7"], "reason": "Potential invariant violation, capability minting risk, SSRF, secrets, or unsafe deserialization."},
    "privilege_escalation": {"patterns": ["security.p3", "ontology.p2"], "reason": "Delegation chain depth exceeded or loop detected."},
    "spec_ambiguity": {"patterns": ["satisfaction.p1", "ontology.p7", "ontology.p8"], "reason": "Spec is ambiguous or underspecified."},
    "irreversible_action": {"patterns": ["ux.p1", "ux.p2"], "reason": "Action is irreversible; blast radius must be computed."},
    "untyped_output_sink": {"patterns": ["security.p4"], "reason": "Output sink has no declared encoder."},
    "missing_boundary_manifest": {"patterns": ["boundaries.p1"], "reason": "Boundary has no contract.yaml."},
    "deadline_missed": {"patterns": ["temporal.p2", "boundaries.p4"], "reason": "Operation exceeded propagated deadline."},
    "concurrent_conflict": {"patterns": ["temporal.p1", "temporal.p4"], "reason": "Race or duplicate write without idempotency key or lease."},
    "trace_correlation_needed": {"patterns": ["obs.p1", "obs.p3"], "reason": "Need to correlate failure across spans or boundaries."},
    "budget_exceeded": {"patterns": ["budgets.p1", "budgets.p2"], "reason": "Latency or cost over limit; or consult depth or iteration cap reached."},
    "schema_version_mismatch": {"patterns": ["schema_evolve.p1", "schema_evolve.p2", "schema_evolve.p3", "schema_evolve.p4"], "reason": "Client version unsupported or deprecated."},
    "dependency_unpinned": {"patterns": ["deps_trust.p1"], "reason": "Unpinned or untrusted dependency in use."},
    "circuit_open": {"patterns": ["resilience.p1"], "reason": "Circuit breaker open; dependency call skipped."},
    "approval_required": {"patterns": ["governance.p1", "ux.p1"], "reason": "Irreversible or high-risk action requires approval tier."},
    "speculation_without_source": {"patterns": ["containment.p1", "containment.p2"], "reason": "Claim or speculative content without provenance."},
    "falsification_loop": {"patterns": ["evidence_harness.p2"], "reason": "Falsification run; counterexample or property check."},
    "fragment_outdated": {"patterns": [], "reason": "Fragment deprecated or outdated; apply with reduced confidence and log."},
    "write_ownership_unspecified": {"patterns": ["ontology.p9"], "reason": "Resource has no explicit write owner; risk of split-brain or duplicate writes."},
    "implicit_constraints_omitted": {"patterns": ["ontology.p10", "temporal.p1"], "reason": "Idempotency, uniqueness, or ordering not declared."},
    "transaction_boundary_uncertain": {"patterns": ["temporal.p5"], "reason": "External I/O inside transaction or exactly-once semantics unclear."},
    "clock_time_misuse": {"patterns": ["temporal.p6"], "reason": "Local time, naive timestamps, or cross-service time comparison without contract."},
    "resource_leak_risk": {"patterns": ["temporal.p7", "resilience.p1"], "reason": "Unbounded concurrency or resources not closed/released."},
    "tests_tautological_or_nondeterministic": {"patterns": ["evidence_harness.p3", "evidence_harness.p4", "evidence_harness.p5"], "reason": "Tests mirror implementation, or rely on real time."},
    "refactor_without_equivalence": {"patterns": ["governance.p3"], "reason": "Large refactor without behavioral equivalence or delete-path plan."},
    "failed_test": {"patterns": ["evidence_harness.p1", "evidence_harness.p2", "satisfaction.p2"], "reason": "Test failed; consult scenario generation, falsification, and evidenced validation."},
    "invariant_uncertain": {"patterns": ["ontology.p4", "ontology.p7"], "reason": "Invariant applicability unclear; consult Global Invariant Registry and Spec Ambiguity Handling."},
    "multi_valid_paths": {"patterns": ["satisfaction.p1", "ontology.p7", "ontology.p8"], "reason": "Multiple valid implementation paths; consult goals and spec ambiguity/proposal."},
    "error_taxonomy_undefined": {"patterns": ["boundaries.p1", "boundaries.p2"], "reason": "Error taxonomy missing or unclear; consult boundary contract and error taxonomy."},
    "partial_effect_uncertain": {"patterns": ["boundaries.p5", "satisfaction.p2"], "reason": "Partial effect or side-effect outcome unclear."},
}


def normalize_module_key(segments: list[str]) -> str:
    """Build module key from path segments. Allow [A-Za-z0-9_.-] and @ for version."""
    key = ".".join(segments)
    # Collapse repeated dots, normalize slashes already joined
    key = re.sub(r"[^A-Za-z0-9_.@-]", ".", key)
    key = re.sub(r"\.+", ".", key).strip(".")
    return key or "unknown"


def derive_module_key(rel_path: Path, content: str) -> str:
    """
    Derive module key from relative path and optional frontmatter.
    Path: patterns/foo.md -> foo; patterns/bar/baz.md -> bar.baz;
    patterns/acme@1.0.0/security.md -> acme@1.0.0.security (if we keep @ in segment).
    """
    stem = rel_path.stem
    parts = list(rel_path.parts[:-1]) + [stem]
    # Optional YAML frontmatter at start of file: --- \\n module_key: xxx \\n version: yyy \\n ---
    if content.strip().startswith("---"):
        fm_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if fm_match:
            try:
                fm = yaml.safe_load(fm_match.group(1)) if yaml else None
                if isinstance(fm, dict):
                    if "module_key" in fm:
                        return str(fm["module_key"]).strip()
                    if "version" in fm:
                        version = str(fm["version"]).strip()
                        base = ".".join(parts) if len(parts) > 1 else stem
                        return f"{base}@{version}"
            except Exception:
                pass
    # Path-based: e.g. security_trust -> check if we want canonical key "security"
    if len(parts) == 1 and stem in FILENAME_TO_MODULE_KEY:
        return FILENAME_TO_MODULE_KEY[stem]
    return normalize_module_key(parts)


def parse_pattern_file(path: Path, content: str) -> list[dict[str, Any]]:
    """
    Parse a pattern file for ## pN: headers and following YAML block.
    Returns list of {"rule_id": "p3", "triggers": [...], "requires_primitives": [], ...}.
    """
    rules: list[dict[str, Any]] = []
    # Match ## pN: or ## pN : optional title
    rule_header = re.compile(r"^##\s+(p\d+)\s*:?\s*(.*)$", re.MULTILINE)
    yaml_fence = re.compile(r"^```(?:yaml)?\s*\n(.*?)\n```", re.MULTILINE | re.DOTALL)
    pos = 0
    while True:
        m = rule_header.search(content, pos)
        if not m:
            break
        rule_id = m.group(1)
        block_start = m.end()
        fence = yaml_fence.search(content, block_start)
        if not fence:
            pos = block_start
            continue
        yaml_str = fence.group(1).strip()
        try:
            meta = yaml.safe_load(yaml_str) if yaml else {}
        except Exception:
            meta = {}
        if not isinstance(meta, dict):
            meta = {}
        meta["rule_id"] = rule_id
        rules.append(meta)
        pos = fence.end()
    return rules


def discover_patterns(patterns_dir: Path) -> list[tuple[Path, str]]:
    """Return list of (relative_path, content) for each .md under patterns_dir."""
    results: list[tuple[Path, str]] = []
    for path in patterns_dir.rglob("*.md"):
        rel = path.relative_to(patterns_dir)
        if rel.name == "README.md":
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            content = ""
        results.append((rel, content))
    return results


def build_pattern_map_and_rules(
    patterns_dir: Path,
    patterns_base_rel: str,
    verbose: bool,
    strict: bool,
) -> tuple[dict[str, str], dict[str, list[dict[str, Any]]], list[str]]:
    """
    Discover all pattern files, parse rules, return (pattern_map, module_key -> rules, warnings).
    patterns_base_rel is the relative path from repo root to patterns dir (e.g. "patterns").
    """
    pattern_map: dict[str, str] = {}
    module_rules: dict[str, list[dict[str, Any]]] = {}
    warnings: list[str] = []

    for rel_path, content in discover_patterns(patterns_dir):
        module_key = derive_module_key(rel_path, content)
        file_path_str = f"{patterns_base_rel}/{rel_path.as_posix()}"
        if module_key in pattern_map and pattern_map[module_key] != file_path_str:
            warnings.append(f"Duplicate module key '{module_key}' for {file_path_str} (existing: {pattern_map[module_key]})")
        pattern_map[module_key] = file_path_str
        rules = parse_pattern_file(patterns_dir / rel_path, content)
        if not rules and verbose:
            warnings.append(f"No ## pN rules found in {rel_path}")
        for r in rules:
            rid = r.get("rule_id", "")
            if strict:
                for req in ("triggers", "requires_primitives", "output_type", "domain", "category"):
                    if req not in r or r[req] is None:
                        warnings.append(f"Missing required field '{req}' in {module_key} {rid}")
            # Normalize triggers to list of strings
            t = r.get("triggers")
            if isinstance(t, str):
                r["triggers"] = [t]
            elif not isinstance(t, list):
                r["triggers"] = []
        module_rules.setdefault(module_key, []).extend(rules)

    return pattern_map, module_rules, warnings


def build_precedence_hierarchy(
    pattern_map_keys: list[str],
    override_path: Path | None,
) -> dict[int, str]:
    """Build precedence_hierarchy: 1 = highest. Known order first, then unknown alphabetically."""
    rank = 1
    out: dict[int, str] = {}
    known_set = set(KNOWN_PRECEDENCE_ORDER)
    if override_path and override_path.exists():
        try:
            with open(override_path, encoding="utf-8") as f:
                data = yaml.safe_load(f) if yaml else {}
            ph = data.get("precedence_hierarchy") or data.get("precedence") or {}
            if isinstance(ph, dict):
                for k, v in sorted(ph.items(), key=lambda x: (int(x[0]) if str(x[0]).isdigit() else 999, x[0])):
                    out[rank] = str(v).strip()
                    rank += 1
                return out
        except Exception:
            pass
    for key in KNOWN_PRECEDENCE_ORDER:
        if key in pattern_map_keys:
            out[rank] = key
            rank += 1
    unknown = sorted([k for k in pattern_map_keys if k not in known_set])
    for key in unknown:
        out[rank] = key
        rank += 1
    return out


def build_ambiguity_triggers(
    module_rules: dict[str, list[dict[str, Any]]],
    precedence_rank: dict[str, int],
    pattern_map: dict[str, str],
    max_fragments_per_trigger: int = 8,
) -> dict[str, dict[str, Any]]:
    """
    For each trigger key, build list of fragments (module.pN) from rules that list that trigger.
    Sort by precedence (lower rank first) then by rule number; cap at max_fragments_per_trigger.
    """
    # Invert: trigger_key -> [(module_key, rule_id), ...] with precedence
    trigger_to_fragments: dict[str, list[tuple[int, str, str]]] = {k: [] for k in AMBIGUITY_TRIGGER_KEYS}
    for module_key, rules in module_rules.items():
        rank = precedence_rank.get(module_key, 999)
        for r in rules:
            triggers = r.get("triggers") or []
            rule_id = r.get("rule_id", "")
            if not rule_id:
                continue
            frag = f"{module_key}.{rule_id}"
            for t in triggers:
                t_str = t if isinstance(t, str) else str(t)
                if t_str in trigger_to_fragments:
                    trigger_to_fragments[t_str].append((rank, module_key, frag))
    out: dict[str, dict[str, Any]] = {}
    for key in AMBIGUITY_TRIGGER_KEYS:
        candidates = trigger_to_fragments.get(key, [])
        candidates.sort(key=lambda x: (x[0], x[2]))
        fragments = [c[2] for c in candidates[:max_fragments_per_trigger]]
        default = DEFAULT_AMBIGUITY_TRIGGERS.get(key, {"patterns": [], "reason": "No matching fragments found; consult pattern library."})
        if fragments:
            out[key] = {"patterns": fragments, "reason": default.get("reason", "Condition detected; load listed fragments.")}
        else:
            out[key] = {"patterns": default.get("patterns", []), "reason": default.get("reason", "No matching fragments; proceed with reduced confidence.")}
    return out


def get_embedded_defaults() -> dict[str, Any]:
    """Return the full confidence_model, consultation_protocol, telemetry, audit_log to embed."""
    return {
        "confidence_model": {
            "baseline": 0.95,
            "drop_conditions": {
                "unknown_domain_term": -0.25,
                "failed_test": -0.30,
                "invariant_uncertain": -0.40,
                "multi_valid_paths": -0.20,
                "error_taxonomy_undefined": -0.20,
                "retry_instability": -0.25,
                "partial_effect_uncertain": -0.20,
                "security_risk_detected": -0.40,
                "invalid_state_transition": -0.35,
                "missing_boundary_manifest": -0.20,
                "deadline_missed": -0.25,
                "concurrent_conflict": -0.30,
                "budget_exceeded": -0.20,
                "dependency_unpinned": -0.35,
                "circuit_open": -0.20,
                "speculation_without_source": -0.25,
                "write_ownership_unspecified": -0.25,
                "implicit_constraints_omitted": -0.25,
                "transaction_boundary_uncertain": -0.30,
                "clock_time_misuse": -0.20,
                "resource_leak_risk": -0.25,
                "tests_tautological_or_nondeterministic": -0.20,
                "refactor_without_equivalence": -0.20,
                "spec_ambiguity": -0.25,
                "conflicting_mappings": -0.25,
                "privilege_escalation": -0.35,
                "irreversible_action": -0.30,
                "trace_correlation_needed": -0.20,
                "approval_required": -0.25,
                "falsification_loop": -0.20,
                "fragment_outdated": -0.20,
                "missing_invariant": -0.30,
                "partial_failure": -0.20,
                "untyped_output_sink": -0.25,
                "schema_version_mismatch": -0.25,
            },
            "consult_threshold": 0.90,
            "recheck_after_resolution": True,
        },
        "consultation_protocol": {
            "trigger": [
                "Confidence drops at or below consult_threshold (0.90).",
                "Any test fails.",
                "An ambiguity_trigger condition is detected.",
                "An invariant violation is detected.",
                "Multiple equally valid implementation paths exist.",
            ],
            "steps": {
                1: "Compute confidence using drop_conditions.",
                2: "If confidence <= 0.90: enter Reference Mode.",
                3: "Classify the ambiguity using ambiguity_triggers.",
                4: "Load ONLY the fragments listed for that trigger.",
                5: "Apply the decision logic from the fragment.",
                6: "Emit a FITPAC_CONSULTATION_EVENT_V1 (see telemetry).",
                7: "Append the event to the audit log (see audit_log).",
                8: "Recheck confidence. If still <= 0.90: repeat from step 3.",
                9: "If unresolvable: emit SpecAmbiguityDetected or SpecProposal (ontology.p7).",
            },
            "minimal_loading_rule": [
                "Load only the fragment(s) listed in ambiguity_triggers.",
                "Do NOT load full pattern files.",
                "If a trigger maps to an empty fragment list, emit a consultation event and proceed with reduced confidence.",
            ],
        },
        "telemetry": {
            "consultation_required": True,
            "emit_on": ["ambiguity_detected", "invariant_violation", "test_failure", "multi_path_decision", "retry_instability", "security_risk"],
            "report_format": {
                "header": "FITPAC_CONSULTATION_EVENT_V1",
                "plain_english_required": "All reasoning fields MUST be in plain English for full auditability.",
                "fields": {
                    "inflection_point": "Plain English. What happened that reduced confidence?",
                    "ambiguity_type": "Which ambiguity_trigger matched?",
                    "trigger_rule": "Which key in ambiguity_triggers fired?",
                    "pattern_selected": "Which file and fragment?",
                    "fragment_loaded": "Exact section ID (e.g., boundaries.p4)",
                    "reasoning_delta": "Plain English. What changed in the decision space after consulting the pattern?",
                    "resolution_applied": "Plain English. What rule or fix was applied?",
                    "resolution_result": "Solved | Partial | Unsolved",
                    "confidence_before": "0.0–1.0",
                    "confidence_after": "0.0–1.0",
                    "tokens_loaded_estimate": "Rough token count of fragments loaded",
                    "contributing_factors": "Array of { condition: string, delta: float | null }.",
                },
            },
            "suppress_if": [
                "Confidence never dropped below threshold.",
                "No ambiguity trigger fired.",
                "No test failed.",
            ],
        },
        "audit_log": {
            "enabled": True,
            "file": ".fitpac_audit.jsonl",
            "format": "jsonl",
            "entry_schema": {
                "timestamp": "ISO 8601",
                "session_id": "Unique per agent session",
                "inflection_point": "Plain English. What happened that triggered consultation?",
                "ambiguity_type": "string",
                "trigger_rule": "string",
                "fragment_loaded": "string",
                "resolution_applied": "Plain English. What rule or fix was applied?",
                "resolution_result": "Solved | Partial | Unsolved",
                "confidence_before": "float",
                "confidence_after": "float",
                "tokens_loaded_estimate": "int",
                "contributing_factors": "Array of { condition: string, delta: float | null }.",
                "reasoning": "Plain English. MUST capture at least: trigger condition(s) observed, fragment IDs consulted, chosen resolution, brief justification for alternatives rejected when applicable, and links or references to evidentiary artifacts when those inform the decision (RFC-0004 §7).",
            },
            "rules": [
                "Append only. Never overwrite or delete entries.",
                "One JSON object per line.",
                "Emit one entry per consultation event.",
                "Reasoning MUST be in plain English.",
            ],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate FITPAC master_index.yaml from pattern tree.")
    script_dir = Path(__file__).resolve().parent
    fitpac_root = script_dir.parent
    default_patterns = fitpac_root / "patterns"
    default_output = fitpac_root / "master_index.yaml"
    parser.add_argument("--patterns-dir", type=Path, default=default_patterns, help="Path to patterns directory (default: FITPAC/patterns)")
    parser.add_argument("--output", type=Path, default=default_output, help="Output path for master_index.yaml")
    parser.add_argument("--precedence-override", type=Path, default=None, help="Optional YAML file with precedence_hierarchy or precedence mapping")
    parser.add_argument("--strict", action="store_true", help="Fail on missing required YAML fields or non-sequential rules")
    parser.add_argument("--verbose", action="store_true", help="Print warnings")
    args = parser.parse_args()

    if not yaml:
        print("PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
        return 1

    patterns_dir = args.patterns_dir.resolve()
    if not patterns_dir.is_dir():
        print(f"Patterns directory not found: {patterns_dir}", file=sys.stderr)
        return 1

    # Relative path from FITPAC root to patterns dir (for pattern_map values)
    try:
        patterns_base_rel = patterns_dir.relative_to(fitpac_root).as_posix()
    except ValueError:
        patterns_base_rel = "patterns"

    pattern_map, module_rules, warnings = build_pattern_map_and_rules(
        patterns_dir, patterns_base_rel, args.verbose, args.strict
    )
    if args.strict and warnings:
        for w in warnings:
            print(w, file=sys.stderr)
        return 1
    if args.verbose:
        for w in warnings:
            print("Warning:", w, file=sys.stderr)

    precedence_hierarchy = build_precedence_hierarchy(list(pattern_map.keys()), args.precedence_override)
    precedence_rank = {v: k for k, v in precedence_hierarchy.items()}
    ambiguity_triggers = build_ambiguity_triggers(module_rules, precedence_rank, pattern_map)
    defaults = get_embedded_defaults()

    out = {
        "precedence_hierarchy": precedence_hierarchy,
        "pattern_map": dict(sorted(pattern_map.items())),
        "confidence_model": defaults["confidence_model"],
        "ambiguity_triggers": ambiguity_triggers,
        "consultation_protocol": defaults["consultation_protocol"],
        "telemetry": defaults["telemetry"],
        "audit_log": defaults["audit_log"],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write("# ============================================================\n")
        f.write("# FITPAC Master Pattern Index (generated)\n")
        f.write("# ============================================================\n")
        f.write("# License: CC-BY-4.0\n")
        f.write("# License URL: https://creativecommons.org/licenses/by/4.0/\n")
        f.write("# Copyright Holder: Paul Roy and FITPAC Contributors\n")
        f.write("# Attribution Note: Attribution required under CC BY 4.0.\n")
        f.write("# PRECEDENCE: 1 = highest importance. When two patterns conflict, lower number wins.\n")
        f.write("# LOADING RULE: Load THIS file only. Fetch pattern fragments on demand.\n")
        f.write("# Regenerate with: python FITPAC/tools/generate_master_index.py\n")
        f.write("# ============================================================\n\n")
        yaml.dump(out, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=1000)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
