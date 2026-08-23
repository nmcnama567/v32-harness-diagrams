#!/usr/bin/env python3
# Crewline V3.2 receptacle diagram generator.
# Per panel receptacle: internal Y-split pigtail diagram + mating-face pinout diagram.
# Data: ../data/*.json (one file per receptacle + meta.json). Stdlib only.
# Cavity positions: TE STEP models (c-hd34-*-3d.stp). Cavity IDs: TE 0425-013-1800 rev D /
# 0425-014-2400 rev H (rear/grommet PIN-insert views). Wire tables: docs/internal-wiring-definition.md
import json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "output")

with open(os.path.join(DATA, "meta.json")) as f:
    META = json.load(f)
DATE = META["date"]
PROJECT = META["project"]
WIRE_TABLE = f'{META["wire_table"]} ({META["wire_table_date"]})'

RECEPTACLES = []
for fn in sorted(os.listdir(DATA)):
    if fn.endswith(".json") and fn != "meta.json":
        with open(os.path.join(DATA, fn)) as f:
            RECEPTACLES.append(json.load(f))
RECEPTACLES.sort(key=lambda rc: rc["order"])

# ---------------------------------------------------------------- palette
C = {
    "PWR":    "#c62828",   # +13V feeds, BAT+
    "GND":    "#212121",   # grounds / returns
    "CANH":   "#c8901c",   # CAN high
    "CANL":   "#2e7d32",   # CAN low
    "SIG":    "#757575",   # generic signal
    "SAFE":   "#7b1fa2",   # e-stop loop / RX trio
    "SPARE":  "#b5b5b5",
    "ink":    "#1a1a1a",
    "muted":  "#8a8a8a",
    "line":   "#c9c9c9",
    "paper":  "#ffffff",
    "band":   "#f2f2f0",
}
LEGEND_NAMES = {"PWR": "power +13 V / BAT+", "GND": "ground / return", "CANH": "CAN H",
                "CANL": "CAN L", "SIG": "signal", "SAFE": "safety chain", "SPARE": "spare (plugged)"}

FONT = "Helvetica Neue, Helvetica, Arial, sans-serif"
MONO = "Menlo, Consolas, monospace"

# cavity display radii (mm) by contact size: (outer, inner pin)
CAVR = {12: (2.667, 1.19), 16: (2.159, 0.79), 20: (1.60, 0.51)}

# ---------------------------------------------------------------- svg helpers
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

class SVG:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.b = []
    def add(self, s): self.b.append(s)
    def line(self, x1,y1,x2,y2, stroke, w=1.5, dash=None, cap="round"):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{w}" stroke-linecap="{cap}"{d}/>')
    def path(self, d, stroke, w=1.5, fill="none", dash=None):
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<path d="{d}" stroke="{stroke}" stroke-width="{w}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round"{dd}/>')
    def circle(self, cx,cy,r, stroke="none", fill="none", w=1.5):
        self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" stroke="{stroke}" fill="{fill}" stroke-width="{w}"/>')
    def rect(self, x,y,w,h, stroke="none", fill="none", rx=0, sw=1.5):
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" stroke="{stroke}" fill="{fill}" stroke-width="{sw}"/>')
    def text(self, x,y, s, size=12, fill=C["ink"], anchor="start", weight="normal", family=FONT, spacing=None):
        sp = f' letter-spacing="{spacing}"' if spacing else ""
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}"{sp}>{esc(s)}</text>')
    def out(self, fn):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}">'
                f'<rect x="0" y="0" width="{self.w}" height="{self.h}" fill="{C["paper"]}"/>')
        with open(fn, "w") as f:
            f.write(head + "".join(self.b) + "</svg>")

def title_block(s, W, title, sub, right1, right2):
    s.rect(0, 0, W, 78, fill=C["band"])
    s.line(0, 78, W, 78, C["line"], 1)
    s.text(28, 34, title, 21, weight="bold", spacing="0.5")
    s.text(28, 58, sub, 12.5, fill="#555")
    s.text(W-28, 34, right1, 13, anchor="end", weight="bold", fill="#444")
    s.text(W-28, 56, right2, 12, anchor="end", fill="#666")

