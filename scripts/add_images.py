"""Dodaje ilustrativne fotografije vijestima u news.json.

Fotografije se traže na Openverseu (openverse.org) – samo slike pod
Creative Commons licencama, uz autora i licencu koje stranica prikazuje.
Pronađene slike pamte se u images.json pa se ista vijest ne pretražuje ponovno.
"""
import json, os, re, sys, time
import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEWS = os.path.join(ROOT, "news.json")
CACHE = os.path.join(ROOT, "images.json")
UA = "Okretaji/1.0 (https://okretaji.com)"
API = "https://api.openverse.org/v1/images/"

FALLBACK_Q = {
    "f1": "formula one car", "motogp": "motogp motorcycle racing", "auto": "sports car",
    "moto": "motorcycle road", "reli": "rally car", "tech": "technology circuit board",
    "energy": "wind turbines solar",
}


def load(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def search(q, used):
    params = {"q": q, "page_size": 12, "mature": "false",
              "license_type": "all-cc", "aspect_ratio": "wide", "size": "large"}
    r = requests.get(API, params=params, headers={"User-Agent": UA}, timeout=20)
    r.raise_for_status()
    for res in r.json().get("results", []):
        if res.get("id") in used or not res.get("thumbnail"):
            continue
        lic = (res.get("license") or "").upper()
        ver = res.get("license_version") or ""
        lic = "CC0" if lic == "CC0" else ("Javno vlasništvo" if lic == "PDM" else f"CC {lic} {ver}".strip())
        return {
            "id": res["id"],
            "src": res["thumbnail"],
            "by": (res.get("creator") or "nepoznat autor")[:60],
            "lic": lic,
            "link": res.get("foreign_landing_url") or res.get("url"),
        }
    return None


def main():
    data = load(NEWS, None)
    if not data:
        print("news.json ne postoji"); return
    cache = load(CACHE, {})
    used = {v["id"] for v in cache.values() if v}
    found = calls = 0
    for it in data.get("items", []):
        key = it["u"].split("?")[0]
        if key in cache:
            if cache[key]:
                it["img"] = cache[key]
            continue
        if calls >= 25:      # pristojno prema besplatnom API-ju
            continue
        queries = [q for q in [it.get("img_q"), FALLBACK_Q.get(it["c"])] if q]
        img = None
        for q in queries:
            try:
                calls += 1
                img = search(q, used)
                time.sleep(1.2)
            except Exception as e:
                print(f"  ! Openverse ({q}): {e}", file=sys.stderr)
                break
            if img:
                break
        cache[key] = img
        if img:
            used.add(img["id"]); it["img"] = img; found += 1
    # stari unosi koji više nisu u vijestima brišu se iz predmemorije
    live = {it["u"].split("?")[0] for it in data.get("items", [])}
    cache = {k: v for k, v in cache.items() if k in live}
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=1)
    with open(NEWS, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"Fotografije: {found} novih, {calls} upita.")


if __name__ == "__main__":
    main()
