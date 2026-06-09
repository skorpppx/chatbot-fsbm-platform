# -*- coding: utf-8 -*-
"""Guide_Installation_FSBM.pdf — Guide complet d'installation et d'execution (liens cliquables)."""
from report_engine import *
from report_engine import _hr, _scaled
from front import cc
from reportlab.platypus import NextPageTemplate, PageBreak, Spacer, Paragraph

LINKBLUE = "#1565C0"


def lnk(url, text=None):
    """Lien cliquable (fonctionne dans para/bullets/numbered, pas dans les cellules de table)."""
    return f'<a href="{url}" color="{LINKBLUE}"><u>{text or url}</u></a>'


def cov(s):
    s += [NextPageTemplate("cover"), Spacer(1, 1.3*cm)]
    s.append(cc("Universite Hassan II de Casablanca", 13, True, NAVY, sa=1))
    s.append(cc("Faculte des Sciences Ben M'Sick — Departement de Mathematiques et Informatique", 9.5, False, MUTED, sa=10))
    try:
        lf = _scaled(LOGO_FSBM, max_w=7*cm, max_h=3*cm); lf.hAlign = "CENTER"; s.append(lf)
    except Exception: pass
    s += [Spacer(1, 0.5*cm), _hr(NAVY, 1.6), Spacer(1, 0.5*cm)]
    s.append(cc("GUIDE D'INSTALLATION & D'EXECUTION", 13, True, ACCENT, sa=3))
    s.append(cc("Plateforme Universitaire Intelligente FSBM", 22, True, NAVY, lead=27, sa=8))
    s.append(cc("Logiciels requis, configuration et lancement du projet sur une nouvelle machine",
                12.5, False, BLUE, lead=17, sa=14))
    s.append(_hr(LINE, 1.0)); s.append(Spacer(1, 0.4*cm))
    s.append(cc("Chatbot multilingue (Angular 17 · FastAPI · MySQL · LLaMA 3 / Groq)", 10.5, False, INK, sa=10))
    s.append(cc("Akram BELMOUSSA · Zakaria BENGHAZALE · Nouhaila BEN SOUMANE", 10.5, True, NAVY_D, sa=4))
    s.append(cc("Annee universitaire 2025-2026", 10.5, True, NAVY, sa=2))
    s += [NextPageTemplate("normal"), PageBreak()]


def build_guide():
    reset_numbering()
    s = []
    cov(s)
    s += plain_heading("Sommaire"); s.append(make_toc())

    # ── Introduction ──────────────────────────────────────────────────────────
    s += chapter("Introduction")
    s.append(para(
        "Ce guide explique, pas a pas, comment installer les logiciels necessaires et lancer la "
        "plateforme FSBM sur une <b>nouvelle machine</b>. Il s'adresse a toute personne (membre du "
        "jury, enseignant, etudiant) souhaitant executer le projet en local."))
    s.append(para(
        "La procedure detaillee vise <b>Windows 10/11</b> (environnement de developpement du projet). "
        "Une annexe fournit les equivalents <b>Linux / macOS</b>. Comptez environ <b>30 a 45 minutes</b> "
        "pour une premiere installation."))
    s += table([
        ["Composant", "Technologie", "Port"],
        ["Frontend", "Angular 17 (Node.js)", "4200"],
        ["Service chatbot", "FastAPI (Python)", "8001"],
        ["Service academique", "FastAPI (Python)", "8002"],
        ["Base de donnees", "MySQL 8", "3306"],
    ], "Vue d'ensemble des composants et de leurs ports", col_widths=[3.2, 4.8, 2.0])
    s.append(alert(
        "La persistance utilise <b>MySQL</b>. <b>MongoDB n'est pas requis</b> pour executer la version "
        "actuelle (il figure dans l'architecture cible comme evolution prevue pour les journaux de "
        "conversation). Vous n'avez donc pas besoin de l'installer.", "info"))

    s += _ch_logiciels()
    s += _ch_verif()
    s += _ch_projet()
    s += _ch_db()
    s += _ch_env()
    s += _ch_deps()
    s += _ch_lancement()
    s += _ch_verification()
    s += _ch_depannage()
    s += _ch_annexe()

    build("Guide_Installation_FSBM.pdf", s, title="Guide d'Installation FSBM",
          author="A. BELMOUSSA, Z. BENGHAZALE, N. BEN SOUMANE")


