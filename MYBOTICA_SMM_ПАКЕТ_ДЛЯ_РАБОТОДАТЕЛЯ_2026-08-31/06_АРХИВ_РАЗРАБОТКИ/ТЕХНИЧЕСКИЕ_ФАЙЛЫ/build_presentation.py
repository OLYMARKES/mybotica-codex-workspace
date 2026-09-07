from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "00_ПРЕЗЕНТАЦИЯ_MYBOTICA_SMM.pdf"

GREEN = HexColor("#0F2A24")
GREEN_2 = HexColor("#17483D")
CREAM = HexColor("#F6F2EE")
BURGUNDY = HexColor("#8C1D26")
RED = HexColor("#B42032")
INK = HexColor("#171A18")
MUTED = HexColor("#66716D")
WHITE = HexColor("#FFFFFF")
LINE = HexColor("#DADFD9")
PALE_GREEN = HexColor("#E7EFE9")
PALE_RED = HexColor("#F3E4E3")

PAGE_W, PAGE_H = landscape(A4)


def register_fonts():
    regular = Path("/Users/olymarkes/Library/Fonts/GolosText-Variable.ttf")
    heading = Path("/Users/olymarkes/Library/Fonts/Olymarkes-Cyrillic-Carousel-Pack/Unbounded-VF.ttf")
    bold = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
    pdfmetrics.registerFont(TTFont("Golos", str(regular)))
    pdfmetrics.registerFont(TTFont("Unbounded", str(heading)))
    pdfmetrics.registerFont(TTFont("ArialBold", str(bold)))


def wrap_lines(text, font_name, size, width):
    lines = []
    for paragraph in text.split("\n"):
        if not paragraph:
            lines.append("")
            continue
        words = paragraph.split()
        current = ""
        for word in words:
            trial = word if not current else f"{current} {word}"
            if pdfmetrics.stringWidth(trial, font_name, size) <= width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


