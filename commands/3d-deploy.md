---
description: Deploy the current 3D site to Vercel free tier (or fall back to Cloudflare Pages instructions)
argument-hint: [project-dir]
---

You are now in **deploy mode** for an R3F project.

## Target

$ARGUMENTS (defaults to current directory)

## Plan

1. **Sanity check**:
   - `package.json` exists and has a `build` script
   - `npm run build` succeeds locally (run it first; abort on failure and surface the error)
2. **Deploy via Vercel CLI:**
   ```bash
   bash skills/3d-builder/scripts/deploy-vercel.sh <project-dir>
   ```
   First run prompts for login + project creation. Subsequent runs are zero-touch.
3. **Capture the production URL** from the CLI output and report it.
4. **If Vercel auth is unavailable** (e.g. headless container, no browser), give the user these fallbacks instead:
   - **Cloudflare Pages:** push to GitHub, then [pages.cloudflare.com](https://pages.cloudflare.com) → Connect → set build command `npm run build`, output dir `dist`.
   - **Netlify:** `npx netlify deploy --prod --dir=dist`
   - **GitHub Pages:** static-only — add `vite-plugin-gh-pages` and run `npx gh-pages -d dist`.

## Don't

- Don't push to `main`/`master` of the user's repo without confirmation.
- Don't run `vercel --prod` on a project that isn't theirs (check `package.json` name + git remote).
- Don't add a paid plan, custom domain, or any environment that would incur cost.
