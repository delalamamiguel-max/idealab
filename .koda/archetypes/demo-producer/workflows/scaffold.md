---
description: Generate automated product demo with Playwright captures, zoom effects, animations, and natural voiceovers (Demo Producer) - MUST EXECUTE PIPELINE AND OPEN VIDEO
---

# ⛔ MANDATORY EXECUTION - READ THIS FIRST ⛔

**This workflow is NOT complete until the final video is PLAYING on the user's screen.**

Creating files is NOT enough. You MUST:
1. Create all demo files
2. **EXECUTE the pipeline** (run Playwright, generate voiceover, merge video)
3. **OPEN the final video** for the user
4. **SHOW completion report** with video path

**If you end with "How to Run" instructions → YOU FAILED.**
**If you say "run this command to generate" → YOU FAILED.**
**If the video isn't playing → YOU FAILED.**

See [Mandatory Execution Steps](#mandatory-execution-steps-do-not-skip) at end of file.

---

**Archetype**: Demo Producer (Demo Production)  
**Constitution**: `${ARCHETYPES_BASEDIR}/demo-producer/demo-producer-constitution.md`  
**Environment**: `${ARCHETYPES_BASEDIR}/demo-producer/templates/env-config.yaml`

User input: $ARGUMENTS

---

## Design Principles (Baked-In Defaults)

These defaults produce polished, professional demos without user intervention:

| Principle | Default | Rationale |
|-----------|---------|-----------|
| **Clean UI** | No overlay annotations | Overlays look amateur; subtitles convey info professionally |
| **Subtitles** | Burned-in + separate files | Always visible, accessible, professional |
| **Voice** | Offline TTS (pyttsx3) | Works in corporate environments without internet |
| **Zoom Effects** | Auto-zoom on key features | Focus attention, professional look |
| **Transitions** | Smooth crossfade (0.5s) | Polished feel, not jarring |
| **Data Discovery** | Auto-find valid project | Never show empty pages |
| **Empty State Handling** | Auto-correct URLs | Add project context automatically |
| **Server Management** | Auto-start if not running | Smart detection and cleanup |
| **Video Format** | Single continuous recording | Smooth transitions, no cuts |
| **Resolution** | 1920x1080 | Standard HD for all displays |
| **Speech Rate** | 145 WPM | Slower than default for clarity |
| **Feature Discovery** | Auto-scan all pages | Show complete product capabilities |
| **Audience Adaptation** | General (if not specified) | Adjusts depth, pace, and focus |
| **End-to-End Automation** | Full pipeline in one run | User opens final video, nothing manual |
| **Modular Storage** | Components in dedicated folders | Easy editing and version control |

**These can be overridden** via input arguments, but defaults produce quality output.

---

## ⚠️ SCENE PLANNING VALIDATION (Do Before Creating Spec)

**Before writing the Playwright spec, validate your scene plan:**

### Step A: Discover Available Pages

```bash
# React/Next.js apps
ls frontend/src/pages/*.tsx
ls src/app/**/page.tsx

# Vue/Nuxt apps
ls pages/*.vue

# Or check router configuration
cat src/router.ts
cat src/App.tsx | grep "path:"
```

Example output (your app will differ):
- `DashboardPage.tsx` → `/dashboard`
- `UsersPage.tsx` → `/users` (list)
- `UserDetailPage.tsx` → `/users/:id` (detail - DIFFERENT from list!)
- `SettingsPage.tsx` → `/settings`
- `ReportsPage.tsx` → `/reports`

### Step B: URL Uniqueness Check

```
List your planned scene URLs and check for duplicates:

Scene 1: /dashboard        ✅
Scene 2: /dashboard        ❌ DUPLICATE! Use /users instead
Scene 3: /users            ✅ (list page)
Scene 4: /users            ❌ DUPLICATE! Use /users/:id (detail)
Scene 5: /users/:id        ✅ (detail page - different from list!)
Scene 6: /settings         ✅
Scene 7: /dashboard        ❌ DUPLICATE! Use /reports instead

RULE: Each scene MUST go to a DIFFERENT URL
TIP: /items (list) and /items/:id (detail) are DIFFERENT pages
```

### Step C: Narration-URL Alignment

```
For EACH scene, verify narration matches what will be ON SCREEN:

❌ BAD: 
   URL: /items (list page)
   Narration: "Here you can edit the item details..."
   Problem: List page doesn't show editor!
   
✅ FIX:
   URL: /items/{itemId} (detail/editor page)
   Narration: "Here you can edit the item details..."

❌ BAD:
   URL: /dashboard
   Narration: "Upload your files here..."
   Problem: Dashboard doesn't have upload!
   
✅ FIX:
   URL: /uploads (or wherever upload feature lives)
   Narration: "Upload your files here..."

PRINCIPLE: If you SAY it, you must SHOW it. If you can't show it, don't say it.
```

### Step D: Feature Coverage

Discover the app's pages and aim for 8-12 unique screens:
- Dashboard/Home (1x only - don't repeat!)
- Primary list pages
- Detail/Editor pages (different from list!)
- Create/Form pages
- Settings/Config
- Reports/Analytics
- Search

**MORE screens with LESS time each = more impactful executive demo**

---

## Handling AI Features (Variable Response Times)

AI features have unpredictable response times (5-60+ seconds). **Never show dead air.**

### Quick Decision Guide

| AI Response Time | Strategy |
|------------------|----------|
| <5 seconds | Show real-time (no edit needed) |
| 5-15 seconds | Time compression (speed up 4x) |
| 15-60 seconds | Jump cut (splice input → output) |
| Unreliable | Pre-capture with cache warming |

### Jump Cut Implementation

```typescript
// SCENE: AI Feature Demo
// Part 1: Show input (normal speed)
await page.fill('[data-testid="ai-input"]', 'Generate a summary...');
await page.click('[data-testid="submit"]');
await showSubtitle(page, "Let's ask the AI to generate a summary...");
await page.waitForTimeout(2000); // Brief loading indicator

// === NATURAL BREAK POINT ===
// Wait for AI off-camera, or pre-capture this response
await page.waitForSelector('[data-testid="ai-result"]', { timeout: 120000 });

// Part 2: Show output (normal speed)
await showSubtitle(page, "And there's our summary, ready to use.");
await page.waitForTimeout(4000);
```

### Narration Bridge

```
"Let's see what the AI comes up with... [2 second pause, cut] ...and there we go."
```

### Anti-Patterns

- ❌ 30 seconds of loading spinner
- ❌ Narrator: "This usually takes about 30 seconds..."
- ❌ Skipping AI features entirely
- ❌ Fake/mock responses

---

## 🔧 PRE-CAPTURE CHECKLIST (Run Before Every Capture)

**These checks prevent the most common failures:**

### 1. Port Detection (Vite auto-increments!)

```python
# DON'T hardcode port 5173!
import requests

def find_frontend_port():
    """Scan multiple ports - Vite increments when busy"""
    for port in [5173, 5174, 5175, 5176, 5177, 5178, 3000, 3001]:
        try:
            r = requests.get(f'http://localhost:{port}', timeout=2)
            if r.status_code == 200:
                print(f'✓ Frontend on port {port}')
                return port
        except:
            pass
    raise Exception('Frontend not running!')
```

### 2. Server Auto-Start (NEW - Smart Detection)

```python
def ensure_servers_running():
    """Check if servers are running, start them if not"""
    import subprocess
    import time
    
    backend_running = False
    frontend_running = False
    started_processes = []
    
    # Check backend
    try:
        r = requests.get('http://localhost:8000/api/v1/health', timeout=3)
        backend_running = r.status_code == 200
    except:
        pass
    
    if not backend_running:
        print('🚀 Starting backend server...')
        python_exe = 'backend/.venv/Scripts/python.exe'  # Windows
        if not os.path.exists(python_exe):
            python_exe = 'backend/.venv/bin/python'  # Unix
        
        proc = subprocess.Popen(
            [python_exe, '-m', 'uvicorn', 'app.main:app', '--host', '0.0.0.0', '--port', '8000'],
            cwd='backend',
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        started_processes.append(('backend', proc))
        
        # Wait for backend to start (max 30 seconds)
        for _ in range(15):
            time.sleep(2)
            try:
                r = requests.get('http://localhost:8000/api/v1/health', timeout=2)
                if r.status_code == 200:
                    backend_running = True
                    print('✅ Backend started')
                    break
            except:
                pass
    
    # Check frontend
    try:
        r = requests.get('http://localhost:5173', timeout=3)
        frontend_running = r.status_code == 200
    except:
        pass
    
    if not frontend_running:
        print('🚀 Starting frontend server...')
        proc = subprocess.Popen(
            ['npm', 'run', 'dev'],
            cwd='frontend',
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=True  # Required for Windows
        )
        started_processes.append(('frontend', proc))
        
        # Wait for frontend to start (max 60 seconds)
        for _ in range(20):
            time.sleep(3)
            try:
                r = requests.get('http://localhost:5173', timeout=2)
                if r.status_code == 200:
                    frontend_running = True
                    print('✅ Frontend started')
                    break
            except:
                pass
    
    if not backend_running or not frontend_running:
        # Clean up started processes
        for name, proc in started_processes:
            proc.terminate()
        raise Exception('Failed to start servers')
    
    return started_processes  # Return so we can clean up later

def verify_backend():
    """Ensure backend is responding with real data"""
    try:
        # Health check
        r = requests.get('http://localhost:8000/api/v1/health')
        if r.status_code != 200:
            raise Exception('Backend health check failed')
        
        # Data check - ensure not empty
        projects = requests.get('http://localhost:8000/api/v1/projects').json()
        if len(projects) == 0:
            print('⚠️ WARNING: No projects found - demo will show empty states!')
        else:
            print(f'✓ Found {len(projects)} projects')
            
    except Exception as e:
        raise Exception(f'Backend not ready: {e}')
```

### 3. Playwright Config Discovery

```python
import re

def find_playwright_test_dir():
    """Read testDir from playwright.config.ts - don't assume location"""
    config_path = 'frontend/playwright.config.ts'
    with open(config_path, 'r') as f:
        content = f.read()
    
    # Find testDir setting
    match = re.search(r"testDir:\s*['\"]([^'\"]+)['\"]", content)
    if match:
        return match.group(1)  # e.g., './tests/e2e'
    return './tests/e2e'  # default
```

### 4. Windows npx Fix

```python
import platform
import subprocess

def run_playwright(spec_path):
    """npx requires shell=True on Windows"""
    shell = platform.system() == 'Windows'
    subprocess.run(
        ['npx', 'playwright', 'test', spec_path, '--project=chromium'],
        cwd='frontend',
        shell=shell,
        check=True
    )
```

### 5. MoviePy 2.x Syntax

```python
# Use NEW MoviePy 2.x syntax
from moviepy import VideoFileClip, AudioFileClip  # NOT moviepy.editor

video = VideoFileClip('raw.webm')
audio = AudioFileClip('voiceover.mp3')

# NEW methods
video = video.subclipped(0, 60)      # NOT subclip()
video = video.with_audio(audio)       # NOT set_audio()
video.write_videofile('output.mp4')   # NO verbose param
```

### 6. Initial Timing Delay (Voice Sync)

```typescript
// In Playwright spec - CRITICAL for audio sync
test('Demo', async ({ page }) => {
  // Wait for app to FULLY render before starting
  await page.goto('/dashboard');
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(3000);  // ← CRITICAL: Buffer before voice

  // NOW start the narration
  await showSubtitle(page, "Welcome to the application...");
});
```

### 7. Screenshot at Each Scene

```typescript
// Capture screenshot at EVERY scene
async function captureScene(page: Page, sceneId: string, url: string) {
  await page.goto(url);
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1500);
  
  // ALWAYS capture screenshot
  await page.screenshot({ 
    path: path.join(__dirname, `../assets/screenshots/${sceneId}.png`),
    fullPage: false 
  });
}
```

### 8. test.use() at Top Level

```typescript
// ✅ CORRECT - at file top level
test.use({ 
  video: { mode: 'on', size: { width: 1920, height: 1080 } },
  viewport: { width: 1920, height: 1080 },
});

// ❌ WRONG - inside describe block (causes error)
test.describe('Demo', () => {
  test.use({ video: 'on' });  // ERROR!
});
```

---

## CRITICAL: End-to-End Automation

**The archetype MUST produce a viewable demo video in ONE execution.** The user should NOT have to:
- ❌ Run Playwright manually
- ❌ Copy video files from test-results
- ❌ Run FFmpeg commands manually
- ❌ Generate voiceover separately
- ❌ Merge audio and video manually

**Instead, the archetype MUST:**
- ✅ Create all files (script, spec, subtitles)
- ✅ Run Playwright capture automatically
- ✅ Copy video to demo folder automatically
- ✅ Generate voiceover using pyttsx3 (offline TTS - works in corporate environments)
- ✅ Apply zoom effects to highlight key features
- ✅ Add smooth transitions between scenes
- ✅ Merge video + audio + effects using moviepy
- ✅ Open the final video with voiceover for the user
- ✅ Report final video location to user

**Required Python packages:**
```bash
pip install pyttsx3 moviepy
```

**Note:** Do NOT use edge-tts - it requires external network access which is blocked
in corporate environments (AT&T). Use pyttsx3 which works entirely offline.

**Voiceover Generation (pyttsx3 - offline TTS):**
```python
import pyttsx3
from pathlib import Path

def generate_voiceover(script: str, output_path: str, rate: int = 145):
    """
    Generate voiceover using pyttsx3 (offline TTS).
    Works in corporate environments without internet access.
    
    Available Windows SAPI voices:
    - Microsoft David Desktop (male - RECOMMENDED)
    - Microsoft Zira Desktop (female)
    - Microsoft Mark (male, if available)
    
    Script optimization tips for better sound:
    - Use contractions: "you'll" not "you will"
    - Add commas for natural pauses
    - Use ellipsis "..." for longer pauses
    - Avoid acronyms; spell out or use periods (A.I. not AI)
    - Write conversationally, not formally
    """
    engine = pyttsx3.init()
    
    # Set voice (prefer David for male)
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'david' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    
    # Set rate (145 WPM is slower than default for clarity)
    engine.setProperty('rate', rate)
    
    # Save to file
    engine.save_to_file(script, output_path)
    engine.runAndWait()

# Generate voiceover
generate_voiceover(
    script=narration_text,
    output_path='demo/assets/audio/voiceover/narration.mp3',
    rate=145
)
```

**Script Writing for Natural AI Voice:**
```markdown
## Natural Script Guidelines

❌ BAD (robotic):
"This dashboard displays real-time metrics. Users can view KPIs."

✅ GOOD (natural):
"Here's your dashboard... and right away, you'll notice the real-time metrics updating. 
Pretty cool, right? Let's take a closer look at these KPIs."

### Key Techniques:
1. **Use contractions** - "you'll", "we're", "that's"
2. **Add breaths** - Use "..." for natural pauses
3. **Conversational phrases** - "Now, let's", "Here's where", "Notice how"
4. **Questions** - "See how easy that was?"
5. **Transitions** - "Moving on to...", "Next up..."
6. **Avoid jargon** - Spell out abbreviations first time
```

**Video Processing with Zoom and Transitions:**
```python
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip
from moviepy.video.fx import CrossFadeIn, CrossFadeOut, Resize, Crop

def apply_zoom_effect(clip, zoom_center, zoom_factor=1.5, duration=3):
    """
    Apply smooth zoom effect using moviepy's built-in resize capability.
    zoom_center: (x, y) normalized coordinates (0-1)
    zoom_factor: how much to zoom (1.5 = 50% zoom in)
    """
    w, h = clip.size
    
    def zoom_resize(t):
        # Calculate zoom progress with ease-in-out
        if duration <= 0:
            return zoom_factor
        progress = min(t / duration, 1.0)
        ease = 3 * progress**2 - 2 * progress**3
        return 1 + (zoom_factor - 1) * ease
    
    # Apply time-varying resize using moviepy
    zoomed = clip.resized(lambda t: zoom_resize(t))
    
    # Center the zoom on the target area
    cx, cy = zoom_center[0] * w, zoom_center[1] * h
    
    def position_func(t):
        current_zoom = zoom_resize(t)
        # Calculate offset to keep zoom centered on target
        offset_x = (current_zoom - 1) * cx
        offset_y = (current_zoom - 1) * cy
        return (-offset_x, -offset_y)
    
    return zoomed.with_position(position_func)

def add_crossfade_transitions(clips, fade_duration=0.5):
    """Add smooth crossfade transitions between clips."""
    if len(clips) < 2:
        return clips[0] if clips else None
    
    processed = []
    for i, clip in enumerate(clips):
        if i > 0:
            clip = clip.with_effects([CrossFadeIn(fade_duration)])
        if i < len(clips) - 1:
            clip = clip.with_effects([CrossFadeOut(fade_duration)])
        processed.append(clip)
    
    return concatenate_videoclips(processed, method="compose")

# Build final video with effects
clips = []
for scene in scenes:
    clip = VideoFileClip(scene['video_path'])
    
    # Apply zoom if specified
    if scene.get('zoom'):
        clip = apply_zoom_effect(
            clip, 
            zoom_center=scene['zoom']['center'],
            zoom_factor=scene['zoom']['factor'],
            duration=scene['zoom']['duration']
        )
    
    clips.append(clip)

# Combine with transitions
final_video = add_crossfade_transitions(clips, fade_duration=0.5)

# Add audio
audio = AudioFileClip('demo/assets/audio/voiceover.mp3')
if audio.duration > final_video.duration:
    audio = audio.with_duration(final_video.duration)
final = final_video.with_audio(audio)

# Export
final.write_videofile(
    'demo/assets/video/demo-final.mp4',
    codec='libx264',
    audio_codec='aac',
    fps=30
)
```

**Final output:** `demo/assets/video/[product]-demo-final.mp4` - ready to play!

---

## Cross-Platform Support

**The archetype MUST detect the user's operating system and create appropriate scripts.**

### OS Detection

Before creating automation scripts, detect the OS:

```typescript
// Detect OS from system information
function detectOS(): 'windows' | 'macos' | 'linux' {
  // Check from IDE metadata or system
  const platform = process.platform; // 'win32', 'darwin', 'linux'
  
  if (platform === 'win32') return 'windows';
  if (platform === 'darwin') return 'macos';
  return 'linux';
}
```

### Script Generation by OS

| OS | Script File | Shell | Commands |
|----|-------------|-------|----------|
| **Windows** | `run-demo.ps1` | PowerShell | `Get-ChildItem`, `Copy-Item`, `Start-Process` |
| **macOS** | `run-demo.sh` | Bash/Zsh | `find`, `cp`, `open` |
| **Linux** | `run-demo.sh` | Bash | `find`, `cp`, `xdg-open` |

### Windows Script (PowerShell)

```powershell
# demo/scripts/run-demo.ps1
param([string]$ProductName = "AndiSense", [switch]$SkipVoiceover)

$ErrorActionPreference = "Stop"
Write-Host "🎬 Building $ProductName Demo (Windows)..." -ForegroundColor Cyan

# Run Playwright
Push-Location "$PSScriptRoot/../../frontend"
npx playwright test tests/e2e/demo-*.spec.ts --reporter=list
Pop-Location

# Copy video
$video = Get-ChildItem -Path "$PSScriptRoot/../../frontend/test-results" -Filter "*.webm" -Recurse | 
    Sort-Object LastWriteTime -Descending | Select-Object -First 1
Copy-Item $video.FullName "$PSScriptRoot/../assets/video/$ProductName-demo.webm"

# Open video
Start-Process "$PSScriptRoot/../assets/video/$ProductName-demo.webm"
Write-Host "✅ Done! Video opened." -ForegroundColor Green
```

### macOS/Linux Script (Bash)

```bash
#!/bin/bash
# demo/scripts/run-demo.sh

set -e
PRODUCT_NAME="${1:-AndiSense}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEMO_DIR="$(dirname "$SCRIPT_DIR")"
FRONTEND_DIR="$(dirname "$DEMO_DIR")/frontend"

echo "🎬 Building $PRODUCT_NAME Demo..."

# Run Playwright
cd "$FRONTEND_DIR"
npx playwright test tests/e2e/demo-*.spec.ts --reporter=list

# Find and copy video
VIDEO=$(find "$FRONTEND_DIR/test-results" -name "*.webm" -type f | head -1)
if [ -n "$VIDEO" ]; then
    cp "$VIDEO" "$DEMO_DIR/assets/video/${PRODUCT_NAME,,}-demo.webm"
    echo "✅ Video copied to: $DEMO_DIR/assets/video/${PRODUCT_NAME,,}-demo.webm"
else
    echo "❌ No video found in test-results"
    exit 1
fi

# Open video (OS-specific)
FINAL_VIDEO="$DEMO_DIR/assets/video/${PRODUCT_NAME,,}-demo.webm"
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "$FINAL_VIDEO"
elif command -v xdg-open &> /dev/null; then
    # Linux with xdg-open
    xdg-open "$FINAL_VIDEO"
else
    echo "📹 Video ready: $FINAL_VIDEO"
fi

echo "✅ Done!"
```

### Archetype Decision Logic

When creating the demo package:

```
1. Detect user's OS from IDE metadata or system
2. IF Windows:
   - Create `demo/scripts/run-demo.ps1`
   - Use PowerShell syntax
   - Use `Start-Process` to open video
3. ELSE IF macOS:
   - Create `demo/scripts/run-demo.sh`
   - Use Bash syntax
   - Use `open` command to open video
   - Make script executable: `chmod +x run-demo.sh`
4. ELSE (Linux):
   - Create `demo/scripts/run-demo.sh`
   - Use Bash syntax
   - Use `xdg-open` to open video
   - Make script executable: `chmod +x run-demo.sh`
5. Update README with correct run command for the OS
```

### README OS-Specific Instructions

**For Windows users:**
```markdown
## Quick Start
\`\`\`powershell
cd demo/scripts
.\run-demo.ps1
\`\`\`
```

**For macOS/Linux users:**
```markdown
## Quick Start
\`\`\`bash
cd demo/scripts
chmod +x run-demo.sh  # First time only
./run-demo.sh
\`\`\`
```

### Universal Alternative: npm Script

For maximum portability, also create a `package.json` script that works everywhere:

```json
// demo/package.json
{
  "name": "andisense-demo",
  "scripts": {
    "build": "node scripts/build-demo.js",
    "capture": "cd ../frontend && npx playwright test tests/e2e/demo-*.spec.ts"
  }
}
```

```javascript
// demo/scripts/build-demo.js
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const DEMO_DIR = path.join(__dirname, '..');
const FRONTEND_DIR = path.join(DEMO_DIR, '..', 'frontend');

console.log('🎬 Building demo...');

// Run Playwright
execSync('npx playwright test tests/e2e/demo-*.spec.ts --reporter=list', {
  cwd: FRONTEND_DIR,
  stdio: 'inherit'
});

// Find video
const testResults = path.join(FRONTEND_DIR, 'test-results');
const videos = fs.readdirSync(testResults, { recursive: true })
  .filter(f => f.endsWith('.webm'));

if (videos.length > 0) {
  const src = path.join(testResults, videos[0]);
  const dest = path.join(DEMO_DIR, 'assets', 'video', 'demo.webm');
  fs.copyFileSync(src, dest);
  console.log(`✅ Video: ${dest}`);
  
  // Open video
  const { platform } = process;
  if (platform === 'win32') execSync(`start ${dest}`);
  else if (platform === 'darwin') execSync(`open ${dest}`);
  else execSync(`xdg-open ${dest}`);
}
```

Then users on ANY platform can run:
```bash
cd demo
npm run build
```

### 5.5 Generate Supporting Scripts via Orchestration (ENHANCED)

**Prerequisites:** Ensure Python dependencies are installed:
```bash
pip install pyyaml
```

**Instead of manually creating scripts, delegate to specialized archetypes:**

#### A. PowerShell Runner Script

```bash
python3 .cdo-aifc/scripts/python/discover-archetype.py \
  --input "Create PowerShell script to run demo pipeline" \
  --json
```

✓ Detected: Automation Scripter (confidence: 95%)  
  Routing to: /scaffold-automation

Execute:
```
/scaffold-automation "Create PowerShell script run-demo.ps1 that:
- Detects if frontend/backend servers are running on common ports (5173-5178, 3000-3001, 8000-8001)
- Auto-starts servers if needed (npm run dev, uvicorn)
- Runs Playwright capture (npx playwright test demo/captures/demo-capture.spec.ts)
- Generates voiceover with pyttsx3
- Merges video/audio with moviepy
- Opens final video in default player
- Cleans up temporary files on exit
- Provides progress indicators and error handling
- Supports --skip-voiceover flag for testing"
```

Output: `demo/scripts/run-demo.ps1`

#### B. Python Build Pipeline

```bash
python3 .cdo-aifc/scripts/python/discover-archetype.py \
  --input "Create Python script for video processing pipeline" \
  --json
```

✓ Detected: Automation Scripter (confidence: 92%)  
  Routing to: /scaffold-automation

Execute:
```
/scaffold-automation "Create Python script build-demo.py that:
- Processes raw Playwright video from test-results/
- Applies zoom effects based on demo-manifest.yaml
- Generates voiceover with pyttsx3 (offline TTS)
- Merges audio/video with moviepy
- Generates subtitles (SRT/VTT formats)
- Outputs final MP4 to demo/assets/video/final/
- Includes progress bar with tqdm
- Handles errors gracefully with rollback
- Supports --dry-run mode for testing"
```

Output: `demo/scripts/build-demo.py`

#### C. Voiceover Generation Script

```bash
python3 .cdo-aifc/scripts/python/discover-archetype.py \
  --input "Create Python script for TTS voiceover generation" \
  --json
```

✓ Detected: Automation Scripter (confidence: 94%)  
  Routing to: /scaffold-automation

Execute:
```
/scaffold-automation "Create Python script generate-voiceover.py that:
- Reads script from demo/script/demo-script.md
- Extracts scene narration with timing cues
- Generates audio with pyttsx3 (offline, no API keys)
- Adjusts speech rate to 145 WPM for clarity
- Supports male/female voice selection
- Outputs MP3 to demo/assets/audio/voiceover/
- Validates audio duration matches target
- Includes retry logic for TTS failures"
```

Output: `demo/scripts/generate-voiceover.py`

**Benefits of Orchestration:**
- ✅ Scripts follow automation-scripter best practices
- ✅ Consistent error handling across all scripts
- ✅ Proper logging and validation
- ✅ Cross-platform compatibility (Windows/macOS/Linux)
- ✅ Idempotent operations (safe to re-run)
- ✅ 70%+ reduction in manual script writing
- ✅ Scripts are maintainable and well-documented

**Fallback Strategy:**
If orchestration fails or archetype discovery is unavailable:
1. Generate scripts manually using templates above
2. Log warning that scripts may not follow best practices
3. Recommend running `/refactor-automation` later to improve scripts

---

## Audience-Based Demo Customization

The archetype adapts the demo based on target audience:

### Executive Demo (`audience: executive`)
- **Duration**: 1-2 minutes (short attention span)
- **Focus**: ROI, metrics, dashboards, high-level value
- **Pace**: Fast, punchy transitions
- **Content**: 
  - Skip technical details
  - Emphasize business outcomes
  - Show summary views, not detail pages
  - Highlight integrations with familiar tools (ADO, JIRA)
- **Script tone**: Business value, competitive advantage
- **Scenes**: Dashboard → Key metrics → One "wow" feature → Call to action

### Technical Demo (`audience: technical`)
- **Duration**: 3-5 minutes (deeper exploration)
- **Focus**: Architecture, APIs, integrations, workflows
- **Pace**: Moderate, allow time to see details
- **Content**:
  - Show configuration options
  - Demonstrate API responses (if visible)
  - Walk through complete workflows
  - Show error handling, edge cases
- **Script tone**: How it works, technical capabilities
- **Scenes**: All features with workflow demonstrations

### Business Analyst Demo (`audience: business`)
- **Duration**: 2-3 minutes (balanced)
- **Focus**: Workflows, traceability, reporting
- **Pace**: Moderate
- **Content**:
  - Requirements management
  - Process flows and traceability
  - Matrices and coverage
  - Document processing
- **Script tone**: Process improvement, compliance
- **Scenes**: Core workflows with data examples

### General Demo (`audience: general` or not specified)
- **Duration**: 2-3 minutes
- **Focus**: Balanced overview of all features
- **Pace**: Moderate
- **Content**: All major features, one scene each
- **Script tone**: Neutral, informative
- **Scenes**: Auto-discovered features in logical order

---

## Modular Component Storage

The demo package uses a **modular architecture** for easy editing, versioning, and reuse:

```
demo/
├── manifest.yaml              # Master configuration (scenes, timing, zoom)
├── README.md                  # Quick start and final video location
│
├── assets/                    # All generated outputs
│   ├── video/                 # Video files
│   │   ├── raw/               # Raw scene captures (pre-processing)
│   │   │   ├── scene-01-intro.webm
│   │   │   ├── scene-02-dashboard.webm
│   │   │   └── ...
│   │   ├── processed/         # Post-processing (zoom applied)
│   │   │   ├── scene-01-intro.mp4
│   │   │   └── ...
│   │   └── final/             # Complete demos
│   │       ├── [product]-demo-final.mp4   ← MAIN OUTPUT
│   │       ├── [product]-demo-no-audio.mp4
│   │       └── [product]-executive-demo.mp4
│   │
│   ├── audio/                 # Audio files
│   │   ├── voiceover/         # Generated voiceovers
│   │   │   ├── full-narration.mp3
│   │   │   ├── scene-01-narration.mp3
│   │   │   └── ...
│   │   └── music/             # Background music (optional)
│   │       └── subtle-corporate.mp3
│   │
│   ├── screenshots/           # Static captures
│   │   ├── annotated/         # With highlights
│   │   └── clean/             # Without annotations
│   │
│   └── subtitles/             # Subtitle files
│       ├── demo-subtitles.srt
│       └── demo-subtitles.vtt
│
├── frames/                    # Individual frame definitions
│   ├── scene-01-intro/
│   │   ├── frame.yaml         # Frame metadata
│   │   ├── script.md          # Narration for this scene
│   │   └── zoom-config.yaml   # Zoom effect settings
│   ├── scene-02-dashboard/
│   │   ├── frame.yaml
│   │   ├── script.md
│   │   └── zoom-config.yaml
│   └── ...
│
├── scripts/                   # Automation scripts
│   ├── run-demo.ps1           # Windows runner
│   ├── run-demo.sh            # macOS/Linux runner
│   ├── build-demo.py          # Python build pipeline
│   └── generate-voiceover.py  # Voiceover generation
│
├── captures/                  # Playwright capture specs
│   ├── demo-capture.spec.ts   # Main capture test
│   └── helpers/
│       ├── zoom-helpers.ts    # Zoom effect utilities
│       └── subtitle-helpers.ts
│
└── docs/                      # Generated documentation
    ├── presenter-guide.md
    ├── maintenance-guide.md
    └── CHANGELOG.md
```

### Frame Definition (frames/scene-XX/frame.yaml)

Each scene is self-contained with its own configuration:

```yaml
# frames/scene-02-dashboard/frame.yaml
id: "scene-02"
title: "Dashboard Overview"
type: "video"                  # video | screenshot
duration: 15                   # seconds

# Navigation
url: "/dashboard"
wait_for: "networkidle"
pre_actions:                   # Actions before capture
  - type: "wait"
    selector: "[data-loaded='true']"
    timeout: 5000

# Zoom Effect (optional but recommended for engagement)
zoom:
  enabled: true
  target: ".metrics-panel"     # Element to zoom into
  center: [0.7, 0.3]           # Normalized coordinates
  factor: 1.4                  # Zoom level (1.4 = 40% closer)
  start_time: 3                # When to start zooming (seconds)
  duration: 4                  # How long to zoom

# Transitions
transition:
  in: "crossfade"              # crossfade | slide | fade | cut
  in_duration: 0.5
  out: "crossfade"
  out_duration: 0.5

# Audience variants (optional)
variants:
  executive:
    duration: 8                # Shorter for executives
    zoom:
      factor: 1.6              # More zoom for emphasis
  technical:
    duration: 20               # Longer for technical detail
    include_console: true      # Show browser console
```

### Scene Script (frames/scene-XX/script.md)

```markdown
# Scene 02: Dashboard Overview

**Duration:** 15 seconds  
**Timing:** 0:15 - 0:30

## Narration (Natural Voice)

Here's your dashboard... and right away, you'll notice the real-time metrics updating.

See those numbers changing? That's live data, flowing in as your team works.

Let's zoom in on the key performance indicators...

## Key Visual Cues

- Metrics panel glowing/updating
- Navigation sidebar visible
- User avatar in top-right

## Zoom Focus

At 3 seconds, smoothly zoom to the metrics panel to emphasize real-time updates.

## Transitions

- **IN:** Crossfade from intro (0.5s)
- **OUT:** Crossfade to next scene (0.5s)
```

### Master Manifest (demo/manifest.yaml)

```yaml
# demo/manifest.yaml
demo:
  title: "AndiSense Demo"
  product: "AndiSense"
  version: "2.0.0"
  created: "2025-12-17"
  duration_target: 180         # 3 minutes in seconds
  
  # Target audience (affects defaults)
  audience: "general"          # executive | technical | business | general

# Global settings
settings:
  resolution:
    width: 1920
    height: 1080
  fps: 30
  
  # Voiceover settings
  voice:
    engine: "edge-tts"
    voice_id: "en-US-GuyNeural"
    rate: "-10%"               # Slightly slower for clarity
    pitch: "+0Hz"
  
  # Default transition
  transition:
    type: "crossfade"
    duration: 0.5
  
  # Default zoom (can be overridden per scene)
  zoom:
    default_factor: 1.3
    ease: "ease-in-out"

# Branding
branding:
  primary_color: "#009FDB"     # AT&T Blue
  subtitle_bg: "rgba(0, 0, 0, 0.75)"
  subtitle_font: "ATT Aleck Sans, sans-serif"
  subtitle_size: 22

# Scene order (references frames/ directory)
scenes:
  - "scene-01-intro"
  - "scene-02-dashboard"
  - "scene-03-create-project"
  - "scene-04-requirements"
  - "scene-05-process-flows"
  - "scene-06-ai-analysis"
  - "scene-07-outro"

# Output configuration
output:
  primary: "assets/video/final/andisense-demo-final.mp4"
  variants:
    - name: "executive"
      scenes: ["scene-01-intro", "scene-02-dashboard", "scene-07-outro"]
      output: "assets/video/final/andisense-executive-demo.mp4"
    - name: "no-audio"
      include_audio: false
      output: "assets/video/final/andisense-demo-no-audio.mp4"
```

---

## Zoom Effects System

### Purpose
Zoom effects draw viewer attention to specific UI elements, making demos more engaging and professional.

### Zoom Configuration Options

```yaml
zoom:
  enabled: true
  mode: "element"              # element | coordinates | auto
  
  # Mode: element - zoom to a specific DOM element
  target: ".metrics-panel"
  padding: 20                  # pixels around element
  
  # Mode: coordinates - zoom to specific screen position
  center: [0.7, 0.3]           # normalized (0-1)
  
  # Mode: auto - AI detects important elements
  auto_detect: true
  prefer_interactive: true     # Prefer buttons, inputs
  
  # Animation
  factor: 1.4                  # 1.4 = 40% zoom
  duration: 3                  # seconds to zoom in
  hold: 2                      # seconds to stay zoomed
  ease: "ease-in-out"          # ease | ease-in | ease-out | linear
  
  # Zoom out
  zoom_out: true               # Whether to zoom back out
  zoom_out_duration: 2
```

### Auto-Zoom Detection

```typescript
async function detectZoomTargets(page: Page): Promise<ZoomTarget[]> {
  // Find interactive elements that deserve attention
  const targets: ZoomTarget[] = [];
  
  // Primary buttons
  const primaryButtons = await page.locator('button.primary, [data-action]').all();
  for (const btn of primaryButtons) {
    targets.push({
      element: btn,
      importance: 'high',
      reason: 'Primary action button'
    });
  }
  
  // Data visualizations
  const charts = await page.locator('.chart, .graph, canvas').all();
  for (const chart of charts) {
    targets.push({
      element: chart,
      importance: 'medium',
      reason: 'Data visualization'
    });
  }
  
  // Recently changed elements (for feature demos)
  const newBadges = await page.locator('[data-new], .badge-new').all();
  for (const badge of newBadges) {
    targets.push({
      element: badge,
      importance: 'high',
      reason: 'New feature indicator'
    });
  }
  
  return targets.sort((a, b) => 
    (b.importance === 'high' ? 1 : 0) - (a.importance === 'high' ? 1 : 0)
  );
}
```

---

## Animation & Transition System

### Available Transitions

| Transition | Description | Best For |
|------------|-------------|----------|
| `crossfade` | Smooth opacity blend | Default, professional |
| `slide-left` | Slide in from right | Sequential workflows |
| `slide-up` | Slide up from bottom | Revealing details |
| `zoom-in` | Zoom into next scene | Drilling down |
| `zoom-out` | Zoom out from detail | Big picture views |
| `fade-black` | Fade through black | Section changes |
| `cut` | Instant transition | Fast-paced demos |

### Transition Configuration

```yaml
# In frame.yaml
transition:
  in: "slide-left"
  in_duration: 0.7
  in_ease: "ease-out"
  
  out: "crossfade"
  out_duration: 0.5
  out_ease: "ease-in"
```

### Purposeful Animation Guidelines

```markdown
## When to Use Animations

✅ DO use animations for:
- Transitions between major sections
- Drawing attention to key features
- Showing cause-and-effect relationships
- Making the demo feel polished

❌ DON'T use animations for:
- Every single scene change (gets tiresome)
- Purely decorative effects
- Distracting from the content
- Extending demo unnecessarily

## Animation Value Assessment

Before adding an animation, ask:
1. Does this help the viewer understand something?
2. Does this guide attention appropriately?
3. Would the demo be worse without it?

If you can't answer "yes" to at least one, skip the animation.
```

---

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup

Run environment validation to check Playwright and app availability:
```bash
# Check if Playwright is installed
npx playwright --version

# Check if app is accessible (adjust URL as needed)
curl -s -o /dev/null -w "%{http_code}" http://localhost:5173/
```

Parse results for PLAYWRIGHT_INSTALLED, APP_RUNNING. Halt if either check fails.

### 2. Load Configuration

- The constitution rules are already loaded in context above.
- Load existing `playwright.config.ts` for base URL and browser settings
- Check for existing E2E tests that can be leveraged

### 3. Parse Input

Extract from $ARGUMENTS:
- **Product/App Name**: Name of the application to demo
- **Target Audience**: technical | business | executive
- **Duration Target**: 1-5 minutes (default: 3 minutes)
- **Key Features**: List of features to showcase
- **Existing Tests**: Path to E2E tests to leverage (optional)
- **Output Directory**: Where to save demo assets (default: `demo/`)
- **Voice Preference**: male | female | specific voice name (default: male)
- **Include Audio**: voiceover | music | both | none (default: voiceover)
- **Subtitle Style**: burned-in | separate-file | both (default: both)

Request clarification if product name or features are not specified.

### 3.1 Pre-Capture Data Discovery (CRITICAL)

**Before planning scenes, discover what data exists in the application:**

```typescript
// Discover available data to ensure demos show real content
async function discoverApplicationData(page: Page): Promise<AppDataContext> {
  const context: AppDataContext = {
    projects: [],
    hasRequirements: false,
    hasProcessFlows: false,
    hasDocuments: false,
    recommendedProjectId: null,
  };
  
  // 1. Find projects with data
  try {
    const response = await page.request.get('/api/v1/projects');
    if (response.ok()) {
      const projects = await response.json();
      context.projects = projects;
      
      // Find project with most data for demo
      for (const project of projects) {
        const reqCount = await getRequirementCount(page, project.id);
        const flowCount = await getFlowCount(page, project.id);
        
        if (reqCount > 0 || flowCount > 0) {
          context.recommendedProjectId = project.id;
          context.hasRequirements = reqCount > 0;
          context.hasProcessFlows = flowCount > 0;
          break;
        }
      }
    }
  } catch (e) {
    console.log('API discovery failed, will use navigation');
  }
  
  // 2. If no API, navigate and discover
  if (!context.recommendedProjectId) {
    await page.goto('/projects');
    await page.waitForLoadState('networkidle');
    
    const projectCards = page.locator('[data-testid="project-card"], .project-card, a[href*="/projects/"]');
    if (await projectCards.count() > 0) {
      const href = await projectCards.first().getAttribute('href');
      const match = href?.match(/projects\/([^/]+)/);
      context.recommendedProjectId = match?.[1] || null;
    }
  }
  
  return context;
}
```

**Use discovered data to plan scenes:**

- If `recommendedProjectId` exists → Use it for all data-dependent pages
- If no projects → Warn user and suggest seeding data first
- If project has requirements but no flows → Adjust scenes accordingly
- Always verify data exists BEFORE adding scene to plan

### 4. Analyze Application Structure & Auto-Discover Features

Scan for ALL pages, routes, and features in the application:
```bash
# Find existing E2E tests
find . -path ./node_modules -prune -o -name "*.spec.ts" -print | head -20

# Find page components (React)
find . -path ./node_modules -prune -o -name "*Page.tsx" -print | head -30

# Find route definitions (React Router, Next.js, etc.)
grep -r "path:" --include="*.tsx" --include="*.ts" src/ | head -30
grep -r "<Route" --include="*.tsx" src/ | head -30

# Find navigation/sidebar items
grep -r "href=" --include="*.tsx" src/components/ | head -20
```

**Comprehensive Feature Discovery:**

```typescript
// Discover ALL features in the application
interface DiscoveredFeature {
  name: string;
  route: string;
  category: 'dashboard' | 'crud' | 'workflow' | 'report' | 'settings' | 'integration';
  priority: 'high' | 'medium' | 'low';
  requiresData: boolean;
  requiresAuth: boolean;
  audienceRelevance: {
    executive: number;    // 0-10 relevance score
    technical: number;
    business: number;
  };
}

async function discoverAllFeatures(page: Page): Promise<DiscoveredFeature[]> {
  const features: DiscoveredFeature[] = [];
  
  // 1. Scan navigation/sidebar for all links
  const navLinks = await page.locator('nav a, aside a, [role="navigation"] a').all();
  for (const link of navLinks) {
    const href = await link.getAttribute('href');
    const text = await link.textContent();
    if (href && !href.startsWith('http') && !href.includes('logout')) {
      features.push(categorizeFeature(href, text || ''));
    }
  }
  
  // 2. Check for common enterprise app patterns
  const commonRoutes = [
    { route: '/dashboard', name: 'Dashboard', category: 'dashboard', priority: 'high' },
    { route: '/projects', name: 'Projects', category: 'crud', priority: 'high' },
    { route: '/requirements', name: 'Requirements', category: 'crud', priority: 'high' },
    { route: '/process-flows', name: 'Process Flows', category: 'workflow', priority: 'high' },
    { route: '/documents', name: 'Documents', category: 'crud', priority: 'medium' },
    { route: '/reports', name: 'Reports', category: 'report', priority: 'medium' },
    { route: '/matrices', name: 'Matrices', category: 'report', priority: 'medium' },
    { route: '/settings', name: 'Settings', category: 'settings', priority: 'low' },
    { route: '/integrations', name: 'Integrations', category: 'integration', priority: 'medium' },
    { route: '/search', name: 'Search', category: 'workflow', priority: 'low' },
    { route: '/notifications', name: 'Notifications', category: 'workflow', priority: 'low' },
  ];
  
  for (const common of commonRoutes) {
    // Check if route exists by trying to navigate
    const exists = await checkRouteExists(page, common.route);
    if (exists && !features.find(f => f.route === common.route)) {
      features.push({
        ...common,
        requiresData: ['requirements', 'process-flows', 'documents'].some(r => common.route.includes(r)),
        requiresAuth: true,
        audienceRelevance: getAudienceRelevance(common.category),
      });
    }
  }
  
  // 3. Sort by priority and logical flow
  return sortFeaturesForDemo(features);
}

function getAudienceRelevance(category: string): { executive: number; technical: number; business: number } {
  const relevance = {
    dashboard: { executive: 10, technical: 5, business: 7 },
    crud: { executive: 3, technical: 8, business: 9 },
    workflow: { executive: 5, technical: 9, business: 10 },
    report: { executive: 9, technical: 6, business: 10 },
    settings: { executive: 1, technical: 10, business: 3 },
    integration: { executive: 7, technical: 10, business: 6 },
  };
  return relevance[category] || { executive: 5, technical: 5, business: 5 };
}

function sortFeaturesForDemo(features: DiscoveredFeature[]): DiscoveredFeature[] {
  // Logical demo order: Dashboard → Core features → Advanced → Settings
  const order = ['dashboard', 'crud', 'workflow', 'report', 'integration', 'settings'];
  return features.sort((a, b) => {
    const aOrder = order.indexOf(a.category);
    const bOrder = order.indexOf(b.category);
    if (aOrder !== bOrder) return aOrder - bOrder;
    // Within category, sort by priority
    const priorityOrder = { high: 0, medium: 1, low: 2 };
    return priorityOrder[a.priority] - priorityOrder[b.priority];
  });
}
```

**Filter Features by Audience:**

```typescript
function filterFeaturesForAudience(
  features: DiscoveredFeature[], 
  audience: 'executive' | 'technical' | 'business' | 'general',
  maxScenes: number
): DiscoveredFeature[] {
  
  if (audience === 'general') {
    // Show all high-priority features
    return features.filter(f => f.priority === 'high').slice(0, maxScenes);
  }
  
  // Score and sort by audience relevance
  const scored = features.map(f => ({
    ...f,
    score: f.audienceRelevance[audience] || 5,
  }));
  
  scored.sort((a, b) => b.score - a.score);
  
  // Apply audience-specific limits
  const limits = {
    executive: 4,   // Max 4 scenes for executives
    technical: 10,  // Up to 10 scenes for technical
    business: 6,    // 6 scenes for business analysts
  };
  
  return scored.slice(0, Math.min(limits[audience] || maxScenes, maxScenes));
}
```

Identify:
- **All available pages/routes** in the application
- **Feature categories** (dashboard, CRUD, workflow, report, settings)
- **Audience relevance scores** for each feature
- Existing test flows that can become demo scenes
- UI components suitable for highlighting
- Authentication requirements
- **Routes that require parameters** (e.g., `/projects/:id`, `/requirements?project_id=X`)
- **Data dependencies** (pages that need pre-existing data to display content)

### 4.1 Intelligent Route Analysis (CRITICAL)

**Before generating any demo scene, analyze each target URL:**

1. **Detect Parameterized Routes**:
   - Routes with `:id`, `:projectId`, etc. require valid IDs
   - Query parameters like `?project_id=X` need valid values
   - Nested routes like `/projects/:id/requirements` need parent data

2. **Identify Data-Dependent Pages**:
   - List/grid pages that show "No data" when empty
   - Detail pages that 404 without valid ID
   - Dashboard pages that need projects/data to show metrics

3. **Pre-flight Data Check**:
   ```typescript
   // Before capturing, verify data exists
   async function verifyPageHasData(page: Page, url: string): Promise<boolean> {
     await page.goto(url);
     await page.waitForLoadState('networkidle');
     
     // Check for common empty state indicators
     const emptyIndicators = [
       'text="No data"',
       'text="No results"', 
       'text="No items"',
       'text="Nothing to show"',
       'text="Get started"',
       'text="Create your first"',
       '[data-testid="empty-state"]',
       '.empty-state',
     ];
     
     for (const indicator of emptyIndicators) {
       if (await page.locator(indicator).count() > 0) {
         return false; // Page has no data
       }
     }
     
     // Check for actual content
     const contentIndicators = [
       'table tbody tr',
       '[data-testid="card"]',
       '.grid > div',
       'ul li',
     ];
     
     for (const indicator of contentIndicators) {
       if (await page.locator(indicator).count() > 0) {
         return true; // Page has data
       }
     }
     
     return false; // Uncertain, treat as no data
   }
   ```

4. **Auto-Discovery of Valid Data**:
   ```typescript
   // Find a valid project ID by checking the API or navigating
   async function findValidProjectId(page: Page): Promise<string | null> {
     // Try API endpoint
     const response = await page.request.get('/api/v1/projects');
     if (response.ok()) {
       const projects = await response.json();
       if (projects.length > 0) {
         return projects[0].id;
       }
     }
     
     // Try navigating to projects list and extracting
     await page.goto('/projects');
     await page.waitForLoadState('networkidle');
     const firstProjectLink = page.locator('a[href*="/projects/"]').first();
     if (await firstProjectLink.count() > 0) {
       const href = await firstProjectLink.getAttribute('href');
       const match = href?.match(/\/projects\/([^/]+)/);
       return match ? match[1] : null;
     }
     
     return null;
   }
   ```

5. **Route Correction Strategy**:
   - If `/requirements` shows empty → Try `/projects/:validId/requirements`
   - If `/process-flows` shows empty → Try with `?project_id=:validId`
   - If detail page 404s → Find valid ID from list page first
   - If dashboard empty → Navigate to a project with data first

### 4.5 Analyze Requirements and Provide Recommendations (COLLABORATIVE DESIGN)

**Purpose:** Collaborate with user to design better demo upfront, preventing common quality issues.

#### Step 1: Feature Discovery Analysis

Scan application to discover all pages:
```bash
# Find all page components
ls frontend/src/pages/*.tsx
cat src/router.ts | grep "path:"
```

Present findings to user:
```
═══════════════════════════════════════════════════════════════
  🔍 FEATURE DISCOVERY ANALYSIS
═══════════════════════════════════════════════════════════════

Found 12 pages in application:
✓ /dashboard - Dashboard overview
✓ /projects - Project list
✓ /projects/:id - Project detail
✓ /requirements - Requirements list
✓ /requirements/:id - Requirement detail
✓ /flows - Process flows
✓ /flows/:id - Flow editor
✓ /users - User management
✓ /settings - Settings
✓ /reports - Reports
✓ /search - Search
✓ /help - Help documentation

═══════════════════════════════════════════════════════════════
  📊 RECOMMENDED SCENES FOR EXECUTIVE DEMO (2 min, 6-8 scenes)
═══════════════════════════════════════════════════════════════

Priority 1 (Must Include):
1. /dashboard (overview) - 15s
2. /projects (show list) - 20s
3. /projects/:id (show detail) - 20s

Priority 2 (Strongly Recommended):
4. /requirements (traceability) - 20s
5. /flows (process visualization) - 20s
6. /reports (metrics) - 15s

Priority 3 (Optional):
7. /search (discovery) - 10s
8. /settings (configuration) - 10s

Total Duration: 2:10 (within target)
Unique URLs: 8 (no duplicates ✓)
Feature Coverage: 67% (8/12 pages)

═══════════════════════════════════════════════════════════════
  ❓ PROCEED WITH THIS PLAN?
═══════════════════════════════════════════════════════════════

Options:
[Y] Yes, proceed with recommended scenes
[M] Modify - I want to change scenes
[A] Auto - Use your best judgment

Your choice:
```

**Wait for user input before proceeding.**

#### Step 2: Identify Logical Pitfalls

Review demo plan for common issues:
```
═══════════════════════════════════════════════════════════════
  ⚠️  DEMO PLAN ANALYSIS - POTENTIAL ISSUES
═══════════════════════════════════════════════════════════════

Checking for common quality issues...

❌ CRITICAL ISSUE #1: Duplicate URLs
   Scene 2: /dashboard
   Scene 5: /dashboard
   
   Why: Showing same page twice wastes screen time
   Impact: Demo looks repetitive and unprofessional
   Fix: Replace Scene 5 with /flows or /reports
   
⚠️  WARNING #2: Narration-Visual Misalignment
   Scene 3: URL is /requirements (list page)
   Narration: "Here you can edit requirement details..."
   
   Why: List page doesn't show editor
   Impact: Narration doesn't match what's on screen
   Fix: Change URL to /requirements/:id (detail page)
   
⚠️  WARNING #3: Missing Data Verification
   Scene 4: /projects/:id requires valid project ID
   
   Why: Page will 404 if project doesn't exist
   Impact: Demo capture will fail
   Fix: Auto-discover valid project ID from /projects list
   
✓ PASS: No AI features detected (no wait time issues)
✓ PASS: All scenes have unique URLs
✓ PASS: Coverage score 67% (good for executive demo)

═══════════════════════════════════════════════════════════════
  🔧 RECOMMENDED FIXES
═══════════════════════════════════════════════════════════════

1. Remove duplicate /dashboard from Scene 5
2. Change Scene 3 URL from /requirements to /requirements/:id
3. Auto-discover valid project ID for Scene 4

Apply these fixes automatically? [Y/n]
```

#### Step 3: Recommend Scene Structure

Based on audience and app features:
```
═══════════════════════════════════════════════════════════════
  🎬 RECOMMENDED SCENE STRUCTURE
═══════════════════════════════════════════════════════════════

Audience: Executive
Duration: 2 minutes
Recommended Structure:

Scene 1 (15s): Dashboard overview
  URL: /dashboard
  Focus: High-level metrics, project count
  Narration: "Welcome to AndiSense..."

Scene 2 (20s): Project list with data
  URL: /projects
  Focus: Active projects, status indicators
  Narration: "The system tracks multiple projects..."

Scene 3 (20s): Project detail page
  URL: /projects/{auto-discovered-id}
  Focus: Requirements count, process flows
  Narration: "Each project contains requirements..."

Scene 4 (20s): Requirements traceability
  URL: /requirements?project_id={id}
  Focus: Traceability matrix, status
  Narration: "Requirements are fully traceable..."

Scene 5 (20s): Process flow visualization
  URL: /flows/{auto-discovered-id}
  Focus: draw.io integration, visual workflow
  Narration: "Process flows are visualized..."

Scene 6 (15s): Reports and metrics
  URL: /reports
  Focus: Dashboards, analytics
  Narration: "Generate comprehensive reports..."

Scene 7 (10s): Closing summary
  URL: /dashboard (return to home)
  Focus: Call to action
  Narration: "Contact your team lead to get started."

═══════════════════════════════════════════════════════════════
  ✅ QUALITY CHECKS
═══════════════════════════════════════════════════════════════

✓ Total Duration: 2:00 minutes (within target)
✓ Unique URLs: 7 (no duplicates)
✓ Feature Coverage: 58% (7/12 pages - appropriate for exec demo)
✓ Narration-Visual Alignment: All scenes validated
✓ Data Dependencies: Auto-discovery configured
✓ Logical Flow: Dashboard → Features → Reports → Close

═══════════════════════════════════════════════════════════════

Approve this structure? [Y/n/modify]
```

#### Step 4: Data Verification

Before generating capture spec, verify data exists:
```typescript
// Auto-discover valid data for parameterized routes
async function verifyDataAvailability(page: Page): Promise<DataContext> {
  const context: DataContext = {
    hasProjects: false,
    validProjectId: null,
    hasRequirements: false,
    hasFlows: false,
    warnings: [],
  };
  
  // Check if projects exist
  await page.goto('/projects');
  await page.waitForLoadState('networkidle');
  
  const projectCards = page.locator('[data-testid="project-card"], .project-card');
  const projectCount = await projectCards.count();
  
  if (projectCount === 0) {
    context.warnings.push('⚠️  No projects found - demo will show empty states');
    context.warnings.push('   Recommendation: Seed data before capturing demo');
    return context;
  }
  
  context.hasProjects = true;
  
  // Extract valid project ID
  const firstProjectLink = projectCards.first().locator('a[href*="/projects/"]');
  const href = await firstProjectLink.getAttribute('href');
  const match = href?.match(/\/projects\/([^/]+)/);
  context.validProjectId = match ? match[1] : null;
  
  // Check if project has requirements
  if (context.validProjectId) {
    await page.goto(`/projects/${context.validProjectId}`);
    const reqCount = await page.locator('[data-testid="requirement-count"]').textContent();
    context.hasRequirements = parseInt(reqCount || '0') > 0;
    
    const flowCount = await page.locator('[data-testid="flow-count"]').textContent();
    context.hasFlows = parseInt(flowCount || '0') > 0;
  }
  
  return context;
}
```

Present data verification results:
```
═══════════════════════════════════════════════════════════════
  📊 DATA VERIFICATION RESULTS
═══════════════════════════════════════════════════════════════

✓ Projects: 5 found
✓ Valid Project ID: proj-abc123
✓ Requirements: 12 found in proj-abc123
✓ Process Flows: 3 found in proj-abc123

All data dependencies satisfied. Demo will show real content.

═══════════════════════════════════════════════════════════════
```

**Benefits of Collaborative Design:**
- ✅ Catches duplicate URLs before capture (saves 30+ min rework)
- ✅ Validates feature coverage upfront
- ✅ Ensures data exists (no empty states)
- ✅ Prevents narration-visual misalignment
- ✅ Investment: 10-15 min upfront saves hours of rework

### 5. Generate Demo Plan

Create a YAML demo manifest based on features and audience:

```yaml
# demo/demo-manifest.yaml
demo:
  title: "[PRODUCT_NAME] Demo"
  version: "1.0.0"
  created: "[DATE]"
  duration_target: "[DURATION]"
  target_audience: "[AUDIENCE]"
  
branding:
  highlight_color: "#009FDB"  # AT&T Blue
  annotation_style: "rounded"
  font: "ATT Aleck Sans"

scenes:
  - id: "scene-01"
    title: "[SCENE_TITLE]"
    type: "screenshot"  # or "video"
    duration: "0:15"
    url: "[PAGE_URL]"
    wait_for: "networkidle"
    
    # For screenshots
    capture:
      selector: "main"  # or specific element
      full_page: false
      
    # Optional highlights
    highlights:
      - selector: "[ELEMENT_SELECTOR]"
        annotation: "[ANNOTATION_TEXT]"
        style: "glow"  # glow | border | arrow
    
    # Voiceover script for this scene
    script: |
      [VOICEOVER_TEXT]
    
    # Timing cues
    timing:
      start: "0:00"
      end: "0:15"
      pause_after: 2  # seconds

  - id: "scene-02"
    title: "[SCENE_TITLE]"
    type: "video"
    duration: "0:30"
    url: "[PAGE_URL]"
    
    # For video captures
    actions:
      - type: "click"
        selector: "[BUTTON_SELECTOR]"
        delay_before: 1000
      - type: "fill"
        selector: "[INPUT_SELECTOR]"
        value: "[DEMO_VALUE]"
        typing_delay: 50  # ms per character
      - type: "click"
        selector: "[SUBMIT_SELECTOR]"
      - type: "wait"
        for: "url"
        value: "**/success/**"
    
    script: |
      [VOICEOVER_TEXT]
    
    timing:
      start: "0:15"
      end: "0:45"

output:
  formats:
    - "screenshots"  # PNG files
    - "video"        # WebM clips
    - "script"       # Markdown script
  directory: "demo/"
```

### 6. Generate Playwright Capture Script

Create the Playwright test file that captures all scenes with **burned-in subtitles** (no overlay annotations):

```typescript
// demo/captures/demo-video-subtitles.spec.ts
import { test, Page } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

// ES Module compatible paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Output directories
const DEMO_DIR = path.join(__dirname, '..', '..', '..', 'demo');
const ASSETS_DIR = path.join(DEMO_DIR, 'assets');
const SCREENSHOTS_DIR = path.join(ASSETS_DIR, 'screenshots');
const VIDEOS_DIR = path.join(ASSETS_DIR, 'videos');
const SUBTITLES_DIR = path.join(ASSETS_DIR, 'subtitles');

// Subtitle data - synced with script timing
// IMPORTANT: Update these to match your demo script
const SUBTITLES = [
  { start: 0, end: 5, text: "[SUBTITLE_1]" },
  { start: 5, end: 10, text: "[SUBTITLE_2]" },
  // Add more subtitles matching your script...
];

// Ensure output directories exist
test.beforeAll(async () => {
  [ASSETS_DIR, SCREENSHOTS_DIR, VIDEOS_DIR, SUBTITLES_DIR].forEach(dir => {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  });
  
  // Generate subtitle files
  generateSubtitleFiles();
});

// Generate SRT and VTT subtitle files
function generateSubtitleFiles() {
  // SRT format
  let srt = '';
  SUBTITLES.forEach((sub, i) => {
    srt += `${i + 1}\n${formatSRTTime(sub.start)} --> ${formatSRTTime(sub.end)}\n${sub.text}\n\n`;
  });
  fs.writeFileSync(path.join(SUBTITLES_DIR, 'demo-subtitles.srt'), srt);
  
  // VTT format (web-compatible)
  let vtt = 'WEBVTT\n\n';
  SUBTITLES.forEach((sub, i) => {
    vtt += `${i + 1}\n${formatVTTTime(sub.start)} --> ${formatVTTTime(sub.end)}\n${sub.text}\n\n`;
  });
  fs.writeFileSync(path.join(SUBTITLES_DIR, 'demo-subtitles.vtt'), vtt);
}

function formatSRTTime(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  return `${pad(h)}:${pad(m)}:${pad(s)},000`;
}

function formatVTTTime(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  return `${pad(h)}:${pad(m)}:${pad(s)}.000`;
}

function pad(num: number): string {
  return num.toString().padStart(2, '0');
}

// Helper: Show subtitle at bottom of screen (burned into video)
// NOTE: No overlay annotations - clean UI with subtitles only
async function showSubtitle(page: Page, text: string) {
  await page.evaluate((t: string) => {
    const existing = document.getElementById('demo-subtitle');
    if (existing) existing.remove();
    
    if (!t) return;
    
    const subtitle = document.createElement('div');
    subtitle.id = 'demo-subtitle';
    subtitle.textContent = t;
    subtitle.style.cssText = `
      position: fixed;
      bottom: 60px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(0, 0, 0, 0.75);
      color: white;
      padding: 12px 24px;
      border-radius: 8px;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      font-size: 22px;
      font-weight: 500;
      max-width: 80%;
      text-align: center;
      z-index: 10000;
      line-height: 1.4;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    `;
    document.body.appendChild(subtitle);
  }, text);
}

// Helper: Clear subtitle
async function clearSubtitle(page: Page) {
  await page.evaluate(() => {
    const subtitle = document.getElementById('demo-subtitle');
    if (subtitle) subtitle.remove();
  });
}

// Helper: Display subtitle for duration
async function displaySubtitle(page: Page, text: string, durationMs: number) {
  await showSubtitle(page, text);
  await page.waitForTimeout(durationMs);
}

// Helper: Verify page has data (not empty state)
async function verifyPageHasData(page: Page): Promise<boolean> {
  const emptyIndicators = [
    'text="No data"', 'text="No results"', 'text="No items"',
    'text="Nothing to show"', 'text="Get started"',
    'text="Create your first"', '[data-testid="empty-state"]',
  ];
  
  for (const indicator of emptyIndicators) {
    if (await page.locator(indicator).count() > 0) {
      return false;
    }
  }
  return true;
}

// Helper: Find valid project ID for data-dependent pages
async function findValidProjectId(page: Page): Promise<string | null> {
  // Try API first
  try {
    const response = await page.request.get('/api/v1/projects');
    if (response.ok()) {
      const projects = await response.json();
      if (projects.length > 0) return projects[0].id;
    }
  } catch (e) { /* API not available */ }
  
  // Fall back to navigation
  await page.goto('/projects');
  await page.waitForLoadState('networkidle');
  const link = page.locator('a[href*="/projects/"]').first();
  if (await link.count() > 0) {
    const href = await link.getAttribute('href');
    const match = href?.match(/projects\/([^/]+)/);
    return match?.[1] || null;
  }
  return null;
}

// Configure for video recording - SINGLE continuous test for smooth video
test.use({
  viewport: { width: 1920, height: 1080 },
  video: { mode: 'on', size: { width: 1920, height: 1080 } },
});

test.describe('[PRODUCT_NAME] Demo - Clean Video with Subtitles', () => {
  
  test.setTimeout(120000); // 2 minutes for full demo

  test('Complete Demo Recording', async ({ page }) => {
    // ============================================
    // SETUP: Discover valid project for data pages
    // ============================================
    let projectId: string | null = null;
    
    // Login first
    await page.goto('/login');
    await page.waitForLoadState('domcontentloaded');
    await page.locator('input[type="text"], input[type="email"]').first().fill('[LOGIN_EMAIL]');
    await page.locator('input[type="password"]').fill('[LOGIN_PASSWORD]');
    await page.locator('button:has-text("Sign In")').click();
    await page.waitForTimeout(2000);
    
    // Discover project with data
    projectId = await findValidProjectId(page);
    if (!projectId) {
      console.warn('⚠️ No projects found - some scenes may show empty states');
    } else {
      console.log(`✓ Using project: ${projectId}`);
    }

    // ============================================
    // SCENE 1: [SCENE_TITLE]
    // ============================================
    console.log('📹 Scene 1: [SCENE_TITLE]');
    await page.goto('[PAGE_URL]');
    await page.waitForLoadState('networkidle');
    
    // Verify data exists, correct URL if needed
    if (!await verifyPageHasData(page) && projectId) {
      console.log('  → Empty state detected, adding project context...');
      await page.goto(`[PAGE_URL]?project_id=${projectId}`);
      await page.waitForLoadState('networkidle');
    }
    
    await page.waitForTimeout(500);
    await displaySubtitle(page, SUBTITLES[0].text, 5000);
    // Add more subtitles for this scene...
    await clearSubtitle(page);

    // ============================================
    // SCENE 2: [SCENE_TITLE]
    // ============================================
    console.log('📹 Scene 2: [SCENE_TITLE]');
    // Use project context for data-dependent pages
    const scene2Url = projectId ? `[PAGE_URL]?project_id=${projectId}` : '[PAGE_URL]';
    await page.goto(scene2Url);
    await page.waitForLoadState('networkidle');
    
    await page.waitForTimeout(500);
    await displaySubtitle(page, SUBTITLES[1].text, 5000);
    await clearSubtitle(page);

    // Add more scenes following the same pattern...

    // ============================================
    // SAVE VIDEO
    // ============================================
    console.log('📹 Demo recording complete!');
    
    const video = page.video();
    if (video) {
      const videoPath = await video.path();
      await page.close();
      
      const destPath = path.join(VIDEOS_DIR, '[PRODUCT]-demo-subtitles.webm');
      if (fs.existsSync(videoPath)) {
        fs.copyFileSync(videoPath, destPath);
        console.log(`✅ Video saved to: ${destPath}`);
      }
    }
  });
});
```

**Key Design Decisions (baked into archetype):**

1. **No overlay annotations** - Clean UI capture, information conveyed via subtitles
2. **Burned-in subtitles** - Professional look, always visible
3. **Single continuous test** - Smooth video without cuts between scenes
4. **Auto project discovery** - Finds valid data before capturing
5. **Empty state detection** - Corrects URLs automatically
6. **Subtitle files generated** - SRT + VTT for flexibility

### 7. Generate Markdown Script

Create the voiceover script with timing cues:

```markdown
# [PRODUCT_NAME] Demo Script

**Version:** 1.0.0  
**Duration:** [DURATION]  
**Audience:** [AUDIENCE]  
**Last Updated:** [DATE]

---

## Overview

This demo showcases [PRODUCT_NAME]'s key features:
[LIST_OF_FEATURES]

**Total Runtime:** [DURATION]  
**Scenes:** [SCENE_COUNT]

---

## Scene 1: [SCENE_TITLE] (0:00 - 0:15)

**Visual:** [SCREENSHOT/VIDEO_DESCRIPTION]

**Asset:** `assets/screenshots/scene-01-[SCENE_NAME].png`

### Script

> [VOICEOVER_TEXT]

### Key Points
- [KEY_POINT_1]
- [KEY_POINT_2]

### Timing Notes
- **0:00** - Scene starts
- **0:05** - Highlight [ELEMENT]
- **0:12** - Begin transition
- **0:15** - Scene ends

---

## Scene 2: [SCENE_TITLE] (0:15 - 0:45)

**Visual:** Video of [ACTION_DESCRIPTION]

**Asset:** `assets/videos/scene-02-[SCENE_NAME].webm`

### Script

> [VOICEOVER_TEXT]

### Actions Shown
1. [ACTION_1] (0:18)
2. [ACTION_2] (0:25)
3. [ACTION_3] (0:35)
4. [RESULT] (0:42)

### Key Points
- [KEY_POINT_1]
- [KEY_POINT_2]

---

## Closing (X:XX - X:XX)

**Visual:** [CLOSING_VISUAL]

### Script

> [CLOSING_VOICEOVER]

### Call to Action
- [CTA_1]
- [CTA_2]

---

## Production Notes

### Recording Tips
- Speak at moderate pace (~150 words/minute)
- Pause briefly between scenes
- Emphasize key feature names
- Keep energy consistent

### Technical Requirements
- Resolution: 1920x1080
- Frame rate: 30fps (video)
- Audio: Clear, no background noise

### Assets Checklist
- [ ] Scene 1 screenshot captured
- [ ] Scene 2 video captured
- [ ] All highlights visible
- [ ] No sensitive data shown
- [ ] AT&T branding consistent
```

### 8. Execute Captures

Run Playwright to capture all demo scenes:
```bash
# Run demo captures
npx playwright test demo/captures/demo-capture.spec.ts --project=chromium --reporter=list

# Check output
ls -la demo/assets/screenshots/
ls -la demo/assets/videos/
```

### 9. Validate Output (CRITICAL - Self-Correction Loop)

**Automated validation with self-correction:**

```typescript
// demo/captures/validate-captures.ts
interface ValidationResult {
  scene: string;
  passed: boolean;
  issues: string[];
  suggestions: string[];
}

async function validateCaptures(): Promise<ValidationResult[]> {
  const results: ValidationResult[] = [];
  const screenshotDir = 'demo/assets/screenshots';
  const files = fs.readdirSync(screenshotDir);
  
  for (const file of files) {
    const result: ValidationResult = {
      scene: file,
      passed: true,
      issues: [],
      suggestions: [],
    };
    
    const filePath = path.join(screenshotDir, file);
    const stats = fs.statSync(filePath);
    
    // Check 1: File size (empty or too small = problem)
    if (stats.size < 10000) { // Less than 10KB
      result.passed = false;
      result.issues.push('Screenshot too small - likely blank or error page');
      result.suggestions.push('Check if page loaded correctly, verify selectors');
    }
    
    // Check 2: Analyze image for empty states (requires sharp or similar)
    // This is a simplified check - in practice, use image analysis
    
    // Check 3: Look for error indicators in filename
    if (file.includes('error') || file.includes('404')) {
      result.passed = false;
      result.issues.push('Error page captured instead of content');
      result.suggestions.push('Verify URL and authentication');
    }
    
    results.push(result);
  }
  
  return results;
}
```

**Visual Content Validation:**

1. **Empty State Detection**:
   - Analyze screenshot for common empty patterns
   - Check for "No data", "No results" text in image (OCR or DOM check before capture)
   - Verify actual content is visible, not just chrome/navigation

2. **Error Page Detection**:
   - Check for 404, 500 error indicators
   - Detect login redirects (captured login page instead of target)
   - Identify "Access Denied" or permission errors

3. **Content Quality Checks**:
   - Verify highlights are visible (color detection)
   - Check that main content area has data
   - Ensure no loading spinners are captured

**Self-Correction Protocol:**

When validation fails, automatically attempt corrections:

```typescript
async function selfCorrectCapture(
  page: Page, 
  scene: SceneConfig, 
  validationResult: ValidationResult
): Promise<boolean> {
  
  console.log(`🔄 Self-correcting scene: ${scene.id}`);
  
  // Issue: Empty page (no data)
  if (validationResult.issues.includes('empty_state')) {
    console.log('  → Detected empty state, finding data...');
    
    // Strategy 1: Add project context
    const projectId = await findValidProjectId(page);
    if (projectId) {
      const newUrl = addProjectContext(scene.url, projectId);
      console.log(`  → Trying with project context: ${newUrl}`);
      scene.url = newUrl;
      return await recaptureScene(page, scene);
    }
    
    // Strategy 2: Navigate from parent page
    const parentUrl = getParentRoute(scene.url);
    if (parentUrl) {
      console.log(`  → Navigating from parent: ${parentUrl}`);
      await page.goto(parentUrl);
      // Click into first item to get to detail with data
      const firstItem = page.locator('a, [role="button"]').first();
      if (await firstItem.count() > 0) {
        await firstItem.click();
        await page.waitForLoadState('networkidle');
        return await captureCurrentPage(page, scene);
      }
    }
  }
  
  // Issue: Login redirect
  if (validationResult.issues.includes('login_redirect')) {
    console.log('  → Detected login redirect, re-authenticating...');
    await performLogin(page);
    return await recaptureScene(page, scene);
  }
  
  // Issue: 404 error
  if (validationResult.issues.includes('not_found')) {
    console.log('  → Page not found, discovering valid URL...');
    const validUrl = await discoverValidUrl(page, scene.url);
    if (validUrl) {
      scene.url = validUrl;
      return await recaptureScene(page, scene);
    }
  }
  
  return false; // Could not self-correct
}

function addProjectContext(url: string, projectId: string): string {
  // /requirements → /projects/{id}/requirements or /requirements?project_id={id}
  if (url.includes('?')) {
    return `${url}&project_id=${projectId}`;
  }
  
  // Check if route supports nested format
  const nestedRoutes = ['requirements', 'process-flows', 'documents', 'capabilities'];
  for (const route of nestedRoutes) {
    if (url.endsWith(`/${route}`)) {
      return `/projects/${projectId}/${route}`;
    }
  }
  
  return `${url}?project_id=${projectId}`;
}
```

**Validation Report:**

After all captures and corrections, generate a validation report:

```
📋 Capture Validation Report

✅ Passed: 3/4 scenes
⚠️ Corrected: 1 scene (requirements - added project context)
❌ Failed: 0 scenes

Scene Details:
  ✅ scene-01-dashboard: OK (245 KB)
  ✅ scene-02-process-flows: OK (189 KB)
  🔄 scene-03-requirements: CORRECTED
     Issue: Empty state detected
     Fix: Added project_id parameter
     Result: OK (156 KB)
  ✅ scene-04-closing: OK (267 KB)

All scenes validated successfully!
```

**Hard Stops (Cannot Self-Correct):**

- No projects exist in the system → Prompt user to seed data
- Authentication credentials invalid → Prompt for correct credentials
- Application not running → Halt and report
- Critical feature not accessible → Report and suggest alternatives

### 10. Generate Audio (Voiceover + Music)

**Default: Male voice (Microsoft David)** - More professional for corporate demos.

Generate the voiceover script file and Python generator:

```python
# demo/scripts/generate_voiceover.py
"""
Generate voiceover for demo using pyttsx3 (offline TTS).
Run: python demo/scripts/generate_voiceover.py [--voice male|female|<name>]

DEFAULT: Male voice (Microsoft David) - professional corporate tone
"""
import pyttsx3
import argparse
from pathlib import Path

# Full script - update this with your demo script
SCRIPT = """
[VOICEOVER_SCRIPT_TEXT]
"""

def list_available_voices():
    """List all available TTS voices on the system."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print("Available voices:")
    for i, voice in enumerate(voices):
        print(f"  {i}: {voice.name}")
    return voices

def generate_voiceover(voice_preference: str = "male"):
    """
    Generate voiceover with specified voice preference.
    
    Args:
        voice_preference: "male" (default), "female", or specific voice name
    """
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    print(f"Available voices: {len(voices)}")
    
    # Find matching voice - DEFAULT TO MALE (David)
    selected_voice = None
    for voice in voices:
        name_lower = voice.name.lower()
        
        if voice_preference.lower() == "male":
            # Prefer David for male voice
            if 'david' in name_lower:
                selected_voice = voice
                break
            elif 'guy' in name_lower or 'mark' in name_lower:
                selected_voice = voice
        elif voice_preference.lower() == "female":
            # Prefer Jenny/Zira for female voice
            if 'jenny' in name_lower:
                selected_voice = voice
                break
            elif 'zira' in name_lower or 'aria' in name_lower:
                selected_voice = voice
        else:
            # Match by specific name
            if voice_preference.lower() in name_lower:
                selected_voice = voice
                break
    
    if selected_voice:
        engine.setProperty('voice', selected_voice.id)
        print(f"Using voice: {selected_voice.name}")
    else:
        print(f"Using default voice: {voices[0].name if voices else 'unknown'}")
    
    # Configure for clarity - slightly slower for professional tone
    engine.setProperty('rate', 145)  # Default is ~200, slower is clearer
    engine.setProperty('volume', 1.0)
    
    # Setup output paths
    script_dir = Path(__file__).parent.parent
    audio_dir = script_dir / "assets" / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    wav_path = audio_dir / "voiceover.wav"
    
    print("Generating voiceover...")
    engine.save_to_file(SCRIPT.strip(), str(wav_path))
    engine.runAndWait()
    
    print(f"✅ Voiceover saved to: {wav_path}")
    return wav_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate demo voiceover")
    parser.add_argument("--voice", default="male", help="Voice: male, female, or specific name")
    parser.add_argument("--list", action="store_true", help="List available voices")
    args = parser.parse_args()
    
    if args.list:
        list_available_voices()
    else:
        generate_voiceover(args.voice)
```

**Why male voice is default:**
- More common in corporate/enterprise demos
- Microsoft David has clear enunciation
- Consistent across Windows installations
- User can override with `--voice female` or specific name

**For higher quality voices (optional):**

1. **Edge TTS** (Microsoft Neural voices, requires internet):
   ```bash
   pip install edge-tts
   edge-tts --voice "en-US-GuyNeural" --file script.txt --write-media voiceover.mp3
   ```

2. **ElevenLabs** (Premium quality, requires API key):
   ```python
   # Contact team for API access
   ```

3. **Azure Cognitive Services** (AT&T approved):
   ```python
   # Requires AZURE_SPEECH_KEY environment variable
   ```

**Merge Video + Audio:**

```bash
# Merge video with voiceover
ffmpeg -y -i demo/assets/videos/demo-subtitles.webm \
       -i demo/assets/audio/voiceover.mp3 \
       -c:v libx264 -preset fast -crf 23 \
       -c:a aac -b:a 128k \
       -map 0:v:0 -map 1:a:0 -shortest \
       demo/assets/videos/demo-with-voiceover.mp4

# Add background music (optional, at 10% volume)
ffmpeg -y -i demo/assets/videos/demo-with-voiceover.mp4 \
       -i demo/assets/audio/background.mp3 \
       -filter_complex "[0:a]volume=1.0[voice];[1:a]volume=0.1,afade=t=out:st=55:d=5[music];[voice][music]amix=inputs=2:duration=first[aout]" \
       -map 0:v -map "[aout]" \
       -c:v copy -c:a aac \
       demo/assets/videos/demo-final.mp4
```

**Subtitle Generation:**

```typescript
// Generate SRT and VTT subtitle files from script timing
function generateSubtitleFiles(subtitles: Subtitle[]): void {
  // SRT format (for video players)
  let srt = '';
  subtitles.forEach((sub, i) => {
    srt += `${i + 1}\n`;
    srt += `${formatSRTTime(sub.start)} --> ${formatSRTTime(sub.end)}\n`;
    srt += `${sub.text}\n\n`;
  });
  fs.writeFileSync('demo/assets/subtitles/demo.srt', srt);
  
  // VTT format (for web)
  let vtt = 'WEBVTT\n\n';
  subtitles.forEach((sub, i) => {
    vtt += `${i + 1}\n`;
    vtt += `${formatVTTTime(sub.start)} --> ${formatVTTTime(sub.end)}\n`;
    vtt += `${sub.text}\n\n`;
  });
  fs.writeFileSync('demo/assets/subtitles/demo.vtt', vtt);
}
```

### 11. Execute Full Demo Pipeline (AUTOMATED)

**This is the critical step - run everything automatically:**

```powershell
# demo/scripts/build-demo.ps1
# Complete demo build pipeline - runs everything in one go

param(
    [string]$ProductName = "AndiSense",
    [string]$Voice = "male",
    [switch]$SkipVoiceover = $false
)

$ErrorActionPreference = "Stop"
$DemoDir = Split-Path -Parent $PSScriptRoot
$FrontendDir = Join-Path (Split-Path -Parent $DemoDir) "frontend"

Write-Host "🎬 Building $ProductName Demo..." -ForegroundColor Cyan

# Step 1: Ensure directories exist
Write-Host "`n📁 Step 1: Creating directories..." -ForegroundColor Yellow
$dirs = @(
    "$DemoDir/assets/screenshots",
    "$DemoDir/assets/video",
    "$DemoDir/assets/audio",
    "$DemoDir/subtitles"
)
foreach ($dir in $dirs) {
    if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
}

# Step 2: Run Playwright capture
Write-Host "`n🎥 Step 2: Recording demo with Playwright..." -ForegroundColor Yellow
Push-Location $FrontendDir
try {
    npx playwright test tests/e2e/demo-capture.spec.ts --reporter=list
    if ($LASTEXITCODE -ne 0) { throw "Playwright recording failed" }
} finally {
    Pop-Location
}

# Step 3: Find and copy video from test-results
Write-Host "`n📦 Step 3: Copying video to demo folder..." -ForegroundColor Yellow
$testResults = Get-ChildItem -Path "$FrontendDir/test-results" -Filter "*.webm" -Recurse | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($testResults) {
    $destVideo = "$DemoDir/assets/video/$($ProductName.ToLower())-demo-raw.webm"
    Copy-Item $testResults.FullName $destVideo -Force
    Write-Host "  ✓ Video copied to: $destVideo" -ForegroundColor Green
} else {
    throw "No video found in test-results!"
}

# Step 4: Generate voiceover (unless skipped)
if (!$SkipVoiceover) {
    Write-Host "`n🎤 Step 4: Generating voiceover..." -ForegroundColor Yellow
    $scriptPath = "$DemoDir/script/demo-script-text-only.txt"
    $audioPath = "$DemoDir/assets/audio/voiceover.wav"
    
    # Try pyttsx3 first (offline)
    python "$DemoDir/scripts/generate_voiceover.py" --voice $Voice
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Voiceover generated: $audioPath" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Voiceover generation failed, continuing without audio" -ForegroundColor Yellow
    }
}

# Step 5: Merge video + audio with FFmpeg
Write-Host "`n🔧 Step 5: Merging video and audio..." -ForegroundColor Yellow
$rawVideo = "$DemoDir/assets/video/$($ProductName.ToLower())-demo-raw.webm"
$audioFile = "$DemoDir/assets/audio/voiceover.wav"
$finalVideo = "$DemoDir/assets/video/$($ProductName.ToLower())-demo-final.mp4"

if ((Test-Path $audioFile) -and !$SkipVoiceover) {
    # Check if FFmpeg is available
    $ffmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue
    if ($ffmpeg) {
        ffmpeg -y -i $rawVideo -i $audioFile `
            -c:v libx264 -preset fast -crf 23 `
            -c:a aac -b:a 128k `
            -map 0:v:0 -map 1:a:0 -shortest `
            $finalVideo
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Final video: $finalVideo" -ForegroundColor Green
        }
    } else {
        Write-Host "  ⚠ FFmpeg not found, copying raw video as final" -ForegroundColor Yellow
        Copy-Item $rawVideo $finalVideo.Replace(".mp4", ".webm") -Force
        $finalVideo = $finalVideo.Replace(".mp4", ".webm")
    }
} else {
    # No audio, just copy raw video
    Copy-Item $rawVideo $finalVideo.Replace(".mp4", ".webm") -Force
    $finalVideo = $finalVideo.Replace(".mp4", ".webm")
    Write-Host "  ✓ Video (no audio): $finalVideo" -ForegroundColor Green
}

