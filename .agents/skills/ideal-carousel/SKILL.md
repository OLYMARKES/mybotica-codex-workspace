---
name: ideal-carousel
description: Create high-performing Instagram carousel scripts and slide layouts using a repeatable 8–12 slide blueprint (default 10). Use when asked (in RU/EN) to “make an ideal carousel”, write slide-by-slide copy, craft hooks/CTA, turn a text idea into a carousel outline, or produce exportable HTML slides (1080×1350 with `.slide`) and a canonical project structure (source/build/output).
---

# Ideal Carousel

## Workflow (fast)

Goal: ship a carousel that is readable in 1 second per slide, has one idea per slide, and ends with a concrete action.

### 0) Get inputs (ask, then assume)

- Topic + audience + promise (benefit).
- Primary action: save / comment / DM / click / buy.
- Tone (calm, bold, expert), taboo words, examples of prior posts (optional).
- Slide count: 8–12 (default 10).

### 1) Pick the “one goal”

Write it as: “After this carousel, the reader will do ___”.

### 2) Draft cover hooks (choose 1)

- `X без Y` (e.g., “Лиды без прогрева”)
- `3 ошибки в …`
- `Шаги: от A до B`
- `Чеклист: сохрани и сделай`

Rule: the cover must be readable without context.

### 3) Use the 10-slide blueprint (default)

1) Promise (cover)  
2) Context / problem  
3) Why the old approach fails  
4) Method / principle  
5–7) Steps (one idea each)  
8) Proof (numbers / case / before-after)  
9) Checklist  
10) CTA (single concrete action)

### 4) Write slide copy (density rules)

- One idea per slide.
- 2–6 lines per slide, ~6–12 words per line.
- Bold only keywords; avoid long subordinate clauses.
- Every slide should pull to the next.

### 5) Build HTML slides (export-ready)

If you need HTML output:
- Copy `assets/templates/carousel_v1.html` into your project `build/` (or start from it).
- Keep each slide as a `<section class="slide">…</section>` block.

### 6) Scaffold a canonical project (optional)

Run:

```bash
python3 ~/.codex/skills/ideal-carousel/scripts/init_ideal_carousel_project.py \
  --root /ABS/PATH/TO/WORKSPACE \
  --slug my-carousel \
  --title "Заголовок" \
  --owner "you" \
  --language ru
```

This creates:
`projects/<slug>/{source,build,output}/{...} + manifest.yaml + status.yaml + commands.md`.

### 7) Export PNG/ZIP (optional)

Use the exporter from `instagram-carousel-ai-first`:

```bash
python3 ~/.codex/skills/instagram-carousel-ai-first/scripts/export_slides.py \
  --html build/carousel_v1.html \
  --out-dir output/png/carousel_v1 \
  --zip output/zip/carousel_v1.zip
```

If Playwright is missing:

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
```

## Bundled resources

- `scripts/init_ideal_carousel_project.py`: scaffold a project + copy templates.
- `assets/templates/script_ru.md`: slide-by-slide script template.
- `assets/templates/carousel_v1.html`: clean export-ready HTML template.
- `references/qa-checklist.md`: QA checklist before publishing.
