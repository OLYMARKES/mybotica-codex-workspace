# HyperFrames CLI

Use `npx hyperframes` for project setup, checks, preview, and final output.

## Typical flow

```bash
npx hyperframes init my-video
cd my-video
npx hyperframes lint
npx hyperframes validate
npx hyperframes preview
npx hyperframes render --output final.mp4
```

Lint before previewing. Validate before considering the result done.

## Scaffold

```bash
npx hyperframes init my-video
npx hyperframes init my-video --non-interactive --example blank
npx hyperframes init my-video --example warm-grain --video ./intro.mp4
npx hyperframes init my-video --audio ./track.mp3
```

Use `init` instead of hand-rolling the folder structure when starting from scratch.

Common starter examples from the docs:

- `blank`
- `warm-grain`
- `play-mode`
- `swiss-grid`
- `vignelli`
- `decision-tree`
- `kinetic-type`
- `product-promo`
- `nyt-graph`

## Quality checks

```bash
npx hyperframes lint
npx hyperframes lint --json
npx hyperframes validate
npx hyperframes validate --no-contrast
```

Use `lint` for structural issues and `validate` for runtime problems, missing assets, and contrast warnings.

## Preview

```bash
npx hyperframes preview
npx hyperframes preview --port 4567
```

Preview gives fast iteration and hot reload.

## Render

```bash
npx hyperframes render
npx hyperframes render --output final.mp4
npx hyperframes render --quality draft
npx hyperframes render --fps 60 --quality high
npx hyperframes render --format webm
npx hyperframes render --docker
```

Use:

- `draft` for quick iteration
- `standard` for review
- `high` for final delivery
- `webm` when transparency matters
- `--docker` when reproducibility matters more than speed

## Speech and captions

```bash
npx hyperframes transcribe audio.mp3
npx hyperframes transcribe video.mp4 --model medium.en --language en
npx hyperframes tts "Text here" --voice af_nova --output narration.wav
npx hyperframes tts script.txt --voice bf_emma
npx hyperframes tts --list
```

Use transcription when a source audio/video already exists. Use TTS when narration must be generated locally.

## Troubleshooting

```bash
npx hyperframes doctor
npx hyperframes browser
npx hyperframes info
npx hyperframes compositions
```

Run `doctor` first if preview or render fails. Run `compositions` when the resolved duration looks wrong.
