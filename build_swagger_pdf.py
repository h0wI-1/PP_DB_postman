"""
Генерирует PDF-отчёт по Swagger из docs/report_swagger.md.
Встраивает PNG-скриншоты из screenshots/figSW*.png.
Стиль: Times New Roman 14pt, A4, поля L=3/R=1.5/T=2/B=2 см.
"""

import re
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Image as RLImage, Table, TableStyle, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import HRFlowable

BASE = Path("/Users/howis/Downloads/ПИ лаба 4")
SHOTS = BASE / "screenshots"
OUT   = BASE / "Отчёт_ПИ_лаба_4_Swagger.pdf"

# ─── Шрифты ───────────────────────────────────────────────────────────────────
# На macOS Times New Roman доступен в /Library/Fonts
FONT_PATHS = [
    ("/Library/Fonts/Times New Roman.ttf",         "TimesNR"),
    ("/Library/Fonts/Times New Roman Bold.ttf",    "TimesNR-Bold"),
    ("/Library/Fonts/Times New Roman Italic.ttf",  "TimesNR-Italic"),
    ("/Library/Fonts/Courier New.ttf",             "CourierNR"),
    ("/Library/Fonts/Courier New Bold.ttf",        "CourierNR-Bold"),
]
ALT_PATHS = [
    ("/System/Library/Fonts/Supplemental/Times New Roman.ttf",         "TimesNR"),
    ("/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",    "TimesNR-Bold"),
    ("/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf",  "TimesNR-Italic"),
    ("/System/Library/Fonts/Supplemental/Courier New.ttf",             "CourierNR"),
    ("/System/Library/Fonts/Supplemental/Courier New Bold.ttf",        "CourierNR-Bold"),
]

def try_reg(path, name):
    try:
        pdfmetrics.registerFont(TTFont(name, path))
        return True
    except Exception:
        return False

for path, name in FONT_PATHS + ALT_PATHS:
    if Path(path).exists():
        try_reg(path, name)

# Fallback: use Helvetica if Times not found
def font(bold=False, italic=False):
    try:
        if bold:   return "TimesNR-Bold"
        if italic: return "TimesNR-Italic"
        return "TimesNR"
    except Exception:
        return "Helvetica-Bold" if bold else "Helvetica"

BODY   = 14
SMALL  = 11
CODE_S = 10

# ─── Стили ────────────────────────────────────────────────────────────────────
BODY_STYLE = ParagraphStyle(
    "body", fontName="TimesNR", fontSize=BODY, leading=20,
    alignment=TA_JUSTIFY, firstLineIndent=1.25*cm,
    spaceAfter=0, spaceBefore=0,
)
H1_STYLE = ParagraphStyle(
    "h1", fontName="TimesNR-Bold", fontSize=BODY, leading=20,
    alignment=TA_CENTER, spaceAfter=6, spaceBefore=12,
)
H2_STYLE = ParagraphStyle(
    "h2", fontName="TimesNR-Bold", fontSize=BODY, leading=20,
    alignment=TA_LEFT, spaceAfter=3, spaceBefore=8,
)
H3_STYLE = ParagraphStyle(
    "h3", fontName="TimesNR-Bold", fontSize=BODY, leading=20,
    alignment=TA_LEFT, spaceAfter=3, spaceBefore=6,
)
CAPTION_STYLE = ParagraphStyle(
    "cap", fontName="TimesNR", fontSize=SMALL, leading=14,
    alignment=TA_CENTER, spaceBefore=3, spaceAfter=8,
)
CODE_STYLE = ParagraphStyle(
    "code", fontName="Courier", fontSize=CODE_S, leading=14,
    alignment=TA_LEFT, spaceAfter=0, spaceBefore=0,
    backColor=colors.HexColor("#F2F2F2"),
    leftIndent=6, rightIndent=6,
)
TITLE_STYLE = ParagraphStyle(
    "title", fontName="TimesNR", fontSize=BODY, leading=20,
    alignment=TA_CENTER, spaceAfter=0, spaceBefore=0,
)
TITLE_BOLD = ParagraphStyle(
    "titlebold", fontName="TimesNR-Bold", fontSize=BODY, leading=20,
    alignment=TA_CENTER, spaceAfter=0, spaceBefore=0,
)

