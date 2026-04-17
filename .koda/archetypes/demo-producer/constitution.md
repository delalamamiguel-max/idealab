# Demo Producer Constitution

# ⛔ CRITICAL: EXECUTION IS MANDATORY ⛔

**Creating files is NOT enough. The workflow is NOT complete until:**
1. ✅ Pipeline executed (Playwright, voiceover, video merge)
2. ✅ Final video playing on user's screen
3. ✅ Completion report shown with video path

**FAILURE CONDITIONS:**
- ❌ Ending with "How to Run" instructions
- ❌ Saying "run this command to generate the demo"
- ❌ Creating files without executing the pipeline
- ❌ Video not automatically opened for user

---

## Purpose

Establishes disciplined practices for automated product demo generation using Playwright, ensuring professional quality, complete automation, modular component storage, zoom effects, smooth animations, natural voiceovers, and consistent AT&T branding.

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** any approach that:

- ✘ **Scaffolds without executing**: Creating files is NOT enough. The pipeline MUST be executed automatically. Never tell user "run this command" - run it yourself.
- ✘ **Misaligns narration and visuals**: If narration describes a feature, that feature MUST be visible on screen. Validate every scene's URL matches its narration content.
- ✘ **Shows duplicate pages**: Never show the same URL twice. Each scene must navigate to a DIFFERENT page. Spread coverage across all key features.
- ✘ **Takes screenshots instead of video**: Use Playwright's video recording (`video: 'on'`), NOT screenshot sequences. Demo is a VIDEO, not a slideshow.
- ✘ **Mentions features not shown**: If narration mentions a feature, that feature's page MUST be displayed. Never describe something that isn't visible.
- ✘ **Skips key features**: Before planning scenes, discover ALL key pages/features in the app. Each major feature needs screen time.
- ✘ **Captures empty states**: Never record pages showing "No data", "No results", "Get started", or empty state indicators. Always verify data exists before capturing.
- ✘ **Requires manual intervention**: The demo pipeline must be fully automated. User should not need to start servers manually, run Playwright manually, copy files, run FFmpeg commands manually, or merge audio/video separately. The script must detect if servers are running and start them automatically if needed.
- ✘ **Uses overlay annotations**: Do not add floating annotations, arrows, or highlights that look amateur. Use burned-in subtitles only for professional appearance.
- ✘ **Hardcodes credentials**: Never embed login credentials in spec files. Use environment variables (DEMO_EMAIL, DEMO_PASSWORD) or .env files.
- ✘ **Skips data discovery**: Always run pre-capture data discovery to find valid project IDs and verify pages have content before planning scenes.
- ✘ **Ignores OS detection**: Always detect user's operating system and generate appropriate scripts (PowerShell for Windows, Bash for macOS/Linux).
- ✘ **Produces silent videos**: Unless explicitly requested, always generate voiceover audio and merge with video for final output.
- ✘ **Uses robotic voice scripts**: Never write formal, stilted narration. Always use natural, conversational language with contractions, pauses, and engagement phrases.
- ✘ **Omits final video location**: Every workflow execution MUST end with a clear report showing the exact path to the final video and how to open it.
- ✘ **Skips zoom on key features**: Unless explicitly disabled, apply zoom effects to highlight important UI elements and guide viewer attention.
- ✘ **Shows AI wait times**: Never show 10-30 seconds of "loading" while waiting for AI. Use time compression, jump cuts, or pre-captured responses. See AI Feature Handling section.
- ✘ **Ends with "run this to build"**: The workflow ends when the VIDEO IS PLAYING, not when files are created.

## II. Mandatory Patterns (Must Apply)

The LLM **must** ensure:

