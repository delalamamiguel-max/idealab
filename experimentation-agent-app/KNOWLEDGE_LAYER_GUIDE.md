# 🧠 Knowledge Layer Subagent — 2025 Experiment Data Guide

## Overview

The Knowledge Layer Subagent is the **data intelligence engine** of the Experimentation Agent. It retrieves, normalizes, and ranks historical experiments from your 2025 XTrack export to ground all recommendations in real evidence.

**Dataset:** 55 experiments across 41 fields, covering all AT&T digital experiences.

---

## 📊 Data Structure

### Primary Dimensions for Searching

| Dimension | Values | Purpose |
|---|---|---|
| **Impacted Journey** | Wireless Buyflow, Wireline Buyflow, Account Mgmt, Converged, SMB, etc. | Identify experiments in the same customer flow |
| **Technical Site Area** | PDP, Cart, Config, Plans, Homepage, Deals, Checkout, etc. | Find experiments on the same page/component |
| **Primary Metrics** | Progression, POCR, Clicks, Sales, CVR, OSA calls, Enrollments, etc. | Match by success measurement |
| **Audience** | Consumer, IRU, SMB, CaaS, FirstNet, Authenticated, Anonymous, etc. | Find experiments targeting the same segment |
| **Test Results** | Win, Loss, None, N/A | Identify winning patterns or failure modes |
| **Lift Measurement** | Numeric % (e.g., +104.86%, -5.63%) | Quantify impact magnitude |
| **Capability Focus Area** | Trade-in, Plans, Offers, AiA, Port-in, Add-a-Line, etc. | Find experiments addressing the same business lever |
| **Tags** | Custom labels (e.g., "Messaging", "UX", "Offer", "Flow") | Cross-cutting theme identification |

---

## 🔍 How to Find Analogs

### Analog Ranking (Strongest to Weakest)

**DIRECT ANALOG** (Use with high confidence)
- Same journey + same site area + same tactic + same metric + same audience
- Example: "Wireless PDP trade-in messaging test" → find other wireless PDP trade-in tests
- Confidence: Very High

**PARTIAL ANALOG** (Use with moderate confidence)
- 3-4 dimensions match (e.g., same journey + site area + metric, but different audience)
- Example: "Wireless PDP test" → find other wireless PDP tests even if different metric
- Confidence: Moderate

**WEAK ANALOG** (Use cautiously)
- 1-2 dimensions match (e.g., same metric but different journey/site area)
- Example: "Progression metric test" → find other progression tests even on different pages
- Confidence: Low — flag as "weak precedent"

**CONTRADICTORY ANALOG** (Investigate!)
- Same setup but opposite result (e.g., both tested trade-in messaging, one won +5%, one lost -3%)
- Action: Dig into "Learnings & Opportunities" to understand why
- Example: "Auto-Select Trade-In on Upgrade PDP" lost -5.63% — why? → UX confusion. Don't repeat.

---

## 📈 Key Patterns in 2025 Data

### Winning Mechanisms

