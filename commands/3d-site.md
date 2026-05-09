---
description: Scaffold a complete 3D animated website (R3F + GSAP + Tailwind) from a one-line brief
argument-hint: <theme/topic> [style] [project-dir]
---

You are now in **3D-site builder mode**. Use the `3d-builder` skill at `~/.claude/skills/3d-builder/` (or this repo's `skills/3d-builder/`).

## Brief

$ARGUMENTS

## Plan

Read `skills/3d-builder/SKILL.md` for the full workflow. Then execute:

1. **Pick a project name** — kebab-case slug derived from the theme (e.g. "kávézó Budapesten" → `kavezo-budapest`).
2. **Pick a target directory** — if the user gave one in the args, use it; otherwise `./<slug>` relative to cwd.
3. **Scaffold** — run `bash skills/3d-builder/scripts/scaffold.sh <target> <slug>`.
4. **Customize content** — replace the `__PLACEHOLDER__` tokens in:
   - `index.html` (title + description)
   - `tailwind.config.js` (brand color palette — pick 50/500/900 hex matching the theme/style)
   - `src/components/Scene.tsx` (`__BRAND_500__` for the mesh color)
   - `src/components/Hero.tsx` (hero title + subtitle)
   - `src/components/Features.tsx` (3 feature cards)
   - `src/components/Contact.tsx` (CTA copy)
   Write copy in the language the user's brief is in (default Hungarian if mixed).
5. **Install + run dev** — `cd <target> && npm install && npm run dev` (run in background so the URL prints).
6. **Report** — give the user the local URL, what was generated, and the next 1-2 prompts they can use:
   - `/3d-asset <theme>` to fetch a CC0 model
   - `/3d-deploy` to push to Vercel free tier
   - "Cseréld a hero modellt erre: <url>" for manual model swap
   - "Adj hozzá egy gallery section-t scroll-triggered fade-innel"

## Style guidance

- **modern / minimalista** — neutral grays, single accent color, lots of whitespace, `Inter` font
- **playful / fun** — saturated palette, multiple accent colors, rounded shapes
- **luxury / premium** — black/gold/cream, serif headings, slow animations
- **tech / futuristic** — black/cyan/purple, glassmorphism, neon glow

If the brief is ambiguous, pick a sensible default for the topic and tell the user what you chose so they can redirect with a follow-up prompt.

## Speed mode

Don't ask clarifying questions unless the brief is genuinely ambiguous (e.g. one word like "site"). Default to action — the user can always say "more playful" or "change the colors" in a follow-up.
