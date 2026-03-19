---
name: html-pitch-deck
description: "Use when the user asks for a presentation, pitch deck, slide deck, PPT, 路演 deck, 匯報 slides, or product presentation that should be delivered as a single standalone HTML file with animation, interaction, and browser navigation. Prefer this skill when the deck is meant for presenting in a browser rather than editing in PowerPoint or Keynote. Do not use when the user explicitly requires a .pptx file or a corporate PPTX template."
---

# HTML Pitch Deck

## Overview

Create a single self-contained HTML presentation with strong visual polish, motion, and browser-first navigation.

Keep the main skill lean. Load the references only when needed:

- Read [references/brief-and-structure.md](references/brief-and-structure.md) when the brief is thin, when slide count is unclear, or when you need deck outlines and content-filling heuristics.
- Read [references/visual-system.md](references/visual-system.md) when building or revising the HTML, motion system, navigation, color palette, or component patterns.

## Workflow

1. Confirm delivery mode.
   If the user needs editable `.pptx` output, stop and switch to a PPTX-oriented skill instead of forcing HTML.

2. Clarify only the missing high-impact inputs.
   Ask concise plain-text questions only when the brief is materially underspecified. Prioritize:
   - product, project, or topic
   - audience
   - tone
   - slide count if it materially changes scope

   If the user already gave enough context, proceed. Reasonable defaults:
   - `4-6` slides
   - browser presentation, not file export to PPTX
   - formal or data-driven tone for business contexts

3. Plan the deck before writing code.
   Choose a structure from [references/brief-and-structure.md](references/brief-and-structure.md). If the user gave sparse content, expand it with credible supporting context rather than leaving empty slides.

4. Build one standalone HTML file.
   Requirements:
   - fixed `1280x720` stage with responsive scale-to-fit behavior
   - keyboard and touch navigation
   - top progress bar and bottom navigation dots
   - inline CSS and inline JS unless the user explicitly provides local assets
   - SVG icons instead of emoji
   - production-grade motion and hover polish

5. Match the requested visual direction.
   Start from a coherent palette and interaction system. If the user asks for a recolor, adjust variables and dependent effects first instead of rewriting layout structure. Use [references/visual-system.md](references/visual-system.md).

6. Verify before handing off.
   Confirm:
   - every slide has entry animation
   - interactive cards include glow/hover treatment
   - navigation works with click, keyboard, and touch
   - the deck scales correctly in the browser
   - no stale theme colors remain after recoloring

## Codex-Specific Notes

- In Codex default mode, use normal chat questions instead of `ask_user_input_v0`.
- Save output where the task expects it. If the user does not specify a path, prefer the current workspace and use a descriptive filename such as `topic-pitch-YYYYMMDD.html`.
- Do not depend on external CDNs unless the user explicitly allows them.
- Preserve user-provided branding, screenshots, or copy. Expand weak content, but do not invent sensitive business facts.

## Quality Bar

- Favor bold, intentional visual direction over generic slideware.
- Keep the file self-contained and presentation-ready.
- Prefer small, reusable sections and CSS variables so recoloring is cheap.
- Treat motion as part of the narrative, not decoration.
