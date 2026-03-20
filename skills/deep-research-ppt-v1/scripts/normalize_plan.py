#!/usr/bin/env python3
"""Normalize and validate PPT plan structure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ALLOWED_SLIDE_COUNTS = {2, 5, 8}
REQUIRED_ROOT_KEYS = {"title", "ppt_style", "steps"}
REQUIRED_STEP_KEYS = {"title", "description", "need_search", "step_type"}


def _fail(message: str) -> None:
    raise ValueError(message)


def normalize_plan(plan: dict, slide_count: int) -> dict:
    if slide_count not in ALLOWED_SLIDE_COUNTS:
        _fail(f"slide_count must be one of {sorted(ALLOWED_SLIDE_COUNTS)}, got {slide_count}")

    missing = REQUIRED_ROOT_KEYS - set(plan.keys())
    if missing:
        _fail(f"plan missing required keys: {sorted(missing)}")

    title = str(plan.get("title", "")).strip()
    ppt_style = str(plan.get("ppt_style", "")).strip()
    steps = plan.get("steps")

    if not title:
        _fail("plan.title must be non-empty")
    if not ppt_style:
        _fail("plan.ppt_style must be non-empty")
    if not isinstance(steps, list):
        _fail("plan.steps must be an array")
    if len(steps) != slide_count:
        _fail(f"plan.steps length {len(steps)} does not match expected slide_count {slide_count}")

    normalized_steps = []
    for idx, step in enumerate(steps, start=1):
        if not isinstance(step, dict):
            _fail(f"step {idx} must be an object")
        step_missing = REQUIRED_STEP_KEYS - set(step.keys())
        if step_missing:
            _fail(f"step {idx} missing keys: {sorted(step_missing)}")

        step_title = str(step.get("title", "")).strip()
        desc = str(step.get("description", "")).strip()
        need_search = bool(step.get("need_search"))
        step_type = str(step.get("step_type", "")).strip()

        if not step_title:
            _fail(f"step {idx}.title must be non-empty")
        if not desc:
            _fail(f"step {idx}.description must be non-empty")
        if step_type != "research":
            _fail(f"step {idx}.step_type must be 'research', got '{step_type}'")

        normalized_steps.append(
            {
                "title": step_title,
                "description": desc,
                "need_search": need_search,
                "step_type": "research",
            }
        )

    return {
        "title": title,
        "ppt_style": ppt_style,
        "steps": normalized_steps,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize PPT plan")
    parser.add_argument("--input", required=True, help="Path to raw ppt_plan.json")
    parser.add_argument("--output", required=True, help="Path to normalized output")
    parser.add_argument("--slide-count", type=int, required=True, help="Expected slide count")
    args = parser.parse_args()

    in_path = Path(args.input).resolve()
    out_path = Path(args.output).resolve()

    with in_path.open("r", encoding="utf-8") as f:
        plan = json.load(f)

    normalized = normalize_plan(plan, args.slide_count)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(normalized, f, ensure_ascii=False, indent=2)

    print(f"Normalized plan written to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
