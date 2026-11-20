#!/usr/bin/env python3
"""One-shot, consented production GA4 network probe.

Unlike qa_consent_browser.py, this does NOT mock the Google tag. It checks
the actual outbound request/response in Chromium and emits only redacted
diagnostics. A single, explicitly opted-in synthetic session is expected.
It proves network submission, NOT GA4 property ingestion.
"""
from __future__ import annotations

from urllib.parse import parse_qs, urlsplit

from playwright.sync_api import TimeoutError as PlaywrightTimeout
from playwright.sync_api import sync_playwright

SITE = "https://okretaji.com/kako-smo-dosli-do-1-0-turba.html"
TAG_ID = "G-426646FTQH"
PAGE = SITE + "?utm_source=okretaji_qa&utm_medium=internal&utm_campaign=ga4_network_probe"
CONSENT_KEY = "okretaji_analytics_consent"


def is_google_tag(url: str) -> bool:
    parts = urlsplit(url)
    return parts.hostname == "www.googletagmanager.com" and parts.path == "/gtag/js"


def is_ga4_collect(url: str) -> bool:
    parts = urlsplit(url)
    return (parts.hostname or "").endswith("google-analytics.com") and "/g/collect" in parts.path


def run() -> None:
    tag_requests: list[dict] = []
    collect_requests: list[dict] = []
    failed_requests: list[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            locale="hr-HR", viewport={"width": 390, "height": 844},
        )
        page = context.new_page()

        def on_request(request) -> None:
            if is_google_tag(request.url):
                tag_requests.append({"url": request.url, "status": "requested"})
            if is_ga4_collect(request.url):
                # GA4 may send a GET, POST, or fetch beacon. Never log cid,
                # cookies, user identifiers, or complete URLs.
                params = parse_qs(urlsplit(request.url).query)
                collect_requests.append({
                    "status": "requested",
                    "method": request.method,
                    "tid": params.get("tid", [None])[0],
                    "event": params.get("en", [None])[0],
                    "page_path": urlsplit(params.get("dl", [""])[0]).path,
                })

        def on_response(response) -> None:
            if is_google_tag(response.url):
                for item in tag_requests:
                    if item["url"] == response.url:
                        item["status"] = response.status
            if is_ga4_collect(response.url):
                params = parse_qs(urlsplit(response.url).query)
                for item in collect_requests:
                    if (item["tid"] == params.get("tid", [None])[0]
                            and item["event"] == params.get("en", [None])[0]):
                        item["status"] = response.status

        def on_failed(request) -> None:
            if is_google_tag(request.url) or is_ga4_collect(request.url):
                failed_requests.append("ga4-tag" if is_google_tag(request.url) else "ga4-collect")

        page.on("request", on_request)
        page.on("response", on_response)
        page.on("requestfailed", on_failed)

        page.goto(PAGE, wait_until="domcontentloaded", timeout=35000)
        page.locator("#okretaji-consent").wait_for(state="visible", timeout=15000)
        page.wait_for_timeout(900)
        assert not tag_requests and not collect_requests, (
            "FAIL: Google Analytics requested data before explicit consent"
        )

        page.get_by_role("button", name="Prihvaćam analitiku").click()
        assert page.evaluate(f"localStorage.getItem('{CONSENT_KEY}')") == "granted"
        try:
            page.wait_for_function(
                """() => performance.getEntriesByType('resource').some(
                    r => r.name.includes('googletagmanager.com/gtag/js')
                )""", timeout=20000
            )
        except PlaywrightTimeout:
            print("WARNING: Google tag not visible as loaded resource")
        page.wait_for_timeout(9000)

        print("TAG:", [{
            "status": t["status"], "expected_id": TAG_ID in t["url"],
        } for t in tag_requests])
        print("COLLECT:", collect_requests)
        print("FAILED_REQUEST_CLASSES:", failed_requests)
        browser.close()

    has_tag = any(TAG_ID in t["url"] and t["status"] == 200 for t in tag_requests)
    has_page_view = any(
        c["tid"] == TAG_ID and c["event"] == "page_view"
        and c["page_path"] == urlsplit(SITE).path
        and c["status"] in (200, 202, 204)
        for c in collect_requests
    )
    if not has_tag or not has_page_view:
        raise SystemExit(
            "INCONCLUSIVE/FAIL: no successful, verified outbound GA4 "
            "page_view request. Check tag network, consent, blockers and GA ID."
        )
    print("PASS: real Google tag HTTP 200 and real GA4 page_view HTTP success.")
    print("NOTE: network success does not prove ingestion into GA4 property.")


if __name__ == "__main__":
    run()
