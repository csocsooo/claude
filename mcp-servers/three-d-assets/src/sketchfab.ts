/**
 * Sketchfab API wrapper.
 *
 * Docs: https://docs.sketchfab.com/data-api/v3/index.html
 *
 * The /v3/search endpoint is public and needs no token. To get a direct
 * .glb download URL you need to authenticate as a user (SKETCHFAB_TOKEN);
 * without it we still return the model page URL so the user can download
 * manually.
 */
const BASE = 'https://api.sketchfab.com/v3'

interface SketchfabSearchInput {
  query: string
  license?: 'cc0' | 'by' | 'by-sa' | 'by-nd' | 'by-nc' | 'any'
  limit?: number
}

interface SketchfabResult {
  uid: string
  name: string
  author: string
  license: string
  thumbnail: string | null
  page_url: string
  download_url: string | null
  face_count: number | null
  vertex_count: number | null
}

const LICENSE_SLUGS: Record<string, string> = {
  cc0: 'cc0',
  by: 'by',
  'by-sa': 'by-sa',
  'by-nd': 'by-nd',
  'by-nc': 'by-nc',
}

export async function sketchfabSearch({
  query,
  license = 'cc0',
  limit = 10,
}: SketchfabSearchInput): Promise<{ count: number; results: SketchfabResult[] }> {
  const params = new URLSearchParams({
    type: 'models',
    q: query,
    downloadable: 'true',
    count: String(limit),
  })
  if (license !== 'any' && LICENSE_SLUGS[license]) {
    params.set('licenses', LICENSE_SLUGS[license])
  }

  const res = await fetch(`${BASE}/search?${params}`)
  if (!res.ok) throw new Error(`Sketchfab ${res.status}: ${await res.text()}`)
  const data = (await res.json()) as { results: SketchfabModel[] }

  const token = process.env.SKETCHFAB_TOKEN
  const results: SketchfabResult[] = await Promise.all(
    data.results.slice(0, limit).map(async (m) => ({
      uid: m.uid,
      name: m.name,
      author: m.user?.username ?? 'unknown',
      license: m.license?.slug ?? 'unknown',
      thumbnail: m.thumbnails?.images?.[0]?.url ?? null,
      page_url: m.viewerUrl,
      download_url: token ? await fetchDownloadUrl(m.uid, token) : null,
      face_count: m.faceCount ?? null,
      vertex_count: m.vertexCount ?? null,
    })),
  )

  return { count: results.length, results }
}

async function fetchDownloadUrl(uid: string, token: string): Promise<string | null> {
  const r = await fetch(`${BASE}/models/${uid}/download`, {
    headers: { Authorization: `Token ${token}` },
  })
  if (!r.ok) return null
  const j = (await r.json()) as { glb?: { url: string }; gltf?: { url: string } }
  return j.glb?.url ?? j.gltf?.url ?? null
}

interface SketchfabModel {
  uid: string
  name: string
  viewerUrl: string
  faceCount?: number
  vertexCount?: number
  user?: { username: string }
  license?: { slug: string }
  thumbnails?: { images?: Array<{ url: string }> }
}
