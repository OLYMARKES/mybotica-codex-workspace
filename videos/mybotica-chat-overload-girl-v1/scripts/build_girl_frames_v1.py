from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "source"
OUT = ROOT / "assets" / "frames"
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


EMOTION_SHEET = Image.open(ASSETS / "girl-emotions-v10.png").convert("RGBA")
ACTION_SHEET = Image.open(ASSETS / "girl-actions-v10.png").convert("RGBA")


def pose_crop(sheet, number):
    i = number - 1
    col, row = i % 4, i // 4
    x0 = round(col * sheet.width / 4)
    x1 = round((col + 1) * sheet.width / 4)
    y0 = round(row * sheet.height / 2)
    y1 = round((row + 1) * sheet.height / 2)
    return sheet.crop((x0, y0, x1, y1))


def paste_pose(frame, kind, number, box, opacity=255):
    x0, y0, x1, y1 = box
    sheet = ACTION_SHEET if kind == "action" else EMOTION_SHEET
    pose = ImageOps.contain(pose_crop(sheet, number), (x1 - x0, y1 - y0), Image.Resampling.LANCZOS)
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
    x0, x1 = 110, 970
    draw.rounded_rectangle((x0, y, x1, y + 126), radius=32, fill=WHITE, outline=GREEN, width=5)
    draw.ellipse((x0 + 30, y + 34, x0 + 88, y + 92), outline=GREEN, width=6)
    draw.line((x0 + 44, y + 64, x0 + 56, y + 78, x0 + 77, y + 48), fill=GREEN, width=7, joint="curve")
    draw.text((x0 + 116, y + 63), text, font=font(41, True), fill=GREEN, anchor="lm")


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


def paste_logo(frame, box, green_ink=False):
    x0, y0, x1, y1 = box
    logo = Image.open(ASSETS / "mybotica-logo-transparent.png").convert("RGBA")
    if green_ink:
        data = []
        for r, g, b, a in logo.getdata():
            if a == 0 or r > g * 1.25:
                data.append((r, g, b, a))
            else:
                data.append((15, 42, 36, a))
        logo.putdata(data)
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
    paste_pose(im, "action", 1, (80, 390, 1000, 1560))
    d.text((540, 1690), "Тишина. Один ноутбук. Никакой паники.", font=font(39), fill=GREEN, anchor="mm")
    return im


def frame_2():
    im, d = base(2, "0:02–0:04", "ПЕРВЫЕ ВОПРОСЫ")
    paste_pose(im, "action", 2, (410, 590, 1040, 1480))
    bubble(d, (60, 500), "Сколько стоит?", width=440)
    bubble(d, (60, 735), "Есть запись?", width=390)
    bubble(d, (60, 970), "Как оплатить?", width=420)
    return im


def frame_3():
    im, d = base(3, "0:04–0:06", "ПОТОК РАСТЁТ")
    paste_pose(im, "emotion", 5, (205, 590, 875, 1430))
    bubble(d, (40, 450), "Есть доставка?", 7, 400)
    bubble(d, (625, 520), "Когда открыты?", 12, 410)
    bubble(d, (55, 1285), "Можно сегодня?", 18, 430)
    bubble(d, (665, 1375), "А скидка?", 23, 340)
    return im


def frame_4():
    im, d = base(4, "0:06–0:08", "СЛИШКОМ МНОГО")
    # Urgency lives at the edges; a giant red container made the whole frame
    # feel boxed-in and competed with the questions.
    for line in [
        (24, 560, 24, 400, 184, 400), (896, 400, 1056, 400, 1056, 560),
        (24, 1650, 24, 1810, 184, 1810), (896, 1810, 1056, 1810, 1056, 1650),
    ]:
        d.line(line, fill=RED, width=14, joint="curve")
    paste_pose(im, "emotion", 8, (175, 555, 905, 1445))
    for x, y, text, count in [
        (40, 460, "Можно сегодня?", 35),
        (690, 430, "Есть доставка?", 47),
        (35, 1300, "Как записаться?", 58),
        (700, 1370, "Когда открыты?", 63),
    ]:
        bubble(d, (x, y), text, count, 330)
    for line in [(145, 800, 65, 750), (925, 780, 1010, 725), (155, 1170, 65, 1225), (925, 1170, 1015, 1230)]:
        d.line(line, fill=RED, width=13)
    return im