# ─── Утилиты ──────────────────────────────────────────────────────────────────
def sp(h=6):  return Spacer(1, h)

def find_png(num):
    """Найти figSWNN_*.png по номеру."""
    for p in sorted(SHOTS.glob(f"figSW{num:02d}_*.png")):
        return p
    return None

def embed_image(num, caption, max_w=14*cm):
    """Возвращает список: Image + Caption или заглушку если файл не найден."""
    path = find_png(num)
    items = []
    if path and path.exists():
        try:
            from PIL import Image as PILImage
            with PILImage.open(path) as im:
                w, h = im.size
            ratio = h / w
            rw = min(max_w, 14*cm)
            rh = rw * ratio
            items.append(RLImage(str(path), width=rw, height=rh))
        except Exception:
            items.append(RLImage(str(path), width=max_w, height=max_w * 0.6))
    else:
        # Заглушка
        items.append(Paragraph(f"[ СКРИНШОТ — Рисунок {num} ]",
            ParagraphStyle("ph", fontName="TimesNR", fontSize=SMALL,
                           alignment=TA_CENTER, backColor=colors.HexColor("#D9D9D9"),
                           spaceBefore=6, spaceAfter=0, textColor=colors.HexColor("#606060"))))
    items.append(Paragraph(f"Рисунок {num} – {caption}", CAPTION_STYLE))
    return KeepTogether(items)

def body_p(text):
    # Простое преобразование inline-разметки
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'`(.+?)`', r'<font name="Courier" size="12">\1</font>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    return Paragraph(text, BODY_STYLE)

def code_lines(block):
    """Кодовый блок → список параграфов."""
    out = [sp(4)]
    for line in block.split("\n"):
        line_e = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        out.append(Paragraph(line_e if line_e.strip() else "&nbsp;", CODE_STYLE))
    out.append(sp(4))
    return out

# ─── Контент ──────────────────────────────────────────────────────────────────
story = []

# Титульный лист
def tp(text, bold=False, size=None):
    st = ParagraphStyle("tp", fontName="TimesNR-Bold" if bold else "TimesNR",
                        fontSize=size or BODY, leading=20, alignment=TA_CENTER,
                        spaceAfter=0, spaceBefore=0)
    story.append(Paragraph(text, st))
    story.append(sp(2))

tp("МИНИСТЕРСТВО ЦИФРОВОГО РАЗВИТИЯ, СВЯЗИ И МАССОВЫХ")
tp("КОММУНИКАЦИЙ РОССИЙСКОЙ ФЕДЕРАЦИИ")
tp("Федеральное государственное бюджетное образовательное учреждение")
tp("высшего образования")
tp('«Московский технический университет связи и информатики»')
story.append(sp(24))
tp("Кафедра «Системное программирование»")
story.append(sp(24))
tp("Отчёт по лабораторной работе", bold=True)
tp("по дисциплине «Программная инженерия»")
tp("на тему «Документирование REST API интернет-магазина с помощью Swagger»")
story.append(sp(28))

right_style = ParagraphStyle("right", fontName="TimesNR", fontSize=BODY,
                              leading=20, alignment=TA_RIGHT)
story.append(Paragraph("Выполнил: студент группы ________", right_style))
story.append(sp(2))
story.append(Paragraph("Солотонов А.Э.", right_style))
story.append(sp(6))
story.append(Paragraph("Проверил: ________________________", right_style))
story.append(sp(40))
tp("Москва 2026")
story.append(PageBreak())

# ── РАЗДЕЛ 1 ──────────────────────────────────────────────────────────────────
story.append(Paragraph("1. Цель работы", H1_STYLE))

