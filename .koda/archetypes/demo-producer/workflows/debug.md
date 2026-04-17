---
description: Fix broken demo captures, zoom effects, animations, voiceovers, or timing issues (Demo Producer)
---

**Archetype**: Demo Producer (Demo Production)  
**Constitution**: `${ARCHETYPES_BASEDIR}/demo-producer/demo-producer-constitution.md`

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup

Verify environment and identify issues:
```bash
# Check app is running
curl -s -o /dev/null -w "%{http_code}" http://localhost:5173/

# Check Playwright
npx playwright --version

# Check demo structure
ls -la demo/
```

### 2. Parse Input

Extract from $ARGUMENTS:
- **Issue Description**: What's broken or failing
- **Scene ID**: Specific scene to debug (optional)
- **Error Message**: Playwright error output (if provided)
- **Demo Path**: Path to demo package (default: `demo/`)

### 3. Diagnose Issue

Run diagnostic checks based on symptoms:

**Symptom: Capture Timeout**
```bash
# Run with debug mode
DEBUG=pw:api npx playwright test demo/captures/demo-capture.spec.ts --timeout=60000
```

Common causes:
- Element selector changed
- Page load too slow
- Network request pending
- Animation not complete

**Symptom: Element Not Found**
```bash
# Launch Playwright Inspector
npx playwright codegen http://localhost:5173/[PAGE]
```

Common causes:
- Selector changed after UI update
- Element loaded dynamically
- Wrong page/route
- Element inside iframe

**Symptom: Screenshot Blank/Wrong**
- Check if page fully loaded
- Check if auth required
- Check viewport size
- Check for overlays/modals

**Symptom: Video Not Recording**
- Check Playwright video config
- Check disk space
- Check output directory permissions

### 4. Identify Root Cause

**For Selector Issues:**
```typescript
// Use Playwright's locator debugging
test('Debug scene', async ({ page }) => {
  await page.goto('[URL]');
  
  // Try multiple selector strategies
  const byTestId = page.locator('[data-testid="element"]');
  const byRole = page.getByRole('button', { name: 'Submit' });
  const byText = page.getByText('Submit');
  const byCss = page.locator('.submit-button');
  
  // Check which one works
  console.log('byTestId:', await byTestId.count());
  console.log('byRole:', await byRole.count());
  console.log('byText:', await byText.count());
  console.log('byCss:', await byCss.count());
  
  // Take debug screenshot
  await page.screenshot({ path: 'debug-screenshot.png', fullPage: true });
});
```

**For Timing Issues:**
```typescript
// Add explicit waits
await page.waitForLoadState('networkidle');
await page.waitForSelector('[data-loaded="true"]');
await page.waitForTimeout(1000); // Last resort
```

**For Auth Issues:**
```typescript
// Check if redirected to login
const url = page.url();
if (url.includes('/login')) {
  console.log('Auth required - adding login step');
}
```

### 5. Generate Fix

Based on diagnosis, generate appropriate fix:

**Fix: Update Selector**
```typescript
// Before (broken)
await page.click('.old-selector');

// After (fixed)
await page.click('[data-testid="new-selector"]');
// OR
await page.getByRole('button', { name: 'Action' }).click();
```

**Fix: Add Wait Condition**
```typescript
// Before (flaky)
await page.goto('/dashboard');
await page.screenshot({ path: 'dashboard.png' });

// After (stable)
await page.goto('/dashboard');
await page.waitForLoadState('networkidle');
await page.waitForSelector('.dashboard-loaded');
await page.screenshot({ path: 'dashboard.png' });
```

**Fix: Add Authentication**
```typescript
// Add to beforeEach
test.beforeEach(async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'demo@example.com');
  await page.fill('[name="password"]', 'password');
  await page.click('button[type="submit"]');
  await page.waitForURL('**/dashboard/**');
});
```

**Fix: Handle Dynamic Content**
```typescript
// Wait for specific content
await page.waitForSelector('text=Welcome');

// Or wait for network idle
await page.waitForLoadState('networkidle');

// Or wait for specific request
await page.waitForResponse('**/api/data');
```

### 6. Apply Fix

Update the capture script with the fix:

```bash
# Backup original
cp demo/captures/demo-capture.spec.ts demo/captures/demo-capture.spec.ts.bak

# Apply fix (done via edit tool)
```

### 7. Verify Fix

Run the fixed capture:
```bash
# Run specific scene
npx playwright test demo/captures/demo-capture.spec.ts -g "Scene [X]" --reporter=list

# Run all captures
npx playwright test demo/captures/demo-capture.spec.ts --reporter=list
```

### 8. Update Manifest

If selectors or timing changed, update `demo-manifest.yaml`:

```yaml
scenes:
  - id: "scene-XX"
    # Updated selector
    capture:
      selector: "[data-testid='new-selector']"  # Changed from .old-selector
    
    # Updated timing
    duration: "0:20"  # Changed from 0:15 due to slower load
```

### 9. Report Resolution