| Mechanism | Example Experiment | Lift | Key Learning |
|---|---|---|---|
| **Value Surfacing at Decision Point** | Converged Tiered Reward Card (#4357300) | +4,362% progression | Show the customer what they get right when deciding |
| **Friction Removal** | Protect Advantage OE Market Trial (#4287987) | +104.86% enrollment | Simplify the path, remove unnecessary steps |
| **Human-Assist Escape Valve** | CTO for 3+ Line Porters (#4367400) | +18.96% OSA calls | Offer help at the exact friction point without cannibalizing online |
| **Deep-Link + Visual Redesign** | HTP Deep Link Redesign (#4833504) | High conversion | Combine routing optimization with UX polish |
| **Multi-Line Discount Messaging** | Internet HP Link Shift (#4785710) | +9.7% progression | Highlight family/bundle benefits early |

### Loss Patterns (Avoid These)

| Pattern | Example Experiment | Loss | Why It Failed |
|---|---|---|---|
| **Assuming Customer Context** | Auto-Select Trade-In on Upgrade PDP (#4199564) | -5.63% | Customers resisted auto-assumptions; they want control |
| **Over-Engineering Simple Flows** | Progress Bar for Add-ons (#4261650) | -4.39% | 3-step flow doesn't need a progress bar; CTA copy is better |
| **Upper-Funnel Messaging Without Routing** | Homepage ATF Structure Test (#4671307) | -1.24% | Removing OEM placements hurt CTR; messaging alone doesn't drive conversion |
| **Accessibility Without High-Traffic Validation** | Tap to Translate (#4390850) | -3.44% | Good intent, but low-traffic page; retest on high-traffic area |

### Untested Opportunities

| Area | Why It Matters | Recommendation |
|---|---|---|
| **Post-Purchase / ARPU** | PA OE trial drove +105% — massive upside | Invest heavily here; test insurance attach, add-on flows, deep-links |
| **Converged Flow Optimization** | New flow (Jan 2025) — mostly sustainment so far | As it matures, shift from sustainment to true A/B optimization |
| **Port-in UX** | 3+ line porters have high friction | Test CTO placement, port-in wizard, progress indicators |
| **SMB Flows** | Small audience, hard to measure | Low priority for A/B testing; fix known defects via sustainment |

---

## 🎯 Using the Knowledge Layer

### When the User Asks to Search

**User:** "What experiments have we run on the wireless PDP?"

**Knowledge Layer Response:**
1. Search by Impacted Journey = "Wireless Buyflow" AND Technical Site Area = "PDP"
2. Return all matching experiments with:
   - Reference number, name, status, result, lift
   - Primary metric, audience, learnings
3. Rank by recency and result (wins first, then losses, then neutrals)
4. Highlight patterns: "3 wins on trade-in messaging, 1 loss on auto-select"

### When the User Asks for Ideas

**User:** "Generate ideas for the add-a-line flow"

**Knowledge Layer Response:**
1. Search by Capability Focus Area = "Add-a-Line"
2. Search by Impacted Journey = "Wireless Buyflow" (AAL is part of wireless)
3. Find analogs: multi-line discount messaging, plan config optimization, CTO placement
4. Return: "Here are 5 experiments that tested similar mechanics. Here's what worked."

### When the User Asks for Predictions

**User:** "Would urgency messaging on the cart page likely win?"

**Knowledge Layer Response:**
1. Search by Technical Site Area = "Cart" AND Tactic = "Messaging"
2. Search by Primary Metrics = "POCR" or "Progression"
3. Find analogs: upper-funnel messaging tests, urgency tests elsewhere
4. Return: "We tested similar messaging on the homepage (lost -1.24%). We tested urgency on [X] (result: Y). Here's the evidence."

---

## 📋 Data Fields Reference

### Always Available (High Confidence)
- Reference Number
- Name
- Status
- Test Results
- Lift Measurement
- Impacted Journey
- Technical Site Area
- Primary Metrics

### Usually Available (Moderate Confidence)
- Description
- Testing Hypothesis
- Learnings & Opportunities
- Audience Definition
- Estimated Value
- Capability Focus Area

### Sometimes Available (Lower Confidence)
- Secondary Metrics
- Traffic
- Conversion
- Audience Exclusion
- Tags
- Owning Pod

### Data Quality Flags

| Flag | Meaning | Action |
|---|---|---|
| Status = "In Analysis" | Results not final | Don't cite as precedent yet |
| Status = "Sustainment" | Operational fix, not optimization | Use for "what we've tried" but not for "what works" |
| Lift < 0.5% | Marginal lift | Flag as "small effect size" — may not be statistically significant |
| Lift > 50% | Massive lift | Investigate: is this real or a data anomaly? |
| No "Learnings & Opportunities" | Missing insights | Reach out to experiment owner for context |

---

## 🔄 Knowledge Layer Workflow

```
User Query
    │
    ▼
Parse Intent
    │
    ├─ Search? → Find by journey/site area/metric/audience
    ├─ Ideate? → Find analogs + winning mechanisms
    ├─ Predict? → Find precedents + risk factors
    └─ Intake? → Find similar experiments for reference
    │
    ▼
Rank Analogs
    │
    ├─ Direct analog (high confidence)
    ├─ Partial analog (moderate confidence)
    ├─ Weak analog (low confidence)
    └─ Contradictory analog (investigate!)
    │
    ▼
Surface Patterns
    │
    ├─ What worked? (mechanisms)
    ├─ What failed? (anti-patterns)
    ├─ What's untested? (gaps)
    └─ What's uncertain? (confidence flags)
    │
    ▼
Return to Experimentation Agent
```

---

## 💡 Pro Tips

1. **Always cite the reference number** — makes it easy to look up the full experiment
2. **Distinguish between "win" and "do no harm"** — a +0.27% lift on 5M DUVs is a win; a +0.27% lift on 100 DUVs is noise
3. **Check the Learnings field first** — experiment owners often capture the "why" there
4. **Look for contradictions** — if two similar experiments have opposite results, that's a signal to dig deeper
5. **Consider audience** — a win for Consumer may not apply to IRU; flag these differences
6. **Track effort vs. impact** — a +2% lift on a high-effort test may be lower priority than a +1% lift on a low-effort test

---

## 📞 Questions for the Knowledge Layer

**Good questions that leverage the data:**
- "What experiments have we run on [journey/site area]?"
- "Find all experiments that tested [tactic] — what was the result?"
- "What's the strongest precedent for [hypothesis]?"
- "Which experiments had the highest lift? What did they have in common?"
- "Have we tested [idea] before? If so, what happened?"

**Questions the Knowledge Layer can't answer alone:**
- "Should we run this test?" → Reasoning Layer decides
- "How do we implement this?" → Skill Modules execute
- "What should the ticket say?" → Output Layer formats

---

*The Knowledge Layer is your team's institutional memory. Use it to avoid repeating mistakes and to accelerate learning from past experiments.*
