---
description: Validate demo captures, zoom effects, transitions, voiceovers, and modular structure meet quality standards (Demo Producer)
---

**Archetype**: Demo Producer (Demo Production)  
**Constitution**: `${ARCHETYPES_BASEDIR}/demo-producer/demo-producer-constitution.md`

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup

Verify demo package exists and Playwright is available:
```bash
# Check demo directory
ls -la demo/

# Check Playwright
npx playwright --version
```

### 2. Load Demo Configuration

- Read `demo/demo-manifest.yaml` for scene definitions
- Load `demo/captures/demo-capture.spec.ts` for test structure
- Identify expected outputs

### 3. Parse Input

Extract from $ARGUMENTS:
- **Demo Path**: Path to demo package (default: `demo/`)
- **Test Scope**: all | captures | assets | script
- **Fix Mode**: Whether to attempt auto-fixes (default: false)

### 4. Validate Capture Scripts

Run Playwright tests in check mode:
```bash
npx playwright test demo/captures/demo-capture.spec.ts --reporter=list --retries=0
```

Check for:
- All tests pass
- No timeout errors
- No element-not-found errors
- Consistent execution time

### 5. Validate Screenshots

For each screenshot in `demo/assets/screenshots/`:

```typescript
// Validation checks
interface ScreenshotValidation {
  exists: boolean;
  size: number;           // bytes, should be > 10KB
  dimensions: {
    width: number;        // should be 1920
    height: number;       // should be 1080
  };
  isBlank: boolean;       // detect all-white or all-black
  hasHighlights: boolean; // detect AT&T Blue (#009FDB)
  hasErrorState: boolean; // detect error messages/red elements
}
```

**Quality Checks:**
- ✓ File exists and is non-empty
- ✓ Resolution is 1920x1080 (or configured size)
- ✓ Not a blank/error page
- ✓ Highlights are visible (if expected)
- ✓ No sensitive data visible (manual check flag)

### 6. Validate Videos

For each video in `demo/assets/videos/`:

```typescript
interface VideoValidation {
  exists: boolean;
  size: number;           // bytes, should be > 100KB
  duration: number;       // seconds, should match manifest
  format: string;         // should be webm
  hasAudio: boolean;      // typically false for captures
  frameRate: number;      // should be ~30fps
}
```

Check video metadata:
```bash
# Get video info (if ffprobe available)
ffprobe -v quiet -print_format json -show_format -show_streams demo/assets/videos/*.webm
```

**Quality Checks:**
- ✓ File exists and is non-empty
- ✓ Duration matches expected (±10%)
- ✓ Format is WebM
- ✓ Resolution is correct
- ✓ No frozen frames at start/end

### 7. Validate Script

Check `demo/script/demo-script.md`:

**Structure Checks:**
- ✓ Has title and metadata
- ✓ All scenes documented
- ✓ Timing cues present
- ✓ Asset references valid

**Content Checks:**
- ✓ Word count appropriate for duration (~150 words/minute)
- ✓ No placeholder text remaining
- ✓ Key points listed for each scene
- ✓ Call to action present

**Reference Checks:**
- All referenced assets exist
- Scene numbers match manifest
- Timing adds up to total duration

### 7.1 Validate Scene URLs (Duplicates & Alignment)

**This is critical to catch the most common quality issues:**

