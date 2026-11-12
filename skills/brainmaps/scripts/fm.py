import re, os, hashlib, subprocess, base64, struct, concurrent.futures as cf, shutil
SYM = {'ĝ':r'\hat{g}','r\u0302':r'\hat{r}','\u0302':'','Â':r'\hat{A}','π':r'\pi','θ':r'\theta','γ':r'\gamma','λ':r'\lambda','δ':r'\delta','ε':r'\epsilon','ρ':r'\rho','β':r'\beta','σ':r'\sigma',
 'μ':r'\mu','ψ':r'\psi','φ':r'\phi','α':r'\alpha','η':r'\eta','τ':r'\tau','ω':r'\omega','Δ':r'\Delta','Σ':r'\sum','∇':r'\nabla','∂':r'\partial',
 '≈':r'\approx','≥':r'\ge','≤':r'\le','∝':r'\propto','→':r'\to','∞':r'\infty','×':r'\times','·':r'\cdot','−':'-','–':'-','≻':r'\succ',
 '⁺':'^{+}','⁻':'^{-}','∈':r'\in','…':r'\ldots','₀':'_0','₁':'_1','₂':'_2','²':'^2','³':'^3','±':r'\pm','≠':r'\ne','∑':r'\sum','√':r'\sqrt{}',
 'ν':r'\nu','κ':r'\kappa','ξ':r'\xi','Π':r'\prod','∏':r'\prod','⊂':r'\subset','ϵ':r'\epsilon','₃':'_3','₄':'_4','₅':'_5','c₁':'c_1','c₂':'c_2',
 '‖':r'\Vert','·':r'\cdot','ℝ':r'\mathbb{R}','∣':'|'}
FUN = {'log':r'\log','exp':r'\exp','min':r'\min','max':r'\max','ln':r'\ln','sqrt':r'\sqrt'}
BAD = ('None','beta =','num_gen','==')
def is_formula(x):
    return len(x) >= 6 and any(c in x for c in "=Σ∇≈∝≻∈") and not re.search(r"[a-z]{3,}_[a-z]{3,}", x) and not any(b in x for b in BAD)
def to_tex(s):
    s = s.replace('\\|', '|').replace('||', ' \\Vert ')
    s = s.replace('%', r'\%').replace('&', r'\&').replace('#', r'\#').replace('~', r'\sim ').replace('·,', r'\cdot,')
    def word(m):
        w = m.group(0)
        if w in FUN: return FUN[w]
        return r'\mathrm{%s}' % w
    s = re.sub(r'(?<![\\A-Za-z])[A-Za-z]{2,}(?![A-Za-z])', word, s)
    for k in sorted(SYM, key=len, reverse=True): s = s.replace(k, SYM[k] + (' ' if SYM[k][:1] == '\\' else ''))
    s = re.sub(r'\bc_1\b', 'c_1', s)
    return s
HDR = r"\documentclass[border=3pt,preview]{standalone}\usepackage{amsmath,amssymb}\begin{document}"
def key(tex): return hashlib.md5(tex.encode()).hexdigest()[:12]
HDR2 = r"\documentclass[border={0.6pt 3pt},preview]{standalone}\usepackage{amsmath,amssymb,xcolor}\begin{document}"
def build_one(tex, seg=False):
    k = key(("SEG" if seg else "") + tex); png = "fcache/%s.png" % k
    if os.path.exists(png): return k
    d = "fcache/w_%s" % k; os.makedirs(d, exist_ok=True)
    open(d + "/f.tex", "w").write((HDR2 if seg else HDR) + "$\\displaystyle " + tex + "$\\end{document}")
    if not shutil.which("pdflatex") or not shutil.which("pdftocairo"):
        open("fcache/%s.fail" % k, "w").write("Math tools missing: pdflatex and pdftocairo\n" + tex)
        return None
    try:
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "f.tex"], cwd=d, capture_output=True, timeout=60)
        if r.returncode != 0 or not os.path.exists(d + "/f.pdf"):
            open("fcache/%s.fail" % k, "w").write(tex); return None
        r = subprocess.run(["pdftocairo", "-png", "-r", "220", "-transp", "-singlefile", d + "/f.pdf", d + "/o"], capture_output=True, timeout=60)
        if r.returncode != 0 or not os.path.exists(d + "/o.png"):
            open("fcache/%s.fail" % k, "w").write(tex); return None
        os.replace(d + "/o.png", png); return k
    except (OSError, subprocess.TimeoutExpired) as exc:
        open("fcache/%s.fail" % k, "w").write(f"Math rendering failed: {exc}\n{tex}")
        return None
def png_size(path):
    with open(path, "rb") as f: b = f.read(24)
    return struct.unpack(">II", b[16:24])
_cache = {}
def get(tex, seg=False):
    """returns (fileid, w, h) or None"""
    if (tex, seg) in _cache: return _cache[(tex, seg)]
    k = build_one(tex, seg); r = None
    if k:
        w, h = png_size("fcache/%s.png" % k); r = (k, w, h)
    _cache[(tex, seg)] = r; return r
def prebuild(texes):
    with cf.ThreadPoolExecutor(8) as ex: list(ex.map(build_one, set(texes)))
