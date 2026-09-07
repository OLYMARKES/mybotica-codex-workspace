from pathlib import Path
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUT = ROOT / "storyboards" / "chat-overload-v1"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
GREEN = "#0F2A24"
CREAM = "#F6F2EE"
PAPER = "#FCF8F5"
RED = "#8C1D26"
MUTED = "#C9BFB5"
WHITE = "#FFFFFF"

FONT_REG = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
FONT_BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")


def font(size, bold=False):
    path = FONT_BOLD if bold else FONT_REG
    return ImageFont.truetype(str(path), size=size)


def fit_text(draw, text, box, start_size=72, bold=True, min_size=28, fill=GREEN):
    x0, y0, x1, y1 = box
    for size in range(start_size, min_size - 1, -2):
        f = font(size, bold)
        bbox = draw.multiline_textbbox((0, 0), text, font=f, spacing=int(size * .2), align="center")
        if bbox[2] - bbox[0] <= x1 - x0 and bbox[3] - bbox[1] <= y1 - y0:
            x = (x0 + x1) / 2
            draw.multiline_text((x, y0), text, font=f, fill=fill, anchor="ma", align="center", spacing=int(size * .2))
            return


@lru_cache(maxsize=1)
def character_card():
    """Keep the supplied character pixels unchanged inside a rounded paper field."""
    src = Image.open(ASSETS / "mybotica-dragon-mirrored-exact.jpeg").convert("RGBA")
    mask = Image.new("L", src.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, src.width - 1, src.height - 1), radius=10, fill=255)
    src.putalpha(mask)
    return src


def load_character(max_w=620, max_h=900):
    return ImageOps.contain(character_card(), (max_w, max_h), Image.Resampling.LANCZOS)


def paste_character(frame, x, y, max_w=620, max_h=900):
    char = load_character(max_w, max_h)
    frame.alpha_composite(char, (x, y))
    return (x, y, x + char.width, y + char.height)


def bubble(draw, xy, text, count=None, width=360):
    x, y = xy
    f = font(34)
    bb = draw.textbbox((0, 0), text, font=f)
    h = max(92, bb[3] - bb[1] + 46)
    draw.rounded_rectangle((x, y, x + width, y + h), radius=26, fill=WHITE, outline=GREEN, width=5)
    draw.polygon([(x + 70, y + h), (x + 100, y + h), (x + 82, y + h + 26)], fill=WHITE, outline=GREEN)
    draw.text((x + 26, y + h / 2), text, font=f, fill=GREEN, anchor="lm")
    if count is not None:
        cx, cy = x + width - 8, y - 8
        draw.ellipse((cx - 36, cy - 36, cx + 36, cy + 36), fill=RED)
        draw.text((cx, cy), str(count), font=font(28, True), fill=WHITE, anchor="mm")


def check_pill(draw, y, text):
    x0, x1 = 170, 910
    draw.rounded_rectangle((x0, y, x1, y + 110), radius=28, fill=WHITE, outline=GREEN, width=5)
    draw.ellipse((x0 + 28, y + 28, x0 + 82, y + 82), outline=GREEN, width=6)
    draw.line((x0 + 42, y + 56, x0 + 52, y + 68, x0 + 70, y + 42), fill=GREEN, width=7, joint="curve")
    draw.text((x0 + 105, y + 55), text, font=font(38, True), fill=GREEN, anchor="lm")


def logo(frame, box):
    im = Image.open(ASSETS / "mybotica-logo-transparent.png").convert("RGBA")
    im = ImageOps.contain(im, (box[2] - box[0], box[3] - box[1]), Image.Resampling.LANCZOS)
    x = box[0] + (box[2] - box[0] - im.width) // 2
    y = box[1] + (box[3] - box[1] - im.height) // 2
    frame.alpha_composite(im, (x, y))


def base(idx, timecode, title, dark=False):
    bg = GREEN if dark else PAPER
    frame = Image.new("RGBA", (W, H), bg)
    draw = ImageDraw.Draw(frame)
    draw.rounded_rectangle((55, 55, 230, 118), radius=30, fill=RED)
    draw.text((142, 87), f"{idx}/8", font=font(34, True), fill=WHITE, anchor="mm")
    draw.text((1025, 88), timecode, font=font(32, True), fill=CREAM if dark else GREEN, anchor="rm")
    if dark:
        fit_text(draw, title, (80, 155, 1000, 355), 72, True, fill=CREAM)
    else:
        fit_text(draw, title, (90, 155, 990, 355), 76, True)
    return frame, draw


def frame_1():
    im, d = base(1, "0:00–0:02", "ВСЁ СПОКОЙНО")
    paste_character(im, 270, 470, 540, 850)
    d.rounded_rectangle((245, 1260, 835, 1580), radius=36, fill=GREEN)
    d.rectangle((315, 1340, 765, 1550), fill="#153A32", outline=CREAM, width=5)
    d.text((540, 1450), "работа идёт", font=font(48, True), fill=CREAM, anchor="mm")
    d.text((540, 1730), "Всё под контролем", font=font(40), fill=GREEN, anchor="mm")
    return im


def frame_2():
    im, d = base(2, "0:02–0:04", "ПЕРВЫЕ ВОПРОСЫ")
    paste_character(im, 520, 770, 470, 740)
    bubble(d, (80, 500), "Сколько стоит?", width=440)
    bubble(d, (80, 690), "Есть запись?", width=390)
    bubble(d, (80, 880), "Как оплатить?", width=420)
    d.text((150, 1540), "тук", font=font(34, True), fill=RED)
    d.text((260, 1620), "тук", font=font(34, True), fill=RED)
    return im


