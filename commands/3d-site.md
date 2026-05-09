---
description: Scaffold a complete 3D animated website (R3F + GSAP + Tailwind) from a one-line brief
argument-hint: <theme/topic> [vite|business] [--recon <dir>]
---

You are now in **3D-site builder mode**. Use the `3d-builder` skill at `~/.claude/skills/3d-builder/` (or this repo's `skills/3d-builder/`).

## Brief

$ARGUMENTS

## Pick a template

Parse the args. The second positional arg (after the theme) selects the template:

- `vite` (default) — minimal hero + 3 features + contact CTA. Use for portfolio, single-product showcase, simple landing.
- `business` — nav + hero + 6-service grid + pinned project showcase + working form + footer. Use for company sites, agencies, anything with services + case studies.

If the user mentions "company", "agency", "services", "construction", "studio", "rebrand <url>", default to `business`.

## Detect a recon directory

If args contain `--recon <path>` (or the user previously ran `/3d-recon`), read these from that path:

- `recon.json` — title, description, top color
- `colors-top.txt` — pick a brand primary that's NOT a neutral (skip `#000000`, `#ffffff`, `#f8f9fa`, `#e9ecef`, `#dc3545`-style Bootstrap defaults are fine *if* dominant; ignore if site is pure Bootstrap untweaked). Pick the most-frequent saturated color.
- `copy.md` — for hero title/subtitle, services list, project name
- `images/` — for project showcase images and logo
- `logo-candidates.txt` — first .svg or first .png is usually the logo

## Plan

1. **Slug** — kebab-case from theme. e.g. "ARNOX rebrand" → `arnox-rebrand`.
2. **Target dir** — `./<slug>` unless user gave one in args.
3. **Scaffold:**
   ```bash
   bash skills/3d-builder/scripts/scaffold.sh ./<slug> <slug> <template>
   ```
4. **Move recon assets in** (if recon supplied):
   ```bash
   cp <recon>/images/*logo* ./<slug>/public/logo.svg  # or .png if no svg
   mkdir -p ./<slug>/public/projects
   cp <recon>/images/*.{jpg,png,webp} ./<slug>/public/projects/  # let user curate later
   cp <recon>/images/*favicon* ./<slug>/public/favicon.svg 2>/dev/null || true
   ```
5. **Replace `__PLACEHOLDER__` tokens.** Use Edit tool, batched. Token reference is in `skills/3d-builder/SKILL.md`. Key categories:
   - **Brand identity** — `__BRAND_NAME__`, `__TITLE__`, `__DESCRIPTION__`, `__OG_*`, `__LANG__` (`hu` for Hungarian)
   - **Colors** — `__BRAND_50__` … `__BRAND_900__` in `tailwind.config.js`, `__BRAND_500__` in `Scene.tsx` and `index.css`. Use a 6-step scale; if you only have one brand color, tint/shade it for the rest.
   - **Hero** — `__HERO_KICKER__`, `__HERO_TITLE__`, `__HERO_SUBTITLE__`, `__HERO_CTA_PRIMARY__`, `__HERO_CTA_SECONDARY__`
   - **Services (business only)** — 6 × `__SERVICE_N_TITLE__` + `__SERVICE_N_BODY__`. Pick Lucide icon imports in `Services.tsx` matching each service.
   - **Project showcase (business only)** — `__PROJECT_TITLE__`, `__PROJECT_BODY__`, 3 stats, 4 image alt texts
   - **Contact form** — `__CONTACT_*`, `__FORM_*` (Hungarian if `__LANG__=hu`)
   - **Footer** — column titles, legal links, address, email, phone, year, rights statement
   - **Address (JSON-LD)** — `__ADDRESS_*`
   - **Fonts** — `__FONT_DISPLAY__` (default `Playfair Display`), `__FONT_SANS__` (default `Inter`)

6. **Install + dev:**
   ```bash
   cd ./<slug> && npm install && npm run dev &
   ```
   Run dev in background so the URL prints. Wait ~3s then report.

7. **Report** to the user:
   - Local URL
   - What was generated (sections)
   - What still has `__PLACEHOLDER__` tokens (search: `grep -rn "__[A-Z0-9_]\+__" src/ index.html tailwind.config.js public/ | head -20`)
   - Suggested next prompts:
     - `/3d-asset "modern villa" model` — fetch a 3D hero model
     - `/3d-asset "industrial studio HDRI" hdri`
     - "Cseréld a service ikonokat: blueprint, hammer, home, key, brick, wallet"
     - "Tedd a Szőlőliget projekt képeket a /public/projects/ mappába és frissítsd az alt szövegeket"
     - `/3d-deploy` — push to Vercel

## Style guidance

- **modern / minimalista** — neutral charcoal/black, single accent
- **luxury / premium** — black + warm metallic + serif heading
- **construction / industrial** — navy/charcoal + brand red/orange accent + bold sans
- **tech / futuristic** — deep ink + cyan/violet + glassmorphism
- **eco / wellness** — cream + forest green + soft serif

## Speed mode

Default to action. Don't ask clarifying questions unless the brief is one word ("site", "page"). The user can always say "more playful" / "darker" / "swap red for blue" in a follow-up.
