#!/usr/bin/env python3
"""Build one .excalidraw board from a folder of room files.
usage: python3 build_board.py ROOMS_DIR OUT.excalidraw [--figs FIGS_DIR] [--cols 4]
Each room file is NN-name.txt. Line 1 is "# Room title". Blocks follow, separated by a line "====".
See reference/block-format.md for the block kinds."""
import sys, os, re, json, glob, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser(); ap.add_argument("rooms"); ap.add_argument("out")
ap.add_argument("--figs", default="figs"); ap.add_argument("--cols", type=int, default=4)
args = ap.parse_args(); FIGS = args.figs
from xd2 import *
import xd, fm
from PIL import Image as _Im
os.makedirs("fcache", exist_ok=True)
FULL = 2500
HDR_COL = ["#9fd8dc", "#f6b9a1", "#c9bdee", "#f7d38f", "#c8e6b5"]
def render(fn, *a):
    i0 = len(xd.E); w, h = fn(*a, 0, 0); els = xd.E[i0:]; del xd.E[i0:]
    return els, w, h
def place(els, dx, dy):
    for e in els: e["x"] += dx; e["y"] += dy; xd.E.append(e)
def bbox(els):
    return (min(e["x"] for e in els), min(e["y"] for e in els),
            max(e["x"] + e["width"] for e in els), max(e["y"] + e["height"] for e in els))
import textwrap as _tw
BW, GAP, COLS = 780, 80, 3
def _table(x, y, span_w, lines, fs=14):
    rows = [[c.strip() for c in l.split("|")] for l in lines if l.strip()]
    nc = max(len(r) for r in rows)
    rows = [r + [""] * (nc - len(r)) for r in rows]
    cw = [max(tw(c, fs, FONT_SANS) for c in col) + 18 for col in zip(*rows)]
    cw = [max(min(c, 330), max(tw(wd, fs, FONT_SANS) for cell in col for wd in (cell.split() or [''])) + 22) for c, col in zip(cw, zip(*rows))]
    sc = min(1.0, span_w / sum(cw)); cw = [c * sc for c in cw]
    yy = y
    for ri, r in enumerate(rows):
        wr = [_tw.wrap(c, max(6, int((cw[i] - 14) / 8.6))) or [""] for i, c in enumerate(r)]
        rh = max(len(w) for w in wr) * fs * 1.25 + 12
        xx = x
        for i, w in enumerate(wr):
            rect(xx, yy, cw[i], rh, bg="#f6d1c3" if ri == 0 else ("#ffffff" if ri % 2 else "#f7f4ef"), stroke="#888888")
            text(xx + 8, yy + 6, "\n".join(w), fs, color="#1e1e1e")
            xx += cw[i]
        yy += rh
    return yy - y

