# Hero Section: Arnox
Build a single hero section for **Arnox** — the compute fabric for autonomous agents.
Industry context: Web3 / Crypto Protocol. Target audience: AI infrastructure teams and onchain developers.
## Visual Direction — "Web3 Neon 3D"
**Mood:** futuristic, technical, energetic
**Color palette:**
- Background: #0a0014 with 3D animated mesh (iridescent purple→cyan)
- Surface: thin 1px #ffffff20 outlined cards with neon glow on hover
- Text: #ffffff primary, #b8b8d4 secondary
- Accent: #00f0ff cyan + #ff2ec4 magenta gradient
**Typography:**
- Display: Space Grotesk, weight 700, tracking -0.03em, size clamp(64px, 9vw, 144px); secondary line in monospace
- Body: IBM Plex Mono, weight 400, size 15px
**Layout:** centered headline with rotating 3D torus knot / icosahedron behind it; CTA pill row + "trusted by" logo strip below; animated grid floor in foreground
## Motion & Interaction
Three.js: continuously rotating low-poly geometry with iridescent shader; on-scroll camera dolly forward; headline characters glow-pulse in sync with mesh rotation
## Copy
- Headline: write a single sentence using one of these formulas — `The {layer} for {primitive}.` / `{verb} {asset}. Onchain. Permissionless.` / `A new standard for {category}.`. Make it about: the compute fabric for autonomous agents.
- Subheadline (one sentence, max 18 words): Live on {chains}. Audited by {auditors}. ${tvl}+ TVL.
- Primary CTA: "Launch app"
- Secondary CTA: "Read docs"
- Social proof: grid of supported chain logos + audit firm logos
## Tech Requirements
- Framework: A single, self-contained `index.html` file. Tailwind via CDN. Vanilla JS (no build step). All assets inline or via CDN.
- Suggested libraries: three, @react-three/fiber, @react-three/drei, framer-motion
- Fully responsive (mobile breakpoint at 640px). On mobile: collapse asymmetric layouts to a single column, reduce display type to clamp(40px, 12vw, 72px), drop non-essential motion.
- Accessibility: WCAG AA contrast, prefers-reduced-motion respected (disable looping animations), all CTAs are real `<button>` or `<a>` with descriptive text.
- No lorem ipsum. No placeholder images — use CSS gradients, SVG, or shaders only.
## Inspiration references
- arc.computer
- replicate.com hero
- midjourney homepage
## Additional notes
- Multi-section landing page (not just hero)
- pinned full-viewport canvas with scroll-driven Three.js scene
- UnrealBloom postprocessing
- GSAP ScrollTrigger for camera + mesh transforms
- respect prefers-reduced-motion by serving a single static frame

## Output
Return only the production-ready code, no commentary. Component must look polished on first render — no `/* TODO */`, no empty handlers, no skeleton fallbacks. Treat this as the public homepage of a Series-A funded company.