```typescript
interface SceneURLValidation {
  hasDuplicates: boolean;
  duplicateUrls: string[];
  alignmentIssues: AlignmentIssue[];
  coverageScore: number;  // 0-100, based on unique pages shown
}

interface AlignmentIssue {
  sceneId: string;
  url: string;
  narration: string;
  problem: string;
}

function validateSceneURLs(manifest: DemoManifest): SceneURLValidation {
  const urls = manifest.scenes.map(s => s.url);
  const uniqueUrls = [...new Set(urls)];
  const duplicates = urls.filter((url, i) => urls.indexOf(url) !== i);
  
  // Check for narration-URL alignment
  const alignmentIssues: AlignmentIssue[] = [];
  
  for (const scene of manifest.scenes) {
    const narration = scene.narration.toLowerCase();
    const url = scene.url.toLowerCase();
    
    // Pattern: Narration mentions "editing" but URL is a list page (no :id)
    if ((narration.includes('edit') || narration.includes('detail') || narration.includes('view ')) 
        && !url.match(/\/[a-z-]+\/[a-z0-9-]+$/i)) {
      // URL doesn't end with /:id pattern - likely a list page
      alignmentIssues.push({
        sceneId: scene.id,
        url: scene.url,
        narration: scene.narration,
        problem: 'Narration mentions editing/viewing details but URL appears to be a list page (no :id)'
      });
    }
    
    // Pattern: Narration mentions "upload" but URL is dashboard/home
    if (narration.includes('upload') && (url === '/dashboard' || url === '/' || url === '/home')) {
      alignmentIssues.push({
        sceneId: scene.id,
        url: scene.url,
        narration: scene.narration,
        problem: 'Narration mentions upload but URL is dashboard/home (not upload page)'
      });
    }
    
    // Pattern: Narration describes feature X but URL is generic dashboard
    const featureKeywords = ['create', 'search', 'filter', 'report', 'settings', 'config'];
    for (const keyword of featureKeywords) {
      if (narration.includes(keyword) && (url === '/dashboard' || url === '/' || url === '/home')) {
        alignmentIssues.push({
          sceneId: scene.id,
          url: scene.url,
          narration: scene.narration,
          problem: `Narration mentions "${keyword}" but URL is dashboard (navigate to the feature page)`
        });
        break;
      }
    }
  }
  
  return {
    hasDuplicates: duplicates.length > 0,
    duplicateUrls: [...new Set(duplicates)],
    alignmentIssues,
    coverageScore: (uniqueUrls.length / Math.min(urls.length, 10)) * 100
  };
}
```

**Quality Checks:**
- ❌ FAIL if any URL appears more than once (duplicates)
- ❌ FAIL if narration mentions feature not shown on URL
- ⚠️ WARN if coverage score < 80% (not enough unique pages)
- ✓ PASS if all URLs unique and aligned with narration

**Common Failures to Detect:**
| Narration Contains | URL Should Be | Not Acceptable |
|-------------------|---------------|----------------|
| "edit the item" | `/items/:id` (detail page) | `/items` (list page) |
| "upload files" | `/uploads` or upload page | `/dashboard` |
| "search for" | `/search` | `/dashboard` |
| "create new" | `/items/new` or create page | `/dashboard` |
| "settings" | `/settings` | `/dashboard` |
| "view details" | `/resource/:id` | `/resource` (list) |

### 7.2 Validate Video Recording (Not Screenshots)

**Verify the demo is a continuous video recording, not a screenshot slideshow:**

```typescript
interface VideoModeValidation {
  isVideoRecording: boolean;   // Has actual video file from Playwright
  hasMotion: boolean;          // Contains mouse movements, scrolling
  frameCount: number;          // Should be duration * 30fps
  avgFrameDiff: number;        // Higher = more motion (good)
}

async function validateVideoMode(videoPath: string): Promise<VideoModeValidation> {
  // Check if video exists and has continuous frames
  const stats = await getVideoStats(videoPath);
  
  // A screenshot slideshow has very low frame differences
  // A real recording has motion (mouse, scrolling, typing)
  const avgFrameDiff = stats.averageFrameDifference; // 0-100
  
  return {
    isVideoRecording: stats.format === 'webm' && stats.frameCount > stats.duration * 20,
    hasMotion: avgFrameDiff > 5,  // Threshold for detecting actual motion
    frameCount: stats.frameCount,
    avgFrameDiff
  };
}
```

**Quality Checks:**
- ❌ FAIL if only PNG screenshots exist (no video)
- ❌ FAIL if video has no motion (static frames)
- ⚠️ WARN if frame rate < 25fps
- ✓ PASS if continuous video with visible interactions

### 7.3 Validate Zoom Effects

For each scene with zoom enabled:

```typescript
interface ZoomValidation {
  sceneId: string;
  targetExists: boolean;
  targetVisible: boolean;
  factorInRange: boolean;     // 1.0 - 2.0 recommended
  durationReasonable: boolean; // 2-5 seconds typical
  centerWithinBounds: boolean; // [0-1, 0-1]
}

async function validateZoom(page: Page, frameConfig: FrameConfig): Promise<ZoomValidation> {
  const zoom = frameConfig.zoom;
  if (!zoom?.enabled) return { sceneId: frameConfig.id, ...allValid };
  
  await page.goto(frameConfig.url);
  await page.waitForLoadState('networkidle');
  
  const targetExists = await page.locator(zoom.target).count() > 0;
  const targetVisible = targetExists && await page.locator(zoom.target).isVisible();
  
  return {
    sceneId: frameConfig.id,
    targetExists,
    targetVisible,
    factorInRange: zoom.factor >= 1.0 && zoom.factor <= 2.0,
    durationReasonable: zoom.duration >= 2 && zoom.duration <= 5,
    centerWithinBounds: 
      zoom.center[0] >= 0 && zoom.center[0] <= 1 &&
      zoom.center[1] >= 0 && zoom.center[1] <= 1,
  };
}
```

