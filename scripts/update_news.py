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

def summarize(title, description, category):
    # Use only the supplied RSS title and description. Never invent missing facts.
    fallback = re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", description or "")).strip()
    fallback = fallback[:500]
    if not API_KEY:
        return {"t": title, "s": fallback or title}
    prompt = f"""Pišeš za regionalni portal Okretaji na razumljivom hrvatskom jeziku. Kategorija: {category}.
Koristi ISKLJUČIVO činjenice iz naslova i opisa RSS-a. Ne dodaj kontekst, uzroke, brojke, izjave ni detalje kojih ondje nema.
Vrati samo valjani JSON objekt s ključevima:
1) t: jasan naslov na hrvatskom, najviše 95 znakova
2) s: sažetak od 1–2 rečenice, približno 25–45 riječi, vlastitim riječima.
Ako opis ne sadrži dovoljno podataka, napiši kratak i oprezan sažetak bez nagađanja.
NASLOV: {title}
OPIS: {fallback}"""
    try:
        # Keep within typical free-tier request limits and never put the API key in the URL.
        time.sleep(4)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
        payload = {"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"responseMimeType":"application/json","temperature":0.1}}
        r = requests.post(url, headers={"x-goog-api-key": API_KEY}, json=payload, timeout=35)
        if r.status_code == 429:
            print("Gemini ograničenje zahtjeva (429); pokušavam još jednom nakon 15 sekundi.")
            time.sleep(15)
            r = requests.post(url, headers={"x-goog-api-key": API_KEY}, json=payload, timeout=35)
        r.raise_for_status()
        response_text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        data = json.loads(response_text[response_text.find("{"):response_text.rfind("}")+1])
        data = {
            "t": re.sub(r"\s+", " ", str(data.get("t", ""))).strip()[:140],
            "s": re.sub(r"\s+", " ", str(data.get("s", ""))).strip()[:500],
        }
        if not data["t"] or not data["s"]:
            raise ValueError("empty title or summary")
        return data
    except Exception as e:
        # Never print request URLs or exception text that could contain credentials.
        status = getattr(getattr(e, "response", None), "status_code", None)
        detail = f"HTTP {status}" if status else type(e).__name__
        print("Gemini sažetak nije uspio:", detail)
        return {"t": title, "s": fallback[:450] or title}

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
                dt = e.get("published_parsed") or e.get("updated_parsed")
                date = datetime.fromtimestamp(time.mktime(dt), timezone.utc) if dt else now
                if now-date > timedelta(days=max_age) or date-now > timedelta(days=1): continue
                source = feed.get("source","")
                if feed.get("use_item_source") and e.get("source"): source = e.source.get("title",source)
                candidates.append({"c":feed["cat"],"raw_t":title,"desc":desc,"src":source,"u":link,"date":date.isoformat(timespec="minutes"),"img_q":title[:100]})
        except Exception as e: print("Feed nije dostupan:",feed.get("url"),str(e)[:120])
    candidates.sort(key=lambda x:x["date"], reverse=True)
    counts, out = {}, []
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
        if prev.get("summary_version")==2 and prev.get("orig_t")==item["raw_t"] and prev.get("s"):
            summary={"t":prev.get("t", item["raw_t"]), "s":prev["s"]}
        else:
            # Regenerate legacy summaries once under the stricter no-invention prompt.
            summary=summarize(item["raw_t"],item["desc"],cat)
        record={k:item[k] for k in ("c","src","u","date","img_q")}
        record.update(summary)
        record["orig_t"]=item["raw_t"]
        record["summary_version"]=2
        record["hr"]=True
        out.append(record); counts[cat]=counts.get(cat,0)+1
    # Keep current articles if feeds temporarily fail, up to max age and 45 items.
    for item in old.values():
        if item.get("u") not in {x["u"] for x in out} and item.get("date","")[:10] >= (now-timedelta(days=max_age)).date().isoformat() and len(out)<45 and item.get("summary_version")==2:
            # Keep only articles already processed under the strict summary rules.
            item = {k:v for k,v in item.items() if k not in ("body", "conclusion")}
            out.append(item)
    out.sort(key=lambda x:x.get("date",""),reverse=True)
    today = now.date().isoformat()
    events = sorted((e for e in f1_schedule()+cfg.get("events",[]) if e.get("date","")>=today), key=lambda e:e["date"])[:6]
    with open(OUT,"w",encoding="utf-8") as f: json.dump({"updated":now.isoformat(timespec="minutes"),"items":out[:45],"schedule":events},f,ensure_ascii=False,indent=1)
    print(f"Okretaji: spremljeno {min(len(out),45)} vijesti iz {len(cfg.get('feeds',[]))} RSS izvora i {len(events)} nadolazećih događaja.")

if __name__ == "__main__": main()
