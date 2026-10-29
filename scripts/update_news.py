#!/usr/bin/env python3
"""Fetch automotive/sport/technology/energy RSS items and write concise Croatian summaries."""
import json, os, re, time
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
import feedparser, requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEEDS = os.path.join(ROOT, "feeds.json")
OUT = os.path.join(ROOT, "news.json")
API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
UA = "OkretajiBot/1.0 (+https://okretaji.com)"
CATS = {"f1":"F1", "motogp":"MotoGP", "reli":"reli", "auto":"auto", "moto":"moto", "tech":"tech", "energy":"energy", "kaciga":"kaciga"}

def clean_url(url):
    p = urlparse(url or "")
    q = [(k,v) for k,v in parse_qsl(p.query) if not k.lower().startswith("utm_") and k.lower() not in {"ref","fbclid","gclid"}]
    return urlunparse((p.scheme,p.netloc,p.path.rstrip("/"),p.params,urlencode(q), ""))

def likely_croatian(text):
    """Conservative language check used to preserve already edited Croatian summaries."""
    words = re.findall(r"[a-zčćđšž]+", (text or "").lower())
    hr = {"je","su","u","na","za","od","do","koji","koja","koje","što","prema","nakon","novi","novog","godine","vozač","utrke","motor","model","može","zbog","više","kao","nije","ima","imao","imaju","predstavlja","vraća","tijekom","među","godini","između"}
    en = {"the","and","is","are","with","from","after","new","will","has","have","could","its","their","than","for","to","of","in","on","as","by","this","that","more","over","around","about"}
    h = sum(w in hr for w in words)
    e = sum(w in en for w in words)
    return h > 0 and h >= e

