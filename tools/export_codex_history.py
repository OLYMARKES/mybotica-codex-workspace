#!/usr/bin/env python3
"""Export this workspace's Codex history without credentials or private reasoning."""

from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
import os
import re
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SECRET_KEYS = {
    "access_token", "refresh_token", "api_key", "apikey", "authorization",
    "password", "passwd", "secret", "client_secret", "bot_token", "cookie",
    "set-cookie", "session_token",
}

OTP_DISPLAY_PATTERN = re.compile(
    r"(?<![A-Z0-9_-])\b[A-Z0-9]{4}-[A-Z0-9]{4}\b(?![A-Z0-9_-])"
)
DISCOVERED_OTP_COMPACT: set[str] = set()
AUTH_URL_PATTERN = re.compile(
    r"(?:https?://)?(?:accounts\.google\.com|github\.com/login)"
    r"[^\s\"'<>]*\?[^\s\"'<>]*",
    re.I,
)
IPV4_PATTERN = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")

SECRET_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    re.compile(r"\b\d{6,12}:[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"(?i)(authorization\s*[:=]\s*bearer\s+)[A-Za-z0-9._~+/-]{10,}"),
    re.compile(r"(?i)([?&](?:token|access_token|api_key|key|secret)=)[^&#\s]+"),
    # GitHub device-flow codes are short-lived, but they are still OTP material
    # and must never be preserved in a repository or its history.
    re.compile(
        r"(?i)((?:one[- ]time\s+code|device\s+code|user\s+code|"
        r"одноразов(?:ый|ого)\s+код|код(?:\s+тот\s+же)?)[^\n]{0,120}?)"
        r"\b[A-Z0-9]{4}-[A-Z0-9]{4}\b"
    ),
    # Browser automation can contain the same code without its display hyphen.
    re.compile(r"(?i)((?:typeText|fill)\s*\(\s*[\"'])[A-Z0-9]{8}(?=[\"'])"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")))
    return parser.parse_args()


def connect_readonly(path: Path) -> sqlite3.Connection:
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA query_only=ON")
    return con


def redact_text(text: str, report: Counter) -> str:
    result = text
    result, count = AUTH_URL_PATTERN.subn("[REDACTED_AUTH_URL]", result)
    report["auth_url_redactions"] += count
    result, count = IPV4_PATTERN.subn("[REDACTED_IP]", result)
    report["ip_address_redactions"] += count
    displayed_codes = [match.group(0) for match in OTP_DISPLAY_PATTERN.finditer(result)]
    DISCOVERED_OTP_COMPACT.update(code.replace("-", "") for code in displayed_codes)
    result, count = OTP_DISPLAY_PATTERN.subn("[REDACTED]", result)
    report["secret_pattern_redactions"] += count
    for compact_code in DISCOVERED_OTP_COMPACT:
        result, count = re.subn(
            rf"(?<![A-Z0-9_-]){re.escape(compact_code)}(?![A-Z0-9_-])",
            "[REDACTED]",
            result,
        )
        report["secret_pattern_redactions"] += count
    for pattern in SECRET_PATTERNS:
        result, count = pattern.subn(lambda m: (m.group(1) if m.lastindex else "") + "[REDACTED]", result)
        report["secret_pattern_redactions"] += count
    return result


def binary_extension(data: bytes) -> str:
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if data.startswith((b"GIF87a", b"GIF89a")):
        return ".gif"
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return ".webp"
    if data.startswith(b"RIFF") and data[8:12] == b"WAVE":
        return ".wav"
    if data.startswith(b"%PDF"):
        return ".pdf"
    if len(data) > 12 and data[4:8] == b"ftyp":
        return ".mp4"
    return ".bin"


def maybe_extract_binary(text: str, assets_dir: Path, report: Counter) -> dict[str, Any] | None:
    candidate = text
    mime_ext = None
    match = re.match(r"^data:([a-z0-9.+-]+/[a-z0-9.+-]+);base64,(.+)$", text, re.I | re.S)
    if match:
        mime = match.group(1).lower()
        candidate = match.group(2)
        mime_ext = {
            "image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp",
            "image/gif": ".gif", "audio/wav": ".wav", "application/pdf": ".pdf",
            "video/mp4": ".mp4",
        }.get(mime)
    elif len(text) < 100_000 or not re.fullmatch(r"[A-Za-z0-9+/=\r\n]+", text):
        return None

    try:
        data = base64.b64decode(candidate, validate=False)
    except (ValueError, binascii.Error):
        return None
    if len(data) < 50_000:
        return None

    digest = hashlib.sha256(data).hexdigest()
    ext = mime_ext or binary_extension(data)
    asset_path = assets_dir / f"{digest}{ext}"
    if not asset_path.exists():
        asset_path.write_bytes(data)
        report["binary_assets_written"] += 1
        report["binary_bytes_written"] += len(data)
    report["binary_payload_references"] += 1
    return {"$asset": f"../assets/{asset_path.name}", "sha256": digest, "bytes": len(data)}


def sanitize(value: Any, assets_dir: Path, report: Counter, key: str = "") -> Any:
    if key.lower() in SECRET_KEYS:
        report["secret_key_redactions"] += 1
        return "[REDACTED]"
    if isinstance(value, dict):
        if value.get("type") == "reasoning":
            report["reasoning_items_sanitized"] += 1
            return {
                "type": "reasoning",
                "id": value.get("id"),
                "summary": sanitize(value.get("summary", []), assets_dir, report, "summary"),
                "content": "[PRIVATE_REASONING_REMOVED]",
            }
        return {k: sanitize(v, assets_dir, report, k) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize(v, assets_dir, report, key) for v in value]
    if isinstance(value, str):
        extracted = maybe_extract_binary(value, assets_dir, report)
        if extracted is not None:
            return extracted
        return redact_text(value, report)
    return value


def message_text(item: dict[str, Any]) -> str:
    if item.get("type") == "agentMessage":
        return str(item.get("text", ""))
    blocks = item.get("content", [])
    if isinstance(blocks, str):
        return blocks
    texts = []
    for block in blocks if isinstance(blocks, list) else []:
        if isinstance(block, dict) and isinstance(block.get("text"), str):
            texts.append(block["text"])
    return "\n\n".join(texts)


def collect_skill_paths(value: Any, found: set[str]) -> None:
    """Collect referenced SKILL.md paths without regexing whole serialized events."""
    if isinstance(value, dict):
        for child in value.values():
            collect_skill_paths(child, found)
    elif isinstance(value, list):
        for child in value:
            collect_skill_paths(child, found)
    elif isinstance(value, str) and "SKILL.md" in value:
        pattern = r"(?:https?://[^\s\"'`;|]+|(?:~|/)[^\s\"'`;|]+)/SKILL\.md"
        for match in re.findall(pattern, value):
            if "/path/to/skill/" not in match:
                found.add(match.strip())


def iso_time(seconds: Any) -> str | None:
    if seconds is None:
        return None
    return datetime.fromtimestamp(int(seconds), tz=timezone.utc).isoformat()


def main() -> None:
    args = parse_args()
    workspace = args.workspace.resolve()
    output = workspace / "codex-history"
    threads_dir = output / "threads"
    transcripts_dir = output / "transcripts"
    assets_dir = output / "assets"
    for directory in (output, threads_dir, transcripts_dir, assets_dir):
        directory.mkdir(parents=True, exist_ok=True)

    state_path = args.codex_home / "state_5.sqlite"
    history_path = args.codex_home / "thread_history_1.sqlite"
    if not state_path.exists() or not history_path.exists():
        raise SystemExit("Codex history databases were not found in the selected CODEX_HOME")

    state = connect_readonly(state_path)
    history = connect_readonly(history_path)
    report: Counter = Counter()

    rows = state.execute(
        """SELECT id, title, source, cwd, created_at, updated_at, archived, model,
                  reasoning_effort, approval_mode, sandbox_policy, rollout_path,
                  agent_nickname, agent_role, project_id
           FROM threads WHERE cwd = ? ORDER BY created_at_ms, id""",
        (str(workspace),),
    ).fetchall()

    manifest_threads = []
    type_counts: Counter = Counter()
    tool_counts: Counter = Counter()
    skill_paths: set[str] = set()
    for meta_row in rows:
        meta = dict(meta_row)
        safe_title = redact_text(str(meta.get("title") or "(subagent task)").strip(), report)
        try:
            source_obj = json.loads(meta.get("source") or "null")
        except json.JSONDecodeError:
            source_obj = meta.get("source")
        parent_id = None
        if isinstance(source_obj, dict):
            subagent = source_obj.get("subagent")
            if isinstance(subagent, dict):
                spawn = subagent.get("thread_spawn")
                if isinstance(spawn, dict):
                    parent_id = spawn.get("parent_thread_id")

        turn_rows = history.execute(
            "SELECT * FROM thread_turns WHERE thread_id = ? ORDER BY rollout_ordinal",
            (meta["id"],),
        ).fetchall()
        item_rows = history.execute(
            "SELECT turn_id, rollout_ordinal, item_type, item_json FROM thread_items WHERE thread_id = ? ORDER BY rollout_ordinal",
            (meta["id"],),
        ).fetchall()

        turns: dict[str, dict[str, Any]] = {}
        ordered_ids: list[str] = []
        for turn_row in turn_rows:
            turn = dict(turn_row)
            turn_id = turn["turn_id"]
            ordered_ids.append(turn_id)
            turns[turn_id] = {"metadata": sanitize(turn, assets_dir, report), "items": []}

        transcript = [
            f"# {safe_title}",
            "",
            f"- Thread ID: `{meta['id']}`",
            f"- Parent thread: `{parent_id}`" if parent_id else "- Parent thread: none",
            f"- Model: `{meta.get('model') or 'unknown'}`",
            f"- Reasoning effort: `{meta.get('reasoning_effort') or 'unknown'}`",
            f"- Created: `{iso_time(meta.get('created_at'))}`",
            "",
        ]

        orphan_index = 0
        for item_row in item_rows:
            try:
                raw_item = json.loads(item_row["item_json"])
            except json.JSONDecodeError:
                raw_item = {"type": item_row["item_type"], "raw": item_row["item_json"]}
            safe_item = sanitize(raw_item, assets_dir, report)
            item_type = item_row["item_type"] or safe_item.get("type", "unknown")
            type_counts[item_type] += 1

            tool = safe_item.get("tool") if isinstance(safe_item, dict) else None
            namespace = safe_item.get("namespace") or safe_item.get("server") if isinstance(safe_item, dict) else None
            if tool:
                tool_counts[f"{namespace + '.' if namespace else ''}{tool}"] += 1

            collect_skill_paths(safe_item, skill_paths)

            turn_id = item_row["turn_id"]
            if turn_id not in turns:
                orphan_index += 1
                turn_id = turn_id or f"orphan-{orphan_index}"
                if turn_id not in turns:
                    ordered_ids.append(turn_id)
                    turns[turn_id] = {"metadata": {"turn_id": turn_id, "status": "unknown"}, "items": []}
            turns[turn_id]["items"].append(safe_item)

            if item_type in {"userMessage", "agentMessage"}:
                text = message_text(safe_item).strip()
                if text:
                    role = "Пользователь" if item_type == "userMessage" else "Агент"
                    phase = safe_item.get("phase") if isinstance(safe_item, dict) else None
                    transcript.extend([f"## {role}" + (f" · {phase}" if phase else ""), "", text, ""])

        safe_meta = sanitize({
            **{k: v for k, v in meta.items() if k != "rollout_path"},
            "source": source_obj,
            "parent_thread_id": parent_id,
            "created_at_iso": iso_time(meta.get("created_at")),
            "updated_at_iso": iso_time(meta.get("updated_at")),
        }, assets_dir, report)
        payload = {"schema_version": 1, "thread": safe_meta, "turns": [turns[x] for x in ordered_ids]}
        (threads_dir / f"{meta['id']}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (transcripts_dir / f"{meta['id']}.md").write_text("\n".join(transcript), encoding="utf-8")

        manifest_threads.append({
            "id": meta["id"],
            "title": safe_title,
            "parent_thread_id": parent_id,
            "source": source_obj,
            "model": meta.get("model"),
            "reasoning_effort": meta.get("reasoning_effort"),
            "created_at": iso_time(meta.get("created_at")),
            "updated_at": iso_time(meta.get("updated_at")),
            "turn_count": len(turn_rows),
            "item_count": len(item_rows),
        })

    export_manifest = {
        "schema_version": 1,
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "workspace": workspace.name,
        "workspace_path_on_source_machine": str(workspace),
        "thread_count": len(manifest_threads),
        "threads": manifest_threads,
    }
    (output / "manifest.json").write_text(json.dumps(export_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "tools-used.json").write_text(
        json.dumps({"item_types": dict(type_counts), "tools": dict(tool_counts)}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output / "skills-used.txt").write_text("\n".join(sorted(skill_paths)) + "\n", encoding="utf-8")
    (output / "redaction-report.json").write_text(json.dumps(dict(report), indent=2) + "\n", encoding="utf-8")
    print(f"Exported {len(manifest_threads)} Codex tasks to {output}")


if __name__ == "__main__":
    main()
