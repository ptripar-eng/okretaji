#!/usr/bin/env python3
"""Validate news data and remove duplicate image assignments before publication."""
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent.parent
NEWS_PATH = ROOT / "news.json"


def image_key(value):
    value = str(value or "").strip()
    if not value:
        return ""
    parts = urlsplit(value)
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/"), "", ""))


def main():
    try:
        data = json.loads(NEWS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"GREŠKA: news.json nije moguće pročitati: {exc}")
    if not isinstance(data, dict) or not isinstance(data.get("items"), list):
        raise SystemExit("GREŠKA: news.json mora sadržavati polje items kao listu.")

    items = data["items"]
    seen_urls, seen_image_ids, seen_image_urls = set(), set(), set()
    duplicate_urls = 0
    removed_images = 0
    missing_sources = 0
    invalid_items = 0
    kept = []
    for item in items:
        if not isinstance(item, dict):
            invalid_items += 1
            continue
        url = str(item.get("u") or "").strip()
        title = str(item.get("t") or "").strip()
        summary = str(item.get("s") or "").strip()
        if not url.startswith("https://") or not title or not summary:
            invalid_items += 1
            continue
        if url in seen_urls:
            duplicate_urls += 1
            continue
        seen_urls.add(url)
        if not str(item.get("src") or "").strip():
            missing_sources += 1

        image = item.get("img")
        if isinstance(image, dict):
            image_id = str(image.get("id") or "").strip()
            src = image_key(image.get("src"))
            duplicated = (
                (image_id and image_id in seen_image_ids)
                or (src and src in seen_image_urls)
                or not str(image.get("src") or "").startswith("https://")
            )
            if duplicated:
                item.pop("img", None)
                removed_images += 1
            else:
                if image_id:
                    seen_image_ids.add(image_id)
                if src:
                    seen_image_urls.add(src)
        kept.append(item)

    data["items"] = kept
    NEWS_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Provjera vijesti: {len(kept)} valjanih članaka; uklonjeni duplikati članaka: {duplicate_urls}.")
    print(f"Uklonjene ponovljene/neispravne fotografije: {removed_images}; članci bez navedenog izvora: {missing_sources}.")
    if invalid_items:
        print(f"UPOZORENJE: preskočeni neispravni zapisi: {invalid_items}.")
    if len(kept) == 0:
        raise SystemExit("GREŠKA: nakon provjere nema valjanih članaka.")


if __name__ == "__main__":
    main()
