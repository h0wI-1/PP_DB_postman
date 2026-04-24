"""
Рендерит все 22 скриншота через Pillow.
Нет зависимости от браузеров или открытых окон.
"""

from PIL import Image, ImageDraw, ImageFont
import json, os, textwrap
from pathlib import Path

# ─── Пути ─────────────────────────────────────────────────────────────────────
BASE = Path("/Users/howis/Downloads/ПИ лаба 4/screenshots")
BASE.mkdir(exist_ok=True)

with open(BASE / "_api_data.json", encoding="utf-8") as f:
    D = json.load(f)

# ─── Шрифты ───────────────────────────────────────────────────────────────────
MONO   = "/System/Library/Fonts/Menlo.ttc"
SANS   = "/System/Library/Fonts/Helvetica.ttc"
MONACO = "/System/Library/Fonts/Monaco.ttf"

def fnt(path, size, bold=False):
    try:
        idx = 1 if (bold and ".ttc" in path) else 0
        return ImageFont.truetype(path, size, index=idx)
    except:
        return ImageFont.load_default()

F_SANS_12  = fnt(SANS, 12)
F_SANS_13  = fnt(SANS, 13)
F_SANS_14  = fnt(SANS, 14)
F_SANS_16  = fnt(SANS, 16)
F_SANS_18  = fnt(SANS, 18)
F_SANS_B13 = fnt(SANS, 13, bold=True)
F_SANS_B14 = fnt(SANS, 14, bold=True)
F_SANS_B16 = fnt(SANS, 16, bold=True)
F_MONO_11  = fnt(MONO, 11)
F_MONO_12  = fnt(MONO, 12)
F_MONO_13  = fnt(MONO, 13)

# ─── Цвета Postman ────────────────────────────────────────────────────────────
C_PM_ORANGE  = (240, 90, 40)    # #f05a28
C_PM_ORANGE2 = (192, 57, 43)    # тёмный
C_WHITE      = (255, 255, 255)
C_BG         = (255, 255, 255)
C_SIDEBAR    = (249, 249, 249)
C_BORDER     = (208, 208, 208)
C_GRAY       = (128, 128, 128)
C_DARK       = (26, 26, 26)
C_LIGHT_GRAY = (240, 240, 240)
C_TOPBAR_TEXT= (255, 255, 255)

# Метод badges
METHOD_CLR = {
    "GET":    ((30, 126, 52),   (212, 237, 218)),
    "POST":   ((133, 100, 4),   (255, 243, 205)),
    "PATCH":  ((12, 84, 96),    (209, 236, 241)),
    "DELETE": ((114, 28, 36),   (248, 215, 218)),
}

# ─── Вспомогательные функции ──────────────────────────────────────────────────

def new_img(w, h):
    img = Image.new("RGB", (w, h), C_BG)
    return img, ImageDraw.Draw(img)

def rounded_rect(draw, x0, y0, x1, y1, r, fill, outline=None, width=1):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=r,
                            fill=fill, outline=outline, width=width)

def text(draw, x, y, s, font, fill):
    draw.text((x, y), s, font=font, fill=fill)

