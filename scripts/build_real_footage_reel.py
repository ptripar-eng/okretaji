#!/usr/bin/env python3
"""Build a real-footage Okretaji motorcycle Reel (15.3 s, 9:16).

No illustrative CGI, animation, scraped racing broadcasts or third-party music.
All source clips and real motorcycle sound effects are downloaded from specified
Mixkit Free License pages. Fails closed on missing/invalid assets.

Produces only a private-to-workflow artifact for EDITORIAL REVIEW, never posts.
"""
from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "build" / "real_footage_reel"
WORK.mkdir(parents=True, exist_ok=True)
OUT = ROOT / "build" / "deliverables"
OUT.mkdir(parents=True, exist_ok=True)

VIDEO = {
    "wheel": ("https://assets.mixkit.co/videos/39917/39917-1080.mp4",
              "https://mixkit.co/free-stock-video/wheels-of-a-motorcycle-traveling-fast-down-a-road-39917/"),
    "rider": ("https://assets.mixkit.co/videos/39929/39929-1080.mp4",
              "https://mixkit.co/free-stock-video/man-on-motorcycle-on-a-road-close-up-39929/"),
    "tunnel": ("https://assets.mixkit.co/videos/4136/4136-1080.mp4",
               "https://mixkit.co/free-stock-video/motorbike-racing-through-tunnels-4136/"),
}
SOUND = {
    "rev": ("https://assets.mixkit.co/active_storage/sfx/2725/2725.wav",
            "https://mixkit.co/free-sound-effects/motorcycle/"),
    "pass": ("https://assets.mixkit.co/active_storage/sfx/1606/1606.wav",
             "https://mixkit.co/free-sound-effects/motorcycle/"),
}
CLIPS = [
    ("wheel", 2.4, 0.1, "OVO TE DRŽI", "U ZAVOJU.", "GUMA / KONTAKT"),
    ("rider", 2.4, 0.2, "NAGNEŠ MOTOR.", "OSLONAC SE MIJENJA.", "NAGIB"),
    ("wheel", 2.3, 4.0, "SA SREDINE", "PREMA RAMENU GUME.", "PROFIL"),
    ("tunnel", 2.7, 0.1, "TLAK + TEMPERATURA", "MIJENJAJU PRIANJANJE.", "PRIANJANJE"),
    ("rider", 2.5, 4.0, "NIJE STVAR SAMO", "U ŠARI GUME.", "KONSTRUKCIJA"),
    ("wheel", 3.0, 7.0, "STABILNOST POČINJE", "NA ASFALTU.", "OKRETAJI.COM"),
]
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
FONT_NORMAL = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
ORANGE = (249, 100, 44, 255)


def run(*args: str) -> None:
    print("$", " ".join(str(x) for x in args), flush=True)
    subprocess.run([str(x) for x in args], check=True)


def download_asset(url: str, name: str, min_bytes: int = 250_000) -> Path:
    dest = WORK / name
    if dest.is_file() and dest.stat().st_size > min_bytes:
        return dest
    for attempt in range(3):
        try:
            req = Request(url, headers={"User-Agent": "Mozilla/5.0 (Okretaji editorial video production)"})
            with urlopen(req, timeout=55) as r, dest.open("wb") as out:
                if r.status != 200:
                    raise ValueError(f"HTTP {r.status} for {name}")
                while chunk := r.read(1 << 20):
                    out.write(chunk)
            if dest.stat().st_size < min_bytes:
                raise ValueError(f"Unexpectedly small asset {name}: {dest.stat().st_size}")
            return dest
        except Exception as exc:
            print(f"download retry {attempt+1}/3 {name}: {type(exc).__name__} {exc}", flush=True)
            dest.unlink(missing_ok=True)
            time.sleep(2 + attempt * 2)
    raise RuntimeError(f"Could not download verified licensed real footage: {name}")


def probe(path: Path) -> dict:
    output = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_format", "-show_streams",
        "-of", "json", str(path),
    ])
    return json.loads(output)


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_NORMAL, size)


