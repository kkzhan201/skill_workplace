# HTML Pitch Deck Skill Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Update the html-pitch-deck skill to enforce an outline-first, copy-lock workflow before component selection and HTML implementation.

**Architecture:** Keep the skill browser-first and HTML-focused, but move content generation control into a strict staged workflow. SKILL.md becomes the gatekeeper, while the brief reference becomes a planning and markdown-copy artifact guide.

**Tech Stack:** Markdown, YAML frontmatter, git

---

### Task 1: Rewrite the main workflow

**Files:**
- Modify: `skills/html-pitch-deck/SKILL.md`

**Step 1: Rewrite the workflow section**
Describe four gated stages: outline, markdown copy confirmation, presentation mapping, HTML build.

**Step 2: Add explicit gating rules**
State that no extra copy, no component choice, and no code are allowed before user confirmation of the markdown copy.

**Step 3: Preserve existing scope**
Keep HTML-only positioning, browser-first output, and visual-system reference intact.

### Task 2: Rewrite the planning reference

**Files:**
- Modify: `skills/html-pitch-deck/references/brief-and-structure.md`

**Step 1: Remove auto-expansion guidance**
Replace content-expansion defaults with gap exposure and approval rules.

**Step 2: Add markdown copy template**
Provide a slide-by-slide markdown structure the skill should output for user confirmation.

**Step 3: Align with stage 1 and stage 2**
Ensure the reference supports page logic first and copy lock second.

### Task 3: Verify and publish

**Files:**
- Verify: `skills/html-pitch-deck/SKILL.md`
- Verify: `skills/html-pitch-deck/references/brief-and-structure.md`

**Step 1: Validate structure manually**
Read the edited files to confirm the gating language is explicit.

**Step 2: Check git diff**
Run `git diff -- skills/html-pitch-deck` to ensure only intended files changed.

**Step 3: Commit and push**
Commit the update and push `main` to origin.
