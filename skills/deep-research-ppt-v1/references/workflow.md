# Workflow

## Inputs
- `ppt_job.json`
- research query/topic
- optional user attachments

## Defaults
- `slide_count=2`
- `style_template=scientific`
- `locale=zh-CN`
- `image_model=banana_pro`

## Quality Gates
1. Research gate:
- At least 2 relevant sources per slide intent
- Include numeric facts and at least 1 concrete example

2. Plan gate:
- `steps.length == slide_count`
- each step has non-empty `title` and `description`

3. Content gate:
- every slide has printable text, not placeholders

4. Rendering gate:
- image count equals slide count
- PDF exists and page count equals slide count

## Execution Skeleton
1. Build `workspace/ppt_job.json`.
2. Produce `workspace/research_notes.md`.
3. Produce `workspace/ppt_plan.json`.
4. Normalize plan with `scripts/normalize_plan.py`.
5. Produce `workspace/slides_payload.json`.
6. Render with `scripts/render_images_pdf.py`.
7. Verify with `scripts/verify_outputs.py`.

## Notes
- Keep source citations in slide research files.
- Do not generate PPTX in V1.
