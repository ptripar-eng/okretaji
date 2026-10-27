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
    fallback = re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", description or "")).strip()
    fallback = fallback[:650]
    if not API_KEY:
        return {"t":title, "s":fallback or title, "body":fallback or title, "conclusion":"Ovo je kratki sažetak dostupnih informacija. Za dodatne detalje provjerite navedeni izvor."}
    prompt = f"""Pišeš za regionalni portal Okretaji na razumljivom hrvatskom jeziku. Kategorija: {category}.
Na temelju ISKLJUČIVO podataka u naslovu i opisu napiši:
1) t: jasan naslov na hrvatskom, najviše 95 znakova
2) s: sažetak 1-2 rečenice, 30-45 riječi
3) body: prošireni sažetak od 70-110 riječi, bez izmišljanja podataka
4) conclusion: kratak zaključak od 1-2 rečenice, jasno označi što je poznato, a što još nije potvrđeno.
Vrati samo valjani JSON objekt s ključevima t,s,body,conclusion. Ne kopiraj rečenice doslovno. Ako nema dovoljno informacija, reci to.
NASLOV: {title}
OPIS: {fallback}"""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
        r = requests.post(url, json={"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"responseMimeType":"application/json","temperature":0.25}}, timeout=35)
        r.raise_for_status()
        text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        data = json.loads(text[text.find("{"):text.rfind("}")+1])
        for k,limit in (("t",140),("s",500),("body",1600),("conclusion",500)):
            data[k] = re.sub(r"\s+"," ",str(data.get(k,""))).strip()[:limit]
        if not data["t"] or not data["s"]: raise ValueError("empty summary")
        return data
    except Exception as e:
        print("Gemini sažetak nije uspio:", str(e)[:180])
        return {"t":title, "s":fallback[:450] or title, "body":fallback[:1200] or title, "conclusion":"Automatski zaključak nije dostupan jer izvor nije dao dovoljno podataka za pouzdanu procjenu."}

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
        # Preserve a previously generated, edited translation while its source item remains unchanged.
        if prev.get("orig_t")==item["raw_t"] and prev.get("s") and prev.get("body") and prev.get("conclusion"):
            summary={k:prev[k] for k in ("t","s","body","conclusion")}
        else:
            summary=summarize(item["raw_t"],item["desc"],cat)
        record={k:item[k] for k in ("c","src","u","date","img_q")}
        record.update(summary)
        record["orig_t"]=item["raw_t"]
        record["hr"]=True
        out.append(record); counts[cat]=counts.get(cat,0)+1
    # Keep current articles if feeds temporarily fail, up to max age and 45 items.
    for item in old.values():
        if item.get("u") not in {x["u"] for x in out} and item.get("date","")[:10] >= (now-timedelta(days=max_age)).date().isoformat() and len(out)<45:
            out.append(item)
    out.sort(key=lambda x:x.get("date",""),reverse=True)
    with open(OUT,"w",encoding="utf-8") as f: json.dump({"updated":now.isoformat(timespec="minutes"),"items":out[:45]},f,ensure_ascii=False,indent=1)
    print(f"Okretaji: spremljeno {min(len(out),45)} vijesti iz {len(cfg.get('feeds',[]))} RSS izvora.")

if __name__ == "__main__": main()
