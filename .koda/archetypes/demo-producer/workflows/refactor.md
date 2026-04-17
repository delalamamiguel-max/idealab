---
description: Update existing demo for product changes, adjust zoom effects, transitions, and voiceovers (Demo Producer)
---

**Archetype**: Demo Producer (Demo Production)  
**Constitution**: `${ARCHETYPES_BASEDIR}/demo-producer/demo-producer-constitution.md`

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup

Verify demo exists and app is running:
```bash
# Check demo structure
ls -la demo/
cat demo/demo-manifest.yaml | head -20

# Check app
curl -s -o /dev/null -w "%{http_code}" http://localhost:5173/
```

### 2. Parse Input

Extract from $ARGUMENTS:
- **Change Description**: What changed in the product
- **Affected Scenes**: Which scenes need updating (optional, will detect)
- **Demo Path**: Path to demo package (default: `demo/`)
- **Preserve Script**: Keep existing voiceover script (default: true)

### 3. Analyze Changes

**Detect UI Changes:**
Run existing captures to identify failures:
```bash
npx playwright test demo/captures/demo-capture.spec.ts --reporter=json > demo/test-results.json 2>&1 || true
```

Parse results to identify:
- Failed scenes (selector changes)
- Timing differences (layout changes)
- New elements (feature additions)
- Removed elements (feature removals)

**Compare with Manifest:**
```typescript
// Check each scene's selectors still exist
for (const scene of manifest.scenes) {
  const exists = await page.locator(scene.capture.selector).count() > 0;
  if (!exists) {
    console.log(`Scene ${scene.id}: Selector changed`);
  }
}
```

### 4. Categorize Updates Needed

**Minor Updates (Auto-fixable):**
- Selector attribute changes (class → data-testid)
- Timing adjustments (±5 seconds)
- Text content changes
- Style changes (colors, spacing)

**Major Updates (Manual review):**
- New features to showcase
- Removed features
- Workflow changes
- Navigation changes
- New pages/routes

**Breaking Changes (Re-scaffold recommended):**
- Complete UI redesign
- >50% of scenes affected
- Core workflow changed
- Authentication flow changed

### 5. Generate Update Plan

```markdown
# Demo Update Plan

**Demo:** [DEMO_NAME]
**Reason:** [CHANGE_DESCRIPTION]
**Impact:** [MINOR/MAJOR/BREAKING]

## Affected Scenes

| Scene | Issue | Action | Effort |
|-------|-------|--------|--------|
| 01 | Selector changed | Update selector | Low |
| 03 | New button added | Add to highlights | Low |
| 05 | Page removed | Remove scene | Medium |
| 07 | New feature | Add new scene | High |

## Recommended Actions

### Auto-Updates (will apply)
1. Scene 01: Update `.old-class` → `[data-testid="new-id"]`
2. Scene 03: Add highlight for new "Export" button

### Manual Updates (need review)
1. Scene 05: Decide whether to remove or replace
2. Scene 07: New "AI Analysis" feature - add scene?

### Script Updates
- Scene 01: No change needed
- Scene 03: Add mention of "Export" feature
- Scene 05: Remove from script
- Scene 07: Write new script section

## Estimated Effort
- Auto-updates: 5 minutes
- Manual updates: 30 minutes
- Script updates: 15 minutes
- Re-capture: 10 minutes
- **Total: ~1 hour**
```

### 6. Apply Auto-Updates

**Update Selectors:**
```typescript
// demo/captures/demo-capture.spec.ts

// Before
await page.click('.old-submit-button');

// After
await page.click('[data-testid="submit-button"]');
```

**Update Timing:**
```yaml
# demo/demo-manifest.yaml
scenes:
  - id: "scene-01"
    duration: "0:20"  # Updated from 0:15
```

**Update Highlights:**
```typescript
// Add new highlight
await addHighlight(page, '[data-testid="export-button"]', 'New: Export Feature');
```

