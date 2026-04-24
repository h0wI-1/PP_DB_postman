"""
Генератор HTML-макетов Swagger UI (18 скриншотов для отчёта).
Открывает каждый HTML в Safari и делает screencapture.
"""

import json, subprocess, time
from pathlib import Path

BASE    = Path("/Users/howis/Downloads/ПИ лаба 4/screenshots")
SW_HTML = BASE / "swagger_html"
SW_HTML.mkdir(parents=True, exist_ok=True)

with open(BASE / "_api_data.json", encoding="utf-8") as f:
    D = json.load(f)

TOKEN = D["token"]
TOKEN_CLIP = TOKEN[:48] + "..."
NEW_ID = D["new_id"]   # 8

# ─── CSS ──────────────────────────────────────────────────────────────────────
CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,'Segoe UI',sans-serif;font-size:13px;background:#fff;color:#3b4151}
.win{width:980px;background:#fff;border:1px solid #d9d9d9}

/* topbar */
.topbar{background:#3b4151;padding:12px 20px;display:flex;align-items:center;gap:12px}
.logo{color:#85ea2d;font-size:22px;font-weight:900;letter-spacing:-1px;font-family:'Arial Black',sans-serif}
.logo span{color:#fff}
.api-ver{color:#ddd;font-size:12px}
.auth-top-btn{margin-left:auto;border:1px solid #d9d9d9;background:transparent;color:#fff;
              padding:5px 14px;border-radius:4px;font-size:12px;cursor:pointer}
.auth-top-btn.done{border-color:#49cc90;color:#49cc90}

/* info */
.info{padding:16px 20px;background:#fff;border-bottom:1px solid #e0e0e0}
.info h2{font-size:24px;font-weight:700;display:inline}
.info .ver{background:#89bf04;color:#fff;font-size:11px;padding:2px 7px;border-radius:3px;
           margin-left:8px;vertical-align:middle}
.info .desc{font-size:12px;color:#555;margin-top:6px;line-height:1.5}
.info .server-label{font-size:11px;color:#888;margin-top:8px}
.info .server-url{font-family:monospace;font-size:13px;font-weight:600;color:#3b4151}
.auth-btn{display:inline-flex;align-items:center;gap:5px;border:2px solid #49cc90;
          background:#fff;color:#49cc90;padding:5px 14px;border-radius:4px;font-weight:600;
          font-size:13px;cursor:pointer;margin-top:10px}

/* schemes */
.schemes{padding:8px 20px;background:#f9f9f9;border-bottom:1px solid #e0e0e0;
         font-size:12px;color:#777;display:flex;align-items:center;gap:8px}
.scheme-sel{border:1px solid #ccc;border-radius:3px;padding:3px 8px;font-size:12px;background:#fff}

/* sections */
.section{margin:8px 20px;border:1px solid #d9d9d9;border-radius:4px}
.sec-hdr{background:#f8f8f8;padding:10px 14px;display:flex;align-items:center;
         gap:8px;cursor:pointer;border-bottom:1px solid #e0e0e0}
.sec-hdr h3{font-size:15px;font-weight:700;flex:1}
.sec-hdr .sec-desc{font-size:11px;color:#888}
.sec-arrow{font-size:12px;color:#888}

/* operations */
.op{border-bottom:1px solid #e8e8e8}
.op:last-child{border-bottom:none}
.op-row{display:flex;align-items:center;padding:9px 14px;gap:10px;cursor:pointer}
.get-row   {background:rgba(73,204,144,.08)}
.post-row  {background:rgba(97,175,254,.08)}
.patch-row {background:rgba(252,161,48,.08)}
.delete-row{background:rgba(249,62,62,.08)}

.badge{display:inline-block;min-width:58px;padding:3px 8px;border-radius:3px;
       font-size:11px;font-weight:700;text-align:center;color:#fff}
.b-get   {background:#49cc90}
.b-post  {background:#61affe}
.b-patch {background:#fca130}
.b-del   {background:#f93e3e}

.op-path{font-family:monospace;font-size:13px;font-weight:600}
.op-sum{font-size:12px;color:#888;margin-left:4px}
.op-lock{margin-left:auto;font-size:15px;color:#b5b5b5}
.op-lock.locked{color:#49cc90}
.op-arr{font-size:10px;color:#888;margin-left:4px}

/* expanded detail */
.detail{padding:16px 20px;background:#fff;border-top:1px solid #eee}
.d-desc{font-size:12px;color:#555;margin-bottom:12px;line-height:1.5}
.d-title{font-size:13px;font-weight:700;color:#3b4151;margin-bottom:8px;
          padding-bottom:4px;border-bottom:1px solid #e0e0e0}
.try-btn{border:2px solid #fca130;background:#fff;color:#fca130;padding:5px 14px;
         border-radius:4px;font-weight:600;font-size:12px;cursor:pointer;margin-bottom:10px}
.exec-btn{background:#4990e2;border:none;color:#fff;padding:6px 16px;border-radius:4px;
          font-weight:600;font-size:13px;cursor:pointer}
.clear-btn{background:#fff;border:1px solid #999;color:#555;padding:6px 14px;
           border-radius:4px;font-size:12px;cursor:pointer;margin-left:6px}

/* params */
.ptable{width:100%;border-collapse:collapse;font-size:12px;margin-bottom:12px}
.ptable th{text-align:left;padding:6px 10px;background:#f5f5f5;border:1px solid #e0e0e0;
           color:#888;font-weight:500}
.ptable td{padding:6px 10px;border:1px solid #e0e0e0;vertical-align:top}
.pname{font-family:monospace;font-weight:700}
.preq{color:#f93e3e;font-size:10px}
.ptype{font-size:11px;color:#888;display:block}
.pdesc{font-size:11px;color:#555}
.inp{width:100%;border:1px solid #ccc;border-radius:3px;padding:4px 8px;
     font-family:monospace;font-size:12px;background:#fff}
.inp.ok{background:#f0fff8;border-color:#49cc90}

/* body */
.body-area{font-family:monospace;font-size:12px;background:#f9f9f9;border:1px solid #ddd;
           padding:10px;border-radius:4px;margin-bottom:10px;line-height:1.5;white-space:pre}
.body-textarea{width:100%;height:90px;font-family:monospace;font-size:12px;border:1px solid #ccc;
               border-radius:3px;padding:8px;background:#f9f9f9;resize:none}

/* responses */
.r-section{margin-top:10px}
.r-row{display:flex;align-items:center;gap:10px;padding:7px 10px;border:1px solid #e0e0e0;margin-bottom:-1px}
.r-200{background:rgba(73,204,144,.07)}
.r-201{background:rgba(97,175,254,.07)}
.r-204{background:rgba(80,227,194,.07)}
.r-401{background:rgba(249,62,62,.07)}
.r-409{background:rgba(252,161,48,.07)}
.s200{color:#49cc90;font-weight:700}
.s201{color:#61affe;font-weight:700}
.s204{color:#50e3c2;font-weight:700}
.s401{color:#f93e3e;font-weight:700}
.s409{color:#fca130;font-weight:700}
.r-desc{font-size:12px;color:#555}

/* actual response */
.actual{border:1px solid #ddd;border-radius:4px;overflow:hidden;margin-top:10px}
.actual-hdr{background:#f8f8f8;padding:6px 12px;font-size:12px;
             display:flex;align-items:center;gap:12px;border-bottom:1px solid #ddd}
.astat{font-weight:700}
.a200{color:#49cc90}.a201{color:#61affe}.a204{color:#50e3c2}
.curl-box{background:#1a1a1a;color:#ccc;padding:8px 12px;
          font-family:monospace;font-size:11px;white-space:pre;line-height:1.4}
.resp-body{padding:10px 12px;font-family:monospace;font-size:12px;
           white-space:pre;line-height:1.5;background:#fff;max-height:180px;overflow-y:auto}

/* syntax */
.jk{color:#0451a5}
.jv{color:#098658}
.js{color:#a31515}

/* schema */
.sch-section{margin:10px 20px 16px}
.sch-item{border:1px solid #d9d9d9;border-radius:4px;margin-bottom:8px;overflow:hidden}
.sch-hdr{background:#f8f8f8;padding:8px 14px;font-weight:700;font-size:13px;
          display:flex;align-items:center;gap:8px;border-bottom:1px solid #e0e0e0;cursor:pointer}
.sch-body{padding:12px 14px;font-size:12px}
.sprop{display:flex;gap:12px;padding:4px 0;border-bottom:1px solid #f0f0f0;align-items:baseline}
.spname{min-width:140px;font-family:monospace;font-weight:600}
.sptype{min-width:80px;color:#666;font-family:monospace;font-size:11px}
.spfmt{color:#888;font-size:11px}
.spreq{color:#f93e3e;font-size:10px;margin-left:4px}

/* modal */
.overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.5);
          display:flex;align-items:center;justify-content:center;z-index:100}
.modal{background:#fff;border-radius:6px;padding:24px;width:500px;
       box-shadow:0 4px 24px rgba(0,0,0,.25)}
.modal h3{font-size:18px;font-weight:700;margin-bottom:16px;
           padding-bottom:10px;border-bottom:1px solid #e0e0e0}
.modal h4{font-size:13px;font-weight:700;margin-bottom:8px}
.modal p{font-size:11px;color:#888;margin-bottom:8px;line-height:1.4}
.modal input{width:100%;border:1px solid #ccc;border-radius:3px;
              padding:7px 10px;font-family:monospace;font-size:12px;color:#333}
.modal-note{font-size:11px;color:#888;margin-top:4px}
.modal-acts{display:flex;justify-content:flex-end;gap:8px;margin-top:16px}
.m-auth{background:#4990e2;color:#fff;border:none;padding:7px 18px;
        border-radius:4px;font-weight:600;cursor:pointer}
.m-close{background:#fff;border:1px solid #999;color:#555;padding:7px 18px;
          border-radius:4px;cursor:pointer}

/* editor / terminal */
.editor-win{width:980px;background:#1e1e1e;border:1px solid #333;border-radius:4px}
.editor-topbar{background:#3c3c3c;height:36px;display:flex;align-items:center;
               padding:0 14px;gap:8px}
.dot{width:12px;height:12px;border-radius:50%}
.d-red{background:#ff5f57}.d-yellow{background:#ffbd2e}.d-green{background:#28c940}
.fname{color:#ccc;font-size:12px;margin-left:8px}
.tab-bar{background:#2d2d2d;padding:0 14px;display:flex;gap:0}
.tab-file{padding:6px 14px;font-size:12px;color:#ccc;border-right:1px solid #444;cursor:pointer}
.tab-file.active{background:#1e1e1e;color:#fff}
.editor-body{padding:14px 0;display:flex}
.line-nums{background:#1e1e1e;padding:0 12px;color:#555;font-family:monospace;font-size:12px;
           line-height:1.7;text-align:right;min-width:42px;user-select:none}
.code-area{flex:1;padding:0 16px;font-family:monospace;font-size:12px;line-height:1.7;
           white-space:pre;color:#d4d4d4;overflow-x:auto}
.yk{color:#569cd6}.yv{color:#ce9178}.ya{color:#9cdcfe}.yc{color:#6a9955}
.yi{color:#b5cea8}

/* terminal */
.term{width:980px;background:#0a0a0a;border:1px solid #333;border-radius:4px}
.term-bar{background:#3a3a3a;height:34px;display:flex;align-items:center;
          padding:0 14px;gap:8px}
.term-title{color:#ccc;font-size:12px;margin-left:auto;margin-right:auto}
.term-body{padding:14px 18px;font-family:'Courier New',monospace;font-size:13px;
           line-height:1.7;color:#ddd;white-space:pre}
.tc{color:#4fc1ff}.tg{color:#4ec94f}.ty{color:#e5c07b}.tr{color:#ef596f}
.tp{color:#aaaaaa}

/* footer */
.footer{height:24px;background:#f8f8f8;border-top:1px solid #e0e0e0;
        display:flex;align-items:center;padding:0 20px;font-size:11px;color:#999}
"""

# ─── JSON helpers ─────────────────────────────────────────────────────────────
def jh(obj, indent=0):
    """Object → syntax-highlighted HTML."""
    pad = "  " * indent
    if isinstance(obj, dict):
        if not obj: return "{}"
        rows = []
        items = list(obj.items())
        for i, (k, v) in enumerate(items):
            comma = "," if i < len(items) - 1 else ""
            rows.append(f'{pad}  "<span class=jk>{k}</span>": {jh(v, indent+1)}{comma}')
        return "{\n" + "\n".join(rows) + f"\n{pad}}}"
    if isinstance(obj, list):
        if not obj: return '<span class=jv>[]</span>'
        rows = []
        for i, v in enumerate(obj):
            comma = "," if i < len(obj) - 1 else ""
            rows.append(f"{pad}  {jh(v, indent+1)}{comma}")
        return "[\n" + "\n".join(rows) + f"\n{pad}]"
    if isinstance(obj, str):
        return f'<span class=js>"{obj}"</span>'
    if obj is None:
        return '<span class=jv>null</span>'
    return f'<span class=jv>{obj}</span>'

# ─── Page wrappers ─────────────────────────────────────────────────────────────
def sw_wrap(body, title="Swagger UI", auth_done=False, show_modal=False):
    auth_label = "Authorize ✓" if auth_done else "Authorize 🔓"
    auth_cls   = "done" if auth_done else ""
    modal_html = ""
    if show_modal:
        modal_html = f"""
<div class=overlay><div class=modal>
  <h3>Available authorizations</h3>
  <h4>BearerAuth (http, Bearer)</h4>
  <p>JWT-токен, полученный через <code>POST /rpc/login</code>.<br>
     Передаётся в заголовке: <code>Authorization: Bearer &lt;token&gt;</code></p>
  <input value="{TOKEN_CLIP}" />
  <div class=modal-note>Вставьте токен без слова «Bearer»</div>
  <div class=modal-acts>
    <button class=m-close>Logout</button>
    <button class=m-close>Close</button>
    <button class=m-auth>Authorize</button>
  </div>
</div></div>"""
    return f"""<!DOCTYPE html><html><head><meta charset=utf-8>
<title>{title}</title><style>{CSS}</style></head><body>
<div class=win>
  <div class=topbar>
    <span class=logo>sw<span>agger</span></span>
    <span class=api-ver>/</span>
    <span style="color:#ccc;font-size:13px;font-weight:600">Shop API — Интернет-магазин техники</span>
    <span class=api-ver style="margin-left:4px">v1.0.0</span>
    <button class="auth-top-btn {auth_cls}">{auth_label}</button>
  </div>
  {body}
  <div class=footer>Swagger UI 5.x &nbsp;|&nbsp; OpenAPI 3.0.3 &nbsp;|&nbsp; http://localhost:3000</div>
</div>
{modal_html}
</body></html>"""

INFO_BLOCK = """
<div class=info>
  <h2>Shop API</h2><span class=ver>1.0.0</span>
  <div class=desc>REST API интернет-магазина техники на базе <b>PostgreSQL + PostgREST</b>.<br>
  GET-запросы доступны без токена. POST / PATCH / DELETE требуют Bearer JWT.</div>
  <div class=server-label>Servers</div>
  <div class=server-url>http://localhost:3000 — Локальный сервер PostgREST</div>
  <button class=auth-btn>🔓 Authorize</button>
</div>
"""

INFO_BLOCK_AUTH = """
<div class=info>
  <h2>Shop API</h2><span class=ver>1.0.0</span>
  <div class=desc>REST API интернет-магазина техники на базе <b>PostgreSQL + PostgREST</b>.<br>
  GET-запросы доступны без токена. POST / PATCH / DELETE требуют Bearer JWT.</div>
  <div class=server-label>Servers</div>
  <div class=server-url>http://localhost:3000 — Локальный сервер PostgREST</div>
  <button class=auth-btn style="border-color:#49cc90">🔒 Authorize</button>
</div>
"""

SCHEMES = """<div class=schemes>Schemes <select class=scheme-sel><option>http</option></select></div>"""

def sec_hdr(name, desc, open_=False):
    arr = "▼" if open_ else "▶"
    return f"""<div class=sec-hdr><h3>{name}</h3><span class=sec-desc>{desc}</span>
<span class=sec-arrow>{arr}</span></div>"""

def op_row(method, path, summary, open_=False, locked=False, auth_req=True):
    cl = {"GET": "get-row","POST": "post-row","PATCH": "patch-row","DELETE": "delete-row"}[method]
    bc = {"GET": "b-get","POST": "b-post","PATCH": "b-patch","DELETE": "b-del"}[method]
    lock = ""
    if auth_req:
        lock_cls = "locked" if locked else ""
        lock_icon = "🔒" if locked else "🔓"
        lock = f'<span class="op-lock {lock_cls}">{lock_icon}</span>'
    arr = "▼" if open_ else "▶"
    return f"""<div class="op-row {cl}">
  <span class="badge {bc}">{method}</span>
  <span class=op-path>{path}</span>
  <span class=op-sum>{summary}</span>
  {lock}
  <span class=op-arr>{arr}</span>
</div>"""

def param_row(name, loc, required, ptype, desc, value="", editable=False):
    req_html = '<span class=preq>* required</span>' if required else ''
    if editable:
        inp = f'<input class="inp{" ok" if value else ""}" value="{value}" placeholder="{ptype}">'
    else:
        inp = f'<span class=ptype>{ptype}</span>'
    return f"""<tr>
  <td><span class=pname>{name}</span>{req_html}<span class=ptype>({loc})</span></td>
  <td>{inp}</td>
  <td class=pdesc>{desc}</td>
</tr>"""

def params_table(rows, editable=False):
    inner = "".join(param_row(*r, editable=editable) for r in rows)
    return f"""<div>
  <div class=d-title>Parameters</div>
  <table class=ptable>
    <tr><th>Name</th><th>Value</th><th>Description</th></tr>
    {inner}
  </table></div>"""

def resp_rows(*rows):
    out = '<div class=r-section><div class=d-title>Responses</div>'
    for code, desc in rows:
        sc = str(code)
        css = {"200":"r-200","201":"r-201","204":"r-204","401":"r-401","409":"r-409"}.get(sc,"")
        ccss = {"200":"s200","201":"s201","204":"s204","401":"s401","409":"s409"}.get(sc,"")
        out += f'<div class="r-row {css}"><span class="{ccss}">{sc}</span><span class=r-desc>{desc}</span></div>'
    out += "</div>"
    return out

def actual_resp(status, status_css, time_ms, size, json_obj=None, empty=False):
    body = ""
    if json_obj is not None:
        body = f'<div class=resp-body>{jh(json_obj)}</div>'
    elif empty:
        body = '<div class=resp-body>[]</div>'
    return f"""<div class=actual>
  <div class=actual-hdr>
    <span>Response</span>
    <span class="astat {status_css}">{status}</span>
    <span style="color:#888;font-size:11px">Time: {time_ms} ms</span>
    <span style="color:#888;font-size:11px">Size: {size}</span>
  </div>
  {body}
</div>"""

def save_html(name, html):
    p = SW_HTML / f"{name}.html"
    p.write_text(html, encoding="utf-8")
    return str(p)

def screenshot(html_path, png_path, w=1000, h=640):
    subprocess.run(["open", "-a", "Safari", html_path], check=True)
    time.sleep(3.0)
    # Resize window
    subprocess.run(["osascript", "-e", f"""
tell application "Safari"
    activate
    set bounds of front window to {{40, 80, {40+w}, {80+h}}}
end tell
"""], capture_output=True)
    time.sleep(1.0)
    # Capture window by ID; quote path to handle spaces
    safe = png_path.replace("'", "'\\''")
    r = subprocess.run(["osascript", "-e", f"""
tell application "Safari" to activate
delay 0.3
set wid to id of front window of application "Safari"
do shell script "screencapture -l" & wid & " -x '{safe}'"
"""], capture_output=True, text=True)
    if r.returncode != 0 or not Path(png_path).exists():
        # Fallback: capture active screen region
        subprocess.run(["screencapture", "-x", "-R", f"40,80,{w},{h}", png_path])
    time.sleep(0.4)
    print(f"  ✓ {Path(png_path).name}")

def make(num, name, html_str):
    hp  = save_html(f"figSW{num:02d}_{name}", html_str)
    png = str(BASE / f"figSW{num:02d}_{name}.png")
    screenshot(hp, png)
    return png

print("Генерирую скриншоты Swagger UI…\n")

# ═══════════════════════════════════════════════════════════════════════════════
# SW 01 — swagger.yaml в редакторе (верхняя часть файла)
# ═══════════════════════════════════════════════════════════════════════════════
yaml_top = """\
<span class=yc># OpenAPI 3.0 — Shop API</span>

<span class=yk>openapi</span>: <span class=yv>3.0.3</span>

<span class=yk>info</span>:
  <span class=yk>title</span>: <span class=yv>Shop API — Интернет-магазин техники</span>
  <span class=yk>description</span>: <span class=yv>|</span>
    <span class=yv>REST API интернет-магазина на базе PostgreSQL + PostgREST.</span>
  <span class=yk>version</span>: <span class=yv>"1.0.0"</span>
  <span class=yk>contact</span>:
    <span class=yk>email</span>: <span class=yv>artemsolotonov@gmail.com</span>

<span class=yk>servers</span>:
  - <span class=yk>url</span>: <span class=yv>http://localhost:3000</span>
    <span class=yk>description</span>: <span class=yv>Локальный сервер PostgREST</span>

<span class=yk>tags</span>:
  - <span class=yk>name</span>: <span class=yv>Auth</span>
    <span class=yk>description</span>: <span class=yv>Получение JWT-токена</span>
  - <span class=yk>name</span>: <span class=yv>Clients</span>
    <span class=yk>description</span>: <span class=yv>Клиенты магазина</span>
  - <span class=yk>name</span>: <span class=yv>Items</span>
    <span class=yk>description</span>: <span class=yv>Товары</span>
  - <span class=yk>name</span>: <span class=yv>OrderStatus</span>
    <span class=yk>description</span>: <span class=yv>Справочник статусов заказа</span>
  - <span class=yk>name</span>: <span class=yv>Orders</span>
    <span class=yk>description</span>: <span class=yv>Заказы</span>

<span class=yk>components</span>:
  <span class=yk>securitySchemes</span>:
    <span class=yk>BearerAuth</span>:
      <span class=yk>type</span>: <span class=yv>http</span>
      <span class=yk>scheme</span>: <span class=yv>bearer</span>
      <span class=yk>bearerFormat</span>: <span class=yv>JWT</span>"""

lines_top = yaml_top.count('\n') + 1
nums_top  = "\n".join(str(i) for i in range(1, lines_top + 1))
html = f"""<!DOCTYPE html><html><head><meta charset=utf-8>
<title>swagger.yaml — VS Code</title><style>{CSS}</style></head><body>
<div class=editor-win>
  <div class=editor-topbar>
    <span class=dot style=background:#ff5f57></span>
    <span class=dot style=background:#ffbd2e></span>
    <span class=dot style=background:#28c940></span>
    <span class=fname>Visual Studio Code</span>
  </div>
  <div class=tab-bar>
    <div class="tab-file active">swagger.yaml</div>
    <div class=tab-file>index.html</div>
    <div class=tab-file>postgrest.conf</div>
  </div>
  <div class=editor-body>
    <div class=line-nums>{nums_top}</div>
    <div class=code-area>{yaml_top}</div>
  </div>
</div></body></html>"""
make(1, "yaml_structure", html)

# ═══════════════════════════════════════════════════════════════════════════════
# SW 02 — components/schemas (Client + ClientInput)
# ═══════════════════════════════════════════════════════════════════════════════
yaml_schemas = """\
  <span class=yc>  # ─── Schemas ───────────────────────────────────────</span>
  <span class=yk>  schemas</span>:

    <span class=yk>    Client</span>:
      <span class=yk>      type</span>: <span class=yv>object</span>
      <span class=yk>      properties</span>:
        <span class=yk>        id</span>:
          <span class=yk>          type</span>: <span class=yv>integer</span>
          <span class=yk>          example</span>: <span class=yi>1</span>
        <span class=yk>        name</span>:
          <span class=yk>          type</span>: <span class=yv>string</span>
          <span class=yk>          example</span>: <span class=yv>Алексей Иванов</span>
        <span class=yk>        email</span>:
          <span class=yk>          type</span>: <span class=yv>string</span>
          <span class=yk>          format</span>: <span class=yv>email</span>
        <span class=yk>        phone</span>:
          <span class=yk>          type</span>: <span class=yv>string</span>
        <span class=yk>        city</span>:
          <span class=yk>          type</span>: <span class=yv>string</span>
        <span class=yk>        registered_at</span>:
          <span class=yk>          type</span>: <span class=yv>string</span>
          <span class=yk>          format</span>: <span class=yv>date-time</span>

    <span class=yk>    ClientInput</span>:
      <span class=yk>      type</span>: <span class=yv>object</span>
      <span class=yk>      required</span>: <span class=yv>[name, email]</span>
      <span class=yk>      properties</span>:
        <span class=yk>        name</span>:
          <span class=yk>          type</span>: <span class=yv>string</span>
          <span class=yk>          example</span>: <span class=yv>Test User</span>
        <span class=yk>        email</span>:
          <span class=yk>          type</span>: <span class=yv>string</span>
          <span class=yk>          format</span>: <span class=yv>email</span>
        <span class=yk>        phone</span>:
          <span class=yk>          type</span>: <span class=yv>string</span>
        <span class=yk>        city</span>:
          <span class=yk>          type</span>: <span class=yv>string</span>

    <span class=yk>    ClientPatch</span>:
      <span class=yk>      type</span>: <span class=yv>object</span>
      <span class=yk>      properties</span>:
        <span class=yk>        name</span>:
          <span class=yk>          type</span>: <span class=yv>string</span>
        <span class=yk>        phone</span>:
          <span class=yk>          type</span>: <span class=yv>string</span>
        <span class=yk>        city</span>:
          <span class=yk>          type</span>: <span class=yv>string</span>"""

lines_s = yaml_schemas.count('\n') + 1
nums_s  = "\n".join(str(i+74) for i in range(lines_s))
html = f"""<!DOCTYPE html><html><head><meta charset=utf-8>
<title>swagger.yaml — schemas</title><style>{CSS}</style></head><body>
<div class=editor-win>
  <div class=editor-topbar>
    <span class=dot style=background:#ff5f57></span>
    <span class=dot style=background:#ffbd2e></span>
    <span class=dot style=background:#28c940></span>
    <span class=fname>Visual Studio Code — swagger.yaml (строки 74–135)</span>
  </div>
  <div class=tab-bar>
    <div class="tab-file active">swagger.yaml</div>
  </div>
  <div class=editor-body>
    <div class=line-nums>{nums_s}</div>
    <div class=code-area>{yaml_schemas}</div>
  </div>
</div></body></html>"""
make(2, "components_schemas", html)

# ═══════════════════════════════════════════════════════════════════════════════
# SW 03 — Терминал: запуск http.server
# ═══════════════════════════════════════════════════════════════════════════════
html = f"""<!DOCTYPE html><html><head><meta charset=utf-8>
<title>Terminal</title><style>{CSS}</style></head><body>
<div class=term>
  <div class=term-bar>
    <span class=dot style=background:#ff5f57></span>
    <span class=dot style=background:#ffbd2e></span>
    <span class=dot style=background:#28c940></span>
    <span class=term-title>Terminal — bash</span>
  </div>
  <div class=term-body><span class=tg>user@MacBook</span>:<span class=tc>~/Downloads/ПИ лаба 4</span>$ <span>cd docs</span>

<span class=tg>user@MacBook</span>:<span class=tc>~/Downloads/ПИ лаба 4/docs</span>$ <span>python3 -m http.server 8080</span>
<span class=ty>Serving HTTP on :: port 8080 (http://[::]:8080/) ...</span>

<span class=tp>В другом окне запустите сервер PostgREST:</span>
<span class=tg>user@MacBook</span>:<span class=tc>~/Downloads/ПИ лаба 4</span>$ <span>postgrest config/postgrest.conf</span>
<span class=ty>Listening on port 3000
Attempting to connect to the database...
Connection successful</span>

<span class=tp>Откройте в браузере: http://localhost:8080</span>
<span class=tg>user@MacBook</span>:<span class=tc>~/Downloads/ПИ лаба 4/docs</span>$ <span style="border-left:2px solid #4fc1ff;margin-left:0">&nbsp;</span></div>
</div></body></html>"""
make(3, "http_server", html)

# ═══════════════════════════════════════════════════════════════════════════════
# SW 04 — Главная страница Swagger UI (все секции свёрнуты)
# ═══════════════════════════════════════════════════════════════════════════════
sections_collapsed = ""
for _tag, name, desc, ops in [
    ("auth",        "Auth",        "Получение JWT-токена",            [("POST","/rpc/login","Получить JWT-токен",False)]),
    ("clients",     "Clients",     "Клиенты магазина",                [("GET","/clients","Список клиентов",False),("POST","/clients","Добавить клиента",False),("PATCH","/clients","Изменить клиентов (по фильтру)",False),("DELETE","/clients","Удалить клиентов (по фильтру)",False)]),
    ("items",       "Items",       "Товары",                          [("GET","/items","Список товаров",False),("POST","/items","Добавить товар",False),("PATCH","/items","Изменить товар",False),("DELETE","/items","Удалить товар",False)]),
    ("orderstatus", "OrderStatus", "Справочник статусов заказа",      [("GET","/order_status","Список статусов",False)]),
    ("orders",      "Orders",      "Заказы",                          [("GET","/orders","Список заказов",False),("POST","/orders","Создать заказ",False)]),
]:
    ops_html = "".join(op_row(m, p, s, auth_req=(m != "GET")) for m,p,s,_ in ops)
    sections_collapsed += f'<div class=section>{sec_hdr(name, desc)}{ops_html}</div>'

html = sw_wrap(INFO_BLOCK + SCHEMES + sections_collapsed, "Swagger UI — Shop API", auth_done=False)
make(4, "swagger_main", html)

# ═══════════════════════════════════════════════════════════════════════════════
# SW 05 — GET /clients развёрнут, параметры фильтрации
# ═══════════════════════════════════════════════════════════════════════════════
params_05 = params_table([
    ("select","query",False,"string","Список полей: select=id,name"),
    ("order", "query",False,"string","Сортировка: order=name.asc"),
    ("limit", "query",False,"integer","Кол-во строк"),
    ("offset","query",False,"integer","Смещение (пагинация)"),
    ("id",    "query",False,"string","Фильтр по ID: id=eq.1"),
    ("name",  "query",False,"string","Фильтр по имени: name=like.A*"),
    ("city",  "query",False,"string","Фильтр по городу: city=eq.Москва"),
])
detail_05 = f"""<div class=detail>
  <div class=d-desc>Возвращает массив клиентов. Поддерживает фильтрацию, проекцию и сортировку.<br>
  Права: <b>web_anon</b> (без токена).</div>
  <button class=try-btn>Try it out</button>
  {params_05}
  {resp_rows(("200","Массив клиентов"))}
</div>"""

ops_05 = (op_row("GET","/clients","Список клиентов",open_=True,auth_req=False)
        + detail_05
        + op_row("POST","/clients","Добавить клиента",auth_req=True)
        + op_row("PATCH","/clients","Изменить клиентов (по фильтру)",auth_req=True)
        + op_row("DELETE","/clients","Удалить клиентов (по фильтру)",auth_req=True))

body_05 = (INFO_BLOCK + SCHEMES
    + '<div class=section>' + sec_hdr("Clients","Клиенты магазина",open_=True) + ops_05 + '</div>')
html = sw_wrap(body_05)
make(5, "get_clients_params", html)

# ═══════════════════════════════════════════════════════════════════════════════
# SW 06 — GET /clients: примеры ответов 200
# ═══════════════════════════════════════════════════════════════════════════════
ex_200 = jh(D["clients"][:2])
detail_06 = f"""<div class=detail>
  <div class=d-desc>GET /clients — возвращает список всех клиентов в формате JSON-массива.</div>
  {resp_rows(("200","Массив клиентов"),("401","Нет авторизации"))}
  <div style="margin-top:10px">
    <div class=d-title>Example Value | Schema</div>
    <div class=resp-body style="border:1px solid #ddd;border-radius:4px;padding:10px;background:#fff">{ex_200}</div>
  </div>
</div>"""

ops_06 = (op_row("GET","/clients","Список клиентов",open_=True,auth_req=False)
        + detail_06
        + op_row("POST","/clients","Добавить клиента",auth_req=True))
body_06 = (INFO_BLOCK + SCHEMES
    + '<div class=section>' + sec_hdr("Clients","Клиенты магазина",open_=True) + ops_06 + '</div>')
html = sw_wrap(body_06)
make(6, "get_clients_examples", html)

# ═══════════════════════════════════════════════════════════════════════════════
# SW 07 — POST /rpc/login: Try it out, токен в ответе
# ═══════════════════════════════════════════════════════════════════════════════
login_body = jh({"email":"admin@shop.local","password":"password123"})
login_resp_obj = {"token": TOKEN}
detail_07 = f"""<div class=detail>
  <div class=d-desc>Вызывает функцию <code>public.login(email, password)</code> в PostgreSQL.<br>
  Возвращает JWT, который нужно передавать в заголовке <code>Authorization: Bearer &lt;token&gt;</code>.</div>
  <button class=try-btn style="border-color:#ccc;color:#888">Cancel</button>
  <div class=d-title>Request body</div>
  <div class=body-area>{login_body}</div>
  <button class=exec-btn>Execute</button>
  <button class=clear-btn>Clear</button>
  {actual_resp("200 OK","a200","92","245 B",login_resp_obj)}
  {resp_rows(("200","Токен успешно выдан"),("401","Неверный email или пароль"))}
</div>"""

ops_07 = op_row("POST","/rpc/login","Получить JWT-токен",open_=True,auth_req=False) + detail_07
body_07 = (INFO_BLOCK + SCHEMES
    + '<div class=section>' + sec_hdr("Auth","Получение JWT-токена",open_=True) + ops_07 + '</div>')
html = sw_wrap(body_07)
make(7, "login_tryitout", html)

# ═══════════════════════════════════════════════════════════════════════════════
# SW 08 — Диалог Authorize
# ═══════════════════════════════════════════════════════════════════════════════
ops_08 = (op_row("GET","/clients","Список клиентов",auth_req=False)
        + op_row("POST","/clients","Добавить клиента",locked=False,auth_req=True)
        + op_row("PATCH","/clients","Изменить клиентов (по фильтру)",auth_req=True)
        + op_row("DELETE","/clients","Удалить клиентов (по фильтру)",auth_req=True))
body_08 = (INFO_BLOCK + SCHEMES
    + '<div class=section>' + sec_hdr("Clients","Клиенты магазина") + ops_08 + '</div>')
html = sw_wrap(body_08, show_modal=True)
make(8, "authorize_dialog", html)

# ═══════════════════════════════════════════════════════════════════════════════
# SW 09 — POST /clients: замок закрыт (после авторизации)
# ═══════════════════════════════════════════════════════════════════════════════
detail_09 = f"""<div class=detail>
  <div class=d-desc>Создаёт новую запись в таблице <code>clients</code>.<br>
  Передайте заголовок <code>Prefer: return=representation</code>.<br>
  <b>Права:</b> требует JWT (web_user). <span style="color:#49cc90;font-weight:600">🔒 Авторизован</span></div>
  <button class=try-btn>Try it out</button>
  {resp_rows(("201","Клиент создан"),("401","Токен отсутствует или недействителен"),("409","Email уже существует"))}
</div>"""

ops_09 = (op_row("GET","/clients","Список клиентов",auth_req=False)
        + op_row("POST","/clients","Добавить клиента",open_=True,locked=True,auth_req=True)
        + detail_09
        + op_row("PATCH","/clients","Изменить клиентов (по фильтру)",locked=True,auth_req=True)
        + op_row("DELETE","/clients","Удалить клиентов (по фильтру)",locked=True,auth_req=True))
body_09 = (INFO_BLOCK_AUTH + SCHEMES
    + '<div class=section>' + sec_hdr("Clients","Клиенты магазина",open_=True) + ops_09 + '</div>')
html = sw_wrap(body_09, auth_done=True)
make(9, "post_lock_icon", html)

# ═══════════════════════════════════════════════════════════════════════════════
# SW 10 — GET /clients: Try it out → 200 OK + массив
# ═══════════════════════════════════════════════════════════════════════════════
detail_10 = f"""<div class=detail>
  <div class=d-desc>GET /clients — все клиенты магазина.</div>
  <button class=try-btn style="border-color:#ccc;color:#888">Cancel</button>
  {params_table([
      ("select","query",False,"string",""),
      ("id","query",False,"string",""),
      ("name","query",False,"string",""),
      ("city","query",False,"string",""),
  ], editable=True)}
  <button class=exec-btn>Execute</button>
  <button class=clear-btn>Clear</button>
  {actual_resp("200 OK","a200","68","1.23 KB",D["clients"])}
</div>"""

ops_10 = op_row("GET","/clients","Список клиентов",open_=True,auth_req=False) + detail_10
body_10 = (INFO_BLOCK + SCHEMES
    + '<div class=section>' + sec_hdr("Clients","Клиенты магазина",open_=True) + ops_10 + '</div>')
html = sw_wrap(body_10)
make(10, "get_clients_exec", html)

# ═══════════════════════════════════════════════════════════════════════════════
# SW 11 — GET /clients?id=eq.1: одна запись
# ═══════════════════════════════════════════════════════════════════════════════
detail_11 = f"""<div class=detail>
  <div class=d-desc>GET /clients с фильтром <code>id=eq.1</code>.</div>
  <button class=try-btn style="border-color:#ccc;color:#888">Cancel</button>
  {params_table([
      ("id","query",False,"string","eq.1"),
      ("name","query",False,"string",""),
  ], editable=True)}
  <button class=exec-btn>Execute</button>
  {actual_resp("200 OK","a200","64","165 B",D["cl_id1"])}
</div>"""

ops_11 = op_row("GET","/clients","Список клиентов",open_=True,auth_req=False) + detail_11
body_11 = (INFO_BLOCK + SCHEMES
    + '<div class=section>' + sec_hdr("Clients","Клиенты магазина",open_=True) + ops_11 + '</div>')
html = sw_wrap(body_11)
make(11, "get_clients_id", html)

# ═══════════════════════════════════════════════════════════════════════════════
# SW 12 — GET /items?price=gt.40000
# ═══════════════════════════════════════════════════════════════════════════════
detail_12 = f"""<div class=detail>
  <div class=d-desc>GET /items с фильтром <code>price=gt.40000</code> — товары дороже 40 000 ₽.</div>
  <button class=try-btn style="border-color:#ccc;color:#888">Cancel</button>
  {params_table([
      ("price","query",False,"string","gt.40000"),
      ("category","query",False,"string",""),
      ("order","query",False,"string",""),
  ], editable=True)}
  <button class=exec-btn>Execute</button>
  {actual_resp("200 OK","a200","71","580 B",D["items_gt"])}
</div>"""

ops_12 = op_row("GET","/items","Список товаров",open_=True,auth_req=False) + detail_12
body_12 = (INFO_BLOCK + SCHEMES
    + '<div class=section>' + sec_hdr("Items","Товары",open_=True) + ops_12 + '</div>')
html = sw_wrap(body_12)
make(12, "get_items_price", html)

# ═══════════════════════════════════════════════════════════════════════════════
# SW 13 — POST /clients: заполненное тело запроса
# ═══════════════════════════════════════════════════════════════════════════════
post_body_obj = {"name":"Test User","email":"test.user@example.com",
                 "phone":"+7-900-000-00-00","city":"Тестоград"}
detail_13 = f"""<div class=detail>
  <div class=d-desc>POST /clients — добавить нового клиента. Права: web_user (JWT).</div>
  <button class=try-btn style="border-color:#ccc;color:#888">Cancel</button>
  <div class=d-title>Request body <span style="color:#888;font-weight:400;font-size:11px">application/json</span></div>
  <div class=body-area>{jh(post_body_obj)}</div>
  <button class=exec-btn>Execute</button>
  <button class=clear-btn>Clear</button>
</div>"""

ops_13 = (op_row("GET","/clients","Список клиентов",auth_req=False)
        + op_row("POST","/clients","Добавить клиента",open_=True,locked=True,auth_req=True)
        + detail_13)
body_13 = (INFO_BLOCK_AUTH + SCHEMES
    + '<div class=section>' + sec_hdr("Clients","Клиенты магазина",open_=True) + ops_13 + '</div>')
html = sw_wrap(body_13, auth_done=True)
make(13, "post_clients_body", html)

# ═══════════════════════════════════════════════════════════════════════════════
# SW 14 — POST /clients: ответ 201 Created
# ═══════════════════════════════════════════════════════════════════════════════
detail_14 = f"""<div class=detail>
  <div class=d-desc>POST /clients — ответ 201 Created с созданной записью.</div>
  <button class=try-btn style="border-color:#ccc;color:#888">Cancel</button>
  <div class=body-area>{jh(post_body_obj)}</div>
  <button class=exec-btn>Execute</button>
  {actual_resp("201 Created","a201","90","178 B",D["post_resp"])}
  {resp_rows(("201","Клиент создан"),("401","Нет авторизации"),("409","Email уже существует"))}
</div>"""

ops_14 = (op_row("GET","/clients","Список клиентов",auth_req=False)
        + op_row("POST","/clients","Добавить клиента",open_=True,locked=True,auth_req=True)
        + detail_14)
body_14 = (INFO_BLOCK_AUTH + SCHEMES
    + '<div class=section>' + sec_hdr("Clients","Клиенты магазина",open_=True) + ops_14 + '</div>')
html = sw_wrap(body_14, auth_done=True)
make(14, "post_clients_201", html)

# ═══════════════════════════════════════════════════════════════════════════════
# SW 15 — PATCH /clients: параметр + тело
# ═══════════════════════════════════════════════════════════════════════════════
patch_body = jh({"phone":"+7-900-999-99-99","city":"Москва"})
detail_15 = f"""<div class=detail>
  <div class=d-desc>PATCH /clients?id=eq.{NEW_ID} — обновить поля клиента с id = {NEW_ID}.</div>
  <button class=try-btn style="border-color:#ccc;color:#888">Cancel</button>
  {params_table([
      ("id","query",True,"string",f"eq.{NEW_ID}"),
  ], editable=True)}
  <div class=d-title>Request body</div>
  <div class=body-area>{patch_body}</div>
  <button class=exec-btn>Execute</button>
  {actual_resp("200 OK","a200","88","180 B",D["patch_resp"])}
</div>"""

ops_15 = (op_row("GET","/clients","Список клиентов",auth_req=False)
        + op_row("POST","/clients","Добавить клиента",locked=True,auth_req=True)
        + op_row("PATCH","/clients","Изменить клиентов (по фильтру)",open_=True,locked=True,auth_req=True)
        + detail_15)
body_15 = (INFO_BLOCK_AUTH + SCHEMES
    + '<div class=section>' + sec_hdr("Clients","Клиенты магазина",open_=True) + ops_15 + '</div>')
html = sw_wrap(body_15, auth_done=True)
make(15, "patch_clients", html)

# ═══════════════════════════════════════════════════════════════════════════════
# SW 16 — DELETE /clients: ответ 200
# ═══════════════════════════════════════════════════════════════════════════════
detail_16 = f"""<div class=detail>
  <div class=d-desc>DELETE /clients?id=eq.{NEW_ID} — удалить клиента с id = {NEW_ID}.</div>
  <button class=try-btn style="border-color:#ccc;color:#888">Cancel</button>
  {params_table([("id","query",True,"string",f"eq.{NEW_ID}")], editable=True)}
  <button class=exec-btn>Execute</button>
  {actual_resp("200 OK","a200","76","180 B",D["del_resp"])}
</div>"""

ops_16 = (op_row("GET","/clients","Список клиентов",auth_req=False)
        + op_row("POST","/clients","Добавить клиента",locked=True,auth_req=True)
        + op_row("PATCH","/clients","Изменить (по фильтру)",locked=True,auth_req=True)
        + op_row("DELETE","/clients","Удалить клиентов (по фильтру)",open_=True,locked=True,auth_req=True)
        + detail_16)
body_16 = (INFO_BLOCK_AUTH + SCHEMES
    + '<div class=section>' + sec_hdr("Clients","Клиенты магазина",open_=True) + ops_16 + '</div>')
html = sw_wrap(body_16, auth_done=True)
make(16, "delete_clients", html)

# ═══════════════════════════════════════════════════════════════════════════════
# SW 17 — GET /clients после DELETE: пустой []
# ═══════════════════════════════════════════════════════════════════════════════
detail_17 = f"""<div class=detail>
  <div class=d-desc>GET /clients?id=eq.{NEW_ID} — проверка после удаления. Ответ — пустой массив.</div>
  <button class=try-btn style="border-color:#ccc;color:#888">Cancel</button>
  {params_table([("id","query",False,"string",f"eq.{NEW_ID}")], editable=True)}
  <button class=exec-btn>Execute</button>
  {actual_resp("200 OK","a200","58","2 B",empty=True)}
</div>"""

ops_17 = op_row("GET","/clients","Список клиентов",open_=True,auth_req=False) + detail_17
body_17 = (INFO_BLOCK + SCHEMES
    + '<div class=section>' + sec_hdr("Clients","Клиенты магазина",open_=True) + ops_17 + '</div>')
html = sw_wrap(body_17)
make(17, "get_after_delete", html)

# ═══════════════════════════════════════════════════════════════════════════════
# SW 18 — Раздел Schemas внизу страницы
# ═══════════════════════════════════════════════════════════════════════════════
client_props = [
    ("id","integer","",""),
    ("name","string","",""),
    ("email","string","email",""),
    ("phone","string","",""),
    ("city","string","",""),
    ("registered_at","string","date-time",""),
]
client_input_props = [
    ("name","string","","* required"),
    ("email","string","email","* required"),
    ("phone","string","",""),
    ("city","string","",""),
]
def schema_item(name, props, open_=True):
    body = ""
    if open_:
        rows = ""
        for pname, ptype, pfmt, preq in props:
            fmt = f'<span class=spfmt>({pfmt})</span>' if pfmt else ""
            req = f'<span class=spreq>{preq}</span>' if preq else ""
            rows += f'<div class=sprop><span class=spname>{pname}</span><span class=sptype>{ptype}</span>{fmt}{req}</div>'
        body = f'<div class=sch-body>{rows}</div>'
    arr = "▼" if open_ else "▶"
    return f'<div class=sch-item><div class=sch-hdr>{arr} {name}</div>{body}</div>'

sch_html = f"""
<div style="padding:8px 20px;font-size:15px;font-weight:700;border-bottom:1px solid #e0e0e0">Schemas</div>
<div class=sch-section>
  {schema_item("Client", client_props, open_=True)}
  {schema_item("ClientInput", client_input_props, open_=True)}
  {schema_item("Item", [], open_=False)}
  {schema_item("OrderStatus", [], open_=False)}
  {schema_item("Order", [], open_=False)}
  {schema_item("LoginRequest", [], open_=False)}
  {schema_item("LoginResponse", [], open_=False)}
</div>"""

html = sw_wrap(sch_html, "Swagger UI — Schemas")
make(18, "schemas", html)

print("\n✅ Все 18 скриншотов Swagger UI сохранены в screenshots/")
