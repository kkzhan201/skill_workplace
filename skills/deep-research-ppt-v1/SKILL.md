---
name: deep-research-ppt-v1
description: Use this skill when the user asks for a presentation that requires deep research before slide image generation. It performs multi-angle research, creates slide-level structure/content, generates slide images, and exports a final PDF deck.
---

# Deep Research PPT V1

## Overview
This skill implements a full research-to-slides workflow for Deerflow 1.0 style PPT generation. It focuses on deep research, structured 2/5/8-slide planning, slide image rendering, and final PDF output.

## Workflow Decision Tree
1. If the request is not about presentation generation, do not use this skill.
2. If the request is presentation-only without factual grounding, still run a lightweight research pass before planning.
3. If `ppt_job.json` does not exist, create it using the schema in `references/schemas/ppt_job.schema.json`.
4. If `slide_count` is not one of `2/5/8`, stop and return an error.
5. Run phases A-E in order. Do not skip normalization and output verification.

## Phase A: Deep Research
1. Use the same multi-angle process as deep research: broad scan, dimension split, deep dive per dimension, cross-check.
2. Produce concise notes in `workspace/research_notes.md`.
3. Ensure notes contain data points, real cases, and at least two source links per planned slide.
4. See `references/workflow.md` for quality gates.

## Phase B: PPT Planning
1. Read `references/ppt_planner.zh_CN.md` and generate `workspace/ppt_plan.json`.
2. The plan must include `title`, `ppt_style`, and `steps`.
3. Each step must include `title`, `description`, `need_search`, `step_type`.
4. Run:
```bash
python scripts/normalize_plan.py --input workspace/ppt_plan.json --output workspace/ppt_plan.normalized.json --slide-count 2
```

## Phase C: Slide Research Writing
1. Read `references/ppt_researcher.zh_CN.md`.
2. Generate one markdown file per slide under `workspace/slide_XX.research.md` with mandatory sections:
- `## Slide Title`
- `## Key Messages`
- `## Layout`
- `## Visual & Data Requirements`
- `## Source References`
3. Convert these files into `workspace/slides_payload.json`.

## Phase D: Image Prompt Assembly
1. Reuse deerflow1.0 prompt assembly logic: `global style + slide title + slide narrative + rendering requirements`.
2. Keep language aligned with chosen locale and style template.
3. Ensure each slide narrative is non-empty.

## Phase E: Render Images + PDF
Run:
```bash
python scripts/render_images_pdf.py --payload-file workspace/slides_payload.json --manifest-file outputs/manifest.json
```

Then verify:
```bash
python scripts/verify_outputs.py --manifest-file outputs/manifest.json --expect-slides 2
```

## Output Contract
1. Required deliverables:
- slide images (`slide_*.png`)
- one PDF (`presentation.pdf`)
- one manifest (`manifest.json`)
2. `manifest.json` format must follow `references/schemas/manifest.schema.json`.

## Failure Handling
1. If `GEMINI_API_KEY` is missing and model is `banana_pro`, fail fast with explicit error.
2. If plan step count mismatches expected slide count, fail in `normalize_plan.py`.
3. If any image or PDF is missing, fail in `verify_outputs.py`.
4. Always write `manifest.json` with `status=failed` and error details when rendering fails.
