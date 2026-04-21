"""
Telecom Signal Classification Agent — LLM-Powered
====================================================

Purpose:
    Transform raw scraped telecom data into normalized market signals
    using LLM-powered classification instead of keyword rules.

Responsibilities:
    - Accept raw MarketSignal inputs from the Ingestion Agent
    - Classify provider, signal type, severity, and AT&T relevance using an LLM
    - Normalize outputs into ClassifiedSignal schema
    - Deduplicate near-identical records
    - Fall back to keyword heuristics if LLM is unavailable

Rules:
    - Do NOT scrape or fetch new data
    - Do NOT perform cross-source reasoning
    - Base classification strictly on source content

Why LLM over keywords:
    - Handles nuance: "T-Mobile dropped Essentials to $50" is BOTH pricing AND competitive_move
    - Multi-label: a single post can be sentiment + churn_signal + pricing
    - Context-aware: understands sarcasm, comparisons, implicit signals
    - Expandable: new signal types without new regex patterns
    - Severity assessment: LLM judges impact, not just presence of keywords
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from telecom_intel.config import (
    CLASSIFICATION_MODEL,
    CLASSIFICATION_TEMPERATURE,
    CLASSIFICATION_MAX_TOKENS,
    SIGNALS_DIR,
)
from telecom_intel.models import (
    MarketSignal,
    ClassifiedSignal,
    SignalType,
    Provider,
    Severity,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Classification prompt
# ---------------------------------------------------------------------------

CLASSIFICATION_SYSTEM_PROMPT = """You are a telecom market signal classifier for AT&T's experimentation team.

Given raw scraped content from telecom websites or Reddit, classify it into a structured signal.

RESPOND WITH VALID JSON ONLY — no markdown, no explanation, no code fences.

Schema:
{
  "signal_type": "pricing | outage | software_update | customer_sentiment | policy_change | competitive_move | churn_signal | general",
  "provider": "t-mobile | verizon | att | google_fi | cricket | mint_mobile | us_mobile | visible | other | unknown",
  "severity": "critical | high | medium | low",
  "relevance_to_att": "direct | indirect | none",
  "summary": "One concise sentence summarizing the signal",
  "reasoning": "Brief explanation of why you chose this classification"
}

Classification guidelines:

SIGNAL TYPES:
- pricing: Plan price changes, new plans, promotions, discounts, fee changes
- outage: Network outages, service disruptions, downtime reports
- software_update: OS updates, firmware patches, carrier updates, OTA rollouts
- customer_sentiment: Customer opinions, complaints, praise, experience reports
- policy_change: ToS changes, eligibility changes, contract terms, regulatory
- competitive_move: Strategic moves by competitors that could affect AT&T (new features, market positioning, aggressive offers)
- churn_signal: Customers explicitly mentioning switching carriers, leaving, or comparing to switch
- general: Doesn't fit any specific category

SEVERITY:
- critical: Major event affecting many customers or significant competitive threat
- high: Notable change that warrants attention
- medium: Standard market activity worth tracking
- low: Minor or routine signal

RELEVANCE TO AT&T:
- direct: Mentions AT&T specifically, or is about AT&T's market/customers
- indirect: About a competitor but has implications for AT&T strategy
- none: Unrelated to AT&T's competitive position

MULTI-SIGNAL RULE: If content contains multiple signal types, classify by the PRIMARY signal. Mention secondary signals in the reasoning field.

PROVIDER DETECTION: Identify the primary provider discussed. If multiple providers are compared, pick the one the content is primarily about."""


def _build_classification_prompt(signal: MarketSignal) -> str:
    """Build the user prompt for classifying a single signal."""
    source_info = f"Source: {signal.source_type}"
    if signal.subreddit:
        source_info += f" (r/{signal.subreddit})"
    source_info += f"\nURL: {signal.url}"

    # Truncate content to keep token usage reasonable
    content = signal.content[:1500]

    return f"""{source_info}
Title: {signal.title}

Content:
{content}

