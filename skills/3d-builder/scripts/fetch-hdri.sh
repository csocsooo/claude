#!/usr/bin/env bash
# fetch-hdri.sh — download a Polyhaven HDRI for environment lighting.
#
# Usage: fetch-hdri.sh <slug> [resolution] [target-path]
# Example: fetch-hdri.sh studio_small_03 1k ./public/env.hdr
#
# Browse: https://polyhaven.com/hdris
set -euo pipefail

SLUG="${1:-}"
RES="${2:-1k}"
TARGET="${3:-./public/env.hdr}"

if [[ -z "$SLUG" ]]; then
  echo "Usage: fetch-hdri.sh <slug> [resolution] [target-path]" >&2
  exit 1
fi

URL="https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/${RES}/${SLUG}_${RES}.hdr"
mkdir -p "$(dirname "$TARGET")"

curl --fail --location --retry 3 --connect-timeout 10 --max-time 120 \
  --output "$TARGET" "$URL"

echo "Downloaded HDRI: $TARGET"
echo "Use in R3F: <Environment files=\"/$(basename "$TARGET")\" background />"