story.append(body_p(
    "Целью данного раздела лабораторной работы является освоение инструментария для "
    "документирования REST API на основе стандарта OpenAPI 3.0. В ходе работы "
    "разработана спецификация API интернет-магазина техники в формате YAML, после "
    "чего она была визуализирована через Swagger UI — интерактивную веб-страницу, "
    "которая позволяет просматривать документацию и отправлять HTTP-запросы "
    "непосредственно из браузера."))
story.append(sp())

# ── РАЗДЕЛ 2 ──────────────────────────────────────────────────────────────────
story.append(Paragraph("2. Используемые инструменты", H1_STYLE))

story.append(body_p(
    "**OpenAPI 3.0.3** — стандарт описания REST API, разработанный Open API Initiative. "
    "Спецификация записывается в формате YAML или JSON и описывает все конечные точки "
    "API, параметры, тела запросов, ответы и схемы безопасности."))
story.append(sp())
story.append(body_p(
    "**Swagger UI** — библиотека с открытым исходным кодом (версия 5), которая читает "
    "OpenAPI-файл и строит по нему интерактивную HTML-страницу. Не требует сборки: "
    "достаточно одного HTML-файла, подключающего библиотеку через CDN."))
story.append(sp())
story.append(body_p(
    "**PostgreSQL + PostgREST** — стек API, задокументированный в спецификации. "
    "Swagger используется как слой документации поверх уже работающего API."))
story.append(sp())
story.append(body_p("**Браузер** — для открытия Swagger UI; дополнительных программ устанавливать не нужно."))
story.append(sp())

# ── РАЗДЕЛ 3 ──────────────────────────────────────────────────────────────────
story.append(Paragraph("3. Структура спецификации OpenAPI", H1_STYLE))

story.append(body_p(
    "Файл `docs/swagger.yaml` содержит полное описание API интернет-магазина. "
    "Он состоит из нескольких логических блоков, подробно описанных ниже."))
story.append(sp())
story.append(Paragraph("3.1  Заголовок и сервер", H2_STYLE))
story.append(body_p(
    "Блок `info` задаёт название, версию и контактные данные API. "
    "Блок `servers` указывает базовый URL: `http://localhost:3000` — порт PostgREST."))
story.append(sp())
story.extend(code_lines(
    'openapi: 3.0.3\n'
    'info:\n'
    '  title: Shop API — Интернет-магазин техники\n'
    '  version: "1.0.0"\n'
    '  contact:\n'
    '    email: artemsolotonov@gmail.com\n'
    'servers:\n'
    '  - url: http://localhost:3000\n'
    '    description: Локальный сервер PostgREST'
))
story.append(embed_image(1, "Файл swagger.yaml в редакторе: общая структура документа"))

story.append(Paragraph("3.2  Схемы данных (components/schemas)", H2_STYLE))
story.append(body_p(
    "В блоке `components/schemas` описаны переиспользуемые схемы данных. "
    "Для каждой таблицы определено три схемы: полный объект из БД (Client), "
    "тело POST-запроса без `id` (ClientInput) и тело PATCH-запроса с "
    "необязательными полями (ClientPatch). Аналогично — для Item, OrderStatus, Order."))
story.append(sp())
story.append(embed_image(2, "Блок components/schemas: описание схем Client и ClientInput"))

story.append(Paragraph("3.3  Переиспользуемые параметры", H2_STYLE))
story.append(body_p(
    "Часто встречающиеся параметры запросов вынесены в `components/parameters`: "
    "`SelectParam`, `OrderParam`, `LimitParam`, `OffsetParam`, `PreferHeader`. "
    "Это исключает дублирование описания в каждом эндпоинте — параметры "
    "подключаются через ссылку `$ref`."))
story.append(sp())

story.append(Paragraph("3.4  Схема безопасности", H2_STYLE))
story.append(body_p(
    "Тип `http` со схемой `bearer` означает, что токен передаётся в заголовке "
    "`Authorization: Bearer <token>`. В Swagger UI это реализуется через кнопку "
    "**Authorize** в верхней части страницы."))
