---
description: Generate documentation for demo package including guides and maintenance docs (Demo Producer)
---

**Archetype**: Demo Producer (Demo Production)  
**Constitution**: `${ARCHETYPES_BASEDIR}/demo-producer/demo-producer-constitution.md`

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Parse Input

Extract from $ARGUMENTS:
- **Demo Path**: Path to demo package (default: `demo/`)
- **Doc Type**: all | guide | maintenance | embed | changelog
- **Output Format**: markdown | html | confluence
- **Audience**: presenters | developers | stakeholders

### 2. Load Demo Package

Read demo configuration and assets:
- `demo/demo-manifest.yaml` - Demo configuration
- `demo/script/demo-script.md` - Voiceover script
- `demo/captures/demo-capture.spec.ts` - Capture scripts
- `demo/assets/` - Screenshots and videos

### 3. Generate Presenter Guide

```markdown
# [PRODUCT_NAME] Demo - Presenter Guide

**Version:** [VERSION]  
**Last Updated:** [DATE]  
**Duration:** [DURATION]

## Overview

This guide helps you deliver the [PRODUCT_NAME] demo effectively.

## Before You Present

### Technical Setup
- [ ] Application running at [URL]
- [ ] Demo assets available in `demo/assets/`
- [ ] Backup: Pre-recorded video available

### Audience Preparation
- [ ] Know your audience (technical/business/executive)
- [ ] Prepare for common questions (see FAQ below)
- [ ] Have follow-up materials ready

## Demo Flow

### Scene 1: [TITLE] (0:00 - 0:15)

**What to Show:** [VISUAL_DESCRIPTION]

**What to Say:**
> [SCRIPT_TEXT]

**Key Points to Emphasize:**
- [POINT_1]
- [POINT_2]

**Common Questions:**
- Q: [QUESTION]
- A: [ANSWER]

**Transition:** [HOW_TO_MOVE_TO_NEXT_SCENE]

---

### Scene 2: [TITLE] (0:15 - 0:45)

[REPEAT_STRUCTURE]

---

## Handling Issues

### If the App is Slow
- Use pre-recorded video backup
- Explain: "Let me show you a recording while the system loads"

### If a Feature Fails
- Skip to next scene
- Note: "We're experiencing a minor issue, let me show you [ALTERNATIVE]"

### If Asked About Unavailable Feature
- Acknowledge the request
- Explain roadmap if appropriate
- Offer to follow up

## FAQ

**Q: How does [FEATURE] work?**
A: [ANSWER]

**Q: What's the pricing?**
A: [ANSWER_OR_REDIRECT]

**Q: Can it integrate with [SYSTEM]?**
A: [ANSWER]

## Follow-Up Materials

- Product documentation: [LINK]
- Technical specs: [LINK]
- Contact sales: [EMAIL]
```

### 4. Generate Maintenance Guide

```markdown
# [PRODUCT_NAME] Demo - Maintenance Guide

**For:** Developers maintaining the demo  
**Last Updated:** [DATE]

## Demo Structure

```
demo/
├── assets/
│   ├── screenshots/     # PNG captures
│   └── videos/          # WebM clips
├── captures/
│   └── demo-capture.spec.ts  # Playwright scripts
├── script/
│   └── demo-script.md   # Voiceover script
├── demo-manifest.yaml   # Configuration
└── README.md
```

## Updating the Demo

### When UI Changes

1. **Identify affected scenes:**
   ```bash
   npx playwright test demo/captures/ --reporter=list
   ```

2. **Update selectors:**
   - Open `demo/captures/demo-capture.spec.ts`
   - Find failing scene
   - Update selector using Playwright Inspector:
     ```bash
     npx playwright codegen http://localhost:5173/
     ```

3. **Re-capture:**
   ```bash
   npx playwright test demo/captures/ -g "Scene [X]"
   ```

4. **Validate:**
   ```bash
   /test-demo
   ```

### When Adding Features

1. **Add scene to manifest:**
   ```yaml
   scenes:
     - id: "scene-XX"
       title: "New Feature"
       type: "screenshot"
       # ...
   ```

2. **Add capture test:**
   ```typescript
   test('Scene XX: New Feature', async ({ page }) => {
     // ...
   });
   ```

3. **Write script section**

4. **Run captures and validate**

### When Removing Features

1. Comment out scene in capture script
2. Remove from manifest
3. Remove from script
4. Delete assets (optional)

## Troubleshooting

### Capture Fails
```bash
# Debug mode
DEBUG=pw:api npx playwright test demo/captures/ -g "Scene [X]"

