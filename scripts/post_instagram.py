#!/usr/bin/env python3
"""Publish one carefully selected Okretaji image post to Instagram via Meta Graph API.

Live publishing requires IG_USER_ID + IG_ACCESS_TOKEN and DRY_RUN=0.
The Instagram account must be professional and connected to a Facebook Page.
"""
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

ROOT = Path(__file__).resolve().parent.parent
NEWS_PATH = ROOT / "news.json"
STATE_PATH = ROOT / "instagram_posted.json"
USER_ID = os.getenv("IG_USER_ID", "").strip()
TOKEN = os.getenv("IG_ACCESS_TOKEN", "").strip()
DRY_RUN = os.getenv("IG_DRY_RUN", "1").strip().lower() not in {"0", "false", "no"}
API_VERSION = os.getenv("IG_GRAPH_API_VERSION", "v24.0").strip()
TZ = ZoneInfo("Europe/Zagreb")
DAILY_LIMIT = 1
API = f"https://graph.facebook.com/{API_VERSION}"


def read_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def normalized_url(value):
    return re.sub(r"[?#].*$", "", str(value or "").strip()).rstrip("/").lower()


def caption(article):
    title = " ".join(str(article.get("t") or "").split()).strip()
    summary = " ".join(str(article.get("s") or "").split()).strip()
    category = str(article.get("c") or "").lower()
    tags = {
        "f1": "#F1 #Formula1",
        "motogp": "#MotoGP #Motorsport",
        "reli": "#WRC #Rally",
        "auto": "#Automobili #AutoMoto",
        "moto": "#Motocikli #Moto",
        "tech": "#Tehnologija #Tech",
        "energy": "#Energija #Tehnologija",
        "kaciga": "#IzaKacige #Motorsport",
    }.get(category, "#Okretaji #AutoMoto")
    img = article.get("img") or {}
    credit = ""
    if img.get("by"):
        credit = f"\n\nFoto: {img['by']}"
        if img.get("lic"):
            credit += f" · {img['lic']}"
        if img.get("link"):
            credit += f" · {img['link']}"
    source = str(article.get("src") or "Izvor").strip()
    source_url = str(article.get("u") or "").strip()
    return (
        f"🏁 {title}\n\n{summary}\n\n"
        "Pratite @okretaji za auto-moto sport, tehnologiju i energiju. "
        "Cijelu priču i izvor pronađite na okretaji.com.\n\n"
        f"Izvor: {source} · {source_url}{credit}\n\n{tags} #Okretaji"
    )[:2200]


def choose_article(articles, state, now):
    history = state.get("items", []) if isinstance(state, dict) else []
    posted_urls = {x.get("url") for x in history}
    posted_images = {
        normalized_url(x.get("image_url"))
        for x in history if x.get("image_url")
    }
    today = now.date().isoformat()
    today_count = sum(
        1 for x in history
        if x.get("posted_at", "")[:10] == today
    )
    if today_count >= DAILY_LIMIT:
        return None, "Dnevno ograničenje Instagram objava dosegnuto."

    category_priority = {"f1": 0, "motogp": 0, "reli": 1, "moto": 1, "auto": 2, "tech": 3, "energy": 3, "kaciga": 0}
    candidates = []
    seen_images = set()
    for item in articles:
        url = str(item.get("u") or "").strip()
        image = item.get("img") or {}
        image_url = str(image.get("src") or "").strip()
        title = " ".join(str(item.get("t") or "").split()).strip()
        summary = " ".join(str(item.get("s") or "").split()).strip()
        if not url.startswith("https://") or not title or not summary:
            continue
        if item.get("hr") is not True or item.get("summary_version") != 3:
            continue
        if not image_url.startswith("https://") or url in posted_urls:
            continue
        image_key = normalized_url(image_url)
        if not image_key or image_key in posted_images or image_key in seen_images:
            continue
        # Only publish images with attribution; this also reduces copyright risk.
        if not image.get("by") or not image.get("lic") or not image.get("link"):
            continue
        seen_images.add(image_key)
        candidates.append((category_priority.get(str(item.get("c") or "").lower(), 9), item))
    if not candidates:
        return None, "Nema novog članka s jedinstvenom fotografijom i potpunom atribucijom."
    candidates.sort(key=lambda pair: (pair[0], str(pair[1].get("date") or "")), reverse=False)
    # Within the selected category rank, prefer the newest article.
    best_rank = candidates[0][0]
    ranked = [item for rank, item in candidates if rank == best_rank]
    ranked.sort(key=lambda item: str(item.get("date") or ""), reverse=True)
    return ranked[0], "Odabran je najnoviji članak s jedinstvenom fotografijom."