### 7. Handle Scene Additions

For new features that should be demoed:

```typescript
// Add new scene to capture script
test('Scene 08: AI Analysis', async ({ page }) => {
  await page.goto('/analysis');
  await page.waitForLoadState('networkidle');
  
  // Highlight the new feature
  await addHighlight(page, '.ai-panel', 'AI-Powered Analysis');
  
  await page.screenshot({
    path: path.join(SCREENSHOTS_DIR, 'scene-08-ai-analysis.png'),
  });
});
```

Update manifest:
```yaml
scenes:
  # ... existing scenes ...
  
  - id: "scene-08"
    title: "AI Analysis"
    type: "screenshot"
    duration: "0:20"
    url: "/analysis"
    highlights:
      - selector: ".ai-panel"
        annotation: "AI-Powered Analysis"
    script: |
      [PLACEHOLDER - needs script]
```

### 8. Handle Scene Removals

For removed features:

```typescript
// Comment out or remove scene
// test('Scene 05: Legacy Reports', async ({ page }) => {
//   // This feature was removed in v2.0
// });
```

Update manifest:
```yaml
scenes:
  # Scene 05 removed - Legacy Reports feature deprecated
  # - id: "scene-05"
  #   title: "Legacy Reports"
```

Update script to remove references.

### 8.1 Update Zoom Effects

**When UI layout changes, zoom targets may need adjustment:**

```yaml
# frames/scene-02-dashboard/zoom-config.yaml (BEFORE)
zoom:
  enabled: true
  target: ".old-metrics-panel"
  center: [0.7, 0.3]
  factor: 1.4

# (AFTER - updated selector and coordinates)
zoom:
  enabled: true
  target: "[data-testid='metrics-grid']"  # New component
  center: [0.5, 0.4]                       # Adjusted for new layout
  factor: 1.3                              # Slightly less zoom
```

**Zoom Adjustment Checklist:**
- [ ] Target element still exists (check selector)
- [ ] Element position hasn't moved significantly
- [ ] Zoom factor still appropriate for new layout
- [ ] Hold duration matches new content density

### 8.2 Update Transitions

**If scene order or pacing changed:**

```yaml
# frames/scene-03-create/frame.yaml
transition:
  in: "slide-left"          # Changed from crossfade for workflow flow
  in_duration: 0.7
  out: "crossfade"
  out_duration: 0.5
```

**Transition Update Scenarios:**
- **New section added**: Use `fade-black` to mark section boundary
- **Quick sequence of actions**: Use `cut` for snappy feel
- **Drilling into details**: Use `zoom-in` transition
- **Returning to overview**: Use `zoom-out` transition

### 8.3 Update Voiceover for Natural Sound

**When script content changes, ensure natural AI voice quality:**

```markdown
# frames/scene-XX/script.md (BEFORE - robotic)
The new Export feature allows users to download data.

# (AFTER - natural)
Now here's something you'll love... the new Export feature.
Just one click, and your data is ready to download.
Pretty handy, right?
```

**Voiceover Update Checklist:**
- [ ] Use contractions ("you'll" not "you will")
- [ ] Add pauses with "..." for natural breathing
- [ ] Include conversational phrases
- [ ] Add rhetorical questions for engagement
- [ ] Match word count to scene duration (~145 WPM)

### 8.4 Regenerate Audio

**After script updates, regenerate voiceover:**

```bash
# Run voiceover generation for updated scenes
cd demo/scripts
python generate-voiceover.py --scenes scene-03,scene-08

# Or regenerate all
python generate-voiceover.py --all
```

```python
# demo/scripts/generate-voiceover.py
import edge_tts
import asyncio
import os

async def regenerate_scene_audio(scene_dir: str):
    script_path = os.path.join(scene_dir, 'script.md')
    audio_path = os.path.join('assets', 'audio', 'voiceover', f'{os.path.basename(scene_dir)}.mp3')
    
    # Extract narration from script.md
    with open(script_path) as f:
        content = f.read()
        # Extract text between ## Narration and next ##
        narration = extract_narration(content)
    
    # Generate with natural voice
    communicate = edge_tts.Communicate(narration, "en-US-GuyNeural", rate="-10%")
    await communicate.save(audio_path)
    print(f"✅ Generated: {audio_path}")
```