story.append(sp())
story.extend(code_lines(
    'components:\n'
    '  securitySchemes:\n'
    '    BearerAuth:\n'
    '      type: http\n'
    '      scheme: bearer\n'
    '      bearerFormat: JWT'
))

# ── РАЗДЕЛ 4 ──────────────────────────────────────────────────────────────────
story.append(Paragraph("4. Запуск Swagger UI", H1_STYLE))

story.append(body_p(
    "Для отображения документации подготовлен файл `docs/index.html`. Он подключает "
    "библиотеку Swagger UI через CDN и передаёт ей путь к спецификации:"))
story.append(sp())
story.extend(code_lines(
    'SwaggerUIBundle({\n'
    '  url: "./swagger.yaml",\n'
    '  dom_id: "#swagger-ui",\n'
    '  presets: [SwaggerUIBundle.presets.apis,\n'
    '            SwaggerUIBundle.SwaggerUIStandalonePreset],\n'
    '  layout: "BaseLayout",\n'
    '  deepLinking: true,\n'
    '  tryItOutEnabled: true\n'
    '});'
))
story.append(body_p(
    "Параметр `tryItOutEnabled: true` активирует кнопку **Try it out** для всех "
    "операций сразу. Для запуска используется встроенный HTTP-сервер Python:"))
story.append(sp())
story.extend(code_lines(
    'cd "path/to/ПИ лаба 4/docs"\n'
    'python3 -m http.server 8080'
))
story.append(body_p("После этого открыть в браузере: `http://localhost:8080`"))
story.append(sp())
story.append(embed_image(3, "Запуск HTTP-сервера в терминале"))
story.append(embed_image(4, "Главная страница Swagger UI: заголовок, пять групп операций, кнопка Authorize"))

# ── РАЗДЕЛ 5 ──────────────────────────────────────────────────────────────────
story.append(Paragraph("5. Интерфейс Swagger UI", H1_STYLE))

story.append(body_p(
    "После открытия страницы отображается следующая структура: вверху — название "
    "API, версия, базовый URL сервера; кнопка **Authorize** для ввода Bearer Token; "
    "пять разделов (тегов), каждый сворачивается и разворачивается кликом."))
story.append(sp())
story.append(body_p(
    "Внутри каждого раздела — список операций. Цвет рамки указывает на HTTP-метод: "
    "GET — зелёный (#49cc90), POST — синий (#61affe), PATCH — оранжевый (#fca130), "
    "DELETE — красный (#f93e3e). При раскрытии операции видны параметры, "
    "схема тела запроса, примеры ответов и коды статусов."))
story.append(sp())
story.append(embed_image(5, "Раздел Clients: GET /clients развёрнут, видны параметры фильтрации"))
story.append(embed_image(6, "Примеры ответов (200) для GET /clients"))

# ── РАЗДЕЛ 6 ──────────────────────────────────────────────────────────────────
story.append(Paragraph("6. Авторизация в Swagger UI", H1_STYLE))

story.append(body_p(
    "Для выполнения защищённых запросов (POST, PATCH, DELETE) через кнопку "
    "**Try it out** необходимо сначала получить токен, а затем ввести его "
    "в интерфейс Swagger UI."))
story.append(sp())
story.append(Paragraph("Шаг 1 — получить токен", H2_STYLE))
story.append(body_p(
    "Развернуть раздел **Auth** → операция `POST /rpc/login`. "
    "Нажать **Try it out**. В поле **Request body** ввести email и пароль. "
    "Нажать **Execute**. В блоке **Responses** → **Response body** скопировать "
    "значение поля `token`."))
story.append(sp())
story.extend(code_lines(
    '{\n'
    '  "email": "admin@shop.local",\n'
    '  "password": "password123"\n'
    '}'
))
story.append(embed_image(7, "Запрос POST /rpc/login через Try it out: тело и ответ с токеном"))

