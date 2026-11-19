#!/usr/bin/env python3
"""Generate campaign-tagged Okretaji.com URLs without third-party services.

Only standard Python library is used. The tool never posts anything.
Example:
    python3 scripts/utm_links.py \
      --path /kako-smo-dosli-do-1-0-turba.html \
      --source instagram --campaign hr_tehnika_202611 --content reel_turbo_01
"""
from __future__ import annotations

import argparse
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

BASE = "https://okretaji.com"
TOKEN = re.compile(r"^[a-z0-9][a-z0-9_-]{1,79}$")
SOURCES = {"instagram", "facebook"}


def tagged_url(path: str, source: str, campaign: str, content: str = "") -> str:
    """Return a canonical on-site link carrying unambiguous social attribution."""
    parsed = urlsplit(path if "://" in path else BASE + "/" + path.lstrip("/"))
    if parsed.scheme != "https" or parsed.netloc.lower() not in {"okretaji.com", "www.okretaji.com"}:
        raise ValueError("Destination must be an HTTPS page on okretaji.com")
    if not parsed.path.endswith(".html") and parsed.path not in {"", "/"}:
        raise ValueError("Use a public article .html path or the homepage")
    if source not in SOURCES:
        raise ValueError("Source must be 'instagram' or 'facebook'")
    if not TOKEN.fullmatch(campaign):
        raise ValueError("Campaign must be 2–80 lowercase letters, numbers, '_' or '-'")
    if content and not TOKEN.fullmatch(content):
        raise ValueError("Content must be 2–80 lowercase letters, numbers, '_' or '-'")
    existing = [(k, v) for k, v in parse_qsl(parsed.query, keep_blank_values=True)
                if not k.startswith("utm_")]
    campaign_tags = [
        ("utm_source", source),
        ("utm_medium", "social"),
        ("utm_campaign", campaign),
    ]
    if content:
        campaign_tags.append(("utm_content", content))
    return urlunsplit(("https", "okretaji.com", parsed.path or "/",
                       urlencode(existing + campaign_tags), parsed.fragment))


def self_test() -> None:
    url = tagged_url("/kako-smo-dosli-do-1-0-turba.html", "instagram",
                     "hr_tehnika_202611", "reel_turbo_01")
    assert url == (
        "https://okretaji.com/kako-smo-dosli-do-1-0-turba.html"
        "?utm_source=instagram&utm_medium=social"
        "&utm_campaign=hr_tehnika_202611&utm_content=reel_turbo_01"
    )
    assert "q=hi" in tagged_url("https://okretaji.com/?utm_source=bad&q=hi",
                               "facebook", "hr_motogp_202611")
    for bad in ("https://example.com/", "http://okretaji.com/", "javascript:alert(1)"):
        try:
            tagged_url(bad, "facebook", "valid_campaign")
        except ValueError:
            pass
        else:
            raise AssertionError("An unsafe target was accepted: " + bad)
    print("UTM link generator self-test: PASS")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--path", help="Article path or absolute okretaji.com link")
    p.add_argument("--source", choices=sorted(SOURCES))
    p.add_argument("--campaign", help="Tracking campaign slug")
    p.add_argument("--content", default="", help="Optional distinct creative ID")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        self_test()
        return
    if not (args.path and args.source and args.campaign):
        p.error("--path, --source and --campaign are required except for --self-test")
    try:
        print(tagged_url(args.path, args.source, args.campaign, args.content))
    except ValueError as exc:
        p.error(str(exc))


if __name__ == "__main__":
    main()
