#!/usr/bin/env python3
"""Add openly licensed illustrative photos to news.json, preserving attribution."""
import json, os, time, requests
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEWS=os.path.join(ROOT,"news.json"); CACHE=os.path.join(ROOT,"images.json")
UA="OkretajiBot/1.0 (+https://okretaji.com)"
def main():
    data=json.load(open(NEWS,encoding="utf-8"))
    try: cache=json.load(open(CACHE,encoding="utf-8"))
    except Exception: cache={}
    changed=0
    for n in data.get("items",[]):
        url=n.get("u","")
        if not url: continue
        if n.get("img",{}).get("src"): continue
        if url in cache and cache[url]:
            n["img"]=cache[url]; continue
        query=(n.get("img_q") or n.get("t") or "").strip()
        if not query: cache[url]=None; continue
        try:
            r=requests.get("https://api.openverse.org/v1/images/",params={"q":query,"page_size":10,"license_type":"commercial"},headers={"User-Agent":UA,"Accept":"application/json"},timeout=18)
            r.raise_for_status()
            results=r.json().get("results",[])
            chosen=None
            for x in results:
                src=x.get("thumbnail") or x.get("url")
                creator=x.get("creator")
                lic=x.get("license")
                link=x.get("foreign_landing_url") or x.get("url")
                if src and creator and lic and link:
                    chosen={"id":x.get("id"),"src":src,"by":creator,"lic":str(lic).upper().replace("CC","CC "),"link":link}
                    break
            cache[url]=chosen
            if chosen: n["img"]=chosen; changed+=1
            time.sleep(.2)
        except Exception as e:
            print("Openverse nije dostupan za",query,":",str(e)[:120])
            cache[url]=None
    with open(NEWS,"w",encoding="utf-8") as f: json.dump(data,f,ensure_ascii=False,indent=1)
    with open(CACHE,"w",encoding="utf-8") as f: json.dump(cache,f,ensure_ascii=False,indent=1)
    total=sum(bool(x.get("img",{}).get("src")) for x in data.get("items",[]))
    print(f"Fotografije: {total}/{len(data.get('items',[]))} vijesti imaju atribuiranu sliku; novo dodano {changed}.")
if __name__=="__main__": main()