# Step 6: Report success
Write-Host "`n✅ Demo build complete!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📹 Final Video: $finalVideo" -ForegroundColor White
Write-Host "📝 Script: $DemoDir/script/demo-script.md" -ForegroundColor White
Write-Host "📸 Screenshots: $DemoDir/assets/screenshots/" -ForegroundColor White
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

# Open the video
Write-Host "`nOpening video..." -ForegroundColor Yellow
Start-Process $finalVideo
```

**After creating all files, the archetype MUST run this script:**

```bash
# Run the complete pipeline
powershell -ExecutionPolicy Bypass -File demo/scripts/build-demo.ps1 -ProductName "AndiSense"
```

**Expected output:**
```
🎬 Building AndiSense Demo...

📁 Step 1: Creating directories...

🎥 Step 2: Recording demo with Playwright...
  Running 1 test using 1 worker
  ✓ Complete Demo Recording (45s)

📦 Step 3: Copying video to demo folder...
  ✓ Video copied to: demo/assets/video/andisense-demo-raw.webm

🎤 Step 4: Generating voiceover...
  Using voice: Microsoft David Desktop
  ✓ Voiceover generated: demo/assets/audio/voiceover.wav

🔧 Step 5: Merging video and audio...
  ✓ Final video: demo/assets/video/andisense-demo-final.mp4