- ✔ **End-to-end automation** with single command execution that produces viewable demo video
- ✔ **Continuous video recording** using Playwright's `video: 'on'` mode, NOT screenshot sequences
- ✔ **Scene-narration alignment validation** - before capture, verify each scene's URL matches its narration
- ✔ **No duplicate URLs** - each scene must show a different page; validate uniqueness before capture
- ✔ **Complete feature coverage** - discover all major features and ensure each gets dedicated screen time
- ✔ **Data discovery** before scene planning to identify valid project IDs and verify page content
- ✔ **Burned-in subtitles** using professional styling (semi-transparent background, centered, readable font)
- ✔ **Separate subtitle files** (SRT and VTT formats) for accessibility
- ✔ **Cross-platform scripts** appropriate for detected OS (PowerShell/Bash)
- ➜ **Voiceover generation** using pyttsx3 (offline TTS - works in corporate environments)
- ✔ **Video/audio merge** using moviepy to produce final MP4 with voiceover
- ✔ **Demo manifest** (YAML) documenting all scenes, timing, and configuration
- ✔ **Audience adaptation** adjusting content, pace, and focus based on target audience
- ✔ **Modular component storage** with separate frames/ directory containing individual scene configs
- ✔ **Zoom effects** on key features using smooth easing functions (ease-in-out)
- ✔ **Smooth transitions** between scenes (crossfade default, 0.5s duration)
- ✔ **Natural voiceover scripts** using contractions, pauses, and conversational tone
- ✔ **Offline TTS voices** using pyttsx3 (works behind corporate firewalls)
- ✔ **Final video location report** clearly showing path and open command at workflow end

## III. Scene Planning Validation (MANDATORY)

**STEP 1: Discover available pages FIRST**

Before planning scenes, discover all pages in the application:
```bash
# React/Next.js
ls frontend/src/pages/*.tsx
ls src/app/**/page.tsx

# Vue/Nuxt
ls pages/*.vue

# Or check router configuration
cat src/router.ts
```

Map file names to routes (e.g., `UsersPage.tsx` → `/users`).

**STEP 2: URL Uniqueness Check**

```
DUPLICATE URL DETECTOR:
┌─────────────────────────────────────────────────────────────┐
│ List ALL scene URLs before capture:                         │
│                                                             │
│ Scene 1: /dashboard        ✅                               │
│ Scene 2: /dashboard        ❌ DUPLICATE! Use different page │
│ Scene 3: /users            ✅                               │
│ Scene 4: /items            ✅ (list page)                   │
│ Scene 5: /items            ❌ DUPLICATE! Use /items/:id     │
│ Scene 6: /settings         ✅                               │
│ Scene 7: /dashboard        ❌ DUPLICATE! 3rd time!          │
│                                                             │
│ RULE: Each scene MUST go to a DIFFERENT URL                 │
│ TIP: /items (list) and /items/:id (detail) are DIFFERENT    │
└─────────────────────────────────────────────────────────────┘
```

**STEP 3: Narration-URL Alignment Check**

```
ALIGNMENT VALIDATOR:
┌─────────────────────────────────────────────────────────────┐
│ For EACH scene, verify narration matches URL:               │
├─────────────────────────────────────────────────────────────┤
│ ❌ BAD: Narration describes "editing an item" but URL is    │
│         /items (the list page, not the editor!)             │
│ ✅ FIX: URL="/items/{id}" (the detail/editor page)          │
│                                                             │
│ ❌ BAD: Narration mentions "file upload" but URL is /home   │
│ ✅ FIX: URL="/uploads" or wherever upload feature lives     │
│                                                             │
│ ❌ BAD: Narration discusses feature X but URL doesn't show X│
│ ✅ FIX: Navigate to page that SHOWS feature X, or remove    │
│         the narration about X                               │
│                                                             │
│ RULE: Never narrate a feature unless you're ON that page    │
└─────────────────────────────────────────────────────────────┘
```

**STEP 4: Feature Coverage**