story.append(Paragraph("Шаг 2 — авторизоваться", H2_STYLE))
story.append(body_p(
    "В верхней части страницы нажать кнопку **Authorize** (иконка замка). "
    "В открывшемся окне в поле **BearerAuth (http, Bearer)** вставить "
    "скопированный токен. Нажать **Authorize**, затем **Close**."))
story.append(sp())
story.append(body_p(
    "После этого все операции, помеченные иконкой замка, будут выполняться "
    "с заголовком `Authorization: Bearer <token>` автоматически. Замок рядом "
    "с операцией «закроется», сигнализируя об активной авторизации."))
story.append(sp())
story.append(embed_image(8, "Диалог Authorize: ввод Bearer Token"))
story.append(embed_image(9, "Иконка закрытого замка рядом с POST /clients после авторизации"))

# ── РАЗДЕЛ 7 ──────────────────────────────────────────────────────────────────
story.append(Paragraph("7. Тестирование запросов через Try it out", H1_STYLE))

story.append(Paragraph("7.1  GET-запросы", H2_STYLE))
story.append(body_p(
    "**GET /clients** — развернуть операцию, нажать **Execute**. "
    "В поле **Response body** выводится массив JSON с клиентами, код ответа — 200."))
story.append(sp())
story.append(body_p(
    "**GET /clients?id=eq.1** — заполнить поле `id` значением `eq.1` и нажать "
    "**Execute**. В ответе — один объект с клиентом, у которого id = 1."))
story.append(sp())
story.append(body_p(
    "**GET /items?price=gt.40000** — заполнить поле `price` значением `gt.40000`. "
    "В ответе — только товары с ценой выше 40 000 ₽."))
story.append(sp())
story.append(embed_image(10, "Try it out: GET /clients — ответ 200, массив клиентов"))
story.append(embed_image(11, "Try it out: GET /clients с параметром id=eq.1"))
story.append(embed_image(12, "Try it out: GET /items с параметром price=gt.40000"))

story.append(Paragraph("7.2  POST — добавление клиента", H2_STYLE))
story.append(body_p(
    "Развернуть операцию `POST /clients`. В поле **Request body** ввести данные "
    "нового клиента. Swagger UI формирует полный HTTP-запрос с заголовком "
    "авторизации и отправляет его на сервер. В ответе — код `201 Created` и "
    "JSON с созданной записью, включая сгенерированный `id`."))
story.append(sp())
story.extend(code_lines(
    '{\n'
    '  "name": "Test User",\n'
    '  "email": "test.user@example.com",\n'
    '  "phone": "+7-900-000-00-00",\n'
    '  "city": "Тестоград"\n'
    '}'
))
story.append(embed_image(13, "Try it out: POST /clients — заполненное тело запроса"))
story.append(embed_image(14, "Try it out: POST /clients — ответ 201, созданная запись с id"))

story.append(Paragraph("7.3  PATCH — изменение записи", H2_STYLE))
story.append(body_p(
    "Развернуть операцию `PATCH /clients`. В параметре `id` указать "
    "`eq.<id нового клиента>`. В теле запроса передать изменяемые поля. "
    "Нажать **Execute**. Код ответа — 200, в теле — обновлённая запись."))
story.append(sp())
story.extend(code_lines(
    '{ "phone": "+7-900-999-99-99", "city": "Москва" }'
))
story.append(embed_image(15, "Try it out: PATCH /clients — параметр id и тело запроса"))

story.append(Paragraph("7.4  DELETE — удаление записи", H2_STYLE))
story.append(body_p(
    "Развернуть операцию `DELETE /clients`. В параметре `id` указать "
    "`eq.<id нового клиента>`. Нажать **Execute**. Код ответа — 200. "
    "Для проверки повторно выполнить `GET /clients?id=eq.<id>` — "
    "в ответе придёт пустой массив `[]`, что подтверждает удаление."))
