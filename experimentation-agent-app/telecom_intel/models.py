"""
Telecom Intel — Shared Data Models

Dataclass-based schemas for market signals, classified signals, and insights.
No external dependencies (no pydantic) — keeps the package lightweight.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SignalType(str, Enum):
    PRICING = "pricing"
    OUTAGE = "outage"
    SOFTWARE_UPDATE = "software_update"
    CUSTOMER_SENTIMENT = "customer_sentiment"
    POLICY_CHANGE = "policy_change"
    COMPETITIVE_MOVE = "competitive_move"
    CHURN_SIGNAL = "churn_signal"
    GENERAL = "general"


class Provider(str, Enum):
    T_MOBILE = "t-mobile"
    VERIZON = "verizon"
    ATT = "att"
    GOOGLE_FI = "google_fi"
    CRICKET = "cricket"
    MINT_MOBILE = "mint_mobile"
    US_MOBILE = "us_mobile"
    VISIBLE = "visible"
    OTHER = "other"
    UNKNOWN = "unknown"


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class InsightCategory(str, Enum):
    RISK = "risk"
    OPPORTUNITY = "opportunity"
    ANOMALY = "anomaly"
    TREND = "trend"
    COMPETITIVE_MOVE = "competitive_move"


# ---------------------------------------------------------------------------
# Raw Market Signal (pre-classification)
# ---------------------------------------------------------------------------

@dataclass
class MarketSignal:
    """Raw scraped data item before classification."""
    url: str
    title: str
    content: str
    source_type: str  # "website" | "reddit"
    ingested_at: str
    subreddit: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    @property
    def fingerprint(self) -> str:
        raw = f"{self.url.strip().lower()}|{self.title.strip().lower()}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Classified Signal (post-LLM classification)
# ---------------------------------------------------------------------------

@dataclass
class ClassifiedSignal:
    """A market signal after LLM-powered classification."""
    signal_id: str
    signal_type: SignalType
    provider: Provider
    severity: Severity
    title: str
    summary: str
    source_url: str
    source_type: str
    ingested_at: str
    classified_at: str
    relevance_to_att: str = "indirect"  # "direct" | "indirect" | "none"
    confidence: float = 0.9
    raw_snippet: str = ""
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["signal_type"] = self.signal_type.value
        d["provider"] = self.provider.value
        d["severity"] = self.severity.value
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "ClassifiedSignal":
        """Reconstruct from a dict (e.g., loaded from JSON)."""
        return cls(
            signal_id=data["signal_id"],
            signal_type=SignalType(data["signal_type"]),
            provider=Provider(data["provider"]),
            severity=Severity(data["severity"]),
            title=data["title"],
            summary=data["summary"],
            source_url=data["source_url"],
            source_type=data["source_type"],
            ingested_at=data["ingested_at"],
            classified_at=data["classified_at"],
            relevance_to_att=data.get("relevance_to_att", "indirect"),
            confidence=data.get("confidence", 0.9),
            raw_snippet=data.get("raw_snippet", ""),
            metadata=data.get("metadata", {}),
        )


# ---------------------------------------------------------------------------
# Market Insight (post-reasoning)
# ---------------------------------------------------------------------------

@dataclass
class SupportingSignalRef:
    """Lightweight reference to a signal that supports an insight."""
    signal_id: str
    signal_type: str
    provider: str
    title: str
    source_url: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class MarketInsight:
    """An actionable insight derived from classified signals."""
    insight_id: str
    category: InsightCategory
    headline: str
    analysis: str
    confidence: float
    generated_at: str
    implications: list = field(default_factory=list)
    experiment_recommendations: list = field(default_factory=list)
    supporting_signals: list = field(default_factory=list)
    providers_involved: list = field(default_factory=list)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["category"] = self.category.value
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "MarketInsight":
        return cls(
            insight_id=data["insight_id"],
            category=InsightCategory(data["category"]),
            headline=data["headline"],
            analysis=data["analysis"],
            confidence=data.get("confidence", 0.7),
            generated_at=data["generated_at"],
            implications=data.get("implications", []),
            experiment_recommendations=data.get("experiment_recommendations", []),
            supporting_signals=data.get("supporting_signals", []),
            providers_involved=data.get("providers_involved", []),
        )


# ---------------------------------------------------------------------------
# Pipeline Report
# ---------------------------------------------------------------------------

@dataclass
class PipelineReport:
    """Full output of a telecom intel pipeline run."""
    report_id: str
    generated_at: str
    mode: str  # "live" | "dry_run" | "from_cache"
    total_raw_items: int
    total_signals: int
    total_insights: int
    signals: list = field(default_factory=list)
    insights: list = field(default_factory=list)
    signal_summary: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "report_id": self.report_id,
            "generated_at": self.generated_at,
            "mode": self.mode,
            "total_raw_items": self.total_raw_items,
            "total_signals": self.total_signals,
            "total_insights": self.total_insights,
            "signals": [s.to_dict() if hasattr(s, "to_dict") else s for s in self.signals],
            "insights": [i.to_dict() if hasattr(i, "to_dict") else i for i in self.insights],
            "signal_summary": self.signal_summary,
        }

    def to_context_string(self) -> str:
        """Format the report as a text block for injection into LLM context."""
        lines = [
            "=" * 60,
            "TELECOM MARKET INTELLIGENCE REPORT",
            f"Generated: {self.generated_at}",
            f"Mode: {self.mode}",
            f"Signals: {self.total_signals} | Insights: {self.total_insights}",
            "=" * 60,
            "",
        ]

        if self.insights:
            lines.append("## KEY MARKET INSIGHTS")
            lines.append("")
            for i, insight in enumerate(self.insights, 1):
                ins = insight if isinstance(insight, dict) else insight.to_dict()
                lines.append(f"### Insight {i}: {ins['headline']}")
                lines.append(f"Category: {ins['category']} | Confidence: {ins.get('confidence', 'N/A')}")
                lines.append(f"Providers: {', '.join(ins.get('providers_involved', []))}")
                lines.append(f"Analysis: {ins['analysis']}")
                if ins.get("implications"):
                    lines.append("Implications:")
                    for imp in ins["implications"]:
                        lines.append(f"  • {imp}")
                if ins.get("experiment_recommendations"):
                    lines.append("Experiment Recommendations:")
                    for rec in ins["experiment_recommendations"]:
                        lines.append(f"  → {rec}")
                lines.append("")

        if self.signals:
            lines.append("## CLASSIFIED SIGNALS SUMMARY")
            lines.append("")
            # Group by type
            by_type: dict = {}
            for sig in self.signals:
                s = sig if isinstance(sig, dict) else sig.to_dict()
                st = s.get("signal_type", "general")
                by_type.setdefault(st, []).append(s)

            for signal_type, sigs in by_type.items():
                lines.append(f"### {signal_type.upper()} ({len(sigs)} signals)")
                for s in sigs[:5]:  # Limit to 5 per type for context window
                    lines.append(
                        f"  [{s.get('provider', '?')}] {s.get('title', '?')[:80]} "
                        f"(severity: {s.get('severity', '?')}, "
                        f"relevance: {s.get('relevance_to_att', '?')})"
                    )
                if len(sigs) > 5:
                    lines.append(f"  ... and {len(sigs) - 5} more")
                lines.append("")

        return "\n".join(lines)
