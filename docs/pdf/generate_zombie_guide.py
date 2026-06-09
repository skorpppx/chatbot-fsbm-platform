"""
============================================================================
 FSBM Platform — Générateur PDF : Guide de dépannage Crash & Zombies de ports
============================================================================
Guide visuel pour diagnostiquer et résoudre les blocages de ports Windows
(WinError 10013, processus zombies, WSL2 leaks, Hyper-V port reservations).
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

# Couleurs
PRIMARY     = HexColor('#1C3F6E')
PRIMARY_MID = HexColor('#265DAB')
ACCENT      = HexColor('#16B5A6')
ACCENT_PALE = HexColor('#E5F8F5')
GREY_DARK   = HexColor('#2D3748')
GREY_MID    = HexColor('#4A5568')
GREY_LIGHT  = HexColor('#EDF1F6')
SUCCESS     = HexColor('#22C55E')
SUCCESS_PALE= HexColor('#F0FDF4')
WARNING     = HexColor('#F59E0B')
WARNING_PALE= HexColor('#FFFBEB')
DANGER      = HexColor('#EF4444')
DANGER_PALE = HexColor('#FEF2F2')
INFO        = HexColor('#3B82F6')
INFO_PALE   = HexColor('#EBF5FF')

ROOT = Path(__file__).parent.parent.parent
LOGO_FSBM = ROOT / "frontend" / "src" / "assets" / "logos" / "fsbm.png"

styles = getSampleStyleSheet()
ST_TITLE = ParagraphStyle('TitleX', parent=styles['Title'], fontName='Helvetica-Bold',
    fontSize=26, textColor=PRIMARY, alignment=TA_CENTER, spaceAfter=12, leading=32)
ST_SUBTITLE = ParagraphStyle('Subtitle', parent=styles['Heading2'], fontName='Helvetica',
    fontSize=15, textColor=GREY_DARK, alignment=TA_CENTER, spaceAfter=10, leading=20)
ST_CHAPTER = ParagraphStyle('Chapter', parent=styles['Heading1'], fontName='Helvetica-Bold',
    fontSize=22, textColor=PRIMARY, alignment=TA_LEFT, spaceBefore=18, spaceAfter=12, leading=28)
ST_H1 = ParagraphStyle('H1', parent=styles['Heading1'], fontName='Helvetica-Bold',
    fontSize=16, textColor=PRIMARY, spaceBefore=14, spaceAfter=9, leading=20)
ST_H2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName='Helvetica-Bold',
    fontSize=13, textColor=PRIMARY_MID, spaceBefore=12, spaceAfter=7, leading=17)
ST_H3 = ParagraphStyle('H3', parent=styles['Heading3'], fontName='Helvetica-Bold',
    fontSize=11.5, textColor=GREY_DARK, spaceBefore=10, spaceAfter=5, leading=15)
ST_BODY = ParagraphStyle('Body', parent=styles['BodyText'], fontName='Helvetica',
    fontSize=10.5, textColor=GREY_DARK, alignment=TA_JUSTIFY, spaceAfter=8, leading=15)
ST_BODY_BOLD = ParagraphStyle('BodyBold', parent=ST_BODY, fontName='Helvetica-Bold')
ST_CODE = ParagraphStyle('Code', parent=styles['Code'], fontName='Courier',
    fontSize=9, textColor=PRIMARY_MID, backColor=GREY_LIGHT,
    leftIndent=12, rightIndent=12, spaceAfter=8, leading=13, borderPadding=10,
    borderColor=PRIMARY_MID, borderWidth=0.5)
ST_LIST = ParagraphStyle('List', parent=ST_BODY, leftIndent=14, bulletIndent=4)
ST_STEP_TITLE = ParagraphStyle('Step', parent=ST_BODY, fontName='Helvetica-Bold',
    fontSize=12, textColor=ACCENT, spaceBefore=12, spaceAfter=6, leading=16)


def header_footer(c, doc):
    c.saveState()
    c.setStrokeColor(GREY_LIGHT); c.setLineWidth(0.5)
    c.line(2*cm, 1.5*cm, A4[0]-2*cm, 1.5*cm)
    c.setFont('Helvetica', 8); c.setFillColor(GREY_MID)
    c.drawString(2*cm, 1*cm, "FSBM Platform — Guide Crash & Zombies de ports")
    c.drawCentredString(A4[0]/2, 1*cm, "2026")
    c.drawRightString(A4[0]-2*cm, 1*cm, f"Page {doc.page}")
    if doc.page > 1:
        c.setFont('Helvetica', 8); c.setFillColor(PRIMARY)
        c.drawString(2*cm, A4[1]-1*cm, "Guide Crash & Zombies — Windows")
        c.line(2*cm, A4[1]-1.2*cm, A4[0]-2*cm, A4[1]-1.2*cm)
    c.restoreState()


def code_block(text: str):
    return Paragraph(text.replace('\n', '<br/>').replace(' ', '&nbsp;'), ST_CODE)


def alert_box(content: str, kind: str = "info", title: str = None):
    colors = {
        "info":    (INFO,     INFO_PALE,    "i"),
        "warning": (WARNING,  WARNING_PALE, "!"),
        "success": (SUCCESS,  SUCCESS_PALE, "OK"),
        "danger":  (DANGER,   DANGER_PALE,  "X"),
    }
    border, bg, icon = colors.get(kind, colors["info"])
    icon_color = border.hexval()
    if title:
        text_html = f'<font color="{icon_color}"><b>[{icon}] {title}</b></font><br/>{content}'
    else:
        text_html = f'<font color="{icon_color}"><b>[{icon}]</b></font> {content}'
    t = Table([[Paragraph(text_html, ST_BODY)]], colWidths=[16*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('LINEBEFORE', (0,0), (-1,-1), 4, border),
        ('PADDING',    (0,0), (-1,-1), 10),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t


def diagnostic_table(rows):
    """Tableau symptôme → cause → solution."""
    data = [[Paragraph(f'<b>{h}</b>', ST_BODY_BOLD) for h in ['Symptôme', 'Cause probable', 'Solution']]] + \
           [[Paragraph(c, ST_BODY) for c in r] for r in rows]
    t = Table(data, colWidths=[5*cm, 5*cm, 6*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR',  (0,0), (-1,0), white),
        ('BOX',        (0,0), (-1,-1), 0.5, GREY_LIGHT),
        ('INNERGRID',  (0,0), (-1,-1), 0.3, GREY_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, GREY_LIGHT]),
        ('PADDING',    (0,0), (-1,-1), 6),
        ('VALIGN',     (0,0), (-1,-1), 'TOP'),
    ]))
    return t


def build():
    out_path = Path(__file__).parent / "FSBM_Platform_Guide_Zombies.pdf"
    doc = SimpleDocTemplate(
        str(out_path), pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="Guide Crash & Zombies - FSBM Platform",
        author="AKRAM BELMOUSSA, ZAKARIA, NOUHAILA",
    )
    story = []

    # ════════════════ COUVERTURE ════════════════
    story.append(Spacer(1, 2*cm))
    if LOGO_FSBM.exists():
        story.append(Image(str(LOGO_FSBM), width=4.5*cm, height=4.5*cm, hAlign='CENTER'))
    story.append(Spacer(1, 0.8*cm))
    story.append(Paragraph("FSBM PLATFORM", ST_TITLE))
    story.append(Paragraph("Guide de dépannage", ST_SUBTITLE))
    story.append(Paragraph("Crash & Processus zombies sur les ports", ST_SUBTITLE))
    story.append(Spacer(1, 0.3*cm))
    t = Table([
        [Paragraph('<font color="#FFFFFF"><b>Manuel pratique de diagnostic Windows</b></font>', ST_BODY)],
    ], colWidths=[14*cm], hAlign='CENTER')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DANGER),
        ('PADDING',    (0,0), (-1,-1), 12),
        ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t)
    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph(
        "Ce guide vous aide à résoudre tous les cas de blocage de ports rencontrés "
        "lors du développement de la plateforme FSBM sous Windows. "
        "Inclut diagnostic, solutions rapides et fix définitif.",
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
        ("Chapitre 1 — Identifier un processus zombie", "3"),
        ("    1.1  Symptômes typiques", "3"),
        ("    1.2  Tableau de diagnostic rapide", "4"),
        ("    1.3  Commandes de détection", "5"),
        ("Chapitre 2 — Pourquoi ça arrive ?", "6"),
        ("    2.1  WSL2 et les proxies de port", "6"),
        ("    2.2  Hyper-V et la plage dynamique", "7"),
        ("    2.3  TIME_WAIT et sockets bloqués", "8"),
        ("Chapitre 3 — Solution RAPIDE", "9"),
        ("    3.1  Le script clean-zombies.ps1", "9"),
        ("    3.2  Méthodes manuelles", "10"),
        ("Chapitre 4 — Solution PERMANENTE", "12"),
        ("    4.1  Lancer fix-windows-ports.ps1 (admin)", "12"),
        ("    4.2  Vérification", "13"),
        ("    4.3  Bonnes pratiques", "14"),
        ("Chapitre 5 — Cas particuliers", "15"),
        ("    5.1  WinError 10013", "15"),
        ("    5.2  Port reste en LISTEN après pkill", "16"),
        ("    5.3  Plusieurs services qui se battent", "17"),
        ("Annexes", "18"),
        ("    A — Scripts complets", "18"),
        ("    B — Glossaire technique", "20"),
        ("    C — Commandes de référence", "21"),
    ]
    for label, page in toc:
        dots = '.' * (max(1, 78 - len(label) - len(page)))
        story.append(Paragraph(
            f"{label} <font color='#8095A8'>{dots}</font> <b>{page}</b>",
            ParagraphStyle('TOC', parent=ST_BODY, fontSize=11, spaceAfter=4, leading=16)))
    story.append(PageBreak())

    # ════════════════ CHAPITRE 1 ════════════════
    story.append(Paragraph("Chapitre 1 — Identifier un processus zombie", ST_CHAPTER))

    story.append(Paragraph("1.1 Symptômes typiques", ST_H1))
    story.append(Paragraph(
        "Un <b>processus zombie</b> dans le contexte des ports réseau désigne un état "
        "dans lequel un port est occupé par un processus qui semble mort ou inaccessible. "
        "Voici les signes qui doivent vous alerter :",
        ST_BODY
    ))
    symptoms = [
        "Le serveur (uvicorn, npm, etc.) refuse de démarrer avec un message d'erreur lié à un port.",
        "<b>WinError 10013</b> : « Une tentative d'accès à un socket de manière interdite par ses autorisations d'accès a été tentée. »",
        "<b>WinError 10048</b> : « Une seule utilisation de chaque adresse de socket est autorisée. »",
        "Message <i>« Address already in use »</i> alors que vous venez de fermer le terminal.",
        "<code>taskkill /F /PID xxx</code> répond <i>« processus introuvable »</i> alors que <code>netstat</code> montre que le PID écoute.",
        "Le navigateur charge encore l'ancienne version de l'application alors que vous l'avez modifiée.",
        "Le port reste en état <code>LISTEN</code> alors qu'aucun processus visible ne devrait l'utiliser.",
    ]
    for s in symptoms:
        story.append(Paragraph(f"• {s}", ST_LIST))

    story.append(alert_box(
        "Si vous voyez un de ces symptômes, vous êtes face à un <b>processus zombie</b> "
        "ou à une <b>réservation de port</b> par Windows. Lisez la suite pour comprendre et résoudre.",
        kind="warning", title="Diagnostic immédiat"
    ))

    story.append(Paragraph("1.2 Tableau de diagnostic rapide", ST_H1))
    story.append(diagnostic_table([
        ["WinError 10013",
         "Port réservé par Hyper-V ou Windows (plage dynamique)",
         "Lancer fix-windows-ports.ps1 en admin pour réserver le port"],
        ["WinError 10048",
         "Un autre processus écoute déjà sur le port",
         "Identifier et tuer le processus avec clean-zombies.ps1"],
        ["taskkill : processus introuvable",
         "Le proxy de port WSL/Hyper-V persiste sans processus visible",
         "wsl --shutdown + Restart-Service hns"],
        ["Port en TIME_WAIT",
         "Socket fermé récemment, attente du timeout réseau (4 min)",
         "Attendre ou changer de port"],
        ["Plusieurs PID sur le même port",
         "Plusieurs instances ont été lancées (npm start dupliqué)",
         "Kill tous les python.exe / node.exe liés"],
        ["Le port se libère puis se reprend",
         "Auto-reload Angular/Vite réutilise le PID",
         "Couper Ctrl+C dans la fenêtre d'origine"],
    ]))

    story.append(Paragraph("1.3 Commandes de détection", ST_H1))
    story.append(Paragraph(
        "Avant toute action, identifiez précisément l'état du port avec ces commandes :",
        ST_BODY
    ))

    story.append(Paragraph("Voir qui utilise un port précis (ex. 5002)", ST_H3))
    story.append(code_block(
        "# PowerShell natif (recommandé)\n"
        "Get-NetTCPConnection -LocalPort 5002 | Format-List\n"
        "\n"
        "# CMD classique\n"
        "netstat -ano | findstr :5002\n"
        "\n"
        "# Identifier le processus à partir du PID\n"
        "Get-Process -Id 17968"
    ))

    story.append(Paragraph("Lister tous les ports écoutés", ST_H3))
    story.append(code_block(
        "Get-NetTCPConnection -State Listen |\n"
        "    Where-Object { $_.LocalAddress -in @('127.0.0.1', '::1', '0.0.0.0') } |\n"
        "    Select-Object LocalPort, OwningProcess,\n"
        "        @{N='Process';E={(Get-Process -Id $_.OwningProcess -EA SilentlyContinue).ProcessName}} |\n"
        "    Sort-Object LocalPort"
    ))

    story.append(Paragraph("Voir les plages réservées par Hyper-V", ST_H3))
    story.append(code_block(
        "netsh int ipv4 show excludedportrange protocol=tcp\n"
        "\n"
        "# Exemple de sortie :\n"
        "#    5357        5357\n"
        "#   50000       50059   *\n"
        "#       * = exclusion administrative"
    ))
    story.append(PageBreak())

    # ════════════════ CHAPITRE 2 ════════════════
    story.append(Paragraph("Chapitre 2 — Pourquoi ça arrive ?", ST_CHAPTER))

    story.append(Paragraph("2.1 WSL2 et les proxies de port", ST_H1))
    story.append(Paragraph(
        "WSL2 (Windows Subsystem for Linux v2) tourne dans une <b>machine virtuelle légère</b> "
        "isolée du système hôte. Pour que les serveurs lancés dans WSL soient accessibles "
        "depuis Windows (sur localhost), Windows installe automatiquement un <b>proxy de port</b> "
        "qui redirige les connexions du host vers la VM.",
        ST_BODY
    ))
    story.append(Paragraph(
        "<b>Le problème :</b> Ce proxy peut survivre à la mort du processus WSL qui l'avait créé. "
        "Résultat : Windows voit qu'un PID écoute sur le port, mais le processus n'existe plus "
        "dans WSL — donc <code>taskkill</code> ne peut rien faire.",
        ST_BODY
    ))
    story.append(alert_box(
        "<b>C'est exactement ce qui s'est passé pendant le développement de FSBM Platform.</b> "
        "Les tests automatisés lancés depuis Bash (WSL) ont créé des proxies persistants sur "
        "les ports 5001 et 5002, qui sont restés actifs jusqu'à redémarrage du service réseau.",
        kind="info"
    ))
    story.append(Paragraph(
        "<b>Comment libérer un proxy WSL :</b>",
        ST_BODY
    ))
    story.append(code_block(
        "# Tuer toutes les instances WSL et libérer les proxies\n"
        "wsl --shutdown\n"
        "\n"
        "# Restart du service réseau Windows (admin recommandé)\n"
        "Restart-Service hns -Force\n"
        "\n"
        "# Si même hns ne suffit pas (cas extrême)\n"
        "Stop-Service vmcompute -Force\n"
        "Start-Service vmcompute"
    ))

    story.append(Paragraph("2.2 Hyper-V et la plage dynamique", ST_H1))
    story.append(Paragraph(
        "Windows réserve une plage de ports pour ses besoins internes et pour Hyper-V "
        "(virtualisation). Cette plage, appelée <b>plage dynamique</b>, peut grimper haut "
        "et inclure des ports « normalement libres » comme 5000-5100.",
        ST_BODY
    ))
    story.append(Paragraph(
        "Quand vous essayez d'écouter sur un port qui tombe dans cette plage réservée, "
        "Windows refuse avec <b>WinError 10013</b>.",
        ST_BODY
    ))
    story.append(Paragraph(
        "<b>La solution :</b> ajouter une <i>exclusion de port</i> qui force Windows à "
        "<b>ne jamais</b> allouer dynamiquement ce port. Le port devient ainsi réservé "
        "exclusivement pour vous.",
        ST_BODY
    ))
    story.append(code_block(
        "# (admin requis)\n"
        "netsh int ipv4 add excludedportrange protocol=tcp startport=5002 numberofports=1\n"
        "\n"
        "# Vérifier l'exclusion\n"
        "netsh int ipv4 show excludedportrange protocol=tcp"
    ))

    story.append(Paragraph("2.3 TIME_WAIT et sockets bloqués", ST_H1))
    story.append(Paragraph(
        "Lorsqu'un serveur ferme une connexion TCP, le socket reste en état <code>TIME_WAIT</code> "
        "pendant <b>2 à 4 minutes</b> (selon la config). Cela permet au système d'éviter de "
        "réutiliser le même port pour une connexion radicalement différente.",
        ST_BODY
    ))
    story.append(Paragraph(
        "Si vous relancez immédiatement un serveur sur le même port, il peut échouer avec "
        "<b>« Address already in use »</b>. Solutions :",
        ST_BODY
    ))
    bullet_solutions = [
        "<b>Attendre 4 minutes</b> et réessayer (le TIME_WAIT se libère naturellement).",
        "<b>Changer de port</b> temporairement (ex. 8002 au lieu de 5002).",
        "<b>Activer SO_REUSEADDR</b> sur le serveur (déjà actif par défaut dans uvicorn).",
        "<b>Vérifier l'état</b> du socket avec <code>Get-NetTCPConnection</code> — si l'état est TIME_WAIT, c'est normal.",
    ]
    for b in bullet_solutions:
        story.append(Paragraph(f"• {b}", ST_LIST))
    story.append(PageBreak())

    # ════════════════ CHAPITRE 3 ════════════════
    story.append(Paragraph("Chapitre 3 — Solution RAPIDE", ST_CHAPTER))

    story.append(Paragraph("3.1 Le script clean-zombies.ps1", ST_H1))
    story.append(Paragraph(
        "Le script <code>scripts\\clean-zombies.ps1</code> automatise les <b>5 méthodes</b> "
        "de nettoyage en cascade. Il fonctionne <b>sans privilèges administrateur</b> dans "
        "la plupart des cas.",
        ST_BODY
    ))
    story.append(Paragraph("Lancement", ST_H3))
    story.append(code_block(
        "cd C:\\Users\\belmo\\studies\\PFE\\chatbot-fsbm-platform\n"
        "powershell -ExecutionPolicy Bypass -File .\\scripts\\clean-zombies.ps1"
    ))
    story.append(Paragraph("Ce que fait le script", ST_H3))
    methods = [
        ("Étape 1 — Stop-Process",
         "Tentative de tuer chaque PID identifié comme occupant un port FSBM "
         "via <code>Stop-Process -Force</code>."),
        ("Étape 2 — taskkill /F /T",
         "Plus brutal : force-kill du processus ET de tout son arbre de processus enfants "
         "(utile si npm a démarré plusieurs node)."),
        ("Étape 3 — Recherche par CommandLine",
         "Liste TOUS les python.exe / node.exe du système et tue ceux dont la ligne de commande "
         "contient « uvicorn », « chatbot-fsbm » ou « ng serve »."),
        ("Étape 4 — wsl --shutdown",
         "Libère les proxies de port créés par WSL (la cause #1 des zombies persistants)."),
        ("Étape 5 — Restart hns",
         "Redémarre le Host Network Service de Windows, qui gère les ports proxy. "
         "Nécessite l'admin pour fonctionner pleinement."),
    ]
    for title, desc in methods:
        story.append(Paragraph(f"<b>{title}.</b> {desc}", ST_LIST))

    story.append(alert_box(
        "Le script <b>réussit dans 90% des cas</b> sans admin. Pour les cas extrêmes "
        "(blocage Hyper-V), passez au Chapitre 4.",
        kind="success"
    ))

    story.append(Paragraph("3.2 Méthodes manuelles", ST_H1))
    story.append(Paragraph(
        "Si vous préférez agir manuellement (debugging, apprentissage), voici les commandes "
        "à exécuter dans l'ordre :",
        ST_BODY
    ))

    story.append(Paragraph("Étape A — Identifier le coupable", ST_STEP_TITLE))
    story.append(code_block(
        "# Lister tous les PID sur les ports FSBM\n"
        "@(5001, 5002, 4200, 8001, 8002) | ForEach-Object {\n"
        "    $c = Get-NetTCPConnection -LocalPort $_ -EA SilentlyContinue\n"
        "    if ($c) { Write-Host \"Port $_ -> PID $($c.OwningProcess)\" }\n"
        "}"
    ))

    story.append(Paragraph("Étape B — Tuer en force", ST_STEP_TITLE))
    story.append(code_block(
        "# Pour chaque PID identifié\n"
        "taskkill /F /T /PID 17968\n"
        "\n"
        "# Si le PID n'existe plus mais le port reste occupé\n"
        "wsl --shutdown\n"
        "Restart-Service hns -Force   # admin requis"
    ))

    story.append(Paragraph("Étape C — Vérification", ST_STEP_TITLE))
    story.append(code_block(
        "Get-NetTCPConnection -LocalPort 5002 -EA SilentlyContinue\n"
        "# Aucune sortie = port libre, vous pouvez relancer"
    ))

    story.append(alert_box(
        "Si après toutes ces étapes le port reste bloqué, c'est probablement une <b>"
        "exclusion Hyper-V</b>. Passez à la solution permanente du Chapitre 4.",
        kind="warning"
    ))
    story.append(PageBreak())

    # ════════════════ CHAPITRE 4 ════════════════
    story.append(Paragraph("Chapitre 4 — Solution PERMANENTE", ST_CHAPTER))

    story.append(Paragraph("4.1 Lancer fix-windows-ports.ps1 (admin)", ST_H1))
    story.append(Paragraph(
        "Cette solution est <b>définitive</b> : une fois appliquée, les ports FSBM sont "
        "réservés à votre usage exclusif. Aucun service Windows ne pourra plus les voler "
        "accidentellement.",
        ST_BODY
    ))
    story.append(alert_box(
        "Ce script <b>nécessite les droits administrateur</b> car il modifie la configuration "
        "réseau du système.",
        kind="warning", title="Prérequis"
    ))

    story.append(Paragraph("Étape 1 — Ouvrir PowerShell en administrateur", ST_STEP_TITLE))
    story.append(Paragraph(
        "Plusieurs méthodes :",
        ST_BODY
    ))
    admin_methods = [
        "Touche <b>Windows</b> → tape « PowerShell » → clic droit → « Exécuter en tant qu'administrateur »",
        "Touche <b>Windows + X</b> → « Terminal Windows (admin) »",
        "Dans l'Explorateur de fichiers, <b>Shift + clic droit</b> dans un dossier vide → « Ouvrir dans Terminal »",
    ]
    for m in admin_methods:
        story.append(Paragraph(f"• {m}", ST_LIST))

    story.append(Paragraph("Étape 2 — Lancer le script", ST_STEP_TITLE))
    story.append(code_block(
        "cd C:\\Users\\belmo\\studies\\PFE\\chatbot-fsbm-platform\n"
        "powershell -ExecutionPolicy Bypass -File .\\scripts\\fix-windows-ports.ps1"
    ))

    story.append(Paragraph("Étape 3 — Ce que fait le script", ST_STEP_TITLE))
    steps = [
        ("1. Vérification admin",
         "Refuse de continuer s'il n'est pas en admin (sécurité)."),
        ("2. Liste des plages réservées",
         "Affiche les exclusions Hyper-V actuelles via <code>netsh</code>."),
        ("3. Kill des processus actuels",
         "<code>taskkill /F /T</code> sur tous les PID sur les ports FSBM."),
        ("4. Arrêt des services réseau",
         "Stop <code>WinNat</code>, <code>hns</code>, <code>vmcompute</code> pour libérer "
         "les locks au niveau Windows."),
        ("5. Ajout des exclusions",
         "<code>netsh int ipv4 add excludedportrange</code> pour 5001, 5002, 8001, 8002, 4200."),
        ("6. Redémarrage des services",
         "Restart de WinNat, hns, vmcompute."),
        ("7. WSL shutdown",
         "Libère les proxies WSL résiduels."),
        ("8. Vérification finale",
         "Confirme que tous les ports sont libres."),
    ]
    for t, d in steps:
        story.append(Paragraph(f"<b>{t}</b> — {d}", ST_LIST))

    story.append(Paragraph("4.2 Vérification", ST_H1))
    story.append(Paragraph(
        "Après le script, vous devriez voir les ports FSBM listés dans les exclusions :",
        ST_BODY
    ))
    story.append(code_block(
        "netsh int ipv4 show excludedportrange protocol=tcp\n"
        "\n"
        "# Sortie attendue :\n"
        "#  Port de début   Port de fin\n"
        "#  ──────────────  ───────────\n"
        "#       4200         4200    *\n"
        "#       5001         5001    *\n"
        "#       5002         5002    *\n"
        "#       8001         8001    *\n"
        "#       8002         8002    *\n"
        "#       (* = exclusion administrative)"
    ))
    story.append(alert_box(
        "Une fois ces exclusions en place, ces ports sont <b>garantis libres</b> au démarrage "
        "de vos services. Hyper-V, Docker, WSL ne pourront plus jamais les voler.",
        kind="success"
    ))

    story.append(Paragraph("4.3 Bonnes pratiques pour ne plus jamais avoir le problème", ST_H1))
    practices = [
        ("Lancer les serveurs depuis Windows natif",
         "Préférez cmd.exe ou PowerShell Windows. Évitez WSL/bash pour les serveurs persistants."),
        ("Arrêter proprement",
         "Utilisez toujours <code>Ctrl+C</code> dans la fenêtre où le serveur tourne. "
         "Ne fermez pas brutalement la fenêtre."),
        ("Utiliser des ports élevés",
         "Pour des tests rapides, préférez 8001-8999 (moins de conflits avec Hyper-V)."),
        ("Vérifier avant de lancer",
         "Lancez <code>clean-zombies.ps1</code> si vous avez des doutes."),
        ("Nettoyage régulier",
         "Une fois par semaine, lancez <code>wsl --shutdown</code> si vous utilisez WSL."),
        ("Réservez vos ports",
         "<code>fix-windows-ports.ps1</code> est à faire <b>une fois</b> au début du projet. "
         "Ensuite, tout fonctionne."),
    ]
    for t, d in practices:
        story.append(Paragraph(f"<b>{t}</b> — {d}", ST_LIST))
    story.append(PageBreak())

    # ════════════════ CHAPITRE 5 ════════════════
    story.append(Paragraph("Chapitre 5 — Cas particuliers", ST_CHAPTER))

    story.append(Paragraph("5.1 WinError 10013", ST_H1))
    story.append(alert_box(
        "<b>WinError 10013 :</b> Une tentative d'accès à un socket de manière interdite "
        "par ses autorisations d'accès a été tentée.",
        kind="danger"
    ))
    story.append(Paragraph(
        "<b>Cause :</b> Le port que vous essayez d'écouter est <i>réservé</i> par "
        "Hyper-V / WSL / un service Windows. Windows refuse de vous le donner.",
        ST_BODY
    ))
    story.append(Paragraph(
        "<b>Solution :</b>",
        ST_BODY_BOLD
    ))
    story.append(code_block(
        "# Vérifier si le port est réservé\n"
        "netsh int ipv4 show excludedportrange protocol=tcp | findstr 5002\n"
        "\n"
        "# Si oui, lancer le fix permanent en admin\n"
        ".\\scripts\\fix-windows-ports.ps1\n"
        "\n"
        "# Solution alternative : utiliser un autre port\n"
        "py -m uvicorn app.main:app --port 8002"
    ))

    story.append(Paragraph("5.2 Port reste en LISTEN après pkill", ST_H1))
    story.append(alert_box(
        "<b>Symptôme :</b> Vous avez tué le processus, mais <code>Get-NetTCPConnection -LocalPort X</code> "
        "montre toujours un PID en état LISTEN — qui n'existe plus.",
        kind="warning"
    ))
    story.append(Paragraph(
        "<b>Cause :</b> Le PID était un proxy WSL, pas un vrai processus Windows. "
        "Windows ne peut pas le libérer sans intervention.",
        ST_BODY
    ))
    story.append(Paragraph(
        "<b>Solution :</b>",
        ST_BODY_BOLD
    ))
    story.append(code_block(
        "wsl --shutdown\n"
        "Start-Sleep 3\n"
        "Restart-Service hns -Force   # admin requis\n"
        "Start-Sleep 5\n"
        "Get-NetTCPConnection -LocalPort 5002   # devrait être vide"
    ))

    story.append(Paragraph("5.3 Plusieurs services qui se battent", ST_H1))
    story.append(alert_box(
        "<b>Symptôme :</b> Vous voyez plusieurs PID python.exe sur le même port, "
        "le serveur démarre puis se ferme tout seul.",
        kind="warning"
    ))
    story.append(Paragraph(
        "<b>Cause :</b> Vous avez lancé plusieurs instances de uvicorn par erreur (par exemple "
        "en cliquant deux fois sur SETUP.bat).",
        ST_BODY
    ))
    story.append(Paragraph(
        "<b>Solution :</b>",
        ST_BODY_BOLD
    ))
    story.append(code_block(
        "# Tuer TOUS les python.exe lies a uvicorn\n"
        "Get-Process python -EA SilentlyContinue | ForEach-Object {\n"
        "    $cmd = (Get-CimInstance Win32_Process -Filter \"ProcessId=$($_.Id)\").CommandLine\n"
        "    if ($cmd -match 'uvicorn') {\n"
        "        Write-Host \"Killing PID $($_.Id)\"\n"
        "        Stop-Process -Id $_.Id -Force\n"
        "    }\n"
        "}\n"
        "\n"
        "# Relancer une seule instance\n"
        "py -m uvicorn app.main:app --port 5002"
    ))
    story.append(PageBreak())

    # ════════════════ ANNEXES ════════════════
    story.append(Paragraph("Annexes", ST_CHAPTER))

    story.append(Paragraph("Annexe A — Scripts complets fournis", ST_H1))
    story.append(Paragraph(
        "Trois scripts sont fournis dans <code>chatbot-fsbm-platform/scripts/</code> :",
        ST_BODY
    ))
    scripts_table = Table([
        [Paragraph('<b>Script</b>', ST_BODY_BOLD), Paragraph('<b>Rôle</b>', ST_BODY_BOLD), Paragraph('<b>Admin ?</b>', ST_BODY_BOLD)],
        [Paragraph('<code>clean-zombies.ps1</code>', ST_BODY),
         Paragraph('Nettoyage rapide en 5 étapes (Stop-Process → taskkill → CommandLine → WSL → hns).', ST_BODY),
         Paragraph('Non', ST_BODY)],
        [Paragraph('<code>fix-windows-ports.ps1</code>', ST_BODY),
         Paragraph('Fix DEFINITIF : réserve les ports FSBM via netsh exclusion. À faire UNE FOIS.', ST_BODY),
         Paragraph('OUI', ST_BODY)],
        [Paragraph('<code>start.ps1</code>', ST_BODY),
         Paragraph('Lance les 3 services (academic, chatbot, frontend) dans 3 fenêtres séparées.', ST_BODY),
         Paragraph('Non', ST_BODY)],
    ], colWidths=[5*cm, 9*cm, 2*cm])
    scripts_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR',  (0,0), (-1,0), white),
        ('BOX',        (0,0), (-1,-1), 0.5, GREY_LIGHT),
        ('INNERGRID',  (0,0), (-1,-1), 0.3, GREY_LIGHT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, GREY_LIGHT]),
        ('PADDING',    (0,0), (-1,-1), 6),
        ('VALIGN',     (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(scripts_table)

    story.append(Paragraph("Annexe B — Glossaire technique", ST_H1))
    glossary = [
        ("Zombie",
         "Processus apparemment mort mais dont le socket est toujours alloué côté kernel."),
        ("Port",
         "Numéro entre 1 et 65535 identifiant une application qui écoute sur le réseau."),
        ("LISTEN",
         "État d'un socket qui attend une connexion entrante."),
        ("TIME_WAIT",
         "État transitoire d'un socket fermé, dure 2-4 min, empêche la réutilisation immédiate."),
        ("Hyper-V",
         "Hyperviseur de Microsoft, utilisé par Docker Desktop, WSL2, sandbox Windows."),
        ("WSL2",
         "Windows Subsystem for Linux v2 — VM Linux légère intégrée à Windows."),
        ("hns",
         "Host Network Service — gère les réseaux virtuels Hyper-V/Docker/WSL."),
        ("WinNat",
         "Windows NAT Driver — réalise la translation d'adresses entre WSL/Docker et l'hôte."),
        ("netsh",
         "Outil en ligne de commande Windows pour configurer le réseau (firewall, ports, NAT)."),
        ("Excluded Port Range",
         "Plage de ports qu'on demande à Windows de NE PAS allouer dynamiquement."),
    ]
    for term, desc in glossary:
        story.append(Paragraph(f"<b>{term}.</b> {desc}", ST_LIST))

    story.append(Paragraph("Annexe C — Commandes de référence", ST_H1))
    story.append(Paragraph("Détection", ST_H3))
    story.append(code_block(
        "Get-NetTCPConnection -LocalPort 5002\n"
        "netstat -ano | findstr :5002\n"
        "Get-Process -Id 17968"
    ))
    story.append(Paragraph("Nettoyage", ST_H3))
    story.append(code_block(
        "Stop-Process -Id 17968 -Force\n"
        "taskkill /F /T /PID 17968\n"
        "wsl --shutdown"
    ))
    story.append(Paragraph("Reset réseau (admin)", ST_H3))
    story.append(code_block(
        "Restart-Service hns -Force\n"
        "Restart-Service WinNat -Force\n"
        "Restart-Service vmcompute -Force"
    ))
    story.append(Paragraph("Réservation permanente (admin)", ST_H3))
    story.append(code_block(
        "netsh int ipv4 add excludedportrange protocol=tcp startport=5002 numberofports=1\n"
        "netsh int ipv4 delete excludedportrange protocol=tcp startport=5002 numberofports=1\n"
        "netsh int ipv4 show excludedportrange protocol=tcp"
    ))
    story.append(Paragraph("Solution radicale", ST_H3))
    story.append(code_block(
        "# Redémarrer Windows = tout est nettoyé\n"
        "shutdown /r /t 0"
    ))

    story.append(Spacer(1, 0.5*cm))
    story.append(alert_box(
        "Ce guide complète <b>FSBM_Platform_Guide_Technique.pdf</b> (installation) et "
        "<b>FSBM_Platform_Rapport_PFE.pdf</b> (présentation du projet).",
        kind="info"
    ))

    # Build
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"PDF généré : {out_path}")
    print(f"Taille : {out_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    build()
