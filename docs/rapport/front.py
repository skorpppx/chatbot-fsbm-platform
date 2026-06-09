# -*- coding: utf-8 -*-
"""Front matter du rapport : couverture, signatures, remerciements, resumes, glossaire."""
from report_engine import *
from report_engine import _hr, _scaled
from reportlab.platypus import Table, TableStyle, Spacer, Image, Paragraph, PageBreak, NextPageTemplate
from reportlab.lib.units import cm
from reportlab.lib import colors

C = ParagraphStyle("cov", parent=ST["body"], alignment=TA_CENTER, spaceAfter=4)
def cc(t, size=11, bold=False, color=INK, lead=None, sa=4):
    s = ParagraphStyle("c", parent=C, fontSize=size, leading=lead or size*1.3,
                       textColor=color, spaceAfter=sa,
                       fontName="Helvetica-Bold" if bold else "Helvetica")
    return Paragraph(t, s)

def cover():
    el = [NextPageTemplate("cover")]
    el += [Spacer(1, 0.5*cm)]
    # Bandeau etablissement
    el.append(cc("ROYAUME DU MAROC", 10, True, MUTED, sa=2))
    el.append(cc("Universite Hassan II de Casablanca", 13, True, NAVY, sa=1))
    el.append(cc("Faculte des Sciences Ben M'Sick", 12, True, NAVY, sa=1))
    el.append(cc("Departement de Mathematiques et Informatique", 10.5, False, MUTED, sa=6))
    # Logos
    try:
        lf = _scaled(LOGO_FSBM, max_w=7.5*cm, max_h=3.2*cm)
    except Exception:
        lf = Spacer(1, 2*cm)
    try:
        ld = _scaled(LOGO_DEPT, max_w=3.2*cm, max_h=2.6*cm)
    except Exception:
        ld = Spacer(1, 2*cm)
    logos = Table([[lf, ld]], colWidths=[10*cm, 6.6*cm])
    logos.setStyle(TableStyle([("ALIGN",(0,0),(0,0),"CENTER"),("ALIGN",(1,0),(1,0),"CENTER"),
                               ("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    el += [Spacer(1, 0.3*cm), logos, Spacer(1, 0.5*cm)]
    el.append(_hr(NAVY, 1.6))
    el.append(Spacer(1, 0.5*cm))
    el.append(cc("MEMOIRE DE PROJET DE FIN D'ETUDES", 13, True, ACCENT, sa=3))
    el.append(cc("Presente en vue de l'obtention de la Licence en Developpement Informatique", 10, False, MUTED, sa=14))
    # Titre
    el.append(cc("Plateforme Universitaire Intelligente FSBM", 23, True, NAVY, lead=28, sa=6))
    el.append(cc("Chatbot Conversationnel Multilingue et Architecture Micro-Services", 13.5, False, BLUE, lead=18, sa=10))
    el.append(_hr(LINE, 1.0))
    el.append(Spacer(1, 0.6*cm))
    # Realise par
    el.append(cc("Realise par :", 11, True, INK, sa=4))
    el.append(cc("Akram BELMOUSSA &nbsp;&middot;&nbsp; Zakaria BENGHAZALE &nbsp;&middot;&nbsp; Nouhaila BEN SOUMANE",
                 12, True, NAVY_D, sa=14))
    # Encadrement (2 colonnes)
    enc = Table([
        [cc("Encadre par :", 10.5, True, INK, sa=1), cc("Co-encadre par :", 10.5, True, INK, sa=1)],
        [cc("Pr. Habib BENLAHMER", 11.5, True, NAVY, sa=1), cc("Pr. Salma HANNOUNI", 11.5, True, NAVY, sa=1)],
        [cc("FSBM — Universite Hassan II", 9, False, MUTED), cc("FSBM — Universite Hassan II", 9, False, MUTED)],
    ], colWidths=[8.3*cm, 8.3*cm])
    enc.setStyle(TableStyle([("ALIGN",(0,0),(-1,-1),"CENTER")]))
    el += [enc, Spacer(1, 0.8*cm)]
    el.append(_hr(LINE, 0.8))
    el.append(Spacer(1, 0.3*cm))
    el.append(cc("Soutenu le _____ / _____ / 2026 devant le jury compose de :", 9.5, False, MUTED, sa=6))
    jury = Table([
        [cc("Pr. ___________________", 9.5, False, INK), cc("Pr. Habib BENLAHMER", 9.5, False, INK), cc("Pr. Salma HANNOUNI", 9.5, False, INK)],
        [cc("President du jury", 8.5, False, MUTED), cc("Encadrant", 8.5, False, MUTED), cc("Co-encadrante", 8.5, False, MUTED)],
    ], colWidths=[5.5*cm, 5.5*cm, 5.5*cm])
    jury.setStyle(TableStyle([("ALIGN",(0,0),(-1,-1),"CENTER")]))
    el += [jury, Spacer(1, 0.6*cm)]
    el.append(cc("Annee Universitaire 2025 — 2026", 12, True, NAVY, sa=2))
    el += [NextPageTemplate("normal")]
    return el


def signatures():
    el = front_chapter("Page de validation et signatures")
    el.append(para(
        "Le present memoire de Projet de Fin d'Etudes, intitule <b>Plateforme Universitaire "
        "Intelligente FSBM — Chatbot Conversationnel Multilingue et Architecture Micro-Services</b>, "
        "a ete realise au sein de la Faculte des Sciences Ben M'Sick (Universite Hassan II de "
        "Casablanca) durant l'annee universitaire 2025-2026. Il atteste du travail personnel et "
        "collectif des etudiants signataires et de l'encadrement assure par le corps professoral."))
    el.append(spacer(0.6))
    def sigrow(role, name):
        return [Paragraph(f"<b>{role}</b><br/><font size=9 color='#5b6577'>{name}</font>", ST["cell"]),
                Paragraph("<br/><br/>", ST["cell"])]
    data = [[Paragraph("<b>Qualite / Nom</b>", ST["cellb"]), Paragraph("<b>Signature</b>", ST["cellb"])],
            sigrow("Etudiant", "Akram BELMOUSSA"),
            sigrow("Etudiant", "Zakaria BENGHAZALE"),
            sigrow("Etudiante", "Nouhaila BEN SOUMANE"),
            sigrow("Encadrant", "Pr. Habib BENLAHMER"),
            sigrow("Co-encadrante", "Pr. Salma HANNOUNI"),
            sigrow("President du jury", "Pr. ____________________")]
    t = Table(data, colWidths=[8.5*cm, 8.1*cm])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("GRID",(0,0),(-1,-1),0.5,LINE),
                           ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,1),(-1,-1),14),
                           ("BOTTOMPADDING",(0,1),(-1,-1),14),("LEFTPADDING",(0,0),(-1,-1),8)]))
    el.append(t)
    return el


