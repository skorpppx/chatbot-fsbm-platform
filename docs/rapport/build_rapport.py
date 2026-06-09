# -*- coding: utf-8 -*-
"""Assemble le rapport PFE complet et lance le multiBuild (TOC/LOF/LOT resolus)."""
from report_engine import *
import front

# Modules de chapitres (importes s'ils existent)
import importlib
def _try(name):
    try: return importlib.import_module(name)
    except Exception as e:
        print(f"  [skip] {name}: {repr(e)[:80]}"); return None

ch1_4   = _try("ch01_04")
ch5_8   = _try("ch05_08")
ch9_14  = _try("ch09_14")
annexes = _try("annexes")

story = []
# ─── Couverture + liminaires ──────────────────────────────────────────────────
story += front.cover()
story += front.signatures()
story += front.dedication()
story += front.acknowledgements()
story += front.resume_fr()
story += front.abstract_en()
# ─── Sommaire + listes ────────────────────────────────────────────────────────
story += plain_heading("Table des matieres")
story.append(make_toc())
story += plain_heading("Liste des figures")
story.append(make_list("LOFEntry"))
story += plain_heading("Liste des tableaux")
story.append(make_list("LOTEntry"))
story += front.glossary()
story += front.acronyms()
# ─── Corps ────────────────────────────────────────────────────────────────────
reset_numbering()
if ch1_4:   story += ch1_4.build()
if ch5_8:   story += ch5_8.build()
if ch9_14:  story += ch9_14.build()
if annexes: story += annexes.build()

build("Rapport_PFE_FSBM.pdf", story,
      title="Rapport PFE - Plateforme Universitaire Intelligente FSBM",
      author="A. BELMOUSSA, Z. BENGHAZALE, N. BEN SOUMANE")
