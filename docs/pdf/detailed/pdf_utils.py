"""
============================================================================
 FSBM Platform - Infrastructure PDF partagée pour les 10 PDFs detailles
============================================================================
Tous les generateurs PDF dans detailed/ importent ce module pour reutiliser
les styles, helpers et widgets visuels communs.

USAGE :
    from pdf_utils import (
        build_doc, ST_TITLE, ST_CHAPTER, ST_H1, ST_H2, ST_H3,
        ST_BODY, ST_CODE, ST_LIST,
        code, diagram, analogy, alert_box, std_table, cover_page,
    )
============================================================================
"""

from __future__ import annotations
import sys
from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image,
    Table, TableStyle,
)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ─── Palette FSBM ────────────────────────────────────────────────────────────
PRIMARY      = HexColor('#1C3F6E')
PRIMARY_MID  = HexColor('#265DAB')
PRIMARY_LT   = HexColor('#3A7BD5')
PRIMARY_PALE = HexColor('#EBF2FB')
ACCENT       = HexColor('#16B5A6')
ACCENT_MID   = HexColor('#0E9B8C')
ACCENT_PALE  = HexColor('#E5F8F5')
GREY_DARK    = HexColor('#2D3748')
GREY_MID     = HexColor('#4A5568')
GREY_LIGHT   = HexColor('#EDF1F6')
SUCCESS      = HexColor('#22C55E')
SUCCESS_PALE = HexColor('#F0FDF4')
WARNING      = HexColor('#F59E0B')
WARNING_PALE = HexColor('#FFFBEB')
DANGER       = HexColor('#EF4444')
DANGER_PALE  = HexColor('#FEF2F2')
INFO         = HexColor('#3B82F6')
INFO_PALE    = HexColor('#EBF5FF')
PURPLE       = HexColor('#A855F7')
PURPLE_PALE  = HexColor('#FAF5FF')
PINK         = HexColor('#EC4899')
PINK_PALE    = HexColor('#FCE7F3')

# ─── Path racine ─────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent.parent.parent
LOGO_FSBM = ROOT / "frontend" / "src" / "assets" / "logos" / "fsbm.png"

# ─── Styles partages ─────────────────────────────────────────────────────────
_base = getSampleStyleSheet()

ST_TITLE = ParagraphStyle('T', parent=_base['Title'], fontName='Helvetica-Bold',
    fontSize=32, textColor=PRIMARY, alignment=TA_CENTER, spaceAfter=14, leading=38)
ST_SUBTITLE = ParagraphStyle('S', parent=_base['Heading2'], fontName='Helvetica',
    fontSize=15, textColor=ACCENT, alignment=TA_CENTER, spaceAfter=10, leading=20)
ST_CHAPTER = ParagraphStyle('Ch', parent=_base['Heading1'], fontName='Helvetica-Bold',
    fontSize=23, textColor=PRIMARY, alignment=TA_LEFT, spaceBefore=20, spaceAfter=13, leading=29)
ST_H1 = ParagraphStyle('H1', parent=_base['Heading1'], fontName='Helvetica-Bold',
    fontSize=16, textColor=PRIMARY, spaceBefore=14, spaceAfter=10, leading=21)
ST_H2 = ParagraphStyle('H2', parent=_base['Heading2'], fontName='Helvetica-Bold',
    fontSize=13, textColor=PRIMARY_MID, spaceBefore=11, spaceAfter=7, leading=17)
ST_H3 = ParagraphStyle('H3', parent=_base['Heading3'], fontName='Helvetica-Bold',
    fontSize=11.5, textColor=GREY_DARK, spaceBefore=9, spaceAfter=5, leading=15)
ST_BODY = ParagraphStyle('B', parent=_base['BodyText'], fontName='Helvetica',
    fontSize=10.5, textColor=GREY_DARK, alignment=TA_JUSTIFY, spaceAfter=8, leading=15)
ST_BODY_BOLD = ParagraphStyle('BB', parent=ST_BODY, fontName='Helvetica-Bold')
ST_CODE = ParagraphStyle('C', parent=_base['Code'], fontName='Courier',
    fontSize=8.5, textColor=PRIMARY_MID, backColor=GREY_LIGHT,
    leftIndent=12, rightIndent=12, spaceAfter=8, leading=12, borderPadding=8,
    borderColor=PRIMARY_MID, borderWidth=0.5)