def _blockfn(kind, x, y, w, body):
    """draws body at (x,y) width w, returns height"""
    if kind == "anat":
        COL = ["#C15F3C", "#2F7F86", "#6B5CA5", "#9A7B2F", "#8E2A3B", "#37535F", "#4F7A5F", "#B0468A"]
        STRUT = r"\vphantom{\sum_{i=1}^{G}\dfrac{\pi^{2}}{\pi_{g}}}"
        pre, segs, post = [], [], []; mode = 0
        for l in body:
            if l.startswith("$$ "):
                mode = 1; t, _, lab_ = l[3:].partition("||"); segs.append((t.strip(), lab_.strip()))
            elif l.strip() == "--": mode = 2
            elif mode == 2: post.append(l)
            else: pre.append(l)
        yy = y
        if pre: yy += _blockfn("text", x, yy, w, pre) + 14
        ims = []; ci = 0
        for t, lab_ in segs:
            c = None
            if lab_: c = COL[ci % len(COL)]; ci += 1
            tex = STRUT + (r"{\color[HTML]{%s}%s}" % (c[1:], t) if c else t)
            r = fm.get(tex, True)
            ims.append((r, c, lab_, t))
        if any(r is None for r, c, l_, t in ims):
            return _blockfn('text', x, y, w, pre + [t + ('    <- ' + l_ if l_ else '') for r, c, l_, t in ims] + post)
        tot = sum(r[1] for r, c, l_, t in ims if r)
        sc = min(0.95, (w - 20) / max(tot, 1))
        H = max(r[2] for r, c, l_, t in ims if r) * sc
        xx = x + max(0, (w - tot * sc) / 2); anchors = []
        for r, c, lab_, t in ims:
            if not r: continue
            fid, pw, ph = r
            xd.image(xx, yy, pw * sc, ph * sc, fid, "fcache/%s.png" % fid)
            if c:
                xd.line([(xx + 2, yy + H + 3), (xx + pw * sc - 2, yy + H + 3)], color=c, sw=2, arrow=False)
                anchors.append((xx + pw * sc / 2, c, lab_))
            xx += pw * sc
        n = max(len(anchors), 1); cwid = w / n; ly = yy + H + 92; lh = 0
        for j, (ax, c, lab_) in enumerate(anchors):
            lx = x + j * cwid
            t = "\n".join(sum([wrapline(p, max(14, int((cwid - 18) / 8.2))) for p in lab_.split("\\n")], []))
            text(lx + 4, ly, t, 15, color=c)
            xd.line([(lx + min(cwid / 2, 90), ly - 6), (ax, yy + H + 10)], color=c, sw=1)
            lh = max(lh, th(t, 15))
        yy = ly + lh + 16
        if post: yy += _blockfn("text", x, yy, w, post)
        return yy - y
    if kind == "table":
        return _table(x, y, w, body)
    if kind in ("flow", "xy", "pie", "seq"):
        fn = {"flow": draw_flow, "xy": draw_xychart, "pie": draw_pie, "seq": draw_seq}[kind]
        els, ww, hh = render(fn, "\n".join(body)); place(els, x, y)
        return hh
    if kind == "img":
        name = body[0].strip(); cap = " ".join(body[1:])
        im = _Im.open(os.path.join(FIGS, name)); iw, ih = im.size
        sc = min(w / iw, 460 / ih, 1.6); dw, dh = iw * sc, ih * sc
        xd.image(x, y, dw, dh, "fig_" + name.rsplit(".", 1)[0], os.path.join(FIGS, name))
        t = "\n".join(wrapline(cap, max(24, int(w / 8.4)))) if cap else ""
        if t: text(x, y + dh + 6, t, 14, color="#444444")
        return dh + 8 + (th(t, 14) if t else 0)
    if kind == "math":
        yy = y
        for l in body:
            if l.startswith("$ "):
                r = fm.get(l[2:])
                if r:
                    fid, pw, ph = r; sc = min(0.6, (w - 20) / pw)
                    xd.image(x + 12, yy, pw * sc, ph * sc, fid, "fcache/%s.png" % fid); yy += ph * sc + 10
                else:
                    text(x, yy, l[2:], 14, fam=FONT_MONO); yy += 22
            else:
                t = "\n".join(wrapline(l, int(w / 8.4))) if l.strip() else " "
                text(x, yy, t, 14, fam=FONT_MONO); yy += th(t, 14) + 4
        return yy - y
    if kind == "code":
        t = "\n".join(body); h = th(t, 14) + 20
        rect(x - 8, y - 4, w, h, bg="#f1ede8", stroke="#aaaaaa")
        text(x + 4, y + 6, t, 14, fam=FONT_MONO)
        return h
    if kind == "qa":
        yy = y
        for l in body:
            if l.startswith("A:"):
                t = "\n".join(wrapline(l, int(w / 8.4)))
                h = th(t, 14) + 14
                rect(x, yy, w - 20, h, bg="#e4f0dc", stroke="#6b9a58", dash="dashed")
                text(x + 10, yy + 7, t, 14, fam=FONT_MONO); yy += h + 8
            else:
                t = "\n".join(wrapline(l, int(w / 8.4))) if l.strip() else " "
                text(x, yy, t, 14, fam=FONT_MONO, color="#222266"); yy += th(t, 14) + 4
        return yy - y
    # plain text
    out = []; lim = int(w / 8.4)
    for l in body:
        if len(l) > lim:
            ind = len(l) - len(l.lstrip(" ")); pad = " " * (ind + (2 if l.lstrip().startswith("- ") else 0))
            ws = wrapline(l.strip(), lim - len(pad))
            out += [" " * ind + ws[0]] + [pad + s_ for s_ in ws[1:]]
        else: out.append(l)
    t = "\n".join(out); text(x, y, t, 14, fam=FONT_MONO)
    return th(t, 14)

