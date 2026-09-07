from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE_A = ROOT / "assets" / "social-trash-character-tests" / "storyboard-day-who-source-v2.png"
SOURCE_B = ROOT / "assets" / "social-trash-character-tests" / "storyboard-day-who-continuation-source-v3.png"
OUT = ROOT / "storyboard-cardboard-day-who-v4-impeccable.png"

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


def clock_overlay(frame, scale=1.0):
    draw = ImageDraw.Draw(frame)
    left, top = 14, 18
    right, bottom = frame.width - 14, round(frame.height * 0.56)
    draw.rounded_rectangle(
        (left, top, right, bottom),
        radius=18,
        fill=GREEN,
        outline=CREAM,
        width=4,
    )
    size = round(45 * scale)
    draw.text(
        (frame.width // 2 + 2, (top + bottom) // 2 + 2),
        "03:47",
        font=font(size, mono=True),
        fill="#6E1721",
        anchor="mm",
    )
    draw.text(
        (frame.width // 2, (top + bottom) // 2),
        "03:47",
        font=font(size, mono=True),
        fill=BRIGHT_RED,
        anchor="mm",
        stroke_width=1,
        stroke_fill=WHITE,
    )


def message_overlay(frame, text):
    draw = ImageDraw.Draw(frame)
    box = (14, 16, frame.width - 14, 75)
    draw.rounded_rectangle(box, radius=17, fill=PAPER, outline=GREEN, width=4)
    draw.text(
        (frame.width // 2, 45),
        text,
        font=font(17, bold=True),
        fill=GREEN,
        anchor="mm",
    )


def line_overlay(frame, text):
    draw = ImageDraw.Draw(frame)
    box = (14, frame.height - 71, frame.width - 14, frame.height - 14)
    draw.rounded_rectangle(box, radius=17, fill=PAPER, outline=RED, width=4)
    draw.text(
        (frame.width // 2, frame.height - 42),
        text,
        font=font(23, bold=True),
        fill=RED,
        anchor="mm",
    )


def green_logo():
    logo = Image.open(ROOT / "assets" / "mybotica-logo-transparent.png").convert("RGBA")
    pixels = []
    for r, g, b, a in logo.getdata():
        if a == 0 or r > g * 1.25:
            pixels.append((r, g, b, a))
        else:
            pixels.append((16, 46, 40, a))
    logo.putdata(pixels)
    return logo


source_a = Image.open(SOURCE_A).convert("RGB")
source_b = Image.open(SOURCE_B).convert("RGB")
a_w, a_h = source_a.width // 2, source_a.height // 4
b_w, b_h = source_b.width // 2, source_b.height // 2

frames = []
for index in range(8):
    col, row = index % 2, index // 2
    frames.append(source_a.crop((col * a_w, row * a_h, (col + 1) * a_w, (row + 1) * a_h)))
for index in range(4):
    col, row = index % 2, index // 2
    frames.append(source_b.crop((col * b_w, row * b_h, (col + 1) * b_w, (row + 1) * b_h)))

canvas_w = 1120
margin = 30
gap = 22
header_h = 205
cols = 3
rows = 4
card_w = (canvas_w - margin * 2 - gap * (cols - 1)) // cols
image_h = round(card_w * 0.75)
caption_h = 116
card_h = image_h + caption_h
canvas_h = header_h + margin + rows * card_h + gap * (rows - 1) + margin

canvas = Image.new("RGB", (canvas_w, canvas_h), CREAM)
draw = ImageDraw.Draw(canvas)
draw.text((canvas_w // 2, 38), "MYBOTICA — «03:47»", font=font(50, True), fill=GREEN, anchor="ma")
draw.text(
    (canvas_w // 2, 105),
    "15 секунд · картонный stop-motion · лицо без мимики",
    font=font(27),
    fill=RED,
    anchor="ma",
)
draw.text(
    (canvas_w // 2, 160),
    "03:47     03:47     03:47",
    font=font(23, mono=True),
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
    "0:07,5–0:09,5",
    "0:09,5–0:10,5",
    "0:10,5–0:11,8",
    "0:11,8–0:13,2",
    "0:13,2–0:15",
]

captions = [
    "03:47. Очень крупно.\nНочной офис.",
    "Клиент пишет:\n«Добрый день!»",
    "Морда дракоши.\nОн просто смотрит.",
    "Снова 03:47.\nКороткая перебивка.",
    "Та же морда,\nно ещё ближе.",
    "Опять 03:47.\nЕщё ярче.",
    "Неприличный\nкрупный план.",
    "Пауза. Устало:\n«День у кого?»",
    "Клиент:\n«Вы работаете?»",
    "Дракоша начинает\nмедленно заваливаться.",
    "Зависает под\nневозможным углом.",
    "Остаётся лежать.\nМаленький логотип.",
]

logo = green_logo()

for index, raw_frame in enumerate(frames):
    frame = ImageOps.fit(raw_frame, (card_w, image_h), method=Image.Resampling.LANCZOS).convert("RGBA")

    if index in (0, 3, 5):
        clock_overlay(frame, (1.0, 1.08, 1.2)[(0, 3, 5).index(index)])
    elif index == 1:
        message_overlay(frame, "Клиент: «Добрый день!»")
    elif index == 7:
        line_overlay(frame, "День у кого?")
    elif index == 8:
        message_overlay(frame, "Клиент: «Вы работаете?»")
    elif index == 11:
        mark = ImageOps.contain(logo, (132, 46), Image.Resampling.LANCZOS)
        frame.alpha_composite(mark, (18, 18))

    col, row = index % cols, index // cols
    x = margin + col * (card_w + gap)
    y = header_h + margin + row * (card_h + gap)

    draw.rounded_rectangle((x - 4, y - 4, x + card_w + 4, y + card_h + 4), radius=18, fill=GREEN)
    canvas.paste(frame.convert("RGB"), (x, y))
    draw.rectangle((x, y + image_h, x + card_w, y + card_h), fill=PAPER)

    # Impeccable polish: keep production metadata out of the visual frame.
    # The timecode and frame number live together in the caption rail, so they
    # never collide with the clock, client messages, character, or final logo.
    meta = f"{index + 1}/12   ·   {times[index]}"
    draw.text(
        (x + card_w // 2, y + image_h + 17),
        meta,
        font=font(14, True, mono=True),
        fill=RED,
        anchor="ma",
    )
    draw.multiline_text(
        (x + card_w // 2, y + image_h + 45),
        captions[index],
        font=font(19, index in (1, 7, 8, 11)),
        fill=GREEN,
        anchor="ma",
        align="center",
        spacing=4,
    )

canvas.save(OUT, quality=95)
print(OUT)