**Quality Checks:**
- Zoom target element exists on page
- Zoom target is visible (not hidden)
- Zoom factor between 1.0 and 2.0
- Zoom duration between 2-5 seconds
- Center coordinates within [0-1] bounds

### 7.4 Validate Transitions

```typescript
interface TransitionValidation {
  sceneId: string;
  hasTransition: boolean;
  typeValid: boolean;
  durationValid: boolean;
  compatibleWithAdjacentScenes: boolean;
}

const VALID_TRANSITIONS = ['crossfade', 'slide-left', 'slide-up', 'zoom-in', 'zoom-out', 'fade-black', 'cut'];

function validateTransitions(scenes: FrameConfig[]): TransitionValidation[] {
  return scenes.map((scene, i) => {
    const trans = scene.transition;
    return {
      sceneId: scene.id,
      hasTransition: !!trans,
      typeValid: !trans || (
        VALID_TRANSITIONS.includes(trans.in) && 
        VALID_TRANSITIONS.includes(trans.out)
      ),
      durationValid: !trans || (
        trans.in_duration >= 0.2 && trans.in_duration <= 1.5 &&
        trans.out_duration >= 0.2 && trans.out_duration <= 1.5
      ),
      compatibleWithAdjacentScenes: !trans || (
        trans.in_duration + trans.out_duration < scene.duration
      ),
    };
  });
}
```

**Quality Checks:**
- Transition type is valid
- Transition duration between 0.2s and 1.5s
- Combined transition time < scene duration
- Adjacent scenes have compatible transitions

### 7.5 Validate Voiceover Quality

```typescript
interface VoiceoverValidation {
  fileExists: boolean;
  durationMatch: boolean;     // Within 10% of target
  formatCorrect: boolean;     // MP3 or WAV
  volumeLevel: 'too-quiet' | 'good' | 'too-loud';
  noClipping: boolean;        // Audio doesn't clip
  wordsPerMinute: number;     // Target: 130-160 WPM
}

async function validateVoiceover(audioPath: string, targetDuration: number): Promise<VoiceoverValidation> {
  const stats = await getAudioStats(audioPath);
  
  return {
    fileExists: fs.existsSync(audioPath),
    durationMatch: Math.abs(stats.duration - targetDuration) / targetDuration < 0.1,
    formatCorrect: audioPath.endsWith('.mp3') || audioPath.endsWith('.wav'),
    volumeLevel: stats.avgVolume > -30 && stats.avgVolume < -10 ? 'good' : 
                 stats.avgVolume <= -30 ? 'too-quiet' : 'too-loud',
    noClipping: stats.peakVolume < 0,  // dB below 0
    wordsPerMinute: stats.wordCount / (stats.duration / 60),
  };
}
```

**Quality Checks:**
- Audio file exists
- Duration within 10% of target
- Format is MP3 or WAV
- Volume level appropriate (not too quiet/loud)
- No audio clipping
- Speech rate 130-160 WPM

### 7.6 Validate Script Natural Language

```typescript
interface ScriptQualityValidation {
  sceneId: string;
  hasContractions: boolean;    // "you'll" instead of "you will"
  hasPauses: boolean;          // "..." for natural pauses
  hasConversational: boolean;  // "Now let's" phrases
  noJargon: boolean;           // Acronyms spelled out
  wordCount: number;
  estimatedDuration: number;   // Based on 145 WPM
}

function validateScript(script: string): Partial<ScriptQualityValidation> {
  const contractionPattern = /\b(you'll|we're|that's|it's|don't|won't|can't|let's|here's)\b/gi;
  const pausePattern = /\.\.\./g;
  const conversationalPattern = /\b(now let's|here's where|notice how|see how|pretty cool)\b/gi;
  const jargonPattern = /\b([A-Z]{2,})\b/g;  // All-caps acronyms
  
  const words = script.split(/\s+/).length;
  
  return {
    hasContractions: contractionPattern.test(script),
    hasPauses: pausePattern.test(script),
    hasConversational: conversationalPattern.test(script),
    noJargon: !jargonPattern.test(script) || 
              script.includes('API') && script.includes('Application Programming Interface'),
    wordCount: words,
    estimatedDuration: words / 145 * 60,  // seconds
  };
}
```