def draw_blocks(f, y):
    raw = [b.strip("\n") for b in open(f).read().split('\n', 1)[1].split("\n====\n")]
    used = set()
    rect(0, y, FULL, 44, bg="#c8e6b5", stroke="#4a7a3a")
    text(16, y + 9, "Learn it here: each block explains one idea in the form that suits it (follow the orange arrows)", 20)
    y += 70
    items = []
    for b in raw:
        lines = b.split("\n"); head = lines[0]; body = lines[1:]
        kind = "text"; span = 1
        m = re.match(r"@(\w+?)(\d?)\s+(.*)", head)
        if m: kind, span, title = m.group(1), int(m.group(2) or 1), m.group(3)
        else: title = head
        if kind == "img": used.add(body[0].strip())
        items.append((kind, span, title, body))
    k = 0; prev = None
    while k < len(items):
        row = []; cols = 0
        while k < len(items) and cols + items[k][1] <= COLS:
            row.append(items[k]); cols += items[k][1]; k += 1
        x = 0; rh = 0; firstx = None; lastend = None; hs = []
        for kind, span, title, body in row:
            w = span * BW + (span - 1) * GAP
            text(x, y, title, 20, color="#8a3b12")
            h = _blockfn(kind, x, y + 34, w, body) + 34
            if prev is not None: pass
            hs.append((x, w, h)); rh = max(rh, h); x += w + GAP
        for j in range(len(hs) - 1):
            xa = hs[j][0] + hs[j][1] + 6
            xd.line([(xa, y + 14), (xa + GAP - 14, y + 14)], color="#C15F3C", sw=2)
        if k < len(items):
            xl = hs[-1][0] + hs[-1][1] / 2
            xd.line([(xl, y + rh + 8), (xl, y + rh + 34), (BW / 2, y + rh + 34), (BW / 2, y + rh + 62)], color="#C15F3C", sw=2)
        y += rh + 90
    return y + 20, used

room_files = sorted(glob.glob(os.path.join(args.rooms, "*.txt")))
if not room_files:
    ap.error(f"No room .txt files found in: {args.rooms}")
if args.cols < 1:
    ap.error("--cols must be at least 1")
rooms = []
for k, f in enumerate(room_files):
    title = open(f).read().split("\n", 1)[0].lstrip("# ").strip()
    i0 = len(xd.E)
    hdr = rect(0, 0, FULL, 96, bg=HDR_COL[k % len(HDR_COL)], stroke="#333333", sw=2)
    text(30, 22, title, 38)
    draw_blocks(f, 130)
    els = xd.E[i0:]; del xd.E[i0:]
    rooms.append((hdr, els, bbox(els)))
N = args.cols; GAP = 520
rows = [rooms[i:i + N] for i in range(0, len(rooms), N)]
colw = [max(r[i][2][2] for r in rows if len(r) > i) for i in range(min(N, len(rooms)))]
colx = [0]
for w_ in colw[:-1]: colx.append(colx[-1] + w_ + GAP)
y = 0; prev = None; right = colx[-1] + colw[-1] + 250
for r in rows:
    for ci, (hdr, els, bb) in enumerate(r):
        place(els, colx[ci], y)
        if prev is not None:
            ay = prev["y"] + 48; by_ = hdr["y"] + 48
            if abs(prev["y"] - hdr["y"]) < 1: xd.line([(prev["x"] + prev["width"], ay), (hdr["x"], by_)], color="#C15F3C", sw=4)
            else:
                gy = hdr["y"] - GAP / 2
                xd.line([(prev["x"] + prev["width"], ay), (right, ay), (right, gy), (-250, gy), (-250, by_), (hdr["x"], by_)], color="#C15F3C", sw=4)
        prev = hdr
    y += max(c[2][3] for c in r) + GAP
doc = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com", "elements": xd.E,
       "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"}, "files": xd.FILES}
os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
with open(args.out, "w", encoding="utf-8") as out_f:
    json.dump(doc, out_f, ensure_ascii=False)
ids = [e["id"] for e in xd.E]
print(len(ids), "elements; unique ids:", len(set(ids)) == len(ids), "; images:", len(xd.FILES))
bad = glob.glob("fcache/*.fail")
if bad: print("LaTeX failed for", len(bad), "formulas (see fcache/*.fail). Each segment must compile on its own.")
