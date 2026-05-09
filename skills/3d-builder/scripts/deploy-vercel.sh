#!/usr/bin/env bash
# deploy-vercel.sh — first-time Vercel deploy via CLI (free tier).
#
# Usage: deploy-vercel.sh [project-dir]
# Requires: npx (vercel CLI pulled on demand). Will prompt for login first run.
set -euo pipefail

DIR="${1:-.}"
cd "$DIR"

if [[ ! -f package.json ]]; then
  echo "No package.json found in $DIR — is this a project root?" >&2
  exit 1
fi

# Build first to fail fast on type errors
npm run build

# --yes accepts default project settings; --prod deploys to production URL
npx --yes vercel deploy --prod --yes
