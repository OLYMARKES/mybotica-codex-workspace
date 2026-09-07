# MyBotica workspace — agent instructions

This repository is the portable source of truth for the MyBotica work created in Codex.

## Start here

- Read `README.md`, `RESTORE.md`, `PRODUCT.md`, and `DESIGN.md` before changing deliverables.
- Treat `codex-history/` as an immutable audit archive. Do not rewrite exported history by hand.
- Repository-scoped skills live in `.agents/skills/`. Load every skill required by the task before acting.
- Preserve existing Russian filenames and user-facing Russian copy unless the user asks otherwise.
- Do not fabricate product capabilities, customer results, pricing, or social proof.
- Keep generated media, source files, briefs, prompts, and final exports together. Never replace source assets with lower-quality derivatives.

## Browser and Telegram

- For Telegram tasks, always use Codex's built-in in-app browser.
- Never control an external browser, Chrome, the native Telegram app, or another desktop app unless the user explicitly asks in that task.
- If the task cannot be completed in the in-app browser, stop and request permission before switching surfaces.
- Never commit login sessions, cookies, OTPs, API keys, OAuth tokens, browser profiles, or `.env` files.

## Exactness and reproducibility

- Keep the model defaults from `.codex/config.toml` unless the user explicitly overrides them.
- Before delivery, run `./tools/verify_clone.sh`.
- After adding or changing project artifacts, run `python3 tools/build_manifest.py` and review `PROJECT-MANIFEST.json`.
- After a Codex conversation changes, refresh the safe history export with `python3 tools/export_codex_history.py`.
- Use Git LFS for binary media. Do not remove LFS rules or recommit LFS objects as ordinary Git blobs.

## Video subprojects

- Nested `videos/*/AGENTS.md` files override this file for their subtree.
- For HyperFrames work, follow the vendored HyperFrames skills and the nested project instructions.
- Run each video's documented check before rendering or handing it off.

## Security boundary

- `codex-history/` is sanitized for version control; `.codex-private/` is local-only and must never be committed.
- Run `./tools/secret_scan.sh` before every push.
- If a secret is detected, stop. Remove it from the working tree and Git history before pushing.
- External services and plugins must be reauthenticated on each machine. Authentication state is intentionally not portable.

