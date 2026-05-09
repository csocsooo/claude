---
description: Scrape a target URL for brand assets (colors, fonts, copy, images, logo) — feeds into /3d-site
argument-hint: <url> [output-dir]
---

You are now in **brand recon mode**. Your job is to extract usable brand inputs from the user's target URL so the next `/3d-site` invocation has real data instead of guesses.

## Target

$ARGUMENTS

## Plan

1. **Run the recon script:**
   ```bash
   bash skills/3d-builder/scripts/recon.sh <url> <output-dir>
   ```
   Default output dir: `./recon-output/`.

2. **Verify outputs.** After the script finishes, read these files in order:
   - `<out>/recon.json` — quick summary
   - `<out>/colors-top.txt` — frequency-ranked palette (pick top 3-5 for brand colors)
   - `<out>/copy.md` — title, meta, headings, opening paragraphs
   - `<out>/fonts.txt` — font stack
   - `<out>/logo-candidates.txt` — likely logo paths
   - `ls <out>/images/` — what's downloaded

3. **Supplement with WebFetch if anything is thin.** Common gaps:
   - Lazy-rendered content (React/Vue SPAs) — recon.sh sees only initial HTML.
   - Background image URLs in inline styles.
   - Service descriptions inside cards rendered by JS.
   For these, use WebFetch with a focused prompt like "list every service the company offers, with name + 1-sentence description."

4. **Summarise for the user** in this format:

   ```
   ## Recon: <url>

   **Brand palette** (from frequency analysis)
   - Primary: #XXXXXX
   - Secondary: #XXXXXX
   - Background: #XXXXXX

   **Typography**: <font stack>

   **Logo**: <path or "not found, will need manual download">

   **Key copy**
   - Tagline: "..."
   - Services: 1) ..., 2) ..., 3) ...
   - Featured project: "..."

   **Images downloaded**: N files in <out>/images/

   **Suggested next prompt**:
   /3d-site <slug> business --recon <out>
   ```

5. **Don't decide brand palette by frequency alone.** Black/white/gray dominate every site. Pick the top non-neutral color as primary; ignore `#000000`, `#ffffff`, `#fafafa`, etc.

## When recon fails

- If the site returns 403 or 503 (anti-bot): the script's UA is generic. Suggest the user paste the page source manually, or fall back to WebFetch.
- If the site is behind login/Cloudflare: tell the user, don't try to bypass.
- If the script outputs zero colors: the site likely uses CSS-in-JS or external CSS the script didn't follow. Use WebFetch to ask for the dominant colors visually.