def frame_5():
    im, d = base(5, "0:08–0:10", "ПОМОЩЬ УЖЕ ЗДЕСЬ")
    paste_logo(im, (95, 500, 815, 850), green_ink=True)
    paste_pose(im, "emotion", 5, (520, 920, 1040, 1570))
    for line in [(130, 560, 70, 500), (105, 700, 35, 700), (145, 820, 80, 885), (775, 545, 845, 480), (800, 700, 885, 700)]:
        d.line(line, fill=RED, width=13)
    d.text((540, 1710), "Сообщения перестают давить на тебя", font=font(39), fill=GREEN, anchor="mm")
    return im


def frame_6():
    im, d = base(6, "0:10–0:12", "MYBOTICA РАБОТАЕТ")
    paste_mark(im, (380, 380, 700, 670))
    check_pill(d, 760, "Ответ отправлен")
    check_pill(d, 930, "Запись создана")
    check_pill(d, 1100, "Заявка передана")
    paste_pose(im, "action", 4, (655, 1330, 1035, 1800))
    return im


def frame_7():
    im, d = base(7, "0:12–0:14", "ТЕПЕРЬ МОЖНО ВЫДОХНУТЬ")
    paste_pose(im, "action", 8, (90, 450, 990, 1550))
    d.text((540, 1690), "Чат разобран. Кофе ещё горячий.", font=font(41), fill=GREEN, anchor="mm")
    return im


def frame_8():
    im, d = base(8, "0:14–0:16", "ЗНАК СТАНОВИТСЯ ЛОГОТИПОМ", green=True)
    paste_mark(im, (185, 510, 895, 1260), white=True)
    d.arc((115, 440, 965, 1330), 205, 335, fill=RED, width=18)
    d.text((540, 1570), "Голова дракоши превращается в знак", font=font(38), fill=CREAM, anchor="mm")
    return im


def frame_9():
    im = Image.new("RGBA", (W, H), GREEN)
    d = ImageDraw.Draw(im)
    paste_logo(im, (90, 430, 990, 800))
    d.line((335, 895, 745, 895), fill=RED, width=10)
    d.multiline_text((540, 1045), "Клиенты пишут.\nMyBotica отвечает.\nТы пьёшь кофе.", font=font(66, True), fill=CREAM, anchor="ma", align="center", spacing=26)
    return im


frames = [frame_1(), frame_2(), frame_3(), frame_4(), frame_5(), frame_6(), frame_7(), frame_8(), frame_9()]

# Clean reference frames for video generation: no storyboard titles, counters,
# timing labels, production notes, or CTA. The actual chat questions remain.
clean_frames = [frame.copy() for frame in frames]
for i in range(7):
    cd = ImageDraw.Draw(clean_frames[i])
    cd.rectangle((0, 0, W, 370), fill=PAPER)

for i in (0, 4, 6):
    cd = ImageDraw.Draw(clean_frames[i])
    cd.rectangle((0, 1580, W, H), fill=PAPER)

clean_frames[7] = Image.new("RGBA", (W, H), GREEN)
c8d = ImageDraw.Draw(clean_frames[7])
paste_mark(clean_frames[7], (185, 510, 895, 1260), white=True)
c8d.arc((115, 440, 965, 1330), 205, 335, fill=RED, width=18)

for i, frame in enumerate(clean_frames, 1):
    frame.convert("RGB").save(OUT / f"frame-{i:02d}.jpg", quality=96)

thumb_w, thumb_h = 270, 480
gap, header = 24, 180
sheet = Image.new("RGB", (gap + 3 * (thumb_w + gap), header + gap + 3 * (thumb_h + gap)), CREAM)
sd = ImageDraw.Draw(sheet)
sd.text((sheet.width // 2, 50), "MYBOTICA — ЧАТ ЗАВАЛИЛО", font=font(58, True), fill=GREEN, anchor="ma")
sd.text((sheet.width // 2, 120), "раскадровка v5 · Impeccable polish · вопросы → спасение → кофе → слоган", font=font(24), fill=RED, anchor="ma")

for i, frame in enumerate(frames):
    thumb = frame.convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    x = gap + (i % 3) * (thumb_w + gap)
    y = header + gap + (i // 3) * (thumb_h + gap)
    sheet.paste(thumb, (x, y))
    sd.rounded_rectangle((x, y, x + thumb_w, y + thumb_h), radius=18, outline=GREEN, width=4)

sheet.save(ROOT / "snapshots" / "storyboard-chat-overload-girl-v1.jpg", quality=95)
print(ROOT / "snapshots" / "storyboard-chat-overload-girl-v1.jpg")
