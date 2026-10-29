#!/usr/bin/env python3
"""Zajedničko za Meta objave: iz FB_PAGE_TOKEN dobij token stranice i ispiši njegovu valjanost.

Vrijednost tokena se nikad ne ispisuje.
"""
import json
from datetime import datetime, timezone

import requests


def _expiry(api, token):
    try:
        data = requests.get(
            f"{api}/debug_token",
            params={"input_token": token, "access_token": token},
            timeout=20,
        ).json().get("data", {})
    except (requests.RequestException, ValueError):
        return "nepoznato"
    exp = data.get("expires_at")
    if exp == 0:
        return "ne istječe"
    if exp:
        return "istječe " + datetime.fromtimestamp(exp, timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return "nepoznato"


def resolve_page_token(api, page_id, token):
    """Vrati token stranice; prihvaća i korisnički token osobe koja upravlja stranicom."""
    me = requests.get(f"{api}/me", params={"fields": "id,name", "access_token": token}, timeout=20).json()
    if me.get("error"):
        raise RuntimeError("Meta token nije valjan: " + json.dumps(me["error"], ensure_ascii=False)[:400])
    if str(me.get("id")) == str(page_id):
        print("Token: token stranice,", _expiry(api, token))
        return token
    print("Token: korisnički token,", _expiry(api, token))
    page = requests.get(
        f"{api}/{page_id}",
        params={"fields": "name,access_token", "access_token": token},
        timeout=20,
    ).json()
    if page.get("error") or not page.get("access_token"):
        raise RuntimeError(
            "Korisnički token ne daje pristup stranici: "
            + json.dumps(page.get("error", {"message": "nema access_token"}), ensure_ascii=False)[:400]
        )
    print("Dohvaćen token stranice", page.get("name", "") + ",", _expiry(api, page["access_token"]))
    return page["access_token"]
