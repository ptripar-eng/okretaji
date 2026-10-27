"""Najava sljedeće utrke Formule 1 za Okretaje -> race.json.

Podaci: Jolpica F1 API (nasljednik Ergasta) i obrisi staza iz
github.com/bacinger/f1-circuits (MIT licenca).
"""
import json, math, os, sys
from datetime import datetime, timezone
import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "race.json")
API = "https://api.jolpi.ca/ergast/f1"
GEO = "https://raw.githubusercontent.com/bacinger/f1-circuits/master/f1-circuits.geojson"
UA = "Okretaji/1.0 (https://okretaji.com)"
TODAY = datetime.now(timezone.utc).date().isoformat()


def get(url):
    r = requests.get(url, headers={"User-Agent": UA}, timeout=25)
    r.raise_for_status()
    return r.json()


def name(d):
    return f"{d.get('givenName','')} {d.get('familyName','')}".strip()


def next_race():
    races = get(f"{API}/current/races/?format=json&limit=40")["MRData"]["RaceTable"]["Races"]
    for r in races:
        if r["date"] >= TODAY:
            return r, len(races)
    return None, len(races)


def past_winners(circuit_id, n=5):
    url = f"{API}/circuits/{circuit_id}/results/1/?format=json&limit=100"
    d = get(url)["MRData"]
    total = int(d.get("total", 0))
    if total > 100:
        d = get(url + f"&offset={total-100}")["MRData"]
    races = d["RaceTable"]["Races"]
    out = []
    for r in races[-n:][::-1]:
        res = r["Results"][0]
        out.append({"season": r["season"], "driver": name(res["Driver"]),
                    "team": res["Constructor"]["name"], "grid": res.get("grid")})
    return out


def standings():
    lists = get(f"{API}/current/driverstandings/?format=json")["MRData"]["StandingsTable"]["StandingsLists"]
    if not lists:
        return [], None
    rows = []
    for s in lists[0]["DriverStandings"][:10]:
        rows.append({"pos": int(s["position"]), "driver": name(s["Driver"]),
                     "code": s["Driver"].get("code", ""),
                     "team": s["Constructors"][0]["name"] if s.get("Constructors") else "",
                     "points": float(s["points"]), "wins": int(s["wins"])})
    return rows, lists[0].get("round")


def track_outline(lat, lon):
    try:
        feats = get(GEO)["features"]
    except Exception as e:
        print(f"  ! obrisi staza: {e}", file=sys.stderr)
        return None
    best, bd = None, 1e9
    for f in feats:
        coords = f["geometry"]["coordinates"]
        if f["geometry"]["type"] == "MultiLineString":
            coords = coords[0]
        cx = sum(c[0] for c in coords) / len(coords)
        cy = sum(c[1] for c in coords) / len(coords)
        dist = math.hypot((cx - lon) * math.cos(math.radians(lat)), cy - lat)
        if dist < bd:
            best, bd, best_coords = f, dist, coords
    if not best or bd > 0.1:      # ~10 km – nema obrisa za ovu stazu
        return None
    k = math.cos(math.radians(lat))
    pts = [((c[0]) * k, -c[1]) for c in best_coords]
    minx, maxx = min(p[0] for p in pts), max(p[0] for p in pts)
    miny, maxy = min(p[1] for p in pts), max(p[1] for p in pts)
    scale = 900 / max(maxx - minx, maxy - miny)
    w, h = (maxx - minx) * scale, (maxy - miny) * scale
    ox, oy = (1000 - w) / 2, (1000 - h) / 2
    xy = [((p[0] - minx) * scale + ox, (p[1] - miny) * scale + oy) for p in pts]
    path = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in xy) + " Z"
    p = best["properties"]
    return {"path": path, "start": [round(xy[0][0], 1), round(xy[0][1], 1)],
            "length_m": p.get("length"), "opened": p.get("opened"), "firstgp": p.get("firstgp"),
            "altitude": p.get("altitude")}


def main():
    try:
        race, total_rounds = next_race()
    except Exception as e:
        print(f"  ! kalendar: {e}", file=sys.stderr)
        return
    if not race:
        print("Nema više utrka ove sezone."); return
    c = race["Circuit"]; loc = c["Location"]
    lat, lon = float(loc["lat"]), float(loc["long"])
    out = {
        "updated": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        "season": race["season"], "round": int(race["round"]), "rounds": total_rounds,
        "name": race["raceName"], "date": race["date"], "time": race.get("time"),
        "circuit": c["circuitName"], "locality": loc.get("locality"), "country": loc.get("country"),
        "sessions": {k: v for k, v in race.items() if isinstance(v, dict) and "date" in v},
    }
    for fn, key in ((past_winners, "winners"),):
        try:
            out[key] = fn(c["circuitId"])
        except Exception as e:
            print(f"  ! {key}: {e}", file=sys.stderr); out[key] = []
    try:
        out["standings"], out["standings_round"] = standings()
    except Exception as e:
        print(f"  ! poredak: {e}", file=sys.stderr); out["standings"] = []
    out["track"] = track_outline(lat, lon)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"Najava: {out['name']} ({out['date']}), pobjednika: {len(out['winners'])}, "
          f"poredak: {len(out['standings'])}, staza: {'da' if out['track'] else 'ne'}")


if __name__ == "__main__":
    main()
