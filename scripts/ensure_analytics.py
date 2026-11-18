#!/usr/bin/env python3
"""Make every Okretaji HTML page load the shared, opt-in analytics UI.

Safe to run repeatedly. Google Analytics is only downloaded after consent,
as implemented in /analytics-consent.js. Run with --check for CI validation.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_TAG = '<script src="/analytics-consent.js" defer></script>'
OLD_MARKER = '<!-- Google Analytics 4: učitava se tek nakon izričitog pristanka korisnika -->'


def transform(html: str, path: Path) -> tuple[str, bool]:
    """Remove the old duplicated consent UI and install the shared script."""
    modified = False
    if OLD_MARKER in html:
        if html.count(OLD_MARKER) != 1:
            raise ValueError(f"Multiple legacy analytics snippets: {path}")
        start = html.index(OLD_MARKER)
        end = html.find('</script>', start)
        if end < 0:
            raise ValueError(f"Missing legacy script closing tag: {path}")
        html = html[:start] + html[end + len('</script>'):]
        modified = True

    if 'googletagmanager.com/gtag/js' in html or "gtag('config'" in html:
        raise ValueError(f"Unexpected inline GA4 code: {path}")

    if html.count(SCRIPT_TAG) > 1:
        raise ValueError(f"Duplicate analytics script tags: {path}")

    if SCRIPT_TAG not in html:
        html, count = re.subn(
            r'</body\s*>',
            SCRIPT_TAG + '</body>',
            html,
            count=1,
            flags=re.IGNORECASE,
        )
        if count != 1:
            raise ValueError(f"Missing body closing tag: {path}")
        modified = True

    if html.count(SCRIPT_TAG) != 1 or OLD_MARKER in html:
        raise ValueError(f"Consent implementation invalid: {path}")

    return html, modified


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='Fail if updates are required')
    args = parser.parse_args()
    if not (ROOT / 'analytics-consent.js').is_file():
        raise SystemExit('Missing analytics-consent.js')
    paths = sorted(ROOT.rglob('*.html'))
    changed = []
    for path in paths:
        if '.git' in path.parts or 'node_modules' in path.parts:
            continue
        old = path.read_text(encoding='utf-8')
        new, modified = transform(old, path)
        if modified:
            changed.append(path.relative_to(ROOT).as_posix())
            if not args.check:
                path.write_text(new, encoding='utf-8')

    print(f'Checked {len(paths)} HTML pages; {"noncompliant" if args.check else "updated"}: {len(changed)}')
    for path in changed:
        print('  ' + path)
    if args.check and changed:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
