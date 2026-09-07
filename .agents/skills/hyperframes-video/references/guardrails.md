# HyperFrames Guardrails

Use this file when authoring or debugging compositions.

## Non-negotiable rules

- Build compositions in plain HTML, not React or another UI abstraction.
- Keep HTML as the source of truth for timing and layout.
- Register every timeline on `window.__timelines` using the exact `data-composition-id`.
- Create timelines with `{ paused: true }`.
- Add `class="clip"` to every timed element.
- Use separate `<audio>` elements; video elements stay `muted playsinline`.
- Keep timeline construction synchronous.
- Avoid `Math.random()`, `Date.now()`, and render-time network fetches.
- Avoid `repeat: -1`; compute a finite repeat count instead.

## Scene choreography

- Every scene should have entrance animation.
- Multi-scene videos should use transitions.
- Do not fade a scene out before its transition; the transition should carry the exit.
- Reserve explicit fade-out exits for the final scene.

## Frequent breakages

### Video freezes or renders badly

Cause: animating `width`, `height`, `top`, or `left` on the `<video>` element itself.

Fix: wrap the video in a non-timed container and animate the wrapper.

### Media goes out of sync

Cause: calling `play()`, `pause()`, or mutating `currentTime`.

Fix: let HyperFrames control playback from data attributes.

### Timed element is always visible

Cause: missing `class="clip"`.

Fix: add `class="clip"` and keep the timing attributes on the same element.

### Animation does not run

Cause: `window.__timelines` key does not match `data-composition-id`, or the timeline was never registered.

Fix: make the keys identical and register synchronously.

### Video cuts off too early

Cause: the resolved composition duration is shorter than the media or intended scene plan.

Fix: extend the timeline deliberately and verify with `npx hyperframes compositions`.

### Preview is sluggish

Cause: oversized images, too many heavy blur layers, or expensive effects over large regions.

Fix: resize images near canvas scale, reduce stacked `backdrop-filter` layers, and simplify effect-heavy scenes.

## Debug order

1. Run `npx hyperframes lint`.
2. Run `npx hyperframes validate`.
3. Check the root `data-composition-id`.
4. Check `window.__timelines`.
5. Check `class="clip"` and timing attributes.
6. Check whether composition duration matches the intended runtime.