def summarize(title, description, category):
    """Create a concise Croatian summary. Failed AI requests are retried on the next run."""
    from html import unescape
    source_context = unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", description or ""))).strip()
    fallback = source_context[:500]
    if not API_KEY:
        print("Gemini ključ nije postavljen; preskačem vijest bez hrvatskog sažetka.")
        return {"t": title, "s": fallback or title, "_ok": False}
    prompt = f"""Pišeš za regionalni portal Okretaji na prirodnom, gramatički ispravnom hrvatskom jeziku.
Koristi ISKLJUČIVO provjerljive činjenice iz naslova, RSS opisa i teksta izvornog članka koji je priložen kao kontekst. Ne dodaj uzroke, brojke, izjave ni detalje kojih u izvoru nema.
Napiši vlastitim riječima; ne kopiraj rečenice, ne koristi duge citate i ne stvaraj članak koji oponaša izvor. Ako je naslov na engleskom, prevedi ga na hrvatski. Vrati samo valjani JSON objekt:
1) t: jasan naslov na hrvatskom, najviše 95 znakova
2) s: sažetak od 1–2 rečenice, približno 25–45 riječi, vlastitim riječima.
Ako izvori ne sadrže dovoljno podataka, sažmi samo ono što je potvrđeno. Poveznica na izvor ostaje obavezna.
NASLOV: {title}
IZVORNI OPIS ILI TEKST: {source_context[:7500]}"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    payload = {"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"responseMimeType":"application/json","temperature":0.1}}
    # Keep below typical free-tier request rates; never put the API key in a URL.
    time.sleep(7)
    for attempt in range(2):
        try:
            r = requests.post(url, headers={"x-goog-api-key": API_KEY}, json=payload, timeout=12)
            if r.status_code == 429:
                print("Gemini ograničenje zahtjeva (429); vijest će se pokušati ponovno u sljedećem ciklusu.")
                return {"t": title, "s": fallback or title, "_ok": False}
            r.raise_for_status()
            response_text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
            data = json.loads(response_text[response_text.find("{"):response_text.rfind("}")+1])
            result = {
                "t": re.sub(r"\s+", " ", str(data.get("t", ""))).strip()[:140],
                "s": re.sub(r"\s+", " ", str(data.get("s", ""))).strip()[:500],
            }
            if not result["t"] or not result["s"]:
                raise ValueError("empty title or summary")
            result["_ok"] = True
            return result
        except requests.exceptions.ReadTimeout:
            if attempt == 0:
                print("Gemini je prekoračio vrijeme čekanja; ponavljam zahtjev jednom.")
                time.sleep(3)
                continue
            print("Gemini nije odgovorio nakon ponovnog pokušaja; vijest će se pokušati ponovno u sljedećem ciklusu.")
        except Exception as e:
            status = getattr(getattr(e, "response", None), "status_code", None)
            print("Gemini sažetak nije uspio:", f"HTTP {status}" if status else type(e).__name__)
            break
    return {"t": title, "s": fallback or title, "_ok": False}

def read_article(url):
    """Read a limited number of linked publisher articles for context; never republish their text."""
    try:
        import trafilatura
        response = requests.get(url, headers={"User-Agent": UA}, timeout=(4, 8), allow_redirects=True)
        if response.status_code != 200 or "text/html" not in response.headers.get("Content-Type", "").lower():
            return ""
        extracted = trafilatura.extract(
            response.text,
            include_comments=False,
            include_tables=False,
            favor_precision=True,
        ) or ""
        return re.sub(r"\s+", " ", extracted).strip()[:6000]
    except Exception as e:
        print("Puni tekst izvora nije dostupan; koristim RSS opis:", type(e).__name__)
        return ""

def f1_schedule():
    """F1 kalendar s Jolpica F1 API-ja za blok 'Nadolazeće utrke'."""
    try:
        r = requests.get("https://api.jolpi.ca/ergast/f1/current/races/?format=json&limit=40", headers={"User-Agent":UA}, timeout=20)
        r.raise_for_status()
        races = r.json()["MRData"]["RaceTable"]["Races"]
    except Exception as e:
        print("F1 kalendar nije dostupan:", str(e)[:120])
        return []
    out = []
    for race in races:
        loc = race.get("Circuit",{}).get("Location",{})
        out.append({"date":race["date"], "title":"F1 – "+race["raceName"].replace("Grand Prix","GP"), "note":", ".join(x for x in [loc.get("locality"),loc.get("country")] if x)})
    return out

def main():
    cfg = json.load(open(FEEDS, encoding="utf-8"))
    now = datetime.now(timezone.utc)
    max_age = int(cfg.get("max_age_days", 7))
    per_cat = int(cfg.get("max_per_category", 4))
    candidates, seen = [], set()
    # Google News can return unrelated stories for broad personality searches.
    # Keep the "Iza kacige" section tied to actual motorsport people/topics.
    kaciga_relevance = ("bottas", "verstappen", "hamilton", "leclerc", "norris", "alonso", "antonelli", "piastri", "marquez", "márquez", "stoner", "rossi", "ricciardo", "horner", "webber", "bagnaia", "martin", "tiffany cromwell", "f1", "formula 1", "formula one", "motogp", "red bull", "ferrari", "racing", "motorsport", "grand prix", "le mans", "wrc", "rally", "dakar", "vozač", "vozači", "utrka", "utrke")
    for feed in cfg.get("feeds", []):
        try:
            parsed = feedparser.parse(feed["url"], request_headers={"User-Agent":UA})
            if getattr(parsed, "bozo", False) and not parsed.entries: print("RSS greška:",feed["url"]); continue
            for e in parsed.entries[:18]:
                link = clean_url(e.get("link",""))
                if not link or link in seen: continue
                seen.add(link)
                title = re.sub(r"\s+"," ",e.get("title","")).strip()
                desc = e.get("summary","") or e.get("description","")
                if not title: continue
                if feed.get("cat") == "kaciga" and not any(term in title.lower() for term in kaciga_relevance):
                    print("Preskačem nepovezanu vijest u rubrici Iza kacige:", title[:100])
                    continue
                dt = e.get("published_parsed") or e.get("updated_parsed")
                date = datetime.fromtimestamp(time.mktime(dt), timezone.utc) if dt else now
                if now-date > timedelta(days=max_age) or date-now > timedelta(days=1): continue
                source = feed.get("source","")
                if feed.get("use_item_source") and e.get("source"): source = e.source.get("title",source)
                candidates.append({"c":feed["cat"],"raw_t":title,"desc":desc,"src":source,"u":link,"date":date.isoformat(timespec="minutes"),"img_q":title[:100]})
        except Exception as e: print("Feed nije dostupan:",feed.get("url"),str(e)[:120])
    candidates.sort(key=lambda x:x["date"], reverse=True)
    counts, out = {}, []
    full_articles_read = 0
    max_full_articles_per_run = 12
    old = {}
    if os.path.exists(OUT):
        try: old={x.get("u"):x for x in json.load(open(OUT,encoding="utf-8")).get("items",[])}
        except Exception: pass
    for item in candidates:
        cat=item["c"]
        if counts.get(cat,0)>=per_cat: continue
        prev=old.get(item["u"],{})
        # Preserve an existing title/summary while the source title is unchanged.
        # Legacy expanded body/conclusion fields are intentionally not carried forward.
        if prev.get("summary_version") in (2, 3) and prev.get("orig_t")==item["raw_t"] and prev.get("s") and (prev.get("summary_version")==3 or likely_croatian(prev.get("t", "") + " " + prev.get("s", ""))):
            summary={"t":prev.get("t", item["raw_t"]), "s":prev["s"]}
        else:
            # Read the linked publisher article for richer context, but cap requests per run.
            # The generated output remains a short original summary with the source link attached.
            context = item["desc"]
            if full_articles_read < max_full_articles_per_run:
                full_articles_read += 1  # Count attempts too, so blocked sites cannot trigger unlimited requests.
                full_text = read_article(item["u"])
                if full_text:
                    context = "RSS OPIS:\n" + str(item["desc"])[:1500] + "\n\nTEKST IZVORNOG ČLANKA (samo za provjeru činjenica):\n" + full_text
            # Regenerate legacy summaries once under the stricter no-invention prompt.
            summary=summarize(item["raw_t"],context,cat)
            if not summary.pop("_ok", False):
                # Do not publish an English RSS fallback as if it were an edited Croatian summary.
                if prev.get("summary_version")==3 and prev.get("s"):
                    summary={"t":prev.get("t", item["raw_t"]), "s":prev["s"]}
                else:
                    continue
        record={k:item[k] for k in ("c","src","u","date","img_q")}
        record.update(summary)
        record["orig_t"]=item["raw_t"]
        record["summary_version"]=3
        record["hr"]=True
        out.append(record); counts[cat]=counts.get(cat,0)+1
    # Keep current articles if feeds temporarily fail, up to max age and 45 items.
    for item in old.values():
        if item.get("c") == "kaciga" and not any(term in (item.get("orig_t") or item.get("t") or "").lower() for term in kaciga_relevance):
            continue
        if item.get("u") not in {x["u"] for x in out} and item.get("date","")[:10] >= (now-timedelta(days=max_age)).date().isoformat() and len(out)<45 and item.get("summary_version")==3:
            # Keep only articles already processed under the strict summary rules.
            item = {k:v for k,v in item.items() if k not in ("body", "conclusion")}
            out.append(item)
    out.sort(key=lambda x:x.get("date",""),reverse=True)
    today = now.date().isoformat()
    events = sorted((e for e in f1_schedule()+cfg.get("events",[]) if e.get("date","")>=today), key=lambda e:e["date"])[:6]
    with open(OUT,"w",encoding="utf-8") as f: json.dump({"updated":now.isoformat(timespec="minutes"),"items":out[:45],"schedule":events},f,ensure_ascii=False,indent=1)
    print(f"Okretaji: spremljeno {min(len(out),45)} vijesti iz {len(cfg.get('feeds',[]))} RSS izvora i {len(events)} nadolazećih događaja.")

if __name__ == "__main__": main()
