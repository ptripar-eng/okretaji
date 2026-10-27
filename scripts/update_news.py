"""Okretaji – automatsko osvježavanje vijesti.

Čita RSS izvore, dohvaća tekst članka kad je dostupan i uz Gemini izrađuje
hrvatski naslov, sažetak i originalno formuliranu vijest od 150–300 riječi.
Izvorni tekst koristi se samo kao kontekst; na portal se sprema AI-urednički tekst i poveznica na izvor.
"""
import html, json, os, re, sys, time, unicodedata
from datetime import datetime, timedelta, timezone

import feedparser
import requests
import trafilatura

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEEDS = os.path.join(ROOT, "feeds.json")
OUT = os.path.join(ROOT, "news.json")
UA = "Mozilla/5.0 (Okretaji news bot; +https://github.com)"
NOW = datetime.now(timezone.utc)


def clean(text, limit=260):
    text = html.unescape(re.sub(r"<[^>]+>", " ", text or ""))
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0] + "…"
    return text


def norm(title):
    # Normalizacija dijakritike pomaže ukloniti duplikate među izvorima.
    title = unicodedata.normalize("NFKD", title.lower())
    title = "".join(ch for ch in title if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]", "", title)[:80]


def load_old():
    try:
        with open(OUT, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"items": []}


def extract_rss_text(entry):
    """Uzima najdulji tekst koji RSS već isporučuje; bez dodatnog HTTP poziva."""
    chunks = []
    for part in entry.get("content", []) or []:
        value = clean(part.get("value", ""), 12000)
        if value:
            chunks.append(value)
    summary = clean(entry.get("summary") or entry.get("description"), 12000)
    if summary:
        chunks.append(summary)
    return max(chunks, key=len, default="")[:10000]


def extract_page_text(link, current_text=""):
    """Dohvaća stranicu samo za članke koji se stvarno šalju na AI obradu."""
    text = current_text or ""
    if len(text) >= 900:
        return text[:10000]
    try:
        response = requests.get(link, headers={"User-Agent": UA}, timeout=18)
        response.raise_for_status()
        extracted = trafilatura.extract(
            response.text, include_comments=False, include_tables=False,
            favor_precision=True, deduplicate=True
        )
        if extracted and len(extracted) > len(text):
            text = extracted
    except Exception as exc:
        print(f"  ! tekst članka nije dohvaćen ({link}): {exc}", file=sys.stderr)
    return clean(text, 10000)


def word_count(text):
    return len(re.findall(r"\b[\wÀ-ž]+(?:[’'-][\wÀ-ž]+)*\b", text or ""))


def fetch_feed(feed, max_age):
    items = []
    try:
        r = requests.get(feed["url"], headers={"User-Agent": UA}, timeout=20)
        r.raise_for_status()
        parsed = feedparser.parse(r.content)
    except Exception as e:
        print(f"  ! {feed['url']}: {e}", file=sys.stderr)
        return items
    for e in parsed.entries[:20]:
        t = e.get("published_parsed") or e.get("updated_parsed")
        when = datetime.fromtimestamp(time.mktime(t), timezone.utc) if t else NOW
        if NOW - when > timedelta(days=max_age) or when > NOW + timedelta(days=1):
            continue
        title = clean(e.get("title"), 200)
        link = e.get("link")
        if not title or not link:
            continue
        items.append({
            "c": feed["cat"], "t": title, "s": clean(e.get("summary") or e.get("description")),
            "src": feed["source"], "u": link, "date": when.isoformat(timespec="minutes"),
            "orig_t": title,
            "_source_text": extract_rss_text(e),
        })
    print(f"  {feed['source']} ({feed['cat']}): {len(items)}")
    return items


def call_gemini(prompt):
    """Gemini API; koristi se besplatna kvota ako je dostupna za projekt/model."""
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY nije postavljen")
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-lite")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    r = requests.post(
        url,
        headers={"x-goog-api-key": key, "content-type": "application/json"},
        json={
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "maxOutputTokens": 6500,
                             "responseMimeType": "application/json"},
        },
        timeout=120,
    )
    r.raise_for_status()
    data = r.json()
    return "".join(part.get("text", "") for part in data["candidates"][0]["content"]["parts"])


