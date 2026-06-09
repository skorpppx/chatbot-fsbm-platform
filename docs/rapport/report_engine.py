# -*- coding: utf-8 -*-
"""
Moteur de generation du rapport PFE FSBM.
- Styles type ecole d'ingenieurs (ENSA/EMI/INPT)
- Table des matieres + liste des figures + liste des tableaux (pages auto)
- Diagrammes UML via Mermaid (mermaid.ink) avec cache local
- Graphiques via matplotlib
- Page de garde, en-tetes/pieds, numerotation chapitres/figures/tableaux
"""
import os, sys, io, json, base64, hashlib, urllib.request

sys.stdout.reconfigure(encoding="utf-8")

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image,
    Table, TableStyle, PageBreak, KeepTogether, Flowable, NextPageTemplate,
    CondPageBreak,
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.utils import ImageReader

# ─── CHEMINS ──────────────────────────────────────────────────────────────────
BASE       = os.path.dirname(os.path.abspath(__file__))
ASSETS     = os.path.join(BASE, "assets")
os.makedirs(ASSETS, exist_ok=True)
PROJECT    = r"C:\Users\belmo\studies\PFE\chatbot-fsbm-platform"
SHOTS      = os.path.join(PROJECT, "Screen-shot")
LOGO_FSBM  = r"C:\Users\belmo\Downloads\logo fsbm\WhatsApp_Image_2023-10-30_at_13.52.46_2037cc1a-removebg-preview.png"
LOGO_DEPT  = r"C:\Users\belmo\Downloads\logo fsbm\logo_departement-removebg-preview (3).png"

def shot(idx):
    """Retourne le chemin du screenshot numero idx (1..23)."""
    files = sorted(f for f in os.listdir(SHOTS) if f.lower().endswith(".png"))
    return os.path.join(SHOTS, files[idx-1])

# ─── PALETTE ──────────────────────────────────────────────────────────────────
NAVY    = HexColor("#1C3F6E")   # bleu FSBM
NAVY_D  = HexColor("#13294B")
BLUE    = HexColor("#2d5a9e")
ACCENT  = HexColor("#FF6B35")   # orange
TEAL    = HexColor("#13A89E")   # vert dept
INK     = HexColor("#1a2233")
MUTED   = HexColor("#5b6577")
LIGHT   = HexColor("#eef2f7")
LINE    = HexColor("#d6deea")
CODE_BG = HexColor("#0f1b2d")
CODE_FG = HexColor("#d7e3f4")
GREEN   = HexColor("#1a7a3d")
RED     = HexColor("#c0392b")
AMBER   = HexColor("#b45309")

# ─── GEOMETRIE ────────────────────────────────────────────────────────────────
PW, PH   = A4
LM, RM   = 2.4*cm, 2.2*cm
TM, BM   = 2.8*cm, 2.6*cm
CONTENT_W = PW - LM - RM
CONTENT_H = PH - TM - BM

# ─── STYLES ───────────────────────────────────────────────────────────────────
_ss = getSampleStyleSheet()
def _mk(name, **kw):
    kw.setdefault("fontName", "Helvetica")
    return ParagraphStyle(name, parent=_ss["Normal"], **kw)

