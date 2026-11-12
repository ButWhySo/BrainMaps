import json, re, random, math, textwrap
R = random.Random(7)
E = []            # all elements
FILES = {}
FONT_SANS, FONT_MONO = 1, 3

_C=[0]
def nid():
    _C[0]+=1
    return "e%06d" % _C[0]
def seed(): return R.randint(1, 2**31 - 1)

def common(t, x, y, w, h, stroke="#1e1e1e", bg="transparent", fill="solid", sw=1, dash="solid",
           rough=1, groups=None, round_=True):
    return dict(id=nid(), type=t, x=x, y=y, width=w, height=h, angle=0, strokeColor=stroke,
                backgroundColor=bg, fillStyle=fill, strokeWidth=sw, strokeStyle=dash, roughness=rough,
                opacity=100, groupIds=groups or [], frameId=None,
                roundness=({"type": 3} if (round_ and t in ("rectangle", "diamond", "ellipse")) else None),
                seed=seed(), version=1, versionNonce=seed(), isDeleted=False, boundElements=[],
                updated=1, link=None, locked=False)

def tw(s, fs, fam):
    f = 0.6 if fam == FONT_MONO else 0.57
    return max((len(l) for l in s.split("\n")), default=0) * fs * f
def th(s, fs): return (s.count("\n") + 1) * fs * 1.25

def text(x, y, s, fs=16, fam=FONT_SANS, color="#1e1e1e", align="left", groups=None, container=None, w=None, h=None, valign="top"):
    w = w if w is not None else tw(s, fs, fam); h = h if h is not None else th(s, fs)
    e = common("text", x, y, w, h, stroke=color, groups=groups)
    e.update(text=s, fontSize=fs, fontFamily=fam, textAlign=align, verticalAlign=valign, containerId=container,
             originalText=s, autoResize=True, lineHeight=1.25)
    e["roundness"] = None
    E.append(e); return e

def rect(x, y, w, h, bg="#ffffff", stroke="#1e1e1e", t="rectangle", dash="solid", sw=1, groups=None, rough=1, fill="solid"):
    e = common(t, x, y, w, h, stroke=stroke, bg=bg, dash=dash, sw=sw, groups=groups, rough=rough, fill=fill)
    E.append(e); return e

def labeled(x, y, w, h, s, bg="#ffffff", stroke="#1e1e1e", t="rectangle", fs=16, fam=FONT_SANS, dash="solid", sw=1):
    sh = rect(x, y, w, h, bg, stroke, t, dash, sw)
    tx = text(x + w / 2 - tw(s, fs, fam) / 2, y + h / 2 - th(s, fs) / 2, s, fs, fam, align="center",
              container=sh["id"], valign="middle")
    sh["boundElements"].append({"id": tx["id"], "type": "text"})
    return sh

def line(points, color="#1e1e1e", sw=1, dash="solid", arrow=True, start=None, end=None, head="arrow"):
    x0, y0 = points[0]
    rel = [[px - x0, py - y0] for px, py in points]
    xs = [p[0] for p in rel]; ys = [p[1] for p in rel]
    e = common("arrow" if arrow else "line", x0, y0, max(xs) - min(xs), max(ys) - min(ys), stroke=color, sw=sw, dash=dash, round_=False)
    e.update(points=rel, lastCommittedPoint=None, startBinding=None, endBinding=None, startArrowhead=None,
             endArrowhead=(head if arrow else None))
    if arrow: e["elbowed"] = False
    if start is not None:
        e["startBinding"] = {"elementId": start["id"], "focus": 0, "gap": 4}; start["boundElements"].append({"id": e["id"], "type": "arrow"})
    if end is not None:
        e["endBinding"] = {"elementId": end["id"], "focus": 0, "gap": 4}; end["boundElements"].append({"id": e["id"], "type": "arrow"})
    E.append(e); return e

def edge_pt(s, tx, ty):
    """point on border of shape s (x,y,w,h) toward (tx,ty)"""
    cx, cy = s["x"] + s["width"] / 2, s["y"] + s["height"] / 2
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0: return cx, cy
    hw, hh = s["width"] / 2, s["height"] / 2
    k = min(hw / abs(dx) if dx else 1e9, hh / abs(dy) if dy else 1e9)
    return cx + dx * k, cy + dy * k

def connect(a, b, label=None, dash="solid", arrow=True, color="#1e1e1e"):
    acx, acy = a["x"] + a["width"] / 2, a["y"] + a["height"] / 2
    bcx, bcy = b["x"] + b["width"] / 2, b["y"] + b["height"] / 2
    p1 = edge_pt(a, bcx, bcy); p2 = edge_pt(b, acx, acy)
    ar = line([p1, p2], color=color, dash=dash, arrow=arrow, start=a, end=b)
    if label:
        mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        text(mx - tw(label, 13, FONT_SANS) / 2, my - 18, label, 13, color="#555555")
    return ar

def connect_tree(a, b):
    ax, ay = a["x"] + a["width"], a["y"] + a["height"] / 2
    bx, by = b["x"], b["y"] + b["height"] / 2
    mx = ax + (bx - ax) * 0.5
    return line([(ax, ay), (mx, ay), (mx, by), (bx, by)], arrow=False, start=a, end=b)

def wrapline(l, width):
    ind = re.match(r"^(\s*(?:[•▸]\s+|\d+\.\s+|-\s+)?)", l).group(1)
    sub = " " * len(ind)
    return textwrap.wrap(l, width=width, subsequent_indent=sub, break_long_words=False, break_on_hyphens=False) or [""]

def clean(s):
    s = s.replace("**", "").replace("`", "").replace("\\|", "|")
    s = re.sub(r"^(\s*)- ", r"\1• ", s)
    return s

import base64, time
def image(x, y, w, h, fid, png_path):
    if fid not in FILES:
        FILES[fid] = {"mimeType": "image/png", "id": fid, "created": 1700000000000, "lastRetrieved": 1700000000000,
                      "dataURL": "data:image/png;base64," + base64.b64encode(open(png_path, "rb").read()).decode()}
    e = common("image", x, y, w, h, round_=False)
    e.update(fileId=fid, status="saved", scale=[1, 1], crop=None)
    E.append(e); return e
