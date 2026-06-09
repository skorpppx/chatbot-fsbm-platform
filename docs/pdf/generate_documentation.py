"""
============================================================================
 FSBM Platform — Generateur de la DOCUMENTATION COMPLETE PEDAGOGIQUE
============================================================================
Documentation master du PFE, 60-80 pages, structuree en 16 chapitres,
destinee a la comprehension complete du projet pour soutenance et
maintenance future.
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
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image,
    Table, TableStyle, KeepTogether,
)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ─── Palette FSBM ─────────────────────────────────────────────────────────────
PRIMARY      = HexColor('#1C3F6E')
PRIMARY_MID  = HexColor('#265DAB')
PRIMARY_LIGHT= HexColor('#3A7BD5')
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
INFO         = HexColor('#3B82F6')
INFO_PALE    = HexColor('#EBF5FF')
PURPLE       = HexColor('#A855F7')
PURPLE_PALE  = HexColor('#FAF5FF')

ROOT = Path(__file__).parent.parent.parent
LOGO_FSBM = ROOT / "frontend" / "src" / "assets" / "logos" / "fsbm.png"

# ─── Styles ───────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

ST_COVER_TITLE = ParagraphStyle('CT', parent=styles['Title'], fontName='Helvetica-Bold',
    fontSize=34, textColor=PRIMARY, alignment=TA_CENTER, spaceAfter=18, leading=42)
ST_COVER_SUB = ParagraphStyle('CS', parent=styles['Heading2'], fontName='Helvetica',
    fontSize=17, textColor=ACCENT, alignment=TA_CENTER, spaceAfter=14, leading=22)
ST_CHAPTER = ParagraphStyle('Chapter', parent=styles['Heading1'], fontName='Helvetica-Bold',
    fontSize=24, textColor=PRIMARY, alignment=TA_LEFT, spaceBefore=24, spaceAfter=14, leading=30)
ST_H1 = ParagraphStyle('H1', parent=styles['Heading1'], fontName='Helvetica-Bold',
    fontSize=17, textColor=PRIMARY, spaceBefore=16, spaceAfter=10, leading=22)
ST_H2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName='Helvetica-Bold',
    fontSize=13.5, textColor=PRIMARY_MID, spaceBefore=12, spaceAfter=7, leading=18)
ST_H3 = ParagraphStyle('H3', parent=styles['Heading3'], fontName='Helvetica-Bold',
    fontSize=11.5, textColor=GREY_DARK, spaceBefore=10, spaceAfter=5, leading=15)
ST_BODY = ParagraphStyle('Body', parent=styles['BodyText'], fontName='Helvetica',
    fontSize=10.5, textColor=GREY_DARK, alignment=TA_JUSTIFY, spaceAfter=8, leading=15)
ST_BODY_BOLD = ParagraphStyle('BB', parent=ST_BODY, fontName='Helvetica-Bold')
ST_CODE = ParagraphStyle('Code', parent=styles['Code'], fontName='Courier',
    fontSize=8.5, textColor=PRIMARY_MID, backColor=GREY_LIGHT,
    leftIndent=12, rightIndent=12, spaceAfter=8, leading=12, borderPadding=8,
    borderColor=PRIMARY_MID, borderWidth=0.5)
ST_LIST = ParagraphStyle('List', parent=ST_BODY, leftIndent=14, bulletIndent=4)
ST_NOTE = ParagraphStyle('Note', parent=ST_BODY, fontName='Helvetica-Oblique',
    textColor=GREY_MID, leftIndent=20)
ST_TOC = ParagraphStyle('TOC', parent=ST_BODY, fontName='Helvetica', fontSize=11, spaceAfter=4, leading=16)
ST_DIAGRAM = ParagraphStyle('Diag', parent=ST_CODE, alignment=TA_CENTER, leading=11)


def header_footer(c, doc):
    c.saveState()
    c.setStrokeColor(GREY_LIGHT); c.setLineWidth(0.5)
    c.line(2*cm, 1.5*cm, A4[0]-2*cm, 1.5*cm)
    c.setFont('Helvetica', 8); c.setFillColor(GREY_MID)
    c.drawString(2*cm, 1*cm, "FSBM Platform - Documentation Complete")
    c.drawCentredString(A4[0]/2, 1*cm, "PFE 2025/2026")
    c.drawRightString(A4[0]-2*cm, 1*cm, f"Page {doc.page}")
    if doc.page > 1:
        c.setFont('Helvetica', 8); c.setFillColor(PRIMARY)
        c.drawString(2*cm, A4[1]-1*cm, "Faculte des Sciences Ben M'Sick - Universite Hassan II Casablanca")
        c.line(2*cm, A4[1]-1.2*cm, A4[0]-2*cm, A4[1]-1.2*cm)
    c.restoreState()


# ─── Helpers visuels ──────────────────────────────────────────────────────────
def code_block(text: str):
    return Paragraph(text.replace('\n', '<br/>').replace(' ', '&nbsp;'), ST_CODE)


def diagram_block(text: str):
    return Paragraph(text.replace('\n', '<br/>').replace(' ', '&nbsp;'), ST_DIAGRAM)


def alert_box(content: str, kind: str = "info", title: str = None):
    colors = {
        "info":    (INFO,     INFO_PALE,    "i"),
        "warning": (WARNING,  WARNING_PALE, "!"),
        "success": (SUCCESS,  SUCCESS_PALE, "OK"),
        "tip":     (ACCENT,   ACCENT_PALE,  "★"),
        "purple":  (PURPLE,   PURPLE_PALE,  "?"),
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
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t


def std_table(rows, header_color=PRIMARY, col_widths=None):
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


# ============================================================================
def build():
    out_path = Path(__file__).parent / "FSBM_Platform_Documentation_Complete.pdf"
    doc = SimpleDocTemplate(
        str(out_path), pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="Documentation Complete - FSBM Platform",
        author="AKRAM BELMOUSSA, ZAKARIA, NOUHAILA",
    )
    story = []

    # ═══════════════════════════════════════════════════════════════════════
    # PAGE DE GARDE
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 2.5*cm))
    if LOGO_FSBM.exists():
        story.append(Image(str(LOGO_FSBM), width=6.5*cm, height=6.5*cm, hAlign='CENTER'))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("UNIVERSITE HASSAN II DE CASABLANCA", ST_COVER_SUB))
    story.append(Paragraph("FACULTE DES SCIENCES BEN M'SICK", ST_COVER_SUB))
    story.append(Spacer(1, 0.5*cm))
    bar = Table([[Paragraph(
        '<font color="#FFFFFF"><b>DOCUMENTATION COMPLETE PROJET DE FIN D\'ETUDES</b></font>',
        ST_BODY)]], colWidths=[14*cm], hAlign='CENTER')
    bar.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PRIMARY),
        ('PADDING',    (0,0), (-1,-1), 14),
        ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(bar)
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("FSBM PLATFORM", ST_COVER_TITLE))
    story.append(Paragraph("Plateforme universitaire intelligente", ST_COVER_SUB))
    story.append(Paragraph("Chatbot trilingue + referentiel academique", ST_COVER_SUB))
    story.append(Spacer(1, 0.8*cm))

    # Tech stack visuel
    techs = Table([
        ['Angular 17', 'Python FastAPI', 'MySQL 8', 'MongoDB 7', 'TF-IDF NLP'],
    ], colWidths=[3*cm]*5, hAlign='CENTER')
    techs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), ACCENT_PALE),
        ('TEXTCOLOR',  (0,0), (-1,-1), ACCENT),
        ('FONT',       (0,0), (-1,-1), 'Helvetica-Bold', 9),
        ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
        ('PADDING',    (0,0), (-1,-1), 8),
        ('BOX',        (0,0), (-1,-1), 0.5, ACCENT),
        ('INNERGRID',  (0,0), (-1,-1), 0.5, ACCENT),
    ]))
    story.append(techs)
    story.append(Spacer(1, 1.5*cm))

    authors = Table([
        [Paragraph('<b>Realise par :</b>', ST_BODY_BOLD)],
        [Paragraph('<b>AKRAM BELMOUSSA</b> - Architecte Backend &amp; Integration NLP', ST_BODY)],
        [Paragraph('<b>ZAKARIA</b> - Frontend Angular &amp; UX/UI', ST_BODY)],
        [Paragraph('<b>NOUHAILA</b> - Base de donnees &amp; Contenu FAQ', ST_BODY)],
    ], colWidths=[14*cm], hAlign='CENTER')
    authors.setStyle(TableStyle([
        ('PADDING', (0,0), (-1,-1), 5),
        ('LINEABOVE', (0,1), (-1,1), 1, ACCENT),
    ]))
    story.append(authors)
    story.append(Spacer(1, 0.8*cm))
    story.append(Paragraph(f"{datetime.now().strftime('%B %Y').upper()}",
        ParagraphStyle('Date', parent=ST_BODY, alignment=TA_CENTER, fontSize=11, textColor=GREY_MID)))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # PREFACE / COMMENT LIRE
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Comment lire cette documentation ?", ST_CHAPTER))
    story.append(Paragraph(
        "Ce document est concu comme un <b>parcours pedagogique complet</b> pour comprendre, "
        "expliquer et maintenir la plateforme FSBM. Il s'adresse a trois publics :",
        ST_BODY))

    story.append(alert_box(
        "<b>L'auteur lui-meme</b> : pour reviser avant la soutenance et reprendre le code apres "
        "une pause de plusieurs mois.",
        kind="tip", title="Public 1"))

    story.append(alert_box(
        "<b>Le jury de soutenance</b> : pour saisir rapidement les choix d'architecture et "
        "evaluer la maitrise technique demontree.",
        kind="info", title="Public 2"))

    story.append(alert_box(
        "<b>Un futur developpeur</b> : pour reprendre ou etendre le projet sans avoir a "
        "deviner les conventions et la logique metier.",
        kind="purple", title="Public 3"))

    story.append(Paragraph("Conseils de lecture", ST_H2))
    bullets = [
        "<b>Premiere lecture</b> : parcourir les chapitres 1, 2, 11 et 14 pour avoir la vision d'ensemble (1h).",
        "<b>Approfondissement</b> : lire les chapitres 4 a 10 dans l'ordre (3h).",
        "<b>Avant soutenance</b> : memoriser le chapitre 14 (questions probables du jury).",
        "<b>Reprise du code</b> : lire les chapitres 4 et 13, puis ouvrir le code en parallele.",
    ]
    for b in bullets:
        story.append(Paragraph(f"• {b}", ST_LIST))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # SOMMAIRE
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Sommaire", ST_CHAPTER))
    toc = [
        ("Comment lire cette documentation", "3"),
        ("Chapitre 1 - Introduction generale", "5"),
        ("    1.1 Contexte universitaire FSBM", "5"),
        ("    1.2 Probleme resolu", "6"),
        ("    1.3 Objectifs SMART", "7"),
        ("    1.4 Utilisateurs cibles (personas)", "8"),
        ("Chapitre 2 - Architecture globale", "10"),
        ("    2.1 Vision a 30 000 pieds", "10"),
        ("    2.2 Architecture micro-services", "11"),
        ("    2.3 Circulation des donnees", "13"),
        ("    2.4 Communication inter-services", "14"),
        ("Chapitre 3 - Technologies utilisees", "16"),
        ("    3.1 Frontend (Angular 17)", "16"),
        ("    3.2 Backend (Python + FastAPI)", "17"),
        ("    3.3 Bases de donnees (MySQL + MongoDB)", "18"),
        ("    3.4 NLP (TF-IDF + Cosine)", "20"),
        ("    3.5 Tableau comparatif des choix", "21"),
        ("Chapitre 4 - Structure des dossiers", "23"),
        ("    4.1 Vue d'ensemble", "23"),
        ("    4.2 Detail dossier par dossier", "24"),
        ("Chapitre 5 - Frontend Angular detaille", "29"),
        ("    5.1 Architecture standalone components", "29"),
        ("    5.2 Routing et lazy loading", "30"),
        ("    5.3 Layout shell (sidebar + topbar)", "31"),
        ("    5.4 Les 9 pages fonctionnelles", "32"),
        ("    5.5 Services HTTP", "34"),
        ("    5.6 Mode sombre", "35"),
        ("Chapitre 6 - Backend FastAPI detaille", "36"),
        ("    6.1 Le chatbot-service", "36"),
        ("    6.2 L'academic-service", "39"),
        ("    6.3 Validation Pydantic", "41"),
        ("    6.4 SQLAlchemy 2.0 async", "42"),
        ("Chapitre 7 - Base de donnees MySQL", "44"),
        ("    7.1 16 tables normalisees", "44"),
        ("    7.2 Schema relationnel", "46"),
        ("    7.3 Donnees seed realistes", "48"),
        ("Chapitre 8 - Base de donnees MongoDB", "50"),
        ("    8.1 6 collections", "50"),
        ("    8.2 Schemas flexibles", "51"),
        ("Chapitre 9 - Fonctionnement du chatbot", "53"),
        ("    9.1 Pipeline NLP en 5 etapes", "53"),
        ("    9.2 Detection de langue", "55"),
        ("    9.3 Personnalisation genre/nom", "56"),
        ("    9.4 Recherche web live", "57"),
        ("Chapitre 10 - Securite", "59"),
        ("    10.1 Mesures actuelles", "59"),
        ("    10.2 JWT en Phase 2", "60"),
        ("Chapitre 11 - Choix techniques justifies", "62"),
        ("Chapitre 12 - Flux complet du systeme", "65"),
        ("Chapitre 13 - Guide de lancement", "68"),
        ("Chapitre 14 - Preparation a la soutenance", "71"),
        ("Chapitre 15 - Analyse professionnelle", "75"),
        ("Chapitre 16 - Conclusion", "78"),
        ("Glossaire", "80"),
    ]
    for label, page in toc:
        dots = '.' * max(1, 78 - len(label) - len(page))
        story.append(Paragraph(
            f"{label} <font color='#8095A8'>{dots}</font> <b>{page}</b>", ST_TOC))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # CHAPITRE 1 - INTRODUCTION GENERALE
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Chapitre 1 - Introduction generale", ST_CHAPTER))

    story.append(Paragraph("1.1 Contexte universitaire FSBM", ST_H1))
    story.append(Paragraph(
        "La <b>Faculte des Sciences Ben M'Sick (FSBM)</b> est l'un des etablissements de "
        "l'Universite Hassan II de Casablanca, fondee en 1984. Elle accueille chaque annee "
        "plusieurs milliers d'etudiants repartis en 5 departements : Mathematiques-Informatique, "
        "Physique, Chimie, Biologie, Geologie. Elle propose 7 licences fondamentales, 18 masters "
        "et un centre d'etudes doctorales.",
        ST_BODY))
    story.append(Paragraph(
        "Comme la plupart des universites publiques marocaines, la FSBM fait face a une "
        "<b>tension informationnelle</b> : les etudiants doivent jongler entre plusieurs sources "
        "d'information (site officiel, panneaux, groupes Facebook, file d'attente au bureau de "
        "scolarite), ce qui cree du stress, des retards et une inegalite d'acces.",
        ST_BODY))

    story.append(Paragraph("1.2 Probleme resolu", ST_H1))
    story.append(Paragraph(
        "Cinq problemes concrets ont ete identifies lors de l'etude prealable :",
        ST_BODY))
    problems = [
        ("Fragmentation des sources",
         "Pour s'inscrire au master IADS, un etudiant doit consulter au moins 4 sources differentes "
         "(site fac, ENT, panneaux scolarite, secretariat). Aucune source ne contient l'information "
         "exhaustive et a jour."),
        ("Saturation du bureau de scolarite",
         "Pendant les pics (rentree, examens, reinscription), 200+ etudiants se presentent chaque "
         "jour pour des questions repetitives qu'un outil automatise pourrait absorber a 80%."),
        ("Indisponibilite hors-horaires",
         "Les services administratifs ferment a 16h30 et le week-end. Les etudiants qui travaillent "
         "ou habitent loin sont penalises."),
        ("Inegalite d'acces a l'information non officielle",
         "Les primo-entrants n'ont pas de reseau pour obtenir des astuces (quel prof choisir, "
         "quels sont les modules elimitatoires, comment reussir un concours d'entree en master)."),
        ("Absence de point d'acces unifie aux ressources",
         "Aucun outil moderne ne permet de naviguer entre departements, filieres, modules, "
         "professeurs, examens et evenements en un seul endroit."),
    ]
    for title, desc in problems:
        story.append(Paragraph(f"<b>{title}.</b> {desc}", ST_LIST))

    story.append(Paragraph("1.3 Objectifs SMART du projet", ST_H1))
    story.append(Paragraph(
        "Les objectifs ont ete formules selon la methode SMART (Specifiques, Mesurables, "
        "Atteignables, Realistes, Temporels) :",
        ST_BODY))
    story.append(std_table([
        ['Objectif', 'Indicateur', 'Cible'],
        ['Couvrir les questions etudiantes', 'Nombre d\'intents reconnus', '60+ intents'],
        ['Repondre en plusieurs langues', 'Langues supportees', 'FR + EN + Darija'],
        ['Recuperer les actus en direct', 'Sources scrapees', 'fsbm.ma + Facebook + DB locale'],
        ['Naviguer dans le referentiel', 'Pages fonctionnelles', '9 pages Angular'],
        ['Demontrer une archi pro', 'Micro-services autonomes', '6 services planifies, 2 livres'],
        ['Donnees realistes', 'Volume seed', '3000+ etudiants, 100+ modules'],
        ['Documentation complete', 'PDF livres', '4 documents (rapport, guide, zombies, doc)'],
    ], col_widths=[5*cm, 5*cm, 6*cm]))

    story.append(Paragraph("1.4 Utilisateurs cibles (personas)", ST_H1))
    story.append(Paragraph(
        "Trois personas ont guide la conception :",
        ST_BODY))

    story.append(Paragraph("Persona 1 : Yassine, primo-entrant", ST_H3))
    story.append(Paragraph(
        "20 ans, vient de decrocher son bac scientifique avec mention bien. Il habite Sidi Bennour "
        "(2h de Casa) et veut s'inscrire en SMI mais ne sait pas par ou commencer. <b>Besoins :</b> "
        "procedure d'inscription claire, liste des documents, periodes, hebergement.",
        ST_BODY))

    story.append(Paragraph("Persona 2 : Salma, en troisieme annee DI", ST_H3))
    story.append(Paragraph(
        "21 ans, etudiante en L3 DI, cherche un stage PFE pour fin de licence. <b>Besoins :</b> "
        "convention de stage, liste d'entreprises qui recrutent, criteres de soutenance, "
        "preparation d'entretien.",
        ST_BODY))

    story.append(Paragraph("Persona 3 : Mehdi, en master IADS", ST_H3))
    story.append(Paragraph(
        "23 ans, en M2 IADS, prepare son memoire. <b>Besoins :</b> dates de soutenance, "
        "ressources avancees, opportunites doctorat, statistiques d'insertion.",
        ST_BODY))

    story.append(alert_box(
        "La conception des intents NLP et des pages Angular a ete pilotee directement par les "
        "besoins de ces 3 personas. Chaque fonctionnalite repond a au moins un besoin identifie.",
        kind="tip", title="Conception centree utilisateur"))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # CHAPITRE 2 - ARCHITECTURE GLOBALE
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Chapitre 2 - Architecture globale", ST_CHAPTER))

    story.append(Paragraph("2.1 Vision a 30 000 pieds", ST_H1))
    story.append(Paragraph(
        "Vue de tres haut, la plateforme FSBM se compose de <b>3 couches</b> superposees :",
        ST_BODY))

    layers = [
        ("Couche Presentation",
         "Application Angular 17 dans le navigateur de l'utilisateur. Aucune logique metier - "
         "uniquement de l'affichage et l'envoi/reception de requetes."),
        ("Couche Services",
         "6 micro-services Python (FastAPI) autonomes communiquant via HTTP REST. Chaque service "
         "est responsable d'un domaine fonctionnel precis."),
        ("Couche Persistance",
         "MySQL 8 pour les donnees structurees (etudiants, filieres, modules), MongoDB 7 pour "
         "les donnees flexibles (reviews, logs, sentiments)."),
    ]
    for n, d in layers:
        story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

    story.append(Paragraph("2.2 Architecture micro-services", ST_H1))
    story.append(Paragraph(
        "Le choix d'une architecture micro-services (vs monolithe) a ete fait pour 5 raisons cles "
        "qui sont detaillees dans le chapitre 11. Voici le diagramme de l'architecture cible :",
        ST_BODY))

    story.append(diagram_block(
        "+-------------------------------------------------------------+\n"
        "|        Frontend Angular 17 SPA (port 4200)                  |\n"
        "+-----------------------+-------------------------------------+\n"
        "                        | HTTP/JSON via proxy.conf.json\n"
        "      +-----+-----+-----+-----+-----+-----+\n"
        "      |     |     |     |     |     |     |\n"
        "  +---v-+ +-v---+ +-v-+ +-v-+ +-v---+ +-v---+\n"
        "  |chat | |acad | |stu| |rev| |noti | |anal |\n"
        "  |:8001| |:8002| |:..| |:..| |:..  | |:..  |\n"
        "  +-+---+ +-+---+ +-+-+ +-+-+ +-+---+ +-----+\n"
        "    |       |       |     |     |\n"
        "    +---+---+-------+-----+-----+\n"
        "        |\n"
        " +------v------+      +-------------+\n"
        " | MySQL 8     |      | MongoDB 7   |\n"
        " | fsbm_db     |      | fsbm_reviews|\n"
        " +-------------+      +-------------+"
    ))

    story.append(Paragraph(
        "Sur les 6 services planifies, <b>2 sont livres en Phase 1</b> "
        "(chatbot-service et academic-service) et 4 sont en scaffolding pour Phase 2.",
        ST_BODY))

    story.append(Paragraph("Les 6 services en detail", ST_H2))
    services_table = [
        ['Service', 'Port', 'Role', 'Statut'],
        ['chatbot-service', '8001', 'NLP TF-IDF, conversations, multilingue', '[LIVRE]'],
        ['academic-service', '8002', 'Departements, filieres, modules, profs, etudiants', '[LIVRE]'],
        ['student-service', '5003', 'Auth JWT, profils, roles', 'Phase 2'],
        ['review-service', '5004', 'Reviews MongoDB, sentiment', 'Phase 2'],
        ['notification-service', '5005', 'SSE temps reel, annonces', 'Phase 2'],
        ['analytics-service', '5006', 'Dashboards admin, stats', 'Phase 2'],
    ]
    story.append(std_table(services_table, col_widths=[4*cm, 1.5*cm, 8*cm, 2.5*cm]))

    story.append(Paragraph("2.3 Circulation des donnees", ST_H1))
    story.append(Paragraph(
        "Suivons le cheminement d'une requete typique : un etudiant envoie le message "
        "<i>Quelles sont les filieres ?</i> depuis le navigateur.",
        ST_BODY))

    flow_steps = [
        ("Etape 1", "Le clic sur 'Envoyer' dans Angular declenche chatService.sendMessage()"),
        ("Etape 2", "Angular emet POST /api/chat (proxifie vers http://localhost:8001/api/chat)"),
        ("Etape 3", "FastAPI recoit, valide le ChatRequest avec Pydantic (longueur, type)"),
        ("Etape 4", "Le preprocesseur (NLTK) nettoie le message : minuscules, stopwords, stemming"),
        ("Etape 5", "Le classifier MultilingualClassifier detecte la langue (FR/EN/Darija)"),
        ("Etape 6", "Vectorisation TF-IDF du message + similarite cosinus contre 461 patterns darija"),
        ("Etape 7", "Selection de l'intent gagnant ('filieres', confidence 1.0)"),
        ("Etape 8", "Pioche d'une reponse au hasard dans intent.responses[lang]"),
        ("Etape 9", "Substitution des placeholders {voc}, {name} selon le contexte session"),
        ("Etape 10", "Sauvegarde en MySQL (table conversations) via SQLAlchemy async"),
        ("Etape 11", "Construction de la ChatResponse Pydantic + JSON"),
        ("Etape 12", "Angular recoit, ajoute le message dans MessageBubbleComponent, animation"),
    ]
    for n, d in flow_steps:
        story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

    story.append(alert_box(
        "Cette chaine de 12 etapes execute en general en <b>150-300 ms</b>, dont environ 50 ms "
        "passes en NLP. L'utilisateur percoit cela comme instantane.",
        kind="success"))

    story.append(Paragraph("2.4 Communication inter-services", ST_H1))
    story.append(Paragraph(
        "Lorsque l'intent <i>live_news</i> est detecte, le chatbot-service doit appeler "
        "academic-service pour recuperer les annonces officielles. La communication se fait "
        "via <b>HTTP REST synchrone</b> avec la lib httpx (asynchrone) :",
        ST_BODY))

    story.append(code_block(
        "# chatbot-service/app/core/web_fetcher.py\n"
        "async with httpx.AsyncClient(timeout=5.0) as client:\n"
        "    r = await client.get(\n"
        "        f\"{self.academic_service_url}/api/announcements\",\n"
        "        params={\"limit\": 5}\n"
        "    )\n"
        "    annonces = r.json()"
    ))

    story.append(Paragraph(
        "Pour une vraie production, on ajouterait un <b>API Gateway</b> (Kong, Traefik), "
        "un <b>service discovery</b> (Consul) et un <b>bus de messages</b> pour les operations "
        "asynchrones (Kafka, NATS). Pour un PFE a echelle pedagogique, le HTTP REST direct "
        "suffit largement.",
        ST_BODY))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # CHAPITRE 3 - TECHNOLOGIES
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Chapitre 3 - Technologies utilisees", ST_CHAPTER))

    story.append(Paragraph("3.1 Frontend - Angular 17", ST_H1))
    story.append(Paragraph("Pourquoi Angular et pas React/Vue ?", ST_H2))
    story.append(Paragraph(
        "Angular est un framework <b>opinionated</b> : il impose une structure (modules, services, "
        "components) et fournit tout ce qu'il faut (routing, forms, HTTP, animations). Cela accelere "
        "le developpement d'apps complexes et facilite la maintenance.",
        ST_BODY))
    story.append(std_table([
        ['Critere', 'Angular 17', 'React 18'],
        ['Routing intégré', 'Oui', 'Lib externe (React Router)'],
        ['Formulaires reactifs', 'Oui (FormsModule)', 'Lib externe'],
        ['HTTP client typé', 'Oui (HttpClient)', 'Lib externe (axios)'],
        ['CLI complet', 'ng generate', 'create-react-app (deprecie)'],
        ['Standalone components', 'Oui (v17)', 'Composants natifs'],
        ['TypeScript par defaut', 'Oui', 'Optionnel'],
        ['Signals (reactif)', 'Oui (v17)', 'Pas natif (hooks)'],
        ['Courbe d\'apprentissage', 'Plus raide', 'Plus douce'],
    ], col_widths=[5*cm, 5.5*cm, 5.5*cm]))

    story.append(Paragraph("Specificites Angular 17 utilisees", ST_H2))
    angular_specifics = [
        ("Standalone components", "Plus besoin de NgModule, chaque composant declare ses imports."),
        ("Signals", "Reactivite fine sans Zone.js, utilises pour le theme service et les listes."),
        ("Lazy loading", "Chaque page est chargee a la demande via loadComponent."),
        ("@for / @if (control flow)", "Syntaxe v17 plus performante que *ngFor/*ngIf."),
        ("inject()", "Injection de dependance fonctionnelle, plus concise."),
    ]
    for t, d in angular_specifics:
        story.append(Paragraph(f"<b>{t}.</b> {d}", ST_LIST))

    story.append(Paragraph("3.2 Backend - Python + FastAPI", ST_H1))
    story.append(Paragraph(
        "Le backend utilise <b>FastAPI</b>, framework moderne sorti en 2018 par Sebastian Ramirez. "
        "Comparaison avec Flask (l'autre concurrent populaire) :",
        ST_BODY))
    story.append(std_table([
        ['Critere', 'FastAPI', 'Flask'],
        ['Annee de creation', '2018', '2010'],
        ['Async natif', 'Oui (async/await)', 'Non (lib externe)'],
        ['Validation des inputs', 'Native (Pydantic)', 'Manuelle (Marshmallow)'],
        ['Documentation API', 'Auto (Swagger UI)', 'Manuelle'],
        ['Performance', '~3x plus rapide', 'OK pour usage simple'],
        ['Type hints obligatoires', 'Oui', 'Non'],
        ['Maturite', 'Solide (2018+)', 'Tres mature (2010)'],
        ['Use case', 'APIs modernes, ML', 'Apps simples, prototypes'],
    ], col_widths=[5*cm, 5.5*cm, 5.5*cm]))

    story.append(alert_box(
        "FastAPI a ete choisi specifiquement pour valoriser le PFE : sa modernite et sa generation "
        "automatique de Swagger impressionnent un jury et demontrent la veille technologique de "
        "l'equipe.",
        kind="tip"))

    story.append(Paragraph("3.3 Bases de donnees - MySQL + MongoDB", ST_H1))
    story.append(Paragraph(
        "Le projet utilise <b>les deux paradigmes</b> de bases de donnees : SQL et NoSQL. Ce n'est "
        "pas pour la beaute du geste - chaque techno est utilisee pour ce qu'elle fait de mieux.",
        ST_BODY))

    story.append(Paragraph("MySQL 8 - donnees structurees", ST_H2))
    story.append(Paragraph(
        "MySQL accueille les <b>donnees au schema fixe et fortement relationnelles</b> : "
        "departements, filieres, modules, etudiants, professeurs, examens. Ces donnees ont des "
        "contraintes d'integrite strictes (un etudiant doit appartenir a une filiere existante) "
        "et beneficient enormement des index B-tree de MySQL pour les requetes complexes "
        "(JOIN, pagination, recherche).",
        ST_BODY))

    story.append(Paragraph("MongoDB 7 - donnees flexibles", ST_H2))
    story.append(Paragraph(
        "MongoDB accueille les <b>donnees au schema variable</b> : reviews textuelles, feedbacks "
        "(pouce haut/bas avec metadata libre), logs d'usage, sentiments analyses. Ces donnees "
        "evoluent souvent (on ajoute des champs sans migration) et beneficient de la flexibilite "
        "JSON. De plus, MongoDB est tres performant pour les <b>ecritures massives</b> (logs).",
        ST_BODY))

    story.append(std_table([
        ['Critere', 'MySQL 8 (utilise pour)', 'MongoDB 7 (utilise pour)'],
        ['Modele', 'Relationnel tabulaire', 'Documentaire JSON'],
        ['Schema', 'Fixe et strict', 'Flexible'],
        ['Relations', 'JOINs natifs', 'Embedding ou references'],
        ['Transactions', 'ACID complet', 'ACID a partir de v4'],
        ['Donnees stockees', 'Etudiants, modules, profs', 'Reviews, logs, sentiments'],
        ['Volume actuel', '~3000 etudiants', '~5 reviews seed'],
        ['Index par defaut', 'B-tree', 'B-tree + hash'],
        ['Cas ideal', 'Donnees critiques liees', 'Donnees evolutives, gros volume'],
    ], col_widths=[3.5*cm, 6*cm, 6.5*cm]))

    story.append(Paragraph("3.4 NLP - TF-IDF + Cosine Similarity", ST_H1))
    story.append(Paragraph(
        "Le moteur NLP du chatbot ne utilise pas de LLM (GPT, Mistral, Llama) car ces modeles :",
        ST_BODY))
    no_llm_reasons = [
        "Necessitent une infrastructure couteuse (GPU, RAM)",
        "Coutent par requete via API (~$0.01-0.10 par message)",
        "Peuvent halluciner (inventer des informations fausses sur la FSBM)",
        "Sont difficilement explicables a un jury (boite noire)",
    ]
    for r in no_llm_reasons:
        story.append(Paragraph(f"• {r}", ST_LIST))

    story.append(Paragraph(
        "Le couple <b>TF-IDF + Cosine Similarity</b> offre un excellent compromis :",
        ST_BODY))
    tfidf_pros = [
        "<b>TF-IDF</b> (Term Frequency - Inverse Document Frequency) vectorise les patterns d'entrainement",
        "<b>Cosine similarity</b> mesure la proximite entre le message utilisateur et chaque pattern",
        "<b>n-grammes (1,2,3)</b> capturent les expressions composees (emploi du temps, master IA)",
        "Fonctionne 100% offline, gratuit, deterministe, explicable",
        "Tres adapte aux FAQ structurees (60+ intents bien definis)",
    ]
    for p in tfidf_pros:
        story.append(Paragraph(f"• {p}", ST_LIST))

    story.append(Paragraph("3.5 Tableau comparatif des choix", ST_H1))
    story.append(std_table([
        ['Couche', 'Choisi', 'Alternative ecartee', 'Raison du rejet'],
        ['Frontend', 'Angular 17', 'React + Redux', 'Plus de boilerplate, moins opinionated'],
        ['Backend', 'FastAPI', 'Flask', 'Pas d\'async natif, pas de Swagger auto'],
        ['Backend', 'FastAPI', 'Django REST', 'Trop monolithe pour micro-services'],
        ['BDD relat.', 'MySQL 8', 'PostgreSQL', 'Equivalent, mais MySQL impose par PFE'],
        ['BDD NoSQL', 'MongoDB 7', 'Redis/DynamoDB', 'Pas adapte aux documents flexibles'],
        ['NLP', 'TF-IDF', 'BERT/GPT', 'Trop lourd, payant, hallucinations'],
        ['ORM', 'SQLAlchemy 2.0', 'Tortoise ORM', 'Plus mature, plus de ressources'],
        ['Auth', 'JWT (planifie)', 'Sessions Redis', 'JWT stateless, scalable'],
        ['Conteneurs', 'Aucun', 'Docker', 'Demande explicite : pas de Docker'],
    ], col_widths=[3*cm, 3*cm, 3.5*cm, 6.5*cm]))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # CHAPITRE 4 - STRUCTURE DOSSIERS
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Chapitre 4 - Structure complete des dossiers", ST_CHAPTER))

    story.append(Paragraph("4.1 Vue d'ensemble", ST_H1))
    story.append(code_block(
        "chatbot-fsbm-platform/\n"
        "|\n"
        "|-- SETUP.bat                        # One-click installer (cmd)\n"
        "|-- SETUP.ps1                        # One-click installer (PowerShell)\n"
        "|-- start.ps1                        # Lance les 3 services\n"
        "|-- README.md                        # Vue d'ensemble + lancement\n"
        "|\n"
        "|-- docs/                            # Documentation complete\n"
        "|   |-- ARCHITECTURE.md              # Architecture detaillee\n"
        "|   |-- TROUBLESHOOTING_PORTS.md     # Doc anti-zombies\n"
        "|   `-- pdf/                         # PDFs generes\n"
        "|       |-- FSBM_Platform_Rapport_PFE.pdf       (165 KB)\n"
        "|       |-- FSBM_Platform_Guide_Technique.pdf   (145 KB)\n"
        "|       |-- FSBM_Platform_Guide_Zombies.pdf     (137 KB)\n"
        "|       `-- FSBM_Platform_Documentation_Complete.pdf  <- CE DOC\n"
        "|\n"
        "|-- database/                        # Tout le SQL et NoSQL\n"
        "|   |-- mysql/\n"
        "|   |   |-- 01_schema.sql            # 16 tables + contraintes (18 KB)\n"
        "|   |   |-- 02_seed_static.sql       # Dept, filieres, masters (19 KB)\n"
        "|   |   |-- 03_seed_modules.sql      # 100+ modules (15 KB)\n"
        "|   |   `-- 04_seed_data.sql         # Profs + etudiants (720 KB)\n"
        "|   |-- mongodb/init.js              # 6 collections + seed (13 KB)\n"
        "|   `-- seed/generate_data.py        # Generateur Python\n"
        "|\n"
        "|-- services/                        # Les 6 micro-services\n"
        "|   |-- chatbot-service/             # FastAPI :8001 - NLP\n"
        "|   |-- academic-service/            # FastAPI :8002 - Referentiel\n"
        "|   |-- student-service/             # Phase 2 - Auth\n"
        "|   |-- review-service/              # Phase 2 - MongoDB\n"
        "|   |-- notification-service/        # Phase 2 - SSE\n"
        "|   `-- analytics-service/           # Phase 2 - Dashboards\n"
        "|\n"
        "|-- frontend/                        # Angular 17 SPA :4200\n"
        "|   `-- src/app/                     # 28 composants, 9 pages\n"
        "|\n"
        "`-- scripts/                         # Utilitaires Windows\n"
        "    |-- install-all.bat\n"
        "    |-- start-all.bat\n"
        "    |-- init-database.bat\n"
        "    |-- configure-env.bat\n"
        "    |-- clean-zombies.ps1            # Nettoie zombies ports\n"
        "    `-- fix-windows-ports.ps1        # Fix definitif (admin)"
    ))

    story.append(Paragraph("4.2 Detail dossier par dossier", ST_H1))

    story.append(Paragraph("docs/", ST_H2))
    story.append(Paragraph(
        "Documentation centralisee. Le sous-dossier <code>pdf/</code> contient les 4 PDFs livres "
        "ainsi que leurs scripts generateurs Python. Cette separation permet de regenerer "
        "n'importe quel PDF apres modification du contenu, sans recompiler le projet.",
        ST_BODY))

    story.append(Paragraph("database/", ST_H2))
    story.append(Paragraph(
        "Le sous-dossier <code>mysql/</code> contient 4 scripts SQL numerotes a executer dans "
        "l'ordre : <b>01</b> cree le schema (DROP DATABASE + CREATE), <b>02</b> peuple les tables "
        "fixes (departements, filieres), <b>03</b> ajoute les modules, <b>04</b> contient 720 KB "
        "de donnees generees (profs + etudiants) - genere par <code>seed/generate_data.py</code>.",
        ST_BODY))

    story.append(Paragraph("services/chatbot-service/", ST_H2))
    story.append(code_block(
        "chatbot-service/\n"
        "|-- app/\n"
        "|   |-- main.py                       # FastAPI app, lifespan, CORS\n"
        "|   |-- core/\n"
        "|   |   |-- config.py                 # Pydantic Settings (.env)\n"
        "|   |   |-- database.py               # SQLAlchemy session\n"
        "|   |   |-- memory.py                 # Memoire conversationnelle\n"
        "|   |   |-- persona.py                # Detection genre/nom + perso\n"
        "|   |   `-- web_fetcher.py            # Scraping fsbm.ma + Facebook\n"
        "|   |-- nlp/\n"
        "|   |   |-- preprocessor.py           # Tokenisation, stopwords, stemming\n"
        "|   |   |-- language_detector.py      # FR / EN / Darija\n"
        "|   |   `-- classifier.py             # TF-IDF + Cosine multi-langue\n"
        "|   |-- models/\n"
        "|   |   `-- schemas.py                # Pydantic v2 schemas\n"
        "|   `-- routers/\n"
        "|       |-- chat.py                   # POST /api/chat, /feedback\n"
        "|       |-- intents.py                # GET /api/intents\n"
        "|       `-- system.py                 # /health, /stats\n"
        "|-- data/\n"
        "|   |-- faq_dataset.json              # 28 intents trilingues\n"
        "|   |-- model.pkl                     # Modele TF-IDF entraine\n"
        "|   `-- chatbot_fsbm.db               # SQLite local (fallback)\n"
        "|-- .env                              # DB password, ports, etc.\n"
        "`-- requirements.txt                  # 18 dependances Python"
    ))

    story.append(Paragraph("services/academic-service/", ST_H2))
    story.append(code_block(
        "academic-service/\n"
        "|-- app/\n"
        "|   |-- main.py                       # FastAPI app\n"
        "|   |-- core/config.py                # Settings\n"
        "|   |-- db/session.py                 # Engine SQLAlchemy async\n"
        "|   |-- models/entities.py            # 15 modeles ORM mappes a MySQL\n"
        "|   |-- schemas/academic.py           # 30+ schemas Pydantic\n"
        "|   `-- routers/                      # 8 routers thematiques\n"
        "|       |-- departments.py            # GET /api/departments\n"
        "|       |-- filieres.py               # GET /api/filieres + filtres\n"
        "|       |-- modules.py                # GET /api/modules\n"
        "|       |-- professors.py             # GET /api/professors (pagine)\n"
        "|       |-- students.py               # GET /api/students (pagine)\n"
        "|       |-- schedule.py               # GET /api/schedule\n"
        "|       |-- exams.py                  # GET /api/exams\n"
        "|       |-- announcements.py          # GET /api/announcements + events + clubs\n"
        "|       `-- system.py                 # /health, /overview\n"
        "|-- .env\n"
        "`-- requirements.txt"
    ))

    story.append(Paragraph("frontend/src/app/", ST_H2))
    story.append(code_block(
        "src/app/\n"
        "|-- app.component.ts                  # Racine - injecte AppShell\n"
        "|-- app.routes.ts                     # 9 routes lazy-loaded\n"
        "|\n"
        "|-- layout/\n"
        "|   |-- app-shell.component.ts        # Sidebar + topbar + outlet\n"
        "|   `-- app-shell.component.css       # Animations, responsive\n"
        "|\n"
        "|-- core/\n"
        "|   `-- theme.service.ts              # Mode sombre/clair\n"
        "|\n"
        "|-- services/\n"
        "|   |-- chat.service.ts               # HTTP client chatbot-service\n"
        "|   `-- academic.service.ts           # HTTP client academic-service\n"
        "|\n"
        "|-- features/                         # Pages lazy-loaded\n"
        "|   |-- dashboard/                    # / (accueil)\n"
        "|   |-- chat/                         # /chat (assistant IA)\n"
        "|   |-- departments/                  # /departements\n"
        "|   |-- filieres/                     # /filieres + /filieres/:code\n"
        "|   |-- modules/                      # /modules\n"
        "|   |-- professors/                   # /professeurs (paginé)\n"
        "|   |-- news/                         # /actualites\n"
        "|   `-- student-life/                 # /vie-etudiante\n"
        "|\n"
        "|-- components/                       # Composants atomiques\n"
        "|   |-- chat-window/\n"
        "|   |-- home-page/                    # (ancien, preserve)\n"
        "|   |-- input-bar/\n"
        "|   |-- message-bubble/\n"
        "|   |-- quick-actions/\n"
        "|   `-- typing-indicator/\n"
        "|\n"
        "`-- models/\n"
        "    `-- message.model.ts              # Interfaces TypeScript"
    ))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # CHAPITRE 5 - FRONTEND ANGULAR
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Chapitre 5 - Frontend Angular detaille", ST_CHAPTER))

    story.append(Paragraph("5.1 Architecture standalone components", ST_H1))
    story.append(Paragraph(
        "Angular 17 introduit officiellement les <b>standalone components</b> : plus besoin de "
        "NgModule, chaque composant declare directement ses dependances dans son decorateur. "
        "Cela rend le code plus modulaire et facilite le tree-shaking.",
        ST_BODY))
    story.append(code_block(
        "// Exemple : app.component.ts\n"
        "@Component({\n"
        "  selector: 'app-root',\n"
        "  standalone: true,\n"
        "  imports: [AppShellComponent],   // <-- directement ici\n"
        "  template: `<app-shell />`,\n"
        "})\n"
        "export class AppComponent {}"
    ))

    story.append(Paragraph("5.2 Routing et lazy loading", ST_H1))
    story.append(Paragraph(
        "Chaque page est chargee a la demande grace a <code>loadComponent</code>. Resultat : "
        "le bundle initial reste petit (175 KB), les pages se chargent en chunks separes (10-30 KB).",
        ST_BODY))
    story.append(code_block(
        "// app.routes.ts\n"
        "export const routes: Routes = [\n"
        "  { path: '', loadComponent: () =>\n"
        "      import('./features/dashboard/dashboard.component')\n"
        "          .then(m => m.DashboardComponent) },\n"
        "  { path: 'chat', loadComponent: () =>\n"
        "      import('./features/chat/chat-page.component')\n"
        "          .then(m => m.ChatPageComponent) },\n"
        "  // ... 7 autres routes\n"
        "];"
    ))

    story.append(Paragraph("5.3 Layout shell (sidebar + topbar)", ST_H1))
    story.append(Paragraph(
        "Le composant <code>AppShellComponent</code> est le squelette commun a toutes les pages. "
        "Il contient :",
        ST_BODY))
    shell_parts = [
        ("Sidebar collapsible", "9 liens de navigation, logos FSBM, toggle mode sombre"),
        ("Topbar", "Banniere FSBM + badge 'En ligne' + bouton 'Assistant IA' rapide"),
        ("Router outlet", "Zone ou Angular injecte le composant de la route active"),
    ]
    for n, d in shell_parts:
        story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

    story.append(Paragraph("5.4 Les 9 pages fonctionnelles", ST_H1))
    pages = [
        ("/", "Dashboard", "Hero anime + 8 cartes stats (live academic-service) + annonces + events"),
        ("/chat", "Assistant IA", "Interface chat multilingue, suggestions, feedback 👍/👎"),
        ("/departements", "Departments", "5 cartes departements avec chef, email, telephone"),
        ("/filieres", "Filieres", "25 cartes (7 licences + 18 masters), recherche, filtres"),
        ("/filieres/:code", "FiliereDetail", "Programme par semestre, debouches, coordinateur"),
        ("/modules", "Modules", "100+ modules avec filtres filiere/semestre"),
        ("/professeurs", "Professors", "Annuaire 107 profs paginé, recherche nom/spec"),
        ("/actualites", "News", "Annonces + evenements a venir"),
        ("/vie-etudiante", "StudentLife", "Clubs avec categories, contacts, reseaux sociaux"),
    ]
    story.append(std_table(
        [['Route', 'Composant', 'Contenu']] +
        [[r, c, d] for r, c, d in pages],
        col_widths=[2.5*cm, 3.5*cm, 10*cm]))

    story.append(Paragraph("5.5 Services HTTP", ST_H1))
    story.append(Paragraph(
        "Deux services injectables encapsulent les appels HTTP :",
        ST_BODY))

    story.append(Paragraph("ChatService", ST_H3))
    story.append(code_block(
        "@Injectable({ providedIn: 'root' })\n"
        "export class ChatService {\n"
        "  private apiUrl = '/api';\n"
        "  constructor(private http: HttpClient) {}\n"
        "  sendMessage(message: string, sessionId: string) {\n"
        "    return this.http.post<ChatResponse>(`${this.apiUrl}/chat`,\n"
        "      { message, session_id: sessionId });\n"
        "  }\n"
        "}"
    ))
    story.append(Paragraph(
        "Le <code>proxy.conf.json</code> redirige <code>/api</code> vers les bons ports backend "
        "(8001 chatbot, 8002 academic). En production, ce sera un reverse proxy nginx.",
        ST_NOTE))

    story.append(Paragraph("5.6 Mode sombre", ST_H1))
    story.append(Paragraph(
        "Le <code>ThemeService</code> utilise un Signal Angular pour la reactivite et persiste "
        "le choix dans localStorage. Les couleurs sont definies en variables CSS qui changent "
        "via l'attribut <code>data-theme</code> sur la racine.",
        ST_BODY))
    story.append(code_block(
        "// theme.service.ts\n"
        "@Injectable({ providedIn: 'root' })\n"
        "export class ThemeService {\n"
        "  readonly theme = signal<'light'|'dark'>('light');\n"
        "  toggle() {\n"
        "    const v = this.theme() === 'light' ? 'dark' : 'light';\n"
        "    this.theme.set(v);\n"
        "    document.documentElement.setAttribute('data-theme', v);\n"
        "    localStorage.setItem('fsbm-theme', v);\n"
        "  }\n"
        "}"
    ))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # CHAPITRE 6 - BACKEND FASTAPI
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Chapitre 6 - Backend FastAPI detaille", ST_CHAPTER))

    story.append(Paragraph("6.1 Le chatbot-service (port 8001)", ST_H1))
    story.append(Paragraph(
        "Service le plus complexe : il gere le NLP, la memoire conversationnelle, la detection "
        "de langue, la personnalisation et la recherche web. Architecture interne :",
        ST_BODY))

    story.append(Paragraph("Lifecycle au demarrage", ST_H2))
    story.append(Paragraph(
        "Le <code>lifespan</code> FastAPI execute :",
        ST_BODY))
    lifecycle = [
        "Chargement de la config depuis .env (Pydantic Settings)",
        "Instanciation du MultilingualClassifier",
        "Tentative de chargement du model.pkl en cache",
        "Si absent : entrainement TF-IDF sur les 3 langues (~3 sec)",
        "Configuration du WebFetcher avec l'URL academic-service",
        "Mise en place du CORS pour http://localhost:4200",
    ]
    for s in lifecycle:
        story.append(Paragraph(f"• {s}", ST_LIST))

    story.append(Paragraph("Endpoints exposes", ST_H2))
    story.append(std_table([
        ['Methode', 'URL', 'Description'],
        ['POST', '/api/chat', 'Envoyer un message - reponse + suggestions'],
        ['POST', '/api/chat/feedback', 'Noter une reponse (1-5 + commentaire)'],
        ['GET', '/api/chat/history/{session_id}', 'Historique d\'une session'],
        ['GET', '/api/chat/suggestions?lang=', 'Questions de demarrage par langue'],
        ['GET', '/api/chat/news?source=', 'News live multi-sources'],
        ['GET', '/api/intents?lang=', 'Liste des 28 intents'],
        ['GET', '/api/health', 'Status du service'],
        ['GET', '/api/stats', 'Statistiques globales'],
    ], col_widths=[1.8*cm, 6.2*cm, 8*cm]))

    story.append(Paragraph("6.2 L'academic-service (port 8002)", ST_H1))
    story.append(Paragraph(
        "Service plus simple : un referentiel academique en lecture seule (CRUD complet possible "
        "mais non expose pour eviter les modifications accidentelles). 8 routers thematiques avec "
        "pagination, filtres et recherche.",
        ST_BODY))

    story.append(std_table([
        ['Methode', 'URL', 'Description'],
        ['GET', '/api/overview', 'Compteurs globaux (dashboard)'],
        ['GET', '/api/departments', 'Liste des 5 departements'],
        ['GET', '/api/filieres?type=&search=', 'Filieres filtrees'],
        ['GET', '/api/filieres/code/{code}', 'Filiere par code (SMI, DI, IADS...)'],
        ['GET', '/api/filieres/{id}/modules', 'Modules groupes par semestre'],
        ['GET', '/api/modules?filiere_id=&semester=', 'Modules filtres'],
        ['GET', '/api/professors?page=&search=', 'Profs pagines'],
        ['GET', '/api/students?filiere_id=&search=', 'Etudiants pagines'],
        ['GET', '/api/schedule?filiere_id=&semester=', 'EDT'],
        ['GET', '/api/exams?session=', 'Examens'],
        ['GET', '/api/announcements', 'Annonces'],
        ['GET', '/api/events', 'Evenements'],
        ['GET', '/api/clubs', 'Clubs etudiants'],
    ], col_widths=[1.8*cm, 6.2*cm, 8*cm]))

    story.append(Paragraph("6.3 Validation Pydantic", ST_H1))
    story.append(Paragraph(
        "Tous les inputs passent par des <b>schemas Pydantic v2</b> qui valident automatiquement "
        "le type, la longueur, le format. Si une requete est invalide, FastAPI retourne un 422 "
        "avec un message d'erreur clair, sans que notre code ait a verifier manuellement.",
        ST_BODY))
    story.append(code_block(
        "class ChatRequest(BaseModel):\n"
        "    message: str = Field(..., min_length=1, max_length=500)\n"
        "    session_id: Optional[str] = None\n"
        "    user_id: Optional[int] = None\n"
        "    language: Optional[str] = None  # fr|en|darija ou None\n"
        "\n"
        "# Dans la route :\n"
        "@router.post(\"/chat\", response_model=ChatResponse)\n"
        "async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db)):\n"
        "    # req est garanti valide ici\n"
        "    ..."
    ))

    story.append(alert_box(
        "Avantage : zero ligne de code de validation manuelle. La doc Swagger est auto-generee a "
        "partir de ces schemas - le jury peut tester chaque endpoint dans le navigateur.",
        kind="success"))

    story.append(Paragraph("6.4 SQLAlchemy 2.0 async", ST_H1))
    story.append(Paragraph(
        "L'ORM utilise la syntaxe moderne 2.0 avec <code>Mapped[T]</code> et "
        "<code>mapped_column()</code>. Toutes les operations DB sont asynchrones (aiomysql) "
        "pour permettre un debit eleve.",
        ST_BODY))
    story.append(code_block(
        "class Department(Base):\n"
        "    __tablename__ = \"departments\"\n"
        "    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)\n"
        "    code: Mapped[str] = mapped_column(String(20), unique=True)\n"
        "    name: Mapped[str] = mapped_column(String(150))\n"
        "    # Relation 1:N\n"
        "    filieres: Mapped[list[\"Filiere\"]] = relationship(back_populates=\"department\")\n"
        "\n"
        "# Usage async :\n"
        "result = await db.execute(select(Department).order_by(Department.id))\n"
        "departments = result.scalars().all()"
    ))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # CHAPITRE 7 - MYSQL
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Chapitre 7 - Base de donnees MySQL", ST_CHAPTER))

    story.append(Paragraph("7.1 16 tables normalisees", ST_H1))
    story.append(Paragraph(
        "La base <code>fsbm_db</code> respecte la <b>3eme forme normale</b> : pas de redondance, "
        "chaque attribut depend de la cle primaire. Voici le catalogue :",
        ST_BODY))

    tables_catalog = [
        ['#', 'Table', 'Description', 'Cardinalite'],
        ['1', 'departments', '5 departements academiques', '5 rows'],
        ['2', 'filieres', '7 licences + 18 masters', '25 rows'],
        ['3', 'modules', 'Matieres par filiere', '100+ rows'],
        ['4', 'professors', 'Enseignants', '~107 rows'],
        ['5', 'students', 'Etudiants inscrits', '~3000 rows'],
        ['6', 'module_teachers', 'N:N module-prof', '~150 rows'],
        ['7', 'schedules', 'Emploi du temps', '~200 rows'],
        ['8', 'exams', 'Calendrier examens', '~400 rows'],
        ['9', 'grades', 'Notes', '~9000 rows'],
        ['10', 'faq_categories', '16 categories FAQ', '16 rows'],
        ['11', 'faq_items', 'Items FAQ', 'extensible'],
        ['12', 'conversations', 'Historique chatbot', 'dynamique'],
        ['13', 'feedbacks', 'Notes utilisateurs', 'dynamique'],
        ['14', 'announcements', 'Annonces officielles', '5+ rows'],
        ['15', 'events', 'Evenements universitaires', '5+ rows'],
        ['16', 'clubs', 'Clubs etudiants', '8 rows'],
    ]
    story.append(std_table(tables_catalog, col_widths=[1*cm, 3.5*cm, 9*cm, 2.5*cm]))

    story.append(Paragraph("7.2 Schema relationnel", ST_H1))
    story.append(diagram_block(
        "departments (1) --< (N) filieres --< (N) modules\n"
        "                      |              |\n"
        "                      v              v\n"
        "                  students       schedules\n"
        "                      |              |\n"
        "                      v              v\n"
        "                   grades         exams\n"
        "\n"
        "departments (1) --< (N) professors --< (N) module_teachers >-- modules\n"
        "\n"
        "faq_categories (1) --< (N) faq_items\n"
        "\n"
        "conversations (1) --< (N) feedbacks"
    ))

    story.append(Paragraph("7.3 Donnees seed realistes", ST_H1))
    story.append(Paragraph(
        "Le script <code>database/seed/generate_data.py</code> genere des donnees authentiques "
        "marocaines :",
        ST_BODY))
    seed_features = [
        "<b>Noms reels</b> : Alaoui, Bennani, Tazi, Filali, Chaoui... (200+ noms de famille)",
        "<b>Prenoms</b> : Mohammed, Fatima, Karim, Salma... (100+ prenoms M/F)",
        "<b>CNE</b> au format reglementaire marocain (10 chiffres)",
        "<b>Emails</b> au format etu.fsbm.ma + suffixes pour unicite",
        "<b>Telephones</b> +212 6XXXXXXXX",
        "<b>Specialites profs</b> coherentes avec leur departement",
        "<b>Notes</b> avec distribution gaussienne autour de 12.5/20",
        "<b>EDT</b> generes par formule modulo deterministe (reproductible)",
    ]
    for f in seed_features:
        story.append(Paragraph(f"• {f}", ST_LIST))

    story.append(alert_box(
        "Volume genere : 107 profs + 2970 etudiants + 9654 notes = ~720 KB de SQL. "
        "Tout est reproductible (random.seed(42)) - chaque execution donne exactement les memes "
        "donnees.",
        kind="success"))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # CHAPITRE 8 - MONGODB
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Chapitre 8 - Base de donnees MongoDB", ST_CHAPTER))

    story.append(Paragraph("8.1 Les 6 collections", ST_H1))
    story.append(Paragraph(
        "La base <code>fsbm_reviews</code> contient 6 collections avec validation JSON Schema. "
        "Le choix MongoDB se justifie par la nature <b>evolutive</b> de ces donnees.",
        ST_BODY))

    mongo_collections = [
        ['Collection', 'Role', 'Volume estime'],
        ['reviews', 'Avis textuels detailles', 'centaines/mois'],
        ['chatbot_feedback', 'Pouce haut/bas par reponse', 'milliers/mois'],
        ['conversations', 'Log complet des sessions', 'milliers/mois'],
        ['sentiment_analysis', 'Sentiments analyses', 'milliers/mois'],
        ['usage_logs', 'Tracking anonyme', 'dizaines de milliers/mois'],
        ['suggestions', 'Suggestions ameliorations', 'dizaines/mois'],
    ]
    story.append(std_table(mongo_collections, col_widths=[4.5*cm, 7.5*cm, 4*cm]))

    story.append(Paragraph("8.2 Schemas flexibles avec validation", ST_H1))
    story.append(Paragraph(
        "MongoDB est souvent critique pour sa flexibilite excessive. On utilise donc le "
        "<b>validator JSON Schema</b> pour imposer une structure minimum :",
        ST_BODY))
    story.append(code_block(
        "db.createCollection(\"reviews\", {\n"
        "  validator: {\n"
        "    $jsonSchema: {\n"
        "      bsonType: \"object\",\n"
        "      required: [\"user_id\", \"rating\", \"created_at\"],\n"
        "      properties: {\n"
        "        user_id:  { bsonType: [\"int\", \"long\"] },\n"
        "        rating:   { bsonType: \"int\", minimum: 1, maximum: 5 },\n"
        "        content:  { bsonType: \"string\", maxLength: 2000 },\n"
        "        sentiment:{ enum: [\"POSITIVE\",\"NEUTRAL\",\"NEGATIVE\"] },\n"
        "        ...\n"
        "      }\n"
        "    }\n"
        "  }\n"
        "});"
    ))

    story.append(Paragraph(
        "On obtient le meilleur des deux mondes : <b>la flexibilite</b> de pouvoir ajouter des "
        "champs sans migration, mais avec <b>une garantie structurelle</b> sur les champs critiques.",
        ST_BODY))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # CHAPITRE 9 - FONCTIONNEMENT CHATBOT
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Chapitre 9 - Fonctionnement du chatbot", ST_CHAPTER))

    story.append(Paragraph("9.1 Pipeline NLP en 5 etapes", ST_H1))
    story.append(diagram_block(
        "  Message utilisateur\n"
        "        |\n"
        "        v\n"
        "[1] Detection de langue\n"
        "    (FR / EN / Darija)\n"
        "        |\n"
        "        v\n"
        "[2] Preprocessing\n"
        "    minuscules, stopwords, stemming\n"
        "        |\n"
        "        v\n"
        "[3] Vectorisation TF-IDF\n"
        "    n-grammes (1,2,3) langue choisie\n"
        "        |\n"
        "        v\n"
        "[4] Similarite cosinus\n"
        "    vs 461 patterns darija (ou 188 FR / 186 EN)\n"
        "        |\n"
        "        v\n"
        "[5] Top-K candidats\n"
        "    Intent gagnant (si conf > 0.15)\n"
        "        |\n"
        "        v\n"
        "  Reponse + personnalisation"
    ))

    story.append(Paragraph("9.2 Detection de langue", ST_H1))
    story.append(Paragraph(
        "Le detecteur est <b>hybride</b> : il combine 3 strategies en cascade.",
        ST_BODY))
    detection_strategies = [
        ("Caracteres arabes", "Si le message contient des caracteres unicode arabes -> darija."),
        ("Chiffres-lettres", "Les chiffres 3, 7, 9, 8 dans des mots latins (3am, 7biba, 9rib) sont des marqueurs darija forts."),
        ("Score lexical", "Comptage des mots-cles distinctifs par langue (110+ mots FR, 100+ EN, 80+ darija dont 'kifash', 'wesh', 'bghit'...)."),
    ]
    for n, d in detection_strategies:
        story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

    story.append(alert_box(
        "Taux de detection : 14/14 sur le jeu de test (100%). Le detecteur fonctionne sans aucune "
        "dependance externe (pas de langdetect, pas de cld3) - 100% offline.",
        kind="success"))

    story.append(Paragraph("9.3 Personnalisation genre/nom", ST_H1))
    story.append(Paragraph(
        "Le module <code>app/core/persona.py</code> ajoute une couche d'intelligence : il detecte "
        "automatiquement quand l'utilisateur revele son genre ou son nom, le memorise dans la "
        "session, et personnalise toutes les reponses suivantes.",
        ST_BODY))

    story.append(Paragraph("Detection", ST_H3))
    story.append(code_block(
        "GENDER_HINTS_F = [\n"
        "    r\"\\bana\\s+bnt\\b\", r\"\\bana\\s+fata\\b\",\n"
        "    r\"je\\s+suis\\s+une?\\s+(fille|etudiante|madame)\",\n"
        "    r\"i\\s+am\\s+a?\\s*(girl|female|woman)\",\n"
        "    ...\n"
        "]"
    ))

    story.append(Paragraph("Substitution des placeholders", ST_H3))
    story.append(Paragraph(
        "Les reponses contiennent des marqueurs comme <code>{voc}</code> qui sont remplaces "
        "selon le genre stocke en session :",
        ST_BODY))
    story.append(code_block(
        "# Avant substitution :\n"
        "\"Salam {voc}{name_comma} ! Ach bghiti t3ref ?\"\n"
        "\n"
        "# Pour Fatima (gender=F) :\n"
        "\"Salam khti, Fatima ! Ach bghiti t3ref ?\"\n"
        "\n"
        "# Pour Karim (gender=M) :\n"
        "\"Salam khoya, Karim ! Ach bghiti t3ref ?\"\n"
        "\n"
        "# Genre inconnu :\n"
        "\"Salam sahbi ! Ach bghiti t3ref ?\""
    ))

    story.append(Paragraph("9.4 Recherche web live", ST_H1))
    story.append(Paragraph(
        "Quand l'utilisateur demande <i>les dernieres actualites</i>, l'intent <code>live_news</code> "
        "est detecte avec <code>trigger_web_fetch: true</code>. Le router declenche alors le "
        "WebFetcher qui agrege 3 sources :",
        ST_BODY))
    sources_fetch = [
        ("Source primaire", "academic-service /api/announcements (notre base, source de verite)"),
        ("Source secondaire", "fsbm.ma/news (souvent vide car SPA JS)"),
        ("Source Facebook", "Lien direct car FB bloque le scraping anonyme"),
    ]
    for n, d in sources_fetch:
        story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

    story.append(Paragraph(
        "Resultat : un texte structure mixant les 3 sources, ainsi qu'une liste typee "
        "<code>news_items</code> que le frontend peut afficher comme cartes interactives.",
        ST_BODY))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # CHAPITRE 10 - SECURITE
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Chapitre 10 - Securite", ST_CHAPTER))

    story.append(Paragraph("10.1 Mesures actuelles (Phase 1)", ST_H1))
    security_measures = [
        ("Validation Pydantic v2",
         "Tous les inputs API sont valides : types, longueurs, formats. Une requete invalide est "
         "rejetee en 422 sans atteindre la logique metier."),
        ("Anti-injection SQL",
         "Utilisation exclusive de SQLAlchemy avec requetes parametriees. Aucune concatenation "
         "manuelle de chaine SQL n'existe dans le code."),
        ("CORS configure",
         "Liste blanche d'origines (localhost:4200 en dev). Pas de wildcard '*' qui ouvrirait "
         "l'API a n'importe quel site."),
        ("Limitation des messages",
         "max_length=500 sur le champ message du chatbot : evite les attaques par denial of "
         "service via gros payloads."),
        ("Variables d'environnement",
         "Mots de passe MySQL stockes en .env (jamais commit). Les .env sont dans .gitignore."),
        ("Gestion d'erreurs centralisee",
         "Exceptions converties en 500/422 avec messages clairs sans leak d'information sensible."),
        ("Documentation auto-securisee",
         "Swagger UI sur /docs disponible uniquement en mode debug."),
    ]
    for n, d in security_measures:
        story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

    story.append(Paragraph("10.2 JWT en Phase 2 (a implementer)", ST_H1))
    story.append(Paragraph(
        "Le student-service planifie en Phase 2 implementera l'authentification JWT :",
        ST_BODY))

    jwt_flow = [
        "POST /api/auth/login avec email + password",
        "Verification du mot de passe via bcrypt (12 rounds)",
        "Generation d'un token JWT signe HS256 avec expiration 24h",
        "Retour du token + refresh token",
        "Les routes protegees verifient le token via Depends(get_current_user)",
        "Rotation du refresh token toutes les 24h",
    ]
    for s in jwt_flow:
        story.append(Paragraph(f"• {s}", ST_LIST))

    story.append(code_block(
        "# Exemple (Phase 2)\n"
        "from fastapi import Depends, HTTPException\n"
        "from jose import jwt\n"
        "\n"
        "async def get_current_user(token: str = Depends(oauth2_scheme)):\n"
        "    try:\n"
        "        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])\n"
        "        return await get_user(payload['sub'])\n"
        "    except JWTError:\n"
        "        raise HTTPException(401, 'Token invalide')\n"
        "\n"
        "@router.get('/me')\n"
        "async def me(user = Depends(get_current_user)):\n"
        "    return user"
    ))

    story.append(Paragraph("Roles prevus", ST_H2))
    story.append(std_table([
        ['Role', 'Permissions'],
        ['STUDENT', 'Lecture seule + chatbot + reviews'],
        ['PROFESSOR', 'Lecture + ajout note + reponse FAQ'],
        ['SCOLARITE', 'Modification donnees etudiants + annonces'],
        ['ADMIN', 'Tout + creation comptes + statistiques'],
    ], col_widths=[3*cm, 13*cm]))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # CHAPITRE 11 - CHOIX TECHNIQUES JUSTIFIES
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Chapitre 11 - Choix techniques justifies", ST_CHAPTER))

    story.append(Paragraph(
        "Cette section anticipe les questions du jury en justifiant les decisions architecturales.",
        ST_BODY))

    story.append(Paragraph("Q: Pourquoi des micro-services et pas un monolithe ?", ST_H1))
    story.append(Paragraph(
        "Pour un projet a echelle pedagogique, un monolithe Flask aurait suffi. Le choix "
        "micro-services se justifie pour 5 raisons :",
        ST_BODY))
    micro_pros = [
        ("Demonstration pedagogique", "Le PFE doit demontrer la maitrise de patterns modernes."),
        ("Separation des responsabilites", "Chaque service a une mission claire."),
        ("Evolutivite independante", "On ajoute un service sans toucher aux autres."),
        ("Stack heterogene", "MySQL pour les donnees fortes, MongoDB pour le flexible."),
        ("Tolerance aux pannes", "Si reviews tombe, le chatbot continue de fonctionner."),
    ]
    for n, d in micro_pros:
        story.append(Paragraph(f"• <b>{n}.</b> {d}", ST_LIST))

    story.append(Paragraph("Q: Pourquoi pas Docker ?", ST_H1))
    story.append(Paragraph(
        "Le cahier des charges PFE imposait explicitement <b>une compatibilite Windows sans "
        "conteneurs</b>. Docker aurait apporte des avantages (isolation, reproductibilite) mais "
        "aurait aussi :",
        ST_BODY))
    no_docker = [
        "Necessite Docker Desktop (lourd sur Windows, conflits Hyper-V)",
        "Ajoute une couche d'abstraction qui masque le fonctionnement reel",
        "Complexifie le debugging pour un debutant",
        "N'est pas necessaire a echelle 'machine de l'enseignant'",
    ]
    for r in no_docker:
        story.append(Paragraph(f"• {r}", ST_LIST))

    story.append(Paragraph(
        "<b>Solution adoptee :</b> scripts batch/PowerShell + .env per service + venv Python. "
        "Resultat equivalent en simplicite, sans la lourdeur Docker.",
        ST_BODY))

    story.append(Paragraph("Q: Pourquoi pas une seule base de donnees ?", ST_H1))
    story.append(Paragraph(
        "MySQL et MongoDB couvrent des besoins differents. Une seule base obligerait a :",
        ST_BODY))
    one_db = [
        "Tout en MySQL : reviews et logs deviennent des BLOBs JSON peu queryables",
        "Tout en MongoDB : on perd les contraintes referentielles et les JOINs efficaces",
        "Postgres : excellent compromis (JSONB) mais MySQL impose par le PFE",
    ]
    for r in one_db:
        story.append(Paragraph(f"• {r}", ST_LIST))

    story.append(alert_box(
        "Combiner MySQL + MongoDB est une <b>vraie pratique industrielle</b> appelee polyglot "
        "persistence. Demontrer cette maitrise est un point fort en soutenance.",
        kind="tip"))

    story.append(Paragraph("Q: Pourquoi TF-IDF et pas GPT/Mistral ?", ST_H1))
    story.append(Paragraph(
        "Detaille au chapitre 3.4. Resume :",
        ST_BODY))
    why_tfidf = [
        "Couts : LLM facture 0.01-0.10 USD par requete, TF-IDF gratuit a vie",
        "Latence : TF-IDF 5ms vs LLM 500-2000ms",
        "Hallucinations : LLM peut inventer (dangereux pour des infos officielles)",
        "Explicabilite : TF-IDF est transparent (on peut justifier chaque score)",
        "Offline : TF-IDF tourne sur CPU, pas de dependance API externe",
    ]
    for r in why_tfidf:
        story.append(Paragraph(f"• {r}", ST_LIST))

    story.append(Paragraph("Q: Pourquoi Angular 17 specifiquement ?", ST_H1))
    story.append(Paragraph(
        "Angular 17 (sorti nov 2023) apporte :",
        ST_BODY))
    angular17 = [
        "<b>Standalone components</b> : plus simple, moins de boilerplate",
        "<b>Signals</b> : reactivite native sans Zone.js",
        "<b>Control flow @if/@for</b> : syntaxe plus claire que *ngIf",
        "<b>SSR/Hydration</b> ameliores (preparation pour migration future)",
        "<b>Performance</b> : bundles plus petits, lazy loading optimise",
    ]
    for r in angular17:
        story.append(Paragraph(f"• {r}", ST_LIST))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # CHAPITRE 12 - FLUX COMPLET
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Chapitre 12 - Flux complet du systeme", ST_CHAPTER))

    story.append(Paragraph(
        "Cette section trace le flux integral du moment ou l'utilisateur ouvre le navigateur "
        "jusqu'a la reponse finale du chatbot.",
        ST_BODY))

    story.append(Paragraph("12.1 Demarrage de l'application (cold start)", ST_H1))
    cold_start = [
        ("T+0 ms", "Utilisateur tape http://localhost:4200 dans son navigateur"),
        ("T+50 ms", "Le serveur de dev Angular sert index.html (175 KB)"),
        ("T+300 ms", "Le navigateur charge main.js, vendor.js, styles.css"),
        ("T+500 ms", "Angular bootstrap, theme service initialise depuis localStorage"),
        ("T+600 ms", "Routing actif sur '/', dashboard.component charge en lazy (28 KB)"),
        ("T+800 ms", "DashboardComponent monte, lance 3 appels HTTP en parallele"),
        ("T+850 ms", "Appel 1: GET /api/academic/overview -> proxy redirect vers :8002"),
        ("T+850 ms", "Appel 2: GET /api/academic/announcements?limit=4"),
        ("T+850 ms", "Appel 3: GET /api/academic/events?upcoming_only=true"),
        ("T+1000 ms", "Reponses recues, signaux Angular mis a jour"),
        ("T+1050 ms", "Cartes statistiques apparaissent avec animation fadeInUp"),
        ("T+1100 ms", "Dashboard pleinement interactif"),
    ]
    for t, d in cold_start:
        story.append(Paragraph(f"<b>{t}</b> - {d}", ST_LIST))

    story.append(Paragraph("12.2 Conversation chatbot en darija", ST_H1))
    story.append(Paragraph(
        "Scenario : l'utilisateur navigue vers /chat, dit 'salam', puis 'ana bnt', puis "
        "'kifash ntsajjel f master IADS'.",
        ST_BODY))

    chat_flow = [
        ("Tour 1", "User: 'salam'"),
        ("Tour 1.1", "Frontend POST /api/chat avec session_id genere"),
        ("Tour 1.2", "Backend detecte darija, classifier matche 'salutation' (1.00)"),
        ("Tour 1.3", "Reponse 'Ahlan sahbi !' (neutre car genre inconnu)"),
        ("Tour 2", "User: 'ana bnt'"),
        ("Tour 2.1", "detect_gender() match -> 'F' stocke en session"),
        ("Tour 2.2", "Classifier match 'identite_genre' (1.00)"),
        ("Tour 2.3", "acknowledge_self_intro(gender='F') retourne reponse perso"),
        ("Tour 2.4", "'Marhba bik khti ! Mzyan li 3rrefti rasek...'"),
        ("Tour 3", "User: 'kifash ntsajjel f master IADS'"),
        ("Tour 3.1", "Detection darija (mots cles: kifash, ntsajjel, dyalkom)"),
        ("Tour 3.2", "Classifier matche 'master_iads' (0.78)"),
        ("Tour 3.3", "Reponse longue avec programme, conditions, salaires"),
        ("Tour 3.4", "personalize_response() substitue {voc} -> 'khti'"),
        ("Tour 3.5", "Sauvegarde MySQL conversations (id auto-genere)"),
        ("Tour 3.6", "Reponse arrive au frontend, MessageBubbleComponent affiche"),
    ]
    for t, d in chat_flow:
        story.append(Paragraph(f"<b>{t}</b> {d}", ST_LIST))

    story.append(alert_box(
        "Toute cette conversation execute en environ <b>1 seconde reseau cumule</b>. "
        "L'experience utilisateur est fluide.",
        kind="success"))

    story.append(Paragraph("12.3 Recherche d'actualites live", ST_H1))
    story.append(Paragraph(
        "User dit '9elleb 3la lkhbar'. Voici le flux interne :",
        ST_BODY))
    news_flow = [
        "Classifier matche live_news (1.00) avec trigger_web_fetch=True",
        "Router chat.py declenche fetcher.get_news(source='all')",
        "fetcher lance 3 appels paralleles :",
        "  - academic-service /api/announcements (cache 5min)",
        "  - GET https://www.fsbm.ma/news (BeautifulSoup parse)",
        "  - GET https://m.facebook.com/FSBMUH2C (best effort)",
        "Resultats agreges : 6 items (5 locaux + 1 lien Facebook)",
        "format_news_response() construit un texte structure en darija",
        "Reponse finale = template darija + news formate + liens officiels",
        "news_items aussi inclus dans la reponse (typed: NewsItemSchema)",
    ]
    for s in news_flow:
        story.append(Paragraph(f"• {s}", ST_LIST))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # CHAPITRE 13 - GUIDE DE LANCEMENT
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Chapitre 13 - Guide de lancement", ST_CHAPTER))

    story.append(Paragraph("13.1 Pre-requis Windows", ST_H1))
    story.append(std_table([
        ['Logiciel', 'Version min', 'Lien'],
        ['Python', '3.10+', 'python.org/downloads'],
        ['Node.js', '18+ (LTS)', 'nodejs.org'],
        ['MySQL Server', '8.0+', 'dev.mysql.com/downloads'],
        ['MongoDB', '7+ (optionnel Phase 1)', 'mongodb.com/try/download/community'],
        ['MySQL Workbench', 'derniere', 'inclus dans MySQL Installer'],
    ], col_widths=[4*cm, 4*cm, 8*cm]))

    story.append(alert_box(
        "Eviter Python 3.14 (tres recent, certains packages peuvent etre incompatibles). "
        "Preferer Python 3.12 ou 3.13.",
        kind="warning"))

    story.append(Paragraph("13.2 Methode one-click (recommandee)", ST_H1))
    story.append(code_block(
        "# Ouvrir PowerShell\n"
        "cd C:\\Users\\belmo\\studies\\PFE\\chatbot-fsbm-platform\n"
        "powershell -ExecutionPolicy Bypass -File .\\SETUP.ps1"
    ))
    story.append(Paragraph(
        "Le script SETUP.ps1 fait <b>tout</b> automatiquement :",
        ST_BODY))
    setup_steps = [
        "Detecte MySQL (cherche dans les chemins standards)",
        "Demande le mot de passe MySQL (1 seul input)",
        "Cree les .env pour chatbot-service et academic-service",
        "Installe les deps Python (pip install -r requirements.txt)",
        "Installe les deps Angular (npm install)",
        "Charge les 4 scripts SQL dans MySQL",
        "Lance les 3 services dans 3 fenetres cmd separees",
    ]
    for s in setup_steps:
        story.append(Paragraph(f"• {s}", ST_LIST))

    story.append(Paragraph("13.3 Methode manuelle (controle total)", ST_H1))
    story.append(Paragraph("Etape A - Installer les deps Python", ST_H3))
    story.append(code_block(
        "cd services\\academic-service\n"
        "py -m pip install -r requirements.txt\n"
        "\n"
        "cd ..\\chatbot-service\n"
        "py -m pip install -r requirements.txt"
    ))

    story.append(Paragraph("Etape B - Installer les deps Angular", ST_H3))
    story.append(code_block(
        "cd ..\\..\\frontend\n"
        "npm install"
    ))

    story.append(Paragraph("Etape C - Configurer .env", ST_H3))
    story.append(code_block(
        "cd ..\\services\\academic-service\n"
        "copy .env.example .env\n"
        "notepad .env  # editer DB_PASSWORD\n"
        "\n"
        "cd ..\\chatbot-service\n"
        "copy .env.example .env\n"
        "notepad .env"
    ))

    story.append(Paragraph("Etape D - Charger MySQL", ST_H3))
    story.append(code_block(
        "# Via MySQL Workbench (recommande)\n"
        "# File > Open SQL Script... et executer dans l'ordre :\n"
        "#   01_schema.sql\n"
        "#   02_seed_static.sql\n"
        "#   03_seed_modules.sql\n"
        "#   04_seed_data.sql"
    ))

    story.append(Paragraph("Etape E - Lancer les 3 services", ST_H3))
    story.append(code_block(
        "# Terminal 1 - academic-service\n"
        "cd services\\academic-service\n"
        "$env:PYTHONIOENCODING=\"utf-8\"\n"
        "py -m uvicorn app.main:app --reload --port 8002\n"
        "\n"
        "# Terminal 2 - chatbot-service\n"
        "cd services\\chatbot-service\n"
        "$env:PYTHONIOENCODING=\"utf-8\"\n"
        "py -m uvicorn app.main:app --reload --port 8001\n"
        "\n"
        "# Terminal 3 - frontend\n"
        "cd frontend\n"
        "npm start"
    ))

    story.append(Paragraph("13.4 Verification", ST_H1))
    story.append(std_table([
        ['URL', 'Resultat attendu'],
        ['http://localhost:8001/docs', 'Swagger UI chatbot'],
        ['http://localhost:8001/api/health', '{"status":"ok"}'],
        ['http://localhost:8002/docs', 'Swagger UI academic'],
        ['http://localhost:8002/api/overview', 'JSON avec compteurs'],
        ['http://localhost:4200', 'Dashboard FSBM'],
    ], col_widths=[7*cm, 9*cm]))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # CHAPITRE 14 - SOUTENANCE
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Chapitre 14 - Preparation a la soutenance", ST_CHAPTER))

    story.append(Paragraph("14.1 Plan de presentation (20 min)", ST_H1))
    presentation_plan = [
        ("0-2 min", "Introduction : contexte FSBM, probleme, equipe"),
        ("2-4 min", "Objectifs SMART et personas"),
        ("4-7 min", "Architecture micro-services (diagramme)"),
        ("7-10 min", "Demo live : chatbot multilingue (FR, EN, Darija)"),
        ("10-13 min", "Demo : navigation dashboard, filieres, modules"),
        ("13-15 min", "Architecture backend : MySQL + MongoDB + FastAPI"),
        ("15-17 min", "Choix techniques justifies (3-4 cles)"),
        ("17-19 min", "Limites + perspectives Phase 2"),
        ("19-20 min", "Conclusion et remerciements"),
    ]
    story.append(std_table(
        [['Temps', 'Contenu']] + [[t, d] for t, d in presentation_plan],
        col_widths=[2.5*cm, 13.5*cm]))

    story.append(Paragraph("14.2 Questions probables du jury", ST_H1))

    qa = [
        ("Pourquoi pas un LLM comme ChatGPT pour le chatbot ?",
         "Couts (0.01-0.10 USD/requete), hallucinations (informations fausses sur la FSBM), "
         "latence (500-2000 ms vs 5 ms), explicabilite (boite noire), dependance internet. "
         "TF-IDF gratuit, deterministe, explicable, fonctionne offline."),

        ("Pourquoi micro-services pour un PFE de licence ?",
         "Demonstration pedagogique de patterns industriels, separation des responsabilites, "
         "stack heterogene (SQL+NoSQL), evolutivite independante. Chaque service est utilement "
         "deploye seul si besoin."),

        ("Comment scaler si 10 000 utilisateurs ?",
         "Plusieurs leviers : (1) repliquer chaque micro-service horizontalement derriere un load "
         "balancer, (2) cache Redis pour les requetes frequentes, (3) replication MySQL master-slave, "
         "(4) MongoDB sharding sur les logs."),

        ("Comment gerez-vous la securite des donnees etudiantes ?",
         "Phase 1 : validation Pydantic + anti-injection SQL + CORS strict + secrets en .env. "
         "Phase 2 : JWT avec bcrypt 12 rounds, RBAC (4 roles), rate limiting, audit logs MongoDB."),

        ("Pourquoi MySQL ET MongoDB ?",
         "Pratique industrielle 'polyglot persistence'. MySQL pour donnees fortement liees "
         "(etudiants, filieres) avec ACID complet. MongoDB pour donnees evolutives (reviews, logs) "
         "avec schema flexible et ecritures massives performantes."),

        ("Comment avez-vous teste le projet ?",
         "Tests fonctionnels : 60+ questions en FR/EN/Darija. Performance : ~150-300 ms par "
         "reponse, < 1.5 sec chargement Angular. NLP : 14/14 tests langue detectee, "
         "11/12 puis 5/5 apres ajustements sur intents news."),

        ("Quelles sont les limites de votre projet ?",
         "(1) NLP TF-IDF ne generalise pas aux formulations totalement nouvelles, (2) auth JWT "
         "et 4 services en Phase 2 non implementes, (3) testabilite : pas de tests automatises, "
         "(4) fsbm.ma est une SPA JS donc scraping limite, (5) pas de dashboard admin."),

        ("Comment maintenir les donnees a jour ?",
         "Le formulaire Google Forms genere pour le responsable scolarite permet de collecter "
         "les donnees officielles. Le faq_dataset.json est versionne et facile a etendre - "
         "ajouter un intent prend 5 minutes."),

        ("Pourquoi pas de tests unitaires ?",
         "Manque de temps en Phase 1, prevu pour Phase 2 avec pytest pour le backend et "
         "Karma/Jasmine pour Angular. Architecture testable (separation des responsabilites)."),

        ("Comment integrer ce systeme a la FSBM en vrai ?",
         "Etapes : (1) deploiement sur serveur Linux univ (Apache + uvicorn workers), "
         "(2) integration auth via Apogee/CAS, (3) collecte donnees reelles via le formulaire "
         "deja prepare, (4) validation contenu par responsable scolarite, (5) phase pilote "
         "1 promo, puis generalisation."),
    ]
    for q, a in qa:
        story.append(Paragraph(f"<b>Q : {q}</b>", ST_H3))
        story.append(Paragraph(f"R : {a}", ST_BODY))
        story.append(Spacer(1, 0.2*cm))

    story.append(Paragraph("14.3 Points techniques impressionnants a mettre en avant", ST_H1))
    impressive = [
        "<b>Architecture 6 micro-services</b> avec 2 deja livres, separation BDD SQL/NoSQL",
        "<b>NLP multilingue</b> FR/EN/Darija avec detection automatique de langue",
        "<b>Personnalisation</b> genre + nom : adaptation 'khoya/khti', 'Monsieur/Madame'",
        "<b>3000+ donnees realistes</b> generees avec noms marocains authentiques",
        "<b>Recherche web live</b> agregeant 3 sources (base + fsbm.ma + Facebook)",
        "<b>Mode sombre</b> persistant avec Signals Angular 17",
        "<b>4 PDFs livres</b> : rapport, guide tech, guide zombies, documentation complete",
        "<b>Setup one-click</b> : 1 seul input (mot de passe MySQL) pour tout installer",
        "<b>Solution definitive aux zombies de ports</b> : netsh excludedportrange",
    ]
    for i in impressive:
        story.append(Paragraph(f"• {i}", ST_LIST))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # CHAPITRE 15 - ANALYSE PROFESSIONNELLE
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Chapitre 15 - Analyse professionnelle", ST_CHAPTER))

    story.append(Paragraph("15.1 Forces du projet", ST_H1))
    forces = [
        ("Architecture moderne",
         "Micro-services + async + multilingue + mode sombre. Demontre une veille technologique."),
        ("Pertinence sociale",
         "Repond a un vrai besoin (information dispersee, scolarite saturee) avec un usage "
         "potentiel reel a la FSBM."),
        ("Trilingualisme",
         "Inclut explicitement le Darija marocain - peu d'outils du genre existent."),
        ("Donnees realistes",
         "3000+ etudiants avec noms et CNE authentiques rendent les demos credibles."),
        ("Documentation exhaustive",
         "4 PDFs + plusieurs MD + README. Le projet est repris facilement par un tiers."),
        ("Bonnes pratiques",
         "Pydantic, async, lazy loading, separation des responsabilites, .env, gitignore."),
        ("Resolution proactive de problemes",
         "Scripts anti-zombies, fix Windows definitif, generation auto Google Forms."),
    ]
    for n, d in forces:
        story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

    story.append(Paragraph("15.2 Faiblesses et limites", ST_H1))
    faiblesses = [
        ("Phase 2 incomplete",
         "4 services scaffoldes mais sans logique metier (student, review, notification, "
         "analytics). Ce sont des squelettes."),
        ("Pas de tests automatises",
         "Aucun test pytest ni Karma. Validation faite manuellement, pas reproductible facilement."),
        ("NLP limite",
         "TF-IDF + cosine fait des choix lexicaux, pas semantiques. Ne generalise pas a des "
         "formulations totalement inedites."),
        ("Scraping fsbm.ma limite",
         "Le site est une SPA JS, le scraping HTTP brut renvoie peu. Necessiterait Playwright."),
        ("Pas de monitoring",
         "Pas de Prometheus, Grafana, ou logging structure. Difficile a debugger en prod."),
        ("Authentification manquante",
         "Pas d'auth en Phase 1 = pas de personnalisation par utilisateur reel."),
        ("Mobile non optimise",
         "Responsive de base, mais pas d'experience native mobile (notifications push, etc.)."),
    ]
    for n, d in faiblesses:
        story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

    story.append(Paragraph("15.3 Scalabilite", ST_H1))
    story.append(Paragraph(
        "L'architecture micro-services est <b>nativement scalable</b>. Voici les actions a mener "
        "pour passer de 100 a 10 000 utilisateurs concurrents :",
        ST_BODY))

    scalability = [
        ("Niveau 1 (1-100 users)", "Setup actuel suffit. Pas d'optimisation necessaire."),
        ("Niveau 2 (100-1k users)", "Workers uvicorn (uvicorn --workers 4), cache Redis pour overview."),
        ("Niveau 3 (1k-10k users)", "Repliquer chaque service x3, MySQL master-slave, MongoDB replica set."),
        ("Niveau 4 (10k+ users)", "Kubernetes, autoscaling, CDN pour Angular, sharding BDD."),
    ]
    for n, d in scalability:
        story.append(Paragraph(f"<b>{n}.</b> {d}", ST_LIST))

    story.append(Paragraph("15.4 Pertinence academique", ST_H1))
    story.append(Paragraph(
        "Ce projet coche les cases attendues d'un PFE Licence DI :",
        ST_BODY))
    academic_pertinence = [
        "Maitrise d'un framework front moderne (Angular)",
        "Conception d'API REST avec validation",
        "Modelisation base relationnelle (16 tables 3NF)",
        "Introduction au NoSQL (MongoDB)",
        "Notions d'IA appliquee (NLP, TF-IDF, cosine)",
        "Architecture distribuee (micro-services)",
        "Gestion de projet (4 livrables PDF, scripts, doc)",
        "Travail d'equipe (3 membres, repartition claire)",
        "Documentation technique (4 PDFs detailles)",
        "Resolution de problemes reels (zombies WSL, encoding, etc.)",
    ]
    for p in academic_pertinence:
        story.append(Paragraph(f"• {p}", ST_LIST))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # CHAPITRE 16 - CONCLUSION
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Chapitre 16 - Conclusion", ST_CHAPTER))

    story.append(Paragraph("16.1 Recapitulatif", ST_H1))
    story.append(Paragraph(
        "Ce projet de fin d'etudes a permis de concevoir et realiser une <b>plateforme universitaire "
        "intelligente complete</b> repondant aux besoins informationnels des etudiants de la FSBM. "
        "Le resultat depasse le simple chatbot : c'est un veritable ecosysteme de services "
        "interconnectes (chatbot multilingue, referentiel academique, donnees realistes, interface "
        "moderne) bati selon les meilleures pratiques de l'industrie logicielle.",
        ST_BODY))

    story.append(Paragraph("16.2 Apports techniques", ST_H1))
    apports = [
        "Maitrise de FastAPI + SQLAlchemy 2.0 async + Pydantic v2",
        "Maitrise d'Angular 17 standalone + Signals + lazy loading",
        "Implementation d'un moteur NLP multilingue de zero",
        "Conception et generation de 3000+ donnees realistes",
        "Architecture micro-services SQL + NoSQL",
        "Resolution de problemes systeme Windows (zombies WSL)",
        "Generation programmatique de PDFs professionnels (reportlab)",
    ]
    for a in apports:
        story.append(Paragraph(f"• {a}", ST_LIST))

    story.append(Paragraph("16.3 Apports humains et methodologiques", ST_H1))
    apports_h = [
        "Travail en equipe avec repartition claire (backend / frontend / contenu)",
        "Documentation systematique a chaque etape",
        "Gestion de versions et iteration (v1, v2, v3 du dataset)",
        "Adaptation aux contraintes Windows et choix techniques imposes",
        "Communication trilingue (FR / EN / Darija marocain)",
    ]
    for a in apports_h:
        story.append(Paragraph(f"• {a}", ST_LIST))

    story.append(Paragraph("16.4 Perspectives", ST_H1))
    story.append(Paragraph(
        "Le projet est conçu comme une <b>base solide et extensible</b>. La Phase 2 ajoutera :",
        ST_BODY))
    phase2 = [
        "<b>Authentification</b> JWT avec 4 roles (Student, Prof, Scolarite, Admin)",
        "<b>Reviews MongoDB</b> avec analyse de sentiment",
        "<b>Notifications</b> push en temps reel via Server-Sent Events",
        "<b>Dashboard admin</b> avec KPIs et top intents",
        "<b>Tests automatises</b> pytest + Karma/Jasmine",
        "<b>Application mobile</b> Flutter avec API existante",
    ]
    for p in phase2:
        story.append(Paragraph(f"• {p}", ST_LIST))

    story.append(Paragraph("16.5 Mot final", ST_H1))
    story.append(alert_box(
        "Au-dela de la valeur technique, ce projet illustre une vision : <b>l'informatique au "
        "service du service public educatif marocain</b>. Le chatbot et la plateforme ne sont pas "
        "des prouesses techniques pour la beaute du geste, mais des outils concrets qui peuvent "
        "ameliorer le quotidien de milliers d'etudiants de la FSBM.",
        kind="success", title="Vision"))

    story.append(Paragraph(
        "Nous esperons que ce travail inspire d'autres etudiants de la FSBM et au-dela a "
        "construire des outils qui resolvent des vrais problemes pour de vrais utilisateurs - "
        "avec rigueur technique, pedagogie et ouverture sur la langue de leurs pairs.",
        ST_BODY))

    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(
        "<i>AKRAM BELMOUSSA, ZAKARIA, NOUHAILA</i><br/>"
        "<i>Faculte des Sciences Ben M'Sick - 2025/2026</i>",
        ParagraphStyle('Signoff', parent=ST_BODY, alignment=TA_CENTER, textColor=PRIMARY)))
    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════
    # GLOSSAIRE
    # ═══════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Glossaire", ST_CHAPTER))
    glossary = [
        ("API REST", "Architecture HTTP pour exposer des donnees structurees (typiquement JSON)."),
        ("Apogee", "Logiciel de gestion etudiante des universites marocaines."),
        ("Async/await", "Modele de programmation asynchrone evitant le blocage I/O."),
        ("Bootstrap (Angular)", "Demarrage de l'application via bootstrapApplication()."),
        ("CNE", "Code National Etudiant - identifiant unique de l'etudiant marocain."),
        ("Cosine similarity", "Mesure de similarite entre 2 vecteurs (0 = orthogonaux, 1 = identiques)."),
        ("Dependency Injection", "Pattern ou les dependances sont fournies de l'exterieur (FastAPI, Angular)."),
        ("Lazy loading", "Chargement d'un composant uniquement au moment ou il est necessaire."),
        ("Lifespan", "Mecanisme FastAPI pour executer du code au demarrage/arret."),
        ("Micro-service", "Service autonome avec une mission unique, communique via reseau."),
        ("n-gramme", "Sequence de N tokens consecutifs (unigramme, bigramme, trigramme)."),
        ("NLP", "Natural Language Processing - traitement automatique du langage."),
        ("ORM", "Object-Relational Mapping - traduit des objets en SQL et inversement."),
        ("Pydantic", "Lib Python de validation par typage."),
        ("Signal (Angular)", "Primitive de reactivite Angular 17 (alternative a RxJS)."),
        ("SPA", "Single Page Application - app web qui charge un seul HTML puis manipule le DOM."),
        ("Stemming", "Reduction d'un mot a sa racine ('mangeait' -> 'mang')."),
        ("Stopwords", "Mots tres frequents sans valeur semantique ('le', 'de', 'et')."),
        ("Swagger", "Specification OpenAPI generee automatiquement par FastAPI."),
        ("TF-IDF", "Term Frequency - Inverse Document Frequency - mesure d'importance lexicale."),
    ]
    for t, d in glossary:
        story.append(Paragraph(f"<b>{t}.</b> {d}", ST_LIST))

    # ═══════════════════════════════════════════════════════════════════════
    # FIN
    # ═══════════════════════════════════════════════════════════════════════
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF genere : {out_path}")
    print(f"Taille : {out_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    build()
