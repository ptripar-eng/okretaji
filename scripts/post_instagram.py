#!/usr/bin/env python3
"""Objavi jednu Okretaji vijest dnevno na Instagram (Meta Graph API).

Vizual je brendirana kartica (scripts/social_card.py), ne tuđa fotografija.
Instagram traži javni URL slike: kartica se sprema u social/cards/, commita i
pusha, a Meta je preuzima s raw.githubusercontent.com za taj commit.

Live objava: IG_DRY_RUN=0 te FB_PAGE_ID + FB_PAGE_TOKEN (token stranice ili
korisnički token administratora stranice). IG_USER_ID nije obavezan: ako ga
nema, dohvaća se s Facebook stranice (instagram_business_account).
"""
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

ROOT = Path(__file__).resolve().parent.parent
NEWS_PATH = ROOT / "news.json"
STATE_PATH = ROOT / "instagram_posted.json"
CARDS_DIR = ROOT / "social" / "cards"
REPO = os.getenv("GITHUB_REPOSITORY", "ptripar-eng/okretaji")
PAGE_ID = os.getenv("FB_PAGE_ID", "").strip()
TOKEN = (os.getenv("IG_ACCESS_TOKEN") or os.getenv("FB_PAGE_TOKEN") or "").strip()
USER_ID = os.getenv("IG_USER_ID", "").strip()
DRY_RUN = os.getenv("IG_DRY_RUN", "1").strip().lower() not in {"0", "false", "no"}
API_VERSION = os.getenv("IG_GRAPH_API_VERSION", "v24.0").strip()
API = f"https://graph.facebook.com/{API_VERSION}"
TZ = ZoneInfo("Europe/Zagreb")
DAILY_LIMIT = 1
TAGS = {
    "f1": "#F1 #Formula1",
    "motogp": "#MotoGP #Motorsport",
    "reli": "#WRC #Rally",
    "auto": "#Automobili #AutoMoto",
    "moto": "#Motocikli #Moto",
    "tech": "#Tehnologija #Tech",
    "energy": "#Energija #Tehnologija",
    "kaciga": "#IzaKacige #Motorsport",
}
PRIORITY = {"f1": 0, "motogp": 0, "kaciga": 0, "reli": 1, "moto": 1, "auto": 2, "tech": 3, "energy": 3}


def read_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def clean(value):
    return " ".join(str(value or "").split()).strip()


def usable_photo(article):
    image = article.get("img") or {}
    src = str(image.get("src") or "").strip()
    creator = str(image.get("by") or "").strip()
    license_name = str(image.get("lic") or "").strip().upper()
    link = str(image.get("link") or "").strip()
    try:
        width, height = int(image.get("width", 0)), int(image.get("height", 0))
        ratio = width / height if height else 0
    except (TypeError, ValueError, ZeroDivisionError):
        ratio = 0
    return (
        src.startswith("https://") and creator and link.startswith("https://")
        and (license_name.startswith("CC") or "PUBLIC DOMAIN" in license_name)
        and 0.8 <= ratio <= 1.91
    )


def caption(article):
    category = str(article.get("c") or "").lower()
    source = clean(article.get("src")) or "izvor"
    source_url = str(article.get("u") or "").strip()
    image = article.get("img") or {}
    photo_credit = f"📷 Foto: {image.get('by')} · {image.get('lic')} · {image.get('link')}"
    return (
        f"🏁 {clean(article.get('t'))}\n\n{clean(article.get('s'))}\n\n"
        "Pratite @okretaji za auto-moto sport, tehnologiju i energiju. "
        "Sve vijesti s poveznicama na izvore: okretaji.com (poveznica u profilu).\n\n"
        f"Izvor: {source} · {source_url}\n"
        f"{photo_credit}\n\n{TAGS.get(category, '#Okretaji #AutoMoto')} #Okretaji"
    )[:2200]


