#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

test -f AGENTS.md
test -f RESTORE.md
test -f .codex/config.toml
test -f skills-lock.json
test -f codex-history/manifest.json
test -f PROJECT-MANIFEST.json

python3 -m json.tool PROJECT-MANIFEST.json >/dev/null
python3 -m json.tool codex-history/manifest.json >/dev/null

skill_count="$(find .agents/skills -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l | tr -d ' ')"
if ((skill_count < 20)); then
  echo "Expected at least 20 repository skills; found $skill_count"
  exit 1
fi

if git lfs version >/dev/null 2>&1; then
  missing_lfs="$(git lfs ls-files --all --name-only | while IFS= read -r file_path; do test -f "$file_path" || echo "$file_path"; done)"
  if [[ -n "$missing_lfs" ]]; then
    echo "Missing Git LFS objects:"
    echo "$missing_lfs"
    exit 1
  fi
else
  echo "git-lfs is required for a complete clone"
  exit 1
fi

./tools/secret_scan.sh
echo "Clone verification passed."

