#!/usr/bin/env python3
"""
Resolve fitpac.prose_compiler extension paths for prose→primitives consumers (RFC-0006 §6.1).

Usage:
  python3 FITPAC/tools/fitpac_prose_compiler_context.py [--repo-root PATH] [--json]

Prints pack root, pattern module path, pipeline fragment ids, manifest path, and
default compiler profile id. Paths are relative to FITPAC/ unless --repo-root is set.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]


def _repo_root(explicit: Path | None) -> Path:
    if explicit is not None:
        return explicit.resolve()
    # FITPAC/tools/ -> repo root is parent of FITPAC/
    fitpac_dir = Path(__file__).resolve().parent.parent
    return fitpac_dir.parent


def resolve(fitpac_root: Path, repo_root: Path) -> dict[str, object]:
    if not yaml:
        raise RuntimeError("PyYAML required: pip install pyyaml")

    core_manifest = yaml.safe_load((repo_root / "FITPAC" / "fitpac_manifest.yaml").read_text())
    ext_entry = next(
        (e for e in (core_manifest.get("extensions") or []) if e.get("id") == "fitpac.prose_compiler"),
        None,
    )
    if not ext_entry:
        raise FileNotFoundError("fitpac.prose_compiler not registered in FITPAC/fitpac_manifest.yaml extensions")

    pack_manifest_rel = ext_entry["manifest"]
    pack_manifest_path = repo_root / pack_manifest_rel
    pack_root = pack_manifest_path.parent
    pack_manifest = yaml.safe_load(pack_manifest_path.read_text(encoding="utf-8"))

    registry = yaml.safe_load((fitpac_root / "extensions" / "extension_registry.yaml").read_text())
    prose = (registry.get("extensions") or {}).get("fitpac.prose_compiler") or {}

    master_index = yaml.safe_load((fitpac_root / "master_index.yaml").read_text())
    pattern_rel = (master_index.get("pattern_map") or {}).get("fitpac.prose_compiler")
    if not pattern_rel:
        raise KeyError("pattern_map.fitpac.prose_compiler missing from master_index.yaml")

    return {
        "extension_id": "fitpac.prose_compiler",
        "semver": ext_entry.get("semver") or prose.get("semver"),
        "pack_root": str(pack_root.relative_to(repo_root)),
        "pack_manifest": str((pack_root / "fitpac_prose_compiler_manifest.yaml").relative_to(repo_root)),
        "pattern_module": str((fitpac_root / pattern_rel).relative_to(repo_root)),
        "pattern_module_fitpac_relative": pattern_rel,
        "pipeline_fragments": prose.get("pipeline_fragments") or [
            f"fitpac.prose_compiler.p{i}" for i in range(1, 7)
        ],
        "default_compiler_profile_id": prose.get("default_compiler_profile_id")
        or "fitpac.prose_compiler.compiler_profile_v0",
        "schema_dir": str(
            (pack_root / "docs/reference/fitpac_prose_compiler/schema").relative_to(repo_root)
        ),
        "inventory_dir": str(
            (pack_root / "docs/reference/fitpac_prose_compiler/data/v0.1.0").relative_to(repo_root)
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve fitpac.prose_compiler paths for consumers.")
    parser.add_argument("--repo-root", type=Path, default=None, help="Repository root (default: parent of FITPAC/)")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()
    repo = _repo_root(args.repo_root)
    fitpac_root = repo / "FITPAC"
    try:
        ctx = resolve(fitpac_root, repo)
    except (FileNotFoundError, KeyError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(ctx, indent=2))
    else:
        for key, val in ctx.items():
            if isinstance(val, list):
                print(f"{key}:")
                for item in val:
                    print(f"  - {item}")
            else:
                print(f"{key}: {val}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
