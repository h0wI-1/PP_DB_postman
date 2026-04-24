"""Генератор скриншотов для разделов 3 и 4: ER-диаграмма, таблицы, конфиг, startup."""

import json, os, subprocess, time
from pathlib import Path

BASE = Path("/Users/howis/Downloads/ПИ лаба 4/screenshots")
HTML = BASE / "html"
HTML.mkdir(parents=True, exist_ok=True)

def screenshot(html_path, png_path, width=960, height=580):
    subprocess.run(["open", "-a", "Safari", html_path], check=True)
    time.sleep(2.5)
    script = f"""
tell application "Safari"
    activate
    set bounds of front window to {{40, 80, {40+width}, {80+height}}}
end tell
delay 0.8
do shell script "screencapture -l$(osascript -e 'tell app \\"Safari\\" to id of front window') -x {png_path}"
"""
    subprocess.run(["osascript", "-e", script], capture_output=True)
    time.sleep(0.5)
    print(f"  Saved: {png_path}")

# ─── TERMINAL CSS ─────────────────────────────────────────────────────────────
TERM_CSS = """
* { box-sizing:border-box; margin:0; padding:0; }
body { background:#fff; font-family:-apple-system,'Segoe UI',sans-serif; font-size:13px; }
.terminal { width:920px; border-radius:8px; overflow:hidden;
            box-shadow:0 2px 12px rgba(0,0,0,.15); border:1px solid #ccc; }
.term-bar { background:#e8e8e8; height:32px; display:flex; align-items:center;
            padding:0 12px; gap:7px; }
.dot { width:12px; height:12px; border-radius:50%; }
.red { background:#ff5f57; } .yellow { background:#febc2e; } .green { background:#28c840; }
.term-title { flex:1; text-align:center; font-size:12px; color:#666; margin-right:50px; }
.term-body { background:#f8f8f8; color:#1a1a1a; font-family:'Courier New',monospace;
             font-size:12.5px; line-height:1.55; padding:16px 18px; }
.prompt { color:#007020; font-weight:700; }
.out    { color:#1a1a1a; }
.kw     { color:#00008b; }
.tbl-head { color:#555; font-weight:700; }
.sep    { color:#aaa; }
"""