def dedication():
    el = front_chapter("Dedicaces")
    st = ParagraphStyle("ded", parent=ST["body"], alignment=TA_CENTER, fontName="Helvetica-Oblique",
                        fontSize=11.5, leading=20, textColor=NAVY_D, spaceAfter=14)
    el.append(Spacer(1, 1*cm))
    el.append(Paragraph("A nos chers parents,<br/>pour leur amour inconditionnel, leurs sacrifices "
                        "et leur soutien sans faille tout au long de notre parcours.", st))
    el.append(Paragraph("A nos familles et a nos amis,<br/>qui n'ont jamais cesse de nous encourager.", st))
    el.append(Paragraph("A nos enseignants de la Faculte des Sciences Ben M'Sick,<br/>"
                        "qui ont su transmettre leur savoir et leur passion.", st))
    el.append(Paragraph("A toutes celles et ceux qui croient que la technologie<br/>"
                        "peut rendre l'universite plus humaine et plus accessible.", st))
    el.append(Spacer(1, 0.6*cm))
    el.append(Paragraph("Nous dedions ce modeste travail.", st))
    return el


def acknowledgements():
    el = front_chapter("Remerciements")
    el.append(para(
        "Au terme de ce Projet de Fin d'Etudes, il nous est particulierement agreable d'exprimer "
        "notre gratitude et notre reconnaissance a toutes les personnes qui ont contribue, de pres "
        "ou de loin, a l'aboutissement de ce travail."))
    el.append(para(
        "Nous tenons en premier lieu a adresser nos plus vifs remerciements a notre encadrant, "
        "<b>Pr. Habib BENLAHMER</b>, pour la confiance qu'il nous a accordee, pour sa disponibilite, "
        "ses conseils avises et la rigueur scientifique qu'il a su nous transmettre. Son expertise "
        "dans le domaine des systemes d'information et de l'intelligence artificielle a constitue un "
        "apport determinant pour l'orientation et la qualite de ce projet."))
    el.append(para(
        "Nous exprimons egalement notre profonde reconnaissance a notre co-encadrante, "
        "<b>Pr. Salma HANNOUNI</b>, pour son accompagnement attentif, ses remarques constructives et "
        "son soutien constant durant toutes les phases de conception et de realisation."))
    el.append(para(
        "Nos remerciements s'adressent aussi a l'ensemble du corps professoral et administratif du "
        "<b>Departement de Mathematiques et Informatique</b> de la Faculte des Sciences Ben M'Sick, "
        "ainsi qu'au service de la scolarite, dont les echanges nous ont permis de mieux cerner les "
        "besoins reels des etudiants et de l'administration."))
    el.append(para(
        "Nous remercions chaleureusement les membres du jury d'avoir accepte d'evaluer notre travail "
        "et de l'enrichir par leurs observations."))
    el.append(para(
        "Enfin, nous ne saurions oublier nos familles et nos camarades de promotion pour leur "
        "patience, leurs encouragements et leur presence bienveillante tout au long de cette annee."))
    el.append(spacer(0.4))
    el.append(quote("La connaissance s'acquiert par l'experience, tout le reste n'est que de "
                    "l'information.", "Albert Einstein"))
    return el


