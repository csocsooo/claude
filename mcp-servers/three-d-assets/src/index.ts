#!/usr/bin/env node
/**
 * three-d-assets MCP server
 *
 * Exposes three tools to Claude Code:
 *  - sketchfab_search  — search CC0/CC-BY downloadable models on Sketchfab
 *  - polyhaven_search  — search Polyhaven HDRIs / textures (all CC0)
 *  - meshy_generate    — submit a text-to-3D job to Meshy.ai
 *
 * Auth (env vars, optional):
 *   SKETCHFAB_TOKEN   — required for Sketchfab download URLs (free account token)
 *   MESHY_API_KEY     — required for Meshy.ai (free tier: 200 credits/month)
 *   Polyhaven needs no key (public API).
 */
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js'
import { sketchfabSearch } from './sketchfab.js'
import { polyhavenSearch } from './polyhaven.js'
import { meshyGenerate, meshyStatus } from './meshy.js'

const server = new Server(
  { name: 'three-d-assets', version: '0.1.0' },
  { capabilities: { tools: {} } },
)

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'sketchfab_search',
      description:
        'Search Sketchfab for downloadable 3D models. Returns up to 10 results with title, author, license, and download URL when available.',
      inputSchema: {
        type: 'object',
        properties: {
          query: { type: 'string', description: 'Search query, e.g. "coffee bean"' },
          license: {
            type: 'string',
            enum: ['cc0', 'by', 'by-sa', 'by-nd', 'by-nc', 'any'],
            default: 'cc0',
            description: 'License filter; cc0 = public domain.',
          },
          limit: { type: 'number', default: 10, minimum: 1, maximum: 24 },
        },
        required: ['query'],
      },
    },
    {
      name: 'polyhaven_search',
      description:
        'Search Polyhaven (CC0) for HDRIs, textures, or 3D models. Returns slug + preview + download URLs at multiple resolutions.',
      inputSchema: {
        type: 'object',
        properties: {
          query: { type: 'string' },
          asset_type: { type: 'string', enum: ['hdris', 'textures', 'models'], default: 'hdris' },
          limit: { type: 'number', default: 10 },
        },
        required: ['query'],
      },
    },
    {
      name: 'meshy_generate',
      description:
        'Submit a text-to-3D generation job to Meshy.ai. Returns a job id; poll with meshy_status. Requires MESHY_API_KEY env var.',
      inputSchema: {
        type: 'object',
        properties: {
          prompt: { type: 'string' },
          art_style: {
            type: 'string',
            enum: ['realistic', 'sculpture', 'cartoon'],
            default: 'realistic',
          },
        },
        required: ['prompt'],
      },
    },
    {
      name: 'meshy_status',
      description: 'Check the status of a Meshy.ai generation job. Returns model URL when ready.',
      inputSchema: {
        type: 'object',
        properties: { job_id: { type: 'string' } },
        required: ['job_id'],
      },
    },
  ],
}))

server.setRequestHandler(CallToolRequestSchema, async (req) => {
  const { name, arguments: args } = req.params
  try {
    let result: unknown
    switch (name) {
      case 'sketchfab_search':
        result = await sketchfabSearch(args as Parameters<typeof sketchfabSearch>[0])
        break
      case 'polyhaven_search':
        result = await polyhavenSearch(args as Parameters<typeof polyhavenSearch>[0])
        break
      case 'meshy_generate':
        result = await meshyGenerate(args as Parameters<typeof meshyGenerate>[0])
        break
      case 'meshy_status':
        result = await meshyStatus(args as Parameters<typeof meshyStatus>[0])
        break
      default:
        throw new Error(`Unknown tool: ${name}`)
    }
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] }
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err)
    return {
      isError: true,
      content: [{ type: 'text', text: `Error: ${msg}` }],
    }
  }
})

const transport = new StdioServerTransport()
await server.connect(transport)
console.error('three-d-assets MCP server running on stdio')
