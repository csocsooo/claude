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

## Templates

Two templates ship with this skill:

### `r3f-vite` — minimal (default)

Single-page hero + 3 features + CTA. Best for portfolios, single-product
showcases, simple landings.

```
templates/r3f-vite/
├── src/components/{Scene,Hero,Features,Contact}.tsx
├── src/{App,main,index.css}
└── {package.json,vite.config.ts,tsconfig.json,tailwind.config.js,...}
```

### `r3f-business` — multi-section company site

Full structure for company / agency / studio sites: nav + hero + 6-service
grid + pinned-scroll project showcase + working contact form + 4-column footer.
Includes JSON-LD LocalBusiness schema, Open Graph, sitemap, robots.txt,
reduced-motion CSS, mobile menu.

```
templates/r3f-business/
├── src/components/{Nav,Hero,Scene,Services,ProjectShowcase,ContactForm,Footer}.tsx
├── src/{App,main,index.css}
├── public/{robots.txt,sitemap.xml}
├── .env.example  (Formspree endpoint)
└── ... (configs as above + lucide-react)
```

## Workflow

### Step 0 — (optional) Recon a target URL

If you're rebranding or matching an existing site:

```bash
bash skills/3d-builder/scripts/recon.sh <url> ./recon-output
```

Produces `colors-top.txt`, `copy.md`, `images/`, `logo-candidates.txt`,
`recon.json`. The `/3d-recon` slash command wraps this and adds smart
post-processing (e.g. ignore neutrals when picking brand palette).

### Step 1 — Scaffold

```bash
bash skills/3d-builder/scripts/scaffold.sh <target-dir> <project-name> [vite|business]
```

Default template is `vite`. Use `business` for company/agency sites.

### Step 2 — Customize content

Replace `__PLACEHOLDER__` tokens. Both templates share these tokens; `business`
adds more.

**Shared (both templates)**

| Token | What to put |
|-------|-------------|
| `__PROJECT_NAME__` | npm package name (kebab-case) |
| `__TITLE__` / `__DESCRIPTION__` | Browser tab + meta |
| `__BRAND_50__` … `__BRAND_900__` | Tailwind brand palette (hex w/o `#`) |
| `__BRAND_500__` (in `Scene.tsx`, `index.css`) | Primary mesh color |
| `__HERO_TITLE__` / `__HERO_SUBTITLE__` | Hero copy |

**`r3f-vite` only**

| Token | What |
|-------|------|
| `__FEATURES_HEADING__` | Features section heading |
| `__FEATURE_{1,2,3}_TITLE__` / `__FEATURE_{1,2,3}_BODY__` | 3 cards |
| `__CONTACT_HEADING__` / `__CONTACT_SUBTITLE__` / `__CONTACT_CTA__` | CTA section |

**`r3f-business` only**

| Token category | Tokens |
|----|----|
| Lang/SEO | `__LANG__`, `__OG_TITLE__`, `__OG_DESCRIPTION__`, `__OG_URL__`, `__OG_LOCALE__`, `__THEME_COLOR__` |
| Brand identity | `__BRAND_NAME__`, `__BRAND_100__`, `__BRAND_400__`, `__BRAND_600__` (full 6-step scale) |
| Fonts | `__FONT_DISPLAY__`, `__FONT_SANS__` |
| Nav | `__NAV_SERVICES__`, `__NAV_PROJECTS__`, `__NAV_CONTACT__`, `__NAV_CTA__` |
| Hero | `__HERO_KICKER__`, `__HERO_CTA_PRIMARY__`, `__HERO_CTA_SECONDARY__` |
| Services | `__SERVICES_KICKER__`, `__SERVICES_HEADING__`, `__SERVICES_SUBTITLE__`, 6× `__SERVICE_N_TITLE__`/`_BODY__` |
| Project | `__PROJECT_KICKER__`, `__PROJECT_TITLE__`, `__PROJECT_BODY__`, 3× `__STAT_N_LABEL__`/`_VALUE__`, 4× `__PROJECT_IMG_N_ALT__` |
| Contact form | `__CONTACT_KICKER__`, `__FORM_NAME_LABEL__`, `__FORM_EMAIL_LABEL__`, `__FORM_PHONE_LABEL__`, `__FORM_MESSAGE_LABEL__`, `__FORM_GDPR_LABEL__`, `__FORM_SUBMIT__`, `__FORM_SENDING__`, `__FORM_SUCCESS__`, `__FORM_ERROR__` |
| Footer | `__FOOTER_TAGLINE__`, `__FOOTER_COL{1,2,3}_TITLE__`, `__FOOTER_LINK_{1,2,3}__`, `__FOOTER_LEGAL_{1,2,3}__`, `__FOOTER_ADDRESS__`, `__FOOTER_EMAIL__`, `__FOOTER_PHONE__`, `__FOOTER_YEAR__`, `__FOOTER_RIGHTS__` |
| JSON-LD address | `__ADDRESS_STREET__`, `__ADDRESS_CITY__`, `__ADDRESS_ZIP__`, `__ADDRESS_COUNTRY__` |

To find every remaining token quickly:
```bash
grep -rn "__[A-Z0-9_]\+__" src/ index.html tailwind.config.js public/
```

Use the Edit tool to replace tokens (preferred), or `sed -i` for bulk swaps.

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

### Step 7 — Lighthouse audit (optional)

```bash
bash scripts/lighthouse.sh http://localhost:5173 ./lighthouse-report
# or against the live URL after deploy:
bash scripts/lighthouse.sh https://<slug>.vercel.app
```

Prints Performance / Accessibility / Best-practices / SEO scores and writes
a full HTML report.

## Form backend (`r3f-business` only)

The `ContactForm.tsx` posts to `import.meta.env.VITE_FORMSPREE_ENDPOINT`.
Free signup at https://formspree.io → New form → copy endpoint.

```bash
cp .env.example .env.local
# edit VITE_FORMSPREE_ENDPOINT=https://formspree.io/f/...
```

Vercel free tier supports env vars in the dashboard or `vercel env add`.

## Asset pipeline (recap)

| Step | Command |
|------|---------|
| Fetch CC0 model | `bash scripts/fetch-cc0-model.sh <url> ./public/model.glb` |
| Fetch HDRI | `bash scripts/fetch-hdri.sh <slug> 1k ./public/env.hdr` |
| Optimize GLB (draco + WebP textures) | `bash scripts/optimize-glb.sh public/model.glb` |
| Generate typed React component | `npx gltfjsx public/model.glb -o src/components/Model.tsx -t` |

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