Classify this signal. Respond with JSON only."""


# ---------------------------------------------------------------------------
# LLM Classification
# ---------------------------------------------------------------------------

def classify_with_llm(
    signal: MarketSignal,
    openai_client: Any,
) -> ClassifiedSignal | None:
    """
    Classify a single MarketSignal using the LLM.

    Parameters
    ----------
    signal : MarketSignal
        Raw signal to classify.
    openai_client : openai.OpenAI
        The OpenAI client instance (shared with the main app).

    Returns
    -------
    ClassifiedSignal or None if classification fails.
    """
    try:
        response = openai_client.chat.completions.create(
            model=CLASSIFICATION_MODEL,
            temperature=CLASSIFICATION_TEMPERATURE,
            max_tokens=CLASSIFICATION_MAX_TOKENS,
            messages=[
                {"role": "system", "content": CLASSIFICATION_SYSTEM_PROMPT},
                {"role": "user", "content": _build_classification_prompt(signal)},
            ],
        )

        raw_text = response.choices[0].message.content.strip()

        # Strip markdown code fences if the model wraps its response
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[-1]  # Remove first line
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            raw_text = raw_text.strip()

        result = json.loads(raw_text)

        # Validate and coerce enum values
        signal_type = _safe_enum(SignalType, result.get("signal_type", "general"), SignalType.GENERAL)
        provider = _safe_enum(Provider, result.get("provider", "unknown"), Provider.UNKNOWN)
        severity = _safe_enum(Severity, result.get("severity", "medium"), Severity.MEDIUM)
        relevance = result.get("relevance_to_att", "indirect")
        if relevance not in ("direct", "indirect", "none"):
            relevance = "indirect"

        return ClassifiedSignal(
            signal_id=signal.fingerprint,
            signal_type=signal_type,
            provider=provider,
            severity=severity,
            title=signal.title[:200] if signal.title else "(no title)",
            summary=result.get("summary", signal.content[:200]),
            source_url=signal.url,
            source_type=signal.source_type,
            ingested_at=signal.ingested_at,
            classified_at=datetime.now(timezone.utc).isoformat(),
            relevance_to_att=relevance,
            confidence=0.95,  # LLM classification is high confidence
            raw_snippet=signal.content[:1000],
            metadata={
                "llm_reasoning": result.get("reasoning", ""),
                "classification_model": CLASSIFICATION_MODEL,
                "subreddit": signal.subreddit,
            },
        )

    except json.JSONDecodeError as e:
        logger.warning("LLM returned invalid JSON for signal %s: %s", signal.fingerprint, e)
        return None
    except Exception as e:
        logger.warning("LLM classification failed for signal %s: %s", signal.fingerprint, e)
        return None


def _safe_enum(enum_cls, value: str, default):
    """Safely convert a string to an enum value, returning default on failure."""
    try:
        return enum_cls(value.lower().replace(" ", "_"))
    except (ValueError, AttributeError):
        return default


# ---------------------------------------------------------------------------
# Keyword fallback (used when LLM is unavailable)
# ---------------------------------------------------------------------------

import re

_PRICING_KW = re.compile(
    r"\b(pric|plan|fee|cost|rate|discount|promo|offer|deal|unlimited|"
    r"prepaid|postpaid|billing|charge|subscription|bundle|save|cheaper|"
    r"expensive|increase|decrease|per\s*month|/mo)\b", re.I)

_OUTAGE_KW = re.compile(
    r"\b(outage|down|downtime|service\s*disruption|no\s*signal|"
    r"network\s*issue|connectivity|can'?t\s*connect|offline|"
    r"intermittent|degraded|maintenance)\b", re.I)

_SOFTWARE_KW = re.compile(
    r"\b(update|patch|firmware|software\s*version|android\s*\d|ios\s*\d|"
    r"security\s*patch|OTA|changelog|release\s*note|bug\s*fix|"
    r"system\s*update|carrier\s*update)\b", re.I)

_POLICY_KW = re.compile(
    r"\b(policy|terms\s*of\s*service|ToS|eligibility|regulation|"
    r"compliance|FCC|rule\s*change|contract|agreement|fine\s*print|"
    r"restriction|requirement|mandate)\b", re.I)

_SENTIMENT_KW = re.compile(
    r"\b(love|hate|terrible|amazing|worst|best|awful|great|"
    r"horrible|excellent|disappointed|happy|angry|frustrated|"
    r"recommend|avoid|switched|leaving|staying|loyal)\b", re.I)

_CHURN_KW = re.compile(
    r"\b(switch(ed|ing)?|leav(e|ing)|cancel|port(ed|ing)?|"
    r"moving\s*to|went\s*to|left\s*(for|to)|ditched)\b", re.I)

_PROVIDER_PATTERNS = [
    (re.compile(r"\bt[\-\s]?mobile\b|tmo\b|magenta|un-?carrier", re.I), Provider.T_MOBILE),
    (re.compile(r"\bverizon\b|fios\b|vzw\b|big\s*red", re.I), Provider.VERIZON),
    (re.compile(r"\bat&?t\b|att\.com|firstnet|cricket", re.I), Provider.ATT),
    (re.compile(r"\bgoogle\s*fi\b|project\s*fi\b", re.I), Provider.GOOGLE_FI),
    (re.compile(r"\bmint\s*mobile\b", re.I), Provider.MINT_MOBILE),
    (re.compile(r"\bvisible\b", re.I), Provider.VISIBLE),
    (re.compile(r"\bus\s*mobile\b", re.I), Provider.US_MOBILE),
]


def classify_with_keywords(signal: MarketSignal) -> ClassifiedSignal:
    """
    Fallback classification using keyword heuristics.
    Used when the LLM is unavailable or fails.
    """
    text = f"{signal.title} {signal.content}"

    # Detect provider
    provider = Provider.UNKNOWN
    for pattern, prov in _PROVIDER_PATTERNS:
        if pattern.search(f"{signal.url} {text}"):
            provider = prov
            break

    # Score signal types
    scores = {
        SignalType.PRICING: len(_PRICING_KW.findall(text)),
        SignalType.OUTAGE: len(_OUTAGE_KW.findall(text)),
        SignalType.SOFTWARE_UPDATE: len(_SOFTWARE_KW.findall(text)),
        SignalType.POLICY_CHANGE: len(_POLICY_KW.findall(text)),
        SignalType.CUSTOMER_SENTIMENT: len(_SENTIMENT_KW.findall(text)),
        SignalType.CHURN_SIGNAL: len(_CHURN_KW.findall(text)),
    }

    # Boost sentiment for Reddit
    if signal.source_type == "reddit" and scores[SignalType.CUSTOMER_SENTIMENT] > 0:
        scores[SignalType.CUSTOMER_SENTIMENT] += 3

    best_type = max(scores, key=scores.get)
    best_score = scores[best_type]

    if best_score == 0:
        best_type = SignalType.GENERAL
        confidence = 0.3
    else:
        total = sum(scores.values())
        confidence = min(best_score / max(total, 1), 0.8)  # Cap at 0.8 for keyword

    # Determine relevance
    relevance = "none"
    if provider == Provider.ATT:
        relevance = "direct"
    elif provider != Provider.UNKNOWN:
        relevance = "indirect"

    return ClassifiedSignal(
        signal_id=signal.fingerprint,
        signal_type=best_type,
        provider=provider,
        severity=Severity.MEDIUM,  # Keywords can't assess severity well
        title=signal.title[:200] if signal.title else "(no title)",
        summary=text[:200],
        source_url=signal.url,
        source_type=signal.source_type,
        ingested_at=signal.ingested_at,
        classified_at=datetime.now(timezone.utc).isoformat(),
        relevance_to_att=relevance,
        confidence=round(confidence, 3),
        raw_snippet=signal.content[:1000],
        metadata={
            "classification_method": "keyword_fallback",
            "subreddit": signal.subreddit,
        },
    )


# ---------------------------------------------------------------------------
# Batch classification with dedup
# ---------------------------------------------------------------------------

def classify_batch(
    signals: list[MarketSignal],
    openai_client: Any = None,
    *,
    use_llm: bool = True,
    progress_callback: Any = None,
) -> list[ClassifiedSignal]:
    """
    Classify a batch of MarketSignals, deduplicating by signal_id.

    Parameters
    ----------
    signals : list[MarketSignal]
        Raw signals from the ingestion agent.
    openai_client : openai.OpenAI or None
        If provided and use_llm=True, uses LLM classification.
        Falls back to keywords if None or if LLM fails.
    use_llm : bool
        Whether to attempt LLM classification (default True).
    progress_callback : callable or None
        Optional callback(current, total) for progress tracking.

    Returns
    -------
    list[ClassifiedSignal]
    """
    seen: set = set()
    classified: list = []
    llm_count = 0
    keyword_count = 0

    for i, signal in enumerate(signals):
        # Dedup by fingerprint
        fp = signal.fingerprint
        if fp in seen:
            logger.debug("Duplicate skipped: %s", fp)
            continue
        seen.add(fp)

        # Try LLM first, fall back to keywords
        result = None
        if use_llm and openai_client is not None:
            result = classify_with_llm(signal, openai_client)
            if result:
                llm_count += 1

        if result is None:
            result = classify_with_keywords(signal)
            keyword_count += 1

        classified.append(result)

        if progress_callback:
            progress_callback(i + 1, len(signals))

    logger.info(
        "Classification complete — %d signals → %d unique "
        "(LLM: %d, keyword fallback: %d, %.0f%% dedup rate)",
        len(signals), len(classified), llm_count, keyword_count,
        (1 - len(classified) / max(len(signals), 1)) * 100,
    )
    return classified


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def save_signals(signals: list[ClassifiedSignal], label: str = "signals") -> Path:
    """Write classified signals to a timestamped JSON file."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = SIGNALS_DIR / f"{label}_{ts}.json"
    data = [s.to_dict() for s in signals]
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    logger.info("Saved %d signals → %s", len(signals), path)
    return path


