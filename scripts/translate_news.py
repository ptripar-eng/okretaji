#!/usr/bin/env python3
"""Iz news.json izradi news_en.json i news_de.json (naslov i sažetak prevodi Gemini).

Prijevodi se pamte u i18n/news-<jezik>.json (ključ = hrvatski naslov + sažetak), pa se
svaka vijest prevodi samo jednom. Vijest bez prijevoda ne prikazuje se na stranoj
inačici (umjesto da se prikaže na hrvatskom); pokušava se ponovno u sljedećem pokretanju.
"""
import json, os, re, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-lite-latest")
LANGS = {"en": "English (British spelling)", "de": "German"}
MAX_NEW = int(os.getenv("NEWS_TRANSLATE_MAX", "60"))

PROMPT = """Translate these Croatian motoring news headlines and summaries for the website Okretaji into {name}.
Return ONLY a JSON array with exactly {n} objects {{"t": ..., "s": ...}} in the same order.
Keep the meaning exactly; do not add facts, numbers or opinions. Natural news style, headline at most 95 characters.
Do not translate names of people, teams, brands, models or series. "VN" means Grand Prix (German: "Großer Preis").
INPUT:
{data}"""


def key(t, s):
    return (t or "").strip() + "\n" + (s or "").strip()


def gemini(batch, lang):
    import requests
    prompt = PROMPT.format(name=LANGS[lang], n=len(batch), data=json.dumps(batch, ensure_ascii=False))
    url = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent" % MODEL
    payload = {"contents": [{"parts": [{"text": prompt}]}],
               "generationConfig": {"responseMimeType": "application/json", "temperature": 0.1}}
    for attempt in range(3):
        try:
            r = requests.post(url, headers={"x-goog-api-key": API_KEY}, json=payload, timeout=90)
            if r.status_code == 429:
                time.sleep(30); continue
            r.raise_for_status()
            txt = r.json()["candidates"][0]["content"]["parts"][0]["text"]
            arr = json.loads(txt[txt.find("["):txt.rfind("]") + 1])
            if isinstance(arr, list) and len(arr) == len(batch):
                return arr
            print("Gemini vratio pogrešan broj prijevoda vijesti (%s)." % lang)
        except Exception as e:
            print("Gemini prijevod vijesti nije uspio:", type(e).__name__)
            time.sleep(5)
    return None


def main():
    src = json.load(open(os.path.join(ROOT, "news.json"), encoding="utf-8"))
    items = src.get("items", [])
    sched = src.get("schedule", [])
    for lang in LANGS:
        cpath = os.path.join(ROOT, "i18n", "news-%s.json" % lang)
        cache = json.load(open(cpath, encoding="utf-8")) if os.path.exists(cpath) else {}
        wanted = [{"t": i.get("t", ""), "s": i.get("s", "")} for i in items]
        wanted += [{"t": e.get("title", ""), "s": e.get("note", "")} for e in sched]
        missing, seen = [], set()
        for w in wanted:
            k = key(w["t"], w["s"])
            if k not in cache and k not in seen:
                missing.append(w); seen.add(k)
        missing = missing[:MAX_NEW]
        done = 0
        if missing and not API_KEY:
            print("%s: %d vijesti bez prijevoda, GEMINI_API_KEY nije postavljen." % (lang, len(missing)))
        elif missing:
            for b in range(0, len(missing), 15):
                batch = missing[b:b + 15]
                res = gemini(batch, lang)
                time.sleep(5)
                for w, r in zip(batch, res or []):
                    if isinstance(r, dict) and str(r.get("t", "")).strip() and (str(r.get("s", "")).strip() or not w["s"]):
                        cache[key(w["t"], w["s"])] = {"t": re.sub(r"\s+", " ", str(r["t"])).strip()[:140],
                                                     "s": re.sub(r"\s+", " ", str(r.get("s", ""))).strip()[:500]}
                        done += 1
        live = {key(w["t"], w["s"]) for w in wanted}
        cache = {k: v for k, v in cache.items() if k in live}
        os.makedirs(os.path.dirname(cpath), exist_ok=True)
        with open(cpath, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=0)
            f.write("\n")
        out_items = []
        for i in items:
            tr = cache.get(key(i.get("t"), i.get("s")))
            if tr:
                n = dict(i); n["t"], n["s"] = tr["t"], tr["s"]; n.pop("hr", None); n["lang"] = lang
                out_items.append(n)
        out_sched = []
        for e in sched:
            tr = cache.get(key(e.get("title"), e.get("note")))
            n = dict(e)
            if tr:
                n["title"], n["note"] = tr["t"], tr["s"] or e.get("note", "")
            out_sched.append(n)
        out = {"updated": src.get("updated"), "lang": lang, "items": out_items, "schedule": out_sched}
        with open(os.path.join(ROOT, "news_%s.json" % lang), "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print("%s: %d/%d vijesti prevedeno, %d novih prijevoda." % (lang, len(out_items), len(items), done))


if __name__ == "__main__":
    main()