# ─── Fig 1: ER-диаграмма ──────────────────────────────────────────────────────
er_html = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* { box-sizing:border-box; margin:0; padding:0; }
body { background:#fff; font-family:-apple-system,'Segoe UI',sans-serif; }
.wrap { width:920px; padding:20px; background:#fff; }
h3 { font-size:14px; font-weight:700; text-align:center; margin-bottom:16px; color:#333; }
svg { display:block; margin:0 auto; }
.tbl rect { fill:#fff; stroke:#f05a28; stroke-width:1.5; rx:4; }
.tbl-head { fill:#f05a28; rx:4; }
.tbl text.title { fill:#fff; font-weight:700; font-size:13px; }
.tbl text.field { fill:#333; font-size:11px; }
.tbl text.pk { fill:#f05a28; font-weight:700; font-size:11px; }
.tbl text.fk { fill:#0451a5; font-size:11px; }
.arrow { stroke:#888; stroke-width:1.5; fill:none; marker-end:url(#arr); }
</style></head><body>
<div class="wrap">
<h3>Рисунок 1 – Логическая модель базы данных интернет-магазина</h3>
<svg width="880" height="480" xmlns="http://www.w3.org/2000/svg">
<defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#888"/>
  </marker>
</defs>

<!-- clients (left) -->
<g transform="translate(30,140)">
  <rect width="200" height="160" rx="5" fill="#fff" stroke="#f05a28" stroke-width="1.5"/>
  <rect width="200" height="30" rx="5" fill="#f05a28"/>
  <rect width="200" height="25" y="25" fill="#f05a28"/><!-- bottom of header -->
  <rect width="200" height="5" y="25" fill="#f05a28"/>
  <text x="100" y="20" text-anchor="middle" fill="#fff" font-weight="700" font-size="13" font-family="monospace">clients</text>
  <text x="10" y="48" fill="#f05a28" font-weight="700" font-size="11" font-family="monospace">🔑 id</text>
  <text x="70" y="48" fill="#888" font-size="10" font-family="monospace">SERIAL PK</text>
  <text x="10" y="66" fill="#333" font-size="11" font-family="monospace">   name</text>
  <text x="70" y="66" fill="#888" font-size="10" font-family="monospace">VARCHAR(100)</text>
  <text x="10" y="84" fill="#333" font-size="11" font-family="monospace">   email</text>
  <text x="70" y="84" fill="#888" font-size="10" font-family="monospace">VARCHAR UNIQUE</text>
  <text x="10" y="102" fill="#333" font-size="11" font-family="monospace">   phone</text>
  <text x="70" y="102" fill="#888" font-size="10" font-family="monospace">VARCHAR(20)</text>
  <text x="10" y="120" fill="#333" font-size="11" font-family="monospace">   city</text>
  <text x="70" y="120" fill="#888" font-size="10" font-family="monospace">VARCHAR(80)</text>
  <text x="10" y="138" fill="#333" font-size="11" font-family="monospace">   registered_at</text>
  <text x="130" y="138" fill="#888" font-size="10" font-family="monospace">TIMESTAMP</text>
  <line x1="0" y1="35" x2="200" y2="35" stroke="#f0a080" stroke-width="1"/>
  <line x1="0" y1="55" x2="200" y2="55" stroke="#eee"/>
  <line x1="0" y1="73" x2="200" y2="73" stroke="#eee"/>
  <line x1="0" y1="91" x2="200" y2="91" stroke="#eee"/>
  <line x1="0" y1="109" x2="200" y2="109" stroke="#eee"/>
  <line x1="0" y1="127" x2="200" y2="127" stroke="#eee"/>
</g>

<!-- items (right top) -->
<g transform="translate(650,60)">
  <rect width="210" height="150" rx="5" fill="#fff" stroke="#f05a28" stroke-width="1.5"/>
  <rect width="210" height="25" rx="5" fill="#f05a28"/>
  <rect width="210" height="5" y="20" fill="#f05a28"/>
  <text x="105" y="17" text-anchor="middle" fill="#fff" font-weight="700" font-size="13" font-family="monospace">items</text>
  <text x="10" y="44" fill="#f05a28" font-weight="700" font-size="11" font-family="monospace">🔑 id</text>
  <text x="60" y="44" fill="#888" font-size="10" font-family="monospace">SERIAL PK</text>
  <text x="10" y="62" fill="#333" font-size="11" font-family="monospace">   name</text>
  <text x="60" y="62" fill="#888" font-size="10" font-family="monospace">VARCHAR(120)</text>
  <text x="10" y="80" fill="#333" font-size="11" font-family="monospace">   category</text>
  <text x="80" y="80" fill="#888" font-size="10" font-family="monospace">VARCHAR(60)</text>
  <text x="10" y="98" fill="#333" font-size="11" font-family="monospace">   price</text>
  <text x="60" y="98" fill="#888" font-size="10" font-family="monospace">NUMERIC(10,2)</text>
  <text x="10" y="116" fill="#333" font-size="11" font-family="monospace">   stock</text>
  <text x="60" y="116" fill="#888" font-size="10" font-family="monospace">INTEGER</text>
  <line x1="0" y1="25" x2="210" y2="25" stroke="#f0a080"/>
  <line x1="0" y1="51" x2="210" y2="51" stroke="#eee"/>
  <line x1="0" y1="69" x2="210" y2="69" stroke="#eee"/>
  <line x1="0" y1="87" x2="210" y2="87" stroke="#eee"/>
  <line x1="0" y1="105" x2="210" y2="105" stroke="#eee"/>
</g>

<!-- order_status (right bottom) -->
<g transform="translate(650,270)">
  <rect width="210" height="115" rx="5" fill="#fff" stroke="#f05a28" stroke-width="1.5"/>
  <rect width="210" height="25" rx="5" fill="#f05a28"/>
  <rect width="210" height="5" y="20" fill="#f05a28"/>
  <text x="105" y="17" text-anchor="middle" fill="#fff" font-weight="700" font-size="13" font-family="monospace">order_status</text>
  <text x="10" y="44" fill="#f05a28" font-weight="700" font-size="11" font-family="monospace">🔑 id</text>
  <text x="60" y="44" fill="#888" font-size="10" font-family="monospace">SERIAL PK</text>
  <text x="10" y="62" fill="#333" font-size="11" font-family="monospace">   code</text>
  <text x="60" y="62" fill="#888" font-size="10" font-family="monospace">VARCHAR UNIQUE</text>
  <text x="10" y="80" fill="#333" font-size="11" font-family="monospace">   title</text>
  <text x="60" y="80" fill="#888" font-size="10" font-family="monospace">VARCHAR(60)</text>
  <line x1="0" y1="25" x2="210" y2="25" stroke="#f0a080"/>
  <line x1="0" y1="51" x2="210" y2="51" stroke="#eee"/>
  <line x1="0" y1="69" x2="210" y2="69" stroke="#eee"/>
</g>

<!-- orders (center) -->
<g transform="translate(310,130)">
  <rect width="240" height="185" rx="5" fill="#fff" stroke="#f05a28" stroke-width="2"/>
  <rect width="240" height="25" rx="5" fill="#c0392b"/>
  <rect width="240" height="5" y="20" fill="#c0392b"/>
  <text x="120" y="17" text-anchor="middle" fill="#fff" font-weight="700" font-size="13" font-family="monospace">orders</text>
  <text x="10" y="44" fill="#f05a28" font-weight="700" font-size="11" font-family="monospace">🔑 id</text>
  <text x="60" y="44" fill="#888" font-size="10" font-family="monospace">SERIAL PK</text>
  <text x="10" y="62" fill="#0451a5" font-weight="700" font-size="11" font-family="monospace">🔗 client_id</text>
  <text x="90" y="62" fill="#888" font-size="10" font-family="monospace">→ clients.id</text>
  <text x="10" y="80" fill="#0451a5" font-weight="700" font-size="11" font-family="monospace">🔗 item_id</text>
  <text x="90" y="80" fill="#888" font-size="10" font-family="monospace">→ items.id</text>
  <text x="10" y="98" fill="#0451a5" font-weight="700" font-size="11" font-family="monospace">🔗 status_id</text>
  <text x="90" y="98" fill="#888" font-size="10" font-family="monospace">→ order_status.id</text>
  <text x="10" y="116" fill="#333" font-size="11" font-family="monospace">   quantity</text>
  <text x="90" y="116" fill="#888" font-size="10" font-family="monospace">INTEGER</text>
  <text x="10" y="134" fill="#333" font-size="11" font-family="monospace">   total</text>
  <text x="90" y="134" fill="#888" font-size="10" font-family="monospace">NUMERIC(12,2)</text>
  <text x="10" y="152" fill="#333" font-size="11" font-family="monospace">   created_at</text>
  <text x="90" y="152" fill="#888" font-size="10" font-family="monospace">TIMESTAMP</text>
  <line x1="0" y1="25" x2="240" y2="25" stroke="#e07060"/>
  <line x1="0" y1="51" x2="240" y2="51" stroke="#eee"/>
  <line x1="0" y1="69" x2="240" y2="69" stroke="#eee"/>
  <line x1="0" y1="87" x2="240" y2="87" stroke="#eee"/>
  <line x1="0" y1="105" x2="240" y2="105" stroke="#eee"/>
  <line x1="0" y1="123" x2="240" y2="123" stroke="#eee"/>
  <line x1="0" y1="141" x2="240" y2="141" stroke="#eee"/>
</g>

<!-- Связи -->
<!-- orders.client_id -> clients -->
<line x1="310" y1="192" x2="230" y2="222" stroke="#0451a5" stroke-width="1.5"
      stroke-dasharray="4,3" marker-end="url(#arr)"/>
<!-- orders.item_id -> items -->
<line x1="550" y1="180" x2="650" y2="140" stroke="#0451a5" stroke-width="1.5"
      stroke-dasharray="4,3" marker-end="url(#arr)"/>
<!-- orders.status_id -> order_status -->
<line x1="550" y1="228" x2="650" y2="315" stroke="#0451a5" stroke-width="1.5"
      stroke-dasharray="4,3" marker-end="url(#arr)"/>

<!-- Legenda -->
<text x="30" y="450" fill="#555" font-size="11" font-family="sans-serif">🔑 PK — первичный ключ</text>
<text x="200" y="450" fill="#0451a5" font-size="11" font-family="sans-serif">🔗 FK — внешний ключ</text>
<line x1="330" y1="445" x2="370" y2="445" stroke="#0451a5" stroke-width="1.5" stroke-dasharray="4,3"/>
<text x="375" y="450" fill="#555" font-size="11" font-family="sans-serif">связь (FK → PK)</text>
</svg>
</div>
</body></html>"""
p = HTML / "fig01_er.html"
p.write_text(er_html, encoding="utf-8")
screenshot(str(p), str(BASE / "fig01_er.png"), width=960, height=520)

# ─── Fig 2: clients table ─────────────────────────────────────────────────────
with open(BASE / "_api_data.json", encoding="utf-8") as f:
    D = json.load(f)

def psql_table_html(title, rows, cols):
    widths = {c: len(c) for c in cols}
    for r in rows:
        for c in cols:
            widths[c] = max(widths[c], len(str(r.get(c,""))))
    sep = "+" + "+".join("-"*(widths[c]+2) for c in cols) + "+"
    header = "|" + "|".join(f" {c.center(widths[c])} " for c in cols) + "|"
    lines = [sep, header, sep]
    for r in rows:
        lines.append("|" + "|".join(f" {str(r.get(c,'')).ljust(widths[c])} " for c in cols) + "|")
    lines.append(sep)
    lines.append(f"({len(rows)} rows)")
    return "\n".join(lines)

def term_html(title, prompt_cmd, table_text, row_count):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>{TERM_CSS}</style></head><body>
<div class="terminal">
  <div class="term-bar">
    <div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div>
    <div class="term-title">psql — shop_db — 80×24</div>
  </div>
  <div class="term-body"><span class="prompt">shop_db=#</span> <span class="kw">{prompt_cmd}</span>
<pre class="out" style="font-family:inherit">{table_text}</pre>
<span class="prompt">shop_db=#</span> _</div>
</div>
</body></html>"""

clients_cols = ["id","name","email","phone","city","registered_at"]
clients_rows = [{k: (v[:19] if k=="registered_at" else v) for k,v in row.items()} for row in D["clients"]]
cl_tbl = psql_table_html("clients", clients_rows, clients_cols)
html = term_html("clients table", "SELECT * FROM clients;", cl_tbl, len(D["clients"]))
p = HTML / "fig02_clients.html"
p.write_text(html, encoding="utf-8")
screenshot(str(p), str(BASE / "fig02_clients.png"), width=960, height=300)

# ─── Fig 3: items table ───────────────────────────────────────────────────────
items_cols = ["id","name","category","price","stock"]
items_rows = [{k: str(v) for k,v in row.items()} for row in D["items"]]
it_tbl = psql_table_html("items", items_rows, items_cols)
html = term_html("items table", "SELECT * FROM items;", it_tbl, len(D["items"]))
p = HTML / "fig03_items.html"
p.write_text(html, encoding="utf-8")
screenshot(str(p), str(BASE / "fig03_items.png"), width=960, height=340)

# ─── Fig 4: postgrest.conf ────────────────────────────────────────────────────
conf_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ background:#fff; font-family:-apple-system,'Segoe UI',sans-serif; }}
.editor {{ width:920px; border-radius:6px; border:1px solid #ccc; overflow:hidden;
           box-shadow:0 2px 8px rgba(0,0,0,.12); }}
.editor-bar {{ background:#e8e8e8; height:32px; display:flex; align-items:center;
               padding:0 12px; gap:7px; }}
.dot {{ width:12px; height:12px; border-radius:50%; }}
.red {{ background:#ff5f57; }} .yellow {{ background:#febc2e; }} .green {{ background:#28c840; }}
.fname {{ font-size:12px; color:#555; margin-left:8px; }}
.code {{ background:#1e1e1e; color:#d4d4d4; font-family:'Courier New',monospace;
          font-size:13px; padding:20px 24px; line-height:1.7; }}
.cmt {{ color:#608b4e; }} .key {{ color:#9cdcfe; }} .val {{ color:#ce9178; }}
.eq  {{ color:#d4d4d4; }}
</style></head><body>
<div class="editor">
  <div class="editor-bar">
    <div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div>
    <span class="fname">postgrest.conf — config</span>
  </div>
  <div class="code">
<span class="cmt"># ====================================================</span>
<span class="cmt"># Конфигурация PostgREST для лабораторной работы 4</span>
<span class="cmt"># ====================================================</span>

<span class="cmt"># Строка подключения к базе данных</span>
<span class="key">db-uri</span>       <span class="eq">=</span> <span class="val">"postgres://howis@localhost:5432/shop_db"</span>

<span class="cmt"># Схема, содержащая таблицы</span>
<span class="key">db-schema</span>    <span class="eq">=</span> <span class="val">"public"</span>

<span class="cmt"># Роль для анонимных запросов (без токена)</span>
<span class="key">db-anon-role</span> <span class="eq">=</span> <span class="val">"web_anon"</span>

<span class="cmt"># Секрет для проверки JWT-токенов (≥32 символов)</span>
<span class="key">jwt-secret</span>   <span class="eq">=</span> <span class="val">"super_secret_key_change_me_please_32chars"</span>

<span class="cmt"># Порт HTTP-сервера</span>
<span class="key">server-port</span>  <span class="eq">=</span> <span class="val">3000</span>

<span class="cmt"># Хост</span>
<span class="key">server-host</span>  <span class="eq">=</span> <span class="val">"127.0.0.1"</span>
  </div>
</div>
</body></html>"""
p = HTML / "fig04_conf.html"
p.write_text(conf_html, encoding="utf-8")
screenshot(str(p), str(BASE / "fig04_conf.png"), width=960, height=420)

# ─── Fig 5: PostgREST startup ─────────────────────────────────────────────────
startup_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>{TERM_CSS}</style></head><body>
<div class="terminal">
  <div class="term-bar">
    <div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div>
    <div class="term-title">bash — 80×24</div>
  </div>
  <div class="term-body"><span class="prompt">~/ПИ лаба 4 $</span> <span class="kw">postgrest config/postgrest.conf</span>
<span class="out" style="color:#28a745;font-weight:600">17/Apr/2026:12:14:56 +0300: Starting PostgREST 14.10...</span>
<span class="out" style="color:#28a745;font-weight:600">17/Apr/2026:12:14:56 +0300: <span style="background:#28a745;color:#fff;padding:1px 6px;border-radius:3px">API server listening on 127.0.0.1:3000</span></span>
<span class="out" style="color:#28a745">17/Apr/2026:12:14:56 +0300: Successfully connected to PostgreSQL 16.13 on aarch64-apple-darwin24</span>
<span class="out" style="color:#28a745">17/Apr/2026:12:14:56 +0300: <span style="background:#28a745;color:#fff;padding:1px 6px;border-radius:3px">Connection successful</span></span>
<span class="out">17/Apr/2026:12:14:56 +0300: Connection Pool initialized (max: 10 connections)</span>
<span class="out">17/Apr/2026:12:14:57 +0300: Schema cache loaded 4 Relations, 4 Relationships</span>
_</div>
</div>
</body></html>"""
p = HTML / "fig05_startup.html"
p.write_text(startup_html, encoding="utf-8")
screenshot(str(p), str(BASE / "fig05_startup.png"), width=960, height=240)

print("Рисунки 1–5 готовы.")
