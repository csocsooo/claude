#!/usr/bin/env bash
# scaffold.sh — copy a 3D website template into a new project directory.
#
# Usage:  scaffold.sh <target-dir> <project-name> [template]
# Example: scaffold.sh ./my-cafe coffee-shop vite
#          scaffold.sh ./arnox arnox-rebrand business
#
# Templates available (under skills/3d-builder/templates/):
#   vite      — minimal hero/features/contact (default)
#   business  — nav + hero + 6 services + pinned project showcase + form + footer
set -euo pipefail

TARGET="${1:-}"
NAME="${2:-r3f-site}"
TEMPLATE="${3:-vite}"

if [[ -z "$TARGET" ]]; then
  echo "Usage: scaffold.sh <target-dir> <project-name> [template]" >&2
  echo "Templates: vite (default), business" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
case "$TEMPLATE" in
  vite)     TEMPLATE_DIR="$SCRIPT_DIR/../templates/r3f-vite" ;;
  business) TEMPLATE_DIR="$SCRIPT_DIR/../templates/r3f-business" ;;
  *)        echo "Unknown template: $TEMPLATE (vite|business)" >&2; exit 1 ;;
esac

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

echo "Scaffolded $NAME at $TARGET (template: $TEMPLATE)"
echo ""
echo "Next steps:"
echo "  cd $TARGET && npm install && npm run dev"
echo ""
echo "Then have Claude replace the __PLACEHOLDER__ tokens for your theme."
echo "Tokens are listed at the top of skills/3d-builder/SKILL.md."