```
✅ Demo Issue Fixed

🔍 Issue: [ISSUE_DESCRIPTION]

📍 Root Cause:
   [ROOT_CAUSE_EXPLANATION]

🔧 Fix Applied:
   File: demo/captures/demo-capture.spec.ts
   Change: [DESCRIPTION_OF_CHANGE]

✓ Verification:
   - Capture runs successfully
   - Screenshot/video generated
   - Quality validated

📋 Files Modified:
   - demo/captures/demo-capture.spec.ts
   - demo/demo-manifest.yaml (if applicable)

💡 Prevention Tips:
   - Use data-testid attributes for stable selectors
   - Add explicit wait conditions
   - Test captures after UI changes

🔄 Next Steps:
   - Run full validation: /test-demo
   - Re-capture all scenes: npx playwright test demo/captures/
```

## Common Issues & Solutions

### Issue: "Timeout waiting for selector"
**Cause:** Element doesn't exist or takes too long to appear
**Solution:**
1. Verify selector with Playwright Inspector
2. Add `waitForSelector` before interaction
3. Increase timeout if needed
4. Check if element is in iframe

### Issue: "Element is not visible"
**Cause:** Element exists but not in viewport or hidden
**Solution:**
1. Scroll element into view: `await element.scrollIntoViewIfNeeded()`
2. Check for overlays/modals blocking
3. Wait for animations to complete

### Issue: "Screenshot is blank"
**Cause:** Page not loaded or wrong viewport
**Solution:**
1. Add `waitForLoadState('networkidle')`
2. Check viewport configuration
3. Verify no auth redirect occurred

### Issue: "Video not generated"
**Cause:** Playwright video config issue
**Solution:**
1. Ensure `video: 'on'` in test.use()
2. Check output directory exists
3. Verify disk space available

### Issue: "Highlights not visible"
**Cause:** CSS injection failed or element changed
**Solution:**
1. Verify selector finds element
2. Check z-index conflicts
3. Add delay after highlight injection

---

## Zoom Effect Troubleshooting

### Issue: "Zoom effect not applied"
**Cause:** MoviePy processing failed or zoom config missing
**Solution:**
```python
# Verify moviepy is installed
import moviepy
print(f"MoviePy: {moviepy.__version__}")

# Check if zoom config exists in frame.yaml
# Ensure zoom target selector exists on page
# Verify zoom parameters are valid (factor > 1.0, duration > 0)
```

### Issue: "Zoom appears jerky/stuttery"
**Cause:** Frame rate mismatch or easing function issues
**Solution:**
```yaml
# Adjust in frame.yaml
zoom:
  duration: 4          # Increase duration for smoother effect
  ease: "ease-in-out"  # Use smooth easing
  fps_factor: 1.5      # Process at higher FPS
```

### Issue: "Zoom centers on wrong element"
**Cause:** Selector matches multiple elements or element moved
**Solution:**
```typescript
// Debug zoom target
const targets = await page.locator(zoomConfig.target).all();
console.log(`Found ${targets.length} matches for zoom target`);

// Use more specific selector
zoom:
  target: "[data-testid='metrics-panel']:first-child"
```

### Issue: "Zoom clips content unexpectedly"
**Cause:** Zoom factor too high or center coordinates wrong
**Solution:**
```yaml
zoom:
  factor: 1.3         # Reduce from 1.5 to 1.3
  padding: 30         # Add padding around target
  center: [0.5, 0.5]  # Verify center is correct (0-1 normalized)
```

---

## Animation & Transition Troubleshooting

### Issue: "Transitions not appearing"
**Cause:** CrossFade effects not imported or applied correctly
**Solution:**
```python
# Verify import
from moviepy.video.fx import CrossFadeIn, CrossFadeOut

# Check clips have duration
for clip in clips:
    print(f"Clip duration: {clip.duration}")  # Must be > 0
```

### Issue: "Flash of black between scenes"
**Cause:** Transition duration longer than clip or timing overlap
**Solution:**
```yaml
transition:
  in_duration: 0.3    # Reduce from 0.5
  out_duration: 0.3   # Keep shorter than scene duration
```

### Issue: "Slide transition goes wrong direction"
**Cause:** Effect applied incorrectly
**Solution:**
```python
# For slide-left (content comes from right)
from moviepy.video.fx import SlideIn

clip = clip.with_effects([SlideIn(duration=0.5, side='right')])
```

---

## Voiceover Troubleshooting

### Issue: "edge-tts fails with network error"
**Cause:** No internet connection or Microsoft Edge TTS service unavailable
**Solution:**
```python
# Fallback to pyttsx3 (offline)
try:
    import edge_tts
    asyncio.run(generate_with_edge_tts(script))
except Exception as e:
    print(f"edge-tts failed: {e}, falling back to pyttsx3")
    import pyttsx3
    engine = pyttsx3.init()
    engine.save_to_file(script, output_path)
    engine.runAndWait()
```

