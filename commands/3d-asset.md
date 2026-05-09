---
description: Fetch a free CC0 3D model (or HDRI) and wire it into the current R3F project
argument-hint: <description-of-asset> [model|hdri]
---

You are now in **3D asset fetcher mode** for the current R3F project (cwd should be a project root with `package.json` + `public/`).

## Request

$ARGUMENTS

## Plan

1. **Decide asset type** — `model` (default, .glb) or `hdri` (.hdr).
2. **Find a CC0 source.** Try in this order:
   a. If a `three-d-assets` MCP server is connected, use it (Sketchfab/Polyhaven search).
   b. Otherwise, suggest the user paste a direct download URL from one of:
      - https://poly.pizza (search → Download → glTF)
      - https://sketchfab.com (CC0 filter → Download → glTF)
      - https://quaternius.com (zip packs)
      - https://polyhaven.com/hdris (for HDRI)
   Prefer Quaternius / poly.pizza for fast direct .glb URLs.
3. **Download:**
   - Model:  `bash skills/3d-builder/scripts/fetch-cc0-model.sh <url> ./public/model.glb`
   - HDRI:   `bash skills/3d-builder/scripts/fetch-hdri.sh <slug> 1k ./public/env.hdr`
4. **Optimize if model > 2 MB:**
   `bash skills/3d-builder/scripts/optimize-glb.sh public/model.glb`
5. **Generate typed component (model only):**
   `npx gltfjsx public/model.glb -o src/components/Model.tsx -t`
6. **Wire into `Scene.tsx`:**
   - Model: replace the `<mesh>` block with `<Suspense fallback={null}><Model /></Suspense>`. Add `import { Suspense } from 'react'` and `import Model from './Model'`.
   - HDRI: replace `<Environment preset="city" />` with `<Environment files="/env.hdr" background={false} />`.
7. **Verify** — make sure dev server still compiles. If types complain about a node in the GLTF, point the user at the exact line in `Model.tsx`.

## Important

- Always credit the asset author in a comment in `Model.tsx` if the license requires it (CC0 doesn't, but Sketchfab CC-BY does).
- Never download from a URL that doesn't end in `.glb`, `.gltf`, or `.hdr` without confirming with the user.
