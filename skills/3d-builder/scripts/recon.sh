#!/usr/bin/env bash
# recon.sh — extract brand assets from a target URL.
#
# Usage: recon.sh <url> [output-dir]
# Example: recon.sh https://arnox.hu ./recon-output
#
# Produces in <output-dir>/:
#   page.html               raw HTML
#   colors.txt              all unique hex colors found in HTML + linked CSS
#   colors-top.txt          top 10 most frequent colors (good brand-palette guess)
#   fonts.txt               font-family declarations + Google Fonts URLs
#   copy.md                 title, meta description, H1/H2 headings
#   image-urls.txt          all <img src> + og:image + apple-touch-icon URLs
#   images/                 every image downloaded locally
#   logo-candidates.txt     URLs whose path/alt/class contains "logo" or "brand"
#   recon.json              machine-readable summary for downstream tools
#
# Best-effort: relies on curl + grep + sed. For sites that lazy-render with
# JS only, supplement with WebFetch from Claude.
set -euo pipefail

URL="${1:-}"
OUT="${2:-./recon-output}"

if [[ -z "$URL" ]]; then
  echo "Usage: recon.sh <url> [output-dir]" >&2
  exit 1
fi

mkdir -p "$OUT/images"
HTML="$OUT/page.html"

# Derive scheme + host for relative URL resolution
HOST=$(echo "$URL" | sed -E 's|(https?://[^/]+).*|\1|')
DIR=$(echo "$URL" | sed -E 's|(https?://[^/]+/.*)/[^/]*$|\1|; t; s|.*|'"$HOST"'|')

