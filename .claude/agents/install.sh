#!/usr/bin/env bash
#
# Az agent-hálózat telepítése GLOBÁLISAN, a ~/.claude/agents/ alá,
# hogy minden projektedben elérhető legyen.
#
# Használat (a saját gépeden, a repó gyökeréből):
#   bash .claude/agents/install.sh
#
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST_DIR="${HOME}/.claude/agents"

AGENTS=(orchestrator kutato fejleszto tesztelo kodellenor)

echo "Agent-hálózat telepítése ide: ${DEST_DIR}"
mkdir -p "${DEST_DIR}"

for name in "${AGENTS[@]}"; do
  src="${SRC_DIR}/${name}.md"
  dest="${DEST_DIR}/${name}.md"
  if [[ ! -f "${src}" ]]; then
    echo "  ! hiányzik: ${src} — kihagyva"
    continue
  fi
  if [[ -f "${dest}" ]]; then
    echo "  ~ felülírás: ${name}.md (már létezett)"
  else
    echo "  + telepítve:  ${name}.md"
  fi
  cp "${src}" "${dest}"
done

echo ""
echo "Kész. Ellenőrzés a Claude Code-ban:  /agents"
echo "A felhasználó-szintű (global) agenteknek meg kell jelenniük a listában."
