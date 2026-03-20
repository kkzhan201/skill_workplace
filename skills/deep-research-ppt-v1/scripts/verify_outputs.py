#!/usr/bin/env python3
"""Verify rendered outputs from manifest.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


REQUIRED_KEYS = {"status", "session_id", "slide_images", "pdf", "slide_count", "errors"}


def count_pdf_pages(pdf_path: Path) -> int:
    try:
        from pypdf import PdfReader  # type: ignore

        return len(PdfReader(str(pdf_path)).pages)
    except Exception:
        try:
            import fitz  # type: ignore

            with fitz.open(str(pdf_path)) as doc:
                return doc.page_count
        except Exception:
            data = pdf_path.read_bytes()
            count = data.count(b"/Type /Page")
            if count > 0:
                # Heuristic fallback: exclude the common /Pages object marker.
                pages_marker = data.count(b"/Type /Pages")
                adjusted = count - pages_marker
                return adjusted if adjusted > 0 else count
            raise RuntimeError(
                "Cannot count PDF pages; install pypdf or PyMuPDF (fitz) for strict validation"
            )


def verify(manifest: dict, expect_slides: int) -> None:
    missing = REQUIRED_KEYS - set(manifest.keys())
    if missing:
        raise ValueError(f"manifest missing keys: {sorted(missing)}")

    if manifest["status"] != "success":
        raise ValueError(f"manifest status is not success: {manifest.get('status')}")

    images = manifest["slide_images"]
    if not isinstance(images, list):
        raise ValueError("manifest.slide_images must be a list")
    if len(images) != expect_slides:
        raise ValueError(f"slide image count {len(images)} != expected {expect_slides}")
    if int(manifest.get("slide_count", -1)) != expect_slides:
        raise ValueError(f"slide_count {manifest.get('slide_count')} != expected {expect_slides}")

    for image_path in images:
        p = Path(image_path)
        if not p.exists():
            raise FileNotFoundError(f"missing slide image: {p}")
        if p.stat().st_size <= 0:
            raise ValueError(f"empty slide image: {p}")
        with Image.open(p) as img:
            w, h = img.size
            if w <= 0 or h <= 0:
                raise ValueError(f"invalid image dimensions: {p} => {w}x{h}")

    pdf_path = Path(manifest["pdf"])
    if not pdf_path.exists():
        raise FileNotFoundError(f"missing pdf: {pdf_path}")
    if pdf_path.stat().st_size <= 0:
        raise ValueError(f"empty pdf: {pdf_path}")

    pages = count_pdf_pages(pdf_path)
    if pages != expect_slides:
        raise ValueError(f"pdf pages {pages} != expected {expect_slides}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify manifest outputs")
    parser.add_argument("--manifest-file", required=True, help="Path to manifest.json")
    parser.add_argument("--expect-slides", type=int, required=True, help="Expected slides count")
    args = parser.parse_args()

    manifest_path = Path(args.manifest_file).resolve()
    with manifest_path.open("r", encoding="utf-8") as f:
        manifest = json.load(f)

    verify(manifest, args.expect_slides)
    print(f"Verification passed: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