ST = {
    "title":   _mk("title", fontName="Helvetica-Bold", fontSize=26, leading=31,
                   textColor=NAVY, alignment=TA_CENTER),
    "subtitle":_mk("subtitle", fontSize=14, leading=19, textColor=MUTED, alignment=TA_CENTER),
    "ch":      _mk("Ch", fontName="Helvetica-Bold", fontSize=20, leading=25,
                   textColor=NAVY, spaceBefore=4, spaceAfter=14),
    "chx":     _mk("ChX", fontName="Helvetica-Bold", fontSize=20, leading=25,
                   textColor=NAVY, spaceBefore=4, spaceAfter=10),
    "h1n":     _mk("H1n", fontName="Helvetica-Bold", fontSize=15, leading=20,
                   textColor=NAVY_D, spaceBefore=18, spaceAfter=9),
    "h2n":     _mk("H2n", fontName="Helvetica-Bold", fontSize=12.5, leading=17,
                   textColor=BLUE, spaceBefore=13, spaceAfter=6),
    "h3n":     _mk("H3n", fontName="Helvetica-BoldOblique", fontSize=10.5, leading=14,
                   textColor=INK, spaceBefore=8, spaceAfter=3),
    "body":    _mk("body", fontSize=11.5, leading=21, textColor=INK,
                   alignment=TA_JUSTIFY, spaceAfter=13),
    "bullet":  _mk("bullet", fontSize=11, leading=16.5, textColor=INK,
                   alignment=TA_JUSTIFY, leftIndent=16, spaceAfter=5, bulletIndent=4),
    "num":     _mk("num", fontSize=11, leading=16.5, textColor=INK,
                   alignment=TA_JUSTIFY, leftIndent=18, spaceAfter=5),
    "figcap":  _mk("FigCap", fontSize=9, leading=12, textColor=MUTED,
                   alignment=TA_CENTER, spaceBefore=4, spaceAfter=10),
    "tblcap":  _mk("TblCap", fontSize=9, leading=12, textColor=MUTED,
                   alignment=TA_CENTER, spaceBefore=8, spaceAfter=4),
    "code":    _mk("code", fontName="Courier", fontSize=8.0, leading=10.6,
                   textColor=CODE_FG, backColor=CODE_BG, borderPadding=8,
                   leftIndent=2, spaceBefore=4, spaceAfter=8),
    "quote":   _mk("quote", fontSize=10.5, leading=16, textColor=NAVY_D,
                   alignment=TA_JUSTIFY, leftIndent=14, rightIndent=10,
                   fontName="Helvetica-Oblique", spaceBefore=4, spaceAfter=8),
    "small":   _mk("small", fontSize=8.6, leading=11.5, textColor=MUTED),
    "cell":    _mk("cell", fontSize=8.8, leading=11.5, textColor=INK),
    "cellb":   _mk("cellb", fontName="Helvetica-Bold", fontSize=8.8, leading=11.5, textColor=colors.white),
    "cellc":   _mk("cellc", fontSize=8.8, leading=11.5, textColor=INK, alignment=TA_CENTER),
}

# ─── ETAT (numerotation) ──────────────────────────────────────────────────────
_n = {"ch": 0, "sec": 0, "sub": 0, "fig": 0, "tbl": 0}
_state = {"chapter": ""}

def reset_numbering():
    _n.update(ch=0, sec=0, sub=0, fig=0, tbl=0)

def _esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

# ─── TITRES ───────────────────────────────────────────────────────────────────
def chapter(title):
    _n["ch"] += 1; _n["sec"] = 0; _n["sub"] = 0
    p = Paragraph(f"Chapitre {_n['ch']} &nbsp;&middot;&nbsp; {_esc(title)}", ST["ch"])
    p._chapnum = _n["ch"]; p._chaptitle = title
    return [NextPageTemplate("normal"), PageBreak(), _ChapterBanner(_n["ch"], title), p]

def front_chapter(title):
    """Section liminaire non numerotee, presente dans la TOC."""
    p = Paragraph(_esc(title), ST["ch"]); p._front = True
    return [PageBreak(), p, _hr(NAVY, 1.4), Spacer(1, 6)]

def plain_heading(title, brk=True):
    """Titre visuel non capture par la TOC (pour TOC/listes elles-memes)."""
    p = Paragraph(_esc(title), ST["chx"])
    out = [p, _hr(NAVY, 1.4), Spacer(1, 6)]
    return ([PageBreak()] + out) if brk else out

def section(title):
    _n["sec"] += 1; _n["sub"] = 0
    return Paragraph(f'<font color="#2d5a9e">{_n["ch"]}.{_n["sec"]}</font>&nbsp;&nbsp;{_esc(title)}', ST["h1n"])

def subsection(title):
    _n["sub"] += 1
    return Paragraph(f'<font color="#5b6577">{_n["ch"]}.{_n["sec"]}.{_n["sub"]}</font>&nbsp;&nbsp;{_esc(title)}', ST["h2n"])

def h3(title):
    return Paragraph(_esc(title), ST["h3n"])

# ─── PARAGRAPHES ──────────────────────────────────────────────────────────────
def para(text):       return Paragraph(text, ST["body"])
def quote(text, by=None):
    t = f'&ldquo;{text}&rdquo;'
    if by: t += f'<br/><font size=9 color="#5b6577">— {by}</font>'
    return Paragraph(t, ST["quote"])