resolve_url() {
  local u="$1"
  case "$u" in
    http*) echo "$u" ;;
    //*) echo "https:$u" ;;
    /*) echo "${HOST}${u}" ;;
    *) echo "${DIR}/${u}" ;;
  esac
}

# Fetch HTML with a real-ish UA
curl --fail --location --silent --max-time 30 \
  -A "Mozilla/5.0 (compatible; recon.sh/0.1)" \
  -o "$HTML" "$URL"

echo "Fetched $URL → $HTML ($(wc -c <"$HTML" | tr -d ' ') bytes)"

# ---------- COLORS ----------
{
  grep -oiE '#[0-9a-f]{6}' "$HTML" || true
  grep -oiE 'rgba?\([^)]+\)' "$HTML" || true
} > "$OUT/colors.raw" || true

# Pull from linked CSS too (hex + rgb)
grep -oiE 'href="[^"]+\.css[^"]*"' "$HTML" \
  | sed 's/href="//; s/"$//' \
  | while read -r css; do
      [[ -z "$css" ]] && continue
      css_url=$(resolve_url "$css")
      css_body=$(curl --fail --location --silent --max-time 10 "$css_url" 2>/dev/null || true)
      [[ -z "$css_body" ]] && continue
      echo "$css_body" | grep -oiE '#[0-9a-f]{6}' || true
      echo "$css_body" | grep -oiE '#[0-9a-f]{3}\b' \
        | awk '{ printf "#%s%s%s%s%s%s\n", substr($1,2,1),substr($1,2,1),substr($1,3,1),substr($1,3,1),substr($1,4,1),substr($1,4,1) }' || true
      echo "$css_body" | grep -oiE 'rgba?\([^)]+\)' || true
    done >> "$OUT/colors.raw" || true

sort -u "$OUT/colors.raw" > "$OUT/colors.txt"
sort "$OUT/colors.raw" | uniq -c | sort -rn | head -10 > "$OUT/colors-top.txt"
rm -f "$OUT/colors.raw"

# ---------- FONTS ----------
{
  echo "# CSS font-family declarations"
  grep -oiE 'font-family:[^;}"]+' "$HTML" | sort -u || true
  echo ""
  echo "# Google Fonts URLs"
  grep -oiE 'fonts\.googleapis\.com/css[^"]*' "$HTML" | sort -u || true
} > "$OUT/fonts.txt"

# ---------- COPY ----------
{
  echo "# Copy from $URL"
  echo ""
  echo "## <title>"
  grep -oiE '<title[^>]*>[^<]+</title>' "$HTML" | sed -E 's|<[^>]+>||g' || true
  echo ""
  echo "## meta description"
  grep -oiE 'name="description"[^>]*content="[^"]+"' "$HTML" \
    | grep -oiE 'content="[^"]+"' | sed 's/content="//; s/"$//' || true
  echo ""
  echo "## meta og:title / og:description"
  grep -oiE 'property="og:(title|description)"[^>]*content="[^"]+"' "$HTML" \
    | grep -oiE 'content="[^"]+"' | sed 's/content="//; s/"$//' || true
  echo ""
  echo "## H1 / H2 headings"
  grep -oiE '<h[12][^>]*>[^<]+</h[12]>' "$HTML" | sed -E 's|<[^>]+>||g' | sort -u || true
  echo ""
  echo "## First 5 paragraphs"
  grep -oiE '<p[^>]*>[^<]{20,400}</p>' "$HTML" | sed -E 's|<[^>]+>||g' | head -5 || true
} > "$OUT/copy.md"

# ---------- IMAGES ----------
{
  grep -oiE '<img[^>]+src="[^"]+"' "$HTML" \
    | grep -oiE 'src="[^"]+"' | sed 's/src="//; s/"$//' || true
  grep -oiE 'property="og:image"[^>]*content="[^"]+"' "$HTML" \
    | grep -oiE 'content="[^"]+"' | sed 's/content="//; s/"$//' || true
  grep -oiE 'rel="apple-touch-icon"[^>]*href="[^"]+"' "$HTML" \
    | grep -oiE 'href="[^"]+"' | sed 's/href="//; s/"$//' || true
  grep -oiE 'rel="icon"[^>]*href="[^"]+"' "$HTML" \
    | grep -oiE 'href="[^"]+"' | sed 's/href="//; s/"$//' || true
} | sort -u > "$OUT/image-urls.txt"

while read -r raw; do
  [[ -z "$raw" ]] && continue
  full=$(resolve_url "$raw")
  name=$(echo "$full" | sed -E 's|^https?://||; s|[?#].*$||; s|/|_|g')
  curl --fail --silent --max-time 30 -L -o "$OUT/images/$name" "$full" 2>/dev/null || true
done < "$OUT/image-urls.txt"

# ---------- LOGO CANDIDATES ----------
grep -iE '(logo|brand)' "$HTML" \
  | grep -oiE '(src|href)="[^"]+\.(svg|png|jpg|jpeg|webp|ico)' \
  | sed -E 's/^(src|href)="//' | sort -u > "$OUT/logo-candidates.txt"

# ---------- JSON SUMMARY ----------
TITLE=$(grep -oiE '<title[^>]*>[^<]+</title>' "$HTML" | head -1 | sed -E 's|<[^>]+>||g' | sed 's/"/\\"/g')
DESC=$(grep -oiE 'name="description"[^>]*content="[^"]+"' "$HTML" | head -1 \
  | grep -oiE 'content="[^"]+"' | sed 's/content="//; s/"$//' | sed 's/"/\\"/g')
COLOR_COUNT=$(wc -l <"$OUT/colors.txt" | tr -d ' ')
IMG_COUNT=$(ls -1 "$OUT/images" 2>/dev/null | wc -l | tr -d ' ')
TOP_COLOR=$(head -1 "$OUT/colors-top.txt" | awk '{print $2}')

cat > "$OUT/recon.json" <<JSON
{
  "url": "$URL",
  "host": "$HOST",
  "title": "$TITLE",
  "description": "$DESC",
  "color_count": $COLOR_COUNT,
  "top_color": "$TOP_COLOR",
  "image_count": $IMG_COUNT,
  "files": {
    "html": "page.html",
    "colors": "colors.txt",
    "colors_top": "colors-top.txt",
    "fonts": "fonts.txt",
    "copy": "copy.md",
    "image_urls": "image-urls.txt",
    "images_dir": "images/",
    "logo_candidates": "logo-candidates.txt"
  }
}
JSON

echo ""
echo "✓ Recon complete → $OUT/"
echo "  $COLOR_COUNT unique colors, $IMG_COUNT images downloaded"
echo "  Top color: $TOP_COLOR"
echo ""
echo "Next: have Claude read $OUT/copy.md + $OUT/colors-top.txt + ls $OUT/images/"
echo "Then run: /3d-site <slug> business --recon $OUT"