def seg_point_dist(px, py, ax, ay, bx, by):
    dx, dy = bx-ax, by-ay
    L2 = dx*dx+dy*dy
    if L2 == 0: return math.hypot(px-ax, py-ay)
    t = max(0, min(1, ((px-ax)*dx+(py-ay)*dy)/L2))
    return math.hypot(px-(ax+t*dx), py-(ay+t*dy))

def txt_w(s, fs):  # crude width estimate (Helvetica avg 0.54em, bold-ish margin)
    return len(s) * fs * 0.56

# ---------------------------------------------------------------- shared face/rear view
def draw_view(s, cx, cy, R, cavs, scale, mirror=False, spares=None):
    s.circle(cx, cy, R+14, stroke="#9a9a9a", fill="#fbfbfa", w=2.2)
    s.circle(cx, cy, R+2, stroke="#c0c0c0", fill="#ffffff", w=1.2)
    for cid, (size, x, y) in cavs.items():
        px = cx + (-x if mirror else x) * scale
        py = cy - y * scale
        ro, ri = CAVR[size][0]*scale, CAVR[size][1]*scale
        is_spare = spares and cid in spares
        col = C["muted"] if is_spare else C["ink"]
        fill = "#f1f1ee" if is_spare else "#ffffff"
        s.circle(px, py, ro, stroke=col, fill=fill, w=1.7)
        s.circle(px, py, ri, stroke="#c9c9c9" if is_spare else "#999", fill="none", w=1.0)
        if len(cid) == 1:
            fs = min(14.5, ro*0.85)
        else:
            fs = min(12.5, ro*0.70)
        s.text(px, py + fs*0.36, cid, fs, fill=col, anchor="middle", weight="bold")

