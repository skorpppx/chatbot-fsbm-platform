"""Test end-to-end Phase 2 (in-process, contre la vraie BDD)."""
import asyncio, sys
sys.stdout.reconfigure(encoding="utf-8")
import httpx
from app.main import app

ADMIN = {"email": "admin@fsbm.ac.ma", "password": "Admin@FSBM2026"}


async def main():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        ok = 0; fail = 0
        def check(name, cond, extra=""):
            nonlocal ok, fail
            if cond: ok += 1; print(f"  [OK] {name}")
            else: fail += 1; print(f"  [FAIL] {name} {extra}")

        # 1. Login admin
        r = await c.post("/api/auth/login", json=ADMIN)
        check("login admin -> 200", r.status_code == 200, f"got {r.status_code} {r.text[:120]}")
        token = r.json().get("access_token") if r.status_code == 200 else None
        check("token recu", bool(token))
        h = {"Authorization": f"Bearer {token}"}

        # 2. Login mauvais mdp
        r = await c.post("/api/auth/login", json={"email": ADMIN["email"], "password": "wrong"})
        check("login mauvais mdp -> 401", r.status_code == 401, f"got {r.status_code}")

        # 3. Reviews publiques
        r = await c.get("/api/reviews")
        check("GET /reviews -> 200", r.status_code == 200, f"got {r.status_code}")
        check("reviews seed presentes (>=4)", len(r.json()) >= 4, f"count={len(r.json())}")

        # 4. Stats
        r = await c.get("/api/reviews/stats")
        s = r.json()
        check("GET /reviews/stats -> 200", r.status_code == 200)
        check("note moyenne IA > 0", s.get("ai_average", 0) > 0, f"avg={s.get('ai_average')}, count={s.get('ai_count')}")

        # 5. Creer un avis (public)
        r = await c.post("/api/reviews", json={
            "target_type": "AI_ASSISTANT", "rating": 5,
            "comment": "Test automatise e2e", "author_name": "Tester"})
        check("POST /reviews -> 201", r.status_code == 201, f"got {r.status_code} {r.text[:120]}")
        new_id = r.json().get("id") if r.status_code == 201 else None

        # 6. Admin reviews SANS token -> 401
        r = await c.get("/api/admin/reviews")
        check("GET /admin/reviews sans token -> 401", r.status_code == 401, f"got {r.status_code}")

        # 7. Admin reviews AVEC token -> 200
        r = await c.get("/api/admin/reviews", headers=h)
        check("GET /admin/reviews avec token -> 200", r.status_code == 200, f"got {r.status_code}")

        # 8. Moderation : masquer puis supprimer l'avis de test
        if new_id:
            r = await c.patch(f"/api/admin/reviews/{new_id}", json={"status": "HIDDEN"}, headers=h)
            check("PATCH moderation -> 200", r.status_code == 200, f"got {r.status_code}")
            r = await c.delete(f"/api/admin/reviews/{new_id}", headers=h)
            check("DELETE avis test -> 200", r.status_code == 200, f"got {r.status_code}")

        # 9. CRUD admin : creer annonce puis supprimer
        r = await c.post("/api/admin/announcements", headers=h, json={
            "title": "Annonce test e2e", "content": "contenu", "type": "INFO"})
        check("POST /admin/announcements -> 201", r.status_code == 201, f"got {r.status_code} {r.text[:120]}")
        ann_id = r.json().get("id") if r.status_code == 201 else None
        if ann_id:
            r = await c.delete(f"/api/admin/announcements/{ann_id}", headers=h)
            check("DELETE annonce test -> 200", r.status_code == 200)

        # 10. CRUD admin sans token -> 401
        r = await c.post("/api/admin/announcements", json={"title": "x", "content": "y"})
        check("POST /admin/announcements sans token -> 401", r.status_code == 401, f"got {r.status_code}")

        # 11. FAQ admin
        r = await c.get("/api/admin/faq", headers=h)
        check("GET /admin/faq -> 200", r.status_code == 200, f"got {r.status_code}")

        print(f"\n==== RESULTAT : {ok} OK / {fail} FAIL ====")
        sys.exit(1 if fail else 0)


asyncio.run(main())
