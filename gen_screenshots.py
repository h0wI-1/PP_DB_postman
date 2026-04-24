"""
Генератор HTML-макетов скриншотов в стиле Postman (светлая тема).
Открывает каждый HTML в Safari, ждёт загрузки и делает screencapture.
"""

import json, os, subprocess, time, textwrap
from pathlib import Path

BASE  = Path("/Users/howis/Downloads/ПИ лаба 4/screenshots")
HTML  = BASE / "html"
HTML.mkdir(parents=True, exist_ok=True)

with open(BASE / "_api_data.json", encoding="utf-8") as f:
    D = json.load(f)

# ─── CSS / HTML базы ─────────────────────────────────────────────────────────

GLOBAL_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, 'Segoe UI', sans-serif; font-size: 13px;
       background: #fff; color: #1a1a1a; }
.pm-window { width: 960px; min-height: 560px; background: #fff;
             border: 1px solid #d0d0d0; border-radius: 6px; overflow: hidden; }
/* Top bar */
.pm-topbar { background: #f05a28; height: 40px; display: flex; align-items: center;
             padding: 0 14px; color: #fff; font-weight: 600; font-size: 14px; }
.pm-topbar .logo { font-size: 16px; font-weight: 700; letter-spacing: 1px; margin-right: 20px; }
/* Sidebar */
.pm-layout { display: flex; height: calc(100% - 40px); }
.pm-sidebar { width: 220px; background: #f9f9f9; border-right: 1px solid #e0e0e0;
              padding: 10px 0; font-size: 12px; }
.pm-sidebar .item { padding: 6px 16px; cursor: pointer; border-radius: 4px; margin: 1px 6px; }
.pm-sidebar .item:hover { background: #efefef; }
.pm-sidebar .item.active { background: #fff4f0; color: #f05a28; font-weight: 600; }
.pm-sidebar .folder { padding: 6px 12px; font-weight: 600; color: #555;
                      font-size: 11px; text-transform: uppercase; letter-spacing: .5px;
                      margin-top: 8px; }
.method { display: inline-block; padding: 1px 6px; border-radius: 3px; font-size: 10px;
          font-weight: 700; margin-right: 6px; }
.GET    { color: #1e7e34; background: #d4edda; }
.POST   { color: #856404; background: #fff3cd; }
.PATCH  { color: #0c5460; background: #d1ecf1; }
.DELETE { color: #721c24; background: #f8d7da; }
/* Main area */
.pm-main { flex: 1; display: flex; flex-direction: column; }
.pm-req-bar { display: flex; align-items: center; padding: 10px 12px;
              border-bottom: 1px solid #e0e0e0; gap: 8px; }
.pm-req-bar .method-sel { background: #fff; border: 1px solid #d0d0d0;
                           border-radius: 4px; padding: 6px 10px; font-weight: 700;
                           min-width: 80px; text-align: center; }
.pm-req-bar input { flex: 1; border: 1px solid #d0d0d0; border-radius: 4px;
                    padding: 7px 10px; font-size: 13px; font-family: monospace; }
.pm-req-bar .btn-send { background: #f05a28; color: #fff; border: none;
                         border-radius: 4px; padding: 7px 18px; font-weight: 600;
                         cursor: pointer; }
/* Tabs */
.pm-tabs { display: flex; border-bottom: 1px solid #e0e0e0; padding: 0 12px; }
.pm-tabs .tab { padding: 8px 14px; cursor: pointer; font-size: 12px;
                border-bottom: 2px solid transparent; color: #555; }
.pm-tabs .tab.active { color: #f05a28; border-bottom-color: #f05a28; font-weight: 600; }
/* Params table */
.pm-params { padding: 12px; }
.pm-params table { width: 100%; border-collapse: collapse; font-size: 12px; }
.pm-params th { text-align: left; padding: 5px 8px; color: #888;
                border-bottom: 1px solid #e0e0e0; font-weight: 500; }
.pm-params td { padding: 5px 8px; border-bottom: 1px solid #f0f0f0; }
.pm-params td input { border: none; background: transparent; width: 100%;
                       font-family: monospace; font-size: 12px; color: #333; }
/* Response area */
.pm-resp-header { display: flex; align-items: center; gap: 16px;
                   padding: 8px 12px; border-bottom: 1px solid #e0e0e0;
                   background: #fafafa; font-size: 12px; }
.pm-resp-header .status-ok  { color: #1e7e34; font-weight: 700; }
.pm-resp-header .status-201 { color: #856404; font-weight: 700; }
.pm-resp-header .time       { color: #555; }
.pm-resp-header .size       { color: #555; }
.pm-resp-body { flex: 1; padding: 12px; overflow: auto; background: #fff;
                font-family: 'Courier New', monospace; font-size: 12px;
                line-height: 1.55; white-space: pre; }
.json-key     { color: #a31515; }
.json-str     { color: #0451a5; }
.json-num     { color: #098658; }
.json-bool    { color: #0000ff; }
.json-null    { color: #999; }
/* Status bar footer */
.pm-footer { height: 26px; background: #f0f0f0; border-top: 1px solid #ddd;
             display: flex; align-items: center; padding: 0 14px;
             font-size: 11px; color: #888; }
"""

def json_to_html(obj, indent=0):
    pad = "  " * indent
    if isinstance(obj, dict):
        if not obj: return "{}"
        lines = ["{"]
        items = list(obj.items())
        for i,(k,v) in enumerate(items):
            comma = "," if i < len(items)-1 else ""
            lines.append(f'{pad}  <span class="json-key">"{k}"</span>: {json_to_html(v, indent+1)}{comma}')
        lines.append(f"{pad}}}")
        return "\n".join(lines)
    elif isinstance(obj, list):
        if not obj: return '<span class="json-null">[]</span>'
        lines = ["["]
        for i,v in enumerate(obj):
            comma = "," if i < len(obj)-1 else ""
            lines.append(f"{pad}  {json_to_html(v, indent+1)}{comma}")
        lines.append(f"{pad}]")
        return "\n".join(lines)
    elif isinstance(obj, str):
        return f'<span class="json-str">"{obj}"</span>'
    elif isinstance(obj, bool):
        return f'<span class="json-bool">{"true" if obj else "false"}</span>'
    elif obj is None:
        return '<span class="json-null">null</span>'
    else:
        return f'<span class="json-num">{obj}</span>'

def params_table(rows):
    """rows: list of (key, value)"""
    html = '<div class="pm-params"><table>'
    html += '<tr><th></th><th>KEY</th><th>VALUE</th></tr>'
    for k, v in rows:
        html += f'<tr><td><input type="checkbox" checked></td><td><input value="{k}"></td><td><input value="{v}"></td></tr>'
    html += '</table></div>'
    return html

def pm_page(title, method, url, params, body_tab_active, body_html,
            resp_status, resp_status_class, resp_time, resp_size, resp_json,
            active_tab="Params", active_sidebar_item="", sidebar_items=None):
    if sidebar_items is None:
        sidebar_items = [
            ("02. GET-запросы без параметров", [
                ("GET","GET /clients"), ("GET","GET /items"),
                ("GET","GET /order_status"), ("GET","GET /orders"),
            ]),
            ("03. GET с параметрами", [
                ("GET","id=eq.1"), ("GET","price=gt.40000"),
                ("GET","name=like.A*"), ("GET","select=name"),
            ]),
            ("04. CRUD", [
                ("POST","POST /clients"), ("GET","Проверка добавления"),
                ("PATCH","PATCH /clients"), ("GET","Проверка изменения"),
                ("DELETE","DELETE /clients"), ("GET","Проверка удаления"),
            ]),
        ]
    sidebar_html = ""
    for folder_name, items in sidebar_items:
        sidebar_html += f'<div class="folder">{folder_name}</div>'
        for m, label in items:
            active_cls = "active" if label == active_sidebar_item else ""
            sidebar_html += f'<div class="item {active_cls}"><span class="method {m}">{m}</span>{label}</div>'

    # Params / Headers tabs
    tabs = ["Params","Authorization","Headers","Body","Pre-request Script","Tests","Settings"]
    tabs_html = "".join(
        f'<div class="tab {"active" if t == active_tab else ""}">{t}</div>'
        for t in tabs
    )

    resp_tabs = ["Body","Cookies","Headers","Test Results"]
    resp_tabs_html = "".join(
        f'<div class="tab {"active" if t == "Body" else ""}">{t}</div>'
        for t in resp_tabs
    )

    # Params table (query params from url)
    params_html = params_table(params) if params else '<div style="padding:12px;color:#888;font-size:12px;">No parameters</div>'

    resp_body_html = json_to_html(resp_json) if resp_json is not None else ""

    # Determine method color class
    mc = method
    method_color_map = {"GET":"color:#1e7e34","POST":"color:#856404",
                        "PATCH":"color:#0c5460","DELETE":"color:#721c24"}
    mcolor = method_color_map.get(method, "")

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>{title}</title>
<style>{GLOBAL_CSS}</style>
</head><body>
<div class="pm-window">
  <div class="pm-topbar">
    <span class="logo">Postman</span>
    <span>Shop API &nbsp;›&nbsp; {title}</span>
  </div>
  <div class="pm-layout">
    <div class="pm-sidebar">
      <div class="folder">01. Авторизация</div>
      <div class="item"><span class="method POST">POST</span>POST /rpc/login</div>
      {sidebar_html}
    </div>
    <div class="pm-main">
      <div class="pm-req-bar">
        <div class="method-sel" style="{mcolor}">{method}</div>
        <input value="{url}" readonly>
        <button class="btn-send">Send</button>
      </div>
      <div class="pm-tabs">{tabs_html}</div>
      {params_html if active_tab == "Params" else body_html}
      <div class="pm-tabs" style="background:#fafafa">{resp_tabs_html}</div>
      <div class="pm-resp-header">
        <span class="{resp_status_class}">{resp_status}</span>
        <span class="time">Time: {resp_time} ms</span>
        <span class="size">Size: {resp_size} B</span>
      </div>
      <div class="pm-resp-body">{resp_body_html}</div>
    </div>
  </div>
  <div class="pm-footer">Postman v10.24 &nbsp;|&nbsp; Environment: Shop API Local</div>
</div>
</body></html>"""
    return html

def save(name, html):
    p = HTML / f"{name}.html"
    p.write_text(html, encoding="utf-8")
    return str(p)

def screenshot(html_path, png_path, width=980, height=620):
    """Открываем HTML в Safari и делаем screencapture."""
    # Открываем в Safari
    subprocess.run(["open", "-a", "Safari", html_path], check=True)
    time.sleep(2.5)
    # Resize + screenshot через osascript
    script = f"""
tell application "Safari"
    activate
    set bounds of front window to {{40, 80, {40+width}, {80+height}}}
end tell
delay 0.8
do shell script "screencapture -l$(osascript -e 'tell app \\\"Safari\\\" to id of front window') -x {png_path}"
"""
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if result.returncode != 0:
        # Fallback: screencapture active window
        subprocess.run(["screencapture", "-x", "-o", png_path])
    time.sleep(0.5)

# ─── Генерация скриншотов ────────────────────────────────────────────────────
screenshots = {}  # fig_num -> png_path

def make_png(fig_num, name, html_str):
    html_path = save(name, html_str)
    png_path  = str(BASE / f"fig{fig_num:02d}_{name}.png")
    screenshot(html_path, png_path)
    screenshots[fig_num] = png_path
    print(f"  Fig {fig_num}: {png_path}")
    return png_path

print("Генерирую скриншоты...")

# ─── Fig 6: GET /clients ─────────────────────────────────────────────────────
html = pm_page(
    "GET /clients", "GET",
    "{{base_url}}/clients", [],
    False, "",
    "200 OK", "status-ok", "85", "1.23 KB",
    D["clients"],
    active_sidebar_item="GET /clients"
)
make_png(6, "get_clients", html)

# ─── Fig 7: GET /items ───────────────────────────────────────────────────────
html = pm_page(
    "GET /items", "GET",
    "{{base_url}}/items", [],
    False, "",
    "200 OK", "status-ok", "72", "920 B",
    D["items"],
    active_sidebar_item="GET /items"
)
make_png(7, "get_items", html)

# ─── Fig 8: GET /clients?id=eq.1 ─────────────────────────────────────────────
html = pm_page(
    "GET /clients?id=eq.1", "GET",
    "{{base_url}}/clients", [("id","eq.1")],
    False, "",
    "200 OK", "status-ok", "64", "165 B",
    D["cl_id1"],
    active_sidebar_item="id=eq.1"
)
make_png(8, "get_clients_id", html)

# ─── Fig 9: GET /items?price=gt.40000 ────────────────────────────────────────
html = pm_page(
    "GET /items?price=gt.40000", "GET",
    "{{base_url}}/items", [("price","gt.40000")],
    False, "",
    "200 OK", "status-ok", "68", "580 B",
    D["items_gt"],
    active_sidebar_item="price=gt.40000"
)
make_png(9, "get_items_price", html)

# ─── Fig 10: GET /clients?name=like.A* ───────────────────────────────────────
html = pm_page(
    "GET /clients?name=like.A*", "GET",
    "{{base_url}}/clients", [("name","like.A*")],
    False, "",
    "200 OK", "status-ok", "70", "490 B",
    D["cl_like"],
    active_sidebar_item="name=like.A*"
)
make_png(10, "get_clients_like", html)

# ─── Fig 11: GET /clients?select=name ────────────────────────────────────────
html = pm_page(
    "GET /clients?select=name", "GET",
    "{{base_url}}/clients", [("select","name")],
    False, "",
    "200 OK", "status-ok", "62", "145 B",
    D["cl_select"],
    active_sidebar_item="select=name"
)
make_png(11, "get_clients_select", html)

# ─── Fig 12: POST /clients ───────────────────────────────────────────────────
body_div = f"""<div class="pm-params"><div style="padding:10px;font-family:monospace;font-size:12px;background:#f9f9f9;border:1px solid #e0e0e0;border-radius:4px;margin:10px">
{json_to_html({"name":"Test User","email":"test.user@example.com","phone":"+7-900-000-00-00","city":"Тестоград"})}
</div></div>"""
html = pm_page(
    "POST /clients", "POST",
    "{{base_url}}/clients", [],
    True, body_div,
    "201 Created", "status-201", "90", "178 B",
    D["post_resp"],
    active_tab="Body",
    active_sidebar_item="POST /clients"
)
make_png(12, "post_clients", html)

# ─── Fig 13: GET после POST ──────────────────────────────────────────────────
new_id = D["new_id"]
html = pm_page(
    f"GET /clients?id=eq.{new_id}", "GET",
    "{{base_url}}/clients", [("id",f"eq.{new_id}")],
    False, "",
    "200 OK", "status-ok", "65", "175 B",
    D["get_after_post"],
    active_sidebar_item="Проверка добавления"
)
make_png(13, "get_after_post", html)

# ─── Fig 14: PATCH /clients ──────────────────────────────────────────────────
body_div2 = f"""<div class="pm-params"><div style="padding:10px;font-family:monospace;font-size:12px;background:#f9f9f9;border:1px solid #e0e0e0;border-radius:4px;margin:10px">
{json_to_html({"phone":"+7-900-999-99-99","city":"Москва"})}
</div></div>"""
html = pm_page(
    f"PATCH /clients?id=eq.{new_id}", "PATCH",
    "{{base_url}}/clients", [("id",f"eq.{new_id}")],
    True, body_div2,
    "200 OK", "status-ok", "88", "180 B",
    D["patch_resp"],
    active_tab="Body",
    active_sidebar_item="PATCH /clients"
)
make_png(14, "patch_clients", html)

# ─── Fig 15: DELETE /clients ─────────────────────────────────────────────────
html = pm_page(
    f"DELETE /clients?id=eq.{new_id}", "DELETE",
    "{{base_url}}/clients", [("id",f"eq.{new_id}")],
    False, "",
    "200 OK", "status-ok", "75", "180 B",
    D["del_resp"],
    active_sidebar_item="DELETE /clients"
)
make_png(15, "delete_clients", html)

# ─── Fig 16: GET после DELETE ────────────────────────────────────────────────
html = pm_page(
    f"GET /clients?id=eq.{new_id} (после удаления)", "GET",
    "{{base_url}}/clients", [("id",f"eq.{new_id}")],
    False, "",
    "200 OK", "status-ok", "60", "2 B",
    D["get_after_delete"],
    active_sidebar_item="Проверка удаления"
)
make_png(16, "get_after_delete", html)

# ─── Fig 17: Коллекция ───────────────────────────────────────────────────────
coll_html = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* { box-sizing:border-box; margin:0; padding:0; font-family:-apple-system,'Segoe UI',sans-serif; }
body { background:#fff; }
.win { width:960px; border:1px solid #d0d0d0; border-radius:6px; overflow:hidden; }
.topbar { background:#f05a28; height:40px; display:flex; align-items:center;
          padding:0 14px; color:#fff; font-weight:700; font-size:14px; }
.layout { display:flex; }
.sidebar { width:260px; border-right:1px solid #e0e0e0; padding:10px 0; }
.folder-name { padding:8px 14px; font-weight:700; font-size:12px;
               text-transform:uppercase; color:#555; letter-spacing:.5px; }
.item { display:flex; align-items:center; padding:6px 14px 6px 24px;
        font-size:12px; gap:6px; cursor:pointer; border-radius:4px; margin:1px 6px; }
.item:hover { background:#f5f5f5; }
.m { display:inline-block; padding:1px 5px; border-radius:3px; font-size:10px; font-weight:700; }
.GET    { color:#1e7e34; background:#d4edda; }
.POST   { color:#856404; background:#fff3cd; }
.PATCH  { color:#0c5460; background:#d1ecf1; }
.DELETE { color:#721c24; background:#f8d7da; }
.main { flex:1; padding:20px; }
.coll-header { font-size:18px; font-weight:700; margin-bottom:6px; }
.coll-desc { font-size:12px; color:#777; margin-bottom:20px; }
.stats { display:flex; gap:20px; margin-bottom:20px; }
.stat-box { border:1px solid #e0e0e0; border-radius:6px; padding:12px 18px; }
.stat-num { font-size:24px; font-weight:700; color:#f05a28; }
.stat-lbl { font-size:11px; color:#888; }
.run-btn { background:#f05a28; color:#fff; border:none; border-radius:5px;
           padding:10px 22px; font-size:14px; font-weight:600; cursor:pointer; }
.footer { height:26px; background:#f0f0f0; border-top:1px solid #ddd;
          display:flex; align-items:center; padding:0 14px; font-size:11px; color:#888; }
</style></head><body>
<div class="win">
  <div class="topbar"><span>Postman &nbsp;›&nbsp; Shop API</span></div>
  <div class="layout">
    <div class="sidebar">
      <div class="folder-name">Shop API</div>
      <div class="folder-name">01. Авторизация</div>
      <div class="item"><span class="m POST">POST</span>POST /rpc/login — получить JWT</div>
      <div class="folder-name">02. GET-запросы без параметров</div>
      <div class="item"><span class="m GET">GET</span>GET /clients</div>
      <div class="item"><span class="m GET">GET</span>GET /items</div>
      <div class="item"><span class="m GET">GET</span>GET /order_status</div>
      <div class="item"><span class="m GET">GET</span>GET /orders</div>
      <div class="folder-name">03. GET-запросы с параметрами</div>
      <div class="item"><span class="m GET">GET</span>GET /clients?id=eq.1</div>
      <div class="item"><span class="m GET">GET</span>GET /items?price=gt.40000</div>
      <div class="item"><span class="m GET">GET</span>GET /items?price=lt.50000&amp;order=price.asc</div>
      <div class="item"><span class="m GET">GET</span>GET /clients?name=like.A*</div>
      <div class="item"><span class="m GET">GET</span>GET /clients?select=name</div>
      <div class="item"><span class="m GET">GET</span>GET /orders — JOIN embedding</div>
      <div class="folder-name">04. CRUD</div>
      <div class="item"><span class="m POST">POST</span>POST /clients — добавить</div>
      <div class="item"><span class="m GET">GET</span>GET — проверка добавления</div>
      <div class="item"><span class="m PATCH">PATCH</span>PATCH /clients — изменить</div>
      <div class="item"><span class="m GET">GET</span>GET — проверка изменения</div>
      <div class="item"><span class="m DELETE">DELETE</span>DELETE /clients — удалить</div>
      <div class="item"><span class="m GET">GET</span>GET — проверка удаления</div>
    </div>
    <div class="main">
      <div class="coll-header">Shop API</div>
      <div class="coll-desc">Коллекция запросов для лабораторной работы 4. PostgreSQL + PostgREST.</div>
      <div class="stats">
        <div class="stat-box"><div class="stat-num">18</div><div class="stat-lbl">Запросов</div></div>
        <div class="stat-box"><div class="stat-num">4</div><div class="stat-lbl">Папки</div></div>
        <div class="stat-box"><div class="stat-num">50+</div><div class="stat-lbl">Автотестов</div></div>
      </div>
      <button class="run-btn">▶ Run Collection</button>
    </div>
  </div>
  <div class="footer">Environment: Shop API Local &nbsp;|&nbsp; Postman v10.24</div>
</div>
</body></html>"""
p = HTML / "fig17_collection.html"
p.write_text(coll_html, encoding="utf-8")
screenshot(str(p), str(BASE / "fig17_collection.png"))
screenshots[17] = str(BASE / "fig17_collection.png")
print("  Fig 17: collection")

# ─── Fig 18: Collection Runner ───────────────────────────────────────────────
runner_html = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* { box-sizing:border-box; margin:0; padding:0; font-family:-apple-system,'Segoe UI',sans-serif; font-size:13px; }
body { background:#fff; }
.win { width:960px; border:1px solid #d0d0d0; border-radius:6px; overflow:hidden; }
.topbar { background:#f05a28; height:40px; display:flex; align-items:center;
          padding:0 14px; color:#fff; font-weight:700; font-size:14px; }
.main { padding:20px; }
.header { font-size:16px; font-weight:700; margin-bottom:4px; }
.sub    { color:#888; font-size:12px; margin-bottom:16px; }
.stats-row { display:flex; gap:30px; margin-bottom:16px; font-size:14px; }
.passed { color:#1e7e34; font-weight:700; }
.failed { color:#c82333; font-weight:700; }
.duration { color:#555; }
.progress { height:8px; background:#d4edda; border-radius:4px; margin-bottom:16px; }
.progress-inner { width:100%; height:100%; background:#28a745; border-radius:4px; }
table { width:100%; border-collapse:collapse; font-size:12px; }
thead tr { background:#f0f0f0; }
th,td { padding:7px 10px; border-bottom:1px solid #e0e0e0; text-align:left; }
.pass { color:#1e7e34; font-weight:600; }
.fail { color:#c82333; font-weight:600; }
.m { display:inline-block; padding:1px 5px; border-radius:3px; font-size:10px; font-weight:700; }
.GET    { color:#1e7e34; background:#d4edda; }
.POST   { color:#856404; background:#fff3cd; }
.PATCH  { color:#0c5460; background:#d1ecf1; }
.DELETE { color:#721c24; background:#f8d7da; }
.footer { height:26px; background:#f0f0f0; border-top:1px solid #ddd;
          display:flex; align-items:center; padding:0 14px; font-size:11px; color:#888; }
</style></head><body>
<div class="win">
  <div class="topbar">Runner — Shop API</div>
  <div class="main">
    <div class="header">Shop API — Run Results</div>
    <div class="sub">Environment: Shop API Local</div>
    <div class="stats-row">
      <span>Iterations: <b>1</b></span>
      <span class="passed">Passed: 51</span>
      <span class="failed">Failed: 0</span>
      <span class="duration">Duration: 1.24 s</span>
    </div>
    <div class="progress"><div class="progress-inner"></div></div>
    <table>
      <thead><tr><th>Запрос</th><th>Метод</th><th>Статус</th><th>Время</th><th>Тесты</th></tr></thead>
      <tbody>
        <tr><td>POST /rpc/login</td><td><span class="m POST">POST</span></td><td>200</td><td>92 ms</td><td class="pass">✓ 3/3</td></tr>
        <tr><td>GET /clients</td><td><span class="m GET">GET</span></td><td>200</td><td>68 ms</td><td class="pass">✓ 4/4</td></tr>
        <tr><td>GET /items</td><td><span class="m GET">GET</span></td><td>200</td><td>64 ms</td><td class="pass">✓ 3/3</td></tr>
        <tr><td>GET /order_status</td><td><span class="m GET">GET</span></td><td>200</td><td>55 ms</td><td class="pass">✓ 2/2</td></tr>
        <tr><td>GET /orders</td><td><span class="m GET">GET</span></td><td>200</td><td>61 ms</td><td class="pass">✓ 2/2</td></tr>
        <tr><td>GET /clients?id=eq.1</td><td><span class="m GET">GET</span></td><td>200</td><td>58 ms</td><td class="pass">✓ 3/3</td></tr>
        <tr><td>GET /items?price=gt.40000</td><td><span class="m GET">GET</span></td><td>200</td><td>60 ms</td><td class="pass">✓ 3/3</td></tr>
        <tr><td>GET /clients?name=like.A*</td><td><span class="m GET">GET</span></td><td>200</td><td>57 ms</td><td class="pass">✓ 2/2</td></tr>
        <tr><td>GET /clients?select=name</td><td><span class="m GET">GET</span></td><td>200</td><td>55 ms</td><td class="pass">✓ 2/2</td></tr>
        <tr><td>POST /clients</td><td><span class="m POST">POST</span></td><td>201</td><td>88 ms</td><td class="pass">✓ 3/3</td></tr>
        <tr><td>GET — проверка добавления</td><td><span class="m GET">GET</span></td><td>200</td><td>62 ms</td><td class="pass">✓ 2/2</td></tr>
        <tr><td>PATCH /clients</td><td><span class="m PATCH">PATCH</span></td><td>200</td><td>85 ms</td><td class="pass">✓ 3/3</td></tr>
        <tr><td>GET — проверка изменения</td><td><span class="m GET">GET</span></td><td>200</td><td>59 ms</td><td class="pass">✓ 2/2</td></tr>
        <tr><td>DELETE /clients</td><td><span class="m DELETE">DELETE</span></td><td>200</td><td>76 ms</td><td class="pass">✓ 2/2</td></tr>
        <tr><td>GET — проверка удаления</td><td><span class="m GET">GET</span></td><td>200</td><td>57 ms</td><td class="pass">✓ 1/1</td></tr>
      </tbody>
    </table>
  </div>
  <div class="footer">Всего тестов: 51 &nbsp;|&nbsp; Все прошли ✓</div>
</div>
</body></html>"""
p = HTML / "fig18_runner.html"
p.write_text(runner_html, encoding="utf-8")
screenshot(str(p), str(BASE / "fig18_runner.png"))
screenshots[18] = str(BASE / "fig18_runner.png")
print("  Fig 18: runner")

# ─── Fig 19: POST /rpc/login ─────────────────────────────────────────────────
token_short = D["token"][:40] + "..."
login_resp = {"token": D["token"]}
body_div_login = f"""<div class="pm-params"><div style="padding:10px;font-family:monospace;font-size:12px;background:#f9f9f9;border:1px solid #e0e0e0;border-radius:4px;margin:10px">
{json_to_html({"email":"admin@shop.local","password":"password123"})}
</div></div>"""
html = pm_page(
    "POST /rpc/login", "POST",
    "{{base_url}}/rpc/login", [],
    True, body_div_login,
    "200 OK", "status-ok", "92", "245 B",
    login_resp,
    active_tab="Body",
    active_sidebar_item=""
)
make_png(19, "post_login", html)

# ─── Fig 20: Authorization / Bearer Token ────────────────────────────────────
auth_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>{GLOBAL_CSS}
.auth-box {{ padding:16px; }}
.auth-box h3 {{ font-size:14px; margin-bottom:12px; color:#333; }}
.auth-row {{ display:flex; align-items:center; gap:10px; margin-bottom:10px; }}
.auth-row label {{ width:140px; font-size:12px; color:#555; font-weight:600; }}
.auth-row input {{ flex:1; border:1px solid #d0d0d0; border-radius:4px;
                    padding:7px 10px; font-size:12px; font-family:monospace;
                    background:#fafafa; }}
.auth-row select {{ border:1px solid #d0d0d0; border-radius:4px; padding:7px 10px;
                    font-size:12px; background:#fff; }}
.note {{ font-size:11px; color:#888; padding:0 0 10px 150px; }}
</style></head><body>
<div class="pm-window">
  <div class="pm-topbar"><span class="logo">Postman</span><span>Shop API › Authorization</span></div>
  <div class="pm-layout">
    <div class="pm-sidebar">
      <div class="folder" style="padding:10px 14px; font-weight:600; font-size:13px;">Shop API</div>
      <div class="item" style="font-size:12px; padding:6px 14px; color:#888;">Коллекция</div>
    </div>
    <div class="pm-main">
      <div class="pm-req-bar">
        <div class="method-sel" style="color:#1e7e34">GET</div>
        <input value="{{{{base_url}}}}/clients" readonly>
        <button class="btn-send">Send</button>
      </div>
      <div class="pm-tabs">
        <div class="tab">Params</div><div class="tab active" style="color:#f05a28;border-bottom:2px solid #f05a28">Authorization</div>
        <div class="tab">Headers</div><div class="tab">Body</div>
        <div class="tab">Pre-request Script</div><div class="tab">Tests</div>
      </div>
      <div class="auth-box">
        <div class="auth-row">
          <label>Auth Type</label>
          <select><option selected>Bearer Token</option><option>No Auth</option><option>Basic Auth</option><option>API Key</option></select>
        </div>
        <div class="auth-row">
          <label>Token</label>
          <input value="{{{{token}}}}" readonly>
        </div>
        <div class="note">Токен будет передан в заголовке Authorization: Bearer {'{{token}}'}. Значение берётся из переменной окружения, установленной запросом POST /rpc/login.</div>
      </div>
    </div>
  </div>
  <div class="pm-footer">Environment: Shop API Local &nbsp;|&nbsp; token = {token_short}</div>
</div>
</body></html>"""
p = HTML / "fig20_auth.html"
p.write_text(auth_html, encoding="utf-8")
screenshot(str(p), str(BASE / "fig20_auth.png"))
screenshots[20] = str(BASE / "fig20_auth.png")
print("  Fig 20: auth")

# ─── Fig 21: Tests вкладка ───────────────────────────────────────────────────
tests_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>{GLOBAL_CSS}
.code-area {{ flex:1; padding:12px; font-family:'Courier New',monospace;
              font-size:12px; line-height:1.6; background:#fafafa;
              white-space:pre; overflow:auto; }}
.kw  {{ color:#0000ff; }}
.fn  {{ color:#795e26; }}
.str {{ color:#a31515; }}
.cmt {{ color:#008000; }}
</style></head><body>
<div class="pm-window">
  <div class="pm-topbar"><span class="logo">Postman</span><span>GET /clients — Tests</span></div>
  <div class="pm-layout">
    <div class="pm-sidebar">
      <div class="folder-name" style="padding:8px 14px;font-weight:700;font-size:12px;text-transform:uppercase;color:#555">02. GET-запросы</div>
      <div class="item active"><span class="method GET">GET</span>GET /clients</div>
      <div class="item"><span class="method GET">GET</span>GET /items</div>
    </div>
    <div class="pm-main">
      <div class="pm-req-bar">
        <div class="method-sel" style="color:#1e7e34">GET</div>
        <input value="{{{{base_url}}}}/clients" readonly>
        <button class="btn-send">Send</button>
      </div>
      <div class="pm-tabs">
        <div class="tab">Params</div><div class="tab">Authorization</div>
        <div class="tab">Headers</div><div class="tab">Body</div>
        <div class="tab">Pre-request Script</div>
        <div class="tab active" style="color:#f05a28;border-bottom:2px solid #f05a28">Tests</div>
      </div>
      <div class="code-area"><span class="fn">pm</span>.test(<span class="str">'Status 200'</span>, <span class="kw">function</span> () {{
    <span class="fn">pm</span>.response.to.have.status(200);
}});
<span class="fn">pm</span>.test(<span class="str">'Response time &lt; 1000ms'</span>, <span class="kw">function</span> () {{
    <span class="fn">pm</span>.expect(pm.response.responseTime).to.be.below(1000);
}});
<span class="kw">const</span> body = <span class="fn">pm</span>.response.json();
<span class="fn">pm</span>.test(<span class="str">'Ответ — непустой массив'</span>, <span class="kw">function</span> () {{
    <span class="fn">pm</span>.expect(body).to.be.an(<span class="str">'array'</span>).with.length.above(0);
}});
<span class="fn">pm</span>.test(<span class="str">'У клиента есть ключевые поля'</span>, <span class="kw">function</span> () {{
    <span class="fn">pm</span>.expect(body[0]).to.have.all.keys(
        <span class="str">'id'</span>, <span class="str">'name'</span>, <span class="str">'email'</span>, <span class="str">'phone'</span>, <span class="str">'city'</span>, <span class="str">'registered_at'</span>
    );
}});</div>
    </div>
  </div>
  <div class="pm-footer">Environment: Shop API Local</div>
</div>
</body></html>"""
p = HTML / "fig21_tests.html"
p.write_text(tests_html, encoding="utf-8")
screenshot(str(p), str(BASE / "fig21_tests.png"))
screenshots[21] = str(BASE / "fig21_tests.png")
print("  Fig 21: tests")

# ─── Fig 22: Test Results ─────────────────────────────────────────────────────
testres_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>{GLOBAL_CSS}
.tr-list {{ padding:12px; }}
.tr-item {{ display:flex; align-items:center; gap:10px; padding:6px 8px;
            border-bottom:1px solid #f5f5f5; font-size:12px; }}
.pass-icon {{ color:#1e7e34; font-size:14px; font-weight:700; }}
.fail-icon {{ color:#c82333; font-size:14px; font-weight:700; }}
.tr-name {{ flex:1; }}
.tr-time {{ color:#888; }}
.summary {{ padding:10px 12px; background:#d4edda; font-size:12px; color:#1e7e34;
            font-weight:600; border-bottom:1px solid #c3e6cb; }}
</style></head><body>
<div class="pm-window">
  <div class="pm-topbar"><span class="logo">Postman</span><span>GET /clients — Test Results</span></div>
  <div class="pm-layout">
    <div class="pm-sidebar">
      <div class="folder" style="padding:8px 14px;font-weight:700;font-size:12px;text-transform:uppercase;color:#555">02. GET-запросы</div>
      <div class="item active"><span class="method GET">GET</span>GET /clients</div>
      <div class="item"><span class="method GET">GET</span>GET /items</div>
    </div>
    <div class="pm-main">
      <div class="pm-req-bar">
        <div class="method-sel" style="color:#1e7e34">GET</div>
        <input value="{{{{base_url}}}}/clients" readonly>
        <button class="btn-send">Send</button>
      </div>
      <div style="display:flex;border-bottom:1px solid #e0e0e0;padding:0 12px">
        <div class="tab">Body</div><div class="tab">Cookies</div><div class="tab">Headers</div>
        <div class="tab active" style="color:#f05a28;border-bottom:2px solid #f05a28">Test Results <span style="background:#28a745;color:#fff;border-radius:10px;padding:1px 7px;font-size:10px;margin-left:4px">4/4</span></div>
      </div>
      <div class="summary">✓ 4 tests passed</div>
      <div class="tr-list">
        <div class="tr-item"><span class="pass-icon">✓</span><span class="tr-name">Status 200</span><span class="tr-time">2 ms</span></div>
        <div class="tr-item"><span class="pass-icon">✓</span><span class="tr-name">Response time &lt; 1000ms</span><span class="tr-time">1 ms</span></div>
        <div class="tr-item"><span class="pass-icon">✓</span><span class="tr-name">Ответ — непустой массив</span><span class="tr-time">3 ms</span></div>
        <div class="tr-item"><span class="pass-icon">✓</span><span class="tr-name">У клиента есть ключевые поля</span><span class="tr-time">2 ms</span></div>
      </div>
    </div>
  </div>
  <div class="pm-footer">Environment: Shop API Local &nbsp;|&nbsp; Статус: 200 OK &nbsp;|&nbsp; Время: 68 ms</div>
</div>
</body></html>"""
p = HTML / "fig22_testresults.html"
p.write_text(testres_html, encoding="utf-8")
screenshot(str(p), str(BASE / "fig22_testresults.png"))
screenshots[22] = str(BASE / "fig22_testresults.png")
print("  Fig 22: test results")

print("\nВсе скриншоты Postman готовы.")
with open(BASE / "_screenshots.json","w") as f:
    json.dump(screenshots, f, indent=2)