story.append(sp())
story.append(embed_image(16, "Try it out: DELETE /clients — ответ 200"))
story.append(embed_image(17, "Try it out: GET /clients после DELETE — пустой массив []"))

# ── РАЗДЕЛ 8 ──────────────────────────────────────────────────────────────────
story.append(Paragraph("8. Документирование схем данных", H1_STYLE))

story.append(body_p(
    "В нижней части страницы Swagger UI расположен раздел **Schemas**, где "
    "перечислены все компонентные схемы файла `swagger.yaml`. Раскрывая любую "
    "схему, можно увидеть тип каждого поля, формат (`string`, `integer`, "
    "`date-time` и т. д.), обязательные поля и примеры значений."))
story.append(sp())

# Таблица схем
from reportlab.platypus import Table, TableStyle
tdata = [
    ["Схема", "Ключевые поля"],
    ["Client", "id, name, email, phone, city, registered_at"],
    ["ClientInput", "name* (req.), email* (req.), phone, city"],
    ["Item", "id, name, category, price, stock"],
    ["OrderStatus", "id, code, title"],
    ["Order", "id, client_id, item_id, status_id, quantity, total"],
    ["LoginRequest", "email* (req.), password* (req.)"],
    ["LoginResponse", "token"],
]
col_w = [4.5*cm, 9.5*cm]
t = Table(tdata, colWidths=col_w)
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#3b4151")),
    ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
    ("FONTNAME",   (0,0), (-1,0), "TimesNR-Bold"),
    ("FONTSIZE",   (0,0), (-1,-1), 11),
    ("FONTNAME",   (0,1), (-1,-1), "TimesNR"),
    ("GRID",       (0,0), (-1,-1), 0.5, colors.HexColor("#d0d0d0")),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f8f8f8")]),
    ("LEFTPADDING",  (0,0), (-1,-1), 8),
    ("RIGHTPADDING", (0,0), (-1,-1), 8),
    ("TOPPADDING",   (0,0), (-1,-1), 4),
    ("BOTTOMPADDING",(0,0), (-1,-1), 4),
    ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
]))
story.append(sp(6))
story.append(t)
story.append(sp(8))
story.append(embed_image(18, "Раздел Schemas: развёрнутые схемы Client и ClientInput"))

# ── РАЗДЕЛ 9 ──────────────────────────────────────────────────────────────────
story.append(Paragraph("9. Вывод", H1_STYLE))

story.append(body_p(
    "В ходе выполнения работы была разработана спецификация REST API в формате "
    "OpenAPI 3.0, которая охватывает все четыре таблицы базы данных и полностью "
    "описывает операции авторизации, получения, добавления, изменения и удаления "
    "записей. Спецификация хранится в файле `docs/swagger.yaml` и содержит "
    "переиспользуемые схемы данных, параметры запросов и настройку JWT-авторизации."))
story.append(sp())
story.append(body_p(
    "Визуализация выполнена через Swagger UI: файл `docs/index.html` отображает "
    "интерактивную документацию без каких-либо фреймворков или сборщиков. "
    "Все основные операции проверены через кнопку **Try it out** непосредственно "
    "в браузере — POST, PATCH, DELETE с авторизацией по Bearer Token и "
    "последующим проверочным GET."))
story.append(sp())
story.append(body_p(
    "Использование Swagger / OpenAPI упрощает взаимодействие между командой "
    "разработки и тестировщиками: актуальная документация всегда доступна в "
    "браузере и не требует ручной синхронизации."))

# ─── Сохранение ───────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    str(OUT),
    pagesize=A4,
    leftMargin   = 3.0 * cm,
    rightMargin  = 1.5 * cm,
    topMargin    = 2.0 * cm,
    bottomMargin = 2.0 * cm,
    title="Отчёт по лабораторной работе 4 — Swagger",
    author="Солотонов А.Э.",
)
doc.build(story)
print(f"PDF сохранён: {OUT}")
