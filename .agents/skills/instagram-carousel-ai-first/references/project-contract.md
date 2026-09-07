# Project Contract

Use this exact shape for each carousel project:

```text
projects/<project_slug>/
  source/
  build/
  output/
    png/
    zip/
  manifest.yaml
  status.yaml
  commands.md
```

## Required `manifest.yaml` fields

- `project_slug`
- `title`
- `owner`
- `language`
- `inputs`
- `outputs`
- `canonical_build`

## Required `status.yaml` fields

- `state` (`draft|review|approved|published|archived`)
- `updated_at` (ISO timestamp)
- `agent`
- `notes` (list)

## Canonical Build Rule

Keep exactly one canonical `build` file in `manifest.yaml`. If multiple variants exist, keep alternatives but point `canonical_build` to one final choice.

