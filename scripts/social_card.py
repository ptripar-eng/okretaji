#!/usr/bin/env python3
"""Generate a branded Okretaji social card (1080x1350 JPEG) for one news item.

The card uses only Okretaji's own design (Gulf livery colours, Big Shoulders Display
+ Barlow), so no third-party photo is needed and there is no copyright risk.
Fonts are read from FONT_DIR (downloaded by the workflow); DejaVu is the fallback.
"""
import os
import sys
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
NAVY = "#0D2B3E"
DEEP = "#081923"
POWDER = "#A9D3EB"
BLUE = "#7DBCE6"
ORANGE = "#FF7433"
WHITE = "#FFFFFF"
MUTED = "#93AEC0"
PAD = 84
FONT_DIR = Path(os.getenv("FONT_DIR", Path(__file__).resolve().parent.parent / ".fonts"))

CATEGORY_LABEL = {
    "f1": "FORMULA 1",
    "motogp": "MOTOGP",
    "reli": "RELI",
    "moto": "MOTOCIKLI",
    "auto": "AUTOMOBILI",
    "tech": "TEHNOLOGIJA",
    "energy": "ENERGIJA",
    "kaciga": "IZA KACIGE",
}


def _font(name, size, weight=None):
    path = FONT_DIR / name
    try:
        font = ImageFont.truetype(str(path), size)
        if weight is not None:
            try:
                font.set_variation_by_axes([weight])
            except (OSError, ValueError, AttributeError):
                pass
        return font
    except OSError:
        for fallback in ("DejaVuSans-Bold.ttf", "DejaVuSans.ttf"):
            try:
                return ImageFont.truetype(fallback, int(size * 0.8))
            except OSError:
                continue
        return ImageFont.load_default()


def display(size):
    return _font("BigShouldersDisplay.ttf", size, 900)


def barlow(size, bold=False):
    return _font("Barlow-Bold.ttf" if bold else "Barlow-Medium.ttf", size)


def wrap(draw, text, font, width):
    words, lines, line = text.split(), [], ""
    for word in words:
        test = (line + " " + word).strip()
        if draw.textlength(test, font=font) <= width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def clamp(draw, text, font, width, max_lines):
    lines = wrap(draw, text, font, width)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    last = lines[-1]
    while last and draw.textlength(last + "…", font=font) > width:
        last = last.rsplit(" ", 1)[0] if " " in last else last[:-1]
    lines[-1] = last.rstrip(",.;:–- ") + "…"
    return lines


def make_card(article, out_path):
    title = " ".join(str(article.get("t") or "").split()).strip()
    summary = " ".join(str(article.get("s") or "").split()).strip()
    category = str(article.get("c") or "").lower()
    source = str(article.get("src") or "").strip()
    label = CATEGORY_LABEL.get(category, "OKRETAJI")

    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # Gulf livery: powder-blue field with an orange racing stripe.
    d.rectangle([0, 0, W, 300], fill=POWDER)
    d.polygon([(0, 214), (W, 128), (W, 196), (0, 282)], fill=ORANGE)
    d.polygon([(0, 300), (W, 300), (W, 260), (0, 346)], fill=NAVY)
    d.text((PAD, 66), "OKRETAJI", font=display(96), fill=NAVY)

    # Category chip.
    chip_font = barlow(30, bold=True)
    chip_w = d.textlength(label, font=chip_font) + 44
    y = 392
    d.rounded_rectangle([PAD, y, PAD + chip_w, y + 56], radius=8, fill=ORANGE)
    d.text((PAD + 22, y + 10), label, font=chip_font, fill=DEEP)

    # Title: largest size that fits in five lines.
    y += 92
    text_w = W - 2 * PAD
    for size in (104, 96, 88, 80, 72, 64, 58):
        tf = display(size)
        lines = wrap(d, title.upper(), tf, text_w)
        if len(lines) <= 5:
            break
    lines = clamp(d, title.upper(), tf, text_w, 5)
    line_h = int(size * 1.02)
    for line in lines:
        d.text((PAD, y), line, font=tf, fill=WHITE)
        y += line_h

    # Summary.
    y += 34
    d.rectangle([PAD, y, PAD + 96, y + 8], fill=ORANGE)
    y += 36
    sf = barlow(38)
    space = (H - 190) - y
    max_lines = max(0, min(6, space // 50))
    for line in clamp(d, summary, sf, text_w, max_lines) if max_lines else []:
        d.text((PAD, y), line, font=sf, fill=POWDER)
        y += 50

    # Footer.
    d.rectangle([0, H - 130, W, H], fill=DEEP)
    d.rectangle([0, H - 130, W, H - 124], fill=ORANGE)
    d.text((PAD, H - 92), "okretaji.com", font=barlow(40, bold=True), fill=WHITE)
    if source:
        src_font = barlow(30)
        src_text = "Izvor: " + source
        while d.textlength(src_text, font=src_font) > 480 and len(src_text) > 10:
            src_text = src_text[:-2].rstrip() + "…"
        d.text((W - PAD - d.textlength(src_text, font=src_font), H - 86),
               src_text, font=src_font, fill=MUTED)

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "JPEG", quality=90, optimize=True)
    return out_path


if __name__ == "__main__":
    # Usage: social_card.py [index] [out.jpg] — renders one news.json item for preview.
    root = Path(__file__).resolve().parent.parent
    items = json.loads((root / "news.json").read_text(encoding="utf-8")).get("items", [])
    idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    out = sys.argv[2] if len(sys.argv) > 2 else "card.jpg"
    print(make_card(items[idx], out))
