#!/usr/bin/env bash
# fetch-cc0-model.sh — download a CC0 .glb from a known asset host.
#
# Usage: fetch-cc0-model.sh <url> <target-path>
# Example: fetch-cc0-model.sh https://example.com/coffee.glb ./public/model.glb
#
# Recommended hosts:
#   - https://poly.pizza         (Google Poly archive)
#   - https://sketchfab.com      (filter: CC0 + downloadable)
#   - https://quaternius.com     (CC0 packs)
#   - https://kenney.nl/assets   (CC0 game assets)
set -euo pipefail

URL="${1:-}"
TARGET="${2:-./public/model.glb}"

if [[ -z "$URL" ]]; then
  echo "Usage: fetch-cc0-model.sh <url> <target-path>" >&2
  exit 1
fi

mkdir -p "$(dirname "$TARGET")"

# Use curl with redirect-follow + retry; timeout to avoid hanging.
curl --fail --location --retry 3 --connect-timeout 10 --max-time 120 \
  --output "$TARGET" "$URL"

SIZE=$(wc -c <"$TARGET" | tr -d ' ')
echo "Downloaded $TARGET ($SIZE bytes)"

if [[ "$SIZE" -gt 5242880 ]]; then
  echo "Warning: model >5 MB. Consider running optimize-glb.sh." >&2
fi
