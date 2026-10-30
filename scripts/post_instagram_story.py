#!/usr/bin/env python3
"""Create and optionally publish one vertical Instagram Story per local day.

Uses an original Okretaji graphic, links the publisher in the visual, and never
copies a publisher's photograph. Meta Story publishing requires IG_LIVE=1.
"""
import json, os, subprocess, time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import requests
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
NEWS = ROOT / "news.json"
STATE = ROOT / "instagram_stories.json"
OUT = ROOT / "social" / "stories"
REPO = os.getenv("GITHUB_REPOSITORY", "ptripar-eng/okretaji")
PAGE_ID = os.getenv("FB_PAGE_ID", "").strip()
TOKEN = (os.getenv("IG_ACCESS_TOKEN") or os.getenv("FB_PAGE_TOKEN") or "").strip()
USER_ID = os.getenv("IG_USER_ID", "").strip()
LIVE = os.getenv("IG_LIVE", "0") == "1"
API_VERSION = os.getenv("IG_GRAPH_API_VERSION", "v24.0")
API = f"https://graph.facebook.com/{API_VERSION}"
TZ = ZoneInfo("Europe/Zagreb")
W, H = 1080, 1920
NAVY, DEEP, ORANGE, POWDER, WHITE, MUTED = "#0D2B3E", "#081923", "#F05A1A", "#A9D3EB", "#FFFFFF", "#C4D9E5"

def font(size, bold=False):
    paths = [
        ROOT / ".fonts" / ("Barlow-Bold.ttf" if bold else "Barlow-Medium.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    ]
    for path in paths:
        try: return ImageFont.truetype(str(path), size)
        except OSError: pass
    return ImageFont.load_default()

def wrap(draw, text, f, width):
    lines, line = [], ""
    for word in str(text).split():
        test = (line + " " + word).strip()
        if draw.textlength(test, font=f) <= width: line = test
        else:
            if line: lines.append(line)
            line = word
    if line: lines.append(line)
    return lines

def render(item, path):
    im = Image.new("RGB", (W,H), NAVY); d = ImageDraw.Draw(im)
    d.rectangle((0,0,W,360), fill=POWDER)
    d.polygon([(0,265),(W,150),(W,245),(0,360)], fill=ORANGE)
    d.text((72,75), "OKRETAJI", font=font(112,True), fill=NAVY)
    cat = str(item.get("c","")).upper().replace("MOTOGP","MOTO GP").replace("F1","FORMULA 1")
    d.rounded_rectangle((72,440,430,510), radius=14, fill=ORANGE)
    d.text((96,452), cat[:22], font=font(34,True), fill=DEEP)
    y=590
    title=font(88,True)
    lines=wrap(d,item.get("t",""),title,936)[:7]
    for line in lines:
        d.text((72,y),line, font=title, fill=WHITE, stroke_width=1, stroke_fill=WHITE); y += 108
    y += 48
    d.rounded_rectangle((72,y,168,y+10),radius=5,fill=ORANGE); y+=55
    body=font(43)
    for line in wrap(d,item.get("s",""),body,920)[:7]:
        d.text((72,y),line,font=body,fill=POWDER); y+=62
    y=max(y+65,1450)
    d.rounded_rectangle((72,y,1008,y+210),radius=24,fill="#173B50")
    d.text((110,y+28),"A TI?",font=font(58,True),fill=ORANGE)
    for i,line in enumerate(wrap(d,"Što ti misliš? Odgovori na ovu priču i uključi se u raspravu.",font(39),820)[:3]):
        d.text((110,y+105+i*48),line,font=font(39),fill=WHITE)
    d.rectangle((0,H-130,W,H),fill=DEEP); d.rectangle((0,H-130,W,H-122),fill=ORANGE)
    source=("IZVOR: "+str(item.get("src",""))).strip()
    d.text((72,H-88),"okretaji.com",font=font(42,True),fill=WHITE)
    d.text((1008-d.textlength(source,font=font(25)),H-82),source,font=font(25),fill=MUTED)
    path.parent.mkdir(parents=True,exist_ok=True); im.save(path,"JPEG",quality=91,optimize=True)
    return path

def git(*args):
    return subprocess.run(["git",*args],cwd=ROOT,check=True,capture_output=True,text=True).stdout.strip()

def api_post(endpoint,data):
    r=requests.post(f"{API}/{endpoint}",data=data,timeout=40)
    payload=r.json()
    if not r.ok or payload.get("error"): raise RuntimeError(json.dumps(payload.get("error",payload),ensure_ascii=False)[:700])
    return payload

def main():
    now=datetime.now(TZ); state=json.loads(STATE.read_text()) if STATE.exists() else {"items":[]}
    if any(str(x.get("posted_at",""))[:10]==now.date().isoformat() for x in state.get("items",[])):
        print("Instagram Story: dnevno ograničenje dosegnuto."); return
    data=json.loads(NEWS.read_text(encoding="utf-8")); posted={x.get("url") for x in state.get("items",[])}
    items=[x for x in data.get("items",[]) if x.get("u","").startswith("https://") and x.get("u") not in posted and x.get("hr") is True and x.get("summary_version")==3 and x.get("t") and x.get("s")]
    if not items: print("Instagram Story: nema nove provjerene vijesti."); return
    items.sort(key=lambda x:x.get("date",""),reverse=True)
    priorities={"f1":0,"motogp":0,"reli":1,"moto":1,"auto":2,"kaciga":2,"tech":3,"energy":3}
    items.sort(key=lambda x:priorities.get(x.get("c"),9))
    item=items[0]
    stamp=now.strftime("%Y%m%d-%H%M"); out=OUT/f"{stamp}-okretaji-story.jpg"; render(item,out)
    rel=out.relative_to(ROOT).as_posix()
    print("Story vizual:",rel,"|",item["t"])
    if not LIVE:
        print("DRY_RUN: vizual je izrađen, objava nije poslana."); return
    if not PAGE_ID or not TOKEN: raise SystemExit("Instagram Story LIVE zahtijeva Meta pristupne podatke.")
    from meta_token import resolve_page_token
    token=resolve_page_token(API,PAGE_ID,TOKEN)
    user=USER_ID
    if not user:
        page=requests.get(f"{API}/{PAGE_ID}",params={"fields":"instagram_business_account","access_token":token},timeout=20).json()
        user=(page.get("instagram_business_account") or {}).get("id","")
    if not user: raise RuntimeError("Nije pronađen povezani Instagram poslovni račun.")
    git("add",rel); git("commit","-m","Instagram Story: "+str(item["t"])[:55]); git("pull","--rebase","--autostash"); git("push")
    sha=git("rev-parse","HEAD"); image_url=f"https://raw.githubusercontent.com/{REPO}/{sha}/{rel}"
    for _ in range(10):
        if requests.head(image_url,timeout=15).status_code==200: break
        time.sleep(3)
    media=api_post(f"{user}/media",{"image_url":image_url,"media_type":"STORIES","access_token":token})
    creation=media.get("id")
    if not creation: raise RuntimeError("Meta nije vratila ID Story spremnika.")
    result=api_post(f"{user}/media_publish",{"creation_id":creation,"access_token":token})
    state.setdefault("items",[]).append({"url":item["u"],"posted_at":now.isoformat(timespec="seconds"),"media_id":result.get("id"),"title":item["t"]})
    state["items"]=state["items"][-500:]
    STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Instagram Story objavljen. Meta media ID:",result.get("id"))

if __name__=="__main__": main()