ST_LIST = ParagraphStyle('L', parent=ST_BODY, leftIndent=14, bulletIndent=4)
ST_NOTE = ParagraphStyle('N', parent=ST_BODY, fontName='Helvetica-Oblique', textColor=GREY_MID)
ST_TOC = ParagraphStyle('TC', parent=ST_BODY, fontSize=11, spaceAfter=4, leading=16)
ST_DIAGRAM = ParagraphStyle('D', parent=ST_CODE, alignment=TA_CENTER, leading=11)


# ─── Widgets visuels ─────────────────────────────────────────────────────────
def _escape_html(text: str) -> str:
    """Echape les caracteres reserves de l'XML/HTML que ReportLab interprete."""
    return (text
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;'))


def code(text: str):
    """Bloc de code formaté (echape les balises HTML)."""
    safe = _escape_html(text)
    return Paragraph(safe.replace('\n', '<br/>').replace(' ', '&nbsp;'), ST_CODE)


def diagram(text: str):
    """Diagramme ASCII centré (echape les balises HTML)."""
    safe = _escape_html(text)
    return Paragraph(safe.replace('\n', '<br/>').replace(' ', '&nbsp;'), ST_DIAGRAM)


def analogy(content: str):
    """Boîte 'analogie' pour vulgarisation."""
    t = Table([[Paragraph(
        f'<font color="{PURPLE.hexval()}"><b>🔮 ANALOGIE :</b></font> {content}',
        ST_BODY)]], colWidths=[16*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PURPLE_PALE),
        ('LINEBEFORE', (0,0), (-1,-1), 4, PURPLE),
        ('PADDING',    (0,0), (-1,-1), 10),
    ]))
    return t


def alert_box(content: str, kind: str = "info", title: str = None):
    """Boîte d'alerte info/warning/success/tip/key/danger."""
    colors = {
        "info":    (INFO,    INFO_PALE,    "ℹ"),
        "warning": (WARNING, WARNING_PALE, "⚠"),
        "success": (SUCCESS, SUCCESS_PALE, "✓"),
        "tip":     (ACCENT,  ACCENT_PALE,  "★"),
        "key":     (PINK,    PINK_PALE,    "🔑"),
        "danger":  (DANGER,  DANGER_PALE,  "✗"),
        "purple":  (PURPLE,  PURPLE_PALE,  "?"),
    }
    border, bg, icon = colors.get(kind, colors["info"])
    if title:
        text_html = f'<font color="{border.hexval()}"><b>[{icon}] {title}</b></font><br/>{content}'
    else:
        text_html = f'<font color="{border.hexval()}"><b>[{icon}]</b></font> {content}'
    t = Table([[Paragraph(text_html, ST_BODY)]], colWidths=[16*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('LINEBEFORE', (0,0), (-1,-1), 4, border),
        ('PADDING',    (0,0), (-1,-1), 10),
    ]))
    return t


def std_table(rows, header_color=PRIMARY, col_widths=None):
    """Tableau standardisé avec en-tête colorée."""
    if col_widths is None:
        col_widths = [16/len(rows[0])*cm]*len(rows[0])
    data = [[Paragraph(f'<b>{c}</b>', ST_BODY_BOLD) if i == 0 else Paragraph(c, ST_BODY)
             for c in row] for i, row in enumerate(rows)]
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), header_color),
        ('TEXTCOLOR',  (0,0), (-1,0), white),
        ('BOX',        (0,0), (-1,-1), 0.4, GREY_LIGHT),
        ('INNERGRID',  (0,0), (-1,-1), 0.3, GREY_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, GREY_LIGHT]),
        ('PADDING',    (0,0), (-1,-1), 6),
        ('VALIGN',     (0,0), (-1,-1), 'TOP'),
    ]))
    return t


def bullet(items: list, marker: str = "•"):
    """Liste à puces formatée."""
    return [Paragraph(f"{marker} {it}", ST_LIST) for it in items]


def toc_entry(label: str, page: str):
    """Entrée de table des matières."""
    dots = '.' * max(1, 78 - len(label) - len(page))
    return Paragraph(
        f"{label} <font color='#8095A8'>{dots}</font> <b>{page}</b>", ST_TOC)


