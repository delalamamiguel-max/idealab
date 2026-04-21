"""
Telecom Intel — Configuration

Central configuration for the telecom intelligence pipeline.
Reads from the parent app's .env file for API keys.
"""

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

TELECOM_INTEL_DIR = Path(__file__).resolve().parent
APP_DIR = TELECOM_INTEL_DIR.parent
OUTPUT_DIR = TELECOM_INTEL_DIR / "output"
RAW_DIR = OUTPUT_DIR / "raw"
SIGNALS_DIR = OUTPUT_DIR / "signals"
INSIGHTS_DIR = OUTPUT_DIR / "insights"
CACHE_DIR = OUTPUT_DIR / "cache"

for _d in (OUTPUT_DIR, RAW_DIR, SIGNALS_DIR, INSIGHTS_DIR, CACHE_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Apify
# ---------------------------------------------------------------------------

APIFY_API_TOKEN = os.getenv(
    "APIFY_API_TOKEN",
    "",
)
APIFY_BASE_URL = os.getenv("APIFY_BASE_URL", "https://api.apify.com/v2")

APIFY_WEBSITE_CRAWLER_ACTOR = "apify/website-content-crawler"
APIFY_REDDIT_SCRAPER_ACTOR = "trudax/reddit-scraper"

# ---------------------------------------------------------------------------
# Approved scrape targets
# ---------------------------------------------------------------------------

APPROVED_URLS: list = [
    "https://www.t-mobile.com/",
    "https://www.verizon.com/",
    "https://www.tmonews.com/",
    "https://www.bestphoneplans.net/news/cell-phone-plan-changelog",
    "https://www.verizon.com/support/software-updates/",
    "https://www.t-mobile.com/support/phones-tablets-devices/software-updates/",
    "https://www.managevendors.io/vendors/verizon/changelog",
]

APPROVED_SUBREDDITS: list = [
    "tmobile", "tmobileisp", "verizon", "Fios",
    "ATT", "NoContract", "GoogleFi",
]

BLOCKED_URLS: list = [
    "https://www.spglobal.com/",
    "https://www.gsmaintelligence.com/",
]

# ---------------------------------------------------------------------------
# Crawler defaults
# ---------------------------------------------------------------------------

CRAWLER_TYPE = "cheerio"
MAX_CRAWL_DEPTH = 2
SAVE_MARKDOWN = True
SAVE_HTML = False

REDDIT_POSTS_LIMIT = 50
REDDIT_COMMENTS_LIMIT = 20
REDDIT_SORT = "new"
REDDIT_INCLUDE_COMMENTS = True

# ---------------------------------------------------------------------------
# Polling
# ---------------------------------------------------------------------------

APIFY_POLL_INTERVAL_SECONDS = 5
APIFY_MAX_WAIT_SECONDS = 600

# ---------------------------------------------------------------------------
# LLM Classification Config
# ---------------------------------------------------------------------------

# Use a cheaper/faster model for classification to keep costs low
CLASSIFICATION_MODEL = os.getenv("CLASSIFICATION_MODEL", "gpt-4o-mini")
CLASSIFICATION_TEMPERATURE = 0.1  # Low temp for consistent classification
CLASSIFICATION_MAX_TOKENS = 500

# ---------------------------------------------------------------------------
# Cache settings
# ---------------------------------------------------------------------------

# How long cached signals remain valid (seconds)
SIGNAL_CACHE_TTL_SECONDS = int(os.getenv("SIGNAL_CACHE_TTL", "3600"))  # 1 hour default
