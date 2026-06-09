# -*- coding: utf-8 -*-
from report_engine import *

story = []
# cover (blank template page)
story += [Spacer(1, 8*cm), Paragraph("TEST", ST["title"]), NextPageTemplate("normal"), PageBreak()]

# TOC
story += front_chapter("Table des matieres")
toc = make_toc(); story.append(toc)
story += front_chapter("Liste des figures")
lof = make_list("LOFEntry"); story.append(lof)
story += front_chapter("Liste des tableaux")
lot = make_list("LOTEntry"); story.append(lot)

# Chapter 1
story += chapter("Test du moteur")
story.append(section("Diagramme Mermaid"))
story.append(para("Ceci verifie le rendu d'un diagramme UML via mermaid.ink."))
story += figure_mermaid(
    "graph LR\n  U[Etudiant]-->A[Angular]\n  A-->|REST|F[FastAPI]\n  F-->M[(MySQL)]\n  F-->G[(MongoDB)]",
    "Architecture simplifiee de la plateforme")
story.append(section("Graphique"))
def draw(fig):
    ax = fig.add_subplot(111)
    ax.bar(["FR","EN","Darija"], [188,186,461], color=["#1C3F6E","#2d5a9e","#FF6B35"])
    ax.set_title("Patterns par langue"); ax.set_ylabel("Nombre")
story += chart(draw, "Repartition des patterns NLP par langue")
story.append(section("Tableau et capture"))
story += table([["Service","Port"],["Frontend","4200"],["Chatbot","8001"],["Academic","8002"]],
               "Ports des services", col_widths=[3,1])
story += figure_img(shot(5), "Tableau de bord de la plateforme", max_h=9*cm)

build("TEST_RAPPORT.pdf", story, title="Test")