# ---------------------------------------------------------------- internal wiring
def gen_internal(rc):
    wires = rc["wires"]
    powers  = [w for w in wires if w[4]=="power"]
    signals = [w for w in wires if w[4]=="signal"]
    p_h = list(dict.fromkeys(w[5] for w in powers))
    s_h = list(dict.fromkeys(w[5] for w in signals))
    powers  = sorted(powers,  key=lambda w: (p_h.index(w[5]), w[6]))
    signals = sorted(signals, key=lambda w: (s_h.index(w[5]), w[6]))

    LANE = 30
    HDR = 58            # block header height above first wire
    def footer_h(h):
        meta = rc["housings"][h]
        n = (1 if meta.get("spare") else 0) + (1 if meta.get("note") else 0) + (1 if meta.get("note2") else 0)
        return 16 + 13*n + 4

    top = 132
    lanes, order = {}, []
    y = top + 30
    bounds = {}
    def place(hlist, wlist, y):
        for hi, h in enumerate(hlist):
            hw = [w for w in wlist if w[5]==h]
            if hi > 0:
                y += footer_h(hlist[hi-1]) + HDR - 10
            y0 = y
            for w in hw:
                lanes[w[0]] = y; order.append(w); y += LANE
            bounds[h] = (y0, y-LANE)
        return y
    y = place(p_h, powers, y)
    y_pow_end = y - LANE
    y += footer_h(p_h[-1]) + HDR + 6      # leg gap accounts for block footer+header
    y = place(s_h, signals, y)
    y += footer_h(s_h[-1]) - LANE + 8
    y_sp0 = y + 26
    n_sp = len(rc["spare_cavs"])
    content_bottom = y_sp0 + n_sp*24 + 10

    X_TAG, TAG_W = 372, 52
    X_W0 = X_TAG + TAG_W
    X_TR1, X_FORK, X_DIV1 = 596, 640, 745
    X_LBL = 770
    X_HOUS, HOUS_W = 1330, 262
    W = X_HOUS + HOUS_W + 30

    # rear view + legend column height
    scale = 7.2 if rc["shell"].startswith("HD34-24") else 8.4
    Rmm = max(math.hypot(x,yy)+CAVR[sz][0] for sz,x,yy in rc["cavities"].values())
    R = Rmm*scale
    cxv, cyv = 178, top + R + 46
    used_classes = list(dict.fromkeys(w[3] for w in wires))
    if rc["spare_cavs"]: used_classes.append("SPARE")
    legend_bottom = (cyv + R + 62) + 20 + 19*len(used_classes)
    H = int(max(content_bottom, legend_bottom) + 96)

    s = SVG(W, H)
    title_block(s, W,
        f'{rc["name"]} — {rc["shell"]} · internal Y-split pigtail',
        f'{rc["arr"]} · cavity IDs per {rc["tedoc"]}',
        PROJECT, DATE)

    s.text(cxv, top + 16, "REAR VIEW (wire side)", 12, anchor="middle", weight="bold", fill="#444")
    draw_view(s, cxv, cyv, R, rc["cavities"], scale, mirror=False, spares=rc["spare_cavs"])
    s.text(cxv, cyv + R + 34, "as seen from inside enclosure", 10.5, anchor="middle", fill=C["muted"])
    ly = cyv + R + 62
    s.text(64, ly, "LEGEND", 11, weight="bold", fill="#444", spacing="1"); ly += 20
    for cl in used_classes:
        s.line(64, ly-4, 96, ly-4, C[cl], 3)
        s.text(104, ly, LEGEND_NAMES[cl], 11, fill="#333"); ly += 19

    # trunk geometry
    allw = order
    n = len(allw)
    tp = 13
    trunk_c = (lanes[allw[0][0]] + lanes[allw[-1][0]])/2
    ty = {w[0]: trunk_c + (i-(n-1)/2)*tp for i, w in enumerate(allw)}
    trunk_top = trunk_c - (n-1)/2*tp
    trunk_bot = trunk_c + (n-1)/2*tp

    # clamp tick + caption in guaranteed pocket above trunk_top between X_TR1..X_FORK
    s.line(X_FORK-4, trunk_top-6, X_FORK-4, trunk_bot+6, "#444", 2.2)
    s.line(X_FORK+1, trunk_top-6, X_FORK+1, trunk_bot+6, "#444", 2.2)
    s.text((X_TR1+X_FORK)/2, trunk_top-16, "Y-fork", 11.5, anchor="middle", weight="bold", fill="#444")

    twmap = {}
    for w in allw:
        cav, circ, awg, cl, leg, hous, pin, note = w
        yl, yt = lanes[cav], ty[cav]
        col = C[cl]
        s.rect(X_TAG, yl-11, TAG_W, 22, stroke="#888", fill="#fff", rx=4, sw=1.2)
        s.text(X_TAG+TAG_W/2, yl+4, cav, 12, anchor="middle", weight="bold", family=MONO)
        d = (f'M {X_W0} {yl} C 470 {yl} 510 {yt} {X_TR1} {yt} '
             f'L {X_FORK} {yt} C 685 {yt} 705 {yl} {X_DIV1} {yl} ')
        if note.startswith("tw"):
            twmap.setdefault(hous, []).append(w)
            d += f'L {X_LBL+228} {yl}'
        else:
            d += f'L {X_HOUS} {yl}'
        s.path(d, col, 2.0)
        awg_disp = awg.replace(" tw", "") + " AWG" + (" (tw)" if "tw" in awg else "")
        s.text(X_LBL, yl-6, f'{circ} · {awg_disp}', 11.5,
               fill=("#8a1010" if "ALWAYS-ON" in circ else "#333"))

    for hous, tws in twmap.items():
        tws = sorted(tws, key=lambda w: w[6])
        for i in range(0, len(tws)-1, 2):
            wa, wb = tws[i], tws[i+1]
            y1, y2 = lanes[wa[0]], lanes[wb[0]]
            x0, x3 = X_LBL+228, X_HOUS
            seg = (x3-x0)/3
            pa = f'M {x0} {y1} C {x0+seg*0.5} {y1} {x0+seg*0.5} {y2} {x0+seg} {y2} C {x0+seg*1.5} {y2} {x0+seg*1.5} {y1} {x0+seg*2} {y1} L {x3} {y1}'
            pb = f'M {x0} {y2} C {x0+seg*0.5} {y2} {x0+seg*0.5} {y1} {x0+seg} {y1} C {x0+seg*1.5} {y1} {x0+seg*1.5} {y2} {x0+seg*2} {y2} L {x3} {y2}'
            s.path(pa, C[wa[3]], 2.0)
            s.path(pb, C[wb[3]], 2.0)
            s.text(x0+seg, (y1+y2)/2+3.5, "tw", 9, anchor="middle", fill=C["muted"])

    s.text(X_DIV1+6, lanes[powers[0][0]] - 26, "POWER LEG", 12.5, weight="bold", fill="#7a1414", spacing="1")
    s.text(X_DIV1+6, lanes[signals[0][0]] - 26, "SIGNAL LEG", 12.5, weight="bold", fill="#3a3a6a", spacing="1")

    for h in p_h + s_h:
        meta = rc["housings"][h]
        y0, y1 = bounds[h]
        by0, by1 = y0 - HDR, y1 + footer_h(h)
        s.rect(X_HOUS, by0, HOUS_W, by1-by0, stroke="#555", fill="#fafaf8", rx=8, sw=1.8)
        s.text(X_HOUS+12, by0+22, meta["title"], 12.5, weight="bold")
        s.text(X_HOUS+12, by0+40, meta["sub"], 10, fill="#666")
        ey = y1 + 26
        for e in ([meta["spare"]] if meta.get("spare") else []) + ([meta["note"]] if meta.get("note") else []) + ([meta["note2"]] if meta.get("note2") else []):
            s.text(X_HOUS+12, ey, e, 9.5, fill=("#8a1010" if "live" in e else C["muted"]))
            ey += 13
        for w in allw:
            if w[5]==h:
                s.line(X_HOUS-2, lanes[w[0]], X_HOUS+7, lanes[w[0]], "#555", 2)
                s.text(X_HOUS+14, lanes[w[0]]+4, str(w[6]), 11, weight="bold", family=MONO, fill="#222")

    yy = y_sp0
    for cid in rc["spare_cavs"]:
        s.rect(X_TAG, yy-11, TAG_W, 22, stroke=C["SPARE"], fill="#f7f7f5", rx=4, sw=1.1)
        s.text(X_TAG+TAG_W/2, yy+4, cid, 12, anchor="middle", weight="bold", family=MONO, fill=C["muted"])
        s.text(X_W0+16, yy+4, "spare (plugged) — no wire", 10.5, fill=C["muted"])
        yy += 24

    fy = H - 40
    s.line(28, fy-14, W-28, fy-14, C["line"], 1)
    s.text(28, fy+2, f'Every conductor crimp-to-crimp, no splices · one wire per contact · Y-fork + leg lengths TBD at enclosure CAD · positions from TE STEP {rc["stepsrc"]}', 10, fill=C["muted"])
    s.text(28, fy+18, f'Wire table: {WIRE_TABLE} · board headers vertical THT — PNs per board-connector-picks.md (pending approval)', 10, fill=C["muted"])
    fn = f'{OUT}/{rc["key"]}-internal.svg'
    s.out(fn)
    return fn, W, H

