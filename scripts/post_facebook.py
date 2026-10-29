#!/usr/bin/env python3
"""Prepare or publish a small number of useful, varied Okretaji Facebook posts.

Safety: DRY_RUN defaults to 1. Live mode requires DRY_RUN=0 and valid Meta Page credentials.
"""
import json
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

ROOT = Path(__file__).resolve().parent.parent
NEWS_PATH = ROOT / "news.json"
POSTED_PATH = ROOT / "posted.json"
PAGE_ID = os.getenv("FB_PAGE_ID", "").strip()
PAGE_TOKEN = os.getenv("FB_PAGE_TOKEN", "").strip()
DRY_RUN = os.getenv("DRY_RUN", "1").strip().lower() not in {"0", "false", "no"}
API_VERSION = os.getenv("FB_GRAPH_API_VERSION", "v24.0").strip()
DAILY_LIMIT = 2
# Najviše jedna objava po pokretanju: dvije dnevne objave razmaknute su barem 6 sati.
MAX_PER_RUN = max(1, int(os.getenv("FB_MAX_PER_RUN", "1") or "1"))
TZ = ZoneInfo("Europe/Zagreb")

CATEGORY = {
    "f1": {
        "tag": "#Formula1 #F1",
        "question": "Što vi mislite o ovoj priči — je li ovo dobar potez?",
        "follow": "Pratite Okretaje za najvažnije vijesti iz Formule 1.",
    },
    "motogp": {
        "tag": "#MotoGP #Motorsport",
        "question": "Kako vi gledate na ovu odluku? Napišite svoje mišljenje.",
        "follow": "Pratite Okretaje za MotoGP novosti i utrke.",
    },
    "reli": {
        "tag": "#WRC #Rally",
        "question": "Koji vozač ili posada bi po vama mogli iznenaditi?",
        "follow": "Pratite Okretaje za rally i regionalni motosport.",
    },
    "moto": {
        "tag": "#Motocikli #Moto",
        "question": "Biste li vi odabrali ovakav motocikl? Zašto?",
        "follow": "Pratite Okretaje za moto novosti i teme za vozače.",
    },
    "auto": {
        "tag": "#Automobili #AutoMoto",
        "question": "Što mislite — dobar izbor ili biste odabrali nešto drugo?",
        "follow": "Pratite Okretaje za automobilske novosti i praktične usporedbe.",
    },
    "tech": {
        "tag": "#Tehnologija #Tech",
        "question": "Je li ovo stvarni napredak ili više marketinška priča?",
        "follow": "Pratite Okretaje za tehnologiju koja mijenja promet i svakodnevicu.",
    },
    "energy": {
        "tag": "#Energija #Tehnologija",
        "question": "Što mislite — može li ovo donijeti mjerljivu promjenu?",
        "follow": "Pratite Okretaje za tehnologiju i energetiku bez uljepšavanja.",
    },
    "kaciga": {
        "tag": "#Motorsport #IzaKacige",
        "question": "Koju biste priču izvan staze voljeli pročitati sljedeću?",
        "follow": "Pratite Okretaje za priče iz svijeta vozača i motosporta.",
    },
}
SPORT = {"f1", "motogp", "reli", "moto"}


def read_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def make_message(article):
    category = str(article.get("c") or "").lower()
    meta = CATEGORY.get(category, {
        "tag": "#Okretaji #AutoMoto",
        "question": "Što vi mislite? Napišite svoje mišljenje.",
        "follow": "Pratite Okretaje za nove priče iz svijeta vozila i tehnologije.",
    })
    title = " ".join(str(article.get("t") or "").split()).strip()
    summary = " ".join(str(article.get("s") or "").split()).strip()
    source = str(article.get("src") or "izvor").strip()
    source_url = (article.get("u") or "").strip()
    return (
        f"🏁 {title}\n\n{summary}\n\n"
        f"💬 {meta['question']}\n\n"
        f"👉 {meta['follow']}\n"
        f"🌐 Sve novosti: https://okretaji.com/#novosti\n"
        f"Izvor: {source} — {source_url}\n\n"
        f"{meta['tag']} #Okretaji"
    )


def choose_candidates(candidates, slots):
    """Favor one fresh motorsport item and one different category each day."""
    remaining = sorted(candidates, key=lambda x: x["date"], reverse=True)
    selected = []
    if slots <= 0:
        return selected

    sports = [x for x in remaining if x["category"] in SPORT]
    first = sports[0] if sports else (remaining[0] if remaining else None)
    if first:
        selected.append(first)
        remaining.remove(first)

    while remaining and len(selected) < slots:
        used_categories = {x["category"] for x in selected}
        different = [x for x in remaining if x["category"] not in used_categories]
        non_sports = [x for x in different if x["category"] not in SPORT]
        pool = non_sports or different or remaining
        choice = pool[0]
        selected.append(choice)
        remaining.remove(choice)
    return selected


