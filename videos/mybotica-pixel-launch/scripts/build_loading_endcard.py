from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "snapshots" / "frame-06-at-7.15s.png"
OUTPUT = ROOT / "assets" / "mybotica-loading-85-endcard.png"
FONT = Path("/System/Library/Fonts/Supplemental/Andale Mono.ttf")

CREAM = "#F6F2EE"
BURGUNDY = "#8C1D26"


def main() -> None:
    image = Image.open(SOURCE).convert("RGB")
    draw = ImageDraw.Draw(image)

    # Retro loading rail, centered beneath the exact supplied MyBotica lockup.
    rail = (180, 1010, 900, 1074)
    draw.rounded_rectangle(rail, radius=3, outline=CREAM, width=4)

    # 85% of the 696 px usable inner rail.
    draw.rounded_rectangle((192, 1022, 783, 1062), radius=1, fill=BURGUNDY)

    font = ImageFont.truetype(str(FONT), 42)
    label = "LOADING... 85%"
    bbox = draw.textbbox((0, 0), label, font=font)
    x = (image.width - (bbox[2] - bbox[0])) // 2
    draw.text((x, 1120), label, font=font, fill=CREAM)

    image.save(OUTPUT, quality=100)


if __name__ == "__main__":
    main()
