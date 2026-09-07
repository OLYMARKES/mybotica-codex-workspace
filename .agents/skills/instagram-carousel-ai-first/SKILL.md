---
name: instagram-carousel-ai-first
description: Create, normalize, and export Instagram carousel projects with an AI-first reproducible workflow. Use when working on carousel scripts, HTML slide layouts, theme variants, PNG/ZIP exports, duplicate cleanup, or migration of ad-hoc carousel files into a canonical source/build/output structure with manifest and status metadata.
---

# Instagram Carousel Ai First

## Overview

Create and maintain one canonical carousel project per topic. Keep every output reproducible from files in `build/` and commands in `commands.md`.

## Execute Workflow

1. Identify a project slug and normalize scope.
2. Bootstrap or refresh the canonical structure.
3. Build or update HTML carousel files in `build/`.
4. Export `PNG` and `ZIP` deterministically.
5. Update `status.yaml` and project notes after each change.

## Bootstrap Canonical Structure

Run:

```bash
python3 scripts/init_carousel_project.py \
  --root <workspace> \
  --slug <project_slug> \
  --title "<project title>" \
  --owner "<team-or-person>" \
  --language ru
```

Use `--force` to rewrite template files when intentionally re-baselining.

Read `references/project-contract.md` before changing project schema.

## Build Carousel HTML

Keep authorable sources in:
- `source/` for scripts/theses/notes
- `build/` for HTML/CSS/JS variants

Use clear variant names:
- `carousel_v1_light.html`
- `carousel_v2_pink.html`

Follow naming and contract rules from `references/naming-and-versioning.md`.

## Export Slides

Run:

```bash
python3 scripts/export_slides.py \
  --html <workspace>/projects/<slug>/build/<variant>.html \
  --out-dir <workspace>/projects/<slug>/output/png/<variant> \
  --zip <workspace>/projects/<slug>/output/zip/<variant>.zip
```

Default selector is `.slide`. Override with `--selector` if needed.

## Quality Gates

1. Keep one canonical build variant in `manifest.yaml`.
2. Keep exported slides aligned with declared dimensions (default `1080x1350`).
3. Keep output traceable to a specific build filename and timestamp.
4. Remove or archive ambiguous duplicates (`final`, `copy`, `gold 2`) after choosing canonical versions.

## Use Bundled Resources

Use scripts:
- `scripts/init_carousel_project.py` to create deterministic project scaffolding.
- `scripts/export_slides.py` to export slides and optional zip archives.

Use references:
- `references/project-contract.md` for required layout and metadata.
- `references/naming-and-versioning.md` for naming policy and canonical decisions.
- `references/iteration-loop.md` for the edit-review-export loop.

Use assets:
- `assets/templates/manifest.yaml`
- `assets/templates/status.yaml`
- `assets/templates/commands.md`
- `assets/templates/carousel_v1.html`