# ══════════════════════════════════════════════════════════════════════════════
def _ch_logiciels():
    el = chapter("Logiciels a Installer")
    el.append(para(
        "Installez les logiciels suivants dans l'ordre. Les liens de telechargement officiels sont "
        "<b>cliquables</b> (cliquez directement sur le nom du site)."))
    el += table([
        ["Logiciel", "Version conseillee", "Role"],
        ["Python", "3.11 ou 3.12 (min. 3.10)", "Execute les 2 services backend (FastAPI)"],
        ["Node.js", "20 LTS (min. 18.13)", "Execute le frontend Angular 17"],
        ["MySQL", "8.0 ou 8.4", "Base de donnees (referentiel + comptes)"],
        ["Git", "Derniere version", "Recuperer le code (optionnel si copie)"],
        ["VS Code", "Derniere version", "Editeur de code (optionnel)"],
    ], "Logiciels requis", col_widths=[2.2, 3.4, 4.4])

    el.append(section("Liens de telechargement officiels"))
    el += bullets([
        f"<b>Python</b> — {lnk('https://www.python.org/downloads/', 'python.org/downloads')} "
        "&nbsp; (a l'installation, cochez <b>« Add python.exe to PATH »</b>).",
        f"<b>Node.js</b> (LTS) — {lnk('https://nodejs.org/', 'nodejs.org')} "
        "&nbsp; (choisissez la version <b>LTS</b> ; npm est inclus).",
        f"<b>MySQL</b> (Community Server / Installer) — {lnk('https://dev.mysql.com/downloads/installer/', 'dev.mysql.com/downloads/installer')} "
        "&nbsp; (notez bien le <b>mot de passe root</b> que vous definissez).",
        f"<b>Git</b> — {lnk('https://git-scm.com/downloads', 'git-scm.com/downloads')}.",
        f"<b>Visual Studio Code</b> (optionnel) — {lnk('https://code.visualstudio.com/', 'code.visualstudio.com')}.",
    ])
    el.append(section("Comptes en ligne (optionnels, pour le mode IA)"))
    el.append(para(
        "Le chatbot fonctionne <b>sans Internet</b> grace au moteur local (TF-IDF + resolveur). Pour "
        "activer le <b>mode IA generatif</b> (LLaMA 3), creez une cle API gratuite :"))
    el += bullets([
        f"<b>Groq</b> (recommande, gratuit) — inscription : {lnk('https://console.groq.com', 'console.groq.com')}, "
        f"puis creez une cle sur {lnk('https://console.groq.com/keys', 'console.groq.com/keys')} "
        "(elle commence par <font face='Courier'>gsk_</font>).",
        f"<b>HuggingFace</b> (repli optionnel) — {lnk('https://huggingface.co/settings/tokens', 'huggingface.co/settings/tokens')} "
        "(cle commencant par <font face='Courier'>hf_</font>).",
    ])
    el.append(alert(
        "Sans cle Groq/HuggingFace, la plateforme reste <b>100 % fonctionnelle</b> : le mode classique "
        "(local, ~10 ms) repond a toutes les questions du referentiel.", "tip"))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch_verif():
    el = chapter("Verifier les Prerequis")
    el.append(para(
        "Apres installation, ouvrez un terminal (<b>PowerShell</b> sur Windows) et verifiez que "
        "chaque outil repond. Les versions affichees peuvent differer legerement."))
    el += code(
        "py --version            # Python 3.11.x  (ou : python --version)\n"
        "node -v                 # v20.x.x\n"
        "npm -v                  # 10.x.x\n"
        "mysql --version         # Ver 8.0.x\n"
        "git --version           # git version 2.x", "Commandes de verification")
    el.append(para(
        "Si une commande n'est <b>pas reconnue</b>, c'est que le logiciel n'est pas installe ou pas "
        "ajoute au PATH (voir le chapitre Depannage)."))
    el.append(alert(
        "Sur Windows, Python s'invoque avec <b>py</b> (le « Python Launcher »). Sur Linux/macOS, "
        "utilisez <b>python3</b> et <b>pip3</b>.", "info"))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch_projet():
    el = chapter("Recuperer le Projet")
    el.append(para(
        "Placez le dossier du projet sur la machine, par exemple dans "
        "<font face='Courier'>C:\\Users\\&lt;vous&gt;\\fsbm-platform</font>. Deux options :"))
    el.append(section("Option A — Copier le dossier"))
    el.append(para("Copiez simplement le dossier complet du projet (cle USB, archive ZIP, reseau), "
                   "puis decompressez-le si necessaire."))
    el.append(section("Option B — Cloner avec Git"))
    el += code("git clone <URL-de-votre-depot> fsbm-platform\n"
               "cd fsbm-platform", "Si le projet est heberge sur un depot Git")
    el.append(para("Le dossier doit contenir notamment : <font face='Courier'>services/</font>, "
                   "<font face='Courier'>frontend/</font>, <font face='Courier'>database/</font>, "
                   "<font face='Courier'>SETUP.ps1</font> et <font face='Courier'>start.ps1</font>."))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch_db():
    el = chapter("Preparer la Base de Donnees MySQL")
    el.append(para(
        "La base s'appelle <b>fsbm_db</b>. Il faut la creer puis executer les scripts SQL <b>dans "
        "l'ordre</b> (du plus ancien au plus recent)."))
    el.append(section("1. Creer la base"))
    el += code('mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS fsbm_db '
               'CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"',
               "Saisissez le mot de passe root MySQL quand il est demande")
    el.append(section("2. Executer les scripts dans l'ordre"))
    el += table([
        ["Ordre", "Fichier (database/mysql/)", "Contenu"],
        ["1", "01_schema.sql", "Schema : creation des tables"],
        ["2", "02_seed_static.sql", "Donnees de base (departements, filieres)"],
        ["3", "03_seed_modules.sql", "Modules"],
        ["4", "04_seed_data.sql", "Etudiants modelises, annonces..."],
        ["5", "05_phase2_reviews_auth.sql", "Avis + comptes admin (auth)"],
        ["6", "06_phase2_uploads.sql", "Champs de televersement (photos/logos)"],
        ["7", "07_real_fsbm_data.sql", "Donnees reelles FSBM (UPSERT)"],
        ["8", "08_real_fsbm_clean.sql", "Remplacement par les donnees reelles propres"],
    ], "Scripts SQL a executer dans l'ordre", col_widths=[1.0, 4.3, 4.7], font=8.4)
    el.append(para("Depuis la racine du projet, sous PowerShell :"))
    el += code(
        "$pwd_mysql = Read-Host 'Mot de passe root MySQL'\n"
        "Get-ChildItem database\\mysql\\0*.sql | Sort-Object Name | ForEach-Object {\n"
        "    Write-Host \"-> $($_.Name)\"\n"
        "    Get-Content $_.FullName | mysql -u root \"-p$pwd_mysql\" fsbm_db\n"
        "}", "Execute 01..08 dans l'ordre (PowerShell)")
    el.append(para("Equivalent ligne par ligne (Windows cmd ou Linux/macOS) :"))
    el += code("mysql -u root -p fsbm_db < database/mysql/01_schema.sql\n"
               "mysql -u root -p fsbm_db < database/mysql/02_seed_static.sql\n"
               "...\n"
               "mysql -u root -p fsbm_db < database/mysql/08_real_fsbm_clean.sql", None)
    el.append(alert(
        "Le script <b>SETUP.ps1</b> (chapitre Lancement) effectue automatiquement cette "
        "initialisation. Cette procedure manuelle est utile en cas de probleme.", "tip"))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch_env():
    el = chapter("Configurer les Variables (.env)")
    el.append(para(
        "Chaque service lit sa configuration dans un fichier <font face='Courier'>.env</font>. Un "
        "modele <font face='Courier'>.env.example</font> est fourni : copiez-le en "
        "<font face='Courier'>.env</font> et renseignez vos valeurs."))
    el += code(
        "copy services\\chatbot-service\\.env.example  services\\chatbot-service\\.env\n"
        "copy services\\academic-service\\.env.example services\\academic-service\\.env",
        "Windows (sous Linux/macOS : cp)")
    el.append(section("Variables principales"))
    el += table([
        ["Variable", "Valeur conseillee", "Description"],
        ["DB_HOST", "localhost", "Hote MySQL"],
        ["DB_PORT", "3306", "Port MySQL"],
        ["DB_NAME", "fsbm_db", "Nom de la base"],
        ["DB_USER", "root", "Utilisateur MySQL"],
        ["DB_PASSWORD", "(votre mot de passe)", "Mot de passe root MySQL"],
        ["GROQ_API_KEY", "(vide ou gsk_...)", "Cle Groq pour le mode IA (optionnel)"],
        ["GROQ_MODEL", "default", "default = LLaMA 3.3-70B"],
        ["CORS_ORIGINS", "http://localhost:4200", "Origines autorisees (frontend)"],
        ["CONFIDENCE_THRESHOLD", "0.15", "Seuil du classifieur (chatbot)"],
    ], "Variables d'environnement (.env)", col_widths=[3.6, 3.2, 3.2], font=8.0)
    el.append(para(
        f"Pour obtenir la cle Groq (gratuite) : {lnk('https://console.groq.com/keys', 'console.groq.com/keys')}. "
        "Collez la valeur apres <font face='Courier'>GROQ_API_KEY=</font> (sans guillemets)."))
    el.append(alert(
        "Ne partagez jamais votre fichier <font face='Courier'>.env</font> : il contient des secrets "
        "(mot de passe BDD, cles API). Il ne doit pas etre publie sur un depot public.", "warn"))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch_deps():
    el = chapter("Installer les Dependances")
    el.append(section("Backend (Python)"))
    el.append(para("Installez les dependances des <b>deux</b> services :"))
    el += code(
        "cd services\\chatbot-service\n"
        "py -m pip install -r requirements.txt\n"
        "cd ..\\academic-service\n"
        "py -m pip install -r requirements.txt\n"
        "cd ..\\..", "Installe FastAPI, SQLAlchemy, scikit-learn, groq, bcrypt, etc.")
    el.append(para("Principaux paquets installes : <b>fastapi</b>, <b>uvicorn</b>, <b>sqlalchemy</b>, "
                   "<b>aiomysql</b>/<b>pymysql</b>, <b>scikit-learn</b>, <b>numpy</b>, <b>groq</b>, "
                   "<b>python-jose</b>, <b>bcrypt</b>, <b>email-validator</b>."))
    el.append(alert(
        "Bonne pratique (optionnel) : creer un environnement virtuel par service avant "
        "l'installation : <font face='Courier'>py -m venv .venv</font> puis "
        "<font face='Courier'>.\\.venv\\Scripts\\activate</font>.", "info"))
    el.append(section("Frontend (Node.js / Angular)"))
    el += code(
        "npm install -g @angular/cli@17     # Angular CLI (une seule fois)\n"
        "cd frontend\n"
        "npm install                        # dependances du projet\n"
        "cd ..", "Installe Angular 17 et les paquets du frontend")
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch_lancement():
    el = chapter("Lancer la Plateforme")
    el.append(para("Deux methodes : <b>automatique</b> (recommandee) ou <b>manuelle</b> (3 terminaux)."))

    el.append(section("Methode A — Script tout-en-un (recommande)"))
    el.append(para("Depuis la racine du projet, sous PowerShell :"))
    el += code("powershell -ExecutionPolicy Bypass -File .\\SETUP.ps1",
               "Configure .env, installe, initialise la BDD et lance tout")
    el.append(para("Si tout est deja installe et configure, lancez simplement les services :"))
    el += code("powershell -ExecutionPolicy Bypass -File .\\start.ps1",
               "Demarre academic (8002), chatbot (8001) et le frontend (4200)")

    el.append(section("Methode B — Lancement manuel (3 terminaux)"))
    el.append(para("Ouvrez <b>trois</b> terminaux a la racine du projet."))
    el.append(para("<b>Terminal 1 — service academique (port 8002) :</b>"))
    el += code("cd services\\academic-service\n"
               "py -m uvicorn app.main:app --reload --port 8002", None)
    el.append(para("<b>Terminal 2 — service chatbot (port 8001) :</b>"))
    el += code("cd services\\chatbot-service\n"
               "py -m uvicorn app.main:app --reload --port 8001", None)
    el.append(para("<b>Terminal 3 — frontend Angular (port 4200) :</b>"))
    el += code("cd frontend\n"
               "npm start            # equivaut a : ng serve (proxy -> 8001/8002)", None)
    el.append(alert(
        "Le frontend communique avec les services via <font face='Courier'>proxy.conf.json</font> : "
        "<font face='Courier'>/api/chat</font> et <font face='Courier'>/api/llm</font> vers le port "
        "<b>8001</b>, <font face='Courier'>/api/academic</font> vers le port <b>8002</b>. Respectez "
        "donc ces deux ports au lancement.", "key"))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch_verification():
    el = chapter("Verifier que Tout Fonctionne")
    el.append(para("Une fois les trois composants demarres, ouvrez votre navigateur :"))
    el += bullets([
        f"Interface principale : {lnk('http://localhost:4200', 'http://localhost:4200')}",
        f"API chatbot (Swagger) : {lnk('http://localhost:8001/docs', 'http://localhost:8001/docs')}",
        f"API academique (Swagger) : {lnk('http://localhost:8002/docs', 'http://localhost:8002/docs')}",
        f"Espace administration : {lnk('http://localhost:4200/admin/login', 'http://localhost:4200/admin/login')}",
    ])
    el.append(para("Test rapide du chatbot : sur la page d'accueil, posez par exemple "
                   "<i>« Qui est le doyen de la FSBM ? »</i> — la reponse attendue est "
                   "<b>Pr. Abdeslam EL BOUARI</b>. Essayez aussi en darija : "
                   "<i>« Chkoun mas'oul 3la filiere DI ? »</i> &rarr; <b>Pr. SAEL Nihal</b>."))
    el.append(alert(
        "Si les pages du referentiel (departements, filieres) sont vides, c'est generalement que la "
        "base n'a pas ete initialisee (chapitre 4) ou que le service academique (8002) n'est pas "
        "demarre.", "info"))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch_depannage():
    el = chapter("Depannage (Problemes Frequents)")
    el += table([
        ["Probleme", "Cause probable", "Solution"],
        ["« py » ou « python » non reconnu", "Python absent du PATH",
         "Reinstaller Python en cochant « Add to PATH », ou utiliser python/python3."],
        ["« ng » non reconnu", "Angular CLI non installe",
         "npm install -g @angular/cli@17"],
        ["Port deja utilise (8001/8002/4200)", "Un service tourne deja",
         "Fermer l'ancien processus, ou changer le port (--port)."],
        ["ModuleNotFoundError (email_validator, bcrypt...)", "Dependances non installees",
         "py -m pip install -r requirements.txt dans le service concerne."],
        ["MySQL : Access denied", "Mauvais mot de passe",
         "Verifier DB_PASSWORD dans .env (mot de passe root)."],
        ["MySQL : Unknown database 'fsbm_db'", "Base non creee",
         "Refaire le chapitre 4 (creation + scripts 01..08)."],
        ["Frontend OK mais donnees vides", "Services backend non lances / mauvais ports",
         "Lancer academic sur 8002 et chatbot sur 8001 (cf. proxy)."],
        ["Erreur CORS dans la console", "Origine non autorisee",
         "Verifier CORS_ORIGINS=http://localhost:4200 dans les .env."],
        ["Mode IA repond « je n'ai pas l'info »", "Cle Groq absente/quota atteint",
         "Le mode local repond quand meme ; ajouter une cle Groq pour le generatif."],
    ], "Tableau de depannage", col_widths=[3.4, 3.0, 3.6], font=7.7)
    el.append(alert(
        "En cas de blocage des ports sous Windows, listez puis arretez le processus : "
        "<font face='Courier'>netstat -ano | findstr :8001</font> puis "
        "<font face='Courier'>taskkill /PID &lt;pid&gt; /F</font>.", "info"))
    return el