### Issue: "Voiceover sounds robotic"
**Cause:** Script not optimized for AI voices
**Solution:**
```markdown
# Rewrite script using natural patterns:

❌ "The system displays real-time metrics."
✅ "Here's where you'll see your metrics... updating in real-time."

❌ "Users can click the button."
✅ "Just click here... and you're done."

# Add to frame script.md:
- Use contractions
- Add "..." for pauses
- Use conversational phrases
```

### Issue: "Audio and video out of sync"
**Cause:** Timing mismatch between capture and voiceover
**Solution:**
```python
# Check durations
print(f"Video duration: {video.duration}")
print(f"Audio duration: {audio.duration}")

# Adjust audio to match video
if audio.duration > video.duration:
    audio = audio.with_duration(video.duration)
elif audio.duration < video.duration:
    # Add silence padding
    from moviepy.audio.AudioClip import AudioClip
    silence = AudioClip(lambda t: 0, duration=video.duration - audio.duration)
    audio = concatenate_audioclips([audio, silence])
```

### Issue: "Wrong voice used"
**Cause:** Voice ID not found or unavailable
**Solution:**
```python
import edge_tts

# List available voices
async def list_voices():
    voices = await edge_tts.list_voices()
    for v in voices:
        if 'en-US' in v['Locale']:
            print(f"{v['ShortName']}: {v['Gender']} - {v['FriendlyName']}")

asyncio.run(list_voices())

# Use specific voice
VOICE_OPTIONS = {
    'male_professional': 'en-US-GuyNeural',
    'female_friendly': 'en-US-JennyNeural',
    'male_warm': 'en-US-DavisNeural',
    'female_calm': 'en-US-JaneNeural',
}
```

---

## Modular Structure Troubleshooting

### Issue: "Frame not found in frames/ directory"
**Cause:** Scene referenced in manifest but frame folder missing
**Solution:**
```bash
# Check manifest references
cat demo/manifest.yaml | grep scenes -A 20

# Verify folders exist
ls -la demo/frames/

# Create missing frame structure
mkdir -p demo/frames/scene-XX-name
touch demo/frames/scene-XX-name/frame.yaml
touch demo/frames/scene-XX-name/script.md
```

### Issue: "frame.yaml parsing error"
**Cause:** YAML syntax error
**Solution:**
```bash
# Validate YAML
python -c "import yaml; yaml.safe_load(open('demo/frames/scene-XX/frame.yaml'))"

# Common fixes:
# - Use quotes around strings with colons
# - Ensure consistent indentation (2 spaces)
# - No tabs in YAML files
```

### Issue: "Assets saved to wrong location"
**Cause:** Path configuration mismatch
**Solution:**
```yaml
# In manifest.yaml, verify output paths:
output:
  primary: "assets/video/final/product-demo-final.mp4"  # Relative to demo/
  
# Check build script uses correct base path
import os
DEMO_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(DEMO_DIR, 'assets')
```

---

## Final Video Not Generated

### Issue: "Final video missing after workflow"
**Cause:** Pipeline failed silently or output path wrong
**Solution:**
```python
# Add explicit verification
import os

final_video = "demo/assets/video/final/product-demo-final.mp4"
if not os.path.exists(final_video):
    print("❌ FINAL VIDEO NOT CREATED")
    print("Check the following:")
    print("1. Raw captures exist:", os.listdir("demo/assets/video/raw/"))
    print("2. Processed clips exist:", os.listdir("demo/assets/video/processed/"))
    print("3. Audio exists:", os.path.exists("demo/assets/audio/voiceover/full-narration.mp3"))
else:
    print(f"✅ Final video: {final_video}")
    print(f"   Size: {os.path.getsize(final_video) / 1024 / 1024:.1f} MB")
```

### Issue: "Can't find the final video"
**Cause:** User confusion about output location
**Solution:**
```
The final video is ALWAYS at:
   demo/assets/video/final/[product]-demo-final.mp4

To open immediately:
   Windows:  start demo\assets\video\final\product-demo-final.mp4
   macOS:    open demo/assets/video/final/product-demo-final.mp4
   Linux:    xdg-open demo/assets/video/final/product-demo-final.mp4
```

## Error Handling

**Cannot Reproduce**: Ask for more details, suggest running with `DEBUG=pw:api`.

**Multiple Issues**: Prioritize by impact, fix one at a time.

**UI Changed Significantly**: Suggest `/refactor-demo` for comprehensive update.

## Examples

**Example 1**: `/debug-demo Scene 03 fails with "Element not found: .stats-card"`
Output: Diagnoses selector issue, finds new selector `.metrics-card`, updates capture script.

**Example 2**: `/debug-demo Screenshots are blank after login`
Output: Identifies auth redirect, adds login step to beforeEach.

**Example 3**: `/debug-demo Video capture freezes at 10 seconds`
Output: Finds pending network request, adds waitForResponse.

## References

- Constitution: (pre-loaded above)
- Playwright Debugging: https://playwright.dev/docs/debug
- Related: `/scaffold-demo`, `/test-demo`, `/refactor-demo`
