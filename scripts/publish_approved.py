#!/usr/bin/env python3
import json, os, re, subprocess, sys, time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import requests

ROOT=Path(__file__).resolve().parent.parent
QUEUE=ROOT/"social"/"queue.json"
CARDS=ROOT/"social"/"cards"
API="https://graph.facebook.com/"+os.getenv("META_GRAPH_VERSION","v24.0")
PAGE_ID=os.getenv("FB_PAGE_ID","").strip()
PAGE_TOKEN=os.getenv("FB_PAGE_TOKEN","").strip()
IG_USER=os.getenv("IG_USER_ID","").strip()
IG_TOKEN=os.getenv("IG_ACCESS_TOKEN","").strip()
REPO=os.getenv("GITHUB_REPOSITORY","ptripar-eng/okretaji")
TZ=ZoneInfo("Europe/Zagreb")

def git(*args):
    return subprocess.run(["git",*args],cwd=ROOT,check=True,capture_output=True,text=True).stdout.strip()

def save(data):
    QUEUE.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def api_post(path,data,files=None):
    r=requests.post(f"{API}/{path}",data=data,files=files,timeout=60)
    return api_payload(r)

def api_payload(response):
    try:
        payload = response.json()
    except ValueError:
        raise RuntimeError(f"Meta je vratila neispravan odgovor (HTTP {response.status_code}).") from None
    if not response.ok or payload.get("error"):
        error = payload.get("error", {})
        code = error.get("code")
        detail = f", Meta kod {code}" if isinstance(code, int) else ""
        raise RuntimeError(f"Meta zahtjev nije uspio (HTTP {response.status_code}{detail}).")
    return payload

def page_token():
    from meta_token import resolve_page_token
    try:
        return resolve_page_token(API,PAGE_ID,PAGE_TOKEN)
    except (RuntimeError, ValueError):
        raise RuntimeError("Meta token nije valjan ili ne daje pristup Facebook stranici.") from None

def make_card(item):
    from social_card import make_card as render
    article={"t":item["title"],"s":item.get("summary") or item["title"],"c":item.get("category","moto"),"src":"Okretaji"}
    name=f"{datetime.now(TZ):%Y%m%d-%H%M%S}-{item['slug']}.jpg"
    return render(article,CARDS/name)

def save_remote(data, message, image=None):
    save(data)
    paths = [QUEUE.relative_to(ROOT).as_posix()]
    if image is not None:
        paths.append(image.relative_to(ROOT).as_posix())
    git("add", "--", *paths)
    git("commit", "-m", message)
    try:
        git("push", "origin", "HEAD:refs/heads/main")
    except subprocess.CalledProcessError:
        raise RuntimeError("GitHub nije spremio stanje. Provjeri main i Meta Sadržaj prije novog pokušaja.") from None
    return git("rev-parse", "HEAD")

def public_card_url(path, revision):
    rel = path.relative_to(ROOT).as_posix()
    url = f"https://raw.githubusercontent.com/{REPO}/{revision}/{rel}"
    for _ in range(12):
        if requests.head(url, timeout=15).status_code == 200:
            return url
        time.sleep(3)
    raise RuntimeError("Javna URL adresa vizuala nije dostupna nakon commita.")

def publish_facebook(item,token,image):
    with open(image,"rb") as fh:
        result=api_post(f"{PAGE_ID}/photos",{"caption":item["facebook"],"published":"true","access_token":token},{"source":("okretaji.jpg",fh,"image/jpeg")})
    return result.get("post_id") or result.get("id")

