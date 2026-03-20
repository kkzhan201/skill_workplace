#!/usr/bin/env python3
"""Render slide images and PDF using deerflow1.0 PPT pipeline."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from detect_paths import detect_paths  # noqa: E402


def _write_manifest(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def _load_payload(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    if not isinstance(payload, dict):
        raise ValueError("slides_payload must be an object")
    style_guide = str(payload.get("style_guide", "")).strip()
    slides = payload.get("slides")
    if not style_guide:
        raise ValueError("slides_payload.style_guide must be non-empty")
    if not isinstance(slides, list) or not slides:
        raise ValueError("slides_payload.slides must be a non-empty array")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Render images+pdf from slides payload")
    parser.add_argument("--payload-file", required=True, help="Path to slides_payload.json")
    parser.add_argument("--manifest-file", required=True, help="Path to output manifest.json")
    args = parser.parse_args()

    paths = detect_paths()
    deerflow_root = Path(paths["deerflow_root"]).resolve()
    outputs_root = Path(paths["outputs_root"]).resolve()

    if str(deerflow_root) not in sys.path:
        sys.path.insert(0, str(deerflow_root))

    payload_path = Path(args.payload_file).expanduser().resolve()
    manifest_path = Path(args.manifest_file).expanduser().resolve()

    manifest = {
        "status": "failed",
        "session_id": "",
        "slide_images": [],
        "pdf": "",
        "slide_count": 0,
        "errors": [],
    }

    try:
        payload = _load_payload(payload_path)
        slides = payload["slides"]
        image_model = str(payload.get("image_model", "banana_pro")).strip() or "banana_pro"

        if image_model == "banana_pro" and not os.getenv("GEMINI_API_KEY"):
            raise RuntimeError("GEMINI_API_KEY is required for image_model=banana_pro")

        from src.ppt.presentation_builder import SESSIONS_ROOT, create_ppt_presentation

        presentation = create_ppt_presentation(
            style_guide=payload["style_guide"],
            slides=slides,
            image_model=image_model,
        )

        session_id = presentation["session_id"]
        session_dir = Path(SESSIONS_ROOT) / session_id

        copied_images = []
        for idx, slide in enumerate(presentation["slides"], start=1):
            src = session_dir / slide["filename"]
            dst = outputs_root / f"{session_id}_slide_{idx:02d}.png"
            shutil.copy2(src, dst)
            copied_images.append(str(dst))

        src_pdf = session_dir / presentation["pdf_filename"]
        dst_pdf = outputs_root / f"{session_id}_presentation.pdf"
        shutil.copy2(src_pdf, dst_pdf)

        manifest.update(
            {
                "status": "success",
                "session_id": session_id,
                "slide_images": copied_images,
                "pdf": str(dst_pdf),
                "slide_count": len(copied_images),
                "errors": [],
            }
        )
    except Exception as exc:  # pylint: disable=broad-except
        manifest["errors"].append(str(exc))

    _write_manifest(manifest_path, manifest)

    if manifest["status"] != "success":
        print(f"Render failed. See {manifest_path}")
        return 1

    print(f"Render succeeded. Manifest written to {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
