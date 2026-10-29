#!/usr/bin/env python3
"""Attach openly licensed illustrative photos, with reliable category-level fallback."""
import json, os, time, requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEWS = os.path.join(ROOT, "news.json")
CACHE = os.path.join(ROOT, "images.json")
UA = "OkretajiBot/1.0 (+https://okretaji.com)"
CATEGORY_QUERY = {
    "f1": "Formula One racing car circuit",
    "motogp": "MotoGP motorcycle racing",
    "reli": "World Rally Championship rally car",
    "auto": "sports car automobile",
    "moto": "motorcycle road riding",
    "tech": "technology computer electronics",
    "energy": "solar panels wind turbines renewable energy",
    "kaciga": "Formula One driver racing",
}
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": UA, "Accept": "application/json"})


def search_image(query):
    """Return only an image with a source, creator, license and attribution page."""
    try:
        r = SESSION.get(
            "https://api.openverse.org/v1/images/",
            params={"q": query, "page_size": 8, "license_type": "commercial"},
            timeout=(4, 8),
        )
        if not r.ok:
            print("Openverse nije vratio uspješan odgovor:", r.status_code)
            return None
        for x in r.json().get("results", []):
            src = x.get("thumbnail") or x.get("url")
            creator = x.get("creator")
            lic = x.get("license")
            link = x.get("foreign_landing_url") or x.get("url")
            if src and src.startswith("https://") and creator and lic and link:
                return {
                    "id": x.get("id"),
                    "src": src,
                    "by": creator,
                    "lic": str(lic).upper().replace("CC", "CC "),
                    "link": link,
                    "illustrative": True,
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

    # Preserve cached category images so one successful broad search can help
    # other stories without repeating the same API request for every card.
    category_cache = cache.get("__category_images__", {})
    changed = 0
    items = data.get("items", [])

    for n in items:
        url = n.get("u", "")
        if not url or n.get("img", {}).get("src"):
            continue
        cached = cache.get(url)
        if isinstance(cached, dict) and cached.get("src"):
            n["img"] = cached
            continue

        query = (n.get("img_q") or n.get("t") or "").strip()
        chosen = search_image(query) if query else None
        if not chosen:
            cat = n.get("c", "")
            chosen = category_cache.get(cat)
            if not chosen:
                chosen = search_image(CATEGORY_QUERY.get(cat, "automotive motorsport technology"))
                if chosen:
                    category_cache[cat] = chosen
        if chosen:
            n["img"] = chosen
            cache[url] = chosen
            changed += 1
        # Do not cache failures: a later scheduled run should retry.
        time.sleep(0.25)

    cache["__category_images__"] = category_cache
    with open(NEWS, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=1)

    total = sum(bool(x.get("img", {}).get("src")) for x in items)
    print(f"Fotografije: {total}/{len(items)} vijesti imaju atribuiranu sliku; novo dodano {changed}.")
    print("Vijesti bez fotografije prikazuju ugrađenu ilustraciju Okretaji.")


if __name__ == "__main__":
    main()
