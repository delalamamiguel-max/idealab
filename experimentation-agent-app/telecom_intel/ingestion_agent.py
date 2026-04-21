"""
Telecom Knowledge Ingestion Agent
==================================

Purpose:
    Collect raw telecom market data from approved public websites and Reddit
    communities using the Apify platform.

Responsibilities:
    - Invoke Apify Website Content Crawler for official sites, news, and changelogs
    - Invoke Apify Reddit Scraper for subreddit monitoring
    - Return raw scraped data only
    - Do NOT summarize, classify, or reason

Rules:
    - Scrape only the explicitly listed URLs and subreddits (see config.py)
    - Do not scrape paywalled or licensed sources
    - Always preserve source URL and timestamp
"""

from __future__ import annotations

import json
import ssl
import time
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from telecom_intel.config import (
    APIFY_API_TOKEN,
    APIFY_BASE_URL,
    APIFY_WEBSITE_CRAWLER_ACTOR,
    APIFY_REDDIT_SCRAPER_ACTOR,
    APPROVED_URLS,
    APPROVED_SUBREDDITS,
    BLOCKED_URLS,
    CRAWLER_TYPE,
    MAX_CRAWL_DEPTH,
    SAVE_MARKDOWN,
    SAVE_HTML,
    REDDIT_POSTS_LIMIT,
    REDDIT_COMMENTS_LIMIT,
    REDDIT_SORT,
    REDDIT_INCLUDE_COMMENTS,
    APIFY_POLL_INTERVAL_SECONDS,
    APIFY_MAX_WAIT_SECONDS,
    RAW_DIR,
)
from telecom_intel.models import MarketSignal

logger = logging.getLogger(__name__)

# Permissive SSL context for corporate proxies / self-signed certs
_SSL_CTX = ssl.create_default_context()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _actor_run_url(actor_id: str) -> str:
    """Build the Apify actor run endpoint URL."""
    return f"{APIFY_BASE_URL}/acts/{actor_id}/runs"


def _validate_urls(urls: list) -> list:
    """Reject any URL that appears in the blocked list."""
    safe: list = []
    for url in urls:
        if any(url.startswith(blocked) for blocked in BLOCKED_URLS):
            logger.warning("BLOCKED — skipping paywalled/licensed URL: %s", url)
        else:
            safe.append(url)
    return safe


