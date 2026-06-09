"""
Web fetcher pour récupérer en direct les actualités FSBM.

Architecture (Phase actuelle) :
  1. Source PRIMAIRE  : academic-service (annonces + événements de la base locale).
                        C'est la source de vérité pour notre plateforme.
  2. Source SECONDAIRE : tentative de scraping fsbm.ma/news (SPA JS — souvent vide).
  3. Source FACEBOOK  : tentative de scraping FB mobile (très restrictif).
  4. Toujours : liens directs vers fsbm.ma/news et facebook.com/FSBMUH2C

Cache TTL de 5 minutes pour éviter de marteler les sources.
"""

from __future__ import annotations
import re
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

import httpx
from bs4 import BeautifulSoup


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


@dataclass
class NewsItem:
    """Une actualité récupérée."""
    title: str
    url: str = ""
    excerpt: str = ""
    date: Optional[str] = None
    image_url: Optional[str] = None
    source: str = "local"      # local | fsbm.ma | facebook
    type: str = "INFO"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class CachedResult:
    items: list[NewsItem]
    fetched_at: float


class WebFetcher:
    """Récupère et agrège les actualités FSBM depuis plusieurs sources."""

    CACHE_TTL = 5 * 60   # 5 minutes
    FSBM_NEWS_URL    = "https://www.fsbm.ma/news"
    FSBM_HOME_URL    = "https://www.fsbm.ma"
    FACEBOOK_URL     = "https://www.facebook.com/FSBMUH2C"
    FACEBOOK_MOBILE  = "https://m.facebook.com/FSBMUH2C/"

    def __init__(self, academic_service_url: str = "http://localhost:5002"):
        self.academic_service_url = academic_service_url.rstrip("/")
        self._cache: dict[str, CachedResult] = {}

    # ─── Public API ───────────────────────────────────────────────────────────

    async def get_news(self, source: str = "all", limit: int = 8) -> dict:
        """
        Renvoie les dernières actualités, agrégées.
        Source: 'all' | 'local' | 'fsbm' | 'facebook'
        """
        all_items: list[NewsItem] = []
        sources_status = {}

        # 1. Source PRIMAIRE : notre base via academic-service
        if source in ("all", "local"):
            try:
                local = await self._fetch_from_academic_service()
                all_items.extend(local)
                sources_status["local_db"] = {"ok": True, "count": len(local)}
            except Exception as e:
                sources_status["local_db"] = {"ok": False, "error": str(e)[:120]}

        # 2. Source SECONDAIRE : fsbm.ma (souvent vide car SPA JS)
        if source in ("all", "fsbm"):
            try:
                fsbm = await self._fetch_fsbm_news()
                all_items.extend(fsbm)
                sources_status["fsbm.ma"] = {
                    "ok": True, "count": len(fsbm),
                    "note": ("Site est une SPA JS — contenu rendu côté client. "
                             "Visitez le site pour les news complètes.") if not fsbm else None,
                }
            except Exception as e:
                sources_status["fsbm.ma"] = {"ok": False, "error": str(e)[:120]}

        # 3. Source FACEBOOK : lien direct (scraping bloqué)
        if source in ("all", "facebook"):
            try:
                fb = await self._fetch_facebook()
                all_items.extend(fb)
                sources_status["facebook"] = {"ok": True, "count": len(fb)}
            except Exception as e:
                sources_status["facebook"] = {"ok": False, "error": str(e)[:120]}

        # Dédupliquer + limiter
        seen_titles = set()
        deduped = []
        for it in all_items:
            key = it.title[:80].lower()
            if key not in seen_titles:
                seen_titles.add(key)
                deduped.append(it)
        deduped = deduped[:limit]

        return {
            "fetched_at": datetime.utcnow().isoformat() + "Z",
            "total": len(deduped),
            "sources": sources_status,
            "items": [it.to_dict() for it in deduped],
            "official_links": {
                "fsbm_news":  self.FSBM_NEWS_URL,
                "fsbm_home":  self.FSBM_HOME_URL,
                "facebook":   self.FACEBOOK_URL,
            },
        }

    # ─── Source 1 : academic-service (LOCAL = source de vérité) ──────────────

    async def _fetch_from_academic_service(self) -> list[NewsItem]:
        """Récupère annonces + événements depuis notre academic-service."""
        cached = self._get_cached("local_db")
        if cached is not None:
            return cached

        items: list[NewsItem] = []
        async with httpx.AsyncClient(timeout=5.0,
                                     headers={"User-Agent": "FSBM-Chatbot/3.0"}) as client:
            # Annonces
            try:
                r = await client.get(f"{self.academic_service_url}/api/announcements",
                                     params={"limit": 5})
                if r.status_code == 200:
                    for a in r.json():
                        items.append(NewsItem(
                            title=a.get("title", "(sans titre)"),
                            excerpt=a.get("content", "")[:300],
                            date=a.get("published_at", "")[:10] if a.get("published_at") else None,
                            type=a.get("type", "INFO"),
                            source="local",
                        ))
            except Exception:
                pass

            # Événements
            try:
                r = await client.get(f"{self.academic_service_url}/api/events",
                                     params={"upcoming_only": True})
                if r.status_code == 200:
                    for e in r.json()[:3]:
                        items.append(NewsItem(
                            title=f"🎉 {e.get('title', '(événement)')}",
                            excerpt=e.get("description", "")[:300],
                            date=e.get("start_date", "")[:10] if e.get("start_date") else None,
                            type=e.get("event_type", "EVENT"),
                            source="local",
                        ))
            except Exception:
                pass

        self._set_cached("local_db", items)
        return items

    # ─── Source 2 : fsbm.ma/news (HTML scraping) ──────────────────────────────

    async def _fetch_fsbm_news(self) -> list[NewsItem]:
        """Tente de récupérer les actualités depuis fsbm.ma. Souvent vide (SPA)."""
        cached = self._get_cached("fsbm_news")
        if cached is not None:
            return cached

        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True,
                                     headers={"User-Agent": USER_AGENT}) as client:
            try:
                resp = await client.get(self.FSBM_NEWS_URL)
                resp.raise_for_status()
                html = resp.text
            except Exception:
                self._set_cached("fsbm_news", [])
                return []

        # Si HTML quasi vide (<5KB), c'est probablement une SPA → on ne tente pas
        if len(html) < 5000:
            self._set_cached("fsbm_news", [])
            return []

        soup = BeautifulSoup(html, "lxml")
        items: list[NewsItem] = []

        # Plusieurs sélecteurs en cascade
        for sel in ["article", ".post", ".news-item", ".entry",
                    ".elementor-post", ".wp-block-post"]:
            nodes = soup.select(sel)
            if nodes:
                for n in nodes[:10]:
                    items.append(self._extract_news_from_node(n))
                if items:
                    break

        # Fallback : tous les h2/h3 liens
        if not items:
            for h in soup.select("h2 a, h3 a")[:10]:
                title = h.get_text(strip=True)
                if title and len(title) > 8:
                    items.append(NewsItem(
                        title=title,
                        url=self._absolute_url(h.get("href", ""), self.FSBM_HOME_URL),
                        source="fsbm.ma",
                    ))

        items = [i for i in items if i.title and len(i.title) > 3]
        self._set_cached("fsbm_news", items)
        return items

    def _extract_news_from_node(self, node) -> NewsItem:
        title_el = (node.select_one("h2 a, h3 a, h1 a, .entry-title a, .post-title a")
                    or node.select_one("h2, h3, h1, .entry-title, .post-title"))
        title = title_el.get_text(strip=True) if title_el else ""

        link = node.select_one("h2 a, h3 a, h1 a, .entry-title a, .post-title a, a")
        url = link.get("href", "") if link else ""

        excerpt_el = node.select_one(".entry-content p, .excerpt, .post-excerpt p, p")
        excerpt = excerpt_el.get_text(" ", strip=True)[:280] if excerpt_el else ""

        date_el = node.select_one("time, .date, .post-date, .entry-date")
        date = date_el.get_text(strip=True) if date_el else None

        img = node.find("img")
        img_url = img.get("src") if img else None
        if img_url:
            img_url = self._absolute_url(img_url, self.FSBM_HOME_URL)

        return NewsItem(
            title=title,
            url=self._absolute_url(url, self.FSBM_HOME_URL),
            excerpt=excerpt,
            date=date,
            image_url=img_url,
            source="fsbm.ma",
        )

    # ─── Source 3 : Facebook (lien direct + tentative scraping mobile) ───────

    async def _fetch_facebook(self) -> list[NewsItem]:
        cached = self._get_cached("facebook")
        if cached is not None:
            return cached

        items: list[NewsItem] = []
        # Toujours fournir au moins le lien direct
        items.append(NewsItem(
            title="📘 Page Facebook officielle FSBM",
            url=self.FACEBOOK_URL,
            excerpt=("Pour les annonces les plus récentes, suivez la page Facebook officielle. "
                     "Facebook bloque le scraping automatique sans authentification."),
            source="facebook",
            type="LINK",
        ))

        # Tentative best-effort sur le mobile (souvent bloquée mais on essaie)
        try:
            async with httpx.AsyncClient(timeout=6.0, follow_redirects=True,
                                         headers={"User-Agent": USER_AGENT}) as client:
                resp = await client.get(self.FACEBOOK_MOBILE)
                if resp.status_code == 200 and len(resp.text) > 5000:
                    soup = BeautifulSoup(resp.text, "lxml")
                    for p in soup.select("div[data-ft], article")[:3]:
                        txt = p.get_text(" ", strip=True)
                        if txt and len(txt) > 30:
                            items.append(NewsItem(
                                title=txt[:120] + ("..." if len(txt) > 120 else ""),
                                url=self.FACEBOOK_URL,
                                excerpt=txt[:280],
                                source="facebook",
                                type="POST",
                            ))
        except Exception:
            pass

        self._set_cached("facebook", items)
        return items

    # ─── Helpers ──────────────────────────────────────────────────────────────

    def _get_cached(self, key: str) -> Optional[list[NewsItem]]:
        if key in self._cache:
            entry = self._cache[key]
            if time.time() - entry.fetched_at < self.CACHE_TTL:
                return entry.items
        return None

    def _set_cached(self, key: str, items: list[NewsItem]):
        self._cache[key] = CachedResult(items=items, fetched_at=time.time())

    @staticmethod
    def _absolute_url(href: str, base: str) -> str:
        if not href:
            return ""
        href = href.strip()
        if href.startswith(("http://", "https://")):
            return href
        if href.startswith("//"):
            return "https:" + href
        if href.startswith("/"):
            return base + href
        return base + "/" + href


