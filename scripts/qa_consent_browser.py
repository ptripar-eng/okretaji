#!/usr/bin/env python3
"""Browser regression test for Okretaji's consent-gated GA4 integration.

Tests the production webpage with Chromium. Intercepts the GA tag request so
this test sends no analytics to Google and does not inflate readership.
Requires 'playwright' and an installed Chromium browser.
"""
from playwright.sync_api import sync_playwright

ARTICLE = "https://okretaji.com/kako-smo-dosli-do-1-0-turba.html"
NEXT_PAGE = "https://okretaji.com/f1.html"
GA_SCRIPT = "https://www.googletagmanager.com/gtag/js?id=G-426646FTQH"
CONSENT = "#okretaji-consent"


def run() -> None:
    ga_requests = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            locale="hr-HR", viewport={"width": 390, "height": 844}
        )
        page = context.new_page()

        def fake_ga(route):
            ga_requests.append(route.request.url)
            route.fulfill(
                status=200,
                content_type="application/javascript",
                body="window.__okretajiTestGtagRequested = true;",
            )

        # All GA tag downloads are intercepted. No real GA data is transmitted.
        page.route("https://www.googletagmanager.com/gtag/js?*", fake_ga)

        page.goto(ARTICLE, wait_until="domcontentloaded", timeout=30000)
        page.locator(CONSENT).wait_for(state="visible")
        assert not ga_requests, "GA script requested before consent!"
        assert page.evaluate("localStorage.getItem('okretaji_analytics_consent')") is None
        assert not page.evaluate("window.__okretajiAnalyticsLoaded === true")

        page.get_by_role("button", name="Prihvaćam analitiku").click()
        page.wait_for_function("window.__okretajiTestGtagRequested === true")
        assert GA_SCRIPT in ga_requests, f"Unexpected GA requests: {ga_requests!r}"
        assert page.locator(CONSENT).is_hidden(), "Dialog remained visible"
        assert page.evaluate("localStorage.getItem('okretaji_analytics_consent')") == "granted"
        assert page.evaluate("window.__okretajiAnalyticsLoaded === true")
        assert page.evaluate("window.dataLayer.length >= 2"), "GA setup commands missing"

        # Consent must persist across navigation to a second page.
        page.goto(NEXT_PAGE, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_function("window.__okretajiTestGtagRequested === true")
        assert page.locator(CONSENT).is_hidden(), "Consent dialog reappeared"
        assert page.evaluate("window.__okretajiAnalyticsLoaded === true")
        assert len(ga_requests) >= 2, "GA script not requested on second page"

        # Explicit rejection in a fresh context must never request GA.
        second = browser.new_context(locale="hr-HR")
        rejected = second.new_page()
        rejected_ga_requests = []

        def on_request(req):
            if "googletagmanager.com/gtag/js" in req.url:
                rejected_ga_requests.append(req.url)

        rejected.on("request", on_request)
        rejected.goto(ARTICLE, wait_until="domcontentloaded", timeout=30000)
        rejected.get_by_role("button", name="Odbijam").click()
        rejected.wait_for_timeout(250)
        assert rejected.locator(CONSENT).is_hidden()
        assert not rejected_ga_requests, "GA script requested after rejection!"
        assert rejected.evaluate("localStorage.getItem('okretaji_analytics_consent')") == "denied"
        second.close()
        context.close()
        browser.close()
    print("PASS: GA tag request only after consent; decline blocks; choice persists")


if __name__ == "__main__":
    run()