def bullets(items):
    return [Paragraph(f"• {it}", ST["bullet"]) for it in items]

def numbered(items):
    return [Paragraph(f'<font color="#2d5a9e"><b>{i}.</b></font>&nbsp;&nbsp;{it}', ST["num"])
            for i, it in enumerate(items, 1)]

def spacer(h=0.4):    return Spacer(1, h*cm)
def pagebreak():      return PageBreak()

def code(text, caption=None):
    safe = _esc(text).replace("\n", "<br/>").replace(" ", "&nbsp;")
    out = [Paragraph(safe, ST["code"])]
    if caption:
        _n["tbl"]  # noop
        out.append(Paragraph(f'<i>{_esc(caption)}</i>', ST["small"]))
    return out

# ─── ENCADRES ─────────────────────────────────────────────────────────────────
def alert(text, kind="info"):
    cfg = {"info": (LIGHT, NAVY, "i"), "tip": (HexColor("#e7f7ec"), GREEN, "+"),
           "warn": (HexColor("#fef3e8"), AMBER, "!"), "danger": (HexColor("#fdecec"), RED, "x"),
           "key": (HexColor("#eef4ff"), BLUE, "*")}
    bg, bd, sym = cfg.get(kind, cfg["info"])
    st = ParagraphStyle("al", parent=ST["body"], backColor=bg, borderColor=bd,
                        borderWidth=0.8, borderPadding=9, leftIndent=4, spaceBefore=4, spaceAfter=8)
    hexcol = "#" + bd.hexval()[2:8]
    return Paragraph(f'<b><font color="{hexcol}">[{sym}]</font></b>&nbsp; {text}', st)

class _hr(Flowable):
    def __init__(self, color=LINE, w=0.8, width=None, pad=2):
        super().__init__(); self.color=color; self.w=w; self.width=width; self.pad=pad
    def wrap(self, aw, ah): self._w = self.width or aw; return (self._w, self.w + 2*self.pad)
    def draw(self):
        self.canv.setStrokeColor(self.color); self.canv.setLineWidth(self.w)
        self.canv.line(0, self.pad, self._w, self.pad)
def hr(color=LINE, w=0.8): return _hr(color, w)

class _ChapterBanner(Flowable):
    """Gros numero de chapitre decoratif."""
    def __init__(self, num, title): super().__init__(); self.num=num; self.title=title
    def wrap(self, aw, ah): self._w=aw; return (aw, 1.5*cm)
    def draw(self):
        c=self.canv; c.setFillColor(LIGHT); c.roundRect(0,0,self._w,1.4*cm,6,fill=1,stroke=0)
        c.setFillColor(NAVY); c.rect(0,0,0.5*cm,1.4*cm,fill=1,stroke=0)
        c.setFillColor(NAVY); c.setFont("Helvetica-Bold",26)
        c.drawString(0.9*cm,0.36*cm,f"{self.num:02d}")
        c.setFillColor(MUTED); c.setFont("Helvetica",9)
        c.drawString(2.4*cm,0.55*cm,"CHAPITRE")

# ─── IMAGES ───────────────────────────────────────────────────────────────────
def _scaled(path, max_w=None, max_h=20*cm):
    max_w = max_w or CONTENT_W
    try:
        iw, ih = ImageReader(path).getSize()
    except Exception:
        return Spacer(1, 1*cm)
    r = min(max_w/iw, max_h/ih)
    return Image(path, iw*r, ih*r)

