# HTML Pitch Deck Skill Design

## Decision
Use a strict gated workflow to prevent content drift.

## Chosen Workflow
1. Define deck narrative and slide logic first.
2. Produce a markdown copy draft for user confirmation.
3. Map confirmed copy to the best presentation pattern and components.
4. Build the HTML deck only after copy is locked.

## Constraints
- Do not expand sparse user content by default.
- Do not invent market background, metrics, user quotes, or competitive claims unless the user explicitly asks for drafting help.
- Treat the markdown copy draft as a required approval gate.
- Do not choose components or write HTML before the user confirms the copy.

## Planned Skill Changes
- Rewrite the workflow in SKILL.md around the four gated stages.
- Update the structure reference so it supports outline-first and copy-lock behavior instead of auto-filling weak briefs.
- Keep the visual-system reference for implementation stage only.
- Preserve the browser-first HTML positioning of the skill.