def text_block(c, text, x, y_top, width, size=14, leading=None, font="Golos", color=INK, max_lines=None):
    leading = leading or size * 1.35
    lines = wrap_lines(text, font, size, width)
    if max_lines:
        lines = lines[:max_lines]
    c.setFont(font, size)
    c.setFillColor(color)
    y = y_top
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def title(c, kicker, headline, sub=None, dark=False):
    color = WHITE if dark else GREEN
    muted = HexColor("#D9E2DE") if dark else MUTED
    c.setFillColor(BURGUNDY if dark else RED)
    c.roundRect(48, PAGE_H - 62, 116, 22, 11, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("ArialBold", 9)
    c.drawCentredString(106, PAGE_H - 55, kicker.upper())
    c.setFillColor(color)
    c.setFont("Unbounded", 25)
    c.drawString(48, PAGE_H - 106, headline)
    if sub:
        text_block(c, sub, 48, PAGE_H - 130, PAGE_W - 96, 11.5, 16, "Golos", muted)


def footer(c, page_no, dark=False):
    c.setStrokeColor(Color(1, 1, 1, 0.22) if dark else LINE)
    c.line(48, 34, PAGE_W - 48, 34)
    c.setFont("Golos", 8)
    c.setFillColor(HexColor("#C9D6D1") if dark else MUTED)
    c.drawString(48, 18, "MyBotica - SMM-концепция запуска")
    c.drawRightString(PAGE_W - 48, 18, f"{page_no:02d}")


def fit_image(c, path, x, y, w, h, radius=0, bg=None):
    path = Path(path)
    c.setFillAlpha(1)
    c.setStrokeAlpha(1)
    if bg:
        c.setFillColor(bg)
        c.roundRect(x, y, w, h, radius, fill=1, stroke=0)
    with PILImage.open(path) as img:
        iw, ih = img.size
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    dx, dy = x + (w - dw) / 2, y + (h - dh) / 2
    c.drawImage(str(path), dx, dy, dw, dh, preserveAspectRatio=True, mask="auto")


def card(c, x, y, w, h, label, heading, body, accent=GREEN, fill=WHITE):
    c.setFillColor(fill)
    c.setStrokeColor(LINE)
    c.roundRect(x, y, w, h, 14, fill=1, stroke=1)
    c.setFillColor(accent)
    c.roundRect(x + 18, y + h - 34, 76, 18, 9, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("ArialBold", 8)
    c.drawCentredString(x + 56, y + h - 28, label.upper())
    c.setFillColor(GREEN)
    c.setFont("ArialBold", 14)
    c.drawString(x + 18, y + h - 58, heading)
    text_block(c, body, x + 18, y + h - 79, w - 36, 10.5, 14.5, "Golos", INK)


def bullet_list(c, items, x, y_top, width, size=12, leading=17, color=INK, bullet_color=RED):
    y = y_top
    for item in items:
        c.setFillColor(bullet_color)
        c.circle(x + 4, y + 3, 3, fill=1, stroke=0)
        y = text_block(c, item, x + 16, y + 8, width - 16, size, leading, "Golos", color) - 5
    return y


def new_page(c, page_no, dark=False):
    c.setFillColor(GREEN if dark else CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    footer(c, page_no, dark)


def build():
    register_fonts()
    c = canvas.Canvas(str(OUT), pagesize=(PAGE_W, PAGE_H))
    c.setTitle("MyBotica - SMM-концепция запуска")
    c.setAuthor("MyBotica SMM")

    # 1. Cover
    new_page(c, 1, dark=True)
    c.setFillColor(BURGUNDY)
    c.roundRect(48, PAGE_H - 72, 132, 24, 12, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("ArialBold", 9)
    c.drawCentredString(114, PAGE_H - 64, "SMM START PACKAGE")
    c.setFillColor(WHITE)
    c.setFont("Unbounded", 36)
    c.drawString(48, PAGE_H - 140, "MyBotica")
    c.setFont("Unbounded", 25)
    c.drawString(48, PAGE_H - 182, "соцсети до запуска продукта")
    text_block(
        c,
        "Стратегия, два персонажа, три готовых ролика, Telegram-оформление, рубрики и контент-план первой недели.",
        48,
        PAGE_H - 225,
        470,
        15,
        21,
        "Golos",
        HexColor("#D7E1DD"),
    )
    c.setFillColor(Color(1, 1, 1, 0.08))
    c.roundRect(570, 76, 220, 430, 28, fill=1, stroke=0)
    fit_image(c, ROOT / "02_ПЕРСОНАЖИ/01_ОСНОВНОЙ_ПЕРСОНАЖ/03_ЛИСТ_ЭМОЦИЙ_И_ДЕЙСТВИЙ.png", 585, 92, 190, 398)
    c.setFont("Golos", 10)
    c.setFillColor(HexColor("#B9CBC4"))
    c.drawString(48, 72, "Подготовлено 31 августа 2026")
    c.showPage()

    # 2. Executive summary
    new_page(c, 2)
    title(c, "идея", "Что предлагается", "Запускать MyBotica через понятную пользу, узнаваемые боли и честную историю создания продукта.")
    card(c, 48, 304, 224, 142, "01", "Объяснять", "Показывать на реальных диалогах, что именно можно передать AI-помощнику.")
    card(c, 286, 304, 224, 142, "02", "Развлекать", "Использовать картонного дракошу для сухого абсурда и пересылаемых роликов.", accent=BURGUNDY)
    card(c, 524, 304, 270, 142, "03", "Строить публично", "Честно показывать тесты, маленькие победы, ошибки и решения команды.", accent=GREEN_2)
    c.setFillColor(GREEN)
    c.roundRect(48, 92, 746, 174, 18, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Unbounded", 20)
    c.drawString(72, 224, "Главная коммуникационная мысль")
    c.setFont("Unbounded", 27)
    c.drawString(72, 166, "Клиенты пишут.")
    c.drawString(72, 126, "MyBotica отвечает. Ты пьёшь кофе.")
    c.setFillColor(HexColor("#C6D6D0"))
    c.setFont("Golos", 10)
    c.drawRightString(770, 108, "Просто, конкретно, без технического снобизма")
    c.showPage()

    # 3. Product / audience
    new_page(c, 3)
    title(c, "позиционирование", "Кому и зачем", "Аудитория должна узнать собственную рутину раньше, чем услышит слово «нейросеть».")
    c.setFillColor(WHITE)
    c.setStrokeColor(LINE)
    c.roundRect(48, 88, 352, 370, 18, fill=1, stroke=1)
    c.setFillColor(GREEN)
    c.setFont("Unbounded", 17)
    c.drawString(72, 420, "Основная аудитория")
    bullet_list(c, [
        "Владельцы малого бизнеса",
        "Самозанятые и специалисты",
        "Администраторы и менеджеры",
        "Команды, которые теряют заявки",
        "Люди, которым AI пока непонятен",
    ], 72, 378, 292, 12.5, 18)
    c.setFillColor(PALE_GREEN)
    c.roundRect(424, 278, 370, 180, 18, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.setFont("Unbounded", 17)
    c.drawString(448, 420, "Проблема")
    text_block(c, "Клиенты задают одинаковые вопросы, пишут вечером и ждут быстрый ответ. Человек тратит время на первый контакт вместо сложной работы.", 448, 384, 320, 13, 19, "Golos", INK)
    c.setFillColor(PALE_RED)
    c.roundRect(424, 88, 370, 166, 18, fill=1, stroke=0)
    c.setFillColor(BURGUNDY)
    c.setFont("Unbounded", 17)
    c.drawString(448, 218, "Роль MyBotica")
    text_block(c, "Ответить на частый вопрос, уточнить запрос, собрать контакты и передать сложную ситуацию человеку. Обещания публикуются только после подтверждения команды.", 448, 182, 320, 13, 19, "Golos", INK)
    c.showPage()

    # 4. Characters
    new_page(c, 4)
    title(c, "персонажи", "Два режима одного бренда", "Внешность и палитра сохраняются; меняются материал, пластика и функция контента.")
    c.setFillColor(WHITE)
    c.roundRect(48, 78, 360, 384, 18, fill=1, stroke=0)
    fit_image(c, ROOT / "02_ПЕРСОНАЖИ/01_ОСНОВНОЙ_ПЕРСОНАЖ/03_ЛИСТ_ЭМОЦИЙ_И_ДЕЙСТВИЙ.png", 66, 214, 324, 218)
    c.setFillColor(GREEN)
    c.setFont("Unbounded", 16)
    c.drawString(70, 178, "Основной дракоша")
    text_block(c, "Полезный, дружелюбный, объясняющий. Карточки, инструкции, новости продукта, функции и кейсы.", 70, 148, 310, 11.5, 16, "Golos", INK)
    c.setFillColor(WHITE)
    c.roundRect(432, 78, 362, 384, 18, fill=1, stroke=0)
    fit_image(c, ROOT / "02_ПЕРСОНАЖИ/02_КАРТОННЫЙ_ТРЭШ_ПЕРСОНАЖ/02_ЛИСТ_ПОЗ_КАРТОННОГО_ДРАКОШИ.png", 454, 206, 318, 226)
    c.setFillColor(BURGUNDY)
    c.setFont("Unbounded", 16)
    c.drawString(456, 178, "Картонный дракоша")
    text_block(c, "Уставшее альтер эго для абсурдных коротких видео: неловкие паузы, крупные планы и сухая реакция.", 456, 148, 310, 11.5, 16, "Golos", INK)
    c.showPage()

    # 5. Visual rules
    new_page(c, 5)
    title(c, "система", "Что нельзя потерять", "Эти правила удерживают персонажа и бренд узнаваемыми во всех форматах.")
    fit_image(c, ROOT / "02_ПЕРСОНАЖИ/01_ОСНОВНОЙ_ПЕРСОНАЖ/04_КАНОНИЧЕСКИЙ_ПЕРСОНАЖ_СМОТРИТ_ВЛЕВО.jpeg", 48, 105, 238, 335, 16, WHITE)
    c.setFillColor(WHITE)
    c.roundRect(312, 105, 482, 335, 18, fill=1, stroke=0)
    bullet_list(c, [
        "Голова повторяет знак MyBotica: чат-облачко с диагональной нижней линией.",
        "Дракоша всегда смотрит влево; персонажа не зеркалить вправо.",
        "Два одинаковых круглых тёмно-зелёных глаза; без новой мимики и анатомии.",
        "Белое грушевидное тело, три бордовых шипа, крыло и хвост.",
        "Основные цвета: #0F2A24, #F6F2EE, #8C1D26.",
        "Фирменный зелёный не заменяется чёрным, особенно в аватаре и контуре головы.",
    ], 338, 402, 428, 11.2, 15.5)
    c.showPage()

    # 6. Video 1
    new_page(c, 6)
    title(c, "готовый ролик 01", "Loading 85%", "Продукт собирается по пикселю и честно зависает до завершения запуска.")
    fit_image(c, ROOT / "03_ГОТОВЫЕ_РОЛИКИ/01_LOADING_85_ПРЕВЬЮ.jpg", 48, 70, 218, 350, 18, WHITE)
    fit_image(c, ROOT / "04_СЦЕНАРИИ_И_РАСКАДРОВКИ/01_LOADING_85/01_РАСКАДРОВКА.png", 292, 210, 502, 210, 14, WHITE)
    c.setFillColor(GREEN)
    c.setFont("Unbounded", 14)
    c.drawString(292, 180, "Драматургия")
    bullet_list(c, [
        "Один пиксель и длинное ожидание",
        "12% - 31% - 52% - 68% - 85%",
        "Точный персонаж собирается без перерисовки",
        "Финал: MyBotica + LOADING... 85%",
    ], 292, 152, 502, 10.8, 14.5)
    c.showPage()

    # 7. Video 2
    new_page(c, 7)
    title(c, "готовый ролик 02", "Чат завалило", "Проблема - помощь MyBotica - результат - кофе. Спасение показано до отдыха героя.")
    fit_image(c, ROOT / "03_ГОТОВЫЕ_РОЛИКИ/02_ЧАТ_ЗАВАЛИЛО_ПРЕВЬЮ.jpg", 48, 70, 218, 350, 18, WHITE)
    fit_image(c, ROOT / "04_СЦЕНАРИИ_И_РАСКАДРОВКИ/02_ЧАТ_ЗАВАЛИЛО/01_РАСКАДРОВКА.jpg", 292, 70, 238, 350, 14, WHITE)
    c.setFillColor(WHITE)
    c.roundRect(554, 70, 240, 350, 18, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.setFont("Unbounded", 14)
    c.drawString(576, 382, "Сюжет")
    bullet_list(c, [
        "Первые вопросы",
        "Поток растёт",
        "MyBotica приходит на помощь",
        "Ответы отправлены",
        "Только теперь появляется кофе",
    ], 576, 350, 192, 10.8, 14.5)
    c.setFillColor(BURGUNDY)
    c.roundRect(576, 102, 196, 96, 12, fill=1, stroke=0)
    text_block(c, "Клиенты пишут.\nMyBotica отвечает.\nТы пьёшь кофе.", 592, 174, 166, 13.5, 19, "ArialBold", WHITE)
    c.showPage()

    # 8. Video 3
    new_page(c, 8)
    title(c, "готовый ролик 03", "День у кого?", "Картонный трэш-формат: глубокая ночь, сообщение клиента и слишком честная реакция.")
    fit_image(c, ROOT / "03_ГОТОВЫЕ_РОЛИКИ/03_ДЕНЬ_У_КОГО_ПРЕВЬЮ.jpg", 48, 70, 218, 350, 18, WHITE)
    fit_image(c, ROOT / "04_СЦЕНАРИИ_И_РАСКАДРОВКИ/03_ДЕНЬ_У_КОГО/01_ПОЛНАЯ_РАСКАДРОВКА_ПЕРВОНАЧАЛЬНОЙ_ВЕРСИИ.png", 292, 70, 238, 350, 14, WHITE)
    c.setFillColor(WHITE)
    c.roundRect(554, 70, 240, 350, 18, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.setFont("Unbounded", 14)
    c.drawString(576, 382, "Финальная версия")
    bullet_list(c, [
        "Дракоша сидит за столом",
        "Цифровые часы: 23:30",
        "На компьютере: «Добрый день!»",
        "Мысль: «День? У кого?»",
        "Сверчки, уведомление и звук мысли",
        "Чистый зелёный бренд-финал",
    ], 576, 350, 192, 10.5, 14)
    c.setFillColor(PALE_RED)
    c.roundRect(576, 94, 196, 82, 12, fill=1, stroke=0)
    text_block(c, "Психологическая устойчивость в тариф не входит.", 590, 152, 168, 11.3, 15, "ArialBold", BURGUNDY)
    c.showPage()

    # 9. Platform roles
    new_page(c, 9)
    title(c, "площадки", "Instagram привлекает. Telegram объясняет.", "Одна контентная идея получает две упаковки вместо дословного копирования.")
    c.setFillColor(WHITE)
    c.roundRect(48, 92, 352, 350, 18, fill=1, stroke=0)
    c.setFillColor(BURGUNDY)
    c.setFont("Unbounded", 20)
    c.drawString(74, 400, "Instagram")
    text_block(c, "Витрина и первое знакомство", 74, 366, 290, 13, 18, "ArialBold", GREEN)
    bullet_list(c, [
        "Остановить внимание",
        "Дать узнаваемую эмоцию",
        "Показать персонажа и визуальный мир",
        "Получить пересылку или подписку",
        "Привести в Telegram или на запуск",
    ], 74, 322, 290, 11.5, 16)
    c.setFillColor(PALE_RED)
    c.roundRect(74, 122, 300, 74, 12, fill=1, stroke=0)
    text_block(c, "4 публикации + 4 пакета Stories", 94, 169, 260, 13.5, 18, "ArialBold", BURGUNDY)
    c.setFillColor(WHITE)
    c.roundRect(424, 92, 370, 350, 18, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.setFont("Unbounded", 20)
    c.drawString(450, 400, "Telegram")
    text_block(c, "Глубина, доверие и обратная связь", 450, 366, 316, 13, 18, "ArialBold", BURGUNDY)
    bullet_list(c, [
        "Объяснить продукт подробнее",
        "Показать реальные диалоги",
        "Вести дневник разработки",
        "Собирать ответы через опросы",
        "Готовить аудиторию к запуску",
    ], 450, 322, 316, 11.5, 16)
    c.setFillColor(PALE_GREEN)
    c.roundRect(450, 122, 318, 74, 12, fill=1, stroke=0)
    text_block(c, "7 публикаций, включая закреп", 470, 169, 278, 13.5, 18, "ArialBold", GREEN)
    c.showPage()

    # 10. Instagram week
    new_page(c, 10)
    title(c, "instagram", "Первая неделя в ленте и Stories", "Три ролика уже готовы; дополнительно нужны одна карусель и четыре простых Stories-пакета.")
    fit_image(c, ROOT / "03_ГОТОВЫЕ_РОЛИКИ/01_LOADING_85_ПРЕВЬЮ.jpg", 48, 164, 128, 246, 14, WHITE)
    fit_image(c, ROOT / "03_ГОТОВЫЕ_РОЛИКИ/03_ДЕНЬ_У_КОГО_ПРЕВЬЮ.jpg", 188, 164, 128, 246, 14, WHITE)
    fit_image(c, ROOT / "03_ГОТОВЫЕ_РОЛИКИ/02_ЧАТ_ЗАВАЛИЛО_ПРЕВЬЮ.jpg", 328, 164, 128, 246, 14, WHITE)
    c.setFillColor(WHITE)
    c.roundRect(480, 164, 314, 246, 16, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.setFont("Unbounded", 14)
    c.drawString(504, 374, "Лента: 4 единицы")
    bullet_list(c, [
        "Reel: Loading 85%",
        "Карусель: что можно отдать AI",
        "Reel: День у кого?",
        "Reel: Чат завалило",
    ], 504, 342, 266, 11, 15)
    c.setFillColor(BURGUNDY)
    c.setFont("Unbounded", 14)
    c.drawString(504, 258, "Stories: 4 пакета")
    bullet_list(c, [
        "Тизер создания",
        "Опрос о рутине",
        "Закулисье и тесты",
        "Приглашение на запуск",
    ], 504, 226, 266, 11, 15, INK, BURGUNDY)
    c.setFillColor(GREEN)
    c.roundRect(48, 82, 746, 56, 14, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("ArialBold", 12)
    c.drawString(70, 104, "Instagram: увидел → узнал себя → заинтересовался → перешёл в Telegram или на запуск.")
    c.showPage()

    # 11. Instagram highlights
    new_page(c, 11)
    title(c, "актуальное", "Шесть разделов Instagram", "На старте не создаём пустые «Отзывы», «Кейсы» и «Тарифы» - только подтверждённый контент.")
    highlights = [
        ("НАЧАТЬ", "Что такое MyBotica и зачем подписываться", "01", GREEN),
        ("ЧТО МОЖНО", "Частые вопросы, контакты и первичная заявка", "02", BURGUNDY),
        ("КАК", "Клиент → MyBotica → менеджер", "03", GREEN_2),
        ("СОЗДАЁМ", "Loading, тесты, ошибки и раскадровки", "85%", GREEN),
        ("ЗАПУСК", "Первые 100 и ссылка раннего доступа", "100", BURGUNDY),
        ("ДРАКОША", "Два характера и лучшие смешные ролики", "DRG", GREEN_2),
    ]
    for i, (name, desc, symbol, color) in enumerate(highlights):
        col, row = i % 3, i // 3
        x = 48 + col * 252
        y = 292 - row * 168
        c.setFillColor(WHITE)
        c.roundRect(x, y, 226, 142, 16, fill=1, stroke=0)
        c.setFillColor(color)
        c.circle(x + 46, y + 92, 27, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("ArialBold", 9 if len(symbol) > 2 else 12)
        c.drawCentredString(x + 46, y + 89, symbol)
        c.setFillColor(GREEN)
        c.setFont("ArialBold", 12)
        c.drawString(x + 84, y + 105, name)
        text_block(c, desc, x + 84, y + 80, 124, 9.7, 13, "Golos", INK)
    c.showPage()

    # 12. Telegram
    new_page(c, 12)
    title(c, "telegram", "Канал как живая лента", "Три карточки в макете - это три отдельных поста, связанные рубриками и закреплённой навигацией.")
    fit_image(c, ROOT / "05_TELEGRAM/01_ФИНАЛЬНЫЙ_МАКЕТ_КАНАЛА.png", 48, 70, 258, 350, 18, WHITE)
    c.setFillColor(WHITE)
    c.roundRect(334, 70, 460, 350, 18, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.setFont("Unbounded", 17)
    c.drawString(360, 382, "MyBotica | отвечает за вас")
    text_block(c, "Реальные диалоги, тесты и честный запуск. Показываем, как не терять заявки и освобождать время - простыми словами.", 360, 350, 404, 12.2, 17, "Golos", INK)
    c.setFillColor(BURGUNDY)
    c.setFont("ArialBold", 11)
    c.drawString(360, 280, "КАК УСТРОЕНА ЛЕНТА")
    bullet_list(c, [
        "Каждая карточка или ролик - отдельный пост",
        "Хэштеги открывают публикации одной рубрики",
        "Закреплённый пост объясняет навигацию",
        "Перед приглашением аудитории публикуются четыре стартовых материала",
        "Фирменный зелёный используется вместо почти чёрного",
    ], 360, 252, 404, 11.5, 16)
    c.showPage()

    # 13. Rubrics by platform
    new_page(c, 13)
    title(c, "рубрики", "Одна рубрика - две упаковки", "Instagram показывает идею быстро; Telegram раскрывает её и собирает обратную связь.")
    rubric_rows = [
        ("#можно_боту", "Карусель или короткий Reel", "Подробный разбор и примеры"),
        ("#клиент_пишет", "Смешной ролик", "Ролик + объяснение боли"),
        ("#строим_MyBotica", "Stories и тизеры", "Дневник разработки"),
        ("#без_роботоведения", "Простая визуальная схема", "Развёрнутое объяснение"),
        ("#дракоша_на_смене", "Основной трэш-формат", "Характер и дополнительный контекст"),
    ]
    c.setFillColor(GREEN)
    c.roundRect(48, 404, 746, 40, 9, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("ArialBold", 10)
    c.drawString(66, 419, "РУБРИКА")
    c.drawString(262, 419, "INSTAGRAM")
    c.drawString(522, 419, "TELEGRAM")
    for i, (rubric, insta, telegram) in enumerate(rubric_rows):
        yy = 360 - i * 58
        c.setFillColor(WHITE if i % 2 == 0 else PALE_GREEN)
        c.roundRect(48, yy, 746, 48, 8, fill=1, stroke=0)
        c.setFillColor(BURGUNDY)
        c.setFont("ArialBold", 10.5)
        c.drawString(66, yy + 18, rubric)
        c.setFillColor(INK)
        c.setFont("Golos", 10.5)
        c.drawString(262, yy + 18, insta)
        c.drawString(522, yy + 18, telegram)
    c.setFillColor(GREEN)
    c.roundRect(48, 72, 746, 48, 12, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("ArialBold", 11.5)
    c.drawString(70, 91, "Баланс: 40% польза • 25% юмор • 20% строим публично • 15% вовлечение и запуск.")
    c.showPage()

    # 14. Weekly plan split
    new_page(c, 14)
    title(c, "контент-план", "Первая неделя: две площадки", "Ритм рассчитан так, чтобы не производить отдельный контент с нуля для каждого канала.")
    rows = [
        ("ПН", "Reel Loading 85%", "Закреплённое знакомство"),
        ("ВТ", "Stories: опрос о рутине", "Что можно отдать AI-помощнику"),
        ("СР", "Карусель: 4 диалога", "Подробный разбор 4 диалогов"),
        ("ЧТ", "Reel: День у кого?", "Тот же ролик + расширенная подпись"),
        ("ПТ", "Stories: закулисье", "Что сделали, сломали, тестируем"),
        ("СБ", "Reel: Чат завалило", "Опрос о клиентской рутине"),
        ("ВС", "Stories: приглашение", "Схема работы + CTA на запуск"),
    ]
    c.setFillColor(GREEN)
    c.roundRect(48, 414, 746, 38, 9, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("ArialBold", 10)
    c.drawString(64, 428, "ДЕНЬ")
    c.drawString(126, 428, "INSTAGRAM")
    c.drawString(470, 428, "TELEGRAM")
    for i, (day, insta, tg) in enumerate(rows):
        yy = 364 - i * 43
        c.setFillColor(WHITE if i % 2 == 0 else PALE_GREEN)
        c.roundRect(48, yy, 746, 36, 7, fill=1, stroke=0)
        c.setFillColor(BURGUNDY)
        c.setFont("ArialBold", 10)
        c.drawString(64, yy + 13, day)
        c.setFillColor(INK)
        c.setFont("Golos", 10.3)
        c.drawString(126, yy + 13, insta)
        c.drawString(470, yy + 13, tg)
    c.setFillColor(BURGUNDY)
    c.roundRect(48, 62, 746, 52, 13, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("ArialBold", 11.5)
    c.drawString(70, 82, "Итого: Instagram 4 публикации + 4 Stories-пакета; Telegram 7 постов; около 8 уникальных материалов.")
    c.showPage()

    # 15. Next steps
    new_page(c, 15, dark=True)
    title(c, "следующий шаг", "Что согласовать перед публикацией", dark=True)
    c.setFillColor(Color(1, 1, 1, 0.08))
    c.roundRect(48, 106, 746, 352, 20, fill=1, stroke=0)
    bullet_list(c, [
        "Какие функции продукта уже работают, а какие пока тестируются.",
        "Можно ли обещать ответы 24/7, сбор контактов и передачу сложного запроса человеку.",
        "Какие бонусы получат первые 100 пользователей.",
        "Куда вести людей: форма раннего доступа, бот или сообщение менеджеру.",
        "Какая ссылка будет стоять в профиле Instagram и в закрепе Telegram.",
        "Кто раз в неделю передаёт факты для рубрики #строим_MyBotica.",
    ], 78, 414, 686, 12.2, 18, HexColor("#E7EFEC"), RED)
    c.setFillColor(BURGUNDY)
    c.roundRect(78, 132, 686, 64, 14, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Unbounded", 14)
    c.drawString(102, 160, "После согласования можно собирать канал и публиковать первую неделю.")
    c.save()


if __name__ == "__main__":
    build()
    print(OUT)
