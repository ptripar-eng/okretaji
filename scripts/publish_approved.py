#!/usr/bin/env python3
import json, os, subprocess, sys, time
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
IG_TOKEN=(os.getenv("IG_ACCESS_TOKEN") or PAGE_TOKEN).strip()
REPO=os.getenv("GITHUB_REPOSITORY","ptripar-eng/okretaji")
TZ=ZoneInfo("Europe/Zagreb")

def git(*args):
    return subprocess.run(["git",*args],cwd=ROOT,check=True,capture_output=True,text=True).stdout.strip()

def save(data):
    QUEUE.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def api_post(path,data,files=None):
    r=requests.post(f"{API}/{path}",data=data,files=files,timeout=60)
    try: payload=r.json()
    except ValueError: payload={"error":{"message":r.text[:500]}}
    if not r.ok or payload.get("error"): raise RuntimeError(json.dumps(payload.get("error",payload),ensure_ascii=False)[:800])
    return payload

def page_token():
    from meta_token import resolve_page_token
    return resolve_page_token(API,PAGE_ID,PAGE_TOKEN)

def make_card(item):
    from social_card import make_card as render
    article={"t":item["title"],"s":item.get("summary") or item["title"],"c":item.get("category","moto"),"src":"Okretaji"}
    name=f"{datetime.now(TZ):%Y%m%d-%H%M%S}-{item['slug']}.jpg"
    path=render(article,CARDS/name)
    rel=path.relative_to(ROOT).as_posix()
    git("add",rel)
    git("commit","-m","Pripremi vizual za objavu: "+item["title"][:55])
    git("push")
    sha=git("rev-parse","HEAD")
    url=f"https://raw.githubusercontent.com/{REPO}/{sha}/{rel}"
    for _ in range(12):
        if requests.head(url,timeout=15).status_code==200: return path,url
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
        payload=r.json()
        if payload.get("error"): raise RuntimeError(json.dumps(payload["error"],ensure_ascii=False)[:700])
        status=payload.get("status_code","")
        if status=="FINISHED": break
        if status in ("ERROR","EXPIRED"): raise RuntimeError("Instagram obrada nije uspjela: "+status)
    if status!="FINISHED": raise RuntimeError("Instagram vizual nije spreman: "+str(status))
    result=api_post(f"{user_id}/media_publish",{"creation_id":cid,"access_token":token})
    return result.get("id")

def main():
    if len(sys.argv)<3: raise SystemExit("Upotreba: publish_approved.py <slug> <facebook|instagram|both>")
    slug,target=sys.argv[1],sys.argv[2]
    data=json.loads(QUEUE.read_text(encoding="utf-8"))
    items=data.get("items",[])
    item=next((x for x in items if x.get("slug")==slug),None)
    if not item: raise SystemExit("Nacrt nije pronađen: "+slug)
    if item.get("approved") is not True: raise SystemExit("Objava nije odobrena. U social/queue.json postavi approved: true.")
    already=item.get("published_to",{})
    requested={"facebook","instagram"} if target=="both" else {target}
    if requested.issubset(set(already)): raise SystemExit("Odabrani kanal(i) već imaju objavu; zaštita od duplikata je aktivna.")
    if not item.get("title") or not item.get("facebook") or not item.get("instagram"): raise SystemExit("Nedostaje naslov ili tekst objave.")
    article_url="https://okretaji.com/"+item.get("article","")
    if not item.get("article","").endswith(".html"): raise SystemExit("Neispravna poveznica članka.")
    token=None
    if target in ("facebook","both","instagram"):
        if not PAGE_ID or not PAGE_TOKEN: raise SystemExit("Nedostaju GitHub Secrets FB_PAGE_ID i FB_PAGE_TOKEN.")
        token=page_token()
    image_path,image_url=make_card(item)
    if target in ("facebook","both"):
        post_id=(item.get("published_to",{}).get("facebook") or {}).get("id")
        if not post_id: post_id=publish_facebook(item,token,image_path)
        if not post_id: raise RuntimeError("Facebook nije vratio ID objave.")
        item.setdefault("published_to",{})["facebook"]={"id":post_id,"at":datetime.now(TZ).isoformat(timespec="seconds")}
        save(data); print("Facebook objavljeno:",post_id)
    if target in ("instagram","both"):
        if not IG_USER:
            page=requests.get(f"{API}/{PAGE_ID}",params={"fields":"instagram_business_account","access_token":token},timeout=20).json()
            IG_USER=(page.get("instagram_business_account") or {}).get("id","")
        if not IG_USER: raise SystemExit("Nije pronađen povezani Instagram poslovni račun. Postavi IG_USER_ID ili poveži račun sa stranicom.")
        ig_token=IG_TOKEN or token
        media_id=(item.get("published_to",{}).get("instagram") or {}).get("id")
        if not media_id: media_id=publish_instagram(item,ig_token,IG_USER,image_url)
        if not media_id: raise RuntimeError("Instagram nije vratio ID objave.")
        item.setdefault("published_to",{})["instagram"]={"id":media_id,"at":datetime.now(TZ).isoformat(timespec="seconds")}
        save(data); print("Instagram objavljeno:",media_id)
    required={"facebook"} if target=="facebook" else {"instagram"} if target=="instagram" else {"facebook","instagram"}
    if required.issubset(set(item.get("published_to",{}))):
        item["status"]="published"
        item["approved"]=False
        save(data)
    print("Završeno:",slug,target)

if __name__=="__main__": main()