### 9. Update Script

Preserve existing script structure, update only affected sections:

```markdown
# [PRODUCT_NAME] Demo Script

## Scene 03: Dashboard Overview (0:15 - 0:35)

**Visual:** Dashboard with metrics highlighted

### Script

> Welcome to the dashboard. Here you can see all your project metrics at a glance.
> **[NEW]** Notice the new Export button - you can now export your data with one click.

### Key Points
- Real-time metrics
- **[NEW]** One-click export feature
- Customizable widgets
```

### 10. Re-capture Affected Scenes

Run captures for updated scenes:
```bash
# Capture specific scenes
npx playwright test demo/captures/demo-capture.spec.ts -g "Scene 01|Scene 03|Scene 08" --reporter=list

# Or capture all
npx playwright test demo/captures/demo-capture.spec.ts --reporter=list
```

### 11. Validate Updates

Run full validation:
```bash
npx playwright test demo/captures/demo-capture.spec.ts --reporter=list
```

Check:
- All scenes capture successfully
- New assets generated
- Script references valid
- Timing still accurate

### 12. Report Completion

```
✅ Demo Updated Successfully

📝 Change: [CHANGE_DESCRIPTION]

🔄 Updates Applied:

   Selectors Updated: [X]
   - Scene 01: .old-class → [data-testid="new-id"]
   - Scene 03: Added export button highlight

   Scenes Modified: [X]
   - Scene 01: Selector update
   - Scene 03: New highlight added
   - Scene 08: NEW - AI Analysis feature

   Scenes Removed: [X]
   - Scene 05: Legacy Reports (deprecated)

   Script Updates: [X]
   - Scene 03: Added export mention
   - Scene 05: Removed
   - Scene 08: Placeholder added (needs writing)

📸 Assets Re-captured:
   ✓ scene-01-dashboard.png (updated)
   ✓ scene-03-overview.png (updated)
   ✓ scene-08-ai-analysis.png (new)

⚠️ Manual Actions Required:
   1. Write script for Scene 08 (AI Analysis)
   2. Review Scene 03 script for accuracy
   3. Update total duration in manifest

📋 Files Modified:
   - demo/captures/demo-capture.spec.ts
   - demo/demo-manifest.yaml
   - demo/script/demo-script.md
   - demo/assets/screenshots/ (3 files)

💡 Next Steps:
   1. Write Scene 08 script
   2. Run full validation: /test-demo
   3. Review updated assets
   4. Update README if needed
```

## Error Handling

**Too Many Changes**: If >50% of scenes affected, recommend `/scaffold-demo` instead.

**Cannot Detect Changes**: Ask for specific change description, run manual comparison.

**Script Conflicts**: Preserve original, create `.updated` version for review.

**New Feature Unknown**: Ask for feature description, suggest scene structure.

## Examples

**Example 1**: `/refactor-demo Dashboard layout changed, metrics cards are now in a grid`
Output: Updates Scene 01 selectors, adjusts highlight positions, re-captures.

**Example 2**: `/refactor-demo Added new AI Analysis feature on /analysis page`
Output: Adds Scene 08, creates placeholder script, updates manifest.

**Example 3**: `/refactor-demo Removed legacy reports, updated navigation`
Output: Removes Scene 05, updates navigation scenes, adjusts timing.

**Example 4**: `/refactor-demo Complete UI redesign with new design system`
Output: Detects breaking changes, recommends `/scaffold-demo` for fresh start.

## References

- Constitution: (pre-loaded above)
- Related: `/scaffold-demo`, `/test-demo`, `/debug-demo`