def resume_fr():
    el = front_chapter("Resume")
    el.append(para(
        "Ce Projet de Fin d'Etudes porte sur la conception et la realisation d'une <b>plateforme "
        "universitaire intelligente</b> destinee a la Faculte des Sciences Ben M'Sick (FSBM) de "
        "l'Universite Hassan II de Casablanca. La plateforme repond a une problematique concrete : "
        "l'acces difficile et asynchrone des etudiants a l'information academique (filieres, modules, "
        "emplois du temps, annonces, procedures administratives) et la surcharge du service de la "
        "scolarite par des questions repetitives."))
    el.append(para(
        "La solution proposee s'articule autour d'un <b>chatbot conversationnel multilingue</b> "
        "(francais, anglais et darija marocaine) capable de comprendre le langage naturel et de "
        "fournir des reponses fiables 24 heures sur 24. Le moteur de comprehension repose sur une "
        "approche hybride combinant un classifieur <b>TF-IDF / similarite cosinus</b> pour la "
        "reconnaissance d'intentions et un <b>grand modele de langage (LLaMA 3.3-70B)</b> exploite "
        "via une architecture <b>RAG (Retrieval-Augmented Generation)</b>, garantissant a la fois la "
        "rapidite, la fiabilite et la richesse des reponses grace a une cascade de repli (fallback)."))
    el.append(para(
        "Sur le plan logiciel, la plateforme adopte une <b>architecture micro-services</b> : un "
        "frontend <b>Angular 17</b> (composants standalone, signals, lazy loading), deux services "
        "backend <b>FastAPI</b> asynchrones, une base de donnees relationnelle <b>MySQL 8</b> (16 "
        "tables, troisieme forme normale) pour les donnees structurees et une base <b>NoSQL "
        "MongoDB</b> pour les conversations et les sessions. Un espace d'administration securise par "
        "<b>JWT et bcrypt</b> permet la gestion complete des contenus (annonces, evenements, "
        "donnees academiques, vie etudiante, FAQ) ainsi que la moderation des avis etudiants."))
    el.append(para(
        "Le systeme a ete valide par une serie de tests fonctionnels et techniques (33 cas de test "
        "automatises reussis), affichant un temps de reponse moyen inferieur a 200 millisecondes en "
        "mode classique et une disponibilite garantie a 100 % grace au mecanisme de repli. Ce "
        "memoire detaille l'ensemble de la demarche d'ingenierie : etude de l'existant, analyse des "
        "besoins, conception UML, architecture, implementation, securite, tests et perspectives "
        "d'evolution."))
    el.append(spacer(0.3))
    el.append(Paragraph("<b>Mots-cles :</b> Chatbot, Traitement Automatique du Langage Naturel (TALN), "
                        "TF-IDF, RAG, LLaMA, Micro-services, Angular, FastAPI, MySQL, MongoDB, JWT, "
                        "Universite intelligente, Darija.", ST["body"]))
    return el


def abstract_en():
    el = front_chapter("Abstract")
    el.append(para(
        "This graduation project deals with the design and implementation of an <b>intelligent "
        "university platform</b> for the Faculty of Sciences Ben M'Sick (FSBM), Hassan II University "
        "of Casablanca. The platform addresses a concrete problem: the difficult and asynchronous "
        "access of students to academic information (programs, modules, timetables, announcements, "
        "administrative procedures) and the overload of the registrar's office with repetitive "
        "questions."))
    el.append(para(
        "The proposed solution is built around a <b>multilingual conversational chatbot</b> (French, "
        "English and Moroccan Darija) able to understand natural language and provide reliable "
        "answers around the clock. The understanding engine relies on a hybrid approach combining a "
        "<b>TF-IDF / cosine-similarity</b> classifier for intent recognition and a <b>Large Language "
        "Model (LLaMA 3.3-70B)</b> used through a <b>Retrieval-Augmented Generation (RAG)</b> "
        "architecture, ensuring speed, reliability and rich answers thanks to a fallback cascade."))
    el.append(para(
        "From a software standpoint, the platform adopts a <b>micro-services architecture</b>: an "
        "<b>Angular 17</b> frontend (standalone components, signals, lazy loading), two asynchronous "
        "<b>FastAPI</b> backend services, a relational <b>MySQL 8</b> database (16 tables, third "
        "normal form) for structured data, and a <b>MongoDB</b> NoSQL database for conversations and "
        "sessions. A secure administration area protected by <b>JWT and bcrypt</b> enables full "
        "content management (announcements, events, academic data, student life, FAQ) and the "
        "moderation of student reviews."))
    el.append(para(
        "The system was validated through a series of functional and technical tests (33 successful "
        "automated test cases), achieving an average response time below 200 milliseconds in classic "
        "mode and 100% guaranteed availability thanks to the fallback mechanism. This report details "
        "the complete engineering process: state of the art, requirements analysis, UML design, "
        "architecture, implementation, security, testing and future work."))
    el.append(spacer(0.3))
    el.append(Paragraph("<b>Keywords:</b> Chatbot, Natural Language Processing (NLP), TF-IDF, RAG, "
                        "LLaMA, Micro-services, Angular, FastAPI, MySQL, MongoDB, JWT, Smart "
                        "University, Darija.", ST["body"]))
    return el


