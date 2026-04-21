"""
Telecom Intel Pipeline — Market intelligence for the Experimentation Agent.

Scrapes competitor sites + Reddit via Apify, classifies signals with an LLM,
and synthesizes actionable market insights that feed into experiment planning.
"""

from telecom_intel.models import (
    MarketSignal,
    ClassifiedSignal,
    MarketInsight,
    SignalType,
    Provider,
    Severity,
)
from telecom_intel.pipeline import TelecomIntelPipeline

__all__ = [
    "MarketSignal",
    "ClassifiedSignal",
    "MarketInsight",
    "SignalType",
    "Provider",
    "Severity",
    "TelecomIntelPipeline",
]