def _api_get(url: str, timeout: int = 30) -> dict:
    """HTTP GET returning parsed JSON."""
    sep = "&" if "?" in url else "?"
    full = f"{url}{sep}token={APIFY_API_TOKEN}"
    req = Request(full, method="GET")
    with urlopen(req, context=_SSL_CTX, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def _api_post(url: str, payload: dict, timeout: int = 30) -> dict:
    """HTTP POST with JSON body returning parsed JSON."""
    sep = "&" if "?" in url else "?"
    full = f"{url}{sep}token={APIFY_API_TOKEN}"
    data = json.dumps(payload).encode()
    req = Request(full, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    with urlopen(req, context=_SSL_CTX, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def _poll_run(run_id: str) -> dict:
    """Poll an Apify actor run until it reaches a terminal state."""
    url = f"{APIFY_BASE_URL}/actor-runs/{run_id}"
    elapsed = 0

    while elapsed < APIFY_MAX_WAIT_SECONDS:
        data = _api_get(url)["data"]
        status = data.get("status")
        logger.info("Run %s status: %s (elapsed %ds)", run_id, status, elapsed)

        if status in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
            return data

        time.sleep(APIFY_POLL_INTERVAL_SECONDS)
        elapsed += APIFY_POLL_INTERVAL_SECONDS

    raise TimeoutError(f"Apify run {run_id} did not finish within {APIFY_MAX_WAIT_SECONDS}s")


def _fetch_dataset(dataset_id: str) -> list:
    """Download all items from an Apify dataset."""
    url = f"{APIFY_BASE_URL}/datasets/{dataset_id}/items?format=json&clean=true"
    sep = "&" if "?" in url else "?"
    full = f"{url}{sep}token={APIFY_API_TOKEN}"
    req = Request(full, method="GET")
    with urlopen(req, context=_SSL_CTX, timeout=120) as resp:
        return json.loads(resp.read().decode())


# ---------------------------------------------------------------------------
# Website Content Crawler
# ---------------------------------------------------------------------------

def scrape_websites(
    urls: list | None = None,
    *,
    crawler_type: str = CRAWLER_TYPE,
    max_crawl_depth: int = MAX_CRAWL_DEPTH,
    save_markdown: bool = SAVE_MARKDOWN,
    save_html: bool = SAVE_HTML,
) -> list[MarketSignal]:
    """
    Launch the Apify Website Content Crawler for the given URLs.
    Returns list of MarketSignal objects.
    """
    urls = _validate_urls(urls or APPROVED_URLS)
    if not urls:
        logger.error("No valid URLs to scrape after filtering.")
        return []

    payload = {
        "startUrls": [{"url": u} for u in urls],
        "crawlerType": crawler_type,
        "maxCrawlDepth": max_crawl_depth,
        "saveMarkdown": save_markdown,
        "saveHtml": save_html,
    }

    logger.info("Starting Website Content Crawler for %d URLs …", len(urls))

    # 1. Start the actor run
    resp = _api_post(_actor_run_url(APIFY_WEBSITE_CRAWLER_ACTOR), payload)
    run_id = resp["data"]["id"]
    logger.info("Crawler run started — id=%s", run_id)

    # 2. Poll until finished
    final = _poll_run(run_id)
    if final["status"] != "SUCCEEDED":
        logger.error("Crawler run %s ended with status %s", run_id, final["status"])
        return []

    # 3. Fetch dataset
    items = _fetch_dataset(final["defaultDatasetId"])

    # 4. Convert to MarketSignal objects
    now = datetime.now(timezone.utc).isoformat()
    signals = []
    for item in items:
        title = item.get("title", "") or ""
        if not title and isinstance(item.get("metadata"), dict):
            title = item["metadata"].get("title", "")
        content = item.get("markdown", "") or item.get("text", "") or ""
        url = item.get("url", "") or item.get("loadedUrl", "") or ""

        if not content.strip():
            continue

        signals.append(MarketSignal(
            url=url,
            title=title,
            content=content,
            source_type="website",
            ingested_at=now,
            metadata={k: v for k, v in item.items()
                      if k not in ("markdown", "text", "html") and not k.startswith("_")},
        ))

    logger.info("Website crawl complete — %d signals collected.", len(signals))
    return signals


# ---------------------------------------------------------------------------
# Reddit Scraper
# ---------------------------------------------------------------------------

def scrape_reddit(
    subreddits: list | None = None,
    *,
    posts_limit: int = REDDIT_POSTS_LIMIT,
    comments_limit: int = REDDIT_COMMENTS_LIMIT,
    sort: str = REDDIT_SORT,
    include_comments: bool = REDDIT_INCLUDE_COMMENTS,
) -> list[MarketSignal]:
    """
    Launch the Apify Reddit Scraper for the given subreddits.
    Returns list of MarketSignal objects.
    """
    subreddits = subreddits or APPROVED_SUBREDDITS

    start_urls = [{"url": f"https://www.reddit.com/r/{sub}"} for sub in subreddits]

    payload = {
        "startUrls": start_urls,
        "maxItems": posts_limit,
        "maxComments": comments_limit,
        "sort": sort,
        "includeComments": include_comments,
        "skipComments": not include_comments,
    }

    logger.info("Starting Reddit Scraper for %d subreddits …", len(subreddits))

    resp = _api_post(_actor_run_url(APIFY_REDDIT_SCRAPER_ACTOR), payload)
    run_id = resp["data"]["id"]
    logger.info("Reddit scraper run started — id=%s", run_id)

    final = _poll_run(run_id)
    if final["status"] != "SUCCEEDED":
        logger.error("Reddit run %s ended with status %s", run_id, final["status"])
        return []

    items = _fetch_dataset(final["defaultDatasetId"])

    now = datetime.now(timezone.utc).isoformat()
    signals = []
    for item in items:
        title = item.get("title", "") or item.get("parsedTitle", "") or ""
        body = item.get("body", "") or item.get("text", "") or item.get("selftext", "") or ""
        url = item.get("url", "") or item.get("permalink", "") or ""
        if url and not url.startswith("http"):
            url = f"https://www.reddit.com{url}"
        subreddit = item.get("subreddit", "") or item.get("dataSubreddit", "") or ""

        content = f"{title}\n\n{body}" if body else title
        if not content.strip():
            continue

        signals.append(MarketSignal(
            url=url,
            title=title,
            content=content,
            source_type="reddit",
            ingested_at=now,
            subreddit=subreddit,
            metadata={k: v for k, v in item.items()
                      if k not in ("body", "text", "selftext", "html")
                      and not k.startswith("_")},
        ))

    logger.info("Reddit scrape complete — %d signals collected.", len(signals))
    return signals


# ---------------------------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------------------------

def _save_raw(signals: list[MarketSignal], label: str) -> Path:
    """Write raw signals to a timestamped JSON file under output/raw/."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = RAW_DIR / f"{label}_{ts}.json"
    data = [
        {
            "url": s.url,
            "title": s.title,
            "content": s.content[:2000],  # Truncate for storage
            "source_type": s.source_type,
            "ingested_at": s.ingested_at,
            "subreddit": s.subreddit,
        }
        for s in signals
    ]
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    logger.info("Saved %d raw signals → %s", len(signals), path)
    return path


# ---------------------------------------------------------------------------
# Public orchestration entry-point
# ---------------------------------------------------------------------------

def run_ingestion() -> dict:
    """
    Execute the full ingestion pipeline:
      1. Crawl approved websites
      2. Scrape approved subreddits
      3. Persist raw JSON to disk
      4. Return a manifest with MarketSignal objects

    Returns dict with keys: website_signals, reddit_signals, all_signals, etc.
    """
    logger.info("=" * 60)
    logger.info("TELECOM KNOWLEDGE INGESTION AGENT — starting")
    logger.info("=" * 60)

    website_signals = scrape_websites()
    if website_signals:
        _save_raw(website_signals, "websites")

    reddit_signals = scrape_reddit()
    if reddit_signals:
        _save_raw(reddit_signals, "reddit")

    all_signals = website_signals + reddit_signals

    manifest = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "website_count": len(website_signals),
        "reddit_count": len(reddit_signals),
        "total_count": len(all_signals),
        "all_signals": all_signals,
    }

    logger.info("Ingestion complete — %d website signals, %d Reddit signals",
                len(website_signals), len(reddit_signals))
    return manifest
