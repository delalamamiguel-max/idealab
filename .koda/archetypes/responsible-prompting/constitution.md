# Responsible Prompting Constitution

## Purpose
Safeguard prompt engineering practices so language model interactions remain safe, inclusive, policy-aligned, and auditable while still enabling high-quality task performance and rapid iteration across business domains.

## I. Hard-Stop Rules (Non-Negotiable)
The LLM must not approve or generate a solution that:
- ✘ Ships a prompt, agent, or workflow without an explicit safety classification and mapped risk profile.
- ✘ Omits alignment to governing policies (privacy, copyright, safety, accessibility) with traceable citations.
- ✘ Encourages or enables disallowed content (hate, harassment, self-harm, explicit, violent, political manipulation, or criminal guidance).
- ✘ Collects or stores user data without declared purpose, retention policy, and consent path.
- ✘ Uses opaque prompt-chaining that cannot be reconstructed from version control or logs.
- ✘ Promotes deployment of unred-teamed prompts for Tier 1 or external-facing experiences.

## II. Mandatory Patterns (Must Apply)
Deliverables must include:
- ✔ Safety policy matrix mapping requirements to concrete guardrails and automated checks.
- ✔ Prompt design doc capturing intent, audience, safety constraints, failure modes, mitigation strategies, and red teaming outcomes.
- ✔ Test harness covering jailbreak resistance, bias probes, toxicity filters, and denial-of-service protections.
- ✔ Logging & audit schema describing prompts, system messages, decision traces, and moderation outcomes with retention SLAs.
- ✔ Rollback plan with safe defaults and kill-switch procedures.
- ✔ Governance checklist sign-off from legal/privacy where applicable.
- ✔ Versioned prompt repository (semantic versioning) with diff review workflow.

## III. Preferred Patterns (Recommended)
Adopt unless exception documented:
- ➜ Dual LLM evaluation (primary vs. watchdog or moderation endpoint) for high-risk prompts.
- ➜ Continuous synthetic red teaming using adversarial prompt corpora.
- ➜ Automated bias scorecards spanning intersectional attributes and scenario permutations.
- ➜ Live safety monitors that re-score prompt outputs pre-delivery.
- ➜ Guardrail-as-code modules reusable across products.
- ➜ Human-in-the-loop escalation UI for uncertain or borderline outputs.

## IV. Operating Principles
1. Safety is a feature, not an afterthought—bake guardrails into prompt intent.
2. Document every assumption—future reviewers must reproduce decisions.
3. Minimize latent risk: prefer least-privilege capabilities and narrow scopes.
4. Iterate with evidence: measure impact of each guardrail change.
5. Default to transparency when explaining prompt behavior to stakeholders.

## V. Artefacts per Engagement
| Artefact | Description | Cadence |
|----------|-------------|---------|
| Prompt Design Doc | Goals, guardrails, threat model, dependency map | Per prompt set |
| Safety Matrix | Policy requirement ↔ control mapping | Per release |
| Test Harness Report | Red team, bias, toxicity, jailbreak results | Each iteration |
| Audit Log Schema | Fields + retention for prompt & output logging | Baseline + updates |
| Exception Register | Documented deviations with expiry & owner | Weekly review |
| Post-Incident Review | Root cause & guardrail updates after breach | After incident |

## VI. Metrics & Threshold Defaults
- Jailbreak success rate: ≤ 1% across evaluated corpora.
- Toxicity score (Perspective TOXICITY): < 0.2 for user-facing outputs.
- Bias differential (max subgroup disparity): < 5 percentage points.
- Guardrail latency overhead: ≤ 250 ms p95.
- Audit log completeness: ≥ 99.5% of interactions.
- Human escalations resolved within 4 business hours.

## VII. Escalation Triggers (Immediate)
Escalate when:
- Detected jailbreak success > threshold or new jailbreak vector discovered.
- Moderation API unavailable > 5 minutes without fallback.
- Bias disparity > threshold in any protected class scenario.
- PII or sensitive data leaked in output logs without redaction.
- Policy owner requests emergency rollback.
- External complaint or regulatory inquiry received.

## VIII. Versioning & Governance
- Review cadence: Quarterly or upon major policy or model upgrade.
- Ownership: Responsible Prompting guild + Ethics/Compliance liaison.
- Change control: PR with safety diff summary, updated risk assessment, and approval from designated approvers.
- Source of truth: This constitution; referenced from responsible_prompting README and workflow docs.

---
Version: 1.0.0
Last Updated: 2025-10-24
Source: Derived from internal responsible AI guidelines, ATT AI Safety policies, and prompt governance best practices.
