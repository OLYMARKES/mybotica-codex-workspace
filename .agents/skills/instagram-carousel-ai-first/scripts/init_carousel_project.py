#!/usr/bin/env python3
"""Create a canonical AI-first carousel project scaffold."""

from __future__ import annotations

import argparse
from pathlib import Path


MANIFEST_TEMPLATE = """project_slug: {project_slug}
title: "{title}"
owner: "{owner}"
language: "{language}"
inputs:
  - source/script_{language}.md
outputs:
  png_dir: output/png
  zip_dir: output/zip
canonical_build: build/carousel_v1.html
"""


STATUS_TEMPLATE = """state: draft
updated_at: "{updated_at}"
agent: "{agent}"
notes:
  - "Project initialized"
"""


COMMANDS_TEMPLATE = """# Commands

## Export PNG and ZIP
python3 ../../../../.codex/skills/instagram-carousel-ai-first/scripts/export_slides.py \\
  --html build/carousel_v1.html \\
  --out-dir output/png/carousel_v1 \\
  --zip output/zip/carousel_v1.zip
"""


CAROUSEL_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Carousel v1</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #f3f1ec;
      display: flex;
      flex-direction: column;
      gap: 20px;
      align-items: center;
      padding: 24px;
      font-family: "Inter", sans-serif;
    }
    .slide {
      width: 1080px;
      height: 1350px;
      background: #fff;
      border-radius: 20px;
      padding: 80px;
      display: flex;
      flex-direction: column;
      gap: 18px;
      justify-content: center;
    }
    .kicker {
      font-size: 24px;
      letter-spacing: 1px;
      text-transform: uppercase;
      color: #b2514f;
      font-weight: 700;
    }
    h1, h2 { line-height: 1.12; color: #121212; }
    h1 { font-size: 86px; }
    h2 { font-size: 58px; }
    p { font-size: 36px; line-height: 1.35; color: #2e2e2e; }
  </style>
</head>
<body>
  <section class="slide">
    <div class="kicker">cover</div>
    <h1>Заголовок карусели</h1>
    <p>Подзаголовок или обещание пользы.</p>
  </section>
  <section class="slide">
    <div class="kicker">slide 1</div>
    <h2>Первая мысль</h2>
    <p>Одна идея на слайд, без перегруза текстом.</p>
  </section>
</body>
</html>
"""


def write_if_needed(path: Path, content: str, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap AI-first carousel project")
    parser.add_argument("--root", required=True, help="Workspace root path")
    parser.add_argument("--slug", required=True, help="Project slug (lowercase-hyphen)")
    parser.add_argument("--title", required=True, help="Project title")
    parser.add_argument("--owner", default="unknown", help="Owner/team")
    parser.add_argument("--language", default="ru", help="Primary language code")
    parser.add_argument("--agent", default="codex", help="Agent name for status")
    parser.add_argument(
        "--updated-at",
        default="1970-01-01T00:00:00Z",
        help="ISO timestamp for status.yaml",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite templates")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    project = root / "projects" / args.slug
    source = project / "source"
    build = project / "build"
    out_png = project / "output" / "png"
    out_zip = project / "output" / "zip"

    for path in (source, build, out_png, out_zip):
        path.mkdir(parents=True, exist_ok=True)

    created = []
    if write_if_needed(
        project / "manifest.yaml",
        MANIFEST_TEMPLATE.format(
            project_slug=args.slug,
            title=args.title.replace('"', "'"),
            owner=args.owner.replace('"', "'"),
            language=args.language,
        ),
        args.force,
    ):
        created.append("manifest.yaml")

    if write_if_needed(
        project / "status.yaml",
        STATUS_TEMPLATE.format(
            updated_at=args.updated_at,
            agent=args.agent.replace('"', "'"),
        ),
        args.force,
    ):
        created.append("status.yaml")

    if write_if_needed(project / "commands.md", COMMANDS_TEMPLATE, args.force):
        created.append("commands.md")

    if write_if_needed(
        source / f"script_{args.language}.md",
        "# Carousel Script\n\n- Replace with actual content.\n",
        args.force,
    ):
        created.append(f"source/script_{args.language}.md")

    if write_if_needed(build / "carousel_v1.html", CAROUSEL_TEMPLATE, args.force):
        created.append("build/carousel_v1.html")

    print(f"[OK] Initialized: {project}")
    if created:
        for item in created:
            print(f"[OK] Wrote: {item}")
    else:
        print("[OK] No files changed. Use --force to overwrite templates.")


if __name__ == "__main__":
    main()
