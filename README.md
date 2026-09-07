# MyBotica — portable Codex workspace

This private repository preserves the complete MyBotica project folder, the repository-scoped skills used to create it, reproducibility settings, and a sanitized archive of the related Codex conversations and tool activity.

## Restore on another Codex installation

```bash
git clone https://github.com/OLYMARKES/mybotica-codex-workspace.git mybotica-codex-workspace
cd mybotica-codex-workspace
git lfs pull
./tools/bootstrap.sh
```

Then add/open this folder as a local Codex project, mark the repository as trusted, and start a new task from the repository root with:

```text
Read AGENTS.md and RESTORE.md completely. Verify the workspace with ./tools/verify_clone.sh. Then read PRODUCT.md, DESIGN.md, and the relevant prior transcript in codex-history/transcripts/ before continuing the MyBotica work.
```

Repository skills under `.agents/skills/` are discovered automatically by Codex when a task starts in this repository. Project defaults are in `.codex/config.toml`.

## What is preserved

- All project files, media, briefs, prompts, exports, and nested HyperFrames projects.
- All repository-scoped Higgsfield, HyperFrames, Impeccable, carousel, and related skills used in the work.
- Six user-facing Codex tasks plus their spawned subagent/approval tasks, exported as sanitized JSON.
- Human-readable user/assistant transcripts in `codex-history/transcripts/`.
- Tool calls, command outputs, file changes, model metadata, and subagent relationships in `codex-history/threads/`.
- Extracted binary payloads from conversation records, deduplicated in `codex-history/assets/`.
- A machine-verifiable file manifest in `PROJECT-MANIFEST.json`.

## What cannot be cloned one-for-one

Codex task IDs, UI state, account entitlements, hidden platform prompts, model implementation, browser sessions, OAuth grants, secrets, approval history, and live third-party state are controlled by the Codex installation or external account. They cannot safely be reconstructed from Git.

The repository therefore preserves the maximum safe, portable layer: project files, instructions, skills, configuration defaults, readable transcripts, and sanitized structured event history. It does not claim that a cloned task will have the same internal ID or byte-identical model behavior.

See `RESTORE.md` for the full setup matrix and `codex-history/README.md` for archive details.

## Refresh the archive

On the original Mac, after conversations finish:

```bash
python3 tools/export_codex_history.py
python3 tools/build_manifest.py
./tools/secret_scan.sh
```

The exporter reads only tasks whose working directory exactly matches this repository. It removes private chain-of-thought, redacts common secret formats, extracts large binary payloads into deduplicated files, and records a redaction report.
