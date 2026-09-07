from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DRAGON_PATH = ROOT / "assets" / "mybotica-dragon-mirrored-exact.jpeg"
ENDCARD_PATH = ROOT / "assets" / "mybotica-loading-85-endcard.png"
OUTPUT = ROOT / "storyboard-screen-exact-v3.png"

GREEN = "#0F2A24"
BURGUNDY = "#8C1D26"
CREAM = "#F6F2EE"
FONT_MONO = Path("/System/Library/Fonts/Supplemental/Andale Mono.ttf")
FONT_SANS = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")

CANVAS_W = 1200
CANVAS_H = 1320
PANEL_W = 270
PANEL_H = 480
GAP_X = 20
GAP_Y = 86
LEFT = 30
TOP = 112


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def fit_cover(image: Image.Image, width: int, height: int) -> Image.Image:
    scale = max(width / image.width, height / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    x = (resized.width - width) // 2
    y = (resized.height - height) // 2
    return resized.crop((x, y, x + width, y + height))


def pixelate(image: Image.Image, cell: int) -> Image.Image:
    small = image.resize(
        (max(1, image.width // cell), max(1, image.height // cell)),
        Image.Resampling.BOX,
    )
    return small.resize(image.size, Image.Resampling.NEAREST)


def draw_centered(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fnt, fill: str) -> None:
    bbox = draw.textbbox((0, 0), text, font=fnt)
    x = xy[0] - (bbox[2] - bbox[0]) // 2
    y = xy[1] - (bbox[3] - bbox[1]) // 2
    draw.text((x, y), text, font=fnt, fill=fill)


def main() -> None:
    dragon = Image.open(DRAGON_PATH).convert("RGB")
    endcard = Image.open(ENDCARD_PATH).convert("RGB")
    source_bg = dragon.getpixel((0, 0))

    board = Image.new("RGB", (CANVAS_W, CANVAS_H), CREAM)
    draw = ImageDraw.Draw(board)

    title_font = font(FONT_SANS, 34)
    label_font = font(FONT_MONO, 27)
    number_font = font(FONT_SANS, 31)
    tiny_font = font(FONT_MONO, 18)

    draw_centered(draw, (CANVAS_W // 2, 46), "MYBOTICA // LOADING STORYBOARD", title_font, GREEN)
    draw_centered(
        draw,
        (CANVAS_W // 2, 82),
        "точный механически развёрнутый персонаж",
        tiny_font,
        GREEN,
    )

    progresses = [0, 0, 12, 31, 52, 68, 85, 85]
    timings = ["0–1.5", "1.5–3", "3–5", "5–7", "7–9", "9–11", "11–13", "13–15"]
    cells = [0, 0, 18, 14, 10, 7, 4, 0]

    sprite_w = 190
    sprite_h = round(sprite_w * dragon.height / dragon.width)
    sprite_base = dragon.resize((sprite_w, sprite_h), Image.Resampling.LANCZOS)

    for index in range(8):
        row = index // 4
        col = index % 4
        x = LEFT + col * (PANEL_W + GAP_X)
        y = TOP + row * (PANEL_H + GAP_Y)

        if index == 7:
            panel = fit_cover(endcard, PANEL_W, PANEL_H)
        else:
            panel = Image.new("RGB", (PANEL_W, PANEL_H), source_bg)
            pdraw = ImageDraw.Draw(panel)

            if index == 1:
                px = 18
                pdraw.rectangle(
                    ((PANEL_W - px) // 2, (PANEL_H - px) // 2,
                     (PANEL_W + px) // 2, (PANEL_H + px) // 2),
                    fill=GREEN,
                )

            if 2 <= index <= 6:
                rendered = pixelate(sprite_base, cells[index])
                reveal_h = max(1, round(rendered.height * progresses[index] / 100))
                crop = rendered.crop((0, 0, rendered.width, reveal_h))
                sx = (PANEL_W - rendered.width) // 2
                sy = 78
                panel.paste(crop, (sx, sy))

                percent = f"{progresses[index]}%"
                bbox = pdraw.textbbox((0, 0), percent, font=label_font)
                pdraw.text(
                    (PANEL_W - 18 - (bbox[2] - bbox[0]), PANEL_H - 58),
                    percent,
                    font=label_font,
                    fill=GREEN,
                )

                if index == 3:
                    # A compact pause cue, kept outside the character.
                    pdraw.rectangle((211, 214, 239, 218), fill=BURGUNDY)
                    pdraw.rectangle((217, 220, 233, 224), fill=BURGUNDY)
                    pdraw.rectangle((223, 226, 227, 230), fill=BURGUNDY)

        board.paste(panel, (x, y))
        draw.rectangle((x, y, x + PANEL_W, y + PANEL_H), outline=GREEN, width=3)
        draw_centered(draw, (x + PANEL_W // 2, y + PANEL_H + 28), str(index + 1), number_font, GREEN)
        draw_centered(
            draw,
            (x + PANEL_W // 2, y + PANEL_H + 58),
            f"{timings[index]} s",
            tiny_font,
            GREEN,
        )

    board.save(OUTPUT, quality=100)


if __name__ == "__main__":
    main()
