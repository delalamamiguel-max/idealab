"""
Telecom Market Reasoning Agent
================================

Purpose:
    Synthesize classified telecom signals into actionable insights.

Responsibilities:
    - Analyze patterns across multiple signals
    - Identify risks, opportunities, and anomalies
    - Generate product, experimentation, or strategy implications

Rules:
    - Never invent facts
    - Always cite supporting signals
    - Do NOT scrape or reclassify data
"""

from __future__ import annotations

import json
import logging
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from telecom_intel.config import INSIGHTS_DIR
from telecom_intel.models import (
    ClassifiedSignal,
    MarketInsight,
    SupportingSignalRef,
    InsightCategory,
    PipelineReport,
    SignalType,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_refs(signals: list[ClassifiedSignal], limit: int = 10) -> list[SupportingSignalRef]:
    """Build SupportingSignalRef list from ClassifiedSignal objects."""
    return [
        SupportingSignalRef(
            signal_id=s.signal_id,
            signal_type=s.signal_type.value,
            provider=s.provider.value,
            title=s.title,
            source_url=s.source_url,
        )
        for s in signals[:limit]
    ]


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M")


# ---------------------------------------------------------------------------
# Pattern detectors
# ---------------------------------------------------------------------------

def _detect_pricing_moves(signals: list[ClassifiedSignal]) -> list[MarketInsight]:
    """Detect pricing-related patterns across providers."""
    pricing = [s for s in signals if s.signal_type == SignalType.PRICING]
    if not pricing:
        return []

    insights: list = []
    by_provider: dict = defaultdict(list)
    for s in pricing:
        by_provider[s.provider.value].append(s)

    if len(by_provider) >= 2:
        providers = list(by_provider.keys())
        insights.append(MarketInsight(
            insight_id=f"pricing-multi-{_ts()}",
            category=InsightCategory.COMPETITIVE_MOVE,
            headline=f"Pricing activity detected across {', '.join(providers)}",
            analysis=(
                f"Multiple providers ({', '.join(providers)}) show pricing-related signals "
                f"within the same collection window. This may indicate competitive pricing "
                f"adjustments or seasonal promotions. Total pricing signals: {len(pricing)}."
            ),
            implications=[
                "Monitor for plan price changes that could affect churn",
                "Consider A/B testing promotional counter-offers",
                "Review competitive positioning of current plans",
            ],
            experiment_recommendations=[
                "Test competitive price-match messaging on wireless PDP",
                "A/B test value-comparison tables highlighting AT&T advantages",
                "Test urgency messaging around competitor price increases",
            ],
            confidence=min(0.6 + len(pricing) * 0.05, 0.95),
            supporting_signals=[r.to_dict() for r in _make_refs(pricing)],
            providers_involved=providers,
            generated_at=datetime.now(timezone.utc).isoformat(),
        ))

    for provider, items in by_provider.items():
        if len(items) >= 3:
            insights.append(MarketInsight(
                insight_id=f"pricing-surge-{provider}-{_ts()}",
                category=InsightCategory.TREND,
                headline=f"High pricing signal volume from {provider} ({len(items)} signals)",
                analysis=(
                    f"{provider} has {len(items)} pricing-related signals in this batch. "
                    f"This concentration suggests active plan restructuring or promotional campaigns."
                ),
                implications=[
                    f"Deep-dive into {provider}'s latest plan changes",
                    "Assess impact on competitive positioning",
                    "Flag for product team review",
                ],
                experiment_recommendations=[
                    f"Test retention offers for customers comparing {provider} plans",
                    "A/B test plan comparison landing page with updated competitor data",
                ],
                confidence=min(0.5 + len(items) * 0.1, 0.9),
                supporting_signals=[r.to_dict() for r in _make_refs(items, 5)],
                providers_involved=[provider],
                generated_at=datetime.now(timezone.utc).isoformat(),
            ))

    return insights


def _detect_outage_patterns(signals: list[ClassifiedSignal]) -> list[MarketInsight]:
    """Detect outage-related patterns."""
    outages = [s for s in signals if s.signal_type == SignalType.OUTAGE]
    if not outages:
        return []

    insights: list = []
    by_provider: dict = defaultdict(list)
    for s in outages:
        by_provider[s.provider.value].append(s)

    for provider, items in by_provider.items():
        if len(items) >= 2:
            insights.append(MarketInsight(
                insight_id=f"outage-{provider}-{_ts()}",
                category=InsightCategory.OPPORTUNITY,
                headline=f"Multiple outage signals for {provider} ({len(items)} reports)",
                analysis=(
                    f"{provider} has {len(items)} outage-related signals. "
                    f"Clustered outage reports may indicate systemic network issues — "
                    f"this is a competitive opportunity for AT&T."
                ),
                implications=[
                    f"Monitor {provider} service status pages",
                    "Prepare competitive messaging if outage is confirmed",
                    "Track customer sentiment for churn opportunity",
                ],
                experiment_recommendations=[
                    f"Test targeted ads to {provider} customers in affected areas",
                    "A/B test network reliability messaging on AT&T landing pages",
                    f"Test win-back offers for former AT&T customers now on {provider}",
                ],
                confidence=min(0.5 + len(items) * 0.15, 0.95),
                supporting_signals=[r.to_dict() for r in _make_refs(items, 5)],
                providers_involved=[provider],
                generated_at=datetime.now(timezone.utc).isoformat(),
            ))

    return insights


def _detect_sentiment_shifts(signals: list[ClassifiedSignal]) -> list[MarketInsight]:
    """Detect customer sentiment patterns from Reddit signals."""
    sentiment = [s for s in signals if s.signal_type == SignalType.CUSTOMER_SENTIMENT]
    if not sentiment:
        return []

    insights: list = []
    by_provider: dict = defaultdict(list)
    for s in sentiment:
        by_provider[s.provider.value].append(s)

    for provider, items in by_provider.items():
        if len(items) >= 3:
            category = InsightCategory.OPPORTUNITY if provider != "att" else InsightCategory.RISK
            insights.append(MarketInsight(
                insight_id=f"sentiment-{provider}-{_ts()}",
                category=category,
                headline=f"Customer sentiment activity for {provider} ({len(items)} signals)",
                analysis=(
                    f"Detected {len(items)} customer sentiment signals for {provider} "
                    f"from Reddit communities. Sentiment patterns can indicate emerging "
                    f"churn risk or competitive opportunity."
                ),
                implications=[
                    "Analyze sentiment polarity (positive vs negative)",
                    "Correlate with recent pricing or policy changes",
                    "Consider proactive customer retention campaigns if negative",
                ],
                experiment_recommendations=[
                    "Test social proof messaging referencing customer satisfaction",
                    "A/B test community-driven testimonials on landing pages",
                ],
                confidence=min(0.4 + len(items) * 0.08, 0.85),
                supporting_signals=[r.to_dict() for r in _make_refs(items, 8)],
                providers_involved=[provider],
                generated_at=datetime.now(timezone.utc).isoformat(),
            ))

    return insights


def _detect_churn_signals(signals: list[ClassifiedSignal]) -> list[MarketInsight]:
    """Detect churn-related signals — customers switching carriers."""
    churn = [s for s in signals if s.signal_type == SignalType.CHURN_SIGNAL]
    if not churn:
        return []

    insights: list = []

    # Check if AT&T is losing customers
    att_churn = [s for s in churn if s.relevance_to_att == "direct"]
    if att_churn:
        insights.append(MarketInsight(
            insight_id=f"churn-att-{_ts()}",
            category=InsightCategory.RISK,
            headline=f"AT&T churn signals detected ({len(att_churn)} mentions)",
            analysis=(
                f"Detected {len(att_churn)} signals where customers mention leaving AT&T "
                f"or switching away. This is a direct retention risk."
            ),
            implications=[
                "Investigate common churn reasons from signal content",
                "Review retention offer effectiveness",
                "Prioritize churn-prevention experiments",
            ],
            experiment_recommendations=[
                "Test proactive retention offers before contract end",
                "A/B test loyalty rewards messaging for long-tenure customers",
                "Test exit-intent interventions on account management pages",
            ],
            confidence=min(0.6 + len(att_churn) * 0.1, 0.95),
            supporting_signals=[r.to_dict() for r in _make_refs(att_churn)],
            providers_involved=["att"],
            generated_at=datetime.now(timezone.utc).isoformat(),
        ))

    # Check if competitors are losing customers (opportunity)
    competitor_churn = [s for s in churn if s.relevance_to_att == "indirect"]
    if competitor_churn:
        providers = list({s.provider.value for s in competitor_churn})
        insights.append(MarketInsight(
            insight_id=f"churn-opportunity-{_ts()}",
            category=InsightCategory.OPPORTUNITY,
            headline=f"Competitor churn signals ({len(competitor_churn)} mentions from {', '.join(providers)})",
            analysis=(
                f"Detected {len(competitor_churn)} signals where customers mention leaving "
                f"competitors ({', '.join(providers)}). This represents a win-back opportunity."
            ),
            implications=[
                "Target dissatisfied competitor customers with switch offers",
                "Highlight AT&T advantages in areas competitors are failing",
            ],
            experiment_recommendations=[
                "Test targeted switch offers for competitor customers",
                "A/B test comparison landing pages highlighting AT&T advantages",
                "Test trade-in value messaging for competitor device owners",
            ],
            confidence=min(0.5 + len(competitor_churn) * 0.08, 0.9),
            supporting_signals=[r.to_dict() for r in _make_refs(competitor_churn)],
            providers_involved=providers,
            generated_at=datetime.now(timezone.utc).isoformat(),
        ))

    return insights


def _detect_software_update_waves(signals: list[ClassifiedSignal]) -> list[MarketInsight]:
    """Detect software update activity patterns."""
    updates = [s for s in signals if s.signal_type == SignalType.SOFTWARE_UPDATE]
    if not updates:
        return []

    insights: list = []
    by_provider: dict = defaultdict(list)
    for s in updates:
        by_provider[s.provider.value].append(s)

    for provider, items in by_provider.items():
        if len(items) >= 2:
            insights.append(MarketInsight(
                insight_id=f"sw-update-{provider}-{_ts()}",
                category=InsightCategory.TREND,
                headline=f"Software update wave from {provider} ({len(items)} updates)",
                analysis=(
                    f"{provider} is pushing {len(items)} software updates. "
                    f"This may indicate a major OS rollout or security patch cycle."
                ),
                implications=[
                    "Align marketing with device update messaging",
                    "Test upgrade prompts for users on affected devices",
                    "Monitor for update-related customer complaints",
                ],
                experiment_recommendations=[
                    "Test device upgrade messaging tied to new OS features",
                    "A/B test 'your device just got better' notification campaigns",
                ],
                confidence=min(0.5 + len(items) * 0.1, 0.9),
                supporting_signals=[r.to_dict() for r in _make_refs(items, 5)],
                providers_involved=[provider],
                generated_at=datetime.now(timezone.utc).isoformat(),
            ))

    return insights


def _detect_policy_changes(signals: list[ClassifiedSignal]) -> list[MarketInsight]:
    """Detect policy/ToS change signals."""
    policy = [s for s in signals if s.signal_type == SignalType.POLICY_CHANGE]
    if not policy:
        return []

    providers = list({s.provider.value for s in policy})

    return [MarketInsight(
        insight_id=f"policy-change-{_ts()}",
        category=InsightCategory.RISK,
        headline=f"Policy/ToS changes detected ({len(policy)} signals across {', '.join(providers)})",
        analysis=(
            f"Detected {len(policy)} policy-related signals from {', '.join(providers)}. "
            f"Policy changes can affect customer eligibility and competitive positioning."
        ),
        implications=[
            "Review policy changes for customer impact",
            "Assess regulatory compliance implications",
            "Prepare customer communications if changes affect existing subscribers",
        ],
        experiment_recommendations=[
            "Test transparent policy communication messaging",
            "A/B test simplified terms presentation on checkout pages",
        ],
        confidence=min(0.5 + len(policy) * 0.1, 0.9),
        supporting_signals=[r.to_dict() for r in _make_refs(policy)],
        providers_involved=providers,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )]


def _detect_competitive_moves(signals: list[ClassifiedSignal]) -> list[MarketInsight]:
    """Detect strategic competitive moves."""
    moves = [s for s in signals if s.signal_type == SignalType.COMPETITIVE_MOVE]
    if not moves:
        return []

    providers = list({s.provider.value for s in moves})
    high_severity = [s for s in moves if s.severity.value in ("critical", "high")]

    category = InsightCategory.RISK if high_severity else InsightCategory.TREND

    return [MarketInsight(
        insight_id=f"competitive-move-{_ts()}",
        category=category,
        headline=f"Competitive moves detected ({len(moves)} signals from {', '.join(providers)})",
        analysis=(
            f"Detected {len(moves)} competitive move signals from {', '.join(providers)}. "
            f"{len(high_severity)} are high/critical severity. "
            f"These may require strategic response."
        ),
        implications=[
            "Assess competitive threat level",
            "Review product roadmap for counter-positioning",
            "Brief leadership on significant competitive shifts",
        ],
        experiment_recommendations=[
            "Test competitive response messaging on key landing pages",
            "A/B test feature comparison tables with updated competitor data",
            "Test urgency-based CTAs referencing market changes",
        ],
        confidence=min(0.6 + len(moves) * 0.08, 0.95),
        supporting_signals=[r.to_dict() for r in _make_refs(moves)],
        providers_involved=providers,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )]


# ---------------------------------------------------------------------------
# Cross-signal anomaly detection
# ---------------------------------------------------------------------------

def _detect_anomalies(signals: list[ClassifiedSignal]) -> list[MarketInsight]:
    """Detect anomalous patterns that don't fit standard categories."""
    insights: list = []
    total = len(signals)

    if total > 5:
        provider_counts = Counter(s.provider.value for s in signals)
        for provider, count in provider_counts.items():
            ratio = count / total
            if ratio > 0.6 and provider != "unknown":
                insights.append(MarketInsight(
                    insight_id=f"anomaly-dominance-{provider}-{_ts()}",
                    category=InsightCategory.ANOMALY,
                    headline=f"{provider} dominates signal volume ({ratio:.0%} of all signals)",
                    analysis=(
                        f"{provider} accounts for {count}/{total} ({ratio:.0%}) of all "
                        f"collected signals. This disproportionate volume may indicate "
                        f"a major event or data collection bias."
                    ),
                    implications=[
                        f"Investigate what's driving high {provider} signal volume",
                        "Check if scraping sources are balanced across providers",
                        "May indicate a newsworthy event worth monitoring",
                    ],
                    confidence=0.7,
                    supporting_signals=[],
                    providers_involved=[provider],
                    generated_at=datetime.now(timezone.utc).isoformat(),
                ))

    general_count = sum(1 for s in signals if s.signal_type == SignalType.GENERAL)
    if total > 5 and general_count / total > 0.4:
        insights.append(MarketInsight(
            insight_id=f"anomaly-unclassified-{_ts()}",
            category=InsightCategory.ANOMALY,
            headline=f"High unclassified signal ratio ({general_count}/{total})",
            analysis=(
                f"{general_count} of {total} signals ({general_count/total:.0%}) could not "
                f"be classified into a specific type. This may indicate new emerging topics "
                f"or classification gaps."
            ),
            implications=[
                "Review unclassified signals for new emerging topics",
                "LLM classification should reduce this — check if fallback is being used",
            ],
            confidence=0.6,
            supporting_signals=[],
            providers_involved=[],
            generated_at=datetime.now(timezone.utc).isoformat(),
        ))

    return insights


# ---------------------------------------------------------------------------
# Main reasoning engine
# ---------------------------------------------------------------------------

def generate_insights(signals: list[ClassifiedSignal]) -> list[MarketInsight]:
    """
    Run all pattern detectors across the classified signals.
    Returns list of MarketInsight sorted by confidence descending.
    """
    all_insights: list = []

    all_insights.extend(_detect_pricing_moves(signals))
    all_insights.extend(_detect_outage_patterns(signals))
    all_insights.extend(_detect_sentiment_shifts(signals))
    all_insights.extend(_detect_churn_signals(signals))
    all_insights.extend(_detect_software_update_waves(signals))
    all_insights.extend(_detect_policy_changes(signals))
    all_insights.extend(_detect_competitive_moves(signals))
    all_insights.extend(_detect_anomalies(signals))

    all_insights.sort(key=lambda i: i.confidence, reverse=True)

    logger.info("Reasoning complete — %d insights generated from %d signals",
                len(all_insights), len(signals))
    return all_insights


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def save_report(report: PipelineReport) -> Path:
    """Write the insight report to a timestamped JSON file."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = INSIGHTS_DIR / f"insight_report_{ts}.json"
    path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    logger.info("Saved insight report → %s", path)
    return path


# ---------------------------------------------------------------------------
# Public entry-point
# ---------------------------------------------------------------------------

def run_reasoning(classified_signals: list[ClassifiedSignal]) -> dict:
    """
    Execute the full reasoning pipeline.

    Parameters
    ----------
    classified_signals : list[ClassifiedSignal]
        Classified signals from the classification agent.

    Returns
    -------
    dict with insights and summary stats.
    """
    logger.info("=" * 60)
    logger.info("TELECOM MARKET REASONING AGENT — starting")
    logger.info("=" * 60)

    if not classified_signals:
        logger.warning("No signals to reason about.")
        return {"insights": [], "total_signals": 0, "total_insights": 0}

    insights = generate_insights(classified_signals)

    type_counts = dict(Counter(s.signal_type.value for s in classified_signals))
    provider_counts = dict(Counter(s.provider.value for s in classified_signals))

    report = PipelineReport(
        report_id=f"report-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        generated_at=datetime.now(timezone.utc).isoformat(),
        mode="live",
        total_raw_items=len(classified_signals),
        total_signals=len(classified_signals),
        total_insights=len(insights),
        signals=classified_signals,
        insights=insights,
        signal_summary={
            "by_type": type_counts,
            "by_provider": provider_counts,
            "total": len(classified_signals),
        },
    )

    save_report(report)

    return {
        "timestamp": report.generated_at,
        "total_signals": len(classified_signals),
        "total_insights": len(insights),
        "insights_by_category": dict(Counter(i.category.value for i in insights)),
        "insights": insights,
        "report": report,
    }