For a complete demo, discover the app's key pages and aim to show:
- □ Dashboard/Home (1 scene max - don't repeat!)
- □ Primary list pages (users, items, projects, etc.)
- □ Detail/Editor pages (different from list pages!)
- □ Forms/Create pages (if exists)
- □ Settings/Configuration (if exists)
- □ Reports/Analytics (if exists)
- □ Search (if exists)

**MORE screens with LESS time each** = better executive demo
**Aim for 8-12 unique pages in a 2-3 minute demo**

## IV. AI Feature Handling (Variable Response Times)

AI features (chat, generation, analysis) have unpredictable response times (5-60+ seconds). Dead air kills demos. Use these strategies:

### Strategy 1: Jump Cut (Recommended)

Record input and output separately, splice together with a brief transition:

```typescript
// Scene A: Show user typing prompt
await page.fill('[data-testid="ai-prompt"]', 'Analyze this document...');
await page.click('[data-testid="submit"]');
await showSubtitle(page, "Let's ask the AI to analyze this document...");
await page.waitForTimeout(2000); // Show loading spinner briefly

// CUT - Stop recording, wait for AI, restart recording

// Scene B: Show AI response (pre-captured or waited for off-camera)
await page.waitForSelector('[data-testid="ai-response"]', { timeout: 120000 });
await showSubtitle(page, "And just like that, we have our analysis.");
await page.waitForTimeout(4000); // Show the result
```

**Video editing**: In moviepy merge step, crossfade between input and output clips.

### Strategy 2: Time Compression

Speed up the waiting portion (2x-8x) while keeping input/output at normal speed:

```python
# In build-demo.py merge step
from moviepy.editor import VideoFileClip, concatenate_videoclips

input_clip = VideoFileClip("ai_input.webm")
wait_clip = VideoFileClip("ai_waiting.webm").fx(vfx.speedx, 4.0)  # 4x speed
output_clip = VideoFileClip("ai_output.webm")

final = concatenate_videoclips([input_clip, wait_clip, output_clip])
```

### Strategy 3: Pre-Capture with Cache

Before demo recording, trigger the AI call to warm the cache:

```typescript
// Pre-warm AI before demo capture
test.beforeAll(async ({ request }) => {
  // Trigger AI call to cache response
  await request.post('/api/ai/analyze', {
    data: { document_id: 'demo-doc-001' }
  });
  // Wait for completion
  await new Promise(r => setTimeout(r, 30000));
});

// During demo, cached response returns instantly
test('Demo with AI feature', async ({ page }) => {
  await page.goto('/ai-analyze');
  await page.click('[data-testid="analyze"]');
  // Response is instant from cache
  await page.waitForSelector('[data-testid="result"]');
});
```

### Strategy 4: Transition Overlay

Show a professional "processing" transition instead of loading spinner:

```typescript
async function showAIProcessingTransition(page: Page) {
  await page.evaluate(() => {
    const overlay = document.createElement('div');
    overlay.id = 'ai-transition';
    overlay.innerHTML = `
      <div style="text-align: center;">
        <div style="font-size: 32px; margin-bottom: 16px;">🤖 AI Processing</div>
        <div style="font-size: 18px; opacity: 0.8;">Typically completes in 5-15 seconds</div>
      </div>
    `;
    overlay.style.cssText = `
      position: fixed; top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.9); color: white;
      display: flex; align-items: center; justify-content: center;
      font-family: system-ui; z-index: 10000;
    `;
    document.body.appendChild(overlay);
  });
  await page.waitForTimeout(2000); // Brief pause
  // Then cut to result
}
```

### Strategy 5: Narration Bridge

Use voiceover to bridge the gap while showing abbreviated wait:

```
Narration during AI wait (keep video to 3-4 seconds):
"While the AI processes this... [brief pause] ...there we go."
```

### Decision Matrix

| Scenario | Best Strategy | Why |
|----------|---------------|-----|
| AI responds in <5s | Show real-time | Fast enough |
| AI responds in 5-15s | Time compression | Reasonable wait sped up |
| AI responds in 15-60s | Jump cut | Too long to show |
| AI is unreliable | Pre-capture cache | Ensure demo works |
| First-time demo | Transition overlay | Professional feel |

### Anti-Patterns

- ❌ Showing 30 seconds of loading spinner
- ❌ Awkward silence while waiting
- ❌ Narrator saying "this usually takes about 30 seconds..."
- ❌ Fake/mock AI responses (dishonest)
- ❌ Skipping AI features entirely

## V. Preferred Patterns (Recommended)

The LLM **should** adopt:

