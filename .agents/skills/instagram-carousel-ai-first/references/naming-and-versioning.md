# Naming and Versioning

Use stable, machine-friendly names.

## File naming rules

1. Use ASCII only: `a-z`, `0-9`, `_`, `-`, `.`
2. Use lowercase only.
3. Avoid spaces and non-latin characters.
4. Encode purpose and version in the filename.

## Recommended patterns

- Script source: `script_ru.md`
- Build variant: `carousel_v2_pink.html`
- PNG output dir: `output/png/carousel_v2_pink/`
- ZIP output: `output/zip/carousel_v2_pink.zip`

## Ambiguity policy

Do not keep names like:

- `final`
- `final2`
- `copy`
- `gold 2`

Convert ambiguous names to explicit versioned names (`v1`, `v2`, `v3`) and update `manifest.yaml`.