def call_claude(prompt):
    """Plaćena rezervna opcija; radi samo ako je izričito omogućena."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY nije postavljen za rezervnu opciju")
    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
        json={"model": os.environ.get("CLAUDE_MODEL", "claude-haiku-4-5"), "max_tokens": 6500,
              "messages": [{"role": "user", "content": prompt}]},
        timeout=120,
    )
    r.raise_for_status()
    return "".join(b.get("text", "") for b in r.json()["content"])


def translate(items, old_by_link):
    """Gemini prvo; Claude se može uključiti kao rezervna opcija uz izričitu postavku."""
    key = os.environ.get("GEMINI_API_KEY")
    todo = []
    for it in items:
        old = old_by_link.get(it["u"])
        if old and old.get("hr") and old.get("orig_t") == it["orig_t"] and (old.get("body") or old.get("nb")):
            it["t"], it["s"], it["hr"] = old["t"], old["s"], True
            if old.get("body"):
                it["body"] = old["body"]
            else:
                it["nb"] = True
            if old.get("img_q"):
                it["img_q"] = old["img_q"]
        else:
            # Zadrži stari prijevod sažetka, ali pokušaj nadograditi ga člankom ako ga nema.
            if old and old.get("hr") and old.get("orig_t") == it["orig_t"]:
                it["t"], it["s"] = old["t"], old["s"]
            todo.append(it)
    if not key or not todo:
        if not key:
            print("  ! GEMINI_API_KEY nije postavljen; nove vijesti ostaju bez AI prijevoda.")
        return
    # Ograničenja čuvaju trošak i sprječavaju da jedan workflow postane predug.
    if len(todo) > 12:
        print(f"  ! Za kontrolu troška prevodim 12 od {len(todo)} novih članaka u ovom pokretanju.")
        todo = todo[:12]
    # Manji batchovi smanjuju rizik od neispravnog JSON-a kod dugih članaka.
    for i in range(0, len(todo), 3):
        batch = todo[i:i + 3]
        payload = []
        for n, it in enumerate(batch):
            source_text = extract_page_text(it["u"], it.get("_source_text") or it.get("s"))
            payload.append({"id": n, "title": it["orig_t"], "rss_summary": it.get("s", ""), "source_text": source_text})
        prompt = (
            "Ti si hrvatski urednik regionalnog auto-moto, tehnologija i energetika portala Okretaji. "
            "Za svaku stavku napiši: t (precizan, prirodan hrvatski naslov), s (sažetak od 1–2 rečenice, do 45 riječi) "
            "i body (originalno formulirana kratka vijest od 150 do 300 riječi na hrvatskom jeziku). "
            "Koristi samo činjenice koje izričito podupire dostavljeni naslov, RSS sažetak i tekst izvora. "
            "Ne dodaj pozadinske tvrdnje, datume, brojke, citate ili zaključke koji nisu u izvoru. "
            "Ako izvor nema dovoljno podataka za vjerodostojan tekst od najmanje 150 riječi, vrati body kao prazan niz; "
            "nemoj umjetno produžavati tekst. Parafraziraj, ne prevodi rečenicu po rečenicu. "
            "Sačuvaj točne nazive vozača, timova, modela, tvrtki, jedinice i brojke. "
            "Ne izmišljaj citate. Bez senzacionalizma. Vrati SAMO JSON listu objekata "
            "{\"id\":0,\"t\":\"...\",\"s\":\"...\",\"body\":\"...\",\"q\":\"...\"}. "
            "Polje q je kratak ENGLESKI upit za pretragu ilustrativne fotografije (2–4 riječi, npr. ime vozača, tima, "
            "modela automobila ili motocikla, ili općeniti pojam poput 'rally car forest'). "
            "Ne uključuj URL-ove ni bibliografiju u body; izvorna poveznica prikazuje se zasebno.\n\n"
            + json.dumps(payload, ensure_ascii=False)
        )
        try:
            try:
                text = call_gemini(prompt)
                provider = "Gemini"
            except Exception as gemini_error:
                # Nikada ne pokreći plaćeni Claude fallback bez eksplicitne dozvole.
                if os.environ.get("ENABLE_CLAUDE_FALLBACK", "false").lower() == "true" and os.environ.get("ANTHROPIC_API_KEY"):
                    print(f"  ! Gemini nije uspio ({gemini_error}); pokušavam izričito omogućeni Claude fallback.", file=sys.stderr)
                    text = call_claude(prompt)
                    provider = "Claude fallback"
                else:
                    raise gemini_error
            text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip()).strip()
            rows = json.loads(text)
            print(f"  AI obrada uspješna: {provider}")
            for row in rows:
                idx = int(row["id"])
                if idx < 0 or idx >= len(batch):
                    continue
                it = batch[idx]
                title = clean(row.get("t", ""), 180)
                it["img_q"] = clean(row.get("q", ""), 60)
                summary = clean(row.get("s", ""), 400)
                body = (row.get("body") or "").strip()
                wc = word_count(body)
                if title and summary:
                    it["t"], it["s"], it["hr"] = title, summary, True
                if 150 <= wc <= 300:
                    it["body"] = body
                    it["body_words"] = wc
                else:
                    it.pop("body", None)
                    it["nb"] = True
                    it.pop("body_words", None)
                    print(f"  ! {it['src']}: nema dovoljno provjerljivih podataka za članak 150–300 riječi (dobiveno {wc}); prikazat će se samo sažetak.")
        except Exception as e:
            print(f"  ! AI obrada nije uspjela: {e}", file=sys.stderr)
    # Interni tekst izvora ne smije završiti u javnom news.json.
    for it in items:
        it.pop("_source_text", None)


def f1_schedule():
    try:
        r = requests.get("https://api.jolpi.ca/ergast/f1/current/races/?format=json",
                         headers={"User-Agent": UA}, timeout=20)
        r.raise_for_status()
        races = r.json()["MRData"]["RaceTable"]["Races"]
    except Exception as e:
        print(f"  ! F1 kalendar: {e}", file=sys.stderr)
        return []
    out = []
    for race in races:
        loc = race.get("Circuit", {}).get("Location", {})
        out.append({"date": race["date"], "title": "F1 – " + race["raceName"].replace("Grand Prix", "GP"),
                    "note": ", ".join(x for x in [loc.get("locality"), loc.get("country")] if x)})
    return out


def main():
    cfg = json.load(open(FEEDS, encoding="utf-8"))
    old = load_old()
    old_by_link = {it["u"]: it for it in old.get("items", [])}

    items, seen = [], set()
    for feed in cfg["feeds"]:
        for it in fetch_feed(feed, cfg.get("max_age_days", 10)):
            k = norm(it["t"])
            if it["u"] in seen or k in seen:
                continue
            seen.update([it["u"], k])
            items.append(it)

    if not items:
        print("Nijedan izvor nije vratio vijesti – news.json ostaje nepromijenjen.")
        return

    items.sort(key=lambda x: x["date"], reverse=True)
    per_cat, kept = {}, []
    for it in items:
        per_cat[it["c"]] = per_cat.get(it["c"], 0) + 1
        if per_cat[it["c"]] <= cfg.get("max_per_category", 9):
            kept.append(it)

    # glavna vijest: najnovija iz F1 ili MotoGP-a
    lead = next((it for it in kept if it["c"] in ("f1", "motogp")), kept[0])
    kept.remove(lead)
    kept.insert(0, lead)

    translate(kept, old_by_link)
    for it in kept:
        it.pop("_source_text", None)

    today = NOW.date().isoformat()
    events = [e for e in f1_schedule() + cfg.get("events", []) if e["date"] >= today]
    events.sort(key=lambda e: e["date"])

    data = {"updated": NOW.isoformat(timespec="minutes"), "items": kept, "schedule": events[:6]}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"Zapisano {len(kept)} vijesti i {len(events[:6])} događaja.")


if __name__ == "__main__":
    main()