# ─── Header / Footer ────────────────────────────────────────────────────────
def make_header_footer(pdf_title: str, project_subtitle: str = "FSBM Platform - PFE 2025/2026"):
    """Fabrique de fonction header/footer parametree par PDF."""
    def header_footer(c, doc):
        c.saveState()
        # Footer
        c.setStrokeColor(GREY_LIGHT); c.setLineWidth(0.5)
        c.line(2*cm, 1.5*cm, A4[0]-2*cm, 1.5*cm)
        c.setFont('Helvetica', 8); c.setFillColor(GREY_MID)
        c.drawString(2*cm, 1*cm, pdf_title)
        c.drawCentredString(A4[0]/2, 1*cm, project_subtitle)
        c.drawRightString(A4[0]-2*cm, 1*cm, f"Page {doc.page}")
        # Header (sauf page de garde)
        if doc.page > 1:
            c.setFont('Helvetica', 8); c.setFillColor(PRIMARY)
            c.drawString(2*cm, A4[1]-1*cm, "Faculte des Sciences Ben M'Sick - Universite Hassan II")
            c.line(2*cm, A4[1]-1.2*cm, A4[0]-2*cm, A4[1]-1.2*cm)
        c.restoreState()
    return header_footer


# ─── Page de garde standard ──────────────────────────────────────────────────
def cover_page(story, pdf_number: str, title_main: str, subtitle: str,
               accent_color=PRIMARY, banner_label: str = "Documentation PFE"):
    """Construit la page de garde standardisee."""
    story.append(Spacer(1, 2*cm))
    if LOGO_FSBM.exists():
        story.append(Image(str(LOGO_FSBM), width=5.5*cm, height=5.5*cm, hAlign='CENTER'))
    story.append(Spacer(1, 0.8*cm))
    story.append(Paragraph("UNIVERSITE HASSAN II DE CASABLANCA", ST_SUBTITLE))
    story.append(Paragraph("FACULTE DES SCIENCES BEN M'SICK", ST_SUBTITLE))
    story.append(Spacer(1, 0.5*cm))
    # Numero du PDF
    badge = Table([[Paragraph(f'<font color="#FFFFFF"><b>{banner_label} - {pdf_number}</b></font>',
                              ST_BODY)]], colWidths=[12*cm], hAlign='CENTER')
    badge.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), accent_color),
        ('PADDING',    (0,0), (-1,-1), 12),
        ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(badge)
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(title_main, ST_TITLE))
    story.append(Paragraph(subtitle, ST_SUBTITLE))
    story.append(Spacer(1, 2*cm))
    # Equipe
    authors = Table([
        [Paragraph('<b>Realise par :</b>', ST_BODY_BOLD)],
        [Paragraph('AKRAM BELMOUSSA - Backend &amp; Integration NLP', ST_BODY)],
        [Paragraph('ZAKARIA - Frontend Angular &amp; UX/UI', ST_BODY)],
        [Paragraph('NOUHAILA - Base de donnees &amp; Contenu FAQ', ST_BODY)],
    ], colWidths=[12*cm], hAlign='CENTER')
    authors.setStyle(TableStyle([
        ('PADDING', (0,0), (-1,-1), 5),
        ('LINEABOVE', (0,1), (-1,1), 1, ACCENT),
    ]))
    story.append(authors)
    story.append(Spacer(1, 0.6*cm))
    story.append(Paragraph(f"{datetime.now().strftime('%B %Y').upper()}",
        ParagraphStyle('D', parent=ST_BODY, alignment=TA_CENTER, fontSize=11, textColor=GREY_MID)))
    story.append(PageBreak())


def build_doc(out_filename: str, story: list, pdf_header_title: str, doc_title: str, doc_author: str = "AKRAM BELMOUSSA, ZAKARIA, NOUHAILA"):
    """Construit et sauve le PDF."""
    out_path = Path(__file__).parent / out_filename
    doc = SimpleDocTemplate(
        str(out_path), pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title=doc_title, author=doc_author,
    )
    hf = make_header_footer(pdf_header_title)
    doc.build(story, onFirstPage=hf, onLaterPages=hf)
    size_kb = out_path.stat().st_size / 1024
    print(f"PDF genere : {out_path.name} ({size_kb:.1f} KB)")
    return out_path
