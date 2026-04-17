---
description: Create executive summaries or reader's guides for existing documentation packages (Documentation Evangelist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype documentation-evangelist --json ` and parse for DOC_FORMAT, DIAGRAM_TOOL, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/documentation-evangelist/templates/env-config.yaml` for format standards

### 3. Parse Input
Extract from $ARGUMENTS: documentation directory/package to summarize, target audience (executives/new developers/operators), summary type (executive summary/reader's guide/quick start/index), key focus areas. Request clarification if incomplete.

### 4. Analyze Documentation Package

Scan and catalog documentation:

**Inventory**:
- List all documentation files
- Identify file types (README, guides, API docs, runbooks, etc.)
- Extract metadata (titles, authors, dates, versions)
- Map document relationships and dependencies

**Content Analysis**:
- Identify main topics and themes
- Extract key concepts and terminology
- Note important diagrams and visuals
- Identify critical procedures and workflows
- Find common patterns and structures

**Audience Assessment**:
- Determine primary audience for each document
- Identify skill level requirements
- Note prerequisites and dependencies
- Assess completeness for different user journeys

**Quality Assessment**:
- Check for outdated content
- Identify gaps in coverage
- Note inconsistencies across documents
- Assess overall organization

### 5. Generate Summary Document

Create appropriate summary based on type:

**Executive Summary** (for leadership):
```markdown
# Executive Summary: [System Name] Documentation

## Overview
[2-3 sentence high-level description of system and its business value]

## Key Capabilities
- [Capability 1]: [Business impact]
- [Capability 2]: [Business impact]
- [Capability 3]: [Business impact]

## Architecture Highlights
[High-level architecture diagram with 3-5 key components]

## Operational Status
- **Availability**: [SLA/uptime]
- **Performance**: [Key metrics]
- **Cost**: [Operating costs]
- **Team**: [Team size and structure]

## Strategic Considerations
- **Strengths**: [What works well]
- **Risks**: [Key risks and mitigations]
- **Opportunities**: [Future enhancements]
- **Dependencies**: [Critical dependencies]

## Recommended Actions
1. [Action item 1]
2. [Action item 2]
3. [Action item 3]

## Documentation Inventory
- [X] documents covering [Y] topics
- Last updated: [Date]
- Completeness: [Assessment]
```

**Reader's Guide** (for new team members):
```markdown
# Reader's Guide: [System Name] Documentation

## Welcome!
[Friendly introduction explaining what this system does and why it matters]

## Documentation Map

### Start Here (Required Reading)
1. **[README.md](link)** - System overview and quick start (15 min)
2. **[ARCHITECTURE.md](link)** - System design and components (30 min)
3. **[GETTING_STARTED.md](link)** - Setup and first steps (45 min)

### By Role

**For Developers**:
- [API_GUIDE.md](link) - API reference and examples
- [DEVELOPMENT.md](link) - Development workflow and standards
- [TESTING.md](link) - Testing strategies and tools

**For Operators**:
- [DEPLOYMENT.md](link) - Deployment procedures
- [MONITORING.md](link) - Monitoring and alerting
- [RUNBOOK.md](link) - Operational procedures

**For Data Engineers**:
- [DATA_PIPELINE.md](link) - Pipeline architecture
- [DATA_QUALITY.md](link) - Quality checks and validation
- [TROUBLESHOOTING.md](link) - Common issues and solutions

### By Task

**Setting Up**:
1. [Prerequisites](link#prerequisites)
2. [Installation](link#installation)
3. [Configuration](link#configuration)
4. [Verification](link#verification)

**Daily Operations**:
- [Monitoring Dashboard](link)
- [Common Tasks](link)
- [Incident Response](link)

**Advanced Topics**:
- [Performance Tuning](link)
- [Security Hardening](link)
- [Disaster Recovery](link)

## Learning Path

### Week 1: Foundations
- [ ] Read system overview
- [ ] Understand architecture
- [ ] Complete setup guide
- [ ] Run first query/job

### Week 2: Deep Dive
- [ ] Study data pipeline
- [ ] Review quality checks
- [ ] Understand monitoring
- [ ] Practice troubleshooting

### Week 3: Mastery
- [ ] Performance optimization
- [ ] Advanced features
- [ ] Contribute to docs
- [ ] Mentor others

## Key Concepts Glossary
- **[Term 1]**: [Definition]
- **[Term 2]**: [Definition]
- **[Term 3]**: [Definition]

## Quick Reference
- **Support**: [Contact info]
- **Repository**: [Git URL]
- **Dashboard**: [Monitoring URL]
- **Runbook**: [Link]

## Tips for Success
1. [Tip 1]
2. [Tip 2]
3. [Tip 3]
```

**Quick Start Guide** (for immediate productivity):
```markdown
# Quick Start: [System Name]

## 5-Minute Setup

### Prerequisites
- [Tool 1] version X.Y+
- [Tool 2] version A.B+
- Access to [Resource]

### Installation
```bash
# Step 1: Clone repository
git clone [URL]

# Step 2: Install dependencies
[command]

# Step 3: Configure
[command]

# Step 4: Verify
[command]
```

### Your First [Task]
[Step-by-step walkthrough of most common task]

## Common Tasks

### Task 1: [Name]
```bash
[command with explanation]
```

### Task 2: [Name]
```bash
[command with explanation]
```

### Task 3: [Name]
```bash
[command with explanation]
```

## Next Steps
- [ ] Read [Architecture Overview](link)
- [ ] Explore [API Documentation](link)
- [ ] Join [Team Channel](link)
- [ ] Review [Best Practices](link)

## Getting Help
- **Questions**: [Slack channel]
- **Issues**: [GitHub issues]
- **Urgent**: [On-call contact]
```

**Documentation Index** (for navigation):
```markdown
# Documentation Index: [System Name]

## By Category

### Architecture & Design
- [System Architecture](link) - High-level design and components
- [Data Model](link) - Database schemas and relationships
- [API Design](link) - API architecture and patterns

### Development
- [Development Guide](link) - Setup and workflow
- [Coding Standards](link) - Style guide and best practices
- [Testing Guide](link) - Unit, integration, and E2E testing

### Operations
- [Deployment Guide](link) - CI/CD and release process
- [Monitoring Guide](link) - Metrics, logs, and alerts
- [Runbook](link) - Operational procedures

### Reference
- [API Reference](link) - Complete API documentation
- [Configuration Reference](link) - All configuration options
- [CLI Reference](link) - Command-line tool documentation

## By Audience

### New Team Members
Start with: [README](link) → [Architecture](link) → [Getting Started](link)

### Developers
Focus on: [Development Guide](link) → [API Reference](link) → [Testing](link)

### Operators
Focus on: [Deployment](link) → [Monitoring](link) → [Runbook](link)

## By Task

### Setup & Configuration
- [Prerequisites](link)
- [Installation](link)
- [Configuration](link)

### Daily Operations
- [Monitoring](link)
- [Common Tasks](link)
- [Troubleshooting](link)

### Advanced Topics
- [Performance Tuning](link)
- [Security](link)
- [Disaster Recovery](link)

## Document Status

| Document | Last Updated | Status | Owner |
|----------|--------------|--------|-------|
| README.md | 2025-01-15 | ✅ Current | Team A |
| ARCHITECTURE.md | 2025-01-10 | ✅ Current | Team B |
| API_GUIDE.md | 2024-12-20 | ⚠️ Needs Update | Team C |
```

### 6. Add Navigation Aids

Include helpful navigation elements:
- Table of contents with links
- Document relationship diagram (Mermaid)
- Recommended reading order
- Skill level indicators
- Time estimates for each document
- Prerequisites and dependencies

### 7. Validate and Report


Report completion with:
- Summary document path
- Document inventory (count and types)
- Coverage assessment
- Recommendations for documentation improvements
- Next steps for maintaining summary

## Error Handling

**Empty Documentation**: Report no documentation found, suggest starting with scaffold workflow.

**Incomplete Documentation**: Note gaps in coverage, suggest missing documents to create.

**Inconsistent Documentation**: Report inconsistencies, suggest refactoring for consistency.

## Examples

**Executive Summary**: `/document-documentation docs/ "Create executive summary for leadership covering system capabilities, operational status, strategic considerations, and key metrics. Audience: C-level executives."`
Output: 2-page executive summary with high-level overview, business value, key metrics, strategic recommendations.

**Reader's Guide**: `/document-documentation docs/ "Generate comprehensive reader's guide for new team members with learning path, documentation map by role and task, quick reference. Audience: new developers and operators."`
Output: Complete reader's guide with structured learning path, role-based navigation, task-based index, glossary.

**Quick Start**: `/document-documentation docs/ "Create quick start guide for immediate productivity. Focus on 5-minute setup and 3 most common tasks. Audience: developers needing fast onboarding."`
Output: Concise quick start with minimal setup steps, common task examples, next steps.

**Documentation Index**: `/document-documentation docs/ "Build comprehensive documentation index organized by category, audience, and task. Include document status table."`
Output: Complete index with multiple navigation paths, document status tracking, recommendations.

## References

Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/documentation-evangelist/templates/env-config.yaml`