- ➜ **Feature auto-discovery** scanning all pages, routes, and navigation to identify demo-worthy content
- ➜ **Audience-specific filtering** showing only relevant features for executive/technical/business audiences
- ➜ **Logical scene ordering** following natural user workflow (Dashboard → Core features → Advanced → Settings)
- ➜ **Professional voice settings** using pyttsx3 with Microsoft David/Zira at 145 WPM for clarity
- ➜ **More screens, less time each** - prefer 10+ quick scenes over 5 long ones for executive demos
- ➜ **Real interactions** - show mouse movements, clicks, typing - not static screenshots
- ➜ **Navigate to DIFFERENT pages** - /dashboard and /dashboard/:id are DIFFERENT pages
- ➜ **Don't narrate non-existent features** - if no AI page exists, don't talk about AI
- ➜ **1920x1080 resolution** for standard HD compatibility across all displays
- ➜ **Single continuous recording** for smooth transitions without cuts
- ➜ **npm script fallback** providing cross-platform `npm run build` option
- ➜ **Existing E2E test reuse** leveraging test infrastructure for demo scenes

## VI. Output Structure

The LLM **must** generate this directory structure:

```
demo/
├── manifest.yaml              # Master configuration (scenes, timing, zoom)
├── README.md                  # Quick start and final video location
│
├── assets/                    # All generated outputs
│   ├── video/
│   │   ├── raw/               # Raw scene captures (pre-processing)
│   │   ├── processed/         # Post-processing (zoom applied)
│   │   └── final/             # Complete demos ← MAIN OUTPUT
│   │       └── [product]-demo-final.mp4
│   ├── audio/
│   │   └── voiceover/         # Generated voiceovers (MP3)
│   ├── screenshots/
│   │   ├── annotated/         # With highlights
│   │   └── clean/             # Without annotations
│   └── subtitles/             # SRT and VTT files
│
├── frames/                    # Individual frame definitions (MODULAR)
│   ├── scene-01-intro/
│   │   ├── frame.yaml         # Frame metadata
│   │   ├── script.md          # Narration for this scene
│   │   └── zoom-config.yaml   # Zoom effect settings
│   └── scene-XX-.../
│
├── scripts/
│   ├── run-demo.ps1           # Windows runner
│   ├── run-demo.sh            # macOS/Linux runner
│   ├── build-demo.py          # Python build pipeline
│   └── generate-voiceover.py  # Voiceover generation
│
├── captures/
│   └── demo-capture.spec.ts   # Playwright capture script
│
└── docs/
    ├── presenter-guide.md
    └── maintenance-guide.md
```

## V. Audience Profiles

### Executive (`audience: executive`)
- **Duration**: 1-2 minutes
- **Focus**: ROI, metrics, dashboards, high-level value
- **Pace**: Fast, punchy transitions
- **Scenes**: Max 4 scenes
- **Content**: Skip technical details, emphasize business outcomes

### Technical (`audience: technical`)
- **Duration**: 3-5 minutes
- **Focus**: Architecture, APIs, integrations, workflows
- **Pace**: Moderate, allow time for details
- **Scenes**: Up to 10 scenes
- **Content**: Configuration options, API responses, error handling

### Business Analyst (`audience: business`)
- **Duration**: 2-3 minutes
- **Focus**: Workflows, traceability, reporting
- **Pace**: Moderate
- **Scenes**: 6 scenes
- **Content**: Requirements management, process flows, matrices

### General (`audience: general`)
- **Duration**: 2-3 minutes
- **Focus**: Balanced overview
- **Pace**: Moderate
- **Scenes**: All high-priority features
- **Content**: Auto-discovered features in logical order

## VII. Quality Standards

### Video Quality
- Resolution: 1920x1080 (HD)
- Format: WebM (capture), MP4 (final with audio)
- Frame rate: 30fps minimum
- **Mode: CONTINUOUS VIDEO recording, NOT screenshot sequences**

```typescript
// CORRECT - Video recording
test.use({
  video: {
    mode: 'on',  // Records continuous video
    size: { width: 1920, height: 1080 },
  },
});

// WRONG - Screenshots only
await page.screenshot({ path: 'frame1.png' });  // ❌ Not a video!
```

**The demo should capture actual mouse movements, scrolling, and interactions - not static images stitched together.**

