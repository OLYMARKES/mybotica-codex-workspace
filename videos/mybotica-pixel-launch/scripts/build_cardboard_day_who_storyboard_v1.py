from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "social-trash-character-tests" / "storyboard-day-who-source-v1.png"
OUT = ROOT / "storyboard-cardboard-day-who-v1.png"

GREEN = "#0F2A24"
RED = "#8C1D26"
CREAM = "#F6F2EE"
PAPER = "#FBF7F0"
WHITE = "#FFFFFF"

FONT_REG = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
FONT_BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")


def font(size, bold=False):
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REG), size=size)


source = Image.open(SOURCE).convert("RGB")
cell_w = source.width // 2
cell_h = source.height // 4

canvas_w = 1120
margin = 36
gap = 28
header_h = 220
card_w = (canvas_w - margin * 2 - gap) // 2
image_h = round(card_w * cell_h / cell_w)
caption_h = 112
card_h = image_h + caption_h
canvas_h = header_h + margin + 4 * card_h + 3 * gap + margin

canvas = Image.new("RGB", (canvas_w, canvas_h), CREAM)
d = ImageDraw.Draw(canvas)
d.text((canvas_w // 2, 48), "MYBOTICA — «ДЕНЬ У КОГО?»", font=font(52, True), fill=GREEN, anchor="ma")
d.text((canvas_w // 2, 120), "10 секунд · картонный stop-motion · реакция без мимики", font=font(28), fill=RED, anchor="ma")
d.line((270, 178, 850, 178), fill=RED, width=6)

times = [
    "0:00–0:01",
    "0:01–0:02",
    "0:02–0:04",
    "0:04–0:05",
    "0:05–0:06",
    "0:06–0:08",
    "0:08–0:09",
    "0:09–0:10",
]

captions = [
    "03:47. MyBotica молча сидит\nза картонным ноутбуком.",
    "Уведомление:\n«Клиент: Добрый день!»",
    "Две секунды абсолютной паузы.\nНе двигается вообще ничего.",
    "Только голова медленно\nподнимается к камере.",
    "Резкая склейка на неприлично\nкрупный план.",
    "Пауза. Уставшим голосом:\n«День у кого?»",
    "Новое уведомление:\n«Клиент: Вы работаете?»",
    "MyBotica медленно складывается\nна пол. Маленький логотип.",
]


def overlay_pill(frame, text, top, fill=WHITE, ink=GREEN, stroke=GREEN):
    fd = ImageDraw.Draw(frame)
    box = (28, top, frame.width - 28, top + 76)
    fd.rounded_rectangle(box, radius=24, fill=fill, outline=stroke, width=4)
    fd.text((frame.width // 2, top + 38), text, font=font(25, True), fill=ink, anchor="mm")


def green_logo():
    logo = Image.open(ROOT / "assets" / "mybotica-logo-transparent.png").convert("RGBA")
    pixels = []
    for r, g, b, a in logo.getdata():
        if a == 0 or r > g * 1.25:
            pixels.append((r, g, b, a))
        else:
            pixels.append((15, 42, 36, a))
    logo.putdata(pixels)
    return logo


logo = green_logo()

for index in range(8):
    col = index % 2
    row = index // 2
    crop = source.crop((col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h))
    crop = crop.resize((card_w, image_h), Image.Resampling.LANCZOS).convert("RGBA")

    if index == 0:
        overlay_pill(crop, "03:47", 26, fill=GREEN, ink=CREAM, stroke=GREEN)
    elif index == 1:
        overlay_pill(crop, "Клиент: «Добрый день!»", 26)
    elif index == 5:
        overlay_pill(crop, "День у кого?", image_h - 104, fill=CREAM, ink=RED, stroke=RED)
    elif index == 6:
        overlay_pill(crop, "Клиент: «Вы работаете?»", 26)
    elif index == 7:
        mark = ImageOps.contain(logo, (245, 86), Image.Resampling.LANCZOS)
        crop.alpha_composite(mark, (28, 24))

    x = margin + col * (card_w + gap)
    y = header_h + margin + row * (card_h + gap)

    d.rounded_rectangle((x - 4, y - 4, x + card_w + 4, y + card_h + 4), radius=22, fill=GREEN)
    canvas.paste(crop.convert("RGB"), (x, y))
    d.rectangle((x, y + image_h, x + card_w, y + card_h), fill=PAPER)

    d.rounded_rectangle((x + 18, y + 16, x + 92, y + 58), radius=18, fill=RED)
    d.text((x + 55, y + 37), f"{index + 1}/8", font=font(19, True), fill=WHITE, anchor="mm")
    d.text((x + card_w - 18, y + 37), times[index], font=font(20, True), fill=GREEN, anchor="rm")
    d.multiline_text(
        (x + card_w // 2, y + image_h + 22),
        captions[index],
        font=font(25, index in (1, 5, 6)),
        fill=GREEN,
        anchor="ma",
        align="center",
        spacing=6,
    )

canvas.save(OUT, quality=95)
print(OUT)
