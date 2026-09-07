#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

pattern='(sk-[A-Za-z0-9_-]{16,}|github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|[0-9]{6,12}:[A-Za-z0-9_-]{20,}|-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----)'

if rg -l -uuu --hidden --glob '!.git/**' --glob '!.codex-private/**' --glob '!node_modules/**' --glob '!*.png' --glob '!*.jpg' --glob '!*.jpeg' --glob '!*.gif' --glob '!*.webp' --glob '!*.mp4' --glob '!*.mov' --glob '!*.wav' --glob '!*.mp3' --glob '!*.pdf' --glob '!*.zip' --glob '!*.bin' --glob '!tools/secret_scan.sh' -e "$pattern" .; then
  echo "Potential secret material found in the files listed above. Do not push."
  exit 1
fi

otp_pattern='(?<![A-Z0-9_-])\b[A-Z0-9]{4}-[A-Z0-9]{4}\b(?![A-Z0-9_-])|(?i)(?:typeText|fill)\s*\(\s*"[A-Z0-9]{8}"'
if rg -l -P -uuu --hidden --glob '!.git/**' --glob '!.codex-private/**' --glob '!node_modules/**' --glob '!tools/secret_scan.sh' -e "$otp_pattern" codex-history; then
  echo "Potential one-time authentication code found in the conversation archive. Do not push."
  exit 1
fi

auth_session_pattern='(?i)(?:accounts\.google\.com|github\.com/login)[^\s"'"'"'<>]*\?[^\s"'"'"'<>]*|(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])'
if rg -l -P -uuu --hidden --glob '!.git/**' --glob '!.codex-private/**' --glob '!node_modules/**' --glob '!tools/secret_scan.sh' -e "$auth_session_pattern" codex-history; then
  echo "Potential login-session URL or IP address found in the conversation archive. Do not push."
  exit 1
fi

for forbidden in auth.json cookies.json .env; do
  if git ls-files | rg -q "(^|/)${forbidden//./\\.}($|\.)"; then
    echo "Forbidden tracked credential file: $forbidden"
    exit 1
  fi
done

echo "Secret scan passed."
