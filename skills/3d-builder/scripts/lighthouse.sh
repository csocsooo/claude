#!/usr/bin/env bash
# lighthouse.sh — run a Lighthouse audit against a local dev server or live URL.
#
# Usage: lighthouse.sh <url> [output-dir]
# Example: lighthouse.sh http://localhost:5173 ./lighthouse-report
#          lighthouse.sh https://arnox-rebrand.vercel.app
#
# Uses unlighthouse-ci (free, no auth). Mobile preset, JSON + HTML report.
set -euo pipefail

URL="${1:-}"
OUT="${2:-./lighthouse-report}"

if [[ -z "$URL" ]]; then
  echo "Usage: lighthouse.sh <url> [output-dir]" >&2
  exit 1
fi

mkdir -p "$OUT"

npx --yes lighthouse "$URL" \
  --preset=desktop \
  --output=json --output=html \
  --output-path="$OUT/report" \
  --chrome-flags="--headless --no-sandbox --disable-gpu" \
  --quiet

echo ""
echo "Report → $OUT/report.html"
echo ""
# Extract scores from JSON for quick glance
node -e "
const r = require('$OUT/report.report.json');
const c = r.categories;
console.log('Performance:    ' + Math.round(c.performance.score * 100));
console.log('Accessibility:  ' + Math.round(c.accessibility.score * 100));
console.log('Best practices: ' + Math.round(c['best-practices'].score * 100));
console.log('SEO:            ' + Math.round(c.seo.score * 100));
" 2>/dev/null || true