✅ Demo build complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📹 Final Video: demo/assets/video/andisense-demo-final.mp4
📝 Script: demo/script/demo-script.md
📸 Screenshots: demo/assets/screenshots/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Opening video...
```

### 12. EXECUTE THE PIPELINE (DO NOT SKIP)

**CRITICAL: The archetype MUST execute the build script automatically, not just create it and tell the user to run it.**

**WHY:** By running it ourselves, we can:
- ✅ Detect errors immediately
- ✅ Fix issues automatically (empty pages, missing data, auth problems)
- ✅ Retry failed steps
- ✅ Deliver a working video, not instructions

**The archetype MUST use `run_command` to execute the pipeline:**

```
# For Windows users:
run_command: powershell -ExecutionPolicy Bypass -File demo/scripts/run-demo.ps1
Blocking: false
WaitMsBeforeAsync: 5000

# For macOS/Linux users:
run_command: bash demo/scripts/run-demo.sh
Blocking: false
WaitMsBeforeAsync: 5000
```

**If the script doesn't exist yet, run commands directly:**

```
# Step 1: Run Playwright capture
run_command: npx playwright test tests/e2e/demo-*.spec.ts --reporter=list
Cwd: [PROJECT]/frontend
Blocking: true

# Step 2: Copy video (Windows)
run_command: $v = Get-ChildItem -Path test-results -Filter *.webm -Recurse | Select -First 1; Copy-Item $v.FullName ../demo/assets/video/demo.webm
Cwd: [PROJECT]/frontend
Blocking: true

