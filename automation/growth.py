#!/usr/bin/env python3
"""Zero-cost editorial queue validator and organic-growth report (stdlib only)."""
import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "automation" / "queue.json"
REPORT = ROOT / "automation" / "report.json"
TOPICS = {"f1", "motogp", "automobili", "tehnologija", "energija"}

def validate(item):
    errors = []
    for field in ("id", "title", "topic", "url", "caption", "status", "verified"):
        if field not in item:
            errors.append("missing " + field)
    if item.get("topic") not in TOPICS:
        errors.append("invalid topic")
    url = item.get("url", "")
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.netloc not in {"okretaji.com", "www.okretaji.com"}:
        errors.append("url must be an HTTPS Okretaji article")
    if item.get("status") not in {"draft", "approved", "published"}:
        errors.append("invalid status")
    if item.get("status") == "approved" and item.get("verified") is not True:
        errors.append("approved content must be fact checked")
    if item.get("media_type") == "reel":
        media = urlparse(item.get("media_url", ""))
        if media.scheme != "https" or not media.netloc:
            errors.append("reel needs a public HTTPS video URL")
        if item.get("media_rights_confirmed") is not True:
            errors.append("reel media rights not confirmed")
    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics", help="Optional CSV with columns date,platform,topic,views,reach,followers_gained,website_clicks")
    args = parser.parse_args()
    items = json.loads(QUEUE.read_text(encoding="utf-8"))
    if not isinstance(items, list):
        raise ValueError("queue.json must contain a list")
    ids = [i.get("id") for i in items]
    problems = {str(i.get("id", index)): validate(i) for index, i in enumerate(items)}
    if len(ids) != len(set(ids)):
        problems["queue"] = ["duplicate ids"]
    metrics = []
    if args.metrics:
        with open(args.metrics, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                metrics.append(row)
    summary = {}
    for row in metrics:
        topic = row.get("topic", "unknown")
        entry = summary.setdefault(topic, {"views": 0, "reach": 0, "followers_gained": 0, "website_clicks": 0})
        for key in entry:
            entry[key] += int(row.get(key) or 0)
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "publishing_enabled": False,
        "ads_enabled": False,
        "queue_total": len(items),
        "approved_ready": sum(i.get("status") == "approved" and not validate(i) for i in items),
        "validation_errors": {k: v for k, v in problems.items() if v},
        "metrics_by_topic": summary,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["validation_errors"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
