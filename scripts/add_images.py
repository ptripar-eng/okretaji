#!/usr/bin/env python3
"""Attach relevant, openly licensed images; never reuse generic photos across unrelated stories."""
import json
import os
import re
import time
import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEWS = os.path.join(ROOT, "news.json")
CACHE = os.path.join(ROOT, "images.json")
UA = "OkretajiBot/1.0 (+https://okretaji.com)"
STOP = {
    "about", "after", "again", "against", "among", "before", "being", "could",
    "from", "have", "into", "just", "more", "over", "than", "that", "their",
    "there", "these", "this", "through", "under", "very", "with", "will", "would",
    "and", "the", "for", "are", "was", "were", "has", "his", "her", "its",
    "new", "next", "one", "two", "how", "why", "what", "when", "where",
}
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": UA, "Accept": "application/json"})


def terms(text):
    words = re.findall(r"[a-z0-9]{3,}", str(text or "").lower())
    return {w for w in words if w not in STOP and not w.isdigit()}


def metadata_text(item):
    title = item.get("title") or ""
    tags = item.get("tags") or []
    if isinstance(tags, list):
        tags = " ".join(str(t.get("name", "")) if isinstance(t, dict) else str(t) for t in tags)
    return title + " " + str(tags)


def relevant(image, story_terms):
    image_terms = terms(metadata_text(image))
    overlap = story_terms & image_terms
    # Require at least two meaningful shared terms. One generic word ("car", "racing")
    # is not enough to imply that a photo depicts the particular story.
    return len(overlap) >= 2, sorted(overlap)


def search_image(query, used_ids):
    """Return a licensed image only when its title/tags match the actual story."""
    story_terms = terms(query)
    if len(story_terms) < 2:
        return None
    try:
        r = SESSION.get(
            "https://api.openverse.org/v1/images/",
            params={"q": query, "page_size": 20, "license_type": "commercial"},
            timeout=(4, 10),
        )
        if not r.ok:
            print("Openverse nije vratio uspješan odgovor:", r.status_code)
            return None
        for x in r.json().get("results", []):
            image_id = x.get("id")
            src = x.get("thumbnail") or x.get("url")
            creator = x.get("creator")
            lic = x.get("license")
            link = x.get("foreign_landing_url") or x.get("url")
            if not image_id or image_id in used_ids:
                continue
            if not (src and src.startswith("https://") and creator and lic and link):
                continue
            ok, matched = relevant(x, story_terms)
            if not ok:
                continue
            return {
                "id": image_id,
                "src": src,
                "by": creator,
                "lic": str(lic).upper().replace("CC", "CC "),
                "link": link,
                "illustrative": True,
                "match_terms": matched,
            }
    except (requests.RequestException, ValueError, TypeError) as e:
        print("Openverse pretraga nije uspjela:", type(e).__name__)
    return None


def main():
    with open(NEWS, encoding="utf-8") as f:
        data = json.load(f)
    try:
        with open(CACHE, encoding="utf-8") as f:
            cache = json.load(f)
    except (OSError, ValueError):
        cache = {}

    items = data.get("items", [])
    used_ids = set()
    changed = 0
    for item in items:
        url = item.get("u", "")
        query = (item.get("img_q") or item.get("orig_t") or item.get("t") or "").strip()
        story_terms = terms(query)

        # Do not keep old generic/category photos or cache entries without proof of relevance.
        current = item.get("img")
        if current:
            valid_terms = set(current.get("match_terms") or [])
            if current.get("id") and len(valid_terms & story_terms) >= 2 and current.get("id") not in used_ids:
                used_ids.add(current["id"])
                continue
            item.pop("img", None)

        cached = cache.get(url)
        if isinstance(cached, dict) and cached.get("src"):
            ok, matched = relevant(
                {"title": cached.get("title", ""), "tags": cached.get("match_terms", [])},
                story_terms,
            )
            if cached.get("id") not in used_ids and ok and cached.get("match_terms"):
                item["img"] = cached
                used_ids.add(cached["id"])
                continue

        chosen = search_image(query, used_ids) if query else None
        if chosen:
            # Store the query/title to allow future cache validation.
            chosen["title"] = query
            item["img"] = chosen
            cache[url] = chosen
            used_ids.add(chosen["id"])
            changed += 1
        else:
            # No generic photo fallback: the site will show its branded placeholder.
            cache.pop(url, None)
        time.sleep(0.3)

    with open(NEWS, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=1)

    total = sum(bool(x.get("img", {}).get("src")) for x in items)
    unique = len({x.get("img", {}).get("id") for x in items if x.get("img", {}).get("id")})
    print(f"Fotografije: {total}/{len(items)} vijesti imaju relevantnu sliku s atribucijom.")
    print(f"Jedinstvene slike: {unique}; nove dodane u ovom ciklusu: {changed}.")
    print("Za vijesti bez relevantne slike prikazuje se brendirana ilustracija Okretaji.")


if __name__ == "__main__":
    main()