### Audio Quality
- Engine: pyttsx3 (offline TTS - works in corporate environments)
- Voice: Microsoft David Desktop (male) or Microsoft Zira (female)
- Rate: 145 WPM (slower than default for clarity)
- Format: MP3 (generation), AAC (final merge)
- Style: Natural, conversational (contractions, pauses, engagement)

**Note:** edge-tts neural voices are NOT recommended for AT&T corporate environments.
They require external network access to Microsoft Edge TTS services which is blocked
by corporate firewalls. Use pyttsx3 which works entirely offline.

### Zoom Effects
- Default factor: 1.3-1.5 (30-50% zoom)
- Duration: 2-4 seconds for zoom in/out
- Easing: ease-in-out for smooth motion
- Target: Primary action elements, data visualizations, new features

### Transitions
- Default: crossfade (0.5s)
- Section changes: fade-black (0.7s)
- Sequential workflow: slide-left (0.5s)
- Duration: 0.3s-1.0s (never longer than scene)

### Subtitle Quality
- Background: Semi-transparent black (rgba(0,0,0,0.75))
- Font: System sans-serif, 22px
- Position: Bottom center, 60px from edge
- Max width: 80% of screen

## VIII. Known Issues & Required Fixes

### MoviePy 2.x API Changes (CRITICAL)

MoviePy 2.x has breaking API changes. Use the NEW syntax:

```python
# OLD (MoviePy 1.x) - DON'T USE
from moviepy.editor import VideoFileClip  # ❌
clip.subclip(0, 10)                        # ❌
clip.set_audio(audio)                      # ❌
clip.write_videofile(..., verbose=False)   # ❌

# NEW (MoviePy 2.x) - USE THIS
from moviepy import VideoFileClip          # ✅
clip.subclipped(0, 10)                     # ✅
clip.with_audio(audio)                     # ✅
clip.write_videofile(...)                  # ✅ (no verbose param)
```

### Playwright Configuration Discovery (CRITICAL)

**Never assume spec location.** Always read `playwright.config.ts`:

```typescript
// Discover testDir from playwright.config.ts
const configPath = 'frontend/playwright.config.ts';
const config = await readConfig(configPath);
const testDir = config.testDir || './tests/e2e';

// Place spec in the correct directory
const specPath = path.join('frontend', testDir, 'demo-capture.spec.ts');
```

### Port Detection (CRITICAL)

Vite auto-increments ports when busy. **Scan multiple ports:**

```typescript
async function findDevServer(): Promise<number> {
  const ports = [5173, 5174, 5175, 5176, 5177, 5178, 3000, 3001];
  for (const port of ports) {
    try {
      const response = await fetch(`http://localhost:${port}`);
      if (response.ok) {
        console.log(`✓ Found dev server on port ${port}`);
        return port;
      }
    } catch {}
  }
  throw new Error('No dev server found. Start with: npm run dev');
}
```

### Windows npx Execution (CRITICAL)

`subprocess.run(["npx", ...])` fails on Windows without shell:

```python
import platform

# Windows requires shell=True for npx
shell = platform.system() == 'Windows'
subprocess.run(["npx", "playwright", "test", spec], shell=shell)
```

### test.use() Placement (Playwright)

**Must be at file top-level**, not inside describe():

```typescript
// ❌ WRONG - causes error
test.describe('Demo', () => {
  test.use({ video: 'on' });  // Error!
});

// ✅ CORRECT - top-level
test.use({ 
  video: { mode: 'on', size: { width: 1920, height: 1080 } }
});

test.describe('Demo', () => {
  // tests here
});
```

### Audio/Video Timing Desync (CRITICAL)

Voice starts before page loads. **Add initial delay:**

```typescript
// BEFORE first subtitle - wait for app to fully render
await page.goto('/dashboard');
await page.waitForLoadState('networkidle');
await page.waitForTimeout(3000);  // Extra buffer for animations