def load_cached_signals() -> list[ClassifiedSignal]:
    """Load the most recent signals file from the cache directory."""
    signal_files = sorted(SIGNALS_DIR.glob("signals_*.json"), reverse=True)
    if not signal_files:
        return []

    try:
        data = json.loads(signal_files[0].read_text())
        return [ClassifiedSignal.from_dict(d) for d in data]
    except Exception as e:
        logger.warning("Failed to load cached signals: %s", e)
        return []


# ---------------------------------------------------------------------------
# Public entry-point
# ---------------------------------------------------------------------------

def run_classification(
    raw_signals: list[MarketSignal],
    openai_client: Any = None,
    *,
    use_llm: bool = True,
    progress_callback: Any = None,
) -> dict:
    """
    Execute the full classification pipeline.

    Parameters
    ----------
    raw_signals : list[MarketSignal]
        Raw signals from the ingestion agent.
    openai_client : openai.OpenAI or None
        OpenAI client for LLM classification.
    use_llm : bool
        Whether to use LLM classification.
    progress_callback : callable or None
        Optional progress callback.

    Returns
    -------
    dict with classified signals and summary stats.
    """
    logger.info("=" * 60)
    logger.info("TELECOM SIGNAL CLASSIFICATION AGENT — starting")
    logger.info("Classification method: %s", "LLM" if (use_llm and openai_client) else "keyword")
    logger.info("=" * 60)

    classified = classify_batch(
        raw_signals,
        openai_client=openai_client,
        use_llm=use_llm,
        progress_callback=progress_callback,
    )

    if classified:
        save_signals(classified)

    # Build summary stats
    type_counts: dict = {}
    provider_counts: dict = {}
    severity_counts: dict = {}
    for s in classified:
        type_counts[s.signal_type.value] = type_counts.get(s.signal_type.value, 0) + 1
        provider_counts[s.provider.value] = provider_counts.get(s.provider.value, 0) + 1
        severity_counts[s.severity.value] = severity_counts.get(s.severity.value, 0) + 1

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_raw": len(raw_signals),
        "total_classified": len(classified),
        "by_type": type_counts,
        "by_provider": provider_counts,
        "by_severity": severity_counts,
        "signals": classified,
    }
