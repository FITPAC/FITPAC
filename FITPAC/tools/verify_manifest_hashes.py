#!/usr/bin/env python3
"""Verify SHA-256 pins in fitpac_manifest.yaml and extension manifests."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import yaml


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _check_list(root: Path, items: list[dict], label: str) -> list[str]:
    errors: list[str] = []
    for item in items:
        rel = item["path"]
        expected = item.get("sha256")
        path = root / rel
        if not path.is_file():
            errors.append(f"{label}: missing {rel}")
            continue
        if expected is None:
            continue
        actual = _sha256(path)
        if actual != expected:
            errors.append(f"{label}: hash mismatch {rel}")
    return errors


def verify_extension_pack(root: Path, manifest_rel: str) -> list[str]:
    manifest_path = root / manifest_rel
    if not manifest_path.is_file():
        return [f"extension manifest missing: {manifest_rel}"]
    data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    pack_root = manifest_path.parent
    errors: list[str] = []
    norm = data.get("normative_artifacts") or {}
    for section, items in norm.items():
        if not isinstance(items, list):
            continue
        errors.extend(_check_list(pack_root, items, f"fitpac.prose_compiler/{section}"))
    ext_manifest_hash = _sha256(manifest_path)
    return errors


def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    core_manifest_path = repo / "FITPAC" / "fitpac_manifest.yaml"
    if not core_manifest_path.is_file():
        print(f"Core manifest not found: {core_manifest_path}", file=sys.stderr)
        return 1

    core = yaml.safe_load(core_manifest_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    refs = core.get("normative_references") or {}
    for section, items in refs.items():
        if section == "extensions":
            continue
        if isinstance(items, list):
            errors.extend(_check_list(repo, items, f"core/{section}"))

    for ext in core.get("extensions") or []:
        manifest_rel = ext["manifest"]
        expected = ext.get("sha256")
        manifest_path = repo / manifest_rel
        if not manifest_path.is_file():
            errors.append(f"extensions: missing manifest {manifest_rel}")
            continue
        actual = _sha256(manifest_path)
        if expected and actual != expected:
            errors.append(f"extensions: manifest hash mismatch {manifest_rel}")
        errors.extend(verify_extension_pack(repo, manifest_rel))

    # Extension registry: pattern modules must exist
    registry_path = repo / "FITPAC" / "extensions" / "extension_registry.yaml"
    if registry_path.is_file() and yaml:
        reg = yaml.safe_load(registry_path.read_text(encoding="utf-8")) or {}
        fitpac_root = repo / "FITPAC"
        for ext_id, spec in (reg.get("extensions") or {}).items():
            for _mk, rel in (spec.get("pattern_map") or {}).items():
                p = fitpac_root / rel
                if not p.is_file():
                    errors.append(f"extension_registry/{ext_id}: missing pattern {rel}")
        for ext in core.get("extensions") or []:
            upstream = ext.get("manifest")
            if upstream and not (repo / upstream).is_file():
                errors.append(f"extensions: missing manifest path {upstream}")

    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    print("OK: all manifest hashes verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