**Quality Checks:**
- Script uses contractions (natural speech)
- Script has pause markers ("...")
- Script uses conversational phrases
- Acronyms are explained
- Word count matches target duration

### 7.7 Validate AI Feature Handling

If the demo includes AI features, validate proper handling:

```typescript
interface AISceneValidation {
  hasAIFeatures: boolean;
  scenes: AISceneCheck[];
  overallScore: 'good' | 'needs-work' | 'poor';
}

interface AISceneCheck {
  sceneId: string;
  aiWaitTime: number;        // seconds of loading/waiting shown
  hasJumpCut: boolean;       // input and output spliced together
  hasTimeCompression: boolean; // sped-up waiting
  hasNarrationBridge: boolean; // voiceover covers the wait
  issue?: string;
}

function validateAIScenes(manifest: DemoManifest, videoAnalysis: VideoAnalysis): AISceneValidation {
  const aiScenes = manifest.scenes.filter(s => 
    s.narration?.toLowerCase().includes('ai') ||
    s.url?.includes('/ai') ||
    s.tags?.includes('ai-feature')
  );
  
  if (aiScenes.length === 0) {
    return { hasAIFeatures: false, scenes: [], overallScore: 'good' };
  }
  
  const checks = aiScenes.map(scene => {
    const waitTime = videoAnalysis.getLoadingSpinnerDuration(scene.id);
    return {
      sceneId: scene.id,
      aiWaitTime: waitTime,
      hasJumpCut: videoAnalysis.hasJumpCut(scene.id),
      hasTimeCompression: videoAnalysis.hasSpeedChange(scene.id),
      hasNarrationBridge: scene.narration?.includes('...'),
      issue: waitTime > 10 ? 'AI wait time too long - needs jump cut or time compression' : undefined
    };
  });
  
  const hasIssues = checks.some(c => c.aiWaitTime > 10);
  return {
    hasAIFeatures: true,
    scenes: checks,
    overallScore: hasIssues ? 'needs-work' : 'good'
  };
}
```

**Quality Checks:**
- ❌ FAIL if any AI scene shows >15 seconds of loading
- ⚠️ WARN if AI scene shows 5-15 seconds without time compression
- ✓ PASS if AI scenes use jump cuts or time compression
- ✓ PASS if narration bridges the AI wait naturally

### 7.8 Validate Modular Structure

```bash
# Check required directories exist
demo/
├── manifest.yaml            # Required
├── assets/
│   ├── video/
│   │   ├── raw/             # Required
│   │   ├── processed/       # Required
│   │   └── final/           # Required - contains output
│   ├── audio/
│   │   └── voiceover/       # Required
│   └── subtitles/           # Required
├── frames/                  # Required - one folder per scene
│   └── scene-XX/
│       ├── frame.yaml       # Required
│       └── script.md        # Required
└── scripts/                 # Required
```

```typescript
function validateModularStructure(demoDir: string): StructureValidation {
  const required = [
    'manifest.yaml',
    'assets/video/final',
    'assets/audio/voiceover',
    'assets/subtitles',
    'frames',
    'scripts',
  ];
  
  const missing = required.filter(p => !fs.existsSync(path.join(demoDir, p)));
  
  // Check each scene in manifest has corresponding frame folder
  const manifest = yaml.load(fs.readFileSync(path.join(demoDir, 'manifest.yaml')));
  const missingFrames = manifest.scenes.filter(
    s => !fs.existsSync(path.join(demoDir, 'frames', s))
  );
  
  return {
    allDirectoriesExist: missing.length === 0,
    missingDirectories: missing,
    allFramesExist: missingFrames.length === 0,
    missingFrames,
  };
}
```

### 8. Validate Manifest

Check `demo/demo-manifest.yaml`:

```yaml
# Required fields
demo:
  title: required
  duration_target: required
  target_audience: required

scenes:
  - id: required
    title: required
    type: required (screenshot|video)
    duration: required
    url: required
    script: required
```