def figure_img(path, caption, max_h=15*cm, max_w=None, border=True):
    _n["fig"] += 1
    img = _scaled(path, max_w, max_h)
    if border:
        inner = Table([[img]], colWidths=[img.drawWidth])
        inner.setStyle(TableStyle([("BOX",(0,0),(-1,-1),0.8,LINE),
                                 ("BACKGROUND",(0,0),(-1,-1),colors.white),
                                 ("LEFTPADDING",(0,0),(-1,-1),3),("RIGHTPADDING",(0,0),(-1,-1),3),
                                 ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
        ih = img.drawHeight + 8
    else:
        inner = img; ih = img.drawHeight
    inner.hAlign = "CENTER"
    cap = Paragraph(f"<b>Figure {_n['fig']}</b> — {_esc(caption)}", ST["figcap"])
    cap._islof = True
    # CondPageBreak garde l'image et sa legende sur la meme page sans masquer la notify TOC
    return [Spacer(1, 10), CondPageBreak(min(ih + 1.4*cm, CONTENT_H)), inner, cap, Spacer(1, 12)]

# ─── MERMAID ──────────────────────────────────────────────────────────────────
def _mermaid_png(code_str):
    h = hashlib.md5(code_str.encode()).hexdigest()[:16]
    path = os.path.join(ASSETS, f"mer_{h}.png")
    if os.path.exists(path) and os.path.getsize(path) > 800:
        return path
    payload = json.dumps({"code": code_str, "mermaid": {"theme": "default"}}).encode()
    b64 = base64.urlsafe_b64encode(payload).decode()
    for url in (f"https://mermaid.ink/img/{b64}",
                f"https://mermaid.ink/img/{b64}?type=png"):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=30).read()
            if data[:4] == b"\x89PNG" and len(data) > 800:
                open(path, "wb").write(data); return path
        except Exception as e:
            print("  [mermaid] retry:", repr(e)[:90])
    return None

def figure_mermaid(code_str, caption, max_h=18*cm, max_w=None):
    path = _mermaid_png(code_str)
    if not path:
        # fallback : afficher le code source encadre
        _n["fig"] += 1
        return [Paragraph(f"<b>Figure {_n['fig']}</b> — {_esc(caption)} (rendu indisponible)", ST["figcap"]),
                Paragraph(_esc(code_str).replace("\n","<br/>").replace(" ","&nbsp;"), ST["code"])]
    return figure_img(path, caption, max_h=max_h, max_w=max_w, border=False)

# ─── GRAPHIQUES (matplotlib) ──────────────────────────────────────────────────
def chart(draw_fn, caption, w_cm=15, h_cm=8.5, dpi=150):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    h = hashlib.md5((caption+str(w_cm)+str(h_cm)).encode()).hexdigest()[:12]
    path = os.path.join(ASSETS, f"chart_{h}.png")
    fig = plt.figure(figsize=(w_cm/2.54, h_cm/2.54), dpi=dpi)
    draw_fn(fig)
    fig.savefig(path, bbox_inches="tight", facecolor="white"); plt.close(fig)
    return figure_img(path, caption, max_h=h_cm*cm*1.1, border=False)

# ─── TABLEAUX ─────────────────────────────────────────────────────────────────
def table(rows, caption, col_widths=None, header=True, align=None, font=8.8):
    _n["tbl"] += 1
    data = []
    for ri, row in enumerate(rows):
        cells = []
        for ci, c in enumerate(row):
            if ri == 0 and header:
                cells.append(Paragraph(f"<b>{_esc(str(c))}</b>", ST["cellb"]))
            else:
                cells.append(Paragraph(_esc(str(c)).replace("\n","<br/>"), ST["cell"]))
        data.append(cells)
    if col_widths:
        total = sum(col_widths); col_widths = [w/total*CONTENT_W for w in col_widths]
    else:
        col_widths = [CONTENT_W/len(rows[0])]*len(rows[0])
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    style = [
        ("BACKGROUND",(0,0),(-1,0), NAVY if header else colors.white),
        ("GRID",(0,0),(-1,-1),0.5, LINE),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, HexColor("#f5f8fc")]),
    ]
    if align:
        for ci, a in enumerate(align):
            if a: style.append(("ALIGN",(ci,0),(ci,-1), a.upper()))
    t.setStyle(TableStyle(style))
    cap = Paragraph(f"<b>Tableau {_n['tbl']}</b> — {_esc(caption)}", ST["tblcap"])
    cap._islot = True
    return [Spacer(1,8), cap, t, Spacer(1,12)]

# ─── TABLES DES MATIERES / FIGURES / TABLEAUX ─────────────────────────────────
class _Index(TableOfContents):
    notifyKind = "TOCEntry"
    def notify(self, kind, stuff):
        if kind == self.notifyKind:
            self.addEntry(*stuff)

