#!/usr/bin/env python3
"""Export carousel slides from HTML to PNG and optional ZIP."""

from __future__ import annotations

import argparse
import os
import zipfile
from pathlib import Path

from playwright.sync_api import sync_playwright


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export .slide elements to PNG files")
    parser.add_argument("--html", required=True, help="Path or URL to HTML")
    parser.add_argument("--out-dir", required=True, help="Output directory for PNG files")
    parser.add_argument("--selector", default=".slide", help="CSS selector for slide nodes")
    parser.add_argument("--width", type=int, default=1080, help="Viewport width")
    parser.add_argument("--height", type=int, default=1350, help="Viewport height")
    parser.add_argument("--dpr", type=float, default=1.0, help="Device pixel ratio")
    parser.add_argument("--wait-ms", type=int, default=1500, help="Wait before capture")
    parser.add_argument("--zip", default="", help="Optional zip output path")
    return parser.parse_args()


def as_url(raw: str) -> str:
    if raw.startswith(("http://", "https://", "file://")):
        return raw
    return Path(raw).expanduser().resolve().as_uri()


def export_pngs(
    html_url: str,
    out_dir: Path,
    selector: str,
    width: int,
    height: int,
    dpr: float,
    wait_ms: int,
) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    exported: list[Path] = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=dpr,
        )
        page.goto(html_url, wait_until="networkidle")
        page.wait_for_timeout(wait_ms)

        nodes = page.query_selector_all(selector)
        if not nodes:
            browser.close()
            raise RuntimeError(f"No nodes found for selector: {selector}")

        for idx, node in enumerate(nodes, start=1):
            file_name = f"slide-{idx:02d}.png"
            target = out_dir / file_name
            node.screenshot(path=str(target), type="png")
            exported.append(target)

        browser.close()

    return exported


def write_zip(png_files: list[Path], zip_path: Path, root: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for png in png_files:
            zf.write(png, arcname=os.path.relpath(png, root))


def main() -> None:
    args = parse_args()
    html_url = as_url(args.html)
    out_dir = Path(args.out_dir).expanduser().resolve()

    png_files = export_pngs(
        html_url=html_url,
        out_dir=out_dir,
        selector=args.selector,
        width=args.width,
        height=args.height,
        dpr=args.dpr,
        wait_ms=args.wait_ms,
    )

    for png in png_files:
        print(f"[OK] {png}")
    print(f"[OK] Exported {len(png_files)} slides from {html_url}")

    if args.zip:
        zip_path = Path(args.zip).expanduser().resolve()
        write_zip(png_files=png_files, zip_path=zip_path, root=out_dir)
        print(f"[OK] Wrote ZIP: {zip_path}")


if __name__ == "__main__":
    main()