def publish(article):
    """Objavi fotografiju s brendiranom karticom; bez kartice objavi poveznicu."""
    base = f"https://graph.facebook.com/{API_VERSION}/{PAGE_ID}"
    try:
        import tempfile
        from social_card import make_card
        card = Path(tempfile.mkdtemp()) / "okretaji-card.jpg"
        make_card(article["raw"], card)
    except Exception as exc:  # Pillow ili fontovi nedostaju
        print("Kartica nije izrađena, objavljujem poveznicu:", type(exc).__name__, exc)
        return requests.post(
            f"{base}/feed",
            data={
                "message": article["message"],
                "link": "https://okretaji.com/#novosti",
                "access_token": PAGE_TOKEN,
            },
            timeout=30,
        )
    print("Kartica:", card)
    with open(card, "rb") as fh:
        return requests.post(
            f"{base}/photos",
            data={
                "caption": article["message"],
                "published": "true",
                "access_token": PAGE_TOKEN,
            },
            files={"source": ("okretaji-card.jpg", fh, "image/jpeg")},
            timeout=60,
        )


def main():
    news = read_json(NEWS_PATH, {})
    articles = news.get("items", []) if isinstance(news, dict) else []
    state = read_json(POSTED_PATH, {"items": []})
    posted = state.get("items", []) if isinstance(state, dict) else []
    posted_urls = {x.get("url") for x in posted if x.get("url")}
    now = datetime.now(TZ)
    today = now.date().isoformat()
    already_today = sum(
        1 for x in posted
        if x.get("posted_at") and x["posted_at"][:10] == today
    )
    slots = max(0, DAILY_LIMIT - already_today)
    if not articles:
        print("DRY_RUN=" + str(int(DRY_RUN)) + " | news.json nema članaka; nema objave.")
        return

    candidates = []
    for article in articles:
        url = (article.get("u") or "").strip()
        title = " ".join(str(article.get("t") or "").split()).strip()
        summary = " ".join(str(article.get("s") or "").split()).strip()
        category = str(article.get("c") or "").lower()
        if not url.startswith("https://") or not title or not summary:
            continue
        if url in posted_urls or category not in CATEGORY:
            continue
        if article.get("hr") is not True or article.get("summary_version") != 3:
            continue
        candidates.append({
            "url": url,
            "title": title,
            "summary": summary,
            "category": category,
            "source": str(article.get("src") or "izvor").strip(),
            "date": str(article.get("date") or ""),
            "message": make_message(article),
            "raw": article,
        })

    selected = choose_candidates(candidates, min(slots, MAX_PER_RUN))
    print(
        f"Facebook plan | mode={'DRY_RUN' if DRY_RUN else 'LIVE'} | "
        f"today={today} | already_today={already_today} | "
        f"daily_limit={DAILY_LIMIT} | candidates={len(candidates)} | selected={len(selected)}"
    )
    if not selected:
        print("Nema novih članaka za objavu ili je dnevno ograničenje dosegnuto.")
        return

    if not DRY_RUN and (not PAGE_ID or not PAGE_TOKEN):
        raise SystemExit("LIVE mode zahtijeva FB_PAGE_ID i FB_PAGE_TOKEN u GitHub Secrets.")

    newly_posted = []
    for article in selected:
        print(f"\n[{article['category'].upper()}] {article['title']}")
        print(article["message"])
        if DRY_RUN:
            print("DRY_RUN: objava nije poslana i članak nije označen kao objavljen.")
            continue

        response = publish(article)
        try:
            payload = response.json()
        except ValueError:
            payload = {"error": {"message": response.text[:500]}}
        post_id = payload.get("post_id") or payload.get("id")
        if not response.ok or payload.get("error") or not post_id:
            raise RuntimeError(
                "Meta Graph API nije prihvatio objavu: "
                + json.dumps(payload.get("error", payload), ensure_ascii=False)[:700]
            )
        print("Objavljeno. Meta post ID:", post_id)
        newly_posted.append({
            "url": article["url"],
            "posted_at": datetime.now(TZ).isoformat(timespec="seconds"),
            "post_id": post_id,
            "category": article["category"],
            "title": article["title"],
        })
        # Persist each successful post immediately so a later API error cannot
        # cause already-published content to be posted again on the next run.
        state["items"] = (posted + newly_posted)[-500:]
        POSTED_PATH.write_text(
            json.dumps(state, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Spremljena evidencija: {len(newly_posted)} novih objava.")


if __name__ == "__main__":
    main()
