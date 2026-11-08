# Organic growth — zero paid ads

This is a safe first phase: editorial validation, a queue, and reporting. It does **not** post to Instagram/Facebook, run ads, follow accounts, scrape users, or generate unverified sports results.

## Queue
Add objects to `queue.json` with: `id`, `title`, `topic` (f1/motogp/automobili/tehnologija/energija), `url` (HTTPS okretaji.com article), `caption`, `status` (draft/approved/published), `verified` (boolean). Optional `media_type: reel` requires a publicly hosted HTTPS `media_url` and `media_rights_confirmed: true`.

Only verified, approved entries are eligible for later publishing. Do not automatically treat RSS articles as verified. Confirm event results against official sources, ensure media licenses and attribution, and write original Croatian captions without generic AI phrasing.

## Reporting
Run `python automation/growth.py`. Optional `--metrics metrics.csv` accepts: `date,platform,topic,views,reach,followers_gained,website_clicks`. Report is uploaded as an Actions artifact. Do not commit access tokens, private analytics exports or user data.

## Next integration gate
Before enabling Meta posting, verify existing workflows, permissions, page/IG IDs, token validity, deduplication and retry handling. Implement a separate explicit publishing switch, default off. For Reels use the official media-container/status/publish flow; never publish until the container is ready. Do not publish unverified results or unlicensed media.

No ads or paid APIs are required.