def publish_instagram(item,token,user_id,image_url):
    container=api_post(f"{user_id}/media",{"image_url":image_url,"caption":item["instagram"],"access_token":token})
    cid=container.get("id")
    if not cid: raise RuntimeError("Meta nije vratila Instagram media container ID.")
    status=""
    for _ in range(12):
        time.sleep(3)
        r=requests.get(f"{API}/{cid}",params={"fields":"status_code","access_token":token},timeout=20)
        payload=api_payload(r)
        status=payload.get("status_code","")
        if status=="FINISHED": break
        if status in ("ERROR","EXPIRED"): raise RuntimeError("Instagram obrada nije uspjela: "+status)
    if status!="FINISHED": raise RuntimeError("Instagram vizual nije spreman: "+str(status))
    result=api_post(f"{user_id}/media_publish",{"creation_id":cid,"access_token":token})
    return result.get("id")

def main():
    if len(sys.argv) != 3:
        raise SystemExit("Upotreba: publish_approved.py <slug> <facebook|instagram|both>")
    slug, target = sys.argv[1:]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise SystemExit("Neispravna oznaka nacrta.")
    if target not in ("facebook", "instagram", "both"):
        raise SystemExit("Nepoznat kanal objave.")
    requested = ("facebook", "instagram") if target == "both" else (target,)

    data = json.loads(QUEUE.read_text(encoding="utf-8"))
    matches = [item for item in data.get("items", []) if item.get("slug") == slug]
    if len(matches) != 1:
        raise SystemExit("Očekuje se točno jedan nacrt s tom oznakom.")
    item = matches[0]
    if item.get("approved") is not True:
        raise SystemExit("Objava nije odobrena.")
    published = item.setdefault("published_to", {})
    pending = item.setdefault("publishing_to", {})
    if any(channel in pending for channel in requested):
        raise SystemExit("Prethodni pokušaj nema potvrđen ishod. Provjeri Meta Sadržaj prije novog pokušaja.")
    remaining = [channel for channel in requested if channel not in published]
    if not remaining:
        raise SystemExit("Odabrani kanali već imaju evidentiranu objavu.")
    if not item.get("title") or any(not item.get(channel) for channel in remaining):
        raise SystemExit("Nedostaje naslov ili tekst objave.")
    if not item.get("article", "").endswith(".html"):
        raise SystemExit("Neispravna poveznica članka.")
    if not PAGE_ID or not PAGE_TOKEN:
        raise SystemExit("Nedostaju GitHub Secrets FB_PAGE_ID i FB_PAGE_TOKEN.")
    token = page_token()
    ig_user = IG_USER
    if "instagram" in remaining:
        response = requests.get(
            f"{API}/{PAGE_ID}",
            params={"fields": "instagram_business_account", "access_token": token},
            timeout=20,
        )
        linked_ig_user = str((api_payload(response).get("instagram_business_account") or {}).get("id", ""))
        if not linked_ig_user or (ig_user and ig_user != linked_ig_user):
            raise SystemExit("Povezani Instagram račun nedostaje ili se ne podudara s IG_USER_ID.")
        ig_user = linked_ig_user

    image = make_card(item)
    for channel in remaining:
        pending[channel] = {"at": datetime.now(TZ).isoformat(timespec="seconds")}
        revision = save_remote(data, f"Zabilježi početak objave: {slug} ({channel})", image)
        if channel == "facebook":
            post_id = publish_facebook(item, token, image)
        else:
            post_id = publish_instagram(item, IG_TOKEN or token, ig_user, public_card_url(image, revision))
        if not post_id:
            raise RuntimeError("Meta nije vratila ID objave.")
        published[channel] = {"id": post_id, "at": datetime.now(TZ).isoformat(timespec="seconds")}
        del pending[channel]
        if all(channel in published for channel in requested):
            item["status"] = "published"
            item["approved"] = False
            if not pending:
                del item["publishing_to"]
        print(f"Meta ID ({channel}): {post_id}", flush=True)
        save_remote(data, f"Zabilježi dovršenu objavu: {slug} ({channel})")


if __name__ == "__main__":
    try:
        main()
    except requests.RequestException:
        raise SystemExit("Meta ili dohvat vizuala nije dostupan. Provjeri stanje prije ponavljanja.") from None