def choose_article(articles, state, now):
    history = state.get("items", []) if isinstance(state, dict) else []
    posted_urls = {x.get("url") for x in history}
    today = now.date().isoformat()
    if sum(1 for x in history if str(x.get("posted_at", ""))[:10] == today) >= DAILY_LIMIT:
        return None, "Dnevno ograničenje Instagram objava dosegnuto."
    candidates = []
    for item in articles:
        url = str(item.get("u") or "").strip()
        category = str(item.get("c") or "").lower()
        if not url.startswith("https://") or url in posted_urls:
            continue
        if not clean(item.get("t")) or not clean(item.get("s")) or category not in TAGS:
            continue
        if item.get("hr") is not True or item.get("summary_version") != 3:
            continue
        if not usable_photo(item):
            continue
        candidates.append(item)
    if not candidates:
        return None, "Nema novog članka za Instagram."
    candidates.sort(key=lambda x: str(x.get("date") or ""), reverse=True)
    candidates.sort(key=lambda x: PRIORITY.get(str(x.get("c") or "").lower(), 9))
    return candidates[0], "Odabran najnoviji članak najvišeg prioriteta."


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def api_post(endpoint, data):
    response = requests.post(f"{API}/{endpoint}", data=data, timeout=35)
    try:
        payload = response.json()
    except ValueError:
        payload = {"error": {"message": response.text[:400]}}
    if not response.ok or payload.get("error"):
        raise RuntimeError(json.dumps(payload.get("error", payload), ensure_ascii=False)[:800])
    return payload


def publish(user_id, token, image_url, text):
    container = api_post(f"{user_id}/media", {"image_url": image_url, "caption": text, "access_token": token})
    creation_id = container.get("id")
    if not creation_id:
        raise RuntimeError("Meta nije vratio ID Instagram medijskog spremnika.")
    status = ""
    for _ in range(10):
        time.sleep(3)
        payload = requests.get(
            f"{API}/{creation_id}", params={"fields": "status_code", "access_token": token}, timeout=20
        ).json()
        if payload.get("error"):
            raise RuntimeError(json.dumps(payload["error"], ensure_ascii=False)[:800])
        status = payload.get("status_code", "")
        if status == "FINISHED":
            break
        if status in {"ERROR", "EXPIRED"}:
            raise RuntimeError(f"Instagram medijski spremnik nije spreman: {status}")
    if status != "FINISHED":
        raise RuntimeError(f"Instagram spremnik nije spreman nakon čekanja: {status or 'nepoznat status'}")
    result = api_post(f"{user_id}/media_publish", {"creation_id": creation_id, "access_token": token})
    if not result.get("id"):
        raise RuntimeError("Meta nije vratila ID objavljene Instagram objave.")
    return result["id"]


def main():
    news = read_json(NEWS_PATH, {})
    articles = news.get("items", []) if isinstance(news, dict) else []
    state = read_json(STATE_PATH, {"items": []})
    article, reason = choose_article(articles, state, datetime.now(TZ))
    print(f"Instagram | mode={'DRY_RUN' if DRY_RUN else 'LIVE'} | {reason}")
    if not article:
        return
    text = caption(article)
    print("Odabran članak:", article.get("t", ""))
    print("Opis:", text)
    if DRY_RUN:
        print("DRY_RUN: objava nije poslana i članak nije označen kao objavljen.")
        return
    if not PAGE_ID or not TOKEN:
        raise SystemExit("LIVE mode zahtijeva FB_PAGE_ID i FB_PAGE_TOKEN u GitHub Secrets.")

    from meta_token import resolve_page_token
    token = resolve_page_token(API, PAGE_ID, TOKEN)
    user_id = USER_ID
    if not user_id:
        page = requests.get(
            f"{API}/{PAGE_ID}", params={"fields": "instagram_business_account", "access_token": token}, timeout=20
        ).json()
        user_id = (page.get("instagram_business_account") or {}).get("id", "")
        if not user_id:
            raise RuntimeError("Facebook stranica nema povezan Instagram poslovni račun.")
    image_url = article["img"]["src"]
    media_id = publish(user_id, token, image_url, text)
    state.setdefault("items", []).append({
        "url": article["u"],
        "posted_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "post_id": media_id,
        "image_url": image_url,
        "title": article.get("t", ""),
        "category": article.get("c", ""),
    })
    state["items"] = state["items"][-500:]
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Instagram objavljeno. Meta media ID:", media_id)


if __name__ == "__main__":
    main()
