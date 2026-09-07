from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUT = ROOT / "storyboards" / "chat-overload-v3"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
GREEN = "#0F2A24"
RED = "#8C1D26"
CREAM = "#F6F2EE"
PAPER = "#F9F6F1"
WHITE = "#FFFFFF"
MUTED = "#C8C0B8"

FONT_REG = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
FONT_BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")


def font(size, bold=False):
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REG), size=size)


def fit_text(draw, text, box, start=76, minimum=28, fill=GREEN):
    x0, y0, x1, y1 = box
    for size in range(start, minimum - 1, -2):
        f = font(size, True)
        bb = draw.multiline_textbbox((0, 0), text, font=f, spacing=10, align="center")
        if bb[2] - bb[0] <= x1 - x0 and bb[3] - bb[1] <= y1 - y0:
            draw.multiline_text(((x0 + x1) / 2, y0), text, font=f, fill=fill, anchor="ma", align="center", spacing=10)
            return


ACTOR_SHEET = Image.open(ASSETS / "mybotica-character-actor-sheet-v1.png").convert("RGBA")


def pose_crop(number):
    i = number - 1
    col, row = i % 4, i // 4
    x0 = round(col * ACTOR_SHEET.width / 4)
    x1 = round((col + 1) * ACTOR_SHEET.width / 4)
    y0 = round(row * ACTOR_SHEET.height / 3)
    y1 = round((row + 1) * ACTOR_SHEET.height / 3)
    return ACTOR_SHEET.crop((x0, y0, x1, y1))


