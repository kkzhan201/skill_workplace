#!/usr/bin/env python3
"""Path detection helpers for deep-research-ppt-v1."""

from __future__ import annotations

import os
from pathlib import Path


DEFAULT_DEERFLOW_ROOT = Path(
    "/Users/ninihkgai/Desktop/KK_HKGAI/df_gemini/deerflow_Allinone"
)


def _resolve_existing(path: str | None) -> Path | None:
    if not path:
        return None
    p = Path(path).expanduser().resolve()
    return p if p.exists() else None


def _detect_deerflow_root() -> Path:
    env_root = _resolve_existing(os.getenv("DEERFLOW_ROOT"))
    if env_root and (env_root / "src" / "ppt" / "presentation_builder.py").exists():
        return env_root

    cwd = Path.cwd().resolve()
    if (cwd / "src" / "ppt" / "presentation_builder.py").exists():
        return cwd

    for parent in Path(__file__).resolve().parents:
        if (parent / "src" / "ppt" / "presentation_builder.py").exists():
            return parent

    if (DEFAULT_DEERFLOW_ROOT / "src" / "ppt" / "presentation_builder.py").exists():
        return DEFAULT_DEERFLOW_ROOT

    raise FileNotFoundError(
        "Cannot locate deerflow root. Set DEERFLOW_ROOT to a directory containing "
        "src/ppt/presentation_builder.py"
    )


def detect_paths() -> dict[str, str]:
    skills_root = _resolve_existing(os.getenv("SKILLS_ROOT"))
    workspace_root = _resolve_existing(os.getenv("WORKSPACE_ROOT"))
    outputs_root = _resolve_existing(os.getenv("OUTPUTS_ROOT"))

    if not skills_root and Path("/mnt/skills").exists():
        skills_root = Path("/mnt/skills")
    if not workspace_root and Path("/mnt/user-data/workspace").exists():
        workspace_root = Path("/mnt/user-data/workspace")
    if not outputs_root and Path("/mnt/user-data/outputs").exists():
        outputs_root = Path("/mnt/user-data/outputs")

    if not workspace_root:
        workspace_root = Path.cwd() / ".skill-workspace"
    if not outputs_root:
        outputs_root = Path.cwd() / ".skill-outputs"

    workspace_root.mkdir(parents=True, exist_ok=True)
    outputs_root.mkdir(parents=True, exist_ok=True)

    return {
        "deerflow_root": str(_detect_deerflow_root()),
        "skills_root": str(skills_root) if skills_root else "",
        "workspace_root": str(workspace_root.resolve()),
        "outputs_root": str(outputs_root.resolve()),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(detect_paths(), ensure_ascii=False, indent=2))