# Step 3: Open video
run_command: Start-Process ../demo/assets/video/demo.webm
Cwd: [PROJECT]/frontend
Blocking: true
```

**If any step fails, the archetype MUST:**
1. Read the error output
2. Diagnose the issue (missing dependency, server not running, empty page, etc.)
3. Attempt to fix it automatically
4. Retry the failed step
5. Only ask the user for help if auto-fix fails

**Example error handling:**
- "Cannot find module playwright" → Run `npm install -D @playwright/test && npx playwright install chromium`
- "ECONNREFUSED localhost:5173" → Tell user to start frontend, or start it automatically
- "No video found" → Check test-results folder, look for errors in Playwright output
- "Empty page detected" → Re-run with different project ID or route

**The user should NOT have to run any commands. The final message should be:**
```
✅ Demo Complete!

📹 Video playing: demo/assets/video/andisense-demo.webm

The demo has been recorded and is now open. No further action needed.
```

### 13. Generate README

Create a quick reference for the demo package:

```markdown
# [PRODUCT_NAME] Demo Package

Generated: [DATE]  
Duration: [DURATION]  
Scenes: [SCENE_COUNT]

## Quick Start

1. **View Script:** Open `script/demo-script.md`
2. **Preview Assets:** Browse `assets/` folder
3. **Re-capture:** Run `npx playwright test demo/captures/`