// THEN start narration
await showSubtitle(page, "Welcome to the application...");
```

### Backend Data Verification (CRITICAL)

**Always verify data exists before capture:**

```typescript
test.beforeAll(async ({ request }) => {
  // Health check
  const health = await request.get('http://localhost:8000/api/v1/health');
  if (!health.ok()) throw new Error('Backend not responding');
  
  // Data check
  const projects = await request.get('http://localhost:8000/api/v1/projects');
  const data = await projects.json();
  if (data.length === 0) {
    console.warn('⚠️ No projects found - demo may show empty states');
  }
});
```

### Screenshot Capture (REQUIRED)

**Always capture screenshots at each scene:**

```typescript
// In scene capture loop
await page.screenshot({ 
  path: `demo/assets/screenshots/scene_${sceneId}.png`,
  fullPage: false 
});
```

## IX. Error Handling

### No Data Found
- Warn user that demo may show empty states
- Suggest seeding data first
- Offer to create minimal demo data

### Playwright Not Installed
- Provide installation command: `npx playwright install chromium`
- Halt execution until resolved

### App Not Running
- Check both frontend and backend URLs
- **Automatically start servers if not running**
- Wait for servers to be ready (backend: 30s, frontend: 60s)
- Clean up started servers on script exit
- Only halt if servers fail to start after timeout

### Voice Generation Failed
- Fall back to subtitle-only video
- Log warning about missing voiceover
- Continue with silent video option

---

## VIII. Natural Script Guidelines

For AI-generated voiceovers to sound human:

### ✅ DO
- Use contractions: "you'll", "we're", "that's", "let's"
- Add pauses: "..." for natural breathing
- Use conversational phrases: "Now let's", "Here's where", "Notice how"
- Ask rhetorical questions: "Pretty cool, right?", "See how easy that was?"
- Add transitions: "Moving on to...", "Next up..."

### ❌ DON'T
- Write formal sentences: "The system displays real-time metrics."
- Use passive voice: "The data is processed by the system."
- Leave acronyms unexplained: "KPI" without context
- Create wall-of-text scripts without pauses

### Example Transformation

**Before (Robotic):**
"This dashboard displays real-time metrics. Users can view KPIs and make data-driven decisions."

**After (Natural):**
"Here's your dashboard... and right away, you'll notice the real-time metrics updating. See those numbers changing? That's live data, flowing in as your team works. Pretty powerful, right?"

---

## IX. Workflow Completion Criteria

**The `/scaffold-demo` workflow is NOT complete until ALL of these are true:**

| Criterion | Check |
|-----------|-------|
| Files created | `demo/` folder with all components exists |
| App verified running | Frontend returns HTTP 200 |
| Pipeline executed | `run-demo.ps1` or `run-demo.sh` ran to completion |
| Video exists | `demo/assets/video/final/*.mp4` file present |
| Video opened | Final video playing in user's default player |
| Report shown | Completion report with video path displayed |

**If ANY of these are false, the workflow FAILED. Do not claim success.**

### Success Message Template

Only show this AFTER the video is playing:

```
═══════════════════════════════════════════════════════════════
✅ DEMO GENERATION COMPLETE
═══════════════════════════════════════════════════════════════

📹 Final Video: demo/assets/video/final/[product]-demo-final.mp4
⏱️  Duration: [X] minutes
🎤 Voice: en-US-GuyNeural (natural AI)
🎯 Audience: [audience type]

The video should now be playing on your screen.
═══════════════════════════════════════════════════════════════
```

### Failure Handling

If pipeline fails at any step:
1. Show clear error message
2. **Attempt to fix it automatically** (e.g., install missing package, adjust selector)
3. Retry the failed step
4. If still failing, suggest manual fix and offer to retry
5. Do NOT claim partial success

### Continuous Improvement

**When you encounter and fix an error, include an "Archetype Improvement Recommendation" in your completion summary:**

```
═══════════════════════════════════════════════════════════════
📝 ARCHETYPE IMPROVEMENT RECOMMENDATION
═══════════════════════════════════════════════════════════════

Issue Encountered: [Brief description of what went wrong]
Root Cause: [Why it happened]
Fix Applied: [What you did to fix it]

Recommended Archetype Update:
- File: [constitution.md / scaffold-demo.md / env-config.yaml]
- Section: [Which section to update]
- Change: [Specific change to prevent this in future]

This will help prevent the same issue for future users.
═══════════════════════════════════════════════════════════════
```

**Examples of improvement recommendations:**
- Missing package → Add to env-config.yaml dependencies
- Selector not found → Add fallback selector pattern to constitution
- Timeout too short → Update default timeout in scaffold-demo.md
- Edge case not handled → Add to error handling section

---

## XII. Enhanced Archetype Patterns (v1.2.0)

### A. OS Detection (Step 0)

- **Detect OS up front** (PowerShell `Get-OS` or `uname -s`) and branch workflow:
  - **Windows**: run `demo/scripts/run-demo.ps1` (full automation: server check, Playwright capture, voiceover, merge, open). Requires PowerShell, Node+Playwright deps, Python venv, ffmpeg optional if using merge script.
  - **macOS/Linux**: run `demo/scripts/run-demo.sh` (bash helper). Requires bash, curl, Node+Playwright deps, Python 3, ffmpeg. If using PowerShell Core, you may still call `run-demo.ps1`, but bash is the default.
- **Prerequisite check**: ensure Node + Playwright deps installed, Python 3 available, ffmpeg installed (e.g., `brew install ffmpeg` on macOS, `apt-get install ffmpeg` on Debian/Ubuntu).
- **Routing to specialist**: when invoking `/scaffold-automation`, include the detected OS so the automation-scripter archetype returns both Windows and macOS/Linux branches.

### A. Simulation Testing (Phase 2)

**Hard-Stop Rule:** Archetype testing is NOT complete until simulation testing passes with 90%+ confidence.

**Simulation testing validates effectiveness, not just structure:**

1. **Design Representative Task**: Extract from use cases (e.g., "Create 2-minute executive demo")
2. **Execute Full Workflow**: Run `/scaffold-demo` with realistic parameters
3. **Track During Execution**: Monitor for URL uniqueness, narration alignment, feature coverage
4. **Evaluate Results**: Check for duplicate URLs, empty states, misaligned narration
5. **Generate Reasoning Trace**: Document issues, root causes, recommended fixes
6. **Iterate**: Fix issues and re-test until 90%+ confidence achieved

**See:** `test-demo.md` Phase 2 for full simulation testing protocol.

### B. Orchestration (Delegate to Specialists)

**Pattern:** Instead of manually creating scripts, delegate to specialized archetypes.

**Example: Script Generation**
```bash
# Discover appropriate archetype
python3 .cdo-aifc/scripts/python/discover-archetype.py \
  --input "Create PowerShell script to run demo pipeline" \
  --json

# Route to specialist
/scaffold-automation "Create PowerShell script run-demo.ps1 that:
- Detects if servers are running
- Auto-starts servers if needed
- Runs Playwright capture
- Generates voiceover
- Merges video/audio
- Opens final video"
```

**Benefits:**
- ✅ Scripts follow automation-scripter best practices
- ✅ Consistent error handling
- ✅ Cross-platform compatibility
- ✅ 70%+ reduction in manual script writing

**See:** `scaffold-demo.md` Step 5.5 for full orchestration examples.

### C. Collaborative Design (Upfront Guidance)

**Pattern:** Guide users through demo planning before capture to prevent common issues.

**Collaborative Design Steps:**

1. **Feature Discovery Analysis**: Scan app, present all pages, recommend scenes
2. **Identify Logical Pitfalls**: Check for duplicate URLs, narration misalignment, missing data
3. **Recommend Scene Structure**: Propose optimal scene order with timing
4. **Data Verification**: Verify data exists before capture

**Benefits:**
- ✅ Catches duplicate URLs before capture (saves 30+ min rework)
- ✅ Validates feature coverage upfront
- ✅ Ensures data exists (no empty states)
- ✅ Prevents narration-visual misalignment
- ✅ Investment: 10-15 min upfront saves hours of rework

**See:** `scaffold-demo.md` Step 4.5 for full collaborative design protocol.

---

**Version**: 2.2.0
**Last Updated**: 2025-01-06
**Source**: Derived from Playwright best practices, AT&T demo standards, and Enhanced Archetype Builder v1.2.0