def api_post(endpoint, data):
    response = requests.post(f"{API}/{endpoint}", data=data, timeout=35)
    try:
        payload = response.json()
    except ValueError:
        payload = {"error": {"message": response.text[:400]}}
    if not response.ok or payload.get("error"):
        raise RuntimeError(json.dumps(payload.get("error", payload), ensure_ascii=False)[:800])
    return payload


def publish(article):
    image_url = article["img"]["src"]
    # Meta needs a publicly reachable image URL; the URL is not downloaded by this script.
    container = api_post(f"{USER_ID}/media", {
        "image_url": image_url,
        "caption": caption(article),
        "access_token": TOKEN,
    })
    creation_id = container.get("id")
    if not creation_id:
        raise RuntimeError("Meta nije vratio ID Instagram medijskog spremnika.")
    # Containers may need a moment to process; poll status briefly before publishing.
    status = ""
    for _ in range(6):
        time.sleep(3)
        response = requests.get(
            f"{API}/{creation_id}",
            params={"fields": "status_code", "access_token": TOKEN},
            timeout=20,
        )
        payload = response.json()
        if not response.ok or payload.get("error"):
            raise RuntimeError(json.dumps(payload.get("error", payload), ensure_ascii=False)[:800])
        status = payload.get("status_code", "")
        if status == "FINISHED":
            break
        if status in {"ERROR", "EXPIRED"}:
            raise RuntimeError(f"Instagram medijski spremnik nije spreman: {status}")
    if status != "FINISHED":
        raise RuntimeError(f"Instagram medijski spremnik nije spreman nakon čekanja: {status or 'nepoznat status'}")
    result = api_post(f"{USER_ID}/media_publish", {
        "creation_id": creation_id,
        "access_token": TOKEN,
    })
    if not result.get("id"):
        raise RuntimeError("Meta nije vratila ID objavljene Instagram objave.")
    return result["id"]


def main():
    news = read_json(NEWS_PATH, {})
    articles = news.get("items", []) if isinstance(news, dict) else []
    state = read_json(STATE_PATH, {"items": []})
    now = datetime.now(TZ)
    article, reason = choose_article(articles, state, now)
    print(f"Instagram | mode={'DRY_RUN' if DRY_RUN else 'LIVE'} | {reason}")
    if not article:
        return
    print("Odabran članak:", article.get("t", ""))
    print("Fotografija:", (article.get("img") or {}).get("src", ""))
    print("Opis:", caption(article))
    if DRY_RUN:
        print("DRY_RUN: objava nije poslana i članak nije označen kao objavljen.")
        return
    if not USER_ID or not TOKEN:
        raise SystemExit("LIVE mode zahtijeva IG_USER_ID i IG_ACCESS_TOKEN u GitHub Secrets.")
    post_id = publish(article)
    state.setdefault("items", []).append({
        "url": article["u"],
        "posted_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "post_id": post_id,
        "image_url": article["img"]["src"],
        "title": article["t"],
        "category": article.get("c", ""),
    })
    state["items"] = state["items"][-500:]
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Instagram objavljeno. Meta media ID:", post_id)


if __name__ == "__main__":
    main()
