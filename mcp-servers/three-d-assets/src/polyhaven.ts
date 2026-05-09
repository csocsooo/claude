/**
 * Polyhaven public API wrapper. All assets are CC0.
 *
 * Docs: https://github.com/Poly-Haven/Public-API
 */
const BASE = 'https://api.polyhaven.com'

interface PolyhavenSearchInput {
  query: string
  asset_type?: 'hdris' | 'textures' | 'models'
  limit?: number
}

interface PolyhavenResult {
  slug: string
  name: string
  asset_type: string
  categories: string[]
  thumbnail: string
  download_urls: Record<string, string>
}

export async function polyhavenSearch({
  query,
  asset_type = 'hdris',
  limit = 10,
}: PolyhavenSearchInput): Promise<{ count: number; results: PolyhavenResult[] }> {
  const typeMap = { hdris: 'hdri', textures: 'texture', models: 'model' }
  const r = await fetch(`${BASE}/assets?type=${typeMap[asset_type]}`)
  if (!r.ok) throw new Error(`Polyhaven ${r.status}`)
  const all = (await r.json()) as Record<string, PolyhavenAsset>

  const q = query.toLowerCase()
  const matches = Object.entries(all)
    .filter(([slug, a]) => slug.includes(q) || a.name.toLowerCase().includes(q) || a.tags?.some((t) => t.toLowerCase().includes(q)))
    .slice(0, limit)

  const results: PolyhavenResult[] = matches.map(([slug, a]) => ({
    slug,
    name: a.name,
    asset_type,
    categories: a.categories ?? [],
    thumbnail: `https://cdn.polyhaven.com/asset_img/thumbs/${slug}.png?width=256`,
    download_urls: buildDownloadUrls(slug, asset_type),
  }))

  return { count: results.length, results }
}

function buildDownloadUrls(slug: string, type: string): Record<string, string> {
  if (type === 'hdris') {
    return {
      '1k': `https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/1k/${slug}_1k.hdr`,
      '2k': `https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/2k/${slug}_2k.hdr`,
      '4k': `https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/4k/${slug}_4k.hdr`,
    }
  }
  if (type === 'models') {
    return {
      glb_1k: `https://dl.polyhaven.org/file/ph-assets/Models/glb/1k/${slug}_1k.glb`,
      glb_2k: `https://dl.polyhaven.org/file/ph-assets/Models/glb/2k/${slug}_2k.glb`,
    }
  }
  return {
    info: `https://polyhaven.com/a/${slug}`,
  }
}

interface PolyhavenAsset {
  name: string
  categories?: string[]
  tags?: string[]
}
