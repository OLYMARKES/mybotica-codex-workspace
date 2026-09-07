#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class TemplateFiles:
    script_ru: Path
    carousel_html: Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Initialize a canonical carousel project with ideal-carousel templates.")
    p.add_argument("--root", required=True, help="Workspace root where projects/<slug> is created")
    p.add_argument("--slug", required=True, help="Project slug (lowercase, ascii, hyphens)")
    p.add_argument("--title", required=True, help="Project title")
    p.add_argument("--owner", required=True, help="Owner name/team")
    p.add_argument("--language", default="ru", help="Language code (default: ru)")
    p.add_argument("--force", action="store_true", help="Overwrite template files if they exist")
    return p.parse_args()


def iso_utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def get_templates(skill_dir: Path) -> TemplateFiles:
    templates_dir = skill_dir / "assets" / "templates"
    script_ru = templates_dir / "script_ru.md"
    carousel_html = templates_dir / "carousel_v1.html"
    if not script_ru.exists():
        raise FileNotFoundError(f"Missing template: {script_ru}")
    if not carousel_html.exists():
        raise FileNotFoundError(f"Missing template: {carousel_html}")
    return TemplateFiles(script_ru=script_ru, carousel_html=carousel_html)


def write_text(path: Path, content: str, *, force: bool) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def copy_file(src: Path, dst: Path, *, force: bool) -> None:
    if dst.exists() and not force:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(src.read_bytes())


def write_manifest(project_dir: Path, *, slug: str, title: str, owner: str, language: str) -> None:
    content = (
        f'project_slug: {slug}\n'
        f'title: "{title}"\n'
        f'owner: "{owner}"\n'
        f'language: "{language}"\n'
        "inputs:\n"
        "  - source/script_ru.md\n"
        "outputs:\n"
        "  png_dir: output/png\n"
        "  zip_dir: output/zip\n"
        "canonical_build: build/carousel_v1.html\n"
    )
    (project_dir / "manifest.yaml").write_text(content, encoding="utf-8")


def write_status(project_dir: Path) -> None:
    content = (
        "state: draft\n"
        f"updated_at: {iso_utc_now()}\n"
        "agent: ideal-carousel\n"
        "notes:\n"
        "  - Initialized with ideal-carousel templates\n"
    )
    (project_dir / "status.yaml").write_text(content, encoding="utf-8")


def write_commands(project_dir: Path) -> None:
    content = (
        "# Commands\n\n"
        "## Export PNG and ZIP\n"
        "python3 ~/.codex/skills/instagram-carousel-ai-first/scripts/export_slides.py \\\n"
        "  --html build/carousel_v1.html \\\n"
        "  --out-dir output/png/carousel_v1 \\\n"
        "  --zip output/zip/carousel_v1.zip\n"
    )
    (project_dir / "commands.md").write_text(content, encoding="utf-8")


def ensure_dirs(project_dir: Path) -> None:
    for rel in [
        "source",
        "build",
        "output/png",
        "output/zip",
    ]:
        (project_dir / rel).mkdir(parents=True, exist_ok=True)


def main() -> None:
    args = parse_args()

    root = Path(args.root).expanduser().resolve()
    skill_dir = Path(__file__).resolve().parents[1]
    templates = get_templates(skill_dir)

    project_dir = root / "projects" / args.slug
    project_dir.mkdir(parents=True, exist_ok=True)
    ensure_dirs(project_dir)

    copy_file(templates.script_ru, project_dir / "source" / "script_ru.md", force=args.force)
    copy_file(templates.carousel_html, project_dir / "build" / "carousel_v1.html", force=args.force)

    write_manifest(
        project_dir,
        slug=args.slug,
        title=args.title,
        owner=args.owner,
        language=args.language,
    )
    write_status(project_dir)
    write_commands(project_dir)

    print(f"[OK] Initialized: {project_dir}")


if __name__ == "__main__":
    main()

