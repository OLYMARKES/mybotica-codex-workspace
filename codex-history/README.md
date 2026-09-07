# Codex conversation archive

This directory is a safe, portable export of every Codex task whose recorded working directory exactly matched the repository root at export time. It includes visible user tasks, spawned subagents, and approval/guardian tasks.

- `manifest.json` — task metadata and parent/child relationships.
- `transcripts/` — readable user and assistant messages.
- `threads/` — sanitized structured event history, ordered by turn and rollout ordinal.
- `assets/` — large binary payloads extracted from event JSON and deduplicated by SHA-256.
- `tools-used.json` — observed event/tool inventory.
- `skills-used.txt` — skill paths observed in commands and tool payloads.
- `redaction-report.json` — counts of removed secrets, private reasoning, and extracted binaries.

The exporter intentionally removes private chain-of-thought. It retains any available reasoning summaries because those are part of the visible/auditable task record. Common credentials and authorization values are redacted. Large base64 blobs are decoded into `assets/` and replaced by content-addressed references.

This is not a supported task-import database. Do not copy the original Codex SQLite databases or `auth.json` into another installation.