def paste_pose(frame, number, box, opacity=255):
    x0, y0, x1, y1 = box
    pose = ImageOps.contain(pose_crop(number), (x1 - x0, y1 - y0), Image.Resampling.LANCZOS)
    mask = Image.new("L", pose.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((24, 18, pose.width - 24, pose.height - 18), radius=70, fill=opacity)
    mask = mask.filter(ImageFilter.GaussianBlur(24))
    pose.putalpha(mask)
    x = x0 + (x1 - x0 - pose.width) // 2
    y = y0 + (y1 - y0 - pose.height) // 2
    frame.alpha_composite(pose, (x, y))


def bubble(draw, xy, text="...", count=None, width=350, muted=False):
    x, y = xy
    outline = MUTED if muted else GREEN
    fill = PAPER
    f = font(34)
    bb = draw.textbbox((0, 0), text, font=f)
    height = max(96, bb[3] - bb[1] + 52)
    draw.rounded_rectangle((x, y, x + width, y + height), radius=28, fill=fill, outline=outline, width=5)
    draw.polygon([(x + 62, y + height), (x + 98, y + height), (x + 78, y + height + 28)], fill=fill, outline=outline)
    draw.text((x + 28, y + height / 2), text, font=f, fill=outline, anchor="lm")
    if count is not None:
        cx, cy = x + width - 6, y - 6
        draw.ellipse((cx - 37, cy - 37, cx + 37, cy + 37), fill=RED if not muted else MUTED)
        draw.text((cx, cy), str(count), font=font(27, True), fill=WHITE, anchor="mm")


def check_pill(draw, y, text):
    x0, x1 = 150, 930
    draw.rounded_rectangle((x0, y, x1, y + 118), radius=30, fill=WHITE, outline=GREEN, width=5)
    draw.ellipse((x0 + 30, y + 31, x0 + 86, y + 87), outline=GREEN, width=6)
    draw.line((x0 + 44, y + 60, x0 + 55, y + 73, x0 + 75, y + 45), fill=GREEN, width=7, joint="curve")
    draw.text((x0 + 112, y + 59), text, font=font(39, True), fill=GREEN, anchor="lm")


def extract_head_mark():
    src = Image.open(ASSETS / "mybotica-head-mark-reference.jpg").convert("RGBA")
    src = src.crop((0, 6, src.width, src.height - 6))
    data = []
    for r, g, b, _ in src.getdata():
        if max(r, g, b) - min(r, g, b) < 18 and (r + g + b) / 3 > 120:
            data.append((r, g, b, 0))
        else:
            data.append((r, g, b, 255))
    src.putdata(data)
    return src


HEAD_MARK = extract_head_mark()


def white_head_mark():
    mark = HEAD_MARK.copy()
    data = []
    for r, g, b, a in mark.getdata():
        if a == 0:
            data.append((r, g, b, 0))
        elif r > g * 1.25:
            data.append((140, 29, 38, a))
        else:
            data.append((246, 242, 238, a))
    mark.putdata(data)
    return mark


def paste_mark(frame, box, white=False, opacity=255):
    x0, y0, x1, y1 = box
    mark = white_head_mark() if white else HEAD_MARK.copy()
    mark = ImageOps.contain(mark, (x1 - x0, y1 - y0), Image.Resampling.LANCZOS)
    if opacity != 255:
        alpha = mark.getchannel("A").point(lambda p: p * opacity // 255)
        mark.putalpha(alpha)
    x = x0 + (x1 - x0 - mark.width) // 2
    y = y0 + (y1 - y0 - mark.height) // 2
    frame.alpha_composite(mark, (x, y))


def paste_logo(frame, box):
    x0, y0, x1, y1 = box
    logo = Image.open(ASSETS / "mybotica-logo-transparent.png").convert("RGBA")
    logo = ImageOps.contain(logo, (x1 - x0, y1 - y0), Image.Resampling.LANCZOS)
    x = x0 + (x1 - x0 - logo.width) // 2
    y = y0 + (y1 - y0 - logo.height) // 2
    frame.alpha_composite(logo, (x, y))


def base(index, timecode, title, green=False):
    bg = GREEN if green else PAPER
    im = Image.new("RGBA", (W, H), bg)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((52, 52, 225, 118), radius=30, fill=RED)
    d.text((138, 85), f"{index}/9", font=font(33, True), fill=WHITE, anchor="mm")
    d.text((1027, 85), timecode, font=font(31, True), fill=CREAM if green else GREEN, anchor="rm")
    fit_text(d, title, (75, 158, 1005, 350), 76, fill=CREAM if green else GREEN)
    return im, d


def frame_1():
    im, d = base(1, "0:00–0:02", "ВСЁ СПОКОЙНО")
    paste_pose(im, 9, (110, 420, 970, 1450))
    d.text((540, 1690), "Вокруг много воздуха и тишины", font=font(39), fill=GREEN, anchor="mm")
    return im


def frame_2():
    im, d = base(2, "0:02–0:04", "ПЕРВЫЕ ВОПРОСЫ")
    paste_pose(im, 10, (380, 570, 1020, 1420))
    bubble(d, (60, 500), "Сколько стоит?", width=420)
    bubble(d, (60, 720), "Есть запись?", width=370)
    bubble(d, (60, 940), "Как оплатить?", width=410)
    return im


def frame_3():
    im, d = base(3, "0:04–0:06", "ПОТОК РАСТЁТ")
    paste_pose(im, 5, (230, 600, 850, 1400))
    bubble(d, (40, 450), "Есть доставка?", 7, 390)
    bubble(d, (620, 500), "Когда открыты?", 12, 410)
    bubble(d, (55, 1270), "Можно сегодня?", 18, 430)
    bubble(d, (650, 1360), "А скидка?", 23, 340)
    return im


def frame_4():
    im, d = base(4, "0:06–0:08", "СЛИШКОМ МНОГО")
    d.rounded_rectangle((20, 370, 1060, 1840), radius=70, outline=RED, width=24)
    paste_pose(im, 6, (190, 570, 890, 1390))
    for x, y, count in [(40, 460, 35), (690, 430, 47), (35, 1300, 58), (700, 1370, 63)]:
        bubble(d, (x, y), "...", count, 330)
    for line in [(160, 790, 70, 730), (910, 760, 1000, 700), (180, 1160, 70, 1220), (900, 1160, 1010, 1230)]:
        d.line(line, fill=RED, width=15)
    return im


def frame_5():
    im, d = base(5, "0:08–0:10", "MYBOTICA ПРИХОДИТ НА ПОМОЩЬ")
    paste_pose(im, 5, (570, 970, 1010, 1510))
    paste_mark(im, (120, 500, 650, 980))
    for line in [(135, 540, 70, 480), (120, 720, 45, 720), (150, 900, 80, 970), (615, 540, 680, 475), (630, 720, 720, 720), (610, 910, 690, 985)]:
        d.line(line, fill=RED, width=14)
    d.text((385, 1040), "mybotica", font=font(70, True), fill=GREEN, anchor="mm")
    d.text((540, 1690), "Поток сообщений наконец останавливается", font=font(38), fill=GREEN, anchor="mm")
    return im


def frame_6():
    im, d = base(6, "0:10–0:12", "MYBOTICA РАБОТАЕТ")
    paste_mark(im, (350, 390, 730, 720))
    check_pill(d, 820, "Ответ отправлен")
    check_pill(d, 990, "Запись создана")
    check_pill(d, 1160, "Заявка передана")
    paste_pose(im, 2, (710, 1390, 1010, 1740))
    return im


def frame_7():
    im, d = base(7, "0:12–0:14", "ТЕПЕРЬ МОЖНО ВЫДОХНУТЬ")
    paste_pose(im, 12, (160, 500, 920, 1440))
    d.text((540, 1660), "Чат разобран. Кофе ещё горячий.", font=font(41), fill=GREEN, anchor="mm")
    return im


def frame_8():
    im, d = base(8, "0:14–0:16", "ЗНАК СТАНОВИТСЯ ЛОГОТИПОМ")
    d.ellipse((-160, 340, 1240, 1740), fill=GREEN)
    paste_mark(im, (225, 600, 855, 1260), white=True)
    d.arc((-210, 290, 1290, 1790), 205, 500, fill=RED, width=20)
    d.text((540, 1570), "Графический дубль головы заполняет экран", font=font(38), fill=CREAM, anchor="mm")
    return im


def frame_9():
    im, d = base(9, "0:16–0:20", "MYBOTICA", green=True)
    paste_logo(im, (100, 510, 980, 850))
    d.line((180, 930, 900, 930), fill=RED, width=12)
    d.multiline_text((540, 1080), "MyBotica работает —\nты пьёшь кофе", font=font(62, True), fill=CREAM, anchor="ma", align="center", spacing=18)
    d.rounded_rectangle((150, 1500, 930, 1650), radius=68, fill=RED)
    d.text((540, 1575), "ПОДПИСЫВАЙТЕСЬ НА ЗАПУСК", font=font(39, True), fill=WHITE, anchor="mm")
    return im


frames = [frame_1(), frame_2(), frame_3(), frame_4(), frame_5(), frame_6(), frame_7(), frame_8(), frame_9()]

for i, frame in enumerate(frames, 1):
    frame.convert("RGB").save(OUT / f"frame-{i:02d}.jpg", quality=95)

thumb_w, thumb_h = 270, 480
gap, header = 24, 180
sheet = Image.new("RGB", (gap + 3 * (thumb_w + gap), header + gap + 3 * (thumb_h + gap)), CREAM)
sd = ImageDraw.Draw(sheet)
sd.text((sheet.width // 2, 50), "MYBOTICA — ЧАТ ЗАВАЛИЛО", font=font(58, True), fill=GREEN, anchor="ma")
sd.text((sheet.width // 2, 120), "раскадровка v3 · спасение → работа → кофе → логотип", font=font(27), fill=RED, anchor="ma")

for i, frame in enumerate(frames):
    thumb = frame.convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    x = gap + (i % 3) * (thumb_w + gap)
    y = header + gap + (i // 3) * (thumb_h + gap)
    sheet.paste(thumb, (x, y))
    sd.rounded_rectangle((x, y, x + thumb_w, y + thumb_h), radius=18, outline=GREEN, width=4)

sheet.save(ROOT / "storyboard-chat-overload-v3.jpg", quality=95)
print(ROOT / "storyboard-chat-overload-v3.jpg")