def make_toc():
    t = _Index(); t.notifyKind = "TOCEntry"
    t.levelStyles = [
        ParagraphStyle("toc0", fontName="Helvetica-Bold", fontSize=11, leading=20,
                       textColor=NAVY, spaceBefore=6),
        ParagraphStyle("toc1", fontName="Helvetica", fontSize=10, leading=16,
                       textColor=INK, leftIndent=18),
        ParagraphStyle("toc2", fontName="Helvetica", fontSize=9.2, leading=14,
                       textColor=MUTED, leftIndent=36),
    ]
    t.dotsMinLevel = 0
    return t

def make_list(kind):
    t = _Index(); t.notifyKind = kind
    t.levelStyles = [ParagraphStyle("li", fontName="Helvetica", fontSize=9.6, leading=16,
                                    textColor=INK, leftIndent=4)]
    t.dotsMinLevel = 0
    return t

# ─── DOCUMENT ─────────────────────────────────────────────────────────────────
class ReportDoc(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, pagesize=A4, leftMargin=LM, rightMargin=RM,
                         topMargin=TM, bottomMargin=BM, title=kw.get("title",""),
                         author=kw.get("author",""))
        frame = Frame(LM, BM, CONTENT_W, CONTENT_H, id="f")
        self.addPageTemplates([
            PageTemplate(id="cover", frames=[frame], onPage=self._blank),
            PageTemplate(id="normal", frames=[frame], onPage=self._deco),
        ])
        self._title = kw.get("title", "Rapport PFE")

    def _blank(self, canv, doc): pass

    def _deco(self, canv, doc):
        canv.saveState()
        # Header
        canv.setStrokeColor(LINE); canv.setLineWidth(0.6)
        canv.line(LM, PH-TM+0.5*cm, PW-RM, PH-TM+0.5*cm)
        canv.setFont("Helvetica", 7.5); canv.setFillColor(MUTED)
        canv.drawString(LM, PH-TM+0.62*cm, "Plateforme Universitaire Intelligente FSBM")
        ch = _state.get("chapter","")
        if ch:
            canv.drawRightString(PW-RM, PH-TM+0.62*cm, ch[:70])
        # Footer
        canv.setStrokeColor(LINE); canv.line(LM, BM-0.45*cm, PW-RM, BM-0.45*cm)
        canv.setFont("Helvetica", 8); canv.setFillColor(MUTED)
        canv.drawString(LM, BM-0.85*cm, "PFE 2025/2026 — FSBM, Universite Hassan II de Casablanca")
        canv.setFont("Helvetica-Bold", 9); canv.setFillColor(NAVY)
        canv.drawRightString(PW-RM, BM-0.85*cm, str(canv.getPageNumber()))
        canv.restoreState()

    def afterFlowable(self, flowable):
        if not isinstance(flowable, Paragraph):
            return
        style = flowable.style.name
        txt = flowable.getPlainText()
        if style == "ChX":
            _state["chapter"] = txt   # MAJ en-tete sans entree TOC (pages sommaire/listes)
            return
        if style == "Ch":
            _state["chapter"] = txt
            key = f"ch{getattr(flowable,'_chapnum','x')}_{abs(hash(txt))%99999}"
            self.canv.bookmarkPage(key); self.canv.addOutlineEntry(txt, key, level=0, closed=False)
            self.notify("TOCEntry", (0, txt, self.page, key))
        elif style == "H1n":
            key = f"s{abs(hash(txt))%999999}"
            self.canv.bookmarkPage(key); self.canv.addOutlineEntry(txt, key, level=1, closed=True)
            self.notify("TOCEntry", (1, txt, self.page, key))
        elif style == "H2n":
            self.notify("TOCEntry", (2, txt, self.page))
        elif style == "FigCap" and getattr(flowable, "_islof", False):
            self.notify("LOFEntry", (0, txt, self.page))
        elif style == "TblCap" and getattr(flowable, "_islot", False):
            self.notify("LOTEntry", (0, txt, self.page))


def build(filename, story, title="Rapport PFE", author=""):
    path = os.path.join(BASE, filename)
    doc = ReportDoc(path, title=title, author=author)
    doc.multiBuild(story)
    size = os.path.getsize(path)/1024
    print(f"[OK] {filename} genere — {size:.0f} KB")
    return path