# Interactive mode
npx playwright test demo/captures/ --debug
```

### Screenshots Blank
- Check app is running
- Check authentication
- Check viewport size

### Videos Not Recording
- Check `video: 'on'` in test config
- Check disk space
- Check output directory permissions

## Automation

### CI/CD Integration

```yaml
# .github/workflows/demo-validation.yml
name: Validate Demo
on:
  push:
    paths:
      - 'src/**'  # Trigger on app changes
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: npx playwright install chromium
      - run: npm run dev &
      - run: npx playwright test demo/captures/
```

### Scheduled Re-capture

```yaml
# Weekly demo refresh
name: Refresh Demo
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
jobs:
  refresh:
    # ...
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | [DATE] | Initial demo |
| 1.1.0 | [DATE] | Added Scene 08 |
```

### 5. Generate Embed Guide

```markdown
# Embedding [PRODUCT_NAME] Demo

## In Documentation (Markdown)

### Screenshot
```markdown
![Dashboard Overview](demo/assets/screenshots/scene-01-dashboard.png)
*Figure 1: Dashboard showing real-time metrics*
```

### Video (HTML in Markdown)
```html
<video width="100%" controls>
  <source src="demo/assets/videos/scene-02-workflow.webm" type="video/webm">
  Your browser does not support video.
</video>
```

### GIF (if converted)
```markdown
![Project Creation](demo/assets/gifs/scene-02-create.gif)
```

## In Confluence

1. Upload assets to Confluence
2. Use multimedia macro for videos
3. Use image macro for screenshots

## In PowerPoint

1. Insert → Video → Video on My PC
2. Select WebM file
3. Set to play on click or automatically

## In Web Pages

```html
<!-- Responsive video embed -->
<div style="position: relative; padding-bottom: 56.25%; height: 0;">
  <video style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" controls>
    <source src="demo/assets/videos/full-demo.webm" type="video/webm">
  </video>
</div>
```

## In Slack/Teams

- Screenshots: Drag and drop PNG files
- Videos: Upload WebM (may need to convert to MP4 for Teams)
- GIFs: Best for short clips (<10 seconds)
```

### 6. Generate Changelog

```markdown
# [PRODUCT_NAME] Demo Changelog

## [1.1.0] - [DATE]

### Added
- Scene 08: AI Analysis feature
- New highlight for Export button

### Changed
- Scene 01: Updated dashboard layout
- Scene 03: New selector for metrics card

### Removed
- Scene 05: Legacy Reports (feature deprecated)

### Fixed
- Scene 02: Timing issue with form submission

---

## [1.0.0] - [DATE]

### Added
- Initial demo with 7 scenes
- Dashboard overview
- Project creation workflow
- Document upload
- Requirements matrix
- Process flow editor
- Reports generation
- Closing CTA
```

### 7. Report Completion

```
✅ Demo Documentation Generated

📚 Documents Created:

   Presenter Guide:
   ✓ demo/docs/presenter-guide.md
   - Scene-by-scene instructions
   - FAQ section
   - Troubleshooting tips

   Maintenance Guide:
   ✓ demo/docs/maintenance-guide.md
   - Update procedures
   - Troubleshooting
   - CI/CD integration

   Embed Guide:
   ✓ demo/docs/embed-guide.md
   - Markdown examples
   - HTML snippets
   - Platform-specific instructions

   Changelog:
   ✓ demo/docs/CHANGELOG.md
   - Version history
   - Change tracking

📂 Output Structure:
   demo/docs/
   ├── presenter-guide.md
   ├── maintenance-guide.md
   ├── embed-guide.md
   └── CHANGELOG.md

💡 Next Steps:
   1. Review presenter guide before demo
   2. Share maintenance guide with team
   3. Use embed guide for documentation
```

## Error Handling

**Demo Not Found**: Report missing demo, suggest `/scaffold-demo`.

**Incomplete Demo**: List missing components, suggest completing first.

**Invalid Format**: Default to markdown, note format limitation.

## Examples

**Example 1**: `/document-demo`
Output: Full documentation suite for demo/ directory.

**Example 2**: `/document-demo --type guide --audience presenters`
Output: Presenter-focused guide only.

**Example 3**: `/document-demo --type maintenance --format confluence`
Output: Maintenance guide formatted for Confluence.

**Example 4**: `/document-demo --type changelog`
Output: Changelog based on git history and manifest versions.

## References

- Constitution: (pre-loaded above)
- Related: `/scaffold-demo`, `/refactor-demo`