**Consistency Checks:**
- Scene count matches actual captures
- Total duration matches sum of scenes
- All URLs are valid routes
- All selectors are valid CSS/XPath

### 9. Run Integration Test

Execute full capture run and compare outputs:
```bash
# Run captures fresh
npx playwright test demo/captures/demo-capture.spec.ts --project=chromium

# Compare with existing assets
diff -r demo/assets/ demo/assets-backup/ 2>/dev/null || echo "No backup to compare"
```

### 10. Generate Test Report

```markdown
# Demo Validation Report

**Demo:** [DEMO_NAME]  
**Tested:** [DATE]  
**Status:** [PASS/FAIL]

## Summary

| Category | Tests | Passed | Failed |
|----------|-------|--------|--------|
| Captures | [X] | [X] | [X] |
| Screenshots | [X] | [X] | [X] |
| Videos | [X] | [X] | [X] |
| Script | [X] | [X] | [X] |
| Manifest | [X] | [X] | [X] |
| **Total** | **[X]** | **[X]** | **[X]** |

## Capture Tests

| Scene | Status | Duration | Notes |
|-------|--------|----------|-------|
| Scene 01 | ✅ PASS | 2.3s | |
| Scene 02 | ✅ PASS | 5.1s | |
| Scene 03 | ❌ FAIL | - | Element not found: .stats-card |

## Asset Validation

### Screenshots
| File | Size | Dimensions | Quality |
|------|------|------------|---------|
| scene-01-dashboard.png | 245KB | 1920x1080 | ✅ Good |
| scene-02-create.png | 189KB | 1920x1080 | ⚠️ No highlights |

### Videos
| File | Size | Duration | Format |
|------|------|----------|--------|
| scene-03-workflow.webm | 2.4MB | 28s | ✅ WebM |

## Script Validation

- Word Count: [X] words
- Estimated Duration: [X] minutes
- Scenes Documented: [X]/[X]
- Missing Assets: [LIST]

## Issues Found

### Critical
- [ ] Scene 03 capture fails - selector `.stats-card` not found

### Warnings
- [ ] Scene 02 screenshot missing highlight overlay
- [ ] Script word count (180) may be short for 3-minute demo

### Info
- [ ] Video duration 28s vs expected 30s (within tolerance)

## Recommendations

1. **Fix Scene 03**: Update selector to `.metrics-card` (UI changed)
2. **Add Highlights**: Scene 02 needs highlight on submit button
3. **Expand Script**: Add 50-70 more words for better pacing
```

### 11. Report Results

```
✅ Demo Validation Complete

📊 Test Results:
   Captures: [X]/[X] passed
   Screenshots: [X]/[X] valid
   Videos: [X]/[X] valid
   Script: [X]/[X] checks passed
   Manifest: [X]/[X] valid

🔍 Issues Found:
   Critical: [X]
   Warnings: [X]
   Info: [X]

📋 Actions Required:
   [LIST_OF_REQUIRED_FIXES]

💡 Commands:
   - Fix captures: /debug-demo
   - Update for UI changes: /refactor-demo
   - Re-run validation: /test-demo
   - View full report: cat demo/validation-report.md
```

## Error Handling

**Demo Not Found**: Report missing demo directory, suggest running `/scaffold-demo` first.

**Captures Fail**: Report specific failures with error messages, suggest `/debug-demo`.

**Assets Missing**: List missing files, suggest re-running captures.

**Script Incomplete**: Report missing sections, provide template for completion.

## Examples

**Example 1**: `/test-demo`
Output: Full validation of demo/ directory with detailed report.

**Example 2**: `/test-demo demo/captures/ --scope captures`
Output: Only run capture tests, skip asset validation.

**Example 3**: `/test-demo --fix`
Output: Run validation and attempt auto-fixes for common issues.

## Phase 2: Simulation Testing (CRITICAL ENHANCEMENT)

### 12. Design Representative Demo Task

Extract from demo-producer constitution use cases:
- "Create 2-minute executive demo of web application"
- "Generate technical walkthrough with feature highlights"
- "Build product demo with AI capabilities"