def frame_3():
    im, d = base(3, "0:04–0:06", "ИХ СТАНОВИТСЯ БОЛЬШЕ")
    paste_character(im, 300, 660, 500, 790)
    bubble(d, (40, 470), "Есть доставка?", 7, 390)
    bubble(d, (600, 520), "Когда открыты?", 12, 420)
    bubble(d, (60, 1240), "Можно сегодня?", 18, 440)
    bubble(d, (620, 1350), "А скидка?", 23, 350)
    return im


def frame_4():
    im, d = base(4, "0:06–0:08", "ПОЛНЫЙ ПОТОК", dark=True)
    paste_character(im, 285, 640, 510, 805)
    for x, y, n in [(35, 500, 35), (650, 470, 47), (35, 1220, 58), (700, 1300, 63)]:
        d.rounded_rectangle((x, y, x + 330, y + 110), radius=24, fill=CREAM, outline=RED, width=6)
        d.text((x + 45, y + 55), "...", font=font(44, True), fill=GREEN, anchor="lm")
        d.ellipse((x + 275, y - 36, x + 347, y + 36), fill=RED)
        d.text((x + 311, y), str(n), font=font(26, True), fill=WHITE, anchor="mm")
    for x0, y0, x1, y1 in [(210, 760, 140, 700), (840, 790, 930, 720), (240, 1080, 130, 1140), (820, 1110, 950, 1170)]:
        d.line((x0, y0, x1, y1), fill=RED, width=16)
    return im


def frame_5():
    im, d = base(5, "0:08–0:10", "Я НЕ УСПЕВАЮ")
    paste_character(im, 295, 820, 490, 775)
    d.arc((345, 470, 735, 760), 200, 510, fill=MUTED, width=18)
    d.arc((430, 520, 650, 710), 210, 500, fill=MUTED, width=14)
    d.text((540, 1640), "Сообщения не заканчиваются", font=font(38), fill=GREEN, anchor="mm")
    return im


def frame_6():
    im, d = base(6, "0:10–0:12", "ПОЯВЛЯЕТСЯ MYBOTICA", dark=True)
    for line in [
        (80, 620, 25, 570), (80, 780, 15, 780), (90, 940, 30, 995),
        (600, 620, 655, 570), (610, 780, 675, 780), (600, 940, 660, 995),
    ]:
        d.line(line, fill=RED, width=13)
    logo(im, (80, 650, 620, 930))
    paste_character(im, 590, 920, 390, 620)
    d.text((540, 1640), "Интерфейс снова становится тихим", font=font(38), fill=CREAM, anchor="mm")
    return im


def frame_7():
    im, d = base(7, "0:12–0:15", "РУТИНА УХОДИТ БОТУ", dark=True)
    logo(im, (150, 380, 930, 650))
    check_pill(d, 760, "Ответ отправлен")
    check_pill(d, 930, "Запись создана")
    check_pill(d, 1100, "Заявка передана")
    paste_character(im, 670, 1370, 280, 440)
    return im


def frame_8():
    im, d = base(8, "0:15–0:18", "МОЖНО ЗАНЯТЬСЯ ВАЖНЫМ", dark=True)
    paste_character(im, 315, 420, 450, 710)
    d.ellipse((210, 1110, 330, 1230), fill=CREAM, outline=RED, width=7)
    d.rounded_rectangle((315, 1145, 385, 1205), radius=25, outline=CREAM, width=10)
    d.line((250, 1090, 230, 1030), fill=CREAM, width=9)
    d.line((285, 1090, 300, 1025), fill=CREAM, width=9)
    d.multiline_text((540, 1370), "Скоро MyBotica будет\nотвечать за вас", font=font(58, True), fill=CREAM, anchor="ma", align="center", spacing=16)
    d.rounded_rectangle((170, 1625, 910, 1760), radius=58, fill=RED)
    d.text((540, 1693), "ПОДПИСЫВАЙТЕСЬ НА ЗАПУСК", font=font(38, True), fill=WHITE, anchor="mm")
    return im


frames = [frame_1(), frame_2(), frame_3(), frame_4(), frame_5(), frame_6(), frame_7(), frame_8()]
for i, im in enumerate(frames, 1):
    im.convert("RGB").save(OUT / f"frame-{i:02d}.jpg", quality=94)

thumb_w, thumb_h = 270, 480
gap, header = 24, 180
sheet = Image.new("RGB", (gap + 4 * (thumb_w + gap), header + gap + 2 * (thumb_h + gap)), CREAM)
sd = ImageDraw.Draw(sheet)
sd.text((sheet.width // 2, 54), "MYBOTICA — ЧАТ ЗАВАЛИЛО", font=font(58, True), fill=GREEN, anchor="ma")
sd.text((sheet.width // 2, 122), "раскадровка v1 · 18 секунд · точный фирменный дракончик", font=font(30), fill=RED, anchor="ma")
for i, im in enumerate(frames):
    thumb = im.convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    x = gap + (i % 4) * (thumb_w + gap)
    y = header + gap + (i // 4) * (thumb_h + gap)
    sheet.paste(thumb, (x, y))
    sd.rounded_rectangle((x, y, x + thumb_w, y + thumb_h), radius=18, outline=GREEN, width=4)

sheet.save(ROOT / "storyboard-chat-overload-v1.jpg", quality=94)
print(ROOT / "storyboard-chat-overload-v1.jpg")