# ---------------------------------------------------------------- face pinout
def seg_x(p1, p2, q1, q2):
    def ccw(a,b,c): return (c[1]-a[1])*(b[0]-a[0]) - (b[1]-a[1])*(c[0]-a[0])
    d1, d2 = ccw(q1,q2,p1), ccw(q1,q2,p2)
    d3, d4 = ccw(p1,p2,q1), ccw(p1,p2,q2)
    if ((d1>0 and d2<0) or (d1<0 and d2>0)) and ((d3>0 and d4<0) or (d3<0 and d4>0)):
        return True
    return False

def gen_face(rc, angle_nudge=None):
    angle_nudge = angle_nudge or {}
    W = 1300
    cavs = rc["cavities"]
    wmap = {w[0]: w for w in rc["wires"]}
    face = {cid: (sz, -x, y) for cid, (sz, x, y) in cavs.items()}
    Rmm = max(math.hypot(x,y)+CAVR[sz][0] for sz,x,y in face.values())
    scale = 200.0/Rmm if Rmm > 13 else 17.0
    R = Rmm*scale
    R_out = R + 34
    cx = W/2

    # ---- rays
    items = []
    for cid, (sz, x, y) in face.items():
        px, py = x*scale, -y*scale
        r = math.hypot(px, py)
        base = math.atan2(py, px) if r > 1 else 0.0
        cands = []
        for dstep in range(0, 81, 2):
            for sgn in ([0] if dstep==0 else [1,-1]):
                a = base + sgn*math.radians(dstep)
                ex, ey = R_out*math.cos(a), R_out*math.sin(a)
                clear = min((seg_point_dist(ox*scale, -oy*scale, px, py, ex, ey) - CAVR[osz][0]*scale
                             for ocid,(osz,ox,oy) in face.items() if ocid != cid), default=99)
                cands.append((clear, dstep, a))
        ok = [c for c in cands if c[0] > 13]
        if ok:
            near = [c for c in ok if c[1] <= 26]
            pick = max(near, key=lambda c: c[0]) if near else min(ok, key=lambda c: c[1])
        else:
            pick = max(cands, key=lambda c: c[0])
        a = pick[2] + math.radians(angle_nudge.get(cid, 0))
        items.append(dict(cid=cid, sz=sz, px=px, py=py, a=a,
                          ex=R_out*math.cos(a), ey=R_out*math.sin(a)))

    # ---- zones
    for it in items:
        deg = math.degrees(it["a"])
        deg = (deg+180) % 360 - 180
        if -115 < deg < -65:  it["zone"] = "T"
        elif 65 < deg < 115:  it["zone"] = "B"
        elif abs(deg) <= 65:  it["zone"] = "R"
        else:                 it["zone"] = "L"
    for z in ("T","B"):
        zl = [it for it in items if it["zone"]==z]
        if len(zl) > 3:
            zl.sort(key=lambda it: it["ex"])
            for it in zl[: (len(zl)-3)//2 + (len(zl)-3)%2 ]: it["zone"] = "L"
            for it in zl[len(zl)-((len(zl)-3)//2):]: it["zone"] = "R"

    def spread(vals, pitch, lo, hi):
        idx = sorted(range(len(vals)), key=lambda i: vals[i])
        out = [0]*len(vals)
        pos = None
        for k, i in enumerate(idx):
            v = max(vals[i], (pos + pitch) if pos is not None else -1e9)
            out[i] = v; pos = v
        # shift back if overflow
        over = max(0, (pos if pos is not None else lo) - hi)
        if over > 0:
            for k, i in enumerate(idx):
                out[i] -= over
            # re-forward-pass to keep >= lo
            pos = None
            for k, i in enumerate(idx):
                v = max(out[i], lo if pos is None else pos + pitch, lo)
                out[i] = v; pos = v
        return out

    lab_font_id, lab_font_c = 11.5, 10.5
    def label_text(cid):
        w = wmap.get(cid)
        if not w: return "spare (plugged)"
        awg_disp = w[2].replace(" tw","") + " AWG" + (" (tw)" if "tw" in w[2] else "")
        return f'{w[1]} · {awg_disp}'

    # side columns
    for z, sgn in (("L",-1),("R",1)):
        col = [it for it in items if it["zone"]==z]
        if not col: continue
        eys = [it["ey"] for it in col]
        lys = spread(eys, 38, -0.92*R_out, 0.92*R_out)
        for it, lyv in zip(col, lys): it["ly"] = lyv
    # top/bottom rows
    for z, sgn in (("T",-1),("B",1)):
        row = [it for it in items if it["zone"]==z]
        if not row: continue
        exs = [it["ex"] for it in row]
        widths = [max(txt_w(label_text(it["cid"]), lab_font_c), 60) for it in row]
        pitch = max(widths) + 26
        lxs = spread(exs, pitch, -W/2+120, W/2-120)
        for it, lxv in zip(row, lxs): it["lx"] = lxv

    # geometry: face center y
    top_n = len([1 for it in items if it["zone"]=="T"])
    bot_n = len([1 for it in items if it["zone"]=="B"])
    cy = 118 + (74 if top_n else 28) + R_out
    face_bottom = cy + R_out + (74 if bot_n else 28)

    # table
    rows = []
    for _, cid in rc["ordmap"]:
        w = wmap.get(cid)
        if w: rows.append((cid, w[1], w[2], f'{w[5]} · {w[6]}', w[3]))
        else: rows.append((cid, "spare (plugged)", "—", "—", "SPARE"))
    half = math.ceil(len(rows)/2)
    colsets = [rows[:half], rows[half:]]
    tab_y = face_bottom + 46
    row_h = 24
    H = int(tab_y + 30 + half*row_h + 88)

    s = SVG(W, H)
    title_block(s, W,
        f'{rc["name"]} — {rc["shell"]} · face pinout',
        f'{rc["arr"]} · cavity IDs per {rc["tedoc"]}',
        PROJECT, DATE)
    s.text(cx, 106, "FRONT VIEW — mating face (panel exterior)", 12.5, anchor="middle", weight="bold", fill="#444")

    draw_view(s, cx, cy, R, cavs, scale, mirror=True, spares=rc["spare_cavs"])

    # ---- draw callouts, collect segments for audit
    segs = []
    for it in items:
        cid = it["cid"]
        w = wmap.get(cid)
        spare = w is None
        tcol = C["muted"] if spare else ("#8a1010" if "ALWAYS-ON" in w[1] else "#333")
        ro = CAVR[it["sz"]][0]*scale
        sx = cx + it["px"] + ro*math.cos(it["a"])
        sy = cy + it["py"] + ro*math.sin(it["a"])
        ex, ey = cx + it["ex"], cy + it["ey"]
        if it["zone"] in ("L","R"):
            sgn = -1 if it["zone"]=="L" else 1
            colx = cx + sgn*(R_out + 44)
            lyv = cy + it["ly"]
            tipx = colx - sgn*2
            s.path(f'M {sx:.1f} {sy:.1f} L {ex:.1f} {ey:.1f} L {tipx:.1f} {lyv:.1f}', "#9a9a9a", 1.1)
            anchor = "end" if it["zone"]=="L" else "start"
            lx = colx + sgn*8
            s.text(lx, lyv-3, cid, lab_font_id, anchor=anchor, weight="bold", family=MONO,
                   fill=("#666" if spare else "#111"))
            s.text(lx, lyv+11, label_text(cid), lab_font_c, anchor=anchor, fill=tcol)
            segs.append((cid, (sx,sy), (ex,ey)))
            segs.append((cid, (ex,ey), (tipx,lyv)))
        else:
            sgn = -1 if it["zone"]=="T" else 1
            lxv = cx + it["lx"]
            base_y = cy + sgn*(R_out + 40)
            tip = (lxv, base_y + sgn*2)
            s.path(f'M {sx:.1f} {sy:.1f} L {ex:.1f} {ey:.1f} L {tip[0]:.1f} {tip[1]:.1f}', "#9a9a9a", 1.1)
            if it["zone"]=="T":
                s.text(lxv, base_y-16, cid, lab_font_id, anchor="middle", weight="bold", family=MONO,
                       fill=("#666" if spare else "#111"))
                s.text(lxv, base_y-3, label_text(cid), lab_font_c, anchor="middle", fill=tcol)
            else:
                s.text(lxv, base_y+14, cid, lab_font_id, anchor="middle", weight="bold", family=MONO,
                       fill=("#666" if spare else "#111"))
                s.text(lxv, base_y+27, label_text(cid), lab_font_c, anchor="middle", fill=tcol)
            segs.append((cid, (sx,sy), (ex,ey)))
            segs.append((cid, (ex,ey), tip))

    # audit
    warn = []
    for i in range(len(segs)):
        for j in range(i+1, len(segs)):
            if segs[i][0] == segs[j][0]: continue
            if seg_x(segs[i][1], segs[i][2], segs[j][1], segs[j][2]):
                warn.append((rc["key"], segs[i][0], segs[j][0]))
    # ray vs foreign cavity circle audit
    for it in items:
        sx, sy = cx+it["px"], cy+it["py"]
        ex, ey = cx + it["ex"], cy + it["ey"]
        for ocid, (osz, ox, oy) in face.items():
            if ocid == it["cid"]: continue
            d = seg_point_dist(cx+ox*scale, cy-oy*scale, sx, sy, ex, ey)
            if d < CAVR[osz][0]*scale + 2:
                warn.append((rc["key"], f'{it["cid"]}-ray', f'circle-{ocid}'))

    tx0 = 60
    col_w = (W - 2*tx0 - 40)/2
    cwx = [0.11, 0.50, 0.13, 0.26]
    for ci, cset in enumerate(colsets):
        x0 = tx0 + ci*(col_w+40)
        yh = tab_y
        s.rect(x0, yh-16, col_w, 22, fill=C["band"])
        acc = x0+10
        for hname, fw in zip(["cav","circuit","AWG","dest header · pin"], cwx):
            s.text(acc, yh, hname, 10.5, weight="bold", fill="#555"); acc += col_w*fw
        yy = yh + row_h
        for ri, (cid, circ, awg, dest, cl) in enumerate(cset):
            if ri % 2 == 0: s.rect(x0, yy-16, col_w, row_h, fill="#f7f7f5")
            muted = cl=="SPARE"
            fcol = C["muted"] if muted else "#222"
            acc = x0+10
            s.text(acc, yy, cid, 11, weight="bold", family=MONO, fill=fcol); acc += col_w*cwx[0]
            s.text(acc, yy, circ, 10.5, fill=("#8a1010" if "ALWAYS-ON" in circ else fcol)); acc += col_w*cwx[1]
            s.text(acc, yy, awg, 10.5, fill=fcol); acc += col_w*cwx[2]
            s.text(acc, yy, dest, 10.5, fill=fcol, family=MONO)
            yy += row_h

    fy = H - 40
    s.line(28, fy-14, W-28, fy-14, C["line"], 1)
    s.text(28, fy+2, f'Cavity positions from TE STEP {rc["stepsrc"]} · IDs per {rc["tedoc"]} (rear-view lettering, mirrored here for face view)', 10, fill=C["muted"])
    s.text(28, fy+18, 'Clocking: orient per shell master key at install · unused cavities sealed with plugs (TE 114-151014 §3.7)', 10, fill=C["muted"])
    fn = f'{OUT}/{rc["key"]}-pinout.svg'
    s.out(fn)
    return fn, W, H, warn

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    manifest, warns = [], []
    NUDGE = {}  # per-connector cavity angle nudges, filled after audit
    for rc in RECEPTACLES:
        f1 = gen_internal(rc)
        f2 = gen_face(rc, NUDGE.get(rc["key"]))
        manifest.append((f1[0], f1[1], f1[2]))
        manifest.append((f2[0], f2[1], f2[2]))
        warns += f2[3]
    with open(f'{OUT}/manifest.txt', 'w') as f:
        for fn, w, h in manifest:
            f.write(f'{os.path.basename(fn)} {w} {h}\n')
    for w in warns: print("XING:", w)
    print("generated", len(manifest), "svgs;", len(warns), "collision warnings")
