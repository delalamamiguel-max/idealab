"""
Telecom Market Intelligence Pipeline
======================================

Orchestrates the 3-agent pipeline:

    1. Ingestion Agent   → scrapes websites + Reddit via Apify
    2. Classification Agent → LLM-powered signal classification
    3. Reasoning Agent   → synthesizes signals into actionable insights

Usage from the main app:
    from telecom_intel.pipeline import TelecomIntelPipeline
    pipeline = TelecomIntelPipeline(openai_client=client)
    report = pipeline.run(mode="dry_run")
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from telecom_intel.config import OUTPUT_DIR, CACHE_DIR, SIGNAL_CACHE_TTL_SECONDS
from telecom_intel.models import (
    MarketSignal,
    ClassifiedSignal,
    MarketInsight,
    PipelineReport,
)
from telecom_intel.ingestion_agent import run_ingestion
from telecom_intel.classification_agent import (
    run_classification,
    load_cached_signals,
)
from telecom_intel.reasoning_agent import run_reasoning

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Sample data for dry-run mode (no Apify calls)
# ---------------------------------------------------------------------------

SAMPLE_RAW_SIGNALS: list[MarketSignal] = [
    MarketSignal(
        url="https://www.t-mobile.com/cell-phone-plans",
        title="T-Mobile Unlimited Plans — Save on Family Plans",
        content=(
            "T-Mobile Plans\n\n"
            "Go5G: $75/mo per line. Go5G Plus: $90/mo per line.\n"
            "New! Go5G Next with Netflix included. Save $10/mo when you "
            "switch from Verizon or AT&T. Limited time offer — "
            "free line with 3+ lines. Price lock guarantee."
        ),
        source_type="website",
        ingested_at=datetime.now(timezone.utc).isoformat(),
    ),
    MarketSignal(
        url="https://www.verizon.com/plans/unlimited/",
        title="Verizon Unlimited Plans — myPlan",
        content=(
            "Verizon myPlan\n\n"
            "Unlimited Welcome: $65/mo. Unlimited Plus: $80/mo.\n"
            "Unlimited Ultimate: $90/mo. Add perks like Disney+, "
            "Walmart+, Apple One for $10/mo each. New pricing effective "
            "April 2026."
        ),
        source_type="website",
        ingested_at=datetime.now(timezone.utc).isoformat(),
    ),
    MarketSignal(
        url="https://www.t-mobile.com/support/phones-tablets-devices/software-updates/",
        title="T-Mobile Software Updates",
        content=(
            "Software Updates\n\n"
            "Samsung Galaxy S25 Ultra: Android 16 update available (April 2026).\n"
            "Security patch level: April 1, 2026. Bug fixes and performance "
            "improvements. OTA rollout in progress."
        ),
        source_type="website",
        ingested_at=datetime.now(timezone.utc).isoformat(),
    ),
    MarketSignal(
        url="https://www.verizon.com/support/software-updates/",
        title="Verizon Device Software Updates",
        content=(
            "Verizon Software Updates\n\n"
            "iPhone 16 Pro: iOS 19.4 carrier update available.\n"
            "Pixel 9: April 2026 security patch. Samsung Galaxy S25: "
            "Android 16 OTA. System update includes 5G SA improvements."
        ),
        source_type="website",
        ingested_at=datetime.now(timezone.utc).isoformat(),
    ),
    MarketSignal(
        url="https://www.tmonews.com/2026/04/t-mobile-network-outage-midwest/",
        title="T-Mobile Network Outage Affects Midwest Customers",
        content=(
            "T-Mobile is experiencing a widespread network outage affecting "
            "customers in the Midwest region. Reports of no signal and "
            "dropped calls have been flooding social media since early "
            "this morning. T-Mobile has acknowledged the service disruption "
            "and says engineers are working to restore connectivity."
        ),
        source_type="website",
        ingested_at=datetime.now(timezone.utc).isoformat(),
    ),
    MarketSignal(
        url="https://www.bestphoneplans.net/news/cell-phone-plan-changelog",
        title="Cell Phone Plan Changelog — April 2026",
        content=(
            "Plan Changelog April 2026\n\n"
            "- AT&T: ValuePlus plan discontinued, replaced by AT&T Value tier at $50/mo\n"
            "- T-Mobile: Go5G price lock extended through 2027\n"
            "- Verizon: myPlan perks now include Max (HBO) bundle\n"
            "- Google Fi: Simply Unlimited raised to $55/mo (was $50/mo)\n"
            "- Policy change: Verizon updated eligibility requirements for "
            "military discount — now requires active duty verification."
        ),
        source_type="website",
        ingested_at=datetime.now(timezone.utc).isoformat(),
    ),
    MarketSignal(
        url="https://www.reddit.com/r/tmobile/comments/abc123/",
        title="T-Mobile just raised my bill by $5 with no warning",
        content=(
            "T-Mobile just raised my bill by $5 with no warning\n\n"
            "Been a customer for 8 years. Just got my bill and it's $5 more "
            "per line. No email, no notification. This is terrible customer "
            "service. Thinking about switching to Verizon. Anyone else see this?"
        ),
        source_type="reddit",
        ingested_at=datetime.now(timezone.utc).isoformat(),
        subreddit="tmobile",
    ),
    MarketSignal(
        url="https://www.reddit.com/r/Fios/comments/def456/",
        title="Verizon Fios has been down for 3 hours in NJ",
        content=(
            "Verizon Fios has been down for 3 hours in NJ\n\n"
            "Internet and TV completely down since 2pm. Called support and "
            "they said it's a known outage in the area. No ETA for fix. "
            "This is the third outage this month. Frustrated beyond belief."
        ),
        source_type="reddit",
        ingested_at=datetime.now(timezone.utc).isoformat(),
        subreddit="Fios",
    ),
    MarketSignal(
        url="https://www.reddit.com/r/tmobile/comments/ghi789/",
        title="Switched from AT&T to T-Mobile — best decision ever",
        content=(
            "Switched from AT&T to T-Mobile — best decision ever\n\n"
            "Was paying $85/mo on AT&T for one line. Switched to T-Mobile "
            "Go5G for $75/mo and the coverage is actually better in my area. "
            "Love the price lock guarantee. Highly recommend making the switch."
        ),
        source_type="reddit",
        ingested_at=datetime.now(timezone.utc).isoformat(),
        subreddit="tmobile",
    ),
    MarketSignal(
        url="https://www.reddit.com/r/GoogleFi/comments/jkl012/",
        title="Google Fi price increase is ridiculous",
        content=(
            "Google Fi price increase is ridiculous\n\n"
            "Simply Unlimited went from $50 to $55/mo. That's a 10% increase! "
            "For what? The service hasn't improved at all. Terrible value now. "
            "Looking at Mint Mobile or US Mobile as alternatives. Avoid Google Fi."
        ),
        source_type="reddit",
        ingested_at=datetime.now(timezone.utc).isoformat(),
        subreddit="GoogleFi",
    ),
    MarketSignal(
        url="https://www.reddit.com/r/ATT/comments/mno345/",
        title="AT&T just changed their trade-in policy again",
        content=(
            "AT&T just changed their trade-in policy again\n\n"
            "New terms of service update: trade-in values now require 36-month "
            "installment agreement instead of 24. Also changed eligibility "
            "requirements for the premium unlimited plan. Read the fine print "
            "before you commit."
        ),
        source_type="reddit",
        ingested_at=datetime.now(timezone.utc).isoformat(),
        subreddit="ATT",
    ),
    MarketSignal(
        url="https://www.reddit.com/r/NoContract/comments/pqr678/",
        title="NoContract: Best prepaid plans right now?",
        content=(
            "NoContract: Best prepaid plans right now?\n\n"
            "Looking for the best prepaid plan under $40/mo with at least "
            "15GB data. Currently on Cricket (AT&T network) but open to "
            "T-Mobile MVNOs. Visible (Verizon) looks interesting at $25/mo. "
            "What's the best deal right now?"
        ),
        source_type="reddit",
        ingested_at=datetime.now(timezone.utc).isoformat(),
        subreddit="NoContract",
    ),
]


# ---------------------------------------------------------------------------
# Pipeline class
# ---------------------------------------------------------------------------

class TelecomIntelPipeline:
    """
    Orchestrates the full telecom intelligence pipeline.

    Modes:
        - "live"        → Runs Apify scrapers, then LLM classification, then reasoning
        - "dry_run"     → Uses sample data, runs LLM classification + reasoning
        - "cached"      → Loads most recent signals from disk, runs reasoning only
        - "web_search"  → Loads real signals from web_search JSON files (Apify bypass)
    """

    def __init__(
        self,
        openai_client: Any = None,
        use_llm: bool = True,
    ):
        self.openai_client = openai_client
        self.use_llm = use_llm
        self._last_report: Optional[PipelineReport] = None

    @property
    def last_report(self) -> Optional[PipelineReport]:
        return self._last_report

    def _load_web_search_signals(self) -> list[MarketSignal]:
        """
        Load real market signals from web_search JSON files on disk.

        This is the Apify bypass: when the corporate network blocks
        api.apify.com, signals can be collected via external web search
        and saved as JSON files in output/raw/web_search_signals_*.json.

        Each JSON file should contain a list of objects with at minimum:
            url, title, content, source_type, ingested_at

        Returns list of MarketSignal objects, newest file first.
        """
        from telecom_intel.config import RAW_DIR

        pattern = "web_search_signals_*.json"
        files = sorted(RAW_DIR.glob(pattern), reverse=True)  # newest first

        if not files:
            logger.warning("No web_search signal files found in %s", RAW_DIR)
            return []

        # Load the most recent file
        target = files[0]
        logger.info("Loading web_search signals from %s", target)

        try:
            data = json.loads(target.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            logger.error("Failed to read web_search signals: %s", exc)
            return []

        signals = []
        for item in data:
            if not isinstance(item, dict):
                continue
            content = item.get("content", "")
            if not content or not content.strip():
                continue

            signals.append(MarketSignal(
                url=item.get("url", ""),
                title=item.get("title", ""),
                content=content,
                source_type=item.get("source_type", "web_search"),
                ingested_at=item.get("ingested_at", datetime.now(timezone.utc).isoformat()),
                subreddit=item.get("subreddit", ""),
                metadata={
                    "provider": item.get("provider", ""),
                    "signal_type": item.get("signal_type", ""),
                    "source_citation": item.get("source_citation", ""),
                },
            ))

        logger.info("Loaded %d web_search signals from %s", len(signals), target.name)
        return signals

    def run(
        self,
        mode: str = "dry_run",
        *,
        progress_callback: Any = None,
    ) -> PipelineReport:
        """
        Execute the pipeline.

        Parameters
        ----------
        mode : str
            "live" | "dry_run" | "cached" | "web_search"
        progress_callback : callable or None
            Optional callback(stage, current, total) for UI progress.

        Returns
        -------
        PipelineReport
        """
        logger.info("=" * 60)
        logger.info("TELECOM INTEL PIPELINE — mode=%s, llm=%s", mode, self.use_llm)
        logger.info("=" * 60)

        start_time = datetime.now(timezone.utc)

        # ── Phase 1: Ingestion ──
        if mode == "live":
            if progress_callback:
                progress_callback("ingestion", 0, 3)
            ingestion_result = run_ingestion()
            raw_signals = ingestion_result["all_signals"]
            if progress_callback:
                progress_callback("ingestion", 1, 3)

        elif mode == "web_search":
            # ── Apify bypass: load real signals from web_search JSON files ──
            if progress_callback:
                progress_callback("ingestion", 0, 3)
            raw_signals = self._load_web_search_signals()
            if not raw_signals:
                logger.warning("No web_search signals found — falling back to dry_run")
                raw_signals = SAMPLE_RAW_SIGNALS
                mode = "dry_run"
            else:
                logger.info("Web search mode — loaded %d real signals from disk", len(raw_signals))
            if progress_callback:
                progress_callback("ingestion", 1, 3)

        elif mode == "cached":
            if progress_callback:
                progress_callback("loading_cache", 0, 3)
            cached = load_cached_signals()
            if cached:
                logger.info("Loaded %d cached signals — skipping ingestion + classification", len(cached))
                if progress_callback:
                    progress_callback("reasoning", 2, 3)
                reasoning_result = run_reasoning(cached)
                report = reasoning_result.get("report")
                if report:
                    report.mode = "from_cache"
                    self._last_report = report
                    if progress_callback:
                        progress_callback("complete", 3, 3)
                    return report
            # Fall through to dry_run if no cache
            logger.warning("No cached signals found — falling back to dry_run mode")
            raw_signals = SAMPLE_RAW_SIGNALS
            mode = "dry_run"
            if progress_callback:
                progress_callback("ingestion", 1, 3)

        else:  # dry_run
            if progress_callback:
                progress_callback("ingestion", 0, 3)
            raw_signals = SAMPLE_RAW_SIGNALS
            logger.info("Dry run — using %d sample signals", len(raw_signals))
            if progress_callback:
                progress_callback("ingestion", 1, 3)

        # ── Phase 2: Classification ──
        if progress_callback:
            progress_callback("classification", 1, 3)

        def _classify_progress(current: int, total: int) -> None:
            if progress_callback:
                progress_callback("classification", current, total)

        classification_result = run_classification(
            raw_signals,
            openai_client=self.openai_client,
            use_llm=self.use_llm and self.openai_client is not None,
            progress_callback=_classify_progress,
        )
        classified_signals = classification_result["signals"]

        if progress_callback:
            progress_callback("classification", 2, 3)

        # ── Phase 3: Reasoning ──
        if progress_callback:
            progress_callback("reasoning", 2, 3)

        reasoning_result = run_reasoning(classified_signals)
        report = reasoning_result.get("report")

        if report:
            report.mode = mode
            self._last_report = report
        else:
            # Build a report if reasoning didn't return one
            report = PipelineReport(
                report_id=f"report-{start_time.strftime('%Y%m%dT%H%M%SZ')}",
                generated_at=start_time.isoformat(),
                mode=mode,
                total_raw_items=len(raw_signals),
                total_signals=len(classified_signals),
                total_insights=len(reasoning_result.get("insights", [])),
                signals=classified_signals,
                insights=reasoning_result.get("insights", []),
                signal_summary=classification_result.get("by_type", {}),
            )
            self._last_report = report

        if progress_callback:
            progress_callback("complete", 3, 3)

        logger.info(
            "Pipeline complete — %d raw → %d classified → %d insights (mode=%s)",
            len(raw_signals), len(classified_signals),
            report.total_insights, mode,
        )

        return report

    def get_context_for_llm(self) -> str:
        """
        Get the latest pipeline report formatted for injection into
        the experimentation agent's LLM context.

        Returns empty string if no report is available.
        """
        if self._last_report:
            return self._last_report.to_context_string()

        # Try loading from cache
        cached = load_cached_signals()
        if cached:
            reasoning_result = run_reasoning(cached)
            report = reasoning_result.get("report")
            if report:
                self._last_report = report
                return report.to_context_string()

        return ""

    def get_signal_count(self) -> int:
        """Return the number of signals in the last report."""
        if self._last_report:
            return self._last_report.total_signals
        return 0

    def get_insight_count(self) -> int:
        """Return the number of insights in the last report."""
        if self._last_report:
            return self._last_report.total_insights
        return 0
