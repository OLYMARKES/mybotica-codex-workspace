from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "social-trash-character-tests" / "storyboard-day-who-source-v2.png"
OUT = ROOT / "storyboard-cardboard-day-who-v2.png"

GREEN = "#102E28"
RED = "#B42032"
BRIGHT_RED = "#F2384F"
CREAM = "#F5EBDD"
PAPER = "#FBF5EC"
WHITE = "#FFFFFF"

FONT_REG = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
FONT_BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
FONT_MONO = Path("/System/Library/Fonts/Menlo.ttc")


def font(size, bold=False, mono=False):
    path = FONT_MONO if mono else (FONT_BOLD if bold else FONT_REG)
    return ImageFont.truetype(str(path), size=size)


def clock_overlay(frame, top, height, scale=1.0):
    draw = ImageDraw.Draw(frame)
    left = 22
    right = frame.width - 22
    draw.rounded_rectangle(
        (left, top, right, top + height),
        radius=24,
        fill=GREEN,
        outline=CREAM,
        width=5,
    )
    size = round(72 * scale)
    # A tiny offset acts like the glow/bloom of an old digital display.
    draw.text(
        (frame.width // 2 + 3, top + height // 2 + 3),
        "03:47",
        font=font(size, mono=True),
        fill="#6E1721",
        anchor="mm",
    )
    draw.text(
        (frame.width // 2, top + height // 2),
        "03:47",
        font=font(size, mono=True),
        fill=BRIGHT_RED,
        anchor="mm",
        stroke_width=1,
        stroke_fill=WHITE,
    )


def message_overlay(frame):
    draw = ImageDraw.Draw(frame)
    box = (24, 26, frame.width - 24, 112)
    draw.rounded_rectangle(box, radius=25, fill=PAPER, outline=GREEN, width=5)
    draw.text(
        (frame.width // 2, 69),
        "Клиент: «Добрый день!»",
        font=font(25, bold=True),
        fill=GREEN,
        anchor="mm",
    )


source = Image.open(SOURCE).convert("RGB")
cell_w = source.width // 2
cell_h = source.height // 4

canvas_w = 1120
margin = 36
gap = 28
header_h = 220
card_w = (canvas_w - margin * 2 - gap) // 2
image_h = round(card_w * cell_h / cell_w)
caption_h = 118
card_h = image_h + caption_h
canvas_h = header_h + margin + 4 * card_h + 3 * gap + margin

canvas = Image.new("RGB", (canvas_w, canvas_h), CREAM)
draw = ImageDraw.Draw(canvas)
draw.text((canvas_w // 2, 44), "MYBOTICA — «03:47»", font=font(52, True), fill=GREEN, anchor="ma")
draw.text(
    (canvas_w // 2, 116),
    "время как навязчивый рефрен · морда не меняется",
    font=font(28),
    fill=RED,
    anchor="ma",
)
draw.text(
    (canvas_w // 2, 174),
    "03:47     03:47     03:47",
    font=font(24, mono=True),
    fill=BRIGHT_RED,
    anchor="ma",
)

times = [
    "0:00–0:00,8",
    "0:00,8–0:01,6",
    "0:01,6–0:03",
    "0:03–0:03,4",
    "0:03,4–0:05",
    "0:05–0:05,4",
    "0:05,4–0:07,5",
    "0:07,5–0:10",
]

captions = [
    "03:47. Слишком крупно.\nТишина ночного офиса.",
    "Клиент пишет:\n«Добрый день!»",
    "Морда дракоши.\nОн просто смотрит.",
    "Снова 03:47.\nРезкая короткая перебивка.",
    "Та же морда, но ближе.\nПауза становится неловкой.",
    "Опять 03:47.\nЕщё крупнее и ярче.",
    "Неприличный крупный план.\nЕщё две секунды молчания.",
    "Он не меняется. Устало:\n«День у кого?»",
]

for index in range(8):
    col = index % 2
    row = index // 2
    crop = source.crop((col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h))
    crop = crop.resize((card_w, image_h), Image.Resampling.LANCZOS).convert("RGBA")

    if index == 0:
        clock_overlay(crop, 36, 150, 1.02)
    elif index == 1:
        message_overlay(crop)
    elif index == 3:
        clock_overlay(crop, 64, 190, 1.18)
    elif index == 5:
        clock_overlay(crop, 38, 250, 1.36)
    elif index == 7:
        frame_draw = ImageDraw.Draw(crop)
        box = (22, image_h - 116, card_w - 22, image_h - 26)
        frame_draw.rounded_rectangle(box, radius=25, fill=PAPER, outline=RED, width=5)
        frame_draw.text(
            (card_w // 2, image_h - 71),
            "День у кого?",
            font=font(35, bold=True),
            fill=RED,
            anchor="mm",
        )

    x = margin + col * (card_w + gap)
    y = header_h + margin + row * (card_h + gap)

    draw.rounded_rectangle((x - 4, y - 4, x + card_w + 4, y + card_h + 4), radius=22, fill=GREEN)
    canvas.paste(crop.convert("RGB"), (x, y))
    draw.rectangle((x, y + image_h, x + card_w, y + card_h), fill=PAPER)

    draw.rounded_rectangle((x + 18, y + 16, x + 92, y + 58), radius=18, fill=RED)
    draw.text((x + 55, y + 37), f"{index + 1}/8", font=font(19, True), fill=WHITE, anchor="mm")
    draw.text((x + card_w - 18, y + 37), times[index], font=font(18, True), fill=GREEN, anchor="rm")
    draw.multiline_text(
        (x + card_w // 2, y + image_h + 22),
        captions[index],
        font=font(25, index in (1, 7)),
        fill=GREEN,
        anchor="ma",
        align="center",
        spacing=6,
    )

canvas.save(OUT, quality=95)
print(OUT)