# ══════════════════════════════════════════════════════════════════════════════
def _ch_annexe():
    el = front_chapter("Annexe — Recapitulatif")
    el.append(section("Tous les liens de telechargement"))
    el += bullets([
        f"Python — {lnk('https://www.python.org/downloads/', 'python.org/downloads')}",
        f"Node.js (LTS) — {lnk('https://nodejs.org/', 'nodejs.org')}",
        f"MySQL — {lnk('https://dev.mysql.com/downloads/installer/', 'dev.mysql.com/downloads/installer')}",
        f"Git — {lnk('https://git-scm.com/downloads', 'git-scm.com/downloads')}",
        f"VS Code — {lnk('https://code.visualstudio.com/', 'code.visualstudio.com')}",
        f"Cle Groq (gratuite) — {lnk('https://console.groq.com/keys', 'console.groq.com/keys')}",
        f"Token HuggingFace — {lnk('https://huggingface.co/settings/tokens', 'huggingface.co/settings/tokens')}",
        f"Documentation Angular — {lnk('https://angular.dev', 'angular.dev')}",
        f"Documentation FastAPI — {lnk('https://fastapi.tiangolo.com', 'fastapi.tiangolo.com')}",
    ])
    el.append(section("Ports utilises"))
    el += table([
        ["Service", "URL locale", "Port"],
        ["Frontend (Angular)", "http://localhost:4200", "4200"],
        ["Service chatbot (API)", "http://localhost:8001/docs", "8001"],
        ["Service academique (API)", "http://localhost:8002/docs", "8002"],
        ["MySQL", "localhost", "3306"],
    ], "Recapitulatif des ports", col_widths=[4.0, 4.0, 2.0])

    el.append(section("Aide-memoire des commandes"))
    el += code(
        "# 1. Base de donnees\n"
        'mysql -u root -p -e "CREATE DATABASE fsbm_db CHARACTER SET utf8mb4;"\n'
        "Get-ChildItem database\\mysql\\0*.sql | Sort-Object Name | %% { Get-Content $_ | mysql -u root -p fsbm_db }\n\n"
        "# 2. Dependances backend (x2 services)\n"
        "py -m pip install -r services\\chatbot-service\\requirements.txt\n"
        "py -m pip install -r services\\academic-service\\requirements.txt\n\n"
        "# 3. Dependances frontend\n"
        "npm install -g @angular/cli@17\n"
        "cd frontend && npm install && cd ..\n\n"
        "# 4. Lancement (tout-en-un)\n"
        "powershell -ExecutionPolicy Bypass -File .\\start.ps1", "Resume des etapes essentielles")

    el.append(section("Equivalents Linux / macOS"))
    el += bullets([
        "Python : <font face='Courier'>python3</font> / <font face='Courier'>pip3</font> "
        "(au lieu de <font face='Courier'>py</font>).",
        "MySQL : installer via <font face='Courier'>apt install mysql-server</font> (Debian/Ubuntu) "
        "ou <font face='Courier'>brew install mysql</font> (macOS).",
        "Copie de fichiers : <font face='Courier'>cp</font> au lieu de "
        "<font face='Courier'>copy</font> ; import SQL : "
        "<font face='Courier'>mysql -u root -p fsbm_db &lt; fichier.sql</font>.",
        "Lancement : memes commandes uvicorn et <font face='Courier'>npm start</font> ; les scripts "
        "<font face='Courier'>.ps1</font> sont specifiques a Windows (lancez les services a la main).",
    ])
    el.append(spacer(0.2))
    el.append(quote("Une fois ces etapes terminees, la plateforme est accessible sur "
                    "http://localhost:4200 et repond en francais, anglais et darija.",
                    "Fin du guide"))
    return el


if __name__ == "__main__":
    build_guide()