## Contents

```
demo/
├── assets/
│   ├── screenshots/     # [X] PNG files
│   └── videos/          # [X] WebM clips
├── captures/
│   └── demo-capture.spec.ts
├── script/
│   └── demo-script.md
├── demo-manifest.yaml
└── README.md
```

✅ Demo Package Generated

📦 Demo: [PRODUCT_NAME] Demo
   Duration: [DURATION] (target: [TARGET])
   Audience: [AUDIENCE]
   Scenes: [SCENE_COUNT]

📸 Assets Captured:
   ✓ Screenshots: [X] files ([SIZE] total)
   ✓ Videos: [X] files ([SIZE] total)
   ✓ Output: demo/

📝 Script Generated:
   ✓ demo/script/demo-script.md
   ✓ Word count: [X] words
   ✓ Estimated read time: [X] minutes

🎨 AT&T Branding Applied:
   ✓ Highlight color: #009FDB (AT&T Blue)
   ✓ Annotation style: Rounded with shadow
   ✓ Consistent styling across scenes

📂 Output Structure:
   demo/
   ├── assets/screenshots/    [X] files
   ├── assets/videos/         [X] files
   ├── captures/              Playwright scripts
   ├── script/                Voiceover script
   ├── demo-manifest.yaml     Configuration
   └── README.md              Quick reference