# Singleton (sera initialisé proprement dans main.py avec l'URL du settings)
fetcher = WebFetcher()


def format_news_response(news_data: dict, lang: str = "fr") -> str:
    """Formate les news en texte humain pour le chatbot."""
    items = news_data.get("items", [])
    links = news_data.get("official_links", {})

    if not items:
        templates = {
            "fr": ("🔄 Aucune annonce trouvée pour le moment.\n\n"
                   "Sources officielles :\n• {fsbm}\n• {fb}"),
            "en": ("🔄 No news found at the moment.\n\n"
                   "Official sources:\n• {fsbm}\n• {fb}"),
            "darija": ("🔄 Ma kayna walou daba.\n\n"
                       "Sources officielles :\n• {fsbm}\n• {fb}"),
        }
        return templates.get(lang, templates["fr"]).format(
            fsbm=links.get("fsbm_news", ""), fb=links.get("facebook", "")
        )

    titles = {
        "fr": "📰 Dernières actualités FSBM :",
        "en": "📰 Latest FSBM news:",
        "darija": "📰 Akhir lkhbar dyal FSBM :",
    }
    lines = [titles.get(lang, titles["fr"]), ""]

    for i, it in enumerate(items[:6], 1):
        title = it.get("title", "(sans titre)")
        date = it.get("date", "")
        date_part = f" — {date}" if date else ""
        src = it.get("source", "local")
        src_emoji = {"local": "📋", "fsbm.ma": "🌐", "facebook": "📘"}.get(src, "•")
        lines.append(f"{src_emoji} **{title}**{date_part}")
        excerpt = (it.get("excerpt") or "")[:160]
        if excerpt:
            lines.append(f"   {excerpt}")
        lines.append("")

    footer = {
        "fr": f"\n🔗 Plus d'infos : {links.get('fsbm_news','')}  •  {links.get('facebook','')}",
        "en": f"\n🔗 More: {links.get('fsbm_news','')}  •  {links.get('facebook','')}",
        "darija": f"\n🔗 Lmazid : {links.get('fsbm_news','')}  •  {links.get('facebook','')}",
    }
    lines.append(footer.get(lang, footer["fr"]))
    return "\n".join(lines)
