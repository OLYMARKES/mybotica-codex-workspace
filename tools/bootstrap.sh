#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

required=(git python3 node npm ffmpeg)
missing=()
for command_name in "${required[@]}"; do
  command -v "$command_name" >/dev/null 2>&1 || missing+=("$command_name")
done

if ! git lfs version >/dev/null 2>&1; then
  missing+=("git-lfs")
else
  git lfs install --local >/dev/null
  git lfs pull
fi

if ((${#missing[@]})); then
  echo "Missing required software: ${missing[*]}"
  echo "Install it, then run this script again."
  exit 1
fi

echo "Portable skills: $(find .agents/skills -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l | tr -d ' ')"
echo "Nested agent instruction files: $(find videos -name AGENTS.md | wc -l | tr -d ' ')"
echo "Bootstrap checks passed. Open this repository as a trusted local Codex project."

