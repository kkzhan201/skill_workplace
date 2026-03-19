---
name: html-pitch-deck
description: "Use when the user asks for a presentation, pitch deck, slide deck, PPT, 路演 deck, 匯報 slides, or product presentation that should be delivered as a single standalone HTML file with animation, interaction, and browser navigation. Prefer this skill when the deck is meant for presenting in a browser rather than editing in PowerPoint or Keynote. Do not use when the user explicitly requires a .pptx file or a corporate PPTX template."
---

# HTML Pitch Deck

## Overview

Create a single self-contained HTML presentation with strong visual polish, motion, and browser-first navigation.

Follow a strict staged workflow to prevent content drift. Lock the deck's narrative and copy before choosing components or writing HTML.

Keep the main skill lean. Load the references only when needed:

- Read [references/brief-and-structure.md](references/brief-and-structure.md) when defining slide logic, resolving missing brief details, or drafting the markdown copy for user confirmation.
- Read [references/visual-system.md](references/visual-system.md) only after the user has confirmed the copy and you are ready to map content to components or implement the HTML.

## Workflow

1. Confirm delivery mode.
   If the user needs editable `.pptx` output, stop and switch to a PPTX-oriented skill instead of forcing HTML.

2. Define the deck outline first.
   Decide the deck's narrative, page order, and what each slide must accomplish before drafting copy. Ask concise plain-text questions only for the missing high-impact inputs:
   - product, project, or topic
   - audience
   - tone
   - slide count if it materially changes scope

   If the user already gave enough context, proceed. Reasonable defaults:
   - `4-6` slides
   - browser presentation, not file export to PPTX
   - formal or data-driven tone for business contexts

3. Draft the copy in markdown and stop for confirmation.
   Produce a markdown document that lists each slide's title and approved talking points. Use the template in [references/brief-and-structure.md](references/brief-and-structure.md). This markdown draft is a hard approval gate.

   Until the user explicitly confirms the markdown copy:
   - do not add background claims, metrics, quotes, or competitive framing on your own
   - do not fill gaps with speculative content
   - do not choose visual components
   - do not write HTML, CSS, or JS

4. Map confirmed copy to presentation patterns.
   After the user confirms the markdown copy, choose the best presentation method for each slide. Components must serve the locked copy rather than reshaping it. Use [references/visual-system.md](references/visual-system.md) only at this stage and later.

5. Build one standalone HTML file.
   Requirements:
   - fixed `1280x720` stage with responsive scale-to-fit behavior
   - keyboard and touch navigation
   - top progress bar and bottom navigation dots
   - inline CSS and inline JS unless the user explicitly provides local assets
   - SVG icons instead of emoji
   - production-grade motion and hover polish

6. Match the requested visual direction.
   Start from a coherent palette and interaction system. If the user asks for a recolor, adjust variables and dependent effects first instead of rewriting layout structure.

7. Verify before handing off.
   Confirm:
   - every slide has entry animation
   - interactive cards include glow/hover treatment
   - navigation works with click, keyboard, and touch
   - the deck scales correctly in the browser
   - no stale theme colors remain after recoloring

## Codex-Specific Notes

- In Codex default mode, use normal chat questions instead of `ask_user_input_v0`.
- Before any implementation, present the markdown copy draft in chat or save it to a `.md` file if the user asks for an artifact to review.
- Save output where the task expects it. If the user does not specify a path, prefer the current workspace and use a descriptive filename such as `topic-pitch-YYYYMMDD.html`.
- Do not depend on external CDNs unless the user explicitly allows them.
- Preserve user-provided branding, screenshots, and copy. Do not invent sensitive business facts or business-facing claims unless the user explicitly asks for drafting help.

## Quality Bar

- Content fidelity comes before visual cleverness.
- Favor bold, intentional visual direction over generic slideware.
- Keep the file self-contained and presentation-ready.
- Prefer small, reusable sections and CSS variables so recoloring is cheap.
- Treat motion as part of the narrative, not decoration.