📋 Demo is READY - No Manual Steps Required!
   The video has been recorded, voiceover generated, and merged automatically.
   Just open the final video and share it!

💡 Optional Commands (if you want to customize):
   - Re-record: /refactor-demo
   - Different audience: /scaffold-demo --audience executive
   - Export to PPT: /scaffold-ppt --from-demo demo/
   - Validate quality: /test-demo
```

## Error Handling

**App Not Running**: Report that application must be running, provide start command.

**Playwright Not Installed**: Provide installation command: `npm install -D @playwright/test && npx playwright install chromium`

**Capture Failed**: Report specific scene that failed, suggest checking selectors or wait conditions.

**Authentication Required**: Detect login redirect, prompt for credentials or suggest adding login to beforeEach.

**Element Not Found**: Report missing selector, suggest using Playwright Inspector: `npx playwright codegen [URL]`

## Intelligent Recovery Strategies

### Empty Page Detection & Recovery

When a page shows no data, the archetype should:

1. **Detect Empty State**:
   ```typescript
   const emptyIndicators = [
     'text="No data"', 'text="No results"', 'text="No items"',
     'text="Nothing to show"', 'text="Get started"', 
     'text="Create your first"', '[data-testid="empty-state"]',
     '.empty-state', 'text="No requirements"', 'text="No process flows"'
   ];
   ```

2. **Auto-Recovery Actions**:
   - **Add project context**: `/requirements` → `/projects/{id}/requirements`
   - **Add query params**: `/process-flows` → `/process-flows?project_id={id}`
   - **Navigate from parent**: Go to `/projects`, click first project, then navigate to feature
   - **Use API discovery**: Query `/api/v1/projects` to find valid IDs

3. **Fallback Scenes**:
   - If requirements page empty → Show projects list instead
   - If detail page 404s → Show list page with data
   - If feature unavailable → Skip scene and note in report

### Data-Dependent Route Mapping

Common patterns to handle:

| Route Pattern | Requires | Recovery Strategy |
|---------------|----------|-------------------|
| `/requirements` | project_id | Add `?project_id={id}` or navigate via project |
| `/process-flows` | project_id | Add `?project_id={id}` or navigate via project |
| `/projects/:id/*` | valid project ID | Discover ID from `/projects` list |
| `/documents` | project_id | Add `?project_id={id}` |
| `/matrices` | project_id | Navigate from project detail |

### Pre-Capture Checklist

Before capturing each scene, verify:

- [ ] Page loaded successfully (no 404, 500)
- [ ] Not redirected to login
- [ ] Main content area has data (not empty state)
- [ ] No loading spinners visible
- [ ] Required elements exist for highlights

### Voice Generation Fallbacks

If primary TTS fails:

1. **pyttsx3** (offline) → Works without internet
2. **edge-tts** (online) → Better quality, needs network
3. **Manual recording** → Prompt user to record voiceover

### FFmpeg Not Available

If FFmpeg not installed:
- Provide installation command: `winget install FFmpeg`
- Output video without audio merge
- Generate separate audio file for manual merge

## Examples

**Example 1**: `/scaffold-demo Create 3-minute demo for AndiSense targeting business analysts. Features: dashboard metrics, project creation, AI document processing, requirements matrix. Voice: male`

Output: 8-scene demo with screenshots of dashboard and matrix, videos of project creation and document upload flows. Uses Microsoft David voice for narration.

**Example 2**: `/scaffold-demo Generate quick 1-minute executive demo for DataPlatform. Focus on: ROI dashboard, cost savings metrics. Voice: female, Include audio: both`

Output: 4-scene demo focused on high-level metrics with minimal interaction, optimized for executive attention span. Uses Microsoft Zira voice with subtle background music.

**Example 3**: `/scaffold-demo Create technical demo from existing E2E tests in tests/e2e/. Duration: 5 minutes. Subtitles: burned-in`

Output: Analyzes existing tests, extracts demo-worthy flows, generates comprehensive technical walkthrough with subtitles burned into video.

**Example 4**: `/scaffold-demo AndiSense demo, 1 minute, show dashboard, process flows, requirements`

Output with intelligent data discovery:
```
🔍 Pre-Capture Data Discovery:
   ✓ Found 3 projects
   ✓ Selected project "AndiSense MVP" (has 64 requirements, 16 flows)
   ✓ Will use project_id=proj_001 for data-dependent pages

📋 Scene Plan (auto-corrected):
   Scene 1: Dashboard → /dashboard (global, no project needed)
   Scene 2: Process Flows → /process-flows?project_id=proj_001 (corrected)
   Scene 3: Requirements → /projects/proj_001/requirements (corrected)
   Scene 4: Closing → /dashboard

🎬 Capturing with validation...
   ✓ Scene 1: Dashboard - 245 KB, has data
   ✓ Scene 2: Process Flows - 189 KB, has data (16 flows visible)
   ✓ Scene 3: Requirements - 156 KB, has data (64 requirements visible)
   ✓ Scene 4: Closing - 267 KB, OK

🎤 Generating voiceover (male voice)...
   ✓ Using: Microsoft David Desktop
   ✓ Audio: 48 seconds

📦 Final Output:
   ✓ demo/assets/videos/andisense-demo-with-voiceover.mp4 (1.9 MB)
   ✓ demo/assets/subtitles/demo.srt
   ✓ demo/assets/subtitles/demo.vtt
```

## Additional Smart Features

### 1. Interaction Demonstrations (Not Just Screenshots)

For technical and business demos, show actual interactions:

```typescript
// Demonstrate a feature with real interaction
async function demonstrateInteraction(page: Page, interaction: DemoInteraction) {
  switch (interaction.type) {
    case 'create':
      // Show creating a new item
      await page.click('[data-testid="create-button"], button:has-text("Create"), button:has-text("New")');
      await page.waitForTimeout(500);
      // Fill form with demo data
      await fillDemoForm(page, interaction.formData);
      await page.click('button[type="submit"], button:has-text("Save")');
      await page.waitForTimeout(1000);
      break;
      
    case 'search':
      // Demonstrate search functionality
      await page.fill('input[type="search"], input[placeholder*="Search"]', interaction.searchTerm);
      await page.waitForTimeout(1500); // Show results appearing
      break;
      
    case 'filter':
      // Show filtering
      await page.click('[data-testid="filter-button"], button:has-text("Filter")');
      await page.waitForTimeout(500);
      await page.click(`text="${interaction.filterValue}"`);
      await page.waitForTimeout(1000);
      break;
      
    case 'expand':
      // Expand a detail view
      await page.click('[data-testid="expand"], [aria-expanded="false"]');
      await page.waitForTimeout(800);
      break;
  }
}
```

### 2. Smart Script Generation Based on Content

Generate contextual voiceover based on what's actually on screen:

```typescript
async function generateContextualScript(page: Page, feature: DiscoveredFeature): Promise<string> {
  // Count items on page
  const itemCount = await page.locator('table tbody tr, [data-testid="card"], .list-item').count();
  
  // Detect metrics/stats
  const stats = await page.locator('[data-testid="stat"], .stat-card, .metric').allTextContents();
  
  // Generate script based on actual content
  let script = `Here we see the ${feature.name} page. `;
  
  if (itemCount > 0) {
    script += `The system currently tracks ${itemCount} ${feature.name.toLowerCase()}. `;
  }
  
  if (stats.length > 0) {
    script += `Key metrics show ${stats.slice(0, 2).join(' and ')}. `;
  }
  
  return script;
}
```

### 3. Automatic Highlight Detection

Find the most important elements to highlight:

```typescript
async function findHighlightTargets(page: Page): Promise<string[]> {
  const targets: string[] = [];
  
  // Priority 1: Stats/metrics cards
  if (await page.locator('.stat-card, [data-testid="metric"]').count() > 0) {
    targets.push('.stat-card, [data-testid="metric"]');
  }
  
  // Priority 2: Primary action buttons
  if (await page.locator('button.primary, button[data-variant="primary"]').count() > 0) {
    targets.push('button.primary');
  }
  
  // Priority 3: Data tables
  if (await page.locator('table').count() > 0) {
    targets.push('table');
  }
  
  // Priority 4: Charts/visualizations
  if (await page.locator('canvas, svg.chart, [data-testid="chart"]').count() > 0) {
    targets.push('canvas, svg.chart');
  }
  
  return targets;
}
```

### 4. Demo Versioning & Comparison

Track demo versions and compare changes:

```yaml
# demo/demo-manifest.yaml
versioning:
  current: "1.2.0"
  previous: "1.1.0"
  changelog:
    - version: "1.2.0"
      date: "2025-12-05"
      changes:
        - "Added new Requirements Matrix scene"
        - "Updated dashboard metrics"
        - "Improved voiceover clarity"
    - version: "1.1.0"
      date: "2025-11-20"
      changes:
        - "Initial demo release"
```

### 5. Multi-Language Support

Generate demos in multiple languages:

```typescript
const SCRIPT_TEMPLATES = {
  en: {
    welcome: "Welcome to {product}, {company}'s {description}.",
    dashboard: "The dashboard provides real-time visibility into your {domain}.",
    closing: "Contact your team lead to get started today.",
  },
  es: {
    welcome: "Bienvenido a {product}, {description} de {company}.",
    dashboard: "El panel proporciona visibilidad en tiempo real de su {domain}.",
    closing: "Contacte a su líder de equipo para comenzar hoy.",
  },
};
```

### 6. Accessibility Compliance

Ensure demos are accessible:

```typescript
async function checkAccessibility(page: Page): Promise<AccessibilityReport> {
  // Check color contrast in screenshots
  // Verify subtitle readability
  // Ensure audio has captions
  // Check video doesn't rely solely on color
  
  return {
    hasSubtitles: true,
    hasAudioDescription: false, // Future enhancement
    colorContrastPasses: true,
    subtitleFileFormats: ['srt', 'vtt'],
  };
}
```

### 7. Demo Analytics Preparation

Add tracking markers for analytics:

```typescript
// Add chapter markers for video analytics
const chapters = scenes.map((scene, i) => ({
  time: scene.timing.start,
  title: scene.title,
  marker: `chapter-${i + 1}`,
}));

// Generate YouTube-compatible chapter list
const youtubeChapters = chapters.map(c => `${c.time} ${c.title}`).join('\n');
```

### 8. Export Formats

Support multiple output formats:

```yaml
output:
  formats:
    - type: "mp4"
      use: "sharing, embedding"
    - type: "gif"
      use: "documentation, chat"
      scenes: [1, 2]  # Only first 2 scenes
    - type: "pptx"
      use: "presentations"
      command: "/scaffold-ppt --from-demo"
    - type: "html"
      use: "web embedding"
      includes_player: true
```

### 9. Thumbnail Generation

Auto-generate thumbnails for video:

```typescript
// Generate thumbnail from best frame
async function generateThumbnail(videoPath: string): Promise<string> {
  // Extract frame at 10% into video (usually shows main content)
  const thumbnailPath = videoPath.replace('.mp4', '-thumbnail.png');
  
  // FFmpeg command to extract frame
  // ffmpeg -i video.mp4 -ss 00:00:05 -vframes 1 thumbnail.png
  
  return thumbnailPath;
}
```

### 10. Demo Health Check

Validate demo before finalizing:

```typescript
interface DemoHealthCheck {
  videoExists: boolean;
  videoPlayable: boolean;
  audioSynced: boolean;
  subtitlesValid: boolean;
  allScenesHaveData: boolean;
  noEmptyStates: boolean;
  brandingConsistent: boolean;
  durationWithinTarget: boolean;
}

async function runHealthCheck(demoPath: string): Promise<DemoHealthCheck> {
  // Comprehensive validation before delivery
}
```

---

## Final Output & User Accessibility

### CRITICAL: Final Video Location

**Every demo workflow execution MUST end with:**

1. **Clear path to the final video**
2. **Command to open the video**
3. **Summary of what was created**

### Completion Report Template

```
══════════════════════════════════════════════════════════════════
  🎬 DEMO GENERATION COMPLETE
══════════════════════════════════════════════════════════════════

  📹 FINAL VIDEO:
     demo/assets/video/final/[product]-demo-final.mp4
     
  ▶️  TO VIEW NOW:
     Windows:  start demo\assets\video\final\[product]-demo-final.mp4
     macOS:    open demo/assets/video/final/[product]-demo-final.mp4
     Linux:    xdg-open demo/assets/video/final/[product]-demo-final.mp4

══════════════════════════════════════════════════════════════════

  📊 DEMO SUMMARY:
     Duration:    [X] minutes [Y] seconds
     Scenes:      [N] scenes
     Audience:    [technical/business/executive/general]
     Voice:       [voice name]
     Resolution:  1920x1080

  🎯 EFFECTS APPLIED:
     Zoom:        [N] scenes with zoom effects
     Transitions: [type] transitions between scenes
     Subtitles:   Burned-in + SRT/VTT files

══════════════════════════════════════════════════════════════════

  📁 ALL GENERATED FILES:

  demo/
  ├── assets/video/final/
  │   ├── [product]-demo-final.mp4      ← MAIN OUTPUT
  │   └── [product]-demo-no-audio.mp4
  ├── assets/audio/voiceover/
  │   └── full-narration.mp3
  ├── assets/subtitles/
  │   ├── demo-subtitles.srt
  │   └── demo-subtitles.vtt
  ├── frames/                            ← Editable scene configs
  └── manifest.yaml                      ← Master configuration

══════════════════════════════════════════════════════════════════

  💡 NEXT STEPS:

  1. WATCH THE DEMO:
     Open the video file listed above to review the demo.

  2. MAKE ADJUSTMENTS (if needed):
     /refactor-demo [describe changes]

  3. VALIDATE QUALITY:
     /test-demo

  4. GENERATE DOCUMENTATION:
     /document-demo

══════════════════════════════════════════════════════════════════
```

### Auto-Open Final Video

**After successful generation, automatically open the video:**

```python
import subprocess
import platform
import os

def open_final_video(video_path: str):
    """Cross-platform video opener."""
    if not os.path.exists(video_path):
        print(f"❌ Video not found: {video_path}")
        return False
    
    system = platform.system()
    try:
        if system == 'Windows':
            os.startfile(video_path)
        elif system == 'Darwin':  # macOS
            subprocess.run(['open', video_path])
        else:  # Linux
            subprocess.run(['xdg-open', video_path])
        
        print(f"✅ Opened: {video_path}")
        return True
    except Exception as e:
        print(f"⚠️ Could not auto-open video: {e}")
        print(f"📍 Video location: {video_path}")
        return False

# Always open the final video after generation
final_video = "demo/assets/video/final/andisense-demo-final.mp4"
open_final_video(final_video)
```

### Quick Access Methods

**For users who want quick access:**

1. **PowerShell (Windows):**
   ```powershell
   # Run demo pipeline and open result
   cd demo/scripts
   .\run-demo.ps1
   # Video opens automatically when complete
   ```

2. **npm (Cross-platform):**
   ```bash
   cd demo
   npm run build
   # Video opens automatically when complete
   ```

3. **Direct Video Path:**
   ```
   demo/assets/video/final/[product]-demo-final.mp4
   ```

4. **Environment Variable (for CI/CD):**
   ```bash
   export DEMO_VIDEO_PATH="demo/assets/video/final/[product]-demo-final.mp4"
   ```

### Integration with File Explorer/Finder

The demo pipeline creates a `OPEN_DEMO_VIDEO.cmd` (Windows) or `open-demo-video.sh` (macOS/Linux) in the demo root for one-click access:

**Windows (OPEN_DEMO_VIDEO.cmd):**
```batch
@echo off
start "" "%~dp0assets\video\final\andisense-demo-final.mp4"
```

**macOS/Linux (open-demo-video.sh):**
```bash
#!/bin/bash
open "$(dirname "$0")/assets/video/final/andisense-demo-final.mp4" 2>/dev/null || \
xdg-open "$(dirname "$0")/assets/video/final/andisense-demo-final.mp4"
```

---

## ⚠️ MANDATORY EXECUTION STEPS

**This section is NOT optional. After creating all files, you MUST execute the demo pipeline.**

The workflow is NOT complete until the final video exists and has been opened for the user.

### Step 1: Create Demo Files (Scaffolding)

Create all demo files:
- `demo/manifest.yaml`
- `demo/script/DEMO_SCRIPT.md`
- `demo/captures/demo-capture.spec.ts`
- `demo/assets/subtitles/*.srt`, `*.vtt`
- `demo/scripts/generate-voiceover.py`
- `demo/scripts/merge-video.py`
- `demo/scripts/run-demo.ps1` (or `run-demo.sh`)
- `demo/frames/scene-*/frame.yaml`
- `demo/README.md`
- `demo/docs/*.md`

### Step 2: Check Prerequisites

Before executing, verify the application is running:

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:5173/
```

If not 200, prompt user to start the application first.

### Step 3: Install Python Dependencies (if needed)

```bash
pip install pyttsx3 moviepy --quiet
```

### Step 4: EXECUTE THE PIPELINE (CRITICAL)

**You MUST run this command. Do NOT skip this step.**

**Windows:**
```powershell
cd demo/scripts; .\run-demo.ps1
```

**macOS/Linux:**
```bash
cd demo/scripts && chmod +x run-demo.sh && ./run-demo.sh
```

**Wait for completion.** This typically takes 2-5 minutes depending on demo length.

### Step 5: Verify Output Exists

After the pipeline completes, verify the final video exists:

```bash
ls -la demo/assets/video/final/*.mp4
```

If no `.mp4` file exists, the pipeline failed. Check errors and retry.

### Step 6: Open Final Video for User

**Windows:**
```powershell
Start-Process "demo\assets\video\final\andisense-demo-final.mp4"
```

**macOS:**
```bash
open demo/assets/video/final/andisense-demo-final.mp4
```

### Step 7: Report Completion

After the video opens, provide completion report:

```
═══════════════════════════════════════════════════════════
✅ DEMO GENERATION COMPLETE
═══════════════════════════════════════════════════════════

📹 Final Video: demo/assets/video/final/andisense-demo-final.mp4
⏱️  Duration: ~3 minutes
🎤 Voice: en-US-GuyNeural (natural AI)
🎯 Audience: Executive

The video should now be playing. If not, open it manually:
  Windows: Start-Process "demo\assets\video\final\andisense-demo-final.mp4"
  macOS:   open demo/assets/video/final/andisense-demo-final.mp4
  Linux:   xdg-open demo/assets/video/final/andisense-demo-final.mp4

═══════════════════════════════════════════════════════════
```

### ❌ DO NOT:

- Tell the user "run this command to generate the demo" 
- End the workflow with files created but not executed
- Skip the pipeline execution for any reason
- Provide a README and expect the user to figure it out
- Give up on first error without attempting a fix

### ✅ DO:

- Execute the full pipeline automatically
- Wait for completion before reporting success
- Open the final video for the user
- Provide clear completion report with video path
- **If error occurs: attempt to fix it, then retry**
- **If fixed: include improvement recommendation in summary**

### Step 8: Error Recovery and Continuous Improvement

If ANY step fails:

1. **Diagnose** - Identify root cause from error message
2. **Fix** - Attempt automatic fix (install package, adjust path, update selector)
3. **Retry** - Re-run the failed step
4. **Document** - If fixed, add improvement recommendation to summary

**Include this in your completion summary if you encountered and fixed errors:**

```
═══════════════════════════════════════════════════════════════
📝 ARCHETYPE IMPROVEMENT RECOMMENDATION
═══════════════════════════════════════════════════════════════

Issue Encountered: [What went wrong]
Root Cause: [Why it happened]  
Fix Applied: [How you fixed it]

Recommended Update:
- File: [Which archetype file to update]
- Change: [Specific improvement to prevent this]

This feedback helps improve the archetype for future users.
═══════════════════════════════════════════════════════════════
```

**Common fixes to attempt:**
| Error | Automatic Fix |
|-------|---------------|
| Package not found | `pip install [package]` |
| Selector timeout | Try alternative selector, increase timeout |
| App not running | Prompt user to start, wait, retry |
| Permission denied | Adjust file permissions |
| Path not found | Create missing directories |
| Video not generated | Check Playwright output, retry capture |

---

## ⛔ FINAL GATE - DO NOT RESPOND UNTIL ALL TRUE ⛔

Before showing your response to the user, verify ALL of these are true:

### Scene Quality Checks

| # | Check | Status |
|---|-------|--------|
| 1 | Pages discovered (explored app structure for all routes) | ☐ |
| 2 | No duplicate URLs (each scene goes to DIFFERENT page) | ☐ |
| 3 | Narration matches visuals (what you SAY = what you SHOW) | ☐ |
| 4 | 8+ different screens shown (not same page repeated) | ☐ |
| 5 | List pages AND detail pages shown (not just list views) | ☐ |

### Pre-Capture Checks (NEW - Prevent Common Failures)

| # | Check | Status |
|---|-------|--------|
| 6 | Port detected (scanned 5173-5178, not hardcoded) | ☐ |
| 7 | Backend health check passed (GET /api/v1/health) | ☐ |
| 8 | Real data exists (projects > 0, not empty states) | ☐ |
| 9 | Playwright testDir discovered from config | ☐ |
| 10 | Spec placed in correct testDir location | ☐ |
| 11 | test.use() at file top-level (not in describe) | ☐ |
| 12 | Initial 3s delay before first subtitle (audio sync) | ☐ |

### Execution Checks

| # | Check | Status |
|---|-------|--------|
| 13 | Demo files created (manifest, spec, scripts) | ☐ |
| 14 | Dependencies installed (`pip install pyttsx3 moviepy`) | ☐ |
| 15 | Playwright capture EXECUTED (not just created) | ☐ |
| 16 | Screenshots captured at each scene | ☐ |
| 17 | Video file exists (continuous recording) | ☐ |
| 18 | Voiceover generated (narration.mp3 exists) | ☐ |
| 19 | Video + audio merged (MoviePy 2.x syntax) | ☐ |
| 20 | Final video OPENED with Start-Process/open command | ☐ |
| 21 | Completion report shown with exact video path | ☐ |

**If ANY box is unchecked, GO BACK AND COMPLETE IT before responding.**

**Your response should end with a completion report like this:**
```
═══════════════════════════════════════════════════════════════
✅ DEMO GENERATION COMPLETE
═══════════════════════════════════════════════════════════════

📹 Final Video: demo/assets/video/final/[product]-demo-final.mp4
⏱️  Duration: [X] minutes
🎤 Voice: pyttsx3 (Microsoft David)
🎯 Audience: [audience type]

The video should now be playing on your screen.
═══════════════════════════════════════════════════════════════
```

**NOT with "How to Run" instructions. The video must already be playing.**

---

## References

- Constitution: (pre-loaded above)
- Environment: `${ARCHETYPES_BASEDIR}/demo-producer/templates/env-config.yaml`
- Related: `/test-demo`, `/refactor-demo`, `/document-demo`
- Integration: `/scaffold-app`, `/test-app`, `/scaffold-ppt`