def fit_text(d: ImageDraw.ImageDraw, text: str, max_w: int, base: int) -> ImageFont.FreeTypeFont:
    size = base
    while size > 38:
        candidate = font(size)
        if d.textbbox((0, 0), text, font=candidate, stroke_width=0)[2] < max_w:
            return candidate
        size -= 3
    return font(size)


def overlay_png(index: int, title: str, subtitle: str, eyebrow: str) -> Path:
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    px = img.load()
    # A mild cinematic shadow for legible text, not a full-screen graphic.
    for y in range(0, 860):
        alpha = int(172 * (1 - y / 860) ** 1.35)
        for x in range(1080):
            px[x, y] = (0, 0, 0, alpha)
    for y in range(1480, 1920):
        alpha = int(85 * ((y - 1480) / 440))
        for x in range(1080):
            px[x, y] = (0, 0, 0, alpha)

    d = ImageDraw.Draw(img)
    d.rounded_rectangle((64, 118, 92, 168), radius=5, fill=ORANGE)
    d.text((111, 124), "OKRETAJI", font=font(32), fill="white",
           stroke_width=0)
    d.text((65, 223), eyebrow.upper(), font=font(28, bold=False),
           fill=(232, 232, 232, 240))
    d.text((61, 282), title, font=fit_text(d, title, 962, 91), fill="white",
           stroke_width=1, stroke_fill=(0, 0, 0, 100))
    d.text((61, 398), subtitle, font=fit_text(d, subtitle, 962, 78),
           fill=ORANGE, stroke_width=1, stroke_fill=(0, 0, 0, 100))
    d.rectangle((65, 536, 222, 543), fill=ORANGE)
    d.text((65, 1735), "TEHNIKA U POKRETU", font=font(25, bold=False),
           fill=(255, 255, 255, 220))
    d.text((877, 1735), f"{index:02d} / 06", font=font(26, bold=False),
           fill=(255, 255, 255, 220))
    path = WORK / f"overlay_{index:02d}.png"
    img.save(path)
    return path


def encode_segment(index: int, clip: Path, overlay: Path, offset: float, seconds: float) -> Path:
    dest = WORK / f"segment_{index:02d}.mp4"
    fx = (
        "fps=24,"
        "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,"
        "crop=1080:1920,"
        "eq=contrast=1.08:saturation=1.10:brightness=-0.015,"
        "format=yuv420p"
    )
    # Text appears over actual moving footage; fade over first 0.12 s.
    filt = (
        f"[0:v]{fx}[base];"
        "[1:v]format=rgba,fade=t=in:st=0:d=0.13:alpha=1[txt];"
        "[base][txt]overlay=0:0:shortest=1:format=auto,format=yuv420p[v]"
    )
    run(
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-ss", f"{offset:.2f}", "-i", str(clip),
        "-loop", "1", "-i", str(overlay),
        "-filter_complex", filt, "-map", "[v]",
        "-t", f"{seconds:.2f}", "-an",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
        "-profile:v", "high", "-level", "4.2",
        "-r", "24", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", str(dest),
    )
    return dest


