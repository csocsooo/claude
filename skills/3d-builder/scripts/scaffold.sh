#!/usr/bin/env bash
# scaffold.sh — copy the r3f-vite template into a new project directory.
#
# Usage:  scaffold.sh <target-dir> [project-name]
# Example: scaffold.sh ./my-cafe coffee-shop
set -euo pipefail

TARGET="${1:-}"
NAME="${2:-r3f-site}"

if [[ -z "$TARGET" ]]; then
  echo "Usage: scaffold.sh <target-dir> [project-name]" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/../templates/r3f-vite"

if [[ ! -d "$TEMPLATE_DIR" ]]; then
  echo "Template not found at $TEMPLATE_DIR" >&2
  exit 1
fi

if [[ -e "$TARGET" ]]; then
  echo "Target $TARGET already exists, refusing to overwrite." >&2
  exit 1
fi

mkdir -p "$TARGET"
cp -r "$TEMPLATE_DIR/." "$TARGET/"

# Replace project name placeholder
sed -i.bak "s/__PROJECT_NAME__/$NAME/g" "$TARGET/package.json"
rm -f "$TARGET/package.json.bak"

echo "Scaffolded $NAME at $TARGET"
echo "Next steps:"
echo "  cd $TARGET && npm install && npm run dev"
echo "Then have Claude replace the __PLACEHOLDER__ tokens in src/ for your theme."
