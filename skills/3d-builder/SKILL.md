---
name: 3d-builder
description: Scaffold, customize, optimize, and deploy a 3D animated website (React Three Fiber + GSAP + Tailwind) from a 1-line brief. Use when the user wants to build, generate, or bootstrap a 3D website, landing page, portfolio, or product showcase with R3F / Three.js / GSAP. Triggers on phrases like "3D website", "R3F site", "Three.js landing page", or after invoking /3d-site, /3d-asset, /3d-deploy.
---

# 3D Website Builder

Build production-ready 3D animated websites in 1-2 prompts. Stack: **Vite + React 18 + TypeScript + React Three Fiber + drei + GSAP + Tailwind CSS**.

## When to use

Activate this skill when the user asks for any of:

- A 3D animated landing page, portfolio, or product showcase
- A React Three Fiber / Three.js scaffolded project
- Scroll-triggered animations on a 3D scene
- Free 3D asset fetching (Sketchfab CC0, Polyhaven, Quaternius)
- Optimization (gltf-transform / draco) or deployment of a 3D site

## Workflow

### Step 1 — Scaffold

Run the scaffold script to copy the bundled R3F template:

```bash
bash "$CLAUDE_DIR/skills/3d-builder/scripts/scaffold.sh" <target-dir> <project-name>
```

Where `$CLAUDE_DIR` resolves to `~/.claude` (user-level) or the repo path.
If `$CLAUDE_DIR` is unset, infer it from the SKILL.md location:
`SKILL_DIR="$(dirname "$0")"` then `scripts/scaffold.sh`.

The template lives at `templates/r3f-vite/` and contains:

- `package.json`, `vite.config.ts`, `tsconfig.json`
- `tailwind.config.js`, `postcss.config.js`
- `src/main.tsx`, `src/App.tsx`, `src/index.css`
- `src/components/Scene.tsx` — R3F canvas with rotating object + Float + Environment
- `src/components/Hero.tsx` — Hero with GSAP entrance animation
- `src/components/Features.tsx` — Scroll-triggered card grid
- `src/components/Contact.tsx` — CTA section

### Step 2 — Customize content

The template uses `__PLACEHOLDER__` tokens. Replace them based on the user's brief:

| Token | What to put |
|-------|-------------|
| `__PROJECT_NAME__` | npm package name (kebab-case) |
| `__TITLE__` | Browser tab title |
| `__DESCRIPTION__` | SEO meta description |
| `__HERO_TITLE__` | Big H1 |
| `__HERO_SUBTITLE__` | Subhead under hero |
| `__FEATURES_HEADING__` | Section title |
| `__FEATURE_{1,2,3}_TITLE__` / `__FEATURE_{1,2,3}_BODY__` | 3 feature cards |
| `__CONTACT_HEADING__` / `__CONTACT_SUBTITLE__` / `__CONTACT_CTA__` | Contact CTA |
| `__BRAND_50__` / `__BRAND_500__` / `__BRAND_900__` | Tailwind brand palette (hex w/o #) |

Use Edit (preferred) or `sed -i` to replace. Pick a color palette that matches the theme — warm amber for coffee, deep blue for tech, forest green for outdoors, etc.

### Step 3 — Add a 3D model (optional but recommended)

Default scene uses an icosahedron. To replace with a real model:

1. Find a CC0 `.glb` URL. Search via the `three-d-assets` MCP server (Sketchfab / Polyhaven / Quaternius) if available, or ask the user.
2. Download:
   ```bash
   bash scripts/fetch-cc0-model.sh <url> ./public/model.glb
   ```
3. Generate a typed component:
   ```bash
   cd <project> && npx gltfjsx public/model.glb -o src/components/Model.tsx -t
   ```
4. Replace the `<mesh>` block inside `Scene.tsx` with `<Model />`.
5. If >5 MB, optimize:
   ```bash
   bash scripts/optimize-glb.sh public/model.glb
   ```

### Step 4 — Add HDRI lighting (optional)

```bash
bash scripts/fetch-hdri.sh studio_small_03 1k ./public/env.hdr
```

Then in `Scene.tsx`, replace `<Environment preset="city" />` with `<Environment files="/env.hdr" />`.

### Step 5 — Run dev server

```bash
cd <project> && npm install && npm run dev
```

The template binds to `0.0.0.0:5173` so it works in remote/container Claude Code.

### Step 6 — Deploy (free tier)

```bash
bash scripts/deploy-vercel.sh <project-dir>
```

Uses Vercel CLI. First run prompts for login; subsequent runs are zero-touch.
Alternative: push to GitHub and import via vercel.com (easier first time).

## Performance budget

- Initial bundle (excluding 3D assets): < 250 KB gzip
- `.glb` model: < 2 MB after optimization
- Lighthouse mobile: > 80
- Use `useGLTF.preload(url)` outside the component
- Set `dpr={[1, 2]}` on `<Canvas>` (already in template)

## Free asset directories

- **CC0 models:** [poly.pizza](https://poly.pizza), [Sketchfab CC0 filter](https://sketchfab.com/3d-models?features=downloadable&licenses=322a749bcfa841b29dff1e8a1bb74b0b), [Quaternius](https://quaternius.com), [Kenney.nl](https://kenney.nl/assets?q=3d)
- **HDRIs / textures:** [Polyhaven](https://polyhaven.com), [ambientCG](https://ambientcg.com)
- **AI text→3D:** [Meshy.ai](https://meshy.ai) (200 credits/mo free), [Hugging Face TripoSR](https://huggingface.co/spaces/stabilityai/TripoSR), [Hunyuan3D-2](https://huggingface.co/spaces/tencent/Hunyuan3D-2)

## Common pitfalls

- **Three.js peer-dep mismatch:** keep `three` and `@types/three` versions in lockstep with `@react-three/fiber`.
- **GSAP ScrollTrigger SSR:** never import in a file that runs on the server — Vite/Next.js client components only. Template handles this with `useEffect`.
- **Tailwind not picking up classes:** make sure `content` glob in `tailwind.config.js` covers all `.tsx` files.
- **Big `.glb` blocks render:** wrap heavy `<Model />` in `<Suspense fallback={null}>` (drei's `useGLTF` triggers suspense).