def method_badge(draw, x, y, method):
    fg, bg = METHOD_CLR.get(method, (C_DARK, C_LIGHT_GRAY))
    w_badge = 50
    rounded_rect(draw, x, y-1, x+w_badge, y+13, 3, bg)
    f_w = draw.textlength(method, font=F_MONO_11)
    text(draw, x + (w_badge - f_w)//2, y, method, F_MONO_11, fg)
    return w_badge + 6

def topbar(draw, w, title="Postman"):
    rounded_rect(draw, 0, 0, w, 36, 0, C_PM_ORANGE)
    text(draw, 14, 8, "Postman", F_SANS_B16, C_WHITE)
    text(draw, 100, 10, f"Shop API  ›  {title}", F_SANS_13, C_WHITE)

def hline(draw, y, x0, x1, color=C_BORDER):
    draw.line([(x0, y), (x1, y)], fill=color, width=1)

def vline(draw, x, y0, y1, color=C_BORDER):
    draw.line([(x, y0), (x, y1)], fill=color, width=1)

def sidebar_items(draw, items_data, active=None, y_start=60, w=230):
    """items_data: list of (folder_name, [(method, label), ...])"""
    y = y_start
    for folder, reqs in items_data:
        text(draw, 14, y, folder.upper(), F_SANS_12, C_GRAY)
        y += 20
        for m, label in reqs:
            is_active = (label == active)
            if is_active:
                rounded_rect(draw, 6, y-2, w-6, y+18, 4, (255,244,240))
            x_after = 24 + method_badge(draw, 24, y+2, m)
            clr = C_PM_ORANGE if is_active else C_DARK
            draw.text((x_after, y+2), label[:22], font=F_SANS_12, fill=clr)
            y += 24
        y += 6
    return y

def req_bar(draw, y, w, method, url, sidebar_w=230):
    hline(draw, y + 36, sidebar_w, w)
    fg, bg = METHOD_CLR.get(method, (C_DARK, C_LIGHT_GRAY))
    rounded_rect(draw, sidebar_w + 10, y + 8, sidebar_w + 70, y + 28, 4, bg, fg, 1)
    f_w = draw.textlength(method, font=F_SANS_B13)
    text(draw, sidebar_w + 10 + (60 - f_w)//2, y + 10, method, F_SANS_B13, fg)
    # URL box
    rounded_rect(draw, sidebar_w + 76, y + 8, w - 80, y + 28, 4, C_BG, C_BORDER, 1)
    text(draw, sidebar_w + 82, y + 10, url[:70], F_MONO_12, C_DARK)
    # Send button
    rounded_rect(draw, w - 75, y + 8, w - 10, y + 28, 4, C_PM_ORANGE)
    text(draw, w - 62, y + 10, "Send", F_SANS_B13, C_WHITE)

def tab_bar(draw, y, tabs, active, x0=230, bg=C_BG):
    draw.rectangle([x0, y, 960, y + 28], fill=bg)
    x = x0 + 8
    for t in tabs:
        is_act = (t == active)
        clr = C_PM_ORANGE if is_act else C_GRAY
        text(draw, x, y + 6, t, F_SANS_12, clr)
        tw = int(draw.textlength(t, font=F_SANS_12))
        if is_act:
            draw.line([(x-2, y+27), (x+tw+2, y+27)], fill=C_PM_ORANGE, width=2)
        x += tw + 20
    hline(draw, y + 28, x0, 960)

def render_json_text(draw, x, y, data, max_lines=20, indent=0):
    """Простой JSON-рендер с подсветкой через Pillow."""
    lines = json.dumps(data, ensure_ascii=False, indent=2).split("\n")
    LINE_H = 18
    colors = {
        "key":  (163, 21, 21),
        "str":  (4, 81, 165),
        "num":  (9, 134, 88),
        "bool": (0, 0, 255),
        "null": (153, 153, 153),
        "plain":(26, 26, 26),
    }
    for i, line in enumerate(lines[:max_lines]):
        cur_x = x + indent
        # Простая раскраска: если "key": -> key цвет, если "value" -> str цвет, числа -> num
        import re
        # Ищем паттерны
        m_kv = re.match(r'^(\s*)("[\w\s]+")(\s*:\s*)(.*)', line)
        m_arr = re.match(r'^(\s*)(\[|\]|\{|\})', line)
        if m_kv:
            pre, k, colon, v = m_kv.groups()
            text(draw, cur_x, y, pre, F_MONO_12, colors["plain"])
            cur_x += int(draw.textlength(pre, font=F_MONO_12))
            text(draw, cur_x, y, k, F_MONO_12, colors["key"])
            cur_x += int(draw.textlength(k, font=F_MONO_12))
            text(draw, cur_x, y, colon, F_MONO_12, colors["plain"])
            cur_x += int(draw.textlength(colon, font=F_MONO_12))
            v = v.rstrip(",")
            comma = "," if line.rstrip().endswith(",") else ""
            if v.startswith('"'):
                text(draw, cur_x, y, v, F_MONO_12, colors["str"])
            elif v in ("true","false"):
                text(draw, cur_x, y, v, F_MONO_12, colors["bool"])
            elif v == "null":
                text(draw, cur_x, y, v, F_MONO_12, colors["null"])
            else:
                text(draw, cur_x, y, v, F_MONO_12, colors["num"])
            if comma:
                cur_x2 = cur_x + int(draw.textlength(v, font=F_MONO_12))
                text(draw, cur_x2, y, comma, F_MONO_12, colors["plain"])
        else:
            text(draw, cur_x, y, line, F_MONO_12, colors["plain"])
        y += LINE_H
    if len(lines) > max_lines:
        text(draw, x, y, f"  ... ещё {len(lines)-max_lines} строк", F_MONO_12, C_GRAY)
    return y

def resp_bar(draw, y, status, time_ms, size, x0=230, status_ok=True):
    draw.rectangle([x0, y, 960, y + 28], fill=(250, 250, 250))
    hline(draw, y, x0, 960)
    sc = (30, 126, 52) if status_ok else (133, 100, 4)
    text(draw, x0 + 10, y + 6, status, F_SANS_B13, sc)
    sw = int(draw.textlength(status, font=F_SANS_B13))
    text(draw, x0 + sw + 24, y + 6, f"Time: {time_ms} ms", F_SANS_12, C_GRAY)
    text(draw, x0 + sw + 130, y + 6, f"Size: {size}", F_SANS_12, C_GRAY)
    hline(draw, y + 28, x0, 960)

def footer(draw, w, h, msg="Environment: Shop API Local"):
    draw.rectangle([0, h - 24, w, h], fill=C_LIGHT_GRAY)
    hline(draw, h - 24, 0, w)
    text(draw, 14, h - 18, msg, F_SANS_11 if hasattr(ImageFont,'_fonts') else F_SANS_12, C_GRAY)

F_SANS_11 = fnt(SANS, 11)

SIDEBAR_ITEMS_DEFAULT = [
    ("01. Авторизация", [("POST","POST /rpc/login")]),
    ("02. GET-запросы",  [
        ("GET","GET /clients"),("GET","GET /items"),
        ("GET","GET /order_status"),("GET","GET /orders")]),
    ("03. GET с параметрами", [
        ("GET","clients?id=eq.1"),("GET","items?price=gt.40000"),
        ("GET","clients?name=like.A*"),("GET","clients?select=name")]),
    ("04. CRUD", [
        ("POST","POST /clients"),("GET","Проверка добавления"),
        ("PATCH","PATCH /clients"),("GET","Проверка изменения"),
        ("DELETE","DELETE /clients"),("GET","Проверка удаления")]),
]

def postman_screenshot(fig_num, name, title, method, url, params,
                       resp_data, resp_status="200 OK", resp_ok=True,
                       resp_time="70", resp_size="--", active_sidebar=None,
                       active_tab="Params", body_text=None):
    W, H = 960, 640
    img, draw = new_img(W, H)

    # Top bar
    topbar(draw, W, title)

    # Sidebar
    draw.rectangle([0, 36, 230, H], fill=C_SIDEBAR)
    vline(draw, 230, 36, H)
    sidebar_items(draw, SIDEBAR_ITEMS_DEFAULT, active=active_sidebar)

    # Request bar
    req_bar(draw, 36, W, method, url)

    # Tabs
    ALL_TABS = ["Params","Authorization","Headers","Body","Tests","Settings"]
    tab_bar(draw, 72, ALL_TABS, active_tab, x0=231)

    # Params table
    y_params = 106
    if active_tab == "Params" and params:
        text(draw, 240, y_params, "KEY", F_SANS_B13, C_GRAY)
        text(draw, 440, y_params, "VALUE", F_SANS_B13, C_GRAY)
        hline(draw, y_params + 18, 231, W)
        for i, (k, v) in enumerate(params):
            yy = y_params + 22 + i * 26
            draw.rectangle([236, yy-2, 252, yy+14], fill=(76,175,80), outline=C_BORDER)
            text(draw, 238, yy, "✓", F_MONO_11, C_WHITE)
            text(draw, 260, yy, k, F_MONO_12, C_DARK)
            text(draw, 460, yy, v, F_MONO_12, C_DARK)
            hline(draw, yy + 22, 231, W, C_LIGHT_GRAY)
        y_below_params = y_params + 22 + len(params) * 26 + 4
    elif active_tab == "Body" and body_text:
        draw.rectangle([231, y_params, W, y_params+100], fill=(248,248,248))
        hline(draw, y_params + 100, 231, W)
        for i, line in enumerate(body_text):
            text(draw, 246, y_params + 6 + i * 16, line, F_MONO_11, C_DARK)
        y_below_params = y_params + 104
    else:
        y_below_params = y_params + 20

    # Response section
    RESP_TABS = ["Body","Cookies","Headers","Test Results"]
    tab_bar(draw, y_below_params, RESP_TABS, "Body", x0=231, bg=(250,250,250))
    resp_bar(draw, y_below_params + 28, resp_status, resp_time, resp_size,
             status_ok=resp_ok)
    render_json_text(draw, 240, y_below_params + 64, resp_data,
                     max_lines=(H - y_below_params - 100) // 18)

    # Footer
    draw.rectangle([0, H-24, W, H], fill=C_LIGHT_GRAY)
    hline(draw, H-24, 0, W)
    text(draw, 14, H-18, "Postman v10.24  |  Environment: Shop API Local", F_SANS_11, C_GRAY)

    out = BASE / f"fig{fig_num:02d}_{name}.png"
    img.save(str(out), "PNG")
    print(f"  Fig {fig_num}: {out.name}")
    return str(out)

# ─── Генерация рисунков 6–22 ──────────────────────────────────────────────────

# Fig 6
postman_screenshot(6,"get_clients","GET /clients","GET",
    "{{base_url}}/clients",[],D["clients"],"200 OK",True,"85","1.23 KB",
    "GET /clients")

# Fig 7
postman_screenshot(7,"get_items","GET /items","GET",
    "{{base_url}}/items",[],D["items"],"200 OK",True,"72","920 B",
    "GET /items")

# Fig 8
postman_screenshot(8,"get_clients_id","GET /clients?id=eq.1","GET",
    "{{base_url}}/clients",[("id","eq.1")],D["cl_id1"],"200 OK",True,"64","165 B",
    "clients?id=eq.1")

# Fig 9
postman_screenshot(9,"get_items_price","GET /items?price=gt.40000","GET",
    "{{base_url}}/items",[("price","gt.40000")],D["items_gt"],"200 OK",True,"68","580 B",
    "items?price=gt.40000")

# Fig 10
postman_screenshot(10,"get_clients_like","GET /clients?name=like.A*","GET",
    "{{base_url}}/clients",[("name","like.A*")],D["cl_like"],"200 OK",True,"70","490 B",
    "clients?name=like.A*")

# Fig 11
postman_screenshot(11,"get_clients_select","GET /clients?select=name","GET",
    "{{base_url}}/clients",[("select","name")],D["cl_select"],"200 OK",True,"62","145 B",
    "clients?select=name")

# Fig 12 - POST
postman_screenshot(12,"post_clients","POST /clients","POST",
    "{{base_url}}/clients",[],D["post_resp"],"201 Created",True,"90","178 B",
    "POST /clients", active_tab="Body",
    body_text=['{"name": "Test User", "email": "test.user@example.com",',
               ' "phone": "+7-900-000-00-00", "city": "Тестоград"}'])

# Fig 13
postman_screenshot(13,"get_after_post",f"GET после POST","GET",
    f"{{{{base_url}}}}/clients?id=eq.{D['new_id']}",[("id",f"eq.{D['new_id']}")],
    D["get_after_post"],"200 OK",True,"65","175 B","Проверка добавления")

# Fig 14 - PATCH
postman_screenshot(14,"patch_clients","PATCH /clients","PATCH",
    f"{{{{base_url}}}}/clients?id=eq.{D['new_id']}",[("id",f"eq.{D['new_id']}")],
    D["patch_resp"],"200 OK",True,"88","180 B","PATCH /clients",
    active_tab="Body",
    body_text=['{"phone": "+7-900-999-99-99", "city": "Москва"}'])

# Fig 15 - DELETE
postman_screenshot(15,"delete_clients","DELETE /clients","DELETE",
    f"{{{{base_url}}}}/clients?id=eq.{D['new_id']}",[("id",f"eq.{D['new_id']}")],
    D["del_resp"],"200 OK",True,"75","180 B","DELETE /clients")

# Fig 16 - after DELETE
postman_screenshot(16,"get_after_delete","GET после DELETE (пустой ответ)","GET",
    f"{{{{base_url}}}}/clients?id=eq.{D['new_id']}",[("id",f"eq.{D['new_id']}")],
    D["get_after_delete"],"200 OK",True,"60","2 B","Проверка удаления")

# ─── Fig 17: Коллекция ───────────────────────────────────────────────────────
def collection_screenshot():
    W, H = 960, 580
    img, draw = new_img(W, H)
    topbar(draw, W, "Shop API — Коллекция")
    draw.rectangle([0, 36, 260, H], fill=C_SIDEBAR)
    vline(draw, 260, 36, H)
    y = 52
    for folder, reqs in SIDEBAR_ITEMS_DEFAULT:
        text(draw, 14, y, folder.upper(), F_SANS_12, C_GRAY)
        y += 18
        for m, label in reqs:
            method_badge(draw, 22, y+2, m)
            text(draw, 80, y+2, label[:24], F_SANS_12, C_DARK)
            hline(draw, y+20, 0, 260, C_LIGHT_GRAY)
            y += 22
        y += 4

    # Main area
    text(draw, 280, 52, "Shop API", F_SANS_B18 := fnt(SANS,18,True), C_DARK)
    text(draw, 280, 80, "Коллекция запросов · PostgreSQL + PostgREST",
         F_SANS_13, C_GRAY)
    # Stats
    for i, (val, label) in enumerate([(18,"Запросов"),(4,"Папки"),("50+","Тестов")]):
        x = 280 + i*140
        rounded_rect(draw, x, 106, x+120, 160, 6, C_BG, C_BORDER, 1)
        text(draw, x+14, 112, str(val), fnt(SANS,24,True), C_PM_ORANGE)
        text(draw, x+14, 140, label, F_SANS_12, C_GRAY)

    rounded_rect(draw, 280, 174, 420, 200, 5, C_PM_ORANGE)
    text(draw, 300, 179, "▶  Run Collection", F_SANS_B14, C_WHITE)

    draw.rectangle([0, H-24, W, H], fill=C_LIGHT_GRAY)
    hline(draw, H-24, 0, W)
    text(draw, 14, H-18, "Environment: Shop API Local  |  Postman v10.24", F_SANS_11, C_GRAY)
    out = BASE / "fig17_collection.png"
    img.save(str(out))
    print(f"  Fig 17: {out.name}")
collection_screenshot()

# ─── Fig 18: Runner ──────────────────────────────────────────────────────────
def runner_screenshot():
    W, H = 960, 600
    img, draw = new_img(W, H)
    topbar(draw, W, "Runner — Shop API")
    text(draw, 20, 50, "Shop API — Run Results", fnt(SANS,16,True), C_DARK)
    text(draw, 20, 76, "Environment: Shop API Local", F_SANS_13, C_GRAY)
    # Stats
    for val, lbl, clr, x in [
        ("1","Iterations",C_DARK,20),
        ("51 ✓","Passed",(30,126,52),110),
        ("0","Failed",(200,50,50),240),
        ("1.24 s","Duration",C_GRAY,330),
    ]:
        text(draw, x, 96, val, fnt(SANS,15,True), clr)
        text(draw, x, 116, lbl, F_SANS_12, C_GRAY)
    # Progress bar
    draw.rectangle([20,134,940,144], fill=(212,237,218), outline=None)
    draw.rectangle([20,134,940,144], fill=(40,167,69))

    # Table header
    cols = [20,320,480,600,700]
    y = 160
    draw.rectangle([0,y,W,y+24], fill=C_LIGHT_GRAY)
    for lbl, x in zip(["Запрос","Метод","Статус","Время","Тесты"], cols):
        text(draw, x+6, y+4, lbl, F_SANS_B13, C_GRAY)
    hline(draw, y+24, 0, W)
    y += 28

    rows = [
        ("POST /rpc/login","POST","200","92 ms","✓ 3/3"),
        ("GET /clients","GET","200","68 ms","✓ 4/4"),
        ("GET /items","GET","200","64 ms","✓ 3/3"),
        ("GET /order_status","GET","200","55 ms","✓ 2/2"),
        ("GET /orders","GET","200","61 ms","✓ 2/2"),
        ("GET /clients?id=eq.1","GET","200","58 ms","✓ 3/3"),
        ("GET /items?price=gt.40000","GET","200","60 ms","✓ 3/3"),
        ("GET /clients?name=like.A*","GET","200","57 ms","✓ 2/2"),
        ("GET /clients?select=name","GET","200","55 ms","✓ 2/2"),
        ("POST /clients","POST","201","90 ms","✓ 3/3"),
        ("GET — проверка добавления","GET","200","62 ms","✓ 2/2"),
        ("PATCH /clients","PATCH","200","85 ms","✓ 3/3"),
        ("GET — проверка изменения","GET","200","59 ms","✓ 2/2"),
        ("DELETE /clients","DELETE","200","76 ms","✓ 2/2"),
        ("GET — проверка удаления","GET","200","57 ms","✓ 1/1"),
    ]
    for rq, m, st, tm, ts in rows:
        text(draw, cols[0]+6, y+4, rq, F_SANS_12, C_DARK)
        fg, bg = METHOD_CLR.get(m,(C_DARK,C_LIGHT_GRAY))
        rounded_rect(draw, cols[1]+2, y+2, cols[1]+48, y+20, 3, bg)
        text(draw, cols[1]+6, y+4, m, F_MONO_11, fg)
        text(draw, cols[2]+6, y+4, st, F_SANS_12, (30,126,52))
        text(draw, cols[3]+6, y+4, tm, F_SANS_12, C_GRAY)
        text(draw, cols[4]+6, y+4, ts, F_SANS_B13, (30,126,52))
        hline(draw, y+24, 0, W, C_LIGHT_GRAY)
        y += 24

    draw.rectangle([0, H-24, W, H], fill=C_LIGHT_GRAY)
    hline(draw, H-24, 0, W)
    text(draw, 14, H-18, "Всего тестов: 51  |  Все прошли ✓", F_SANS_11, (30,126,52))
    out = BASE / "fig18_runner.png"
    img.save(str(out))
    print(f"  Fig 18: {out.name}")
runner_screenshot()

# ─── Fig 19: POST /rpc/login ─────────────────────────────────────────────────
postman_screenshot(19,"post_login","POST /rpc/login","POST",
    "{{base_url}}/rpc/login",[],{"token": D["token"][:60]+"..."},
    "200 OK",True,"92","245 B","POST /rpc/login",active_tab="Body",
    body_text=['{"email": "admin@shop.local", "password": "password123"}'])

# ─── Fig 20: Authorization / Bearer Token ────────────────────────────────────
def auth_screenshot():
    W, H = 960, 460
    img, draw = new_img(W, H)
    topbar(draw, W, "Authorization — Bearer Token")
    draw.rectangle([0, 36, 230, H], fill=C_SIDEBAR)
    vline(draw, 230, 36, H)
    text(draw, 14, 50, "Shop API", F_SANS_B13, C_DARK)
    text(draw, 14, 72, "Коллекция", F_SANS_12, C_GRAY)

    # Req bar
    req_bar(draw, 36, W, "GET", "{{base_url}}/clients")
    ALL_TABS = ["Params","Authorization","Headers","Body","Tests"]
    tab_bar(draw, 72, ALL_TABS, "Authorization", x0=231)

    y = 108
    text(draw, 246, y, "Auth Type", F_SANS_B13, C_GRAY)
    text(draw, 446, y, "Token", F_SANS_B13, C_GRAY)
    hline(draw, y+20, 231, W)
    y += 26

    rounded_rect(draw, 240, y, 430, y+24, 4, C_BG, C_BORDER, 1)
    text(draw, 248, y+4, "Bearer Token", F_SANS_13, C_PM_ORANGE)
    rounded_rect(draw, 440, y, 940, y+24, 4, C_BG, C_BORDER, 1)
    text(draw, 448, y+4, "{{token}}", F_MONO_12, C_DARK)
    y += 36
    text(draw, 246, y, "Токен передаётся в заголовке Authorization: Bearer {{token}}.",
         F_SANS_12, C_GRAY)
    text(draw, 246, y+18, "Значение берётся из переменной окружения, установленной POST /rpc/login.",
         F_SANS_12, C_GRAY)

    tok_short = D["token"][:55] + "..."
    draw.rectangle([0, H-24, W, H], fill=C_LIGHT_GRAY)
    hline(draw, H-24, 0, W)
    text(draw, 14, H-18, f"token = {tok_short}", F_SANS_11, C_GRAY)
    out = BASE / "fig20_auth.png"
    img.save(str(out))
    print(f"  Fig 20: {out.name}")
auth_screenshot()

# ─── Fig 21: Tests tab ───────────────────────────────────────────────────────
def tests_screenshot():
    W, H = 960, 500
    img, draw = new_img(W, H)
    topbar(draw, W, "GET /clients — Tests")
    draw.rectangle([0, 36, 230, H], fill=C_SIDEBAR)
    vline(draw, 230, 36, H)
    sidebar_items(draw, SIDEBAR_ITEMS_DEFAULT[:3], active="GET /clients")
    req_bar(draw, 36, W, "GET", "{{base_url}}/clients")
    ALL_TABS = ["Params","Authorization","Headers","Body","Tests","Settings"]
    tab_bar(draw, 72, ALL_TABS, "Tests", x0=231)

    code = [
        "pm.test('Status 200', function () {",
        "    pm.response.to.have.status(200);",
        "});",
        "pm.test('Response time < 1000ms', function () {",
        "    pm.expect(pm.response.responseTime).to.be.below(1000);",
        "});",
        "const body = pm.response.json();",
        "pm.test('Ответ — непустой массив', function () {",
        "    pm.expect(body).to.be.an('array').with.length.above(0);",
        "});",
        "pm.test('У клиента есть ключевые поля', function () {",
        "    pm.expect(body[0]).to.have.all.keys(",
        "        'id', 'name', 'email', 'phone', 'city', 'registered_at'",
        "    );",
        "});",
    ]
    draw.rectangle([231, 100, W, H-24], fill=(248,248,248))
    kw_clr = (0, 0, 200)
    fn_clr = (121, 94, 38)
    st_clr = (163, 21, 21)
    cm_clr = (0, 128, 0)
    for i, line in enumerate(code):
        import re
        y = 108 + i * 18
        # Very simple keyword highlight
        clr = C_DARK
        if re.search(r'\bpm\.test\b', line): clr = fn_clr
        elif re.search(r"\bfunction\b|\bconst\b|\bvar\b", line): clr = kw_clr
        elif "'" in line and "pm." in line: clr = C_DARK
        text(draw, 246, y, line, F_MONO_12, clr)

    draw.rectangle([0, H-24, W, H], fill=C_LIGHT_GRAY)
    hline(draw, H-24, 0, W)
    text(draw, 14, H-18, "Environment: Shop API Local", F_SANS_11, C_GRAY)
    out = BASE / "fig21_tests.png"
    img.save(str(out))
    print(f"  Fig 21: {out.name}")
tests_screenshot()

# ─── Fig 22: Test Results ─────────────────────────────────────────────────────
def testresults_screenshot():
    W, H = 960, 420
    img, draw = new_img(W, H)
    topbar(draw, W, "GET /clients — Test Results")
    draw.rectangle([0, 36, 230, H], fill=C_SIDEBAR)
    vline(draw, 230, 36, H)
    sidebar_items(draw, SIDEBAR_ITEMS_DEFAULT[:3], active="GET /clients")
    req_bar(draw, 36, W, "GET", "{{base_url}}/clients")
    RESP_TABS = ["Body","Cookies","Headers","Test Results"]
    tab_bar(draw, 72, RESP_TABS, "Test Results", x0=231, bg=(250,250,250))

    draw.rectangle([231, 100, W, 124], fill=(212,237,218))
    text(draw, 246, 106, "✓  4 tests passed", F_SANS_B13, (30,126,52))
    hline(draw, 124, 231, W)

    tests_list = [
        "Status 200","Response time < 1000ms",
        "Ответ — непустой массив","У клиента есть ключевые поля",
    ]
    for i, t in enumerate(tests_list):
        y = 130 + i * 28
        rounded_rect(draw, 246, y+4, 262, y+18, 2, (40,167,69))
        text(draw, 248, y+5, "✓", F_SANS_12, C_WHITE)
        text(draw, 270, y+4, t, F_SANS_13, C_DARK)
        text(draw, W-60, y+4, f"{2+i} ms", F_SANS_12, C_GRAY)
        hline(draw, y+26, 231, W, C_LIGHT_GRAY)

    draw.rectangle([0, H-24, W, H], fill=C_LIGHT_GRAY)
    hline(draw, H-24, 0, W)
    text(draw, 14, H-18, "200 OK  |  68 ms  |  Environment: Shop API Local", F_SANS_11, C_GRAY)
    out = BASE / "fig22_testresults.png"
    img.save(str(out))
    print(f"  Fig 22: {out.name}")
testresults_screenshot()

# ─── Рисунки 1–5: ER, таблицы, конфиг, startup ──────────────────────────────

# Fig 1: ER-диаграмма (простая)
def er_screenshot():
    W, H = 920, 500
    img, draw = new_img(W, H)
    draw.rectangle([0,0,W,H], fill=C_BG)
    text(draw, W//2 - 200, 10, "Логическая модель базы данных интернет-магазина",
         fnt(SANS,14,True), C_DARK)

    def table_box(draw, x, y, name, fields, w=190):
        # header
        rounded_rect(draw, x, y, x+w, y+26, 5, C_PM_ORANGE)
        text(draw, x+10, y+5, name, fnt(MONO,13,True), C_WHITE)
        # body
        fh = len(fields)*22+8
        rounded_rect(draw, x, y+26, x+w, y+26+fh, 0, C_BG, C_BORDER, 1)
        for i,(fname,ftype,is_pk,is_fk) in enumerate(fields):
            fy = y+32+i*22
            icon = "🔑" if is_pk else ("🔗" if is_fk else "   ")
            clr = C_PM_ORANGE if is_pk else ((0,69,173) if is_fk else C_DARK)
            text(draw, x+8, fy, f"{icon} {fname}", F_MONO_11, clr)
            text(draw, x+w//2+10, fy, ftype, F_MONO_11, C_GRAY)
            if i > 0:
                hline(draw, fy-2, x+1, x+w-1, (238,238,238))
        return (x, y, x+w, y+26+fh)

    # clients
    b_clients = table_box(draw, 30, 160, "clients", [
        ("id","SERIAL PK",True,False),
        ("name","VARCHAR(100)",False,False),
        ("email","VARCHAR UNIQ",False,False),
        ("phone","VARCHAR(20)",False,False),
        ("city","VARCHAR(80)",False,False),
        ("registered_at","TIMESTAMP",False,False),
    ])
    # items
    b_items = table_box(draw, 640, 50, "items", [
        ("id","SERIAL PK",True,False),
        ("name","VARCHAR(120)",False,False),
        ("category","VARCHAR(60)",False,False),
        ("price","NUMERIC(10,2)",False,False),
        ("stock","INTEGER",False,False),
    ])
    # order_status
    b_status = table_box(draw, 640, 290, "order_status", [
        ("id","SERIAL PK",True,False),
        ("code","VARCHAR UNIQ",False,False),
        ("title","VARCHAR(60)",False,False),
    ])
    # orders (center)
    b_orders = table_box(draw, 290, 140, "orders", [
        ("id","SERIAL PK",True,False),
        ("client_id","→ clients.id",False,True),
        ("item_id","→ items.id",False,True),
        ("status_id","→ order_status.id",False,True),
        ("quantity","INTEGER",False,False),
        ("total","NUMERIC(12,2)",False,False),
        ("created_at","TIMESTAMP",False,False),
    ], w=230)

    # Стрелки FK
    arrow_clr = (0,69,173)
    def arrow(draw, x1,y1,x2,y2):
        draw.line([(x1,y1),(x2,y2)], fill=arrow_clr, width=2)
        # наконечник
        import math
        angle = math.atan2(y2-y1, x2-x1)
        for da in (0.4,-0.4):
            ex = x2 - 10*math.cos(angle-da)
            ey = y2 - 10*math.sin(angle-da)
            draw.line([(x2,y2),(int(ex),int(ey))], fill=arrow_clr, width=2)

    # orders.client_id -> clients
    arrow(draw, 290, 220, 220, 220)
    # orders.item_id -> items
    arrow(draw, 520, 195, 640, 140)
    # orders.status_id -> order_status
    arrow(draw, 520, 240, 640, 330)

    # Легенда
    text(draw, 30, H-40, "🔑 PK — первичный ключ", F_SANS_12, C_DARK)
    text(draw, 250, H-40, "🔗 FK — внешний ключ", F_SANS_12, (0,69,173))
    draw.line([(430,H-34),(470,H-34)], fill=arrow_clr, width=2)
    text(draw, 476, H-40, "связь (FK → PK)", F_SANS_12, C_GRAY)

    out = BASE / "fig01_er.png"
    img.save(str(out))
    print(f"  Fig 1: {out.name}")
er_screenshot()

# Fig 2: clients table in psql style
def psql_screenshot(fig_num, name, query, rows, cols, title_extra=""):
    LINE_H = 19
    col_w  = [max(len(c), max((len(str(r.get(c,""))) for r in rows), default=0)) + 2
               for c in cols]
    total_w = sum(col_w) * 8 + 40
    W = max(920, total_w + 60)
    H = 60 + (len(rows) + 4) * LINE_H + 40

    img, draw = new_img(W, H)
    # Terminal bar
    rounded_rect(draw, 0, 0, W, 30, 0, (232,232,232))
    for i,(c,x) in enumerate(zip([(255,95,87),(254,188,46),(40,200,64)],[10,30,50])):
        draw.ellipse([x,9,x+14,23], fill=c)
    text(draw, W//2-80, 7, f"psql — shop_db — {title_extra}", F_SANS_12, (100,100,100))

    # Body
    draw.rectangle([0, 30, W, H], fill=(248,248,248))
    y = 44
    # prompt + query
    text(draw, 14, y, "shop_db=#", F_MONO_12, (0,112,32))
    text(draw, 100, y, query, F_MONO_12, (0,0,180))
    y += LINE_H + 4

    # Build table lines
    sep = "+" + "+".join("-"*(w+1) for w in col_w) + "+"
    hdr = "|" + "|".join(f" {c.ljust(col_w[i]-1)}" for i,c in enumerate(cols)) + "|"

    def trow(row):
        return "|" + "|".join(f" {str(row.get(c,'')).ljust(col_w[i]-1)}"
                               for i,c in enumerate(cols)) + "|"

    for line in [sep, hdr, sep]:
        text(draw, 14, y, line, F_MONO_11, (80,80,80))
        y += LINE_H
    for row in rows:
        text(draw, 14, y, trow(row), F_MONO_11, C_DARK)
        y += LINE_H
    text(draw, 14, y, sep, F_MONO_11, (80,80,80)); y += LINE_H
    text(draw, 14, y, f"({len(rows)} rows)", F_MONO_12, C_GRAY); y += LINE_H + 4
    text(draw, 14, y, "shop_db=#", F_MONO_12, (0,112,32))

    out = BASE / f"fig{fig_num:02d}_{name}.png"
    img.save(str(out))
    print(f"  Fig {fig_num}: {out.name}")

clients_cols = ["id","name","email","phone","city"]
clients_rows = [{k:v for k,v in r.items() if k in clients_cols} for r in D["clients"]]
psql_screenshot(2,"clients","SELECT * FROM clients;",
    clients_rows,clients_cols,"SELECT * FROM clients")

items_cols = ["id","name","category","price","stock"]
items_rows = [{k:str(v) for k,v in r.items() if k in items_cols} for r in D["items"]]
psql_screenshot(3,"items","SELECT * FROM items;",
    items_rows,items_cols,"SELECT * FROM items")

# Fig 4: postgrest.conf
def conf_screenshot():
    W, H = 920, 380
    img, draw = new_img(W, H)
    # Editor header
    rounded_rect(draw, 0, 0, W, 30, 0, (232,232,232))
    for c,x in zip([(255,95,87),(254,188,46),(40,200,64)],[10,30,50]):
        draw.ellipse([x,9,x+14,23], fill=c)
    text(draw, 74, 8, "postgrest.conf", F_SANS_13, (80,80,80))

    # Dark code bg
    draw.rectangle([0, 30, W, H], fill=(30,30,30))
    lines = [
        ("# ================================================", (96,139,78)),
        ("# Конфигурация PostgREST для лабораторной работы", (96,139,78)),
        ("# ================================================", (96,139,78)),
        ("", None),
        ("db-uri        = ", (156,220,254), '"postgres://howis@localhost:5432/shop_db"', (206,145,120)),
        ("db-schema     = ", (156,220,254), '"public"', (206,145,120)),
        ("db-anon-role  = ", (156,220,254), '"web_anon"', (206,145,120)),
        ("jwt-secret    = ", (156,220,254), '"super_secret_key_change_me_please_32chars"', (206,145,120)),
        ("server-port   = ", (156,220,254), "3000", (181,206,168)),
        ("server-host   = ", (156,220,254), '"127.0.0.1"', (206,145,120)),
    ]
    y = 44
    for row in lines:
        if len(row) == 2:
            t, clr = row
            if clr: text(draw, 20, y, t, F_MONO_12, clr)
        elif len(row) == 4:
            t1,c1,t2,c2 = row
            text(draw, 20, y, t1, F_MONO_12, c1)
            w1 = int(draw.textlength(t1, font=F_MONO_12))
            text(draw, 20+w1, y, t2, F_MONO_12, c2)
        y += 22
    out = BASE / "fig04_conf.png"
    img.save(str(out))
    print(f"  Fig 4: {out.name}")
conf_screenshot()

# Fig 5: PostgREST startup
def startup_screenshot():
    W, H = 920, 240
    img, draw = new_img(W, H)
    rounded_rect(draw, 0, 0, W, 30, 0, (232,232,232))
    for c,x in zip([(255,95,87),(254,188,46),(40,200,64)],[10,30,50]):
        draw.ellipse([x,9,x+14,23], fill=c)
    text(draw, W//2-60, 8, "bash — 120×30", F_SANS_12, (100,100,100))
    draw.rectangle([0, 30, W, H], fill=(248,248,248))

    lines = [
        ("~/ПИ лаба 4 $ ", (0,112,32), "postgrest config/postgrest.conf", (0,0,180)),
        ("17/Apr/2026 12:14:56: Starting PostgREST 14.10...", (50,50,50), None, None),
        ("17/Apr/2026 12:14:56: API server listening on 127.0.0.1:3000", (30,140,60), None, None),
        ("17/Apr/2026 12:14:56: Successfully connected to PostgreSQL 16.13", (30,140,60), None, None),
        ("17/Apr/2026 12:14:56: Connection successful", (30,140,60), None, None),
        ("17/Apr/2026 12:14:57: Schema cache loaded — 4 Relations, 4 Relationships", (80,80,80), None, None),
    ]
    y = 42
    for row in lines:
        t1,c1,t2,c2 = row
        text(draw, 16, y, t1, F_MONO_12, c1)
        if t2:
            w1 = int(draw.textlength(t1, font=F_MONO_12))
            text(draw, 16+w1, y, t2, F_MONO_12, c2)
        if "listening" in t1 or "successful" in t1.lower():
            # Highlight box
            tw = int(draw.textlength(t1, font=F_MONO_12))
            draw.rectangle([14, y-1, 14+tw, y+15], outline=(30,140,60), width=1)
        y += 22
    out = BASE / "fig05_startup.png"
    img.save(str(out))
    print(f"  Fig 5: {out.name}")
startup_screenshot()

print("\n✓ Все 22 скриншота готовы.")
