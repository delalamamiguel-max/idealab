# Constitution: Release Note Generator

## Purpose
This constitution defines the principles and rules for generating comprehensive release notes from JIRA user stories across one or more sprints. ensures clarity, traceability, and business relevance in documenting software releases.

---

### I. Hard-Stop Rules (Non-Negotiable)
✘ No missing user stories: All completed stories from selected sprints must be included  
✘ No vague descriptions: Each release note must clearly describe the delivered functionality  
✘ No missing metadata: Each entry must include story ID, title, sprint, and business impact  
✘ No unverified status: Only stories marked as "Done" or "Closed" should be included  
✘ No technical jargon without explanation  
✘ No release note published without test coverage summary and Git commit/PR references

---

### II. Mandatory Patterns (Must Apply)
✔ Story Format: Use `"As a [persona], I want [action], so that [outcome]"` for each story  
✔ Acceptance Criteria Summary: Include a brief summary of the Given/When/Then criteria  
✔ Sprint Reference: Tag each story with its originating sprint (e.g., Sprint 23)  
✔ Business Value: Clearly state the value delivered to users or stakeholders  
✔ Release Version: Group stories under the release version (e.g., v2.3.0)  
✔ Categorization: Organize stories by type (Feature, Bug Fix, Enhancement, Technical Debt)  
✔ Test Verification: Summarize automated/manual test coverage deltas, regression suites executed, and notable quality gates  
✔ Git Traceability: Reference merge commits, tags, or pull requests supporting each story or release summary table

---

### III. Preferred Patterns (Recommended)
➜ Include links to JIRA tickets for traceability  
➜ Use bullet points for readability  
➜ Include screenshots or diagrams if applicable  
➜ Highlight key features or changes at the top  
➜ Include a summary section with metrics (e.g., # of stories, velocity, coverage) and coverage deltas versus prior release  
➜ Provide Git tag or release branch link alongside release metadata  
➜ Use consistent formatting across releases

---

### IV. Sample Release Note Structure

#### 📦 Release Version: v2.3.0  
**Release Date**: 2025-10-24  
**Sprints Covered**: Sprint 21, Sprint 22, Sprint 23

---

### 🚀 New Features
- **[JIRA-1234]** As a customer, I want to receive SMS alerts for order updates, so that I stay informed in real-time.  
  _Sprint_: 21  
  _Business Value_: Improves customer engagement and satisfaction  
  _Acceptance Criteria_: Given an order update, When the status changes, Then an SMS is sent

- **[JIRA-1256]** As an admin, I want to export user data to CSV, so that I can analyze usage trends.  
  _Sprint_: 22  
  _Business Value_: Enables data-driven decision making

---

### 🐞 Bug Fixes
- **[JIRA-1278]** Fixed login timeout issue affecting mobile users  
  _Sprint_: 23  
  _Impact_: Reduced login failures by 80%

---

### 📈 Enhancements
- **[JIRA-1289]** Improved dashboard load time by optimizing queries  
  _Sprint_: 22  
  _Business Value_: Enhances user experience and performance

---

### 📊 Summary
- Total Stories: 12  
- Features: 6  
- Bug Fixes: 4  
- Enhancements: 2  
- Velocity: 38 story points  
- Automated Test Coverage: 91% (↑2% from v2.2.0)  
- Key Commits / PRs: `abc1234`, `def5678`

---

### Version
1.1.0

### Last Updated
2025-10-27
