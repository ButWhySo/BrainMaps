from xd import *
import xd

PAL = ["#C15F3C", "#2F7F86", "#6B5CA5", "#D98E3F"]
BR_COL = ["#ffd6c9", "#cdeaec", "#e2dcf5", "#fde3bd", "#d8efd0", "#ffd0e6", "#cfe3ff", "#f6f0b8"]

# ---------------- mindmap ----------------
def parse_mindmap(src):
    items = []
    for l in src.split("\n")[1:]:
        if not l.strip(): continue
        ind = len(l) - len(l.lstrip())
        t = l.strip()
        m = re.match(r"root\(\((.*)\)\)", t)
        items.append((ind, m.group(1) if m else t))
    root = {"t": items[0][1], "c": []}; stack = [(items[0][0], root)]
    for ind, t in items[1:]:
        while stack and stack[-1][0] >= ind: stack.pop()
        n = {"t": t, "c": []}; stack[-1][1]["c"].append(n); stack.append((ind, n))
    return root

def node_size(t, fs=16, maxc=18):
    lines = textwrap.wrap(t, maxc) or [t]
    w = max(tw(l, fs, FONT_SANS) for l in lines) + 28
    h = len(lines) * fs * 1.25 + 18
    return "\n".join(lines), max(w, 80), h

def leaves(n): return 1 if not n["c"] else sum(leaves(c) for c in n["c"])

def draw_tree(root, x0, y0, colors=BR_COL):
    """left-to-right tidy tree. returns (width, height)"""
    VG, HG, LP = 14, 70, 56
    maxx = [0]; maxy = [0]
    def place(n, depth, x, ytop, bi):
        s, w, h = node_size(n["t"], 15, 40) if depth >= 2 else node_size(n["t"])
        lv = leaves(n); span = lv * (LP + VG)
        n["_s"], n["_w"], n["_h"] = s, w, h
        if n["c"]:
            cy = ytop; cx = x + w + HG
            for i, c in enumerate(n["c"]):
                place(c, depth + 1, cx, cy, bi if depth else i)
                cy += leaves(c) * (LP + VG)
            first, last = n["c"][0], n["c"][-1]
            ymid = (first["_y"] + first["_h"] / 2 + last["_y"] + last["_h"] / 2) / 2
            n["_y"] = ymid - h / 2
        else:
            n["_y"] = ytop + (LP - h) / 2 if h < LP else ytop
        n["_x"] = x; n["_bi"] = bi
        maxx[0] = max(maxx[0], x + w); maxy[0] = max(maxy[0], ytop + span)
    place(root, 0, x0, y0, 0)
    def draw(n, depth, parent):
        col = "#ffe9a8" if depth == 0 else colors[n["_bi"] % len(colors)]
        sh = labeled(n["_x"], n["_y"], n["_w"], n["_h"], n["_s"], bg=col, t="ellipse" if depth == 0 else "rectangle",
                     sw=2 if depth == 0 else 1, fs=15 if depth >= 2 else 16)
        if parent is not None: connect_tree(parent, sh)
        for c in n["c"]: draw(c, depth + 1, sh)
    draw(root, 0, None)
    return maxx[0] - x0, maxy[0] - y0

def draw_radial(root, cx, cy, R1=420, R2=980):
    rs, rw, rh = node_size(root["t"], 20, 14)
    rt = labeled(cx - 110, cy - 60, 220, 120, root["t"], bg="#ffe9a8", t="ellipse", fs=20, sw=2)
    n = len(root["c"])
    for i, b in enumerate(root["c"]):
        th_ = 2 * math.pi * i / n - math.pi / 2
        bs, bw, bh = node_size(b["t"], 18, 16)
        bx, by = cx + R1 * math.cos(th_), cy + R1 * math.sin(th_)
        col = BR_COL[i % len(BR_COL)]
        bsh = labeled(bx - bw / 2, by - bh / 2, bw, bh, bs, bg=col, fs=18, sw=2)
        connect_tree(rt, bsh)
        k = len(b["c"]); wedge = 2 * math.pi / n * 0.82
        for j, l in enumerate(b["c"]):
            a = th_ + (j - (k - 1) / 2) * (wedge / max(k, 1))
            lx, ly = cx + R2 * math.cos(a), cy + R2 * math.sin(a)
            ls, lw, lh = node_size(l["t"], 15, 16)
            lsh = labeled(lx - lw / 2, ly - lh / 2, lw, lh, ls, bg="#ffffff", stroke=PAL[i % 4], fs=15)
            connect(bsh, lsh, arrow=False)

