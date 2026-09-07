# Required capabilities and versions

## Repository skills

All portable skills used by this workspace are vendored under `.agents/skills/`. `skills-lock.json` records the original Higgsfield sources and hashes.

Observed non-Higgsfield skills vendored for portability:

- `animation-vocabulary`
- `general-video`
- `hyperframes`
- `hyperframes-animation`
- `hyperframes-audio`
- `hyperframes-cli`
- `hyperframes-core`
- `hyperframes-creative`
- `hyperframes-keyframes`
- `hyperframes-registry`
- `hyperframes-video`
- `ideal-carousel`
- `impeccable`
- `instagram-carousel-ai-first`
- `media-use`
- `motion-graphics`

## Codex-provided capabilities observed

- Codex in-app Browser plugin: observed local bundle `26.818.31338`.
- Computer Use plugin: observed local bundle `1.0.1000816`.
- Visualize plugin: observed local bundle `1.0.22`.
- PDF runtime: observed local bundle `26.826.12353`.
- Image generation system skill.
- Skill installer system skill.
- Codex app tools for opening files and coordinating tasks.
- Web search.

Plugin versions are observations, not vendored executables. Install current compatible versions through Codex and reauthenticate services. Exact old plugin binaries may be unavailable on another installation.

## External software and services

- Git and Git LFS.
- Node.js and npm/npx.
- FFmpeg for media inspection/rendering.
- HyperFrames CLI versions pinned in individual `videos/*/package.json` files.
- Higgsfield CLI/service and a valid Higgsfield login for new generations.
- GitHub authentication for pushing or managing the repository.
- Telegram authentication for live channel work.

No credential is stored here.