def glossary():
    el = front_chapter("Glossaire")
    rows = [["Terme", "Definition"],
        ["Chatbot", "Programme informatique capable de dialoguer avec un utilisateur en langage naturel, par texte ou par voix."],
        ["Darija", "Arabe dialectal marocain, langue maternelle de la majorite des Marocains, ici pris en charge en graphie latine et arabe."],
        ["Embedding", "Representation vectorielle dense d'un mot, d'une phrase ou d'un document dans un espace de grande dimension."],
        ["Fallback (repli)", "Mecanisme de secours active automatiquement lorsqu'un service principal est indisponible, garantissant la continuite."],
        ["Intention (intent)", "Categorie semantique representant le but d'un message utilisateur (ex. : s'inscrire, consulter les filieres)."],
        ["Micro-service", "Style d'architecture ou l'application est decoupee en services autonomes, deployables et evolutifs independamment."],
        ["Middleware", "Composant logiciel intercale dans le traitement d'une requete (authentification, CORS, journalisation)."],
        ["NoSQL", "Famille de bases de donnees non relationnelles, adaptees aux donnees semi-structurees et a la montee en charge horizontale."],
        ["ORM", "Object-Relational Mapping : technique faisant correspondre des objets du code a des tables d'une base relationnelle."],
        ["RAG", "Retrieval-Augmented Generation : technique enrichissant un modele de langage par des connaissances recuperees a la volee."],
        ["Token", "Unite elementaire de texte (mot, sous-mot) manipulee par les modeles de langage ; aussi, jeton d'authentification (JWT)."],
        ["TF-IDF", "Term Frequency-Inverse Document Frequency : ponderation statistique mesurant l'importance d'un terme dans un corpus."],
    ]
    el += table(rows, "Glossaire des termes techniques", col_widths=[2.3, 7.7])
    return el


def acronyms():
    el = front_chapter("Liste des acronymes")
    data = [
        ("API", "Application Programming Interface"),
        ("ASGI", "Asynchronous Server Gateway Interface"),
        ("CORS", "Cross-Origin Resource Sharing"),
        ("CRUD", "Create, Read, Update, Delete"),
        ("FSBM", "Faculte des Sciences Ben M'Sick"),
        ("HTTP", "HyperText Transfer Protocol"),
        ("IA", "Intelligence Artificielle"),
        ("JWT", "JSON Web Token"),
        ("LLM", "Large Language Model"),
        ("MCD", "Modele Conceptuel de Donnees"),
        ("MLD", "Modele Logique de Donnees"),
        ("MPD", "Modele Physique de Donnees"),
        ("NLP", "Natural Language Processing (TALN)"),
        ("ORM", "Object-Relational Mapping"),
        ("OWASP", "Open Worldwide Application Security Project"),
        ("RAG", "Retrieval-Augmented Generation"),
        ("RBAC", "Role-Based Access Control"),
        ("REST", "Representational State Transfer"),
        ("SGBD", "Systeme de Gestion de Base de Donnees"),
        ("SPA", "Single Page Application"),
        ("TALN", "Traitement Automatique du Langage Naturel"),
        ("TF-IDF", "Term Frequency-Inverse Document Frequency"),
        ("UH2C", "Universite Hassan II de Casablanca"),
        ("UML", "Unified Modeling Language"),
        ("XSS", "Cross-Site Scripting"),
    ]
    # deux colonnes
    half = (len(data)+1)//2
    left, right = data[:half], data[half:]
    rows = [["Acronyme", "Signification", "Acronyme", "Signification"]]
    for i in range(half):
        l = left[i]; r = right[i] if i < len(right) else ("","")
        rows.append([l[0], l[1], r[0], r[1]])
    el += table(rows, "Liste des acronymes et abreviations", col_widths=[1.4, 3.6, 1.4, 3.6], font=8.2)
    return el