def make_contact_sheet(final: Path) -> Path:
    import io
    times = [0.3, 2.75, 5.3, 7.9, 11.0, 13.8]
    sheet = Image.new("RGB", (1080, 960), "#101b24")
    d = ImageDraw.Draw(sheet)
    for i, t in enumerate(times):
        jpg = subprocess.check_output([
            "ffmpeg", "-hide_banner", "-loglevel", "error",
            "-ss", str(t), "-i", str(final),
            "-frames:v", "1", "-vf", "scale=330:586",
            "-f", "image2pipe", "-vcodec", "mjpeg", "pipe:1",
        ])
        frame = Image.open(io.BytesIO(jpg)).convert("RGB")
        x = (i % 3) * 360 + 15
        y = (i // 3) * 480 + 15
        # Crop frame for a compact 3x2 proof sheet.
        frame.thumbnail((330, 435))
        sheet.paste(frame, (x, y))
        d.text((x, y + 438), f"{t:.2f} s", font=font(21), fill="white")
    out = OUT / "okretaji_stvarni_kadrovi_kontrola.jpg"
    sheet.save(out, quality=88)
    return out


def main() -> None:
    source: dict[str, Path] = {}
    for name, (url, _) in VIDEO.items():
        source[name] = download_asset(url, f"mixkit_{name}.mp4")
        p = probe(source[name])
        if not any(s["codec_type"] == "video" for s in p["streams"]):
            raise RuntimeError(f"File is not video: {name}")
        print(f"SOURCE {name}: {source[name].stat().st_size} bytes, {p['format'].get('duration')} s")

    segments = []
    for i, (name, duration, offset, title, subtitle, eyebrow) in enumerate(CLIPS, 1):
        img = overlay_png(i, title, subtitle, eyebrow)
        segments.append(encode_segment(i, source[name], img, offset, duration))

    filelist = WORK / "concat.txt"
    filelist.write_text(
        "".join(f"file '{path.resolve()}'\n" for path in segments), encoding="utf-8"
    )
    silent = WORK / "picture.mp4"
    run("ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "concat", "-safe", "0", "-i", str(filelist),
        "-c", "copy", "-movflags", "+faststart", str(silent))

    # Real motorcycles recorded by Mixkit, not synthetic simulated sounds.
    rev = download_asset(SOUND["rev"][0], "mixkit_real_motorcycle_rev.wav", 10_000)
    passing = download_asset(SOUND["pass"][0], "mixkit_real_bike_pass.wav", 10_000)
    final = OUT / "okretaji_moto_guma_stvarne_snimke_1080x1920.mp4"
    run(
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(silent),
        "-stream_loop", "-1", "-i", str(rev),
        "-i", str(passing),
        "-filter_complex",
        "[1:a]atrim=duration=15.3,asetpts=PTS-STARTPTS,volume=0.49,"
        "afade=t=in:st=0:d=0.12,afade=t=out:st=14.35:d=0.9[engine];"
        "[2:a]atrim=duration=1.2,asetpts=PTS-STARTPTS,volume=0.5[pass];"
        "[engine][pass]amix=inputs=2:duration=first:normalize=0,"
        "alimiter=limit=0.90[a]",
        "-map", "0:v:0", "-map", "[a]", "-t", "15.30",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
        "-movflags", "+faststart", str(final),
    )

    info = probe(final)
    streams = info["streams"]
    v = next(s for s in streams if s["codec_type"] == "video")
    a = next((s for s in streams if s["codec_type"] == "audio"), None)
    assert (v["width"], v["height"]) == (1080, 1920)
    assert a is not None, "Audio track missing"
    duration = float(info["format"]["duration"])
    assert 15.0 <= duration <= 15.5, f"Bad video length {duration}"
    run("ffmpeg", "-v", "error", "-i", str(final), "-f", "null", "-")
    poster = OUT / "okretaji_moto_guma_naslovnica.jpg"
    run("ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-ss", "0.35", "-i", str(final), "-frames:v", "1",
        "-q:v", "3", str(poster))
    sheet = make_contact_sheet(final)
    manifest = {
        "status": "REVIEW_ONLY_NOT_PUBLISHED",
        "title": "Što guma radi kad nagneš motor?",
        "file": final.name,
        "duration_seconds": duration,
        "video_codec": v["codec_name"],
        "video_width": v["width"],
        "video_height": v["height"],
        "audio_codec": a["codec_name"],
        "clips": [
            {"key": k, "download_url": u, "source_page": page,
             "license": "Mixkit Stock Video Free License"}
            for k, (u, page) in VIDEO.items()
        ],
        "sound": [
            {"key": k, "download_url": u, "source_page": page,
             "license": "Mixkit Sound Effects Free License"}
            for k, (u, page) in SOUND.items()
        ],
    }
    (OUT / "sources_and_qa.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("DELIVERABLES:", final, poster, sheet, flush=True)
    print("PASS: real footage, dynamic 9:16 H.264/AAC with complete decode", flush=True)


if __name__ == "__main__":
    main()
