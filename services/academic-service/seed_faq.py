"""
Pré-remplit la table faq_items à partir du dataset du chatbot (faq_dataset.json).
Idempotent : n'insère pas un intent_tag déjà présent.

Usage :  py seed_faq.py
"""
import asyncio
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

from sqlalchemy import select
from app.db.session import SessionLocal
from app.models import FaqItem

DATASET = Path(__file__).resolve().parent.parent / "chatbot-service" / "data" / "faq_dataset.json"

# Intents purement conversationnels à ne PAS exposer comme FAQ
SKIP_TAGS = {
    "identite_genre", "comment_vas_tu", "remerciement", "au_revoir",
    "insulte", "compliment", "blague",
}

PLACEHOLDER = re.compile(r"\{[^}]*\}")   # retire {name_space}, {voc}, etc.


def clean(text: str) -> str:
    return PLACEHOLDER.sub("", text).replace("  ", " ").strip()


async def main():
    if not DATASET.exists():
        print(f"[ERREUR] Dataset introuvable : {DATASET}")
        sys.exit(1)

    data = json.loads(DATASET.read_text(encoding="utf-8"))
    intents = data.get("intents", [])
    now = datetime.utcnow()
    added = skipped = 0

    async with SessionLocal() as db:
        for intent in intents:
            tag = intent.get("tag")
            if not tag or tag in SKIP_TAGS:
                continue

            patterns = (intent.get("patterns") or {}).get("fr") or []
            responses = (intent.get("responses") or {}).get("fr") or []
            if not patterns or not responses:
                continue

            # Déjà présent ?
            exists = await db.execute(select(FaqItem).where(FaqItem.intent_tag == tag))
            if exists.scalar_one_or_none():
                skipped += 1
                continue

            question = clean(patterns[0])
            if not question.endswith("?") and len(question) < 60:
                question = question + " ?"
            answer = clean(responses[0])
            keywords = ", ".join(clean(p) for p in patterns[:6])

            db.add(FaqItem(
                category_id=None,
                intent_tag=tag,
                question=question,
                answer=answer,
                keywords=keywords[:500],
                related_url=None,
                consultations=0,
                is_active=True,
                created_at=now,
                updated_at=now,
            ))
            added += 1

        await db.commit()

    print(f"[OK] FAQ seedées : {added} ajoutées, {skipped} déjà présentes.")


asyncio.run(main())
