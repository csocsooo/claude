# three-d-assets MCP server

Lets Claude Code search free 3D assets and submit AI generation jobs without leaving the terminal.

## Tools

| Tool | What it does | Auth |
|------|--------------|------|
| `sketchfab_search` | Search downloadable Sketchfab models (CC0 by default) | Optional `SKETCHFAB_TOKEN` (free) for direct download URLs |
| `polyhaven_search` | Search Polyhaven HDRIs, textures, models (all CC0) | None |
| `meshy_generate` | Submit a text-to-3D job to Meshy.ai | `MESHY_API_KEY` (free tier: 200 credits/mo) |
| `meshy_status` | Poll a Meshy job until the GLB is ready | `MESHY_API_KEY` |

## Build

```bash
cd mcp-servers/three-d-assets
npm install
npm run build
```

## Wire into Claude Code

Add to your `~/.claude/settings.json` (or this repo's `settings.json`):

```json
{
  "mcpServers": {
    "three-d-assets": {
      "command": "node",
      "args": ["./mcp-servers/three-d-assets/dist/index.js"],
      "env": {
        "SKETCHFAB_TOKEN": "${SKETCHFAB_TOKEN:-}",
        "MESHY_API_KEY": "${MESHY_API_KEY:-}"
      }
    }
  }
}
```

Then restart Claude Code. The tools appear as `mcp__three-d-assets__sketchfab_search` etc.

## Get free API keys

- **Sketchfab token:** https://sketchfab.com/settings/password → API tokens. Required only if you want direct `.glb` download URLs in results; without it you get the model page URL.
- **Meshy.ai key:** https://www.meshy.ai/api → "Get API Key". Free 200 credits/month — enough for ~20-40 model generations.

Polyhaven is fully open and needs nothing.

## Status

This is a working skeleton. The Sketchfab and Polyhaven tools work out of the box; Meshy requires the env var. Test with:

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | node dist/index.js
```