# ---------------- flowchart ----------------
NODE = re.compile(r'\s*([A-Za-z][A-Za-z0-9_]*)(?:\["(.*?)"\]|\{"(.*?)"\})?')
EDGE = re.compile(r'\s*(-->|---|==>|-\.->|-\.\s+([^.]*?)\s+\.->)(?:\|"?(.*?)"?\|)?')

def parse_flow(src):
    lines = src.strip().split("\n")
    direction = lines[0].split()[1] if len(lines[0].split()) > 1 else "TB"
    nodes = {}; order = []; edges = []; subs = {}; sub_stack = []; sub_dir = {}
    def add(i, t, dia):
        if i not in nodes: nodes[i] = {"id": i, "t": None, "dia": False, "sub": None}; order.append(i)
        if t: nodes[i]["t"] = t
        if dia: nodes[i]["dia"] = True
        if sub_stack and nodes[i]["sub"] is None and i not in subs: nodes[i]["sub"] = sub_stack[-1]
    for l in lines[1:]:
        s = l.strip()
        if not s: continue
        m = re.match(r'subgraph\s+([A-Za-z0-9_]+)(?:\["(.*?)"\])?', s)
        if m:
            subs[m.group(1)] = {"t": m.group(2) or m.group(1), "dir": None}; sub_stack.append(m.group(1)); continue
        if s == "end": sub_stack.pop(); continue
        m = re.match(r"direction\s+(\w+)", s)
        if m and sub_stack: subs[sub_stack[-1]]["dir"] = m.group(1); continue
        pos = 0; prev = None; pend = None
        while pos < len(s):
            m = NODE.match(s, pos)
            if not m: break
            i, t1, t2 = m.group(1), m.group(2), m.group(3)
            if i not in subs: add(i, t1 or t2, t2 is not None)
            if prev is not None and pend is not None: edges.append((prev, i, pend))
            prev = i; pos = m.end()
            m2 = EDGE.match(s, pos)
            if not m2: break
            lab = m2.group(3) or m2.group(2)
            pend = {"label": lab, "dash": "dashed" if m2.group(1).startswith("-.") else "solid", "arrow": m2.group(1) != "---"}
            pos = m2.end()
    return direction, nodes, order, edges, subs

def layout_nodes(ids, nodes, edges, direction):
    """layered layout; returns positions dict id->(x,y,w,h) with origin 0,0, plus size"""
    idset = set(ids)
    out = {i: [] for i in ids}; indeg = {i: 0 for i in ids}
    E2 = [(a, b) for a, b, _ in edges if a in idset and b in idset]
    # remove back edges via DFS
    adj = {i: [] for i in ids}
    for a, b in E2: adj[a].append(b)
    color = {}; back = set()
    def dfs(u):
        color[u] = 1
        for v in adj[u]:
            if color.get(v) == 1: back.add((u, v))
            elif v not in color: dfs(v)
        color[u] = 2
    for i in ids:
        if i not in color: dfs(i)
    dag = [(a, b) for a, b in E2 if (a, b) not in back]
    rank = {i: 0 for i in ids}
    for _ in range(len(ids)):
        ch = False
        for a, b in dag:
            if rank[b] < rank[a] + 1: rank[b] = rank[a] + 1; ch = True
        if not ch: break
    layers = {}
    for i in ids: layers.setdefault(rank[i], []).append(i)
    sizes = {}
    for i in ids:
        t = nodes[i]["t"] or i
        s, w, h = node_size(t, 16, 24)
        if nodes[i]["dia"]: w, h = w * 1.7, h * 2.0
        sizes[i] = (s, w, h)
    pos = {}; GAP_L, GAP_O = 70, 36
    lr = direction in ("LR", "RL")
    cursor = 0; extents = []
    for r in sorted(layers):
        L = layers[r]
        main = max((sizes[i][1] if lr else sizes[i][2]) for i in L)
        tot = sum((sizes[i][2] if lr else sizes[i][1]) for i in L) + GAP_O * (len(L) - 1)
        extents.append(tot); c2 = 0
        for i in L:
            s, w, h = sizes[i]
            if lr: pos[i] = [cursor + (main - w) / 2, c2, w, h]; c2 += h + GAP_O
            else: pos[i] = [c2, cursor + (main - h) / 2, w, h]; c2 += w + GAP_O
        cursor += main + GAP_L
    mx = max(extents) if extents else 0
    for r in sorted(layers):
        L = layers[r]
        tot = sum((sizes[i][2] if lr else sizes[i][1]) for i in L) + GAP_O * (len(L) - 1)
        off = (mx - tot) / 2
        for i in L:
            if lr: pos[i][1] += off
            else: pos[i][0] += off
    W = max(p[0] + p[2] for p in pos.values()); H = max(p[1] + p[3] for p in pos.values())
    return pos, sizes, back, W, H