**Select Test Scenario:**
```
Task: "Create 2-minute executive demo of AndiSense application showing:
- Dashboard overview
- Project management
- Requirements traceability
- Process flow visualization
- Reports and metrics"

Expected Outcomes:
✓ 6-8 unique scenes (no duplicate URLs)
✓ Narration aligned with visuals
✓ All key features covered
✓ Pipeline executes automatically
✓ Final video quality is professional
```

### 13. Execute Demo Workflow

Run the full scaffold workflow:
```bash
/scaffold-demo "Create 2-minute executive demo of AndiSense application"
```

**Track During Execution:**

#### 13.1 Scene Planning Validation
Monitor for:
- [ ] URL uniqueness check performed
- [ ] Feature discovery analysis completed
- [ ] Duplicate URL warnings issued
- [ ] Narration-visual alignment validated
- [ ] Coverage score calculated

#### 13.2 Capture Execution
Monitor for:
- [ ] Playwright tests run successfully
- [ ] All scenes captured without errors
- [ ] Video files generated (not just screenshots)
- [ ] Motion detected in recordings
- [ ] No frozen frames

#### 13.3 Pipeline Execution
Monitor for:
- [ ] Voiceover generation completed
- [ ] Audio-video merge successful
- [ ] Subtitles generated
- [ ] Final video opened automatically
- [ ] All intermediate files preserved

### 14. Evaluate Results

**Quality Checks:**

#### 14.1 Scene Quality
```bash
# Check for duplicate URLs
cat demo/manifest.yaml | grep "url:" | sort | uniq -d
# Should return empty (no duplicates)
```

✓ Did demo capture all key features?
✓ Were scenes unique (no duplicate URLs)?
✓ Did narration match visuals?
✓ Were all pages shown with data (not empty states)?

#### 14.2 Pipeline Quality
✓ Did pipeline execute automatically without manual intervention?
✓ Was final video opened in default player?
✓ Were all assets preserved in modular structure?
✓ Can demo be re-rendered without re-capturing?

#### 14.3 Output Quality
```bash
# Check video quality
ffprobe -v quiet -print_format json -show_format demo/assets/video/final/demo-final.mp4

# Check audio sync
# Play video and verify narration matches visuals
```

✓ Is video resolution correct (1920x1080)?
✓ Is audio synchronized with video?
✓ Are subtitles accurate and timed correctly?
✓ Is final file size reasonable (<50MB for 2-min demo)?

### 15. Generate Reasoning Trace

Document any issues found during simulation:

```markdown
# Demo Producer Simulation Results

**Date:** [YYYY-MM-DD]
**Test Scenario:** Executive demo of AndiSense
**Status:** [PASS/FAIL]

## Issues Identified

### Critical Issues
- [ ] Scene planning did not detect duplicate URLs
- [ ] Narration mentioned "AI analysis" but no AI page exists
- [ ] Pipeline failed at voiceover generation step

### Warnings
- [ ] Coverage score was 60% (below 80% threshold)
- [ ] Scene 3 showed empty state (no data)
- [ ] Zoom effect target not visible on page

### Observations
- [ ] Collaborative design step was skipped
- [ ] User was not prompted to review scene plan
- [ ] No validation of feature existence before capture

## Root Causes

1. **Ambiguous Scene Planning Instructions**
   - Workflow does not explicitly check for duplicate URLs
   - No validation that narrated features exist in application

2. **Missing Validation Steps**
   - No data verification before capture
   - No feature discovery analysis
   - No upfront collaboration with user

3. **Unclear Error Handling**
   - Pipeline continues even if scenes have issues
   - No rollback on validation failures

## Recommended Fixes

1. Add Step 1.5: Collaborative Design (see improvement plan)
2. Add URL uniqueness validation in scene planning
3. Add feature discovery analysis before capture
4. Add data verification step
5. Add hard-stop on validation failures

## Test Verdict

[PASS/FAIL] - [Explanation]

**Confidence in Archetype:** [0-100%]
**Readiness for Production:** [Yes/No]
```

### 16. Iterate Based on Findings

If simulation revealed issues:

1. **Update Workflows**: Fix ambiguous instructions
2. **Add Validations**: Implement missing checks
3. **Enhance Error Handling**: Add rollback mechanisms
4. **Re-test**: Run simulation again to verify fixes

**Hard-Stop Rule:** Do not mark archetype as complete until simulation passes with 90%+ confidence.

## References

- Constitution: (pre-loaded above)
- Related: `/scaffold-demo`, `/debug-demo`, `/refactor-demo`
