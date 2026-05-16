from __future__ import annotations

from pathlib import Path


def pack_root(pack: str | Path) -> Path:
    p = Path(pack).resolve()
    if not p.is_dir():
        raise FileNotFoundError(p)
    return p


def schema_dir(pack: str | Path) -> Path:
    return pack_root(pack) / "docs" / "reference" / "fitpac_prose_compiler" / "schema"


def data_dir(pack: str | Path, version: str) -> Path:
    return pack_root(pack) / "docs" / "reference" / "fitpac_prose_compiler" / "data" / version


def binding_contract_path(pack: str | Path) -> Path:
    return (
        pack_root(pack)
        / "docs"
        / "reference"
        / "fitpac_prose_compiler"
        / "binding"
        / "binding_contract_v0.yaml"
    )


def profile_path(pack: str | Path, profile_id: str) -> Path:
    return (
        pack_root(pack)
        / "docs"
        / "reference"
        / "fitpac_prose_compiler"
        / "profiles"
        / f"{profile_id}.yaml"
    )