def draw_flow(src, x0, y0):
    direction, nodes, order, edges, subs = parse_flow(src)
    shapes = {}; wmax = 0; hmax = 0
    if not subs:
        pos, sizes, back, W, H = layout_nodes(order, nodes, edges, direction)
        for i in order:
            x, y, w, h = pos[i]; s = sizes[i][0]
            shapes[i] = labeled(x0 + x, y0 + y, w, h, s, bg="#eef1ff" if not nodes[i]["dia"] else "#fff3c4",
                                t="diamond" if nodes[i]["dia"] else "rectangle")
        wmax, hmax = W, H
    else:
        # lay out each subgraph by itself, then stack
        cur_x = 0; cur_y = 0; rects = {}
        for sid, sg in subs.items():
            ids = [i for i in order if nodes[i]["sub"] == sid]
            d = sg["dir"] or direction
            pos, sizes, back, W, H = layout_nodes(ids, nodes, edges, d)
            pad = 30; title_h = 28
            gx, gy = (x0 + cur_x, y0 + cur_y) if True else (0, 0)
            gb = rect(gx, gy, W + 2 * pad, H + 2 * pad + title_h, bg="#fffdf5", stroke="#999999", dash="dashed")
            text(gx + 12, gy + 6, sg["t"], 15, color="#666666")
            for i in ids:
                x, y, w, h = pos[i]; s = sizes[i][0]
                shapes[i] = labeled(gx + pad + x, gy + pad + title_h + y, w, h, s, bg="#eef1ff",
                                    t="diamond" if nodes[i]["dia"] else "rectangle")
            shapes[sid] = gb
            if (sg["dir"] or direction) in ("LR", "RL"):  # stack vertically
                cur_y += H + 2 * pad + title_h + 60; wmax = max(wmax, W + 2 * pad)
            else:
                cur_x += W + 2 * pad + 60; hmax = max(hmax, H + 2 * pad + title_h)
        wmax = max(wmax, cur_x); hmax = max(hmax, cur_y)
        # free (non-subgraph) nodes after
        free = [i for i in order if nodes[i]["sub"] is None]
        fy = y0 + (cur_y if cur_y else hmax) + 20
        for k, i in enumerate(free):
            s, w, h = node_size(nodes[i]["t"] or i, 16, 24)
            shapes[i] = labeled(x0 + wmax / 2 - w / 2, fy, w, h, s, bg="#eef1ff"); fy += h + 50
        hmax = max(hmax, fy - y0)
    for a, b, meta in edges:
        if a in shapes and b in shapes:
            sa, sb = shapes[a], shapes[b]
            if sa["y"] > sb["y"] + sb["height"] and False: pass
            connect(sa, sb, meta["label"], meta["dash"], meta["arrow"])
    return wmax, hmax

