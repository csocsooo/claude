# Claude Code 3D-website builder

Build production-ready 3D animated websites in **1-2 prompts** inside Claude Code.

```
/3d-site "kávézó Budapesten" minimalista
   ↓ ~30s
http://localhost:5173  →  rotating 3D scene, GSAP scroll, Tailwind, ready to deploy
```

## What's in here

| Path | Purpose |
|------|---------|
| `commands/3d-recon.md` | `/3d-recon <url>` — scrape a target URL for colors/copy/images/logo |
| `commands/3d-site.md` | `/3d-site <theme> [vite\|business] [--recon <dir>]` — scaffold + customize |
| `commands/3d-asset.md` | `/3d-asset <description>` — fetch a CC0 model or HDRI and wire it in |
| `commands/3d-deploy.md` | `/3d-deploy [dir]` — push to Vercel (or Cloudflare Pages) free tier |
| `skills/3d-builder/` | Skill triggered when you mention 3D/R3F/Three.js — owns templates + scripts |
| `skills/3d-builder/templates/r3f-vite/` | Minimal: hero + 3 features + CTA |
| `skills/3d-builder/templates/r3f-business/` | Multi-section: nav + hero + 6 services + pinned project showcase + form + footer + SEO/JSON-LD |
| `skills/3d-builder/scripts/` | `recon.sh`, `scaffold.sh`, `fetch-cc0-model.sh`, `fetch-hdri.sh`, `optimize-glb.sh`, `deploy-vercel.sh`, `lighthouse.sh` |
| `agents/3d-architect.md` | Subagent for stack/architecture decisions before you commit to a build |
| `mcp-servers/three-d-assets/` | MCP server for Sketchfab + Polyhaven + Meshy.ai search & generation |
| `settings.json` | Permissions allowlist + MCP wiring + SessionStart hook |

## Install

### Option A — User-global (`~/.claude/`)

Use it across every project on this machine:

```bash
# Backup an existing config first if you have one.
mv ~/.claude ~/.claude.bak 2>/dev/null || true

git clone <this-repo> ~/.claude
cd ~/.claude/mcp-servers/three-d-assets
npm install && npm run build
```

Restart Claude Code. Slash commands `/3d-site`, `/3d-asset`, `/3d-deploy` are now globally available.

### Option B — Project-local (`./.claude/`)

Use it only in one project:

```bash
git clone <this-repo> .claude
cd .claude/mcp-servers/three-d-assets
npm install && npm run build
```

## Usage flows

### Flow A — fresh build (1-2 prompts)

```
/3d-site "specialty coffee shop in Budapest" minimalista warm
/3d-asset "coffee bean" model
/3d-deploy           # optional
```

### Flow B — rebrand from existing URL (5-8 prompts, top quality)

For top-quality production-ready output that mirrors an existing brand:

```
/3d-recon https://arnox.hu                                # scrape colors, copy, logo, images
/3d-site arnox-rebrand business --recon ./recon-output    # scaffold business template with extracted data
/3d-asset "modern villa exterior" model                   # hero 3D model (Sketchfab CC0)
"Replace 6 service icons + copy with: Tervezés/Kivitelezés/Felújítás/Ingatlan/Anyagok/Finanszírozás"
"Wire Szőlőliget Ökopark images from recon into ProjectShowcase, with stats + alts"
"Set up Formspree endpoint in .env.local and verify form submit"
"Polish: SEO meta + JSON-LD address + favicon from recon logo + reduced-motion check"
/3d-deploy                                                # Vercel free tier
```

After deploy, run `bash skills/3d-builder/scripts/lighthouse.sh <live-url>` to verify scores.

## Optional API keys (free tiers)

Set these in your shell to unlock more capability — none are required.

```bash
export SKETCHFAB_TOKEN="..."   # https://sketchfab.com/settings/password (free)
export MESHY_API_KEY="..."     # https://meshy.ai/api (200 credits/mo free)
```

Polyhaven needs no key.

## Performance defaults baked in

- `dpr={[1, 2]}` cap on `<Canvas>` — sharp on retina, not on low-DPI
- `Float` + `Environment` + `OrbitControls` from drei
- GSAP ScrollTrigger registered once, scoped via `gsap.context`
- Tailwind purge configured for `.tsx` files
- `@types/three` pinned to match `three`

## Free-tier asset sources

| Source | License | Best for |
|--------|---------|----------|
| [poly.pizza](https://poly.pizza) | CC0 | Direct .glb downloads, low-poly, many themes |
| [Sketchfab CC0 filter](https://sketchfab.com/3d-models?features=downloadable&licenses=322a749bcfa841b29dff1e8a1bb74b0b) | CC0 | High-quality scanned + artist models |
| [Quaternius](https://quaternius.com) | CC0 | Stylized packs (game-ready) |
| [Kenney.nl](https://kenney.nl/assets) | CC0 | Game assets, isometric |
| [Polyhaven](https://polyhaven.com) | CC0 | HDRIs, textures, PBR |
| [Meshy.ai](https://meshy.ai) | Per ToS | Text → 3D AI |
| [TripoSR on HF](https://huggingface.co/spaces/stabilityai/TripoSR) | Apache 2.0 | Image → 3D |

## Extending

- Add a new template (e.g. Next.js + R3F): drop into `skills/3d-builder/templates/<name>/` and reference it from a new `/3d-site-next` command.
- Add a new MCP tool: edit `mcp-servers/three-d-assets/src/index.ts`, add a handler file, rebuild.
- Add a hook: e.g. PostToolUse hook that auto-runs `optimize-glb.sh` when a `.glb` lands in `public/`.

## License

MIT for the scaffold + scripts. Bundled fonts via Google Fonts CDN. Templates produce code you own.
