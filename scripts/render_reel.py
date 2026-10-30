#!/usr/bin/env python3
"""Render an Okretaji vertical Reel from licensed local clips and a JSON project.

No stock-site scraping/API calls. Every clip must already be downloaded by an editor
and have a matching rights record in assets/reels/credits.json.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets" / "reels"
CLIPS = ASSETS / "clips"
PROJECTS = ASSETS / "projects"
CREDITS = ASSETS / "credits.json"
OUT = ROOT / "reels"


def run(args):
    subprocess.run(args, check=True)


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def safe_text(value):
    return str(value or "").replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'").replace("%", "\\%")


def validate(project):
    if project.get("format") != "vertical-9x16":
        raise ValueError("Projekt mora imati format vertical-9x16.")
    if not project.get("segments"):
        raise ValueError("Projekt nema segmente.")
    credits = load_json(CREDITS) if CREDITS.exists() else {}
    for seg in project["segments"]:
        filename = Path(seg["clip"]).name
        clip = CLIPS / filename
        if not clip.is_file():
            raise FileNotFoundError(f"Nedostaje video kadar: {clip}")
        record = credits.get(filename)
        if not record:
            raise ValueError(f"Nedostaje zapis licence za {filename} u credits.json")
        if not record.get("source_url") or not record.get("license"):
            raise ValueError(f"Zapis licence za {filename} nema source_url ili license.")
        if record.get("commercial_use") is not True:
            raise ValueError(f"Komercijalna uporaba nije izričito dopuštena za {filename}.")
        if record.get("reviewed") is not True:
            raise ValueError(f"Licenca za {filename} nije označena kao reviewed=true.")
        if float(seg.get("duration", 0)) <= 0:
            raise ValueError("Svaki segment mora imati trajanje veće od nule.")
    return credits


def render(project_path):
    project = load_json(project_path)
    credits = validate(project)
    OUT.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-z0-9-]+", "-", project.get("slug", "okretaji-reel").lower()).strip("-")
    temp = OUT / (slug + "-parts")
    temp.mkdir(exist_ok=True)
    parts = []
    for i, seg in enumerate(project["segments"], 1):
        source = CLIPS / Path(seg["clip"]).name
        duration = float(seg["duration"])
        vf = (
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,setsar=1,fps=30,format=yuv420p"
        )
        # Text overlay uses a safe text file to support Croatian diacritics.
        text_file = temp / f"caption-{i}.txt"
        text_file.write_text(seg.get("overlay", ""), encoding="utf-8")
        escaped = str(text_file).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
        vf += (
            f",drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
            f"textfile='{escaped}':fontcolor=white:fontsize=58:"
            "box=1:boxcolor=0x081923@0.82:boxborderw=24:"
            "x=(w-text_w)/2:y=h*0.68"
        )
        part = temp / f"part-{i:02d}.mp4"
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(seg.get("start", 0)),
             "-i", str(source), "-t", str(duration), "-vf", vf,
             "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "21",
             "-r", "30", "-pix_fmt", "yuv420p", str(part)])
        parts.append(part)
    concat = temp / "concat.txt"
    concat.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    output = OUT / f"{slug}.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", str(concat), "-c", "copy", "-movflags", "+faststart", str(output)])

    # Attach a voice track only when a human/editor has supplied a licensed narration file.
    narration = project.get("narration_file")
    if narration:
        audio = ROOT / narration
        if not audio.is_file():
            raise FileNotFoundError(f"Nedostaje naracija: {audio}")
        with_audio = OUT / f"{slug}-with-audio.mp4"
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(output), "-i", str(audio),
             "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac",
             "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(with_audio)])
        output = with_audio

    # Export credit sheet next to video.
    used = {Path(s["clip"]).name for s in project["segments"]}
    credit_file = OUT / f"{slug}-credits.json"
    credit_file.write_text(json.dumps({k: credits[k] for k in sorted(used)}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Gotov video: {output}")
    print(f"Evidencija licenci: {credit_file}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project", help="JSON projekt unutar assets/reels/projects/")
    args = parser.parse_args()
    path = (PROJECTS / args.project).resolve()
    if PROJECTS.resolve() not in path.parents:
        raise ValueError("Projekt mora biti unutar assets/reels/projects/")
    render(path)


if __name__ == "__main__":
    main()