# ---------------- sequence diagram ----------------
def draw_seq(src, x0, y0):
    parts = []; names = {}; msgs = []
    for l in src.strip().split("\n")[1:]:
        s = l.strip()
        m = re.match(r"participant\s+(\w+)\s+as\s+(.*)", s)
        if m: parts.append(m.group(1)); names[m.group(1)] = m.group(2); continue
        m = re.match(r"(\w+)(-->>|->>)(\w+):\s*(.*)", s)
        if m: msgs.append((m.group(1), m.group(3), m.group(4), m.group(2) == "-->>"))
    gap = 190; ys = y0 + 70; H = 70 + 52 * len(msgs) + 40
    cx = {p: x0 + 80 + i * gap for i, p in enumerate(parts)}
    for p in parts:
        labeled(cx[p] - 70, y0, 140, 44, names[p], bg="#e7e1f7")
        line([(cx[p], y0 + 44), (cx[p], y0 + H)], arrow=False, dash="dashed", color="#888888")
    y = ys
    for a, b, t, dashed in msgs:
        if a == b:
            line([(cx[a], y), (cx[a] + 45, y), (cx[a] + 45, y + 22), (cx[a], y + 22)], dash="solid")
            text(cx[a] + 52, y, t, 13, color="#444444")
        else:
            line([(cx[a], y + 10), (cx[b], y + 10)], dash="dashed" if dashed else "solid")
            lo, hi = min(cx[a], cx[b]), max(cx[a], cx[b])
            text((lo + hi) / 2 - tw(t, 13, FONT_SANS) / 2, y - 8, t, 13, color="#444444")
        y += 52
    return gap * (len(parts) - 1) + 160, H

# ---------------- charts ----------------
def draw_xychart(src, x0, y0):
    title = re.search(r'title\s+"(.*?)"', src); title = title.group(1) if title else ""
    xa = re.search(r'x-axis\s+"(.*?)"\s*\[(.*?)\]', src); cats = [c.strip() for c in xa.group(2).split(",")]
    ya = re.search(r'y-axis\s+"(.*?)"\s+([\-\d.]+)\s*-->\s*([\-\d.]+)', src)
    ymin, ymax = float(ya.group(2)), float(ya.group(3))
    series = [[float(v) for v in m.split(",")] for m in re.findall(r"line\s*\[(.*?)\]", src)]
    W, H = 560, 300; px, py = x0 + 70, y0 + 50
    text(x0, y0, title, 16, color="#333333")
    line([(px, py), (px, py + H), (px + W, py + H)], arrow=False)
    for k in range(6):
        v = ymin + (ymax - ymin) * k / 5; yy = py + H - H * k / 5
        text(px - 8 - tw("%.2f" % v, 12, FONT_SANS), yy - 8, "%.2f" % v, 12, color="#555555")
        line([(px, yy), (px + W, yy)], arrow=False, color="#e2e2e2")
    n = len(cats)
    for i, c in enumerate(cats):
        xx = px + 30 + (W - 60) * i / max(n - 1, 1)
        text(xx - tw(c, 12, FONT_SANS) / 2, py + H + 6, c, 12, color="#555555")
    for si, s in enumerate(series):
        pts = [(px + 30 + (W - 60) * i / max(n - 1, 1), py + H - H * (v - ymin) / (ymax - ymin)) for i, v in enumerate(s)]
        line(pts, color=PAL[si % 4], sw=3, arrow=False)
        for p_ in pts: rect(p_[0] - 4, p_[1] - 4, 8, 8, bg=PAL[si % 4], stroke=PAL[si % 4], t="ellipse")
    text(px, py + H + 30, "x: " + xa.group(1) + "     y: " + ya.group(1) + "     lines in order: " + ", ".join(PAL_NAMES[:len(series)]), 12, color="#666666")
    return W + 90, H + 90
PAL_NAMES = ["orange", "teal", "violet", "amber"]

def draw_pie(src, x0, y0):
    title = re.search(r'title\s+"(.*?)"', src); title = title.group(1) if title else ""
    items = re.findall(r'"(.*?)"\s*:\s*([\d.]+)', src)
    text(x0, y0, title, 16, color="#333333"); y = y0 + 34
    tot = sum(float(v) for _, v in items)
    for i, (l, v) in enumerate(items):
        w = 360 * float(v) / tot
        rect(x0 + 90, y, w, 30, bg=BR_COL[i % 8], stroke=PAL[i % 4])
        text(x0, y + 5, l, 15); text(x0 + 100 + w, y + 5, "%g%%" % (100 * float(v) / tot), 14, color="#555555"); y += 42
    return 520, y - y0
