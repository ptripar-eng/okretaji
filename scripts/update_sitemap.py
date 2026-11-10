"""Generate sitemap.xml from the published HTML files."""

import argparse
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://okretaji.com"
LOCALES = ("", "en/", "de/")
# These routes use URL parameters and are not standalone articles.
TEMPLATES = {"clanak.html", "rubrika.html", "404.html"}


class PageHead(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals = []
        self.noindex = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and "canonical" in (attrs.get("rel") or "").lower().split():
            self.canonicals.append(attrs.get("href"))
        if tag == "meta" and (attrs.get("name") or "").lower() in {"robots", "googlebot"}:
            directives = re.split(r"[,\s]+", (attrs.get("content") or "").lower())
            self.noindex |= "noindex" in directives or "none" in directives


def render_sitemap():
    rows = []
    for page in sorted(ROOT.glob("*.html"), key=lambda p: (p.name != "index.html", p.name)):
        if page.name in TEMPLATES or re.fullmatch(r"google\w*\.html", page.name):
            continue
        for locale in LOCALES:
            path = ROOT / locale / page.name
            if not path.is_file():
                continue
            url = f"{SITE}/{locale}{'' if page.name == 'index.html' else page.name}"
            head = PageHead()
            head.feed(re.split(r"</head\s*>", path.read_text(encoding="utf-8"), maxsplit=1, flags=re.I)[0])
            if head.noindex:
                continue
            if head.canonicals != [url]:
                raise ValueError(f"{path.relative_to(ROOT)}: expected exactly one canonical pointing to {url}")
            rows.append(f"  <url><loc>{url}</loc></url>\n")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join(rows) + "</urlset>\n")


def update_sitemap(check=False):
    path = ROOT / "sitemap.xml"
    xml = render_sitemap()
    if path.is_file() and path.read_text(encoding="utf-8") == xml:
        return
    if check:
        raise SystemExit("sitemap.xml je zastario. Pokrenite python scripts/update_sitemap.py.")
    path.write_text(xml, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    update_sitemap(check=parser.parse_args().check)
