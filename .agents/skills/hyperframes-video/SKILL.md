---
name: hyperframes-video
description: Create and edit HTML-based videos in HyperFrames. Use when Codex needs to scaffold a HyperFrames project, author or fix `index.html` / `compositions/*.html`, add GSAP animation, captions, narration, transitions, audio-reactive motion, or validate and render HTML-to-video output with `npx hyperframes`.
---

# HyperFrames Video

HyperFrames uses plain HTML as the video source of truth. Build with HTML, CSS, and GSAP; keep the structure deterministic so preview, validation, and rendering all agree.

## Quick Start

1. Confirm the target: duration, aspect ratio, assets, and visual direction.
2. If the user is starting fresh, scaffold with `npx hyperframes init ...`. See [references/cli.md](references/cli.md).
3. Read the existing project before editing: `meta.json`, `index.html`, `compositions/`, and `assets/`.
4. Build the fully visible layout state first, then add animation.
5. Run `npx hyperframes lint` and `npx hyperframes validate` before previewing or rendering.

## Workflow

### 1. Lock the visual identity first

Do not author generic video UI. Before writing composition HTML, determine:

- mood and style
- light vs dark canvas
- brand colors, fonts, and references

If the project already has `DESIGN.md`, `visual-style.md`, or equivalent style notes, follow them. If not, create a minimal design note before coding so layout and motion choices stay coherent.

### 2. Treat layout as the ground truth

For each scene, identify the hero frame: the moment where all key elements are fully visible and properly placed.

- Write static HTML and CSS for that frame first.
- Make the main content container fill the scene with `width: 100%`, `height: 100%`, padding, flex/grid, and `box-sizing: border-box`.
- Use absolute positioning for decorative layers, not for the main content stack.
- Add entrance motion with `gsap.from()` and exits with `gsap.to()` only after the static layout is correct.

This avoids invisible overlap bugs that only appear during render.

### 3. Follow the composition contract exactly

Every root composition needs:

- `data-composition-id`
- `data-start`
- `data-width`
- `data-height`

Every timed element needs:

- `class="clip"`
- `data-start`
- `data-duration` when required
- `data-track-index`

Media rules:

- video must be `muted playsinline`
- audio must use separate `<audio>` elements
- do not drive playback manually in scripts

Animation rules:

- create GSAP timelines with `{ paused: true }`
- register every timeline on `window.__timelines[compositionId]`
- keep timeline construction synchronous

### 4. Animate like a video editor, not a web app

- Animate visual properties only: opacity, transforms, colors, border radius, filters when needed.
- Do not animate video element dimensions directly; animate a wrapper around the video.
- Prefer varied entrance patterns across a scene instead of repeating the same tween.
- In multi-scene videos, add transitions between scenes instead of jump cuts.
- Let transitions handle scene exits. Reserve full fade-outs for the final scene.

If the task needs exact command syntax, read [references/cli.md](references/cli.md). If the task smells like a structural bug, read [references/guardrails.md](references/guardrails.md) before editing.

### 5. Keep renders deterministic

Never rely on wall-clock or async setup during composition boot:

- no `Math.random()` unless seeded
- no `Date.now()`
- no `fetch()` or delayed timeline assembly
- no infinite repeats

If repeating motion is necessary, compute a finite repeat count from the composition duration.

### 6. Validate before delivery

Minimum completion bar:

1. `npx hyperframes lint`
2. `npx hyperframes validate`
3. `npx hyperframes preview` for visual inspection
4. `npx hyperframes render` for the requested delivery format

If the user gives a website or URL and wants a promo/demo video, follow [references/website-to-video.md](references/website-to-video.md).

## Read These References When Needed

- [references/cli.md](references/cli.md): scaffold, lint, preview, render, TTS, transcription, troubleshooting commands
- [references/guardrails.md](references/guardrails.md): non-negotiable structure rules and common breakages
- [references/website-to-video.md](references/website-to-video.md): source-to-video workflow when input is a URL or site
