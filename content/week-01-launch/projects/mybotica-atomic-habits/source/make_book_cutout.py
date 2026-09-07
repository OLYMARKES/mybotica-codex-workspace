from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "build/assets/atomic-habits-cover.png"
OUTPUT = ROOT / "build/assets/atomic-habits-book-cutout-v2.png"

image = Image.open(SOURCE).convert("RGBA")
scale = 4
mask = Image.new("L", (image.width * scale, image.height * scale), 0)
draw = ImageDraw.Draw(mask)
outline = [(146, 76), (448, 54), (476, 65), (477, 553), (154, 573), (147, 565)]
draw.polygon([(x * scale, y * scale) for x, y in outline], fill=255)
mask = mask.resize(image.size, Image.Resampling.LANCZOS)
image.putalpha(mask)
image = image.crop((140, 48, 484, 580))
image.save(OUTPUT)
