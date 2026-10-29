#!/usr/bin/env python3
"""Prepare or publish a small number of Okretaji Facebook page posts.

Safety: DRY_RUN defaults to 1. In dry-run mode this script never calls Meta's API
and never writes posted.json. Live mode requires explicit DRY_RUN=0 and credentials.
"""
import json
import os
from datetime import datetime, timezone
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
TZ = ZoneInfo("Europe/Zagreb")
PREFERRED = {"f1": 0, "motogp": 1, "moto": 2, "auto": 3, "tech": 4, "energy": 5}


def read_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default


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
        if not url.startswith(("https://", "http://")) or not title or not summary:
            continue
        if url in posted_urls:
            continue
        if category not in PREFERRED:
            continue
        source = str(article.get("src") or "izvor").strip()
        published = str(article.get("date") or "")
        message = (
            f"🏁 {title}\n\n{summary}\n\n"
            f"Više vijesti: https://okretaji.com/\n"
            f"Izvor: {source} — {url}"
        )
        candidates.append({
            "url": url, "title": title, "summary": summary,
            "category": category, "source": source, "date": published,
            "message": message,
        })

    # Newest first within each category, with F1/MotoGP/moto categories prioritized.
    candidates.sort(key=lambda x: x["date"], reverse=True)
    candidates.sort(key=lambda x: PREFERRED.get(x["category"], 99))
    selected = candidates[:slots]
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

        endpoint = f"https://graph.facebook.com/{API_VERSION}/{PAGE_ID}/feed"
        response = requests.post(
            endpoint,
            data={
                "message": article["message"],
                "link": "https://okretaji.com/",
                "access_token": PAGE_TOKEN,
            },
            timeout=30,
        )
        try:
            payload = response.json()
        except ValueError:
            payload = {"error": {"message": response.text[:500]}}
        if not response.ok or payload.get("error") or not payload.get("id"):
            raise RuntimeError(
                "Meta Graph API nije prihvatio objavu: "
                + json.dumps(payload.get("error", payload), ensure_ascii=False)[:700]
            )
        print("Objavljeno. Meta post ID:", payload["id"])
        newly_posted.append({
            "url": article["url"],
            "posted_at": datetime.now(TZ).isoformat(timespec="seconds"),
            "post_id": payload["id"],
            "category": article["category"],
            "title": article["title"],
        })

    if newly_posted:
        # Preserve history for duplicate protection, capped to the most recent 500 posts.
        state["items"] = (posted + newly_posted)[-500:]
        POSTED_PATH.write_text(
            json.dumps(state, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Spremljena evidencija: {len(newly_posted)} novih objava.")


if __name__ == "__main__":
    main()
