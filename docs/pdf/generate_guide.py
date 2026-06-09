"""
============================================================================
 FSBM Platform — Générateur PDF 2 : Guide Technique & Installation
============================================================================
Guide pratique pas-à-pas Windows pour installer, configurer, lancer et
exploiter la plateforme FSBM. ~25-30 pages.
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
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image,
    Table, TableStyle, KeepTogether,
)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ─── Couleurs ──────────────────────────────────────────────────────────────────
PRIMARY     = HexColor('#1C3F6E')
PRIMARY_MID = HexColor('#265DAB')
ACCENT      = HexColor('#16B5A6')
ACCENT_PALE = HexColor('#E5F8F5')
GREY_DARK   = HexColor('#2D3748')
GREY_MID    = HexColor('#4A5568')
GREY_LIGHT  = HexColor('#EDF1F6')
SUCCESS     = HexColor('#22C55E')
WARNING     = HexColor('#F59E0B')
DANGER      = HexColor('#EF4444')

ROOT = Path(__file__).parent.parent.parent
LOGO_FSBM = ROOT / "frontend" / "src" / "assets" / "logos" / "fsbm.png"

# ─── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()
ST_TITLE = ParagraphStyle('TitleX', parent=styles['Title'], fontName='Helvetica-Bold',
    fontSize=26, textColor=PRIMARY, alignment=TA_CENTER, spaceAfter=14, leading=32)
ST_SUBTITLE = ParagraphStyle('Subtitle', parent=styles['Heading2'], fontName='Helvetica',
    fontSize=15, textColor=GREY_DARK, alignment=TA_CENTER, spaceAfter=10, leading=20)
ST_CHAPTER = ParagraphStyle('Chapter', parent=styles['Heading1'], fontName='Helvetica-Bold',
    fontSize=20, textColor=PRIMARY, alignment=TA_LEFT, spaceBefore=20, spaceAfter=12, leading=26)
ST_H1 = ParagraphStyle('H1', parent=styles['Heading1'], fontName='Helvetica-Bold',
    fontSize=16, textColor=PRIMARY, spaceBefore=16, spaceAfter=10, leading=20)
ST_H2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName='Helvetica-Bold',
    fontSize=13, textColor=PRIMARY_MID, spaceBefore=12, spaceAfter=7, leading=17)
ST_H3 = ParagraphStyle('H3', parent=styles['Heading3'], fontName='Helvetica-Bold',
    fontSize=11, textColor=GREY_DARK, spaceBefore=8, spaceAfter=5, leading=15)
ST_BODY = ParagraphStyle('Body', parent=styles['BodyText'], fontName='Helvetica',
    fontSize=10.5, textColor=GREY_DARK, alignment=TA_JUSTIFY, spaceAfter=8, leading=15)
ST_BODY_BOLD = ParagraphStyle('BodyBold', parent=ST_BODY, fontName='Helvetica-Bold')
ST_CODE = ParagraphStyle('Code', parent=styles['Code'], fontName='Courier',
    fontSize=9, textColor=PRIMARY_MID, backColor=GREY_LIGHT,
    leftIndent=12, rightIndent=12, spaceAfter=8, leading=12, borderPadding=8,
    borderColor=PRIMARY_MID, borderWidth=0.5)
ST_LIST = ParagraphStyle('List', parent=ST_BODY, leftIndent=14, bulletIndent=4)
ST_TOC = ParagraphStyle('TOC', parent=ST_BODY, fontName='Helvetica',
    fontSize=11, textColor=GREY_DARK, spaceAfter=4, leading=16)
ST_STEP = ParagraphStyle('Step', parent=ST_BODY, fontName='Helvetica-Bold',
    fontSize=12, textColor=ACCENT, spaceBefore=12, spaceAfter=6, leading=16)


def header_footer(c, doc):
    c.saveState()
    c.setStrokeColor(GREY_LIGHT); c.setLineWidth(0.5)
    c.line(2*cm, 1.5*cm, A4[0]-2*cm, 1.5*cm)
    c.setFont('Helvetica', 8); c.setFillColor(GREY_MID)
    c.drawString(2*cm, 1*cm, "Guide Technique — FSBM Platform")
    c.drawCentredString(A4[0]/2, 1*cm, "2025/2026")
    c.drawRightString(A4[0]-2*cm, 1*cm, f"Page {doc.page}")
    if doc.page > 1:
        c.setFont('Helvetica', 8); c.setFillColor(PRIMARY)
        c.drawString(2*cm, A4[1]-1*cm, "Faculté des Sciences Ben M'Sick — PFE 2025/2026")
        c.line(2*cm, A4[1]-1.2*cm, A4[0]-2*cm, A4[1]-1.2*cm)
    c.restoreState()


def code_block(text: str):
    """Bloc de code formaté."""
    return Paragraph(text.replace('\n', '<br/>').replace(' ', '&nbsp;'), ST_CODE)


def alert_box(content: str, kind: str = "info"):
    colors = {
        "info":    (HexColor('#3B82F6'), HexColor('#EBF5FF'), "ℹ️"),
        "warning": (WARNING,             HexColor('#FFFBEB'), "⚠️"),
        "success": (SUCCESS,             HexColor('#F0FDF4'), "✅"),
        "danger":  (DANGER,              HexColor('#FEF2F2'), "❌"),
    }
    border, bg, icon = colors.get(kind, colors["info"])
    t = Table([[Paragraph(f'{icon} {content}', ST_BODY)]], colWidths=[16*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('LINEBEFORE', (0,0), (-1,-1), 4, border),
        ('PADDING',    (0,0), (-1,-1), 10),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t


def build():
    out_path = Path(__file__).parent / "FSBM_Platform_Guide_Technique.pdf"
    doc = SimpleDocTemplate(
        str(out_path), pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="Guide Technique - FSBM Platform",
        author="AKRAM BELMOUSSA, ZAKARIA, NOUHAILA",
    )
    story = []

    # ════════════════ COUVERTURE ════════════════
    story.append(Spacer(1, 2*cm))
    if LOGO_FSBM.exists():
        story.append(Image(str(LOGO_FSBM), width=5*cm, height=5*cm, hAlign='CENTER'))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("FSBM PLATFORM", ST_TITLE))
    story.append(Paragraph("Guide Technique &amp; d'Installation", ST_SUBTITLE))
    story.append(Spacer(1, 0.4*cm))
    t = Table([
        [Paragraph('<font color="#FFFFFF"><b>Manuel pratique pas-à-pas pour Windows</b></font>', ST_BODY)],
    ], colWidths=[14*cm], hAlign='CENTER')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), ACCENT),
        ('PADDING',    (0,0), (-1,-1), 12),
        ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t)
    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph(
        "Ce guide couvre l'installation, la configuration, le lancement et "
        "l'utilisation de la plateforme FSBM en environnement Windows.",
        ParagraphStyle('Intro', parent=ST_BODY, alignment=TA_CENTER, fontSize=11)
    ))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("Équipe PFE — 2025/2026",
                          ParagraphStyle('A', parent=ST_BODY, alignment=TA_CENTER, fontSize=11, textColor=GREY_MID)))
    story.append(Paragraph("AKRAM BELMOUSSA · ZAKARIA · NOUHAILA",
                          ParagraphStyle('A', parent=ST_BODY, alignment=TA_CENTER, fontSize=10, textColor=GREY_MID)))
    story.append(PageBreak())

    # ════════════════ SOMMAIRE ════════════════
    story.append(Paragraph("Sommaire", ST_CHAPTER))
    toc = [
        ("Chapitre 1 — Pré-requis Windows", "3"),
        ("    1.1  Logiciels nécessaires", "3"),
        ("    1.2  Vérifications préalables", "5"),
        ("Chapitre 2 — Installation pas-à-pas", "6"),
        ("    2.1  Téléchargement du projet", "6"),
        ("    2.2  Méthode 1 : Setup ONE-CLICK (recommandé)", "7"),
        ("    2.3  Méthode 2 : Installation manuelle", "8"),
        ("Chapitre 3 — Configuration", "11"),
        ("    3.1  Fichiers .env", "11"),
        ("    3.2  Base MySQL", "12"),
        ("    3.3  MongoDB (optionnel)", "13"),
        ("Chapitre 4 — Lancement des services", "14"),
        ("    4.1  Démarrage automatique", "14"),
        ("    4.2  Démarrage manuel", "15"),
        ("    4.3  Vérification du bon fonctionnement", "16"),
        ("Chapitre 5 — Référence des APIs", "17"),
        ("    5.1  chatbot-service (port 5001)", "17"),
        ("    5.2  academic-service (port 5002)", "20"),
        ("Chapitre 6 — Utilisation du frontend", "23"),
        ("Chapitre 7 — Dépannage (FAQ)", "25"),
        ("Chapitre 8 — Architecture du code", "28"),
        ("Annexes", "30"),
    ]
    for label, page in toc:
        dots = '.' * (max(1, 78 - len(label) - len(page)))
        story.append(Paragraph(f"{label} <font color='#8095A8'>{dots}</font> <b>{page}</b>", ST_TOC))
    story.append(PageBreak())

    # ════════════════ CHAPITRE 1 — PRÉ-REQUIS ════════════════
    story.append(Paragraph("Chapitre 1 — Pré-requis Windows", ST_CHAPTER))

    story.append(Paragraph("1.1 Logiciels nécessaires", ST_H1))
    story.append(Paragraph(
        "Avant de commencer, vérifie que les logiciels suivants sont installés sur ton poste Windows. "
        "Si l'un manque, suis les liens officiels pour le télécharger.",
        ST_BODY
    ))
    prereq = [
        ("Python 3.10+",  "Recommandé : 3.12 ou 3.13. Évite 3.14 (récent, parfois incompatible).",
         "python.org/downloads", "✅ Cocher « Add Python to PATH » à l'installation"),
        ("Node.js 18+",   "Inclut npm, nécessaire pour Angular.",
         "nodejs.org", "Version LTS recommandée"),
        ("MySQL 8.0+",    "Serveur de base de données relationnelle.",
         "dev.mysql.com/downloads/installer", "Installer aussi « MySQL Workbench »"),
        ("MongoDB 7+",    "Optionnel pour la Phase 1 (reviews/feedbacks).",
         "mongodb.com/try/download/community", "Choisir « MongoDB Server »"),
        ("Git (optionnel)","Pour cloner le projet si distribué via Git.",
         "git-scm.com", "Inclus dans Visual Studio Code"),
        ("Éditeur de code","VS Code recommandé pour explorer le code source.",
         "code.visualstudio.com", "Extensions : Python, Angular Snippets"),
    ]
    pr_table = Table(
        [[Paragraph('<b>Logiciel</b>', ST_BODY_BOLD), Paragraph('<b>Rôle</b>', ST_BODY_BOLD),
          Paragraph('<b>Source</b>', ST_BODY_BOLD), Paragraph('<b>Conseil</b>', ST_BODY_BOLD)]] +
        [[Paragraph(f'<b>{n}</b>', ST_BODY), Paragraph(r, ST_BODY),
          Paragraph(f'<font face="Courier" size="8">{s}</font>', ST_BODY),
          Paragraph(c, ST_BODY)] for n, r, s, c in prereq],
        colWidths=[3*cm, 5*cm, 4*cm, 4*cm]
    )
    pr_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR',  (0,0), (-1,0), white),
        ('BOX',        (0,0), (-1,-1), 0.3, GREY_LIGHT),
        ('INNERGRID',  (0,0), (-1,-1), 0.2, GREY_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, GREY_LIGHT]),
        ('PADDING',    (0,0), (-1,-1), 5),
        ('VALIGN',     (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(pr_table)

    story.append(Paragraph("1.2 Vérifications préalables", ST_H1))
    story.append(Paragraph(
        "Ouvre un terminal <b>PowerShell</b> ou <b>cmd.exe</b> et tape les commandes suivantes "
        "pour vérifier que tout est installé :",
        ST_BODY
    ))
    story.append(code_block(
        "py --version\n"
        "# Doit afficher : Python 3.12.x (ou similaire)\n\n"
        "node --version\n"
        "# Doit afficher : v18.x.x ou v20.x.x\n\n"
        "npm --version\n"
        "# Doit afficher : 9.x ou 10.x"
    ))
    story.append(alert_box(
        "<b>MySQL non détecté ?</b> C'est normal : le client mysql.exe n'est souvent pas "
        "dans le PATH. Le script SETUP.bat le détectera automatiquement.",
        "info"
    ))
    story.append(PageBreak())

    # ════════════════ CHAPITRE 2 — INSTALLATION ════════════════
    story.append(Paragraph("Chapitre 2 — Installation pas-à-pas", ST_CHAPTER))

    story.append(Paragraph("2.1 Téléchargement du projet", ST_H1))
    story.append(Paragraph(
        "Le projet est livré dans un dossier <b>chatbot-fsbm-platform/</b>. Place-le quelque part "
        "sur ton disque, par exemple :",
        ST_BODY
    ))
    story.append(code_block("C:\\Users\\<ton_nom>\\studies\\PFE\\chatbot-fsbm-platform\\"))
    story.append(Paragraph(
        "<b>Structure attendue :</b>",
        ST_BODY
    ))
    story.append(code_block(
        "chatbot-fsbm-platform/\n"
        "  ├── SETUP.bat              <-- Script one-click\n"
        "  ├── README.md\n"
        "  ├── docs/                  Documentation + PDFs\n"
        "  ├── database/              Scripts SQL et générateur\n"
        "  ├── services/              Micro-services FastAPI\n"
        "  ├── frontend/              Application Angular 17\n"
        "  └── scripts/               Scripts utilitaires"
    ))

    story.append(Paragraph("2.2 Méthode 1 — Setup ONE-CLICK (recommandé)", ST_H1))
    story.append(Paragraph(
        "Le script <b>SETUP.bat</b> à la racine du projet fait <b>TOUT</b> automatiquement : "
        "config .env, install Python, install npm, init MySQL, lance les services.",
        ST_BODY
    ))
    story.append(alert_box(
        "Le SEUL input demandé est ton mot de passe MySQL. Aucune autre saisie nécessaire.",
        "success"
    ))
    story.append(Paragraph("Étape 1 : Exécuter le script", ST_STEP))
    story.append(Paragraph(
        "Double-clique sur <b>SETUP.bat</b>, ou depuis un terminal :",
        ST_BODY
    ))
    story.append(code_block(
        "cd C:\\Users\\belmo\\studies\\PFE\\chatbot-fsbm-platform\n"
        "SETUP.bat"
    ))
    story.append(Paragraph("Étape 2 : Entrer ton mot de passe MySQL", ST_STEP))
    story.append(Paragraph(
        "Quand le script te le demande, tape ton mot de passe (utilisateur root) et appuie sur Entrée. "
        "Le mot de passe n'est pas affiché à l'écran — c'est normal.",
        ST_BODY
    ))
    story.append(Paragraph("Étape 3 : Attendre la fin (3 à 5 minutes)", ST_STEP))
    story.append(Paragraph(
        "Le script enchaîne automatiquement :",
        ST_BODY
    ))
    for s in [
        "[1/5] Configuration des fichiers .env (instantané)",
        "[2/5] Installation Python (1 minute)",
        "[3/5] Installation npm (1-2 minutes)",
        "[4/5] Chargement MySQL (30 secondes)",
        "[5/5] Lancement des 3 services (5 secondes)",
    ]:
        story.append(Paragraph(f"• {s}", ST_LIST))
    story.append(Paragraph("Étape 4 : Ouvrir le navigateur", ST_STEP))
    story.append(Paragraph(
        "Au bout de 30 secondes, ouvre <b>http://localhost:4200</b> dans ton navigateur. "
        "Tu devrais voir le dashboard de la plateforme FSBM.",
        ST_BODY
    ))
    story.append(alert_box(
        "Si une erreur survient, lis le message dans la console. Les causes les plus fréquentes sont : "
        "mot de passe MySQL incorrect, MySQL non démarré, ports 5001/5002/4200 déjà occupés.",
        "warning"
    ))

    story.append(Paragraph("2.3 Méthode 2 — Installation manuelle", ST_H1))
    story.append(Paragraph(
        "Si tu préfères contrôler chaque étape, voici la procédure manuelle :",
        ST_BODY
    ))
    story.append(Paragraph("Étape A : Installer les dépendances Python", ST_STEP))
    story.append(code_block(
        "cd C:\\Users\\belmo\\studies\\PFE\\chatbot-fsbm-platform\\services\\academic-service\n"
        "py -m pip install -r requirements.txt\n\n"
        "cd ..\\chatbot-service\n"
        "py -m pip install -r requirements.txt"
    ))
    story.append(Paragraph("Étape B : Installer les dépendances Angular", ST_STEP))
    story.append(code_block(
        "cd ..\\..\\frontend\n"
        "npm install"
    ))
    story.append(Paragraph(
        "<b>Note :</b> npm install peut prendre 1-2 minutes selon ta connexion.",
        ST_BODY
    ))
    story.append(Paragraph("Étape C : Créer les fichiers .env", ST_STEP))
    story.append(Paragraph(
        "Copie <b>.env.example</b> vers <b>.env</b> dans chaque service et édite la ligne "
        "<i>DB_PASSWORD=</i> :",
        ST_BODY
    ))
    story.append(code_block(
        "cd ..\\services\\academic-service\n"
        "copy .env.example .env\n"
        "notepad .env\n"
        "# Edite la ligne : DB_PASSWORD=TON_MOT_DE_PASSE\n\n"
        "cd ..\\chatbot-service\n"
        "copy .env.example .env\n"
        "notepad .env"
    ))
    story.append(Paragraph("Étape D : Initialiser MySQL", ST_STEP))
    story.append(Paragraph(
        "Ouvre <b>MySQL Workbench</b> (recommandé) ou un terminal mysql, puis exécute dans l'ordre :",
        ST_BODY
    ))
    story.append(code_block(
        "SOURCE database\\mysql\\01_schema.sql;\n"
        "SOURCE database\\mysql\\02_seed_static.sql;\n"
        "SOURCE database\\mysql\\03_seed_modules.sql;\n"
        "SOURCE database\\mysql\\04_seed_data.sql;"
    ))
    story.append(Paragraph("Étape E : Lancer les services (3 terminaux)", ST_STEP))
    story.append(Paragraph(
        "Ouvre 3 fenêtres de terminal et lance dans chacune :",
        ST_BODY
    ))
    story.append(Paragraph("<b>Terminal 1</b> — academic-service :", ST_BODY))
    story.append(code_block(
        "set PYTHONIOENCODING=utf-8\n"
        "cd services\\academic-service\n"
        "py -m uvicorn app.main:app --reload --port 5002"
    ))
    story.append(Paragraph("<b>Terminal 2</b> — chatbot-service :", ST_BODY))
    story.append(code_block(
        "set PYTHONIOENCODING=utf-8\n"
        "cd services\\chatbot-service\n"
        "py -m uvicorn app.main:app --reload --port 5001"
    ))
    story.append(Paragraph("<b>Terminal 3</b> — frontend Angular :", ST_BODY))
    story.append(code_block(
        "cd frontend\n"
        "npm start"
    ))
    story.append(PageBreak())

    # ════════════════ CHAPITRE 3 — CONFIGURATION ════════════════
    story.append(Paragraph("Chapitre 3 — Configuration", ST_CHAPTER))

    story.append(Paragraph("3.1 Fichiers .env", ST_H1))
    story.append(Paragraph(
        "Chaque service utilise un fichier <b>.env</b> pour ses paramètres sensibles "
        "(mot de passe BDD, ports, URLs). Ces fichiers ne doivent jamais être commités.",
        ST_BODY
    ))

    story.append(Paragraph("services/academic-service/.env", ST_H2))
    story.append(code_block(
        "SERVICE_NAME=academic-service\n"
        "SERVICE_PORT=5002\n"
        "ENV=development\n"
        "DEBUG=true\n"
        "\n"
        "DB_HOST=localhost\n"
        "DB_PORT=3306\n"
        "DB_NAME=fsbm_db\n"
        "DB_USER=root\n"
        "DB_PASSWORD=TON_MOT_DE_PASSE\n"
        "\n"
        "CORS_ORIGINS=http://localhost:4200,http://localhost:5001"
    ))

    story.append(Paragraph("services/chatbot-service/.env", ST_H2))
    story.append(code_block(
        "SERVICE_NAME=chatbot-service\n"
        "SERVICE_PORT=5001\n"
        "ENV=development\n"
        "DEBUG=true\n"
        "\n"
        "DB_HOST=localhost\n"
        "DB_PORT=3306\n"
        "DB_NAME=fsbm_db\n"
        "DB_USER=root\n"
        "DB_PASSWORD=TON_MOT_DE_PASSE\n"
        "\n"
        "ACADEMIC_SERVICE_URL=http://localhost:5002\n"
        "CONFIDENCE_THRESHOLD=0.15\n"
        "MAX_HISTORY_MESSAGES=20\n"
        "MAX_MESSAGE_LENGTH=500\n"
        "\n"
        "CORS_ORIGINS=http://localhost:4200,http://localhost:3000"
    ))

    story.append(Paragraph("3.2 Base MySQL", ST_H1))
    story.append(Paragraph(
        "Les 4 scripts SQL doivent être exécutés <b>dans l'ordre</b>. Chacun peut être chargé via "
        "MySQL Workbench (recommandé) ou en ligne de commande.",
        ST_BODY
    ))
    sql_files = [
        ("01_schema.sql",      "Crée la base fsbm_db + 16 tables avec contraintes."),
        ("02_seed_static.sql", "Insère 5 départements, 7 licences, 18 masters, 16 catégories FAQ, 8 clubs, 5 événements."),
        ("03_seed_modules.sql","Insère 100+ modules détaillés par filière."),
        ("04_seed_data.sql",   "Génère 107 professeurs + 2970 étudiants + EDT + examens + notes (720 KB)."),
    ]
    sql_t = Table(
        [[Paragraph('<b>Fichier</b>', ST_BODY_BOLD), Paragraph('<b>Contenu</b>', ST_BODY_BOLD)]] +
        [[Paragraph(f'<font face="Courier">{n}</font>', ST_BODY), Paragraph(d, ST_BODY)] for n, d in sql_files],
        colWidths=[4*cm, 12*cm]
    )
    sql_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR',  (0,0), (-1,0), white),
        ('BOX',        (0,0), (-1,-1), 0.3, GREY_LIGHT),
        ('INNERGRID',  (0,0), (-1,-1), 0.2, GREY_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, GREY_LIGHT]),
        ('PADDING',    (0,0), (-1,-1), 5),
        ('VALIGN',     (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(sql_t)
    story.append(alert_box(
        "Si tu utilises MySQL Workbench, désactive le « Safe Update Mode » dans "
        "<b>Edit → Preferences → SQL Editor</b> avant de charger 04_seed_data.sql.",
        "warning"
    ))

    story.append(Paragraph("3.3 MongoDB (optionnel pour Phase 1)", ST_H1))
    story.append(Paragraph(
        "MongoDB est utilisé en Phase 2 pour les reviews et l'analyse de sentiment. Pour l'initialiser :",
        ST_BODY
    ))
    story.append(code_block(
        "# Depuis un terminal\n"
        "mongosh < C:\\Users\\belmo\\studies\\PFE\\chatbot-fsbm-platform\\database\\mongodb\\init.js"
    ))
    story.append(Paragraph(
        "Cela crée la base <b>fsbm_reviews</b> avec 6 collections + des données seed.",
        ST_BODY
    ))
    story.append(PageBreak())

    # ════════════════ CHAPITRE 4 — LANCEMENT ════════════════
    story.append(Paragraph("Chapitre 4 — Lancement des services", ST_CHAPTER))

    story.append(Paragraph("4.1 Démarrage automatique (recommandé)", ST_H1))
    story.append(Paragraph(
        "Le script <b>scripts/start-all.bat</b> ouvre 3 fenêtres et lance les 3 services :",
        ST_BODY
    ))
    story.append(code_block(
        "cd C:\\Users\\belmo\\studies\\PFE\\chatbot-fsbm-platform\n"
        "scripts\\start-all.bat"
    ))

    story.append(Paragraph("4.2 Démarrage manuel", ST_H1))
    story.append(Paragraph(
        "Voir Chapitre 2, Méthode 2, Étape E.",
        ST_BODY
    ))

    story.append(Paragraph("4.3 Vérification du bon fonctionnement", ST_H1))
    story.append(Paragraph(
        "Une fois les services lancés, vérifie chaque URL dans ton navigateur :",
        ST_BODY
    ))
    urls = [
        ("http://localhost:5001/api/health", "Status du chatbot-service",     "{ status: 'ok', nlp_ready: true }"),
        ("http://localhost:5001/docs",        "Documentation Swagger chatbot", "Interface Swagger UI"),
        ("http://localhost:5002/api/health",  "Status de l'academic-service",  "{ status: 'ok' }"),
        ("http://localhost:5002/api/overview","Compteurs globaux",             "JSON avec stats des tables"),
        ("http://localhost:5002/docs",        "Documentation Swagger academic","Interface Swagger UI"),
        ("http://localhost:4200",             "Frontend Angular",              "Dashboard FSBM"),
    ]
    url_t = Table(
        [[Paragraph('<b>URL</b>', ST_BODY_BOLD), Paragraph('<b>Rôle</b>', ST_BODY_BOLD), Paragraph('<b>Attendu</b>', ST_BODY_BOLD)]] +
        [[Paragraph(f'<font face="Courier" size="8">{u}</font>', ST_BODY), Paragraph(r, ST_BODY), Paragraph(a, ST_BODY)] for u, r, a in urls],
        colWidths=[6.5*cm, 4.5*cm, 5*cm]
    )
    url_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR',  (0,0), (-1,0), white),
        ('BOX',        (0,0), (-1,-1), 0.3, GREY_LIGHT),
        ('INNERGRID',  (0,0), (-1,-1), 0.2, GREY_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, GREY_LIGHT]),
        ('PADDING',    (0,0), (-1,-1), 5),
        ('VALIGN',     (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(url_t)
    story.append(PageBreak())

    # ════════════════ CHAPITRE 5 — APIs ════════════════
    story.append(Paragraph("Chapitre 5 — Référence des APIs", ST_CHAPTER))

    story.append(Paragraph("5.1 chatbot-service (port 5001)", ST_H1))

    story.append(Paragraph("POST /api/chat", ST_H2))
    story.append(Paragraph("Envoie un message au chatbot et reçoit la réponse.", ST_BODY))
    story.append(Paragraph("<b>Body JSON :</b>", ST_BODY))
    story.append(code_block(
        '{\n'
        '  "message": "Comment m\'inscrire en master IADS ?",\n'
        '  "session_id": "sess_abc123",   // optionnel\n'
        '  "user_id": null                // optionnel\n'
        '}'
    ))
    story.append(Paragraph("<b>Réponse :</b>", ST_BODY))
    story.append(code_block(
        '{\n'
        '  "response": "Master IADS - Intelligence Artificielle...",\n'
        '  "intent": "master_iads",\n'
        '  "confidence": 0.78,\n'
        '  "conversation_id": 1,\n'
        '  "session_id": "sess_abc123",\n'
        '  "top_candidates": [...],\n'
        '  "suggestions": ["Quels masters", "Master sécurité"],\n'
        '  "response_time_ms": 45\n'
        '}'
    ))

    story.append(Paragraph("POST /api/chat/feedback", ST_H2))
    story.append(Paragraph("Note une réponse du chatbot.", ST_BODY))
    story.append(code_block(
        '{\n'
        '  "conversation_id": 1,\n'
        '  "note": 5,                     // 1 à 5\n'
        '  "is_helpful": true,            // optionnel\n'
        '  "commentaire": "Très clair !"  // optionnel\n'
        '}'
    ))

    story.append(Paragraph("GET /api/chat/history/{session_id}", ST_H2))
    story.append(Paragraph("Récupère l'historique d'une conversation.", ST_BODY))

    story.append(Paragraph("GET /api/chat/suggestions", ST_H2))
    story.append(Paragraph("Retourne 6 questions suggérées pour démarrer.", ST_BODY))

    story.append(Paragraph("GET /api/intents", ST_H2))
    story.append(Paragraph("Liste les 60+ intents reconnus par le chatbot.", ST_BODY))

    story.append(Paragraph("5.2 academic-service (port 5002)", ST_H1))

    api_acad = [
        ("GET", "/api/overview", "Compteurs globaux (dashboard)."),
        ("GET", "/api/departments", "Liste des 5 départements."),
        ("GET", "/api/departments/{id}", "Détail d'un département + comptes."),
        ("GET", "/api/departments/{id}/filieres", "Filières du département."),
        ("GET", "/api/departments/{id}/professors", "Profs du département."),
        ("GET", "/api/filieres", "Filières. Params : type, department_id, search, is_active."),
        ("GET", "/api/filieres/{id}", "Détail filière par ID."),
        ("GET", "/api/filieres/code/{code}", "Filière par code (SMI, DI, IADS...)."),
        ("GET", "/api/filieres/{id}/modules", "Modules groupés par semestre."),
        ("GET", "/api/modules", "Modules. Params : filiere_id, semester, search, limit."),
        ("GET", "/api/modules/{id}", "Détail module avec enseignants."),
        ("GET", "/api/modules/code/{code}", "Module par code."),
        ("GET", "/api/professors", "Profs paginés. Params : department_id, grade, search, page, page_size."),
        ("GET", "/api/professors/{id}", "Détail professeur."),
        ("GET", "/api/students", "Étudiants paginés. Filtres : filiere_id, annee_etude, statut, is_boursier, search."),
        ("GET", "/api/students/{id}", "Détail étudiant."),
        ("GET", "/api/students/cne/{cne}", "Étudiant par CNE."),
        ("GET", "/api/students/stats/by-filiere", "Stats d'effectifs par filière."),
        ("GET", "/api/schedule", "EDT. Params : filiere_id, semester, annee_etude, group_name."),
        ("GET", "/api/exams", "Examens. Params : filiere_id, session."),
        ("GET", "/api/announcements", "Annonces officielles."),
        ("GET", "/api/events", "Événements à venir."),
        ("GET", "/api/clubs", "Clubs étudiants."),
    ]
    aa_t = Table(
        [[Paragraph('<b>M</b>', ST_BODY_BOLD), Paragraph('<b>Endpoint</b>', ST_BODY_BOLD), Paragraph('<b>Description</b>', ST_BODY_BOLD)]] +
        [[Paragraph(f'<font color="#16B5A6"><b>{m}</b></font>', ST_BODY), Paragraph(f'<font face="Courier" size="9">{e}</font>', ST_BODY), Paragraph(d, ST_BODY)] for m, e, d in api_acad],
        colWidths=[1.3*cm, 6.7*cm, 8*cm]
    )
    aa_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR',  (0,0), (-1,0), white),
        ('BOX',        (0,0), (-1,-1), 0.3, GREY_LIGHT),
        ('INNERGRID',  (0,0), (-1,-1), 0.2, GREY_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, GREY_LIGHT]),
        ('PADDING',    (0,0), (-1,-1), 4),
        ('VALIGN',     (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(aa_t)
    story.append(alert_box(
        "Toutes les routes sont documentées et testables interactivement sur "
        "http://localhost:5002/docs (Swagger UI).",
        "info"
    ))
    story.append(PageBreak())

    # ════════════════ CHAPITRE 6 — UTILISATION FRONTEND ════════════════
    story.append(Paragraph("Chapitre 6 — Utilisation du frontend", ST_CHAPTER))
    story.append(Paragraph(
        "Le frontend est accessible sur <b>http://localhost:4200</b>. "
        "Voici un tour d'horizon des 8 pages :",
        ST_BODY
    ))
    pages = [
        ("🏠 Accueil (Dashboard)", "/", "Hero + 8 cartes stats live + actions rapides + 4 dernières annonces + 3 prochains événements."),
        ("🤖 Assistant IA",        "/chat", "Interface de chat avec messages animés, suggestions rapides, feedback 👍/👎."),
        ("🏢 Départements",        "/departements", "5 cartes des départements (Math-Info, Physique, Chimie, Biologie, Géologie)."),
        ("📚 Filières",            "/filieres", "25 cartes (7 licences + 18 masters) avec recherche, filtres par type."),
        ("📖 Détail filière",      "/filieres/:code", "Programme complet par semestre + débouchés + coordinateur."),
        ("📖 Modules",             "/modules", "100+ modules avec filtres filière/semestre, recherche."),
        ("👨‍🏫 Professeurs",       "/professeurs", "Annuaire de 107 profs paginé, recherche par nom/spécialité."),
        ("📰 Actualités",          "/actualites", "Annonces officielles + événements à venir."),
        ("🌟 Vie étudiante",       "/vie-etudiante", "8 clubs étudiants avec catégories, contacts, réseaux sociaux."),
    ]
    pg_t = Table(
        [[Paragraph('<b>Page</b>', ST_BODY_BOLD), Paragraph('<b>URL</b>', ST_BODY_BOLD), Paragraph('<b>Contenu</b>', ST_BODY_BOLD)]] +
        [[Paragraph(n, ST_BODY), Paragraph(f'<font face="Courier" size="9">{u}</font>', ST_BODY), Paragraph(d, ST_BODY)] for n, u, d in pages],
        colWidths=[3.5*cm, 3.5*cm, 9*cm]
    )
    pg_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR',  (0,0), (-1,0), white),
        ('BOX',        (0,0), (-1,-1), 0.3, GREY_LIGHT),
        ('INNERGRID',  (0,0), (-1,-1), 0.2, GREY_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, GREY_LIGHT]),
        ('PADDING',    (0,0), (-1,-1), 5),
        ('VALIGN',     (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(pg_t)

    story.append(Paragraph("Fonctionnalités transversales", ST_H1))
    transv = [
        ("🌙 Mode sombre",        "Toggle dans la sidebar (icône lune/soleil). Persistant entre sessions (localStorage)."),
        ("📱 Responsive",         "Sidebar passe en mode mini sur écrans < 1024px, layout adapté mobile < 768px."),
        ("⚡ Lazy loading",       "Chaque page se charge à la demande (< 30 KB par chunk)."),
        ("🔍 Recherche",          "Disponible sur les pages Filières, Modules, Professeurs avec debounce."),
        ("🎨 Animations",         "fadeInUp à l'affichage des cartes, hover effects, transitions de thème."),
        ("🔄 Live data",          "Toutes les pages consomment les vraies données depuis l'academic-service."),
    ]
    for n, d in transv:
        story.append(Paragraph(f"<b>{n}</b> — {d}", ST_LIST))
    story.append(PageBreak())

    # ════════════════ CHAPITRE 7 — DÉPANNAGE ════════════════
    story.append(Paragraph("Chapitre 7 — Dépannage (FAQ)", ST_CHAPTER))

    faqs = [
        ("« mysql : terme non reconnu » dans PowerShell",
         "Le client mysql.exe n'est pas dans le PATH. Soit utilise le chemin complet : "
         "<code>& \"C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysql.exe\"</code>, "
         "soit ajoute ce dossier au PATH système via Variables d'environnement Windows."),
        ("« No module named uvicorn » au lancement",
         "Les dépendances Python ne sont pas installées. Lance : "
         "<code>py -m pip install -r requirements.txt</code> dans chaque service."),
        ("« Access denied for user 'root' »",
         "Le mot de passe MySQL dans .env est incorrect. Vérifie services/academic-service/.env "
         "et services/chatbot-service/.env. Le mot de passe doit correspondre à celui de root@localhost."),
        ("« Duplicate entry » lors du chargement SQL",
         "Tu as déjà chargé les données. Lance d'abord : DROP DATABASE fsbm_db; puis re-exécute "
         "les 4 scripts dans l'ordre. Le script 01_schema.sql commence par DROP DATABASE IF EXISTS."),
        ("« Safe update mode » dans Workbench",
         "Workbench bloque les UPDATE sans WHERE. Va dans Edit > Preferences > SQL Editor "
         "et décoche « Safe Updates ». Puis Query > Reconnect to Server."),
        ("« UnicodeEncodeError » dans la console Python",
         "Le terminal Windows utilise cp1252 par défaut. Lance d'abord : "
         "<code>set PYTHONIOENCODING=utf-8</code> avant la commande Python."),
        ("Le port 5001/5002/4200 est déjà utilisé",
         "Un autre programme occupe le port. Trouve-le avec : <code>netstat -ano | findstr :5001</code> "
         "puis tue le processus avec son PID. Ou change le port dans le .env."),
        ("Le chatbot répond toujours « Je ne comprends pas »",
         "Le seuil de confiance peut être trop élevé. Vérifie CONFIDENCE_THRESHOLD=0.15 dans "
         "chatbot-service/.env. Sinon, vérifie que faq_dataset.json existe bien dans services/chatbot-service/data/."),
        ("Le dashboard affiche un warning « backend non joignable »",
         "L'academic-service ne tourne pas ou est sur un autre port. Vérifie qu'il répond sur "
         "http://localhost:5002/api/health avant de recharger le frontend."),
        ("Les emojis ne s'affichent pas dans le terminal",
         "C'est uniquement un problème d'affichage du terminal cmd.exe. Les emojis sont bien dans "
         "la base et s'affichent correctement dans le navigateur."),
        ("npm install est très lent",
         "Vérifie ta connexion. Tu peux essayer un autre registry : "
         "<code>npm config set registry https://registry.npmmirror.com/</code>."),
        ("« Cannot find module './app/main' »",
         "Tu lances uvicorn depuis le mauvais dossier. Vérifie que tu es bien dans "
         "services/academic-service/ ou services/chatbot-service/ avant de lancer."),
    ]
    for q, a in faqs:
        story.append(Paragraph(f"<b>Q : {q}</b>", ST_H3))
        story.append(Paragraph(f"R : {a}", ST_BODY))
        story.append(Spacer(1, 0.15*cm))
    story.append(PageBreak())

    # ════════════════ CHAPITRE 8 — ARCHITECTURE DU CODE ════════════════
    story.append(Paragraph("Chapitre 8 — Architecture du code source", ST_CHAPTER))

    story.append(Paragraph("8.1 Structure d'un service FastAPI", ST_H1))
    story.append(code_block(
        "services/academic-service/\n"
        "├── app/\n"
        "│   ├── main.py              <-- Point d'entree, lifespan, CORS\n"
        "│   ├── core/\n"
        "│   │   └── config.py        <-- Pydantic Settings depuis .env\n"
        "│   ├── db/\n"
        "│   │   └── session.py       <-- Engine async, sessionmaker\n"
        "│   ├── models/\n"
        "│   │   └── entities.py      <-- ORM SQLAlchemy 2.0\n"
        "│   ├── schemas/\n"
        "│   │   └── academic.py      <-- Validation Pydantic v2\n"
        "│   └── routers/             <-- 8 modules de routes\n"
        "├── .env                     <-- Configuration secrete\n"
        "├── .env.example             <-- Template\n"
        "└── requirements.txt"
    ))

    story.append(Paragraph("8.2 Structure du frontend Angular", ST_H1))
    story.append(code_block(
        "frontend/src/app/\n"
        "├── app.component.ts          <-- Racine de l'application\n"
        "├── app.routes.ts             <-- Definition des routes (lazy)\n"
        "├── layout/\n"
        "│   ├── app-shell.component.ts   <-- Sidebar + topbar + outlet\n"
        "│   └── app-shell.component.css\n"
        "├── core/\n"
        "│   └── theme.service.ts      <-- Mode sombre/clair\n"
        "├── services/\n"
        "│   ├── chat.service.ts       <-- Client HTTP chatbot-service\n"
        "│   └── academic.service.ts   <-- Client HTTP academic-service\n"
        "├── features/                 <-- Pages lazy-loaded\n"
        "│   ├── dashboard/\n"
        "│   ├── chat/\n"
        "│   ├── departments/\n"
        "│   ├── filieres/\n"
        "│   ├── modules/\n"
        "│   ├── professors/\n"
        "│   ├── news/\n"
        "│   └── student-life/\n"
        "├── components/               <-- Atomiques reutilisables\n"
        "└── models/"
    ))

    story.append(Paragraph("8.3 Bonnes pratiques de développement", ST_H1))
    practices = [
        "Toujours créer un nouveau .env à partir de .env.example, jamais commiter .env.",
        "Utiliser Pydantic v2 pour valider tous les inputs (déjà fait dans le code livré).",
        "Pour ajouter un nouveau intent au chatbot : éditer services/chatbot-service/data/faq_dataset.json, "
        "puis supprimer model.pkl pour forcer le réentraînement.",
        "Pour ajouter une nouvelle route Angular : créer le composant standalone dans features/, "
        "ajouter une entrée dans app.routes.ts avec loadComponent.",
        "Pour ajouter une table MySQL : modifier 01_schema.sql + ajouter le modèle ORM dans "
        "models/entities.py + le schéma Pydantic + le router.",
        "Toujours tester localement avant de pousser du code.",
    ]
    for p in practices:
        story.append(Paragraph(f"• {p}", ST_LIST))
    story.append(PageBreak())

    # ════════════════ ANNEXES ════════════════
    story.append(Paragraph("Annexes", ST_CHAPTER))

    story.append(Paragraph("Annexe A — Liste des fichiers livrés", ST_H1))
    story.append(code_block(
        "chatbot-fsbm-platform/                       (racine)\n"
        "├── SETUP.bat                                Setup one-click\n"
        "├── README.md                                README principal\n"
        "├── docs/\n"
        "│   ├── ARCHITECTURE.md                      Architecture detaillee\n"
        "│   └── pdf/\n"
        "│       ├── FSBM_Platform_Rapport_PFE.pdf    PDF 1 : Rapport\n"
        "│       ├── FSBM_Platform_Guide_Technique.pdf PDF 2 : Ce guide\n"
        "│       ├── generate_report.py               Script generateur PDF 1\n"
        "│       └── generate_guide.py                Script generateur PDF 2\n"
        "├── database/\n"
        "│   ├── mysql/\n"
        "│   │   ├── 01_schema.sql                    (18 KB)\n"
        "│   │   ├── 02_seed_static.sql               (19 KB)\n"
        "│   │   ├── 03_seed_modules.sql              (15 KB)\n"
        "│   │   └── 04_seed_data.sql                 (~720 KB, genere)\n"
        "│   ├── mongodb/init.js                       (13 KB)\n"
        "│   └── seed/generate_data.py                 (Python generator)\n"
        "├── services/\n"
        "│   ├── chatbot-service/  (FastAPI :5001)\n"
        "│   └── academic-service/ (FastAPI :5002)\n"
        "├── frontend/                                 (Angular 17)\n"
        "└── scripts/\n"
        "    ├── install-all.bat\n"
        "    ├── start-all.bat\n"
        "    ├── init-database.bat\n"
        "    └── configure-env.bat"
    ))

    story.append(Paragraph("Annexe B — Commandes utiles", ST_H1))
    cmds = [
        ("Réentraîner le NLP",
         "del services\\chatbot-service\\data\\model.pkl\nRedémarrer le chatbot-service"),
        ("Régénérer les données seed",
         "cd database\\seed\nset PYTHONIOENCODING=utf-8\npy generate_data.py"),
        ("Builder le frontend pour production",
         "cd frontend\nnpm run build:prod"),
        ("Vider la BDD",
         "DROP DATABASE fsbm_db;"),
        ("Vérifier les tables",
         "SELECT TABLE_NAME, TABLE_ROWS FROM information_schema.TABLES WHERE TABLE_SCHEMA='fsbm_db';"),
        ("Tester le chatbot via curl",
         "curl -X POST http://localhost:5001/api/chat \\\n  -H \"Content-Type: application/json\" \\\n  -d \"{\\\"message\\\":\\\"Quelles sont les filieres ?\\\"}\""),
    ]
    for label, cmd in cmds:
        story.append(Paragraph(f"<b>{label}</b>", ST_H3))
        story.append(code_block(cmd))

    story.append(Paragraph("Annexe C — Crédits & contact", ST_H1))
    story.append(Paragraph(
        "Cette plateforme a été développée dans le cadre du Projet de Fin d'Études de la "
        "Licence en Développement Informatique à la Faculté des Sciences Ben M'Sick "
        "(Université Hassan II de Casablanca), année universitaire 2025/2026.",
        ST_BODY
    ))
    story.append(Paragraph("<b>Équipe :</b>", ST_BODY))
    for member in [
        "AKRAM BELMOUSSA — Architecte Backend & NLP",
        "ZAKARIA — Frontend Angular & UX/UI",
        "NOUHAILA — Base de données & Contenu FAQ",
    ]:
        story.append(Paragraph(f"• {member}", ST_LIST))

    story.append(Spacer(1, 0.5*cm))
    story.append(alert_box(
        "Pour toute question ou amélioration, contacte l'équipe ou consulte la documentation "
        "complète dans <b>docs/ARCHITECTURE.md</b>.",
        "success"
    ))

    # Build
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF généré : {out_path}")
    print(f"Taille : {out_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    build()
