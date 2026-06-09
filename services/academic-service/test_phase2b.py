"""Test e2e Partie 2-bis : upload, departements, clubs, FAQ seed, prof modifiable."""
import asyncio, base64, sys
sys.stdout.reconfigure(encoding="utf-8")
import httpx
from app.main import app

ADMIN = {"email": "admin@fsbm.ac.ma", "password": "Admin@FSBM2026"}
PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGIAAQAABQABDQottAAAAABJRU5ErkJggg==")


async def main():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        ok = 0; fail = 0
        def check(name, cond, extra=""):
            nonlocal ok, fail
            if cond: ok += 1; print(f"  [OK] {name}")
            else: fail += 1; print(f"  [FAIL] {name} {extra}")

        token = (await c.post("/api/auth/login", json=ADMIN)).json()["access_token"]
        h = {"Authorization": f"Bearer {token}"}

        # 1. UPLOAD image
        r = await c.post("/api/admin/upload", headers=h,
                         files={"file": ("p.png", PNG, "image/png")})
        check("upload PNG -> 200", r.status_code == 200, f"{r.status_code} {r.text[:120]}")
        up = r.json() if r.status_code == 200 else {}
        check("upload renvoie url + kind=image", up.get("kind") == "image" and "url" in up)
        fname = up.get("filename")

        # 2. Fichier servi en statique
        if fname:
            r = await c.get(f"/uploads/{fname}")
            check("GET /uploads/<file> -> 200", r.status_code == 200, f"{r.status_code}")

        # 3. Upload type interdit
        r = await c.post("/api/admin/upload", headers=h,
                         files={"file": ("x.exe", b"MZ", "application/octet-stream")})
        check("upload .exe rejete -> 400", r.status_code == 400, f"{r.status_code}")

        # 4. DEPARTEMENT create/update/delete (avec logo)
        r = await c.post("/api/admin/departments", headers=h,
                         json={"code": "TEST_DEP", "name": "Dept Test", "logo_url": up.get("url")})
        check("POST departement -> 201", r.status_code == 201, f"{r.status_code} {r.text[:120]}")
        dep_id = r.json().get("id") if r.status_code == 201 else None
        if dep_id:
            r = await c.put(f"/api/admin/departments/{dep_id}", headers=h, json={"name": "Dept Modifie"})
            check("PUT departement -> 200", r.status_code == 200)
            r = await c.delete(f"/api/admin/departments/{dep_id}", headers=h)
            check("DELETE departement -> 200", r.status_code == 200)

        # 5. CLUB create/list/update/delete
        r = await c.post("/api/admin/clubs", headers=h,
                         json={"name": "Club Test", "category": "TECHNIQUE", "logo_url": up.get("url")})
        check("POST club -> 201", r.status_code == 201, f"{r.status_code} {r.text[:120]}")
        club_id = r.json().get("id") if r.status_code == 201 else None
        r = await c.get("/api/admin/clubs", headers=h)
        check("GET /admin/clubs -> 200 + liste", r.status_code == 200 and len(r.json()) >= 1)
        if club_id:
            r = await c.put(f"/api/admin/clubs/{club_id}", headers=h, json={"members_count": 42})
            check("PUT club -> 200", r.status_code == 200)
            await c.delete(f"/api/admin/clubs/{club_id}", headers=h)

        # 6. PROFESSEUR modifiable (le point signale par l'utilisateur)
        r = await c.get("/api/professors", params={"page": 1, "page_size": 1})
        items = r.json().get("items", [])
        check("liste profs non vide", len(items) >= 1, f"count={len(items)}")
        if items:
            pid = items[0]["id"]
            r = await c.put(f"/api/admin/professors/{pid}", headers=h,
                            json={"specialty": "Specialite Test E2E", "photo_url": up.get("url")})
            check("PUT professeur -> 200 (MODIFIABLE)", r.status_code == 200, f"{r.status_code} {r.text[:150]}")
            check("photo_url enregistree", r.json().get("photo_url") == up.get("url") if r.status_code == 200 else False)

        # 7. FAQ seedees + modifiables
        r = await c.get("/api/admin/faq", headers=h)
        faqs = r.json() if r.status_code == 200 else []
        check("FAQ seedees presentes (>=15)", len(faqs) >= 15, f"count={len(faqs)}")
        if faqs:
            fid = faqs[0]["id"]
            r = await c.put(f"/api/admin/faq/{fid}", headers=h, json={"answer": "Reponse modifiee e2e"})
            check("PUT FAQ -> 200", r.status_code == 200)

        # 8. Annonce avec image + PDF
        r = await c.post("/api/admin/announcements", headers=h, json={
            "title": "Annonce media", "content": "Contenu de test e2e", "type": "INFO",
            "image_url": up.get("url"), "attachment_url": up.get("url")})
        check("POST annonce avec media -> 201", r.status_code == 201, f"{r.status_code} {r.text[:120]}")
        if r.status_code == 201:
            aid = r.json()["id"]
            check("attachment_url enregistre", r.json().get("attachment_url") == up.get("url"))
            await c.delete(f"/api/admin/announcements/{aid}", headers=h)

        print(f"\n==== RESULTAT : {ok} OK / {fail} FAIL ====")
        sys.exit(1 if fail else 0)


asyncio.run(main())
