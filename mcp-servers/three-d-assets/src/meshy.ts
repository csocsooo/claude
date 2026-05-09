/**
 * Meshy.ai API wrapper — text-to-3D model generation.
 *
 * Free tier: 200 credits / month. Each text-to-3D job costs ~5-10 credits.
 * Get a key at https://www.meshy.ai/api → MESHY_API_KEY env var.
 *
 * Docs: https://docs.meshy.ai/
 */
const BASE = 'https://api.meshy.ai/openapi/v2/text-to-3d'

interface MeshyGenerateInput {
  prompt: string
  art_style?: 'realistic' | 'sculpture' | 'cartoon'
}

interface MeshyJob {
  id: string
  status: 'PENDING' | 'IN_PROGRESS' | 'SUCCEEDED' | 'FAILED' | 'CANCELED'
  progress?: number
  model_urls?: { glb?: string; fbx?: string; obj?: string }
  thumbnail_url?: string
  task_error?: { message: string }
}

function authHeader(): { Authorization: string } {
  const key = process.env.MESHY_API_KEY
  if (!key) throw new Error('MESHY_API_KEY not set. Get one free at https://meshy.ai/api')
  return { Authorization: `Bearer ${key}` }
}

export async function meshyGenerate({
  prompt,
  art_style = 'realistic',
}: MeshyGenerateInput): Promise<{ job_id: string }> {
  // Step 1: preview (low-poly draft, ~1 min, ~5 credits).
  const r = await fetch(BASE, {
    method: 'POST',
    headers: { ...authHeader(), 'Content-Type': 'application/json' },
    body: JSON.stringify({ mode: 'preview', prompt, art_style }),
  })
  if (!r.ok) throw new Error(`Meshy ${r.status}: ${await r.text()}`)
  const { result } = (await r.json()) as { result: string }
  return { job_id: result }
}

export async function meshyStatus({
  job_id,
}: {
  job_id: string
}): Promise<MeshyJob> {
  const r = await fetch(`${BASE}/${job_id}`, { headers: authHeader() })
  if (!r.ok) throw new Error(`Meshy ${r.status}: ${await r.text()}`)
  return (await r.json()) as MeshyJob
}
