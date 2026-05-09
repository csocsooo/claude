#!/usr/bin/env bash
# optimize-glb.sh — run draco compression + texture downsizing on a .glb.
#
# Usage: optimize-glb.sh <input.glb> [output.glb]
# Requires: npx (gltf-transform pulled on demand).
set -euo pipefail

INPUT="${1:-}"
OUTPUT="${2:-${INPUT%.glb}.opt.glb}"

if [[ -z "$INPUT" || ! -f "$INPUT" ]]; then
  echo "Usage: optimize-glb.sh <input.glb> [output.glb]" >&2
  exit 1
fi

BEFORE=$(wc -c <"$INPUT" | tr -d ' ')

npx --yes @gltf-transform/cli optimize "$INPUT" "$OUTPUT" \
  --compress draco \
  --texture-compress webp \
  --texture-size 1024

AFTER=$(wc -c <"$OUTPUT" | tr -d ' ')
SAVED=$(( (BEFORE - AFTER) * 100 / BEFORE ))
echo "Before: $BEFORE bytes"
echo "After:  $AFTER bytes"
echo "Saved:  ${SAVED}%"
